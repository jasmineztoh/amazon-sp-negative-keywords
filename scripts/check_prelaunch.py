"""检查投前否词表是否误带商品大词，或漏合并重复词根。仅用 Python 标准库。"""

import argparse
import posixpath
import re
import sys
from collections import defaultdict
from xml.etree import ElementTree as ET
from zipfile import ZipFile


MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
OFFICE_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PACKAGE_REL = "http://schemas.openxmlformats.org/package/2006/relationships"
NS = {"m": MAIN}
SKIP = {"a", "an", "and", "for", "in", "of", "on", "the", "to", "with"}


def words(value):
    return re.findall(r"[a-z0-9]+", value.lower())


def stem(word):
    if len(word) > 4 and word.endswith("ies"):
        return word[:-3] + "y"
    if len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word


def cell_text(cell, shared):
    kind = cell.get("t")
    if kind == "inlineStr":
        inline = cell.find("m:is", NS)
        return "" if inline is None else "".join(inline.itertext())
    value = cell.find("m:v", NS)
    if value is None or value.text is None:
        return ""
    if kind == "s":
        return shared[int(value.text)]
    return value.text


def read_terms(book_path):
    with ZipFile(book_path) as archive:
        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        sheets = workbook.find("m:sheets", NS)
        target_sheet = next((s for s in sheets if s.get("name") == "否词表"), None)
        if target_sheet is None:
            raise ValueError("缺少工作表：否词表")
        rel_id = target_sheet.get(f"{{{OFFICE_REL}}}id")
        rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        relation = next((r for r in rels.findall(f"{{{PACKAGE_REL}}}Relationship") if r.get("Id") == rel_id), None)
        if relation is None:
            raise ValueError("无法定位否词表")
        target = relation.get("Target")
        sheet_path = target.lstrip("/") if target.startswith("/") else posixpath.normpath(posixpath.join("xl", target))
        sheet = ET.fromstring(archive.read(sheet_path))
        shared = []
        if "xl/sharedStrings.xml" in archive.namelist():
            strings = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            shared = ["".join(item.itertext()) for item in strings.findall("m:si", NS)]
        result = []
        for row in sheet.findall(".//m:sheetData/m:row", NS):
            number = int(row.get("r"))
            if number < 3:
                continue
            cell = next((c for c in row.findall("m:c", NS) if re.fullmatch(r"B[0-9]+", c.get("r", ""))), None)
            if cell is None:
                continue
            value = cell_text(cell, shared).strip()
            if number == 3 and value != "前置否词":
                raise ValueError("B3 应为“前置否词”")
            if number >= 4 and value:
                result.append((number, value))
        return result


def contains(tokens, phrase):
    size = len(phrase)
    return any(tokens[i:i + size] == phrase for i in range(len(tokens) - size + 1))


def main():
    parser = argparse.ArgumentParser(description="检查投前否词是否包含商品大词，以及是否漏合并重复词根")
    parser.add_argument("workbook", help="已导出的 Excel 否词表")
    parser.add_argument("--core", nargs="+", required=True, help="商品大词，如 light solar spotlight；会检查常见单复数")
    parser.add_argument("--keep-shared", nargs="*", default=[], help="经人工判断不能单独否定、需保留完整组合的重复词根")
    args = parser.parse_args()

    core = [[stem(token) for token in words(item)] for item in args.core]
    keep = {stem(token) for item in args.keep_shared for token in words(item)}
    if not all(core):
        parser.error("商品大词不能为空")
    terms = read_terms(args.workbook)
    blocked = []
    seen = defaultdict(list)
    for number, term in terms:
        tokens = [stem(token) for token in words(term)]
        if any(contains(tokens, item) for item in core):
            blocked.append((number, term))
        for token in set(tokens) - SKIP - keep:
            if len(token) > 2 and not any(token in item for item in core):
                seen[token].append(number)
    repeated = {token: numbers for token, numbers in seen.items() if len(numbers) >= 3}

    if blocked:
        print("FAIL CORE_WORD: remove product words, then assess the remaining modifier:")
        for number, term in blocked[:20]:
            print(f"  row {number}: {term}")
        if len(blocked) > 20:
            print(f"  and {len(blocked) - 20} more rows")
    if repeated:
        print("FAIL REPEATED_ROOT: combine repeated roots or acknowledge an unsafe root with --keep-shared:")
        for token, numbers in sorted(repeated.items(), key=lambda pair: (-len(pair[1]), pair[0])):
            print(f"  {token}: rows {', '.join(map(str, numbers))}")
    if blocked or repeated:
        return 1
    print(f"PASS: {len(terms)} negative keywords; no protected words or unchecked repeated roots.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, KeyError, ValueError, ET.ParseError) as error:
        print(f"检查失败：{error}", file=sys.stderr)
        sys.exit(2)
