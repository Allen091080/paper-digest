# paper-digest 📄

> 学术论文精读助手技能 — 输入 arXiv 链接或 PDF，输出结构化中文精读报告：核心问题、方法、结论、局限性、引用价值评分。

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/Allen091080/paper-digest/releases/tag/v1.0.0)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey)](.)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-green)](https://skills.sh)

---

## ✨ 功能特性

- 🔗 **arXiv 直读** — 粘贴链接，自动拉取元数据和摘要
- 📄 **PDF 支持** — 读取本地 PDF，提取正文内容
- 📋 **结构化输出** — 7个维度的标准精读格式
- ⭐ **价值评分** — 自动评估引用价值（1-10分）
- 📚 **批量处理** — 一次处理多篇论文
- 📎 **BibTeX 生成** — 自动生成引用格式
- 🌏 **中文友好** — 输出语言支持中文/英文

## 📋 需求

| 依赖 | 用途 | 安装 |
|------|------|------|
| Python 3.10+ | 运行环境 | 内置 |
| pdfplumber | 读取 PDF | `pip3 install pdfplumber`（本地PDF需要）|
| 网络访问 | arXiv 链接 | 内置 urllib |

## 🚀 安装

```bash
npx skills add https://github.com/Allen091080/paper-digest -g -y
```

## 📖 使用示例

### 解读 arXiv 论文

```bash
python3 scripts/digest.py --arxiv "https://arxiv.org/abs/2303.08774" --lang zh
```

输出示例：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📄 论文精读报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 【论文信息】
   标题：GPT-4 Technical Report
   作者：OpenAI等
   发表：2023-03-15
   链接：https://arxiv.org/abs/2303.08774

❓ 【核心问题】
   如何构建在专业和学术基准上接近人类水平的大型多模态模型？

💡 【主要贡献】
   1. 发布 GPT-4，支持文本与图像输入
   2. 在 Bar 考试等专业测试达到前 10% 水平
   3. 提出可预测扩展（predictable scaling）方法论

🔬 【方法概述】
   在大规模数据集上预训练 Transformer 架构，
   通过 RLHF 进行对齐，加入视觉编码器支持图像输入...

📊 【关键结果】
   · achieve state-of-the-art performance on various benchmarks
   · outperform GPT-3.5 significantly across professional exams

⚠️  【局限性与不足】
   · 仍存在幻觉问题，知识截止于 2021 年

⭐ 【引用价值评分】
   9/10 — 必读，领域内里程碑
   适合：所有相关研究者

📎 【引用格式（BibTeX）】
   @article{openai2023gpt,
     title  = {GPT-4 Technical Report},
     author = {OpenAI},
     year   = {2023},
     url    = {https://arxiv.org/abs/2303.08774}
   }
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 快速模式（只看核心）

```bash
python3 scripts/digest.py --arxiv "https://arxiv.org/abs/2303.08774" --quick
```

### 解读本地 PDF

```bash
pip3 install pdfplumber
python3 scripts/digest.py --pdf ~/papers/attention_is_all_you_need.pdf --save ~/notes/transformer_digest.md
# ✅ 已保存：~/notes/transformer_digest.md
```

### 批量处理多篇论文

```bash
# 创建 URL 列表文件
cat > arxiv_list.txt << EOF
https://arxiv.org/abs/2303.08774
https://arxiv.org/abs/1706.03762
https://arxiv.org/abs/2005.14165
EOF

python3 scripts/digest.py --arxiv-list arxiv_list.txt --output ~/notes/digests/
# [1/3] 处理：https://arxiv.org/abs/2303.08774
#    ✅ 保存：~/notes/digests/2303.08774_digest.md
# ...
```

### 生成 BibTeX 引用

```bash
python3 scripts/digest.py --arxiv "https://arxiv.org/abs/1706.03762" --cite bibtex
```

## 💬 与 AI Agent 对话

```
帮我看一下这篇论文 https://arxiv.org/abs/2303.08774
→ 输出完整结构化精读报告

快速告诉我这篇论文的核心贡献
→ 使用 --quick 模式，只输出核心信息

帮我批量精读这几篇论文，保存成笔记
→ 生成多个 Markdown 文件到指定目录
```

## 📁 项目结构

```
paper-digest/
├── SKILL.md              # Agent 技能定义
├── scripts/
│   └── digest.py         # 核心脚本
├── README.md
├── LICENSE               # MIT
└── .github/
    └── workflows/
        └── test.yml
```

## 📄 License

MIT © 2026 [Allen091080](https://github.com/Allen091080)
