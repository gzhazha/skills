---
name: notes-skill
description: 将PDF学习课程和笔记整理成MD格式笔记，形成知识库，基于知识库指导学习、制定学习计划、生成测试，发现学习薄弱模块并制定专项学习计划
---

# Notes Skill - PDF到MD笔记转换与学习管理系统

## 技能概述

这个技能帮助用户将PDF形式的学习课程和笔记转换为结构化的MD格式笔记，构建个人知识库，并提供基于知识库的学习指导、学习计划制定、测试生成和学习薄弱点分析功能。

## 使用场景

当用户需要：
- 将PDF课程材料转换为可编辑的Markdown笔记
- 管理和整理学习资料形成知识库
- 基于已有知识制定学习计划
- 生成测试来评估学习进度
- 识别学习薄弱环节并制定针对性学习计划

## 工作流程

### 1. PDF到MD笔记转换
- 读取PDF文件内容
- 提取文本和结构信息
- 转换为Markdown格式
- 按主题组织笔记内容

### 2. 知识库构建
- 将转换后的笔记存储在知识库中
- 按学科/主题分类组织
- 建立知识点之间的关联
- 维护笔记的版本历史

### 3. 学习指导
- 分析知识库内容
- 识别学习重点和难点
- 提供学习建议和资源推荐
- 跟踪学习进度

### 4. 学习计划制定
- 基于知识库内容生成个性化学习计划
- 设定学习目标和时间表
- 分配学习任务和资源
- 调整计划以适应学习进度

### 5. 测试生成与薄弱点分析
- 根据知识库内容生成测试题
- 评估学习掌握程度
- 识别薄弱知识点
- 制定专项强化学习计划

## 使用方法

### 初始化知识库
```bash
# 添加PDF学习资料
notes-skill add-pdf <文件路径> --category <学科类别> --title <笔记标题>

# 转换PDF为MD笔记
notes-skill convert-pdf <文件路径>
```

### 管理知识库
```bash
# 查看知识库结构
notes-skill list-notes

# 搜索特定主题
notes-skill search <关键词>

# 更新笔记内容
notes-skill update-note <笔记ID> --content <新内容>
```

### 学习计划与测试
```bash
# 生成学习计划
notes-skill generate-plan --duration <天数> --focus <重点主题>

# 创建测试
notes-skill generate-test --topics <主题列表> --difficulty <难度级别>

# 分析学习薄弱点
notes-skill analyze-weakness --test-results <测试结果>
```

## 资源文件

### 脚本 (scripts/)
- `pdf_converter.py`: PDF到MD转换脚本
- `knowledge_base_manager.py`: 知识库管理脚本
- `learning_planner.py`: 学习计划生成脚本
- `test_generator.py`: 测试生成脚本
- `weakness_analyzer.py`: 薄弱点分析脚本

### 参考资料 (references/)
- `markdown_syntax.md`: Markdown语法参考
- `learning_theory.md`: 学习理论指导
- `test_design_guidelines.md`: 测试设计指南

### 资产 (assets/)
- `note_templates/`: 笔记模板
- `study_plans/`: 学习计划模板
- `test_templates/`: 测试模板

## 注意事项

1. 确保PDF文件可读性和文本提取质量
2. 定期备份知识库数据
3. 根据学习进度调整学习计划
4. 测试结果应作为学习改进的参考，而非最终评价

## 技术要求

- Python 3.7+
- PDF处理库 (PyPDF2, pdfplumber等)
- Markdown处理库
- 数据库支持 (SQLite, JSON等)
- 自然语言处理能力

## 示例工作流

1. 用户上传PDF课程材料
2. 技能自动转换为MD笔记并分类
3. 构建知识库结构
4. 基于知识库生成个性化学习计划
5. 定期生成测试评估学习效果
6. 分析测试结果，识别薄弱点
7. 调整学习计划，加强薄弱环节学习

这个技能将帮助用户系统化地管理学习过程，提高学习效率和效果。