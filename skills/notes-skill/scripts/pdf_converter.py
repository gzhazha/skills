#!/usr/bin/env python3
"""
PDF到MD笔记转换脚本
"""

import re
import os
from datetime import datetime

def extract_text_from_pdf(pdf_path):
    """从PDF文件中提取文本内容"""
    text = ""
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += (page.extract_text() or "") + "\n"
    except ModuleNotFoundError:
        print("Error: Missing dependency 'pdfplumber'. Install it with: pip install pdfplumber")
        return None
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None
    return text

def structure_notes(text, title="", pdf_path=""):
    """将提取的文本结构化为Markdown笔记"""
    # 基本的Markdown结构
    structured_notes = f"""# {title or "学习笔记"}

**创建时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 内容摘要

{get_summary(text)}

## 主要知识点

{extract_key_points(text)}

## 详细内容

{text}

## 学习要点

- [ ] 理解核心概念
- [ ] 掌握关键技能
- [ ] 完成练习题
- [ ] 复习重要内容

## 相关资源

- [原始PDF文件]({pdf_path or "N/A"})
"""
    return structured_notes

def get_summary(text, max_length=200):
    """生成内容摘要"""
    # 简单的摘要生成逻辑
    sentences = re.split(r'[.!?]', text)
    summary = " ".join(sentences[:3])
    return summary[:max_length] + "..." if len(summary) > max_length else summary

def extract_key_points(text):
    """提取关键知识点"""
    # 简单的关键点提取逻辑
    lines = text.split('\n')
    key_points = []
    for line in lines:
        if any(keyword in line.lower() for keyword in ['重要', '关键', '核心', '要点', '概念']):
            key_points.append(f"- {line.strip()}")

    if not key_points:
        # 如果没有找到明显的关键点，取前5行作为示例
        key_points = [f"- {line.strip()}" for line in lines[:5] if line.strip()]

    return "\n".join(key_points)

def convert_pdf_to_md(pdf_path, output_dir="output"):
    """主转换函数"""
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        return None

    # 提取文本
    text = extract_text_from_pdf(pdf_path)
    if not text:
        print("Failed to extract text from PDF")
        return None

    # 获取文件名作为标题
    title = os.path.splitext(os.path.basename(pdf_path))[0]

    # 结构化笔记
    structured_notes = structure_notes(text, title, pdf_path)

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 生成输出文件名
    output_path = os.path.join(output_dir, f"{title}.md")

    # 保存MD文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(structured_notes)

    print(f"Successfully converted {pdf_path} to {output_path}")
    return output_path

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        pdf_file = sys.argv[1]
        convert_pdf_to_md(pdf_file)
    else:
        print("Usage: python pdf_converter.py <pdf_file_path>")
