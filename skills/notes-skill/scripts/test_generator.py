#!/usr/bin/env python3
"""
测试生成脚本
"""

import json
import os
import random
import re
from datetime import datetime
from typing import List, Dict, Optional

class TestGenerator:
    def __init__(self, knowledge_base_path="knowledge_base.json"):
        self.knowledge_base_path = knowledge_base_path
        self.load_knowledge_base()

    def load_knowledge_base(self):
        """加载知识库"""
        if os.path.exists(self.knowledge_base_path):
            with open(self.knowledge_base_path, 'r', encoding='utf-8') as f:
                self.knowledge_base = json.load(f)
        else:
            self.knowledge_base = {
                "notes": [],
                "categories": {},
                "metadata": {}
            }

    def generate_test(self, topics: List[str], difficulty: str = "medium",
                    num_questions: int = 10, question_types: List[str] = None) -> Dict:
        """
        生成测试

        Args:
            topics: 测试涵盖的主题列表
            difficulty: 难度级别 (easy/medium/hard)
            num_questions: 问题数量
            question_types: 问题类型列表
        """
        if not question_types:
            question_types = ["选择题", "填空题", "简答题"]

        # 获取相关笔记
        relevant_notes = self._get_notes_by_topics(topics)

        if not relevant_notes:
            print("No relevant notes found for the specified topics")
            return None

        # 根据难度调整问题数量和类型分布
        difficulty_settings = {
            "easy": {"num_questions": num_questions, "choices_per_question": 3, "difficulty_weight": 0.3},
            "medium": {"num_questions": num_questions, "choices_per_question": 4, "difficulty_weight": 0.5},
            "hard": {"num_questions": num_questions, "choices_per_question": 5, "difficulty_weight": 0.7}
        }

        settings = difficulty_settings.get(difficulty, difficulty_settings["medium"])

        # 生成问题
        questions = self._generate_questions(relevant_notes, settings, question_types)

        for i, question in enumerate(questions, start=1):
            question.setdefault("id", f"q_{i}")

        # 创建测试
        test = {
            "test_id": f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "title": f"{difficulty.capitalize()} Level Test on {', '.join(topics)}",
            "topics": topics,
            "difficulty": difficulty,
            "num_questions": settings["num_questions"],
            "question_types": question_types,
            "questions": questions,
            "created": datetime.now().isoformat(),
            "duration_minutes": settings["num_questions"] * 5  # 每题5分钟
        }

        return test

    def _get_notes_by_topics(self, topics: List[str]) -> List[Dict]:
        """根据主题获取相关笔记"""
        relevant_notes = []
        for note in self.knowledge_base.get("notes", []):
            if note["category"] in topics:
                relevant_notes.append(note)
        return relevant_notes

    def _generate_questions(self, notes: List[Dict], settings: Dict, question_types: List[str]) -> List[Dict]:
        """生成测试问题"""
        questions = []
        notes_by_topic = {}

        # 按主题组织笔记
        for note in notes:
            topic = note["category"]
            if topic not in notes_by_topic:
                notes_by_topic[topic] = []
            notes_by_topic[topic].append(note)

        # 为每个主题生成问题
        for topic, topic_notes in notes_by_topic.items():
            # 每个主题的问题数量
            topic_questions = max(1, int(settings["num_questions"] * len(topic_notes) / len(notes)))

            for i in range(topic_questions):
                # 随机选择笔记
                note = random.choice(topic_notes)

                # 随机选择问题类型
                question_type = random.choice(question_types)

                # 生成问题
                question = self._create_question(note, question_type, settings)
                if question:
                    questions.append(question)

        # 如果问题数量不足，随机补充
        while len(questions) < settings["num_questions"]:
            note = random.choice(notes)
            question_type = random.choice(question_types)
            question = self._create_question(note, question_type, settings)
            if question:
                questions.append(question)

        return questions[:settings["num_questions"]]

    def _create_question(self, note: Dict, question_type: str, settings: Dict) -> Optional[Dict]:
        """创建单个问题"""
        # 这里简化处理，实际应用中需要更复杂的逻辑
        content = note.get("summary", "") or note.get("title", "")

        if question_type == "选择题":
            return self._create_multiple_choice(content, settings)
        elif question_type == "填空题":
            return self._create_fill_in_the_blank(content)
        elif question_type == "简答题":
            return self._create_short_answer(content)
        else:
            return None

    def _create_multiple_choice(self, content: str, settings: Dict) -> Dict:
        """创建选择题"""
        # 简化的选择题生成逻辑
        sentences = re.split(r'[.!?]', content)
        if not sentences:
            return None

        # 选择一个句子作为问题基础
        question_sentence = random.choice(sentences)
        if len(question_sentence.strip()) < 10:
            return None

        # 创建问题和选项
        question = {
            "type": "选择题",
            "question": question_sentence.strip(),
            "choices": [],
            "correct_answer": "",
            "explanation": ""
        }

        # 生成选项
        num_choices = settings["choices_per_question"]
        correct_answer = random.choice(["A", "B", "C", "D", "E"][:num_choices])
        question["correct_answer"] = correct_answer

        # 正确答案
        question["choices"].append({
            "option": correct_answer,
            "text": self._generate_plausible_answer(question_sentence)
        })

        # 错误答案
        for i in range(num_choices - 1):
            wrong_answer = chr(65 + i + (1 if correct_answer == "A" else 0))
            question["choices"].append({
                "option": wrong_answer,
                "text": self._generate_incorrect_answer(question_sentence)
            })

        # 打乱选项顺序
        random.shuffle(question["choices"])

        # 添加解释
        question["explanation"] = f"正确答案: {correct_answer}. {question_sentence}"

        return question

    def _generate_plausible_answer(self, sentence: str) -> str:
        """生成合理的答案"""
        # 简化的答案生成逻辑
        words = sentence.split()
        if len(words) > 3:
            return " ".join(words[-2:])
        return sentence

    def _generate_incorrect_answer(self, sentence: str) -> str:
        """生成错误答案"""
        # 简化的错误答案生成逻辑
        words = sentence.split()
        if len(words) > 2:
            return " ".join(words[:2]) + " (错误答案)"
        return "不正确的答案"

    def _create_fill_in_the_blank(self, content: str) -> Dict:
        """创建填空题"""
        # 简化的填空题生成逻辑
        words = content.split()
        if len(words) < 5:
            return None

        # 选择一个关键词
        keyword = random.choice(words[2:-2])
        if len(keyword) < 3:
            return None

        question = {
            "type": "填空题",
            "question": content.replace(keyword, "______"),
            "correct_answer": keyword,
            "explanation": f"填空处应填入: {keyword}"
        }

        return question

    def _create_short_answer(self, content: str) -> Dict:
        """创建简答题"""
        # 简化的简答题生成逻辑
        sentences = re.split(r'[.!?]', content)
        if not sentences:
            return None

        question_sentence = random.choice(sentences)
        if len(question_sentence.strip()) < 10:
            return None

        question = {
            "type": "简答题",
            "question": question_sentence.strip() + "?",
            "correct_answer": "根据笔记内容回答",
            "explanation": "请根据学习笔记中的相关内容回答此问题"
        }

        return question

    def save_test(self, test: Dict, output_path: str = "test.json"):
        """保存测试"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(test, f, indent=2, ensure_ascii=False)
        print(f"Test saved to {output_path}")

    def load_test(self, test_path: str) -> Dict:
        """加载测试"""
        with open(test_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def grade_test(self, test: Dict, answers: Dict) -> Dict:
        """评分测试"""
        score = 0
        total = len(test["questions"])
        results = []

        for question in test["questions"]:
            question_id = question.get("id", f"q_{test['questions'].index(question)}")
            user_answer = answers.get(question_id)

            if not user_answer:
                results.append({
                    "question_id": question_id,
                    "correct": False,
                    "user_answer": "未回答",
                    "correct_answer": question["correct_answer"],
                    "explanation": question["explanation"]
                })
                continue

            is_correct = False
            if question["type"] == "选择题":
                is_correct = user_answer.upper() == question["correct_answer"]
            elif question["type"] == "填空题":
                is_correct = user_answer.lower().strip() == question["correct_answer"].lower().strip()
            elif question["type"] == "简答题":
                # 简答题的评分比较复杂，这里简化处理
                is_correct = len(user_answer.split()) > 5  # 简单检查答案长度

            if is_correct:
                score += 1

            results.append({
                "question_id": question_id,
                "correct": is_correct,
                "user_answer": user_answer,
                "correct_answer": question["correct_answer"],
                "explanation": question["explanation"]
            })

        grade = {
            "test_id": test["test_id"],
            "score": score,
            "total": total,
            "percentage": (score / total) * 100,
            "results": results,
            "questions": test["questions"],
            "graded_at": datetime.now().isoformat()
        }

        return grade

if __name__ == "__main__":
    import sys
    generator = TestGenerator()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "generate" and len(sys.argv) > 4:
            topics = sys.argv[2].split(',')
            difficulty = sys.argv[3]
            num_questions = int(sys.argv[4])
            question_types = sys.argv[5].split(',') if len(sys.argv) > 5 else None

            test = generator.generate_test(topics, difficulty, num_questions, question_types)
            if test:
                generator.save_test(test)
                print("Test generated successfully!")

        elif command == "load" and len(sys.argv) > 2:
            test_path = sys.argv[2]
            test = generator.load_test(test_path)
            print(f"Loaded test from {test_path}")
            print(json.dumps(test, indent=2))

        elif command == "grade" and len(sys.argv) > 3:
            test_path = sys.argv[2]
            answers_path = sys.argv[3]

            test = generator.load_test(test_path)
            with open(answers_path, 'r', encoding='utf-8') as f:
                answers = json.load(f)

            grade = generator.grade_test(test, answers)
            print(f"Test graded successfully!")
            print(f"Score: {grade['score']}/{grade['total']} ({grade['percentage']:.1f}%)")

    else:
        print("Usage:")
        print("  python test_generator.py generate <topics> <difficulty> <num_questions> [question_types]")
        print("  python test_generator.py load <test_path>")
        print("  python test_generator.py grade <test_path> <answers_path>")
