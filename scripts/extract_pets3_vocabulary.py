#!/usr/bin/env python3
"""从 PETS3 大纲词汇 PDF 提取词表，生成 Anki 可导入的制表符分隔文件。

用法: python3 extract_pets3_vocabulary.py
输入: /Users/zuokp/data/PETS-3/备考资料/全国英语等级考试第三级 大纲词汇.pdf
输出: ../PETS3-词汇表.txt (Tab 分隔: 单词<Tab>词性+释义)
"""
import re
from pathlib import Path

import fitz  # PyMuPDF

PDF_PATH = Path("/Users/zuokp/data/PETS-3/备考资料/全国英语等级考试第三级 大纲词汇.pdf")
OUT_PATH = Path(__file__).resolve().parent.parent / "PETS3-词汇表.txt"

# 过滤规则：公众号水印行、单字母索引行（A/B/C...）、纯数字页码
AD_RE = re.compile(r"^关注公众号")
INDEX_RE = re.compile(r"^[A-Z]$")
PAGE_RE = re.compile(r"^\d+$")
# 词条行：非空白开头 + 空白 + 释义剩余部分
ENTRY_RE = re.compile(r"^(\S+)\s+(.+)$")
# 词性标记（用于跨行词条合并判断、括号后紧贴词性的修复）
POS_TAGS = (
    "n\\.|v\\.|adj\\.|adv\\.|prep\\.|conj\\.|pron\\.|art\\.|num\\.|"
    "interj\\.|int\\.|aux\\.|vt\\.|vi\\.|abbr\\."
)
POS_START_RE = re.compile(rf"^(?:{POS_TAGS})")
BARE_WORD_RE = re.compile(r"^[A-Za-z][A-Za-z'\-]*$")
# 修复 "refrigerator(=fridge)n.冰箱" 这类括号后无空格的行
PAREN_FIX_RE = re.compile(rf"(\))({POS_TAGS})")


def extract_lines(pdf_path: Path) -> list:
    """逐页提取并清洗出词条行，合并跨行词条、修复紧贴词性。"""
    doc = fitz.open(pdf_path)
    raw = []
    for page in doc:
        for line in page.get_text().split("\n"):
            line = PAREN_FIX_RE.sub(r"\1 \2", line).strip()
            if not line or AD_RE.match(line) or INDEX_RE.match(line) or PAGE_RE.match(line):
                continue
            raw.append(line)
    doc.close()

    # 纯单词行 + 下一行以词性开头 → 合并为一条（如 "hello" / "interj.喂；你好"）
    merged = []
    i = 0
    while i < len(raw):
        cur = raw[i]
        nxt = raw[i + 1] if i + 1 < len(raw) else ""
        if BARE_WORD_RE.match(cur) and POS_START_RE.match(nxt):
            merged.append(f"{cur} {nxt}")
            i += 2
        else:
            merged.append(cur)
            i += 1
    return merged


def parse_entries(lines: list) -> list:
    """把每行拆成 (单词, 释义) 二元组，解析失败的行收集起来人工复核。"""
    entries, skipped = [], []
    for line in lines:
        m = ENTRY_RE.match(line)
        if m and re.match(r"^[A-Za-z]", m.group(1)):
            entries.append((m.group(1), m.group(2)))
        else:
            skipped.append(line)
    return entries, skipped


def main() -> None:
    lines = extract_lines(PDF_PATH)
    entries, skipped = parse_entries(lines)

    # 词表中唯一含空格的词条 "according to" 会被拆开，单独合并回来
    fixed = []
    for word, defn in entries:
        if word == "according" and defn.startswith("to "):
            fixed.append(("according to", defn[3:]))
        else:
            fixed.append((word, defn))

    with OUT_PATH.open("w", encoding="utf-8-sig") as f:
        for word, defn in fixed:
            f.write(f"{word}\t{defn}\n")

    print(f"词条数: {len(fixed)}, 输出: {OUT_PATH}")
    if skipped:
        print(f"跳过 {len(skipped)} 行（需人工复核）:")
        for s in skipped[:20]:
            print("  ", s)


if __name__ == "__main__":
    main()
