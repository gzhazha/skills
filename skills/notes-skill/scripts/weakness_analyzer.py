#!/usr/bin/env python3
"""
学习薄弱点分析脚本
"""

import json
import statistics
from typing import List, Dict, Optional

class WeaknessAnalyzer:
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

    def analyze_weaknesses(self, test_results: Dict, study_plan: Dict = None) -> Dict:
        """
        分析学习薄弱点

        Args:
            test_results: 测试结果
            study_plan: 学习计划（可选）
        """
        # 解析测试结果
        weaknesses = self._parse_test_results(test_results)

        # 结合知识库分析
        knowledge_based_weaknesses = self._analyze_with_knowledge_base(weaknesses)

        # 生成专项学习计划
        targeted_plan = self._generate_targeted_plan(knowledge_based_weaknesses, study_plan)

        analysis = {
            "analysis_id": f"analysis_{test_results.get('graded_at', '').replace(':', '').replace('-', '').replace('T', '').replace('.', '')}",
            "test_id": test_results.get("test_id"),
            "score": test_results.get("score"),
            "total": test_results.get("total"),
            "percentage": test_results.get("percentage"),
            "weaknesses": knowledge_based_weaknesses,
            "targeted_plan": targeted_plan,
            "analysis_date": test_results.get("graded_at", datetime.now().isoformat())
        }

        return analysis

    def _parse_test_results(self, test_results: Dict) -> List[Dict]:
        """解析测试结果，识别薄弱点"""
        weaknesses = []

        for result in test_results.get("results", []):
            if not result["correct"]:
                # 识别问题类型和主题
                question = self._find_question_by_id(test_results.get("questions", []), result["question_id"])
                if question:
                    weakness = {
                        "question_id": result["question_id"],
                        "question_type": question.get("type", "unknown"),
                        "topic": self._extract_topic_from_question(question.get("question", "")),
                        "user_answer": result["user_answer"],
                        "correct_answer": result["correct_answer"],
                        "explanation": result["explanation"],
                        "difficulty": self._assess_difficulty(question)
                    }
                    weaknesses.append(weakness)

        return weaknesses

    def _find_question_by_id(self, questions: List[Dict], question_id: str) -> Optional[Dict]:
        """根据问题ID查找问题"""
        for question in questions:
            if question.get("id") == question_id:
                return question
        return None

    def _extract_topic_from_question(self, question: str) -> str:
        """从问题中提取主题"""
        # 简化的主题提取逻辑
        words = question.split()
        if len(words) > 3:
            return " ".join(words[:3])
        return "general"

    def _assess_difficulty(self, question: Dict) -> str:
        """评估问题难度"""
        # 简化的难度评估逻辑
        if question["type"] == "简答题":
            return "hard"
        elif len(question.get("choices", [])) > 4:
            return "medium"
        return "easy"

    def _analyze_with_knowledge_base(self, weaknesses: List[Dict]) -> List[Dict]:
        """结合知识库分析薄弱点"""
        analyzed_weaknesses = []

        for weakness in weaknesses:
            # 查找相关的笔记
            related_notes = self._find_related_notes(weakness["topic"])

            analyzed_weakness = {
                "question_id": weakness["question_id"],
                "question_type": weakness["question_type"],
                "topic": weakness["topic"],
                "user_answer": weakness["user_answer"],
                "correct_answer": weakness["correct_answer"],
                "explanation": weakness["explanation"],
                "difficulty": weakness["difficulty"],
                "related_notes": related_notes,
                "suggested_actions": self._generate_suggested_actions(weakness)
            }

            analyzed_weaknesses.append(analyzed_weakness)

        return analyzed_weaknesses

    def _find_related_notes(self, topic: str) -> List[Dict]:
        """查找相关笔记"""
        related_notes = []
        for note in self.knowledge_base.get("notes", []):
            if topic.lower() in note["category"].lower() or topic.lower() in note["title"].lower():
                related_notes.append({
                    "id": note["id"],
                    "title": note["title"],
                    "category": note["category"],
                    "summary": note["summary"]
                })

        return related_notes

    def _generate_suggested_actions(self, weakness: Dict) -> List[str]:
        """生成建议行动"""
        actions = []

        # 根据问题类型和难度生成建议
        if weakness["question_type"] == "选择题":
            actions.append("重新阅读相关章节，理解概念")
            actions.append("多做选择题练习")
        elif weakness["question_type"] == "填空题":
            actions.append("重点记忆关键术语和定义")
            actions.append("进行术语复习")
        elif weakness["question_type"] == "简答题":
            actions.append("加强理解和应用能力")
            actions.append("多做案例分析练习")

        if weakness["difficulty"] == "hard":
            actions.append("寻求额外学习资源")
            actions.append("考虑参加辅导或讨论")

        actions.append("复习相关笔记内容")
        actions.append("做更多练习题")

        return actions

    def _generate_targeted_plan(self, weaknesses: List[Dict], study_plan: Dict = None) -> Dict:
        """生成专项学习计划"""
        # 统计各主题的薄弱点数量
        topic_weaknesses = {}
        for weakness in weaknesses:
            topic = weakness["topic"]
            if topic not in topic_weaknesses:
                topic_weaknesses[topic] = 0
            topic_weaknesses[topic] += 1

        # 按薄弱点数量排序
        sorted_topics = sorted(topic_weaknesses.items(), key=lambda x: x[1], reverse=True)

        # 生成专项计划
        targeted_plan = {
            "plan_id": f"targeted_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "duration_days": 7,  # 默认7天专项计划
            "focus_areas": [],
            "daily_activities": []
        }

        # 为每个薄弱主题制定计划
        for topic, count in sorted_topics[:3]:  # 只关注前3个最薄弱的主题
            focus_area = {
                "topic": topic,
                "weakness_count": count,
                "priority": "high" if count >= 3 else "medium",
                "recommended_hours": min(10, count * 2),  # 每个薄弱点建议2小时
                "activities": self._generate_topic_activities(topic)
            }
            targeted_plan["focus_areas"].append(focus_area)

        # 生成每日活动
        for day in range(1, targeted_plan["duration_days"] + 1):
            daily_activity = {
                "day": day,
                "date": (datetime.now() + timedelta(days=day-1)).strftime("%Y-%m-%d"),
                "focus_topics": [area["topic"] for area in targeted_plan["focus_areas"]],
                "activities": self._generate_daily_activities(day, targeted_plan["focus_areas"])
            }
            targeted_plan["daily_activities"].append(daily_activity)

        return targeted_plan

    def _generate_topic_activities(self, topic: str) -> List[str]:
        """生成主题相关的学习活动"""
        activities = [
            "重新阅读相关笔记",
            "做练习题",
            "总结关键概念",
            "制作思维导图",
            "与他人讨论",
            "查找额外资源"
        ]
        return activities

    def _generate_daily_activities(self, day: int, focus_areas: List[Dict]) -> List[str]:
        """生成每日学习活动"""
        activities = []

        # 轮流关注不同的主题
        topic_index = (day - 1) % len(focus_areas)
        focus_topic = focus_areas[topic_index]["topic"]

        activities.append(f"重点学习: {focus_topic}")
        activities.append("阅读相关笔记")
        activities.append("做练习题")
        activities.append("总结学习内容")

        return activities

    def save_analysis(self, analysis: Dict, output_path: str = "weakness_analysis.json"):
        """保存分析结果"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        print(f"Weakness analysis saved to {output_path}")

    def load_analysis(self, analysis_path: str) -> Dict:
        """加载分析结果"""
        with open(analysis_path, 'r', encoding='utf-8') as f:
            return json.load(f)

if __name__ == "__main__":
    import sys
    analyzer = WeaknessAnalyzer()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "analyze" and len(sys.argv) > 3:
            test_results_path = sys.argv[2]
            study_plan_path = sys.argv[3] if len(sys.argv) > 3 else None

            with open(test_results_path, 'r', encoding='utf-8') as f:
                test_results = json.load(f)

            study_plan = None
            if study_plan_path and os.path.exists(study_plan_path):
                with open(study_plan_path, 'r', encoding='utf-8') as f:
                    study_plan = json.load(f)

            analysis = analyzer.analyze_weaknesses(test_results, study_plan)
            analyzer.save_analysis(analysis)
            print("Weakness analysis completed successfully!")

        elif command == "load" and len(sys.argv) > 2:
            analysis_path = sys.argv[2]
            analysis = analyzer.load_analysis(analysis_path)
            print(f"Loaded analysis from {analysis_path}")
            print(json.dumps(analysis, indent=2))

    else:
        print("Usage:")
        print("  python weakness_analyzer.py analyze <test_results_path> [study_plan_path]")
        print("  python weakness_analyzer.py load <analysis_path>")