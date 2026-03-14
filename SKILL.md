---
name: paper-digest
description: 输入学术论文 PDF 或 arXiv 链接，输出结构化精读摘要：核心问题、方法、结论、局限性、引用价值评分。支持中英文。
version: "1.0.0"
metadata: {"openclaw": {"os": ["darwin", "linux", "win32"], "emoji": "📄", "user-invocable": true, "homepage": "https://github.com/Allen091080/paper-digest", "tags": ["research", "academic", "study", "pdf", "arxiv"]}}
---

# Paper Digest — 学术论文精读助手

给你一篇论文（PDF 或 arXiv 链接），我来精读并输出结构化摘要，帮你快速判断是否值得深读，以及论文的核心贡献在哪里。

## 适用场景

| 场景 | 用这个？ |
|------|---------|
| 快速了解一篇论文的核心内容 | ✅ 是 |
| 判断论文是否值得精读 | ✅ 是 |
| 提取论文中的关键方法和数据 | ✅ 是 |
| 生成中文论文笔记 | ✅ 是 |
| 从 arXiv 链接直接解读 | ✅ 是 |
| 批量处理多篇论文 | ✅ 是 |
| 写综述/文献综述 | ✅ 辅助 |
| 生成引用格式 | ✅ 是 |
| 论文写作/代写 | ❌ 否 |

## 输出结构

每篇论文精读输出以下 7 个部分：

```
📌 论文信息
  标题 / 作者 / 机构 / 发表时间 / 期刊/会议

❓ 核心问题
  这篇论文要解决什么问题？现有方法有什么不足？

💡 主要贡献
  1. ...
  2. ...
  3. ...

🔬 方法概述
  技术路线、模型架构、算法核心（非技术读者友好版）

📊 关键结果
  主要实验数据、对比基线、性能提升幅度

⚠️ 局限性与不足
  作者承认的局限 + 我的独立判断

⭐ 引用价值评分
  综合评分 x/10，推荐指数，适合哪类读者
```

## 如何使用

### 1. 从 arXiv 链接解读

```bash
# 输入 arXiv 链接
python3 {baseDir}/scripts/digest.py --arxiv "https://arxiv.org/abs/2303.08774"

# 只要摘要（快速模式）
python3 {baseDir}/scripts/digest.py --arxiv "https://arxiv.org/abs/2303.08774" --quick

# 输出中文摘要
python3 {baseDir}/scripts/digest.py --arxiv "https://arxiv.org/abs/2303.08774" --lang zh
```

### 2. 从本地 PDF 解读

```bash
# 解读本地 PDF
python3 {baseDir}/scripts/digest.py --pdf /path/to/paper.pdf

# 解读并保存笔记
python3 {baseDir}/scripts/digest.py --pdf /path/to/paper.pdf --save ~/notes/paper_notes.md
```

### 3. 批量处理

```bash
# 处理一个文件夹里的所有 PDF
python3 {baseDir}/scripts/digest.py --batch /path/to/papers/ --output ~/notes/digests/

# 从文件列表批量处理 arXiv
python3 {baseDir}/scripts/digest.py --arxiv-list /path/to/urls.txt --output ~/notes/
```

### 4. 生成引用格式

```bash
# 生成 BibTeX
python3 {baseDir}/scripts/digest.py --arxiv "https://arxiv.org/abs/2303.08774" --cite bibtex

# 生成 APA
python3 {baseDir}/scripts/digest.py --arxiv "https://arxiv.org/abs/2303.08774" --cite apa
```

### 5. 提取关键图表

```bash
# 提取论文中所有图表并保存
python3 {baseDir}/scripts/digest.py --pdf paper.pdf --extract-figures --output /tmp/figures/
```

## 与 AI Agent 对话示例

```
用户：帮我看一下这篇论文 https://arxiv.org/abs/2303.08774

Agent：
📌 GPT-4 Technical Report
   OpenAI | 2023-03-15

❓ 核心问题
   如何构建一个在多种专业和学术基准上接近人类水平的大型多模态语言模型？

💡 主要贡献
   1. 发布 GPT-4，支持文本+图像输入
   2. 在 Bar 考试、LSAT 等专业考试达到前 10% 水平
   3. 提出了可预测扩展（predictable scaling）方法论

🔬 方法概述
   在大规模数据集上预训练 Transformer 架构，通过 RLHF 对齐，
   加入视觉编码器支持图像输入...

📊 关键结果
   - Bar Exam: 前 10%（GPT-3.5 为后 10%）
   - MMLU: 86.4%（vs GPT-3.5 的 70.0%）

⚠️ 局限性
   - 仍存在幻觉问题
   - 训练数据截止 2021 年

⭐ 引用价值：9/10 — 必读，AI 领域重要基础文献

用户：帮我把这个摘要保存成 Markdown 笔记
Agent：[保存到 ~/notes/gpt4_digest.md]
```

## 重要规则

1. **解读要客观**，不夸大论文贡献，局限性要如实指出
2. **技术细节用非技术语言描述**，让不同背景的读者都能理解
3. **引用价值评分标准**：
   - 9-10：领域内里程碑论文
   - 7-8：有实质贡献，值得精读
   - 5-6：有参考价值，选读
   - 3-4：贡献有限，快速浏览即可
4. **需要安装 pdfplumber**：`pip3 install pdfplumber requests`
5. **arXiv 解读需要网络连接**拉取 PDF 内容
6. **输出语言默认跟随输入**，可用 `--lang zh/en` 强制指定
