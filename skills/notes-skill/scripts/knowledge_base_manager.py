#!/usr/bin/env python3
"""
知识库管理脚本
"""

import os
import json
import shutil
from datetime import datetime

class KnowledgeBaseManager:
    def __init__(self, db_path="knowledge_base.json"):
        self.db_path = db_path
        self.load_database()

    def load_database(self):
        """加载知识库"""
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r', encoding='utf-8') as f:
                self.database = json.load(f)
        else:
            self.database = {
                "notes": [],
                "categories": {},
                "metadata": {
                    "created": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat()
                }
            }

    def save_database(self):
        """保存知识库"""
        self.database["metadata"]["last_updated"] = datetime.now().isoformat()
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(self.database, f, indent=2, ensure_ascii=False)

    def add_note(self, note_path, category, title=None, tags=None):
        """添加笔记到知识库"""
        if not os.path.exists(note_path):
            print(f"Error: Note file not found at {note_path}")
            return False

        # 读取笔记内容
        with open(note_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 提取摘要
        summary = self._extract_summary(content)

        # 创建笔记记录
        note_record = {
            "id": len(self.database["notes"]) + 1,
            "title": title or os.path.splitext(os.path.basename(note_path))[0],
            "path": note_path,
            "category": category,
            "tags": tags or [],
            "summary": summary,
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat(),
            "content_length": len(content)
        }

        # 添加到知识库
        self.database["notes"].append(note_record)

        # 更新分类统计
        if category not in self.database["categories"]:
            self.database["categories"][category] = []
        self.database["categories"][category].append(note_record["id"])

        # 保存数据库
        self.save_database()
        print(f"Added note '{note_record['title']}' to category '{category}'")
        return True

    def _extract_summary(self, content, max_length=200):
        """提取内容摘要"""
        # 简单的摘要提取逻辑
        lines = content.split('\n')
        summary_lines = []
        for line in lines:
            if line.strip() and not line.startswith('#'):
                summary_lines.append(line.strip())
                if len(' '.join(summary_lines)) > max_length:
                    break

        return ' '.join(summary_lines)[:max_length] + "..." if len(' '.join(summary_lines)) > max_length else ' '.join(summary_lines)

    def list_notes(self, category=None, search_term=None):
        """列出笔记"""
        notes = self.database["notes"]

        # 按分类过滤
        if category:
            category_notes = self.database["categories"].get(category, [])
            notes = [note for note in notes if note["id"] in category_notes]

        # 按搜索词过滤
        if search_term:
            notes = [note for note in notes if search_term.lower() in note["title"].lower() or
                                           search_term.lower() in note["summary"].lower()]

        return notes

    def get_note(self, note_id):
        """获取特定笔记"""
        for note in self.database["notes"]:
            if note["id"] == note_id:
                return note
        return None

    def update_note(self, note_id, new_content):
        """更新笔记内容"""
        for note in self.database["notes"]:
            if note["id"] == note_id:
                # 保存旧文件备份
                backup_path = f"{note['path']}.bak"
                shutil.copy2(note['path'], backup_path)

                # 更新文件内容
                with open(note['path'], 'w', encoding='utf-8') as f:
                    f.write(new_content)

                # 更新数据库记录
                note["summary"] = self._extract_summary(new_content)
                note["updated"] = datetime.now().isoformat()
                note["content_length"] = len(new_content)

                self.save_database()
                print(f"Updated note {note_id}: {note['title']}")
                return True
        return False

    def delete_note(self, note_id):
        """删除笔记"""
        for i, note in enumerate(self.database["notes"]):
            if note["id"] == note_id:
                # 删除文件
                if os.path.exists(note["path"]):
                    os.remove(note["path"])

                # 从数据库中移除
                del self.database["notes"][i]

                # 从分类中移除
                for category in list(self.database["categories"].keys()):
                    if note_id in self.database["categories"][category]:
                        self.database["categories"][category].remove(note_id)
                        if not self.database["categories"][category]:
                            del self.database["categories"][category]

                self.save_database()
                print(f"Deleted note {note_id}: {note['title']}")
                return True
        return False

    def search_notes(self, query):
        """搜索笔记"""
        results = []
        for note in self.database["notes"]:
            if (query.lower() in note["title"].lower() or
                query.lower() in note["summary"].lower() or
                any(query.lower() in tag.lower() for tag in note["tags"])):
                results.append(note)
        return results

    def get_statistics(self):
        """获取知识库统计信息"""
        total_notes = len(self.database["notes"])
        total_categories = len(self.database["categories"])
        total_tags = len(set(tag for note in self.database["notes"] for tag in note["tags"]))

        return {
            "total_notes": total_notes,
            "total_categories": total_categories,
            "total_tags": total_tags,
            "categories_distribution": self.database["categories"]
        }

if __name__ == "__main__":
    import sys
    db_manager = KnowledgeBaseManager()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "add" and len(sys.argv) > 3:
            note_path = sys.argv[2]
            category = sys.argv[3]
            title = sys.argv[4] if len(sys.argv) > 4 else None
            tags = sys.argv[5].split(',') if len(sys.argv) > 5 else None
            db_manager.add_note(note_path, category, title, tags)

        elif command == "list":
            notes = db_manager.list_notes()
            for note in notes:
                print(f"{note['id']}: {note['title']} ({note['category']})")

        elif command == "search" and len(sys.argv) > 2:
            query = sys.argv[2]
            results = db_manager.search_notes(query)
            print(f"Search results for '{query}':")
            for note in results:
                print(f"- {note['title']} ({note['category']})")

        elif command == "stats":
            stats = db_manager.get_statistics()
            print("Knowledge Base Statistics:")
            print(f"Total notes: {stats['total_notes']}")
            print(f"Total categories: {stats['total_categories']}")
            print(f"Total tags: {stats['total_tags']}")
            print("Categories distribution:")
            for category, note_ids in stats['categories_distribution'].items():
                print(f"  {category}: {len(note_ids)} notes")

    else:
        print("Usage:")
        print("  python knowledge_base_manager.py add <note_path> <category> [title] [tags]")
        print("  python knowledge_base_manager.py list")
        print("  python knowledge_base_manager.py search <query>")
        print("  python knowledge_base_manager.py stats")
