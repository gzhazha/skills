#!/usr/bin/env python3
"""
学习计划生成脚本
"""

import json
import os
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class LearningPlanner:
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

    def generate_study_plan(self, duration_days: int, focus_topics: List[str] = None,
                         daily_study_hours: float = 2.0, difficulty_level: str = "medium") -> Dict:
        """
        生成学习计划

        Args:
            duration_days: 学习计划天数
            focus_topics: 重点学习主题列表
            daily_study_hours: 每日学习小时数
            difficulty_level: 难度级别 (easy/medium/hard)
        """
        # 获取知识库中的笔记
        notes = self.knowledge_base.get("notes", [])

        # 如果没有指定重点主题，随机选择一些
        if not focus_topics:
            focus_topics = list(self.knowledge_base.get("categories", {}).keys())[:3]
            if not focus_topics:
                focus_topics = ["general"]

        # 根据难度级别确定学习强度
        difficulty_settings = {
            "easy": {"daily_hours": daily_study_hours * 0.7, "break_frequency": 45},
            "medium": {"daily_hours": daily_study_hours, "break_frequency": 30},
            "hard": {"daily_hours": daily_study_hours * 1.3, "break_frequency": 25}
        }

        settings = difficulty_settings.get(difficulty_level, difficulty_settings["medium"])

        # 为每个主题分配学习时间
        topic_allocation = self._allocate_time_by_topic(focus_topics, duration_days, settings["daily_hours"])

        # 生成每日计划
        daily_plans = self._generate_daily_plans(topic_allocation, settings["break_frequency"])

        # 生成每周复习计划
        weekly_reviews = self._generate_weekly_reviews(duration_days)

        # 生成测试计划
        test_schedule = self._generate_test_schedule(duration_days)

        plan = {
            "plan_id": f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=duration_days)).strftime("%Y-%m-%d"),
            "duration_days": duration_days,
            "daily_study_hours": settings["daily_hours"],
            "difficulty_level": difficulty_level,
            "focus_topics": focus_topics,
            "daily_plans": daily_plans,
            "weekly_reviews": weekly_reviews,
            "test_schedule": test_schedule,
            "created": datetime.now().isoformat()
        }

        return plan

    def _allocate_time_by_topic(self, topics: List[str], duration_days: int, daily_hours: float) -> Dict:
        """按主题分配学习时间"""
        topic_allocation = {}
        total_hours = duration_days * daily_hours

        # 为每个主题分配时间（按主题数量均分，但给予重点主题更多时间）
        base_hours_per_topic = total_hours / len(topics)

        for topic in topics:
            # 给第一个主题多一点时间（假设是重点）
            if topic == topics[0]:
                topic_allocation[topic] = base_hours_per_topic * 1.2
            else:
                topic_allocation[topic] = base_hours_per_topic * 0.8

        # 确保总时间匹配
        current_total = sum(topic_allocation.values())
        if abs(current_total - total_hours) > 0.1:
            adjustment = total_hours / current_total
            for topic in topic_allocation:
                topic_allocation[topic] *= adjustment

        return topic_allocation

    def _generate_daily_plans(self, topic_allocation: Dict, break_frequency: int) -> List[Dict]:
        """生成每日学习计划"""
        daily_plans = []
        topics = list(topic_allocation.keys())

        for day in range(1, int(sum(topic_allocation.values()) / topic_allocation[topics[0]]) + 1):
            day_plan = {
                "day": day,
                "date": (datetime.now() + timedelta(days=day-1)).strftime("%Y-%m-%d"),
                "sessions": []
            }

            # 每天的学习会话
            remaining_hours = topic_allocation[topics[0]]  # 假设每天专注于一个主题

            # 创建学习会话
            session_count = max(2, int(remaining_hours / 1.5))  # 每个会话约1.5小时
            session_duration = remaining_hours / session_count

            for session in range(1, session_count + 1):
                start_hour = 9 + (session - 1) * 3  # 从9点开始，每3小时一个会话

                session_plan = {
                    "session": session,
                    "start_time": f"{start_hour:02d}:00",
                    "end_time": f"{start_hour + int(session_duration):02d}:00",
                    "duration_hours": session_duration,
                    "topic": topics[0],  # 每天专注于一个主题
                    "activities": self._generate_session_activities(session_duration, break_frequency)
                }

                day_plan["sessions"].append(session_plan)

            daily_plans.append(day_plan)

        return daily_plans

    def _generate_session_activities(self, duration_hours: float, break_frequency: int) -> List[Dict]:
        """生成学习会话内的活动"""
        activities = []
        total_minutes = int(duration_hours * 60)

        # 学习-休息循环
        study_blocks = []
        current_time = 0

        while current_time < total_minutes:
            # 学习块（45-60分钟）
            study_duration = min(break_frequency, total_minutes - current_time)
            study_blocks.append(study_duration)
            current_time += study_duration + 10  # 10分钟休息

        # 分配活动类型
        activity_types = ["阅读笔记", "做练习", "复习", "总结", "测试"]
        weights = [0.4, 0.3, 0.1, 0.1, 0.1]  # 活动权重

        for block in study_blocks:
            if block > 0:
                activity = random.choices(activity_types, weights=weights)[0]
                activities.append({
                    "type": activity,
                    "duration_minutes": block,
                    "description": self._get_activity_description(activity)
                })

        return activities

    def _get_activity_description(self, activity_type: str) -> str:
        """获取活动描述"""
        descriptions = {
            "阅读笔记": "仔细阅读相关章节，做笔记",
            "做练习": "完成课后练习题",
            "复习": "复习之前学过的内容",
            "总结": "总结当天学习要点",
            "测试": "进行小测验检验理解"
        }
        return descriptions.get(activity_type, "学习相关内容")

    def _generate_weekly_reviews(self, duration_days: int) -> List[Dict]:
        """生成每周复习计划"""
        weekly_reviews = []
        week_number = 1

        for day in range(7, duration_days + 1, 7):
            review_day = min(day, duration_days)
            weekly_reviews.append({
                "week": week_number,
                "review_day": review_day,
                "date": (datetime.now() + timedelta(days=review_day-1)).strftime("%Y-%m-%d"),
                "focus": "复习本周学习内容，查漏补缺"
            })
            week_number += 1

        return weekly_reviews

    def _generate_test_schedule(self, duration_days: int) -> List[Dict]:
        """生成测试计划"""
        test_schedule = []

        # 在学习计划中间和结束时安排测试
        mid_point = duration_days // 2
        end_point = duration_days

        test_schedule.append({
            "test_id": "midterm",
            "name": "期中测试",
            "day": mid_point,
            "date": (datetime.now() + timedelta(days=mid_point-1)).strftime("%Y-%m-%d"),
            "type": "综合测试",
            "duration": 60,  # 分钟
            "focus": "评估前半段学习效果"
        })

        test_schedule.append({
            "test_id": "final",
            "name": "期末测试",
            "day": end_point,
            "date": (datetime.now() + timedelta(days=end_point-1)).strftime("%Y-%m-%d"),
            "type": "综合测试",
            "duration": 90,  # 分钟
            "focus": "全面评估学习成果"
        })

        return test_schedule

    def save_plan(self, plan: Dict, output_path: str = "study_plan.json"):
        """保存学习计划"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(plan, f, indent=2, ensure_ascii=False)
        print(f"Study plan saved to {output_path}")

    def load_plan(self, plan_path: str) -> Dict:
        """加载学习计划"""
        with open(plan_path, 'r', encoding='utf-8') as f:
            return json.load(f)

if __name__ == "__main__":
    import sys
    planner = LearningPlanner()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "generate" and len(sys.argv) > 4:
            duration = int(sys.argv[2])
            topics = sys.argv[3].split(',')
            hours = float(sys.argv[4])
            difficulty = sys.argv[5] if len(sys.argv) > 5 else "medium"

            plan = planner.generate_study_plan(duration, topics, hours, difficulty)
            planner.save_plan(plan)
            print("Study plan generated successfully!")

        elif command == "load" and len(sys.argv) > 2:
            plan_path = sys.argv[2]
            plan = planner.load_plan(plan_path)
            print(f"Loaded plan from {plan_path}")
            print(json.dumps(plan, indent=2))

    else:
        print("Usage:")
        print("  python learning_planner.py generate <duration_days> <topics> <daily_hours> [difficulty]")
        print("  python learning_planner.py load <plan_path>")
