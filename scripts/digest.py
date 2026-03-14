#!/usr/bin/env python3
"""
paper-digest — 学术论文精读脚本
用法: python3 digest.py --arxiv <url> | --pdf <file>
"""

import argparse
import json
import re
import sys
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path


def fetch_arxiv_metadata(arxiv_url: str) -> dict:
    """从 arXiv 获取论文元数据"""
    # 提取 arXiv ID
    m = re.search(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5}(?:v\d+)?)", arxiv_url, re.I)
    if not m:
        print(f"❌ 无法解析 arXiv URL：{arxiv_url}", file=sys.stderr)
        sys.exit(1)

    arxiv_id = m.group(1)
    api_url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"

    try:
        with urllib.request.urlopen(api_url, timeout=15) as r:
            xml = r.read().decode("utf-8")
    except Exception as e:
        print(f"❌ 无法访问 arXiv API：{e}", file=sys.stderr)
        sys.exit(1)

    def extract_tag(tag, text):
        m = re.search(f"<{tag}[^>]*>(.*?)</{tag}>", text, re.DOTALL)
        return m.group(1).strip() if m else ""

    title = extract_tag("title", xml).replace("\n", " ").strip()
    abstract = extract_tag("summary", xml).replace("\n", " ").strip()
    authors_raw = re.findall(r"<name>(.*?)</name>", xml)
    published = extract_tag("published", xml)[:10]

    return {
        "arxiv_id": arxiv_id,
        "title": title,
        "authors": authors_raw,
        "published": published,
        "abstract": abstract,
        "url": arxiv_url,
    }


def extract_pdf_text(pdf_path: str, max_pages: int = 20) -> str:
    """从 PDF 提取文字"""
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            pages = pdf.pages[:max_pages]
            text = "\n".join(p.extract_text() or "" for p in pages)
        return text
    except ImportError:
        print("❌ 读取 PDF 需要：pip3 install pdfplumber", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ 无法读取 PDF：{e}", file=sys.stderr)
        sys.exit(1)


def score_paper(abstract: str, title: str) -> tuple:
    """基于摘要内容给论文打引用价值分"""
    high_value_kws = ["state-of-the-art", "outperform", "novel", "first", "benchmark", "significant improvement",
                      "大幅提升", "首次", "新方法", "超越", "sota"]
    mid_value_kws = ["propose", "present", "improve", "better", "approach", "提出", "改进", "方法"]
    limit_kws = ["preliminary", "small-scale", "limited", "future work", "局限", "初步", "小规模"]

    text = (abstract + " " + title).lower()
    score = 6  # 基础分
    for kw in high_value_kws:
        if kw.lower() in text:
            score = min(score + 1, 10)
    for kw in limit_kws:
        if kw.lower() in text:
            score = max(score - 1, 1)

    if score >= 9:
        label = "必读，领域内里程碑"
        audience = "所有相关研究者"
    elif score >= 7:
        label = "值得精读，有实质贡献"
        audience = "该领域研究者/从业者"
    elif score >= 5:
        label = "有参考价值，选读"
        audience = "相关方向感兴趣者"
    else:
        label = "贡献有限，快速浏览即可"
        audience = "特定需求读者"

    return score, label, audience


def generate_digest(meta: dict, full_text: str = "", lang: str = "zh", quick: bool = False) -> str:
    title = meta.get("title", "未知标题")
    authors = meta.get("authors", [])
    published = meta.get("published", "未知")
    abstract = meta.get("abstract", "")
    arxiv_id = meta.get("arxiv_id", "")

    authors_str = "、".join(authors[:3]) + ("等" if len(authors) > 3 else "")
    score, score_label, audience = score_paper(abstract, title)

    # 从摘要中提取关键信息
    method_hints = re.findall(r"(?:we propose|we present|we introduce|我们提出|本文提出)[^.。]{10,100}", abstract, re.I)
    result_hints = re.findall(r"(?:achieve|outperform|improve|达到|超越|提升)[^.。]{5,80}", abstract, re.I)
    limit_hints = re.findall(r"(?:limitation|future|however|局限|未来|然而)[^.。]{10,80}", abstract, re.I)

    lines = []
    lines.append("")
    lines.append("━" * 62)
    lines.append(f"  📄 论文精读报告")
    lines.append("━" * 62)
    lines.append("")
    lines.append(f"📌 【论文信息】")
    lines.append(f"   标题：{title}")
    lines.append(f"   作者：{authors_str if authors_str else '未知'}")
    lines.append(f"   发表：{published}")
    if arxiv_id:
        lines.append(f"   链接：https://arxiv.org/abs/{arxiv_id}")
    lines.append("")

    lines.append(f"❓ 【核心问题】")
    # 从摘要前两句提取问题
    abstract_sentences = re.split(r"[.。]", abstract)[:3]
    for s in abstract_sentences:
        s = s.strip()
        if len(s) > 20:
            lines.append(f"   {s}。")
            if quick:
                break
    lines.append("")

    if not quick:
        lines.append(f"💡 【主要贡献】")
        if method_hints:
            for i, h in enumerate(method_hints[:3], 1):
                lines.append(f"   {i}. {h.strip()}")
        else:
            lines.append(f"   （请阅读全文 Introduction 部分获取详细贡献）")
        lines.append("")

        lines.append(f"🔬 【方法概述】")
        if full_text:
            # 从正文找 Method/Approach 段落
            method_match = re.search(r"(?:Method|Approach|Architecture|方法)[^\n]{0,200}", full_text, re.I)
            if method_match:
                lines.append(f"   {method_match.group()[:200].strip()}")
            else:
                lines.append(f"   基于摘要推断：{abstract[:200]}")
        else:
            lines.append(f"   基于摘要：{abstract[:300]}")
        lines.append("")

    lines.append(f"📊 【关键结果】")
    if result_hints:
        for h in result_hints[:3]:
            lines.append(f"   · {h.strip()}")
    else:
        lines.append(f"   （请查看论文 Experiments 章节获取具体数据）")
    lines.append("")

    if not quick:
        lines.append(f"⚠️  【局限性与不足】")
        if limit_hints:
            for h in limit_hints[:2]:
                lines.append(f"   · {h.strip()}")
        else:
            lines.append(f"   · 作者未在摘要中明确说明局限性，请阅读 Conclusion 章节")
        lines.append("")

    lines.append(f"⭐ 【引用价值评分】")
    lines.append(f"   {score}/10 — {score_label}")
    lines.append(f"   适合：{audience}")
    lines.append("")

    if arxiv_id:
        lines.append(f"📎 【引用格式（BibTeX）】")
        year = published[:4] if published else "2024"
        first_author = authors[0].split()[-1].lower() if authors else "unknown"
        key_word = re.sub(r"[^a-z]", "", title.lower().split()[0]) if title else "paper"
        lines.append(f"   @article{{{first_author}{year}{key_word},")
        lines.append(f"     title  = {{{title}}},")
        lines.append(f"     author = {{{' and '.join(authors)}}},")
        lines.append(f"     year   = {{{year}}},")
        lines.append(f"     url    = {{https://arxiv.org/abs/{arxiv_id}}}")
        lines.append(f"   }}")

    lines.append("")
    lines.append("━" * 62)
    lines.append(f"由 paper-digest skill 生成 | {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="学术论文精读工具")
    src = parser.add_mutually_exclusive_group()
    src.add_argument("--arxiv", help="arXiv 论文链接")
    src.add_argument("--pdf", help="本地 PDF 文件路径")
    src.add_argument("--arxiv-list", help="包含多个 arXiv 链接的文件")
    src.add_argument("--batch", help="包含多个 PDF 的文件夹")

    parser.add_argument("--lang", choices=["zh", "en"], default="zh")
    parser.add_argument("--quick", action="store_true", help="快速模式（只输出核心信息）")
    parser.add_argument("--cite", choices=["bibtex", "apa"], default=None)
    parser.add_argument("--save", help="保存摘要到指定路径")
    parser.add_argument("--output", default="/tmp", help="批量处理输出目录")
    parser.add_argument("--extract-figures", action="store_true", help="提取论文图表")

    args = parser.parse_args()

    def process_one(meta: dict, full_text: str = "") -> str:
        return generate_digest(meta, full_text, args.lang, args.quick)

    if args.arxiv:
        meta = fetch_arxiv_metadata(args.arxiv)
        result = process_one(meta)
        print(result)
        if args.save:
            Path(args.save).write_text(result, encoding="utf-8")
            print(f"\n✅ 已保存：{args.save}")

    elif args.pdf:
        text = extract_pdf_text(args.pdf)
        # 简单提取标题（取第一行）
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        meta = {
            "title": lines[0] if lines else Path(args.pdf).stem,
            "authors": [],
            "published": "",
            "abstract": " ".join(lines[1:20]),
        }
        result = process_one(meta, text)
        print(result)
        if args.save:
            Path(args.save).write_text(result, encoding="utf-8")
            print(f"\n✅ 已保存：{args.save}")

    elif args.arxiv_list:
        urls = Path(args.arxiv_list).read_text().strip().split("\n")
        out_dir = Path(args.output)
        out_dir.mkdir(parents=True, exist_ok=True)
        for i, url in enumerate(urls, 1):
            url = url.strip()
            if not url:
                continue
            print(f"\n[{i}/{len(urls)}] 处理：{url}")
            try:
                meta = fetch_arxiv_metadata(url)
                result = process_one(meta)
                fname = f"{meta['arxiv_id']}_digest.md"
                (out_dir / fname).write_text(result, encoding="utf-8")
                print(f"   ✅ 保存：{out_dir / fname}")
            except Exception as e:
                print(f"   ❌ 失败：{e}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
