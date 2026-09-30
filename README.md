# PETS3 备考仓库

零基础备考「上海市继续教育外语水平考试」（难度对标全国 PETS-3，用于专升本学位证书）的学习资料与工具集。

## 文件结构

```
├── PETS3-学习计划.md          # 12 周备考总计划（每日 3-4 小时）
├── PETS3-词汇表.txt           # 大纲词汇 4017 条（Tab 分隔，Anki 可直接导入）
├── 词表导入Anki指南.md         # 词表导入 Anki 并同步手机的逐步操作手册
└── scripts/
    └── extract_pets3_vocabulary.py   # 从大纲 PDF 提取词表的脚本（PyMuPDF）
```

## 快速开始

1. 阅读 `PETS3-学习计划.md` 了解整体路线
2. 按 `词表导入Anki指南.md` 把词表装进 Anki（电脑+手机同步）
3. 每天 40 个新词 + 清空到期复习

## 词表来源

从本地 `全国英语等级考试第三级 大纲词汇.pdf` 提取，脚本位于 `scripts/`，依赖 Python 3 + PyMuPDF：

```bash
pip3 install PyMuPDF
python3 scripts/extract_pets3_vocabulary.py
```
