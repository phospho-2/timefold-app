from dataclasses import dataclass, field
from datetime import time
from typing import List, Optional, Annotated

# 🎯 正しいTimefold API実装 - 公式ドキュメント準拠
from timefold.solver.domain import (
    planning_solution, planning_entity, PlanningVariable, PlanningId, ValueRangeProvider,
    ProblemFactCollectionProperty, PlanningEntityCollectionProperty, PlanningScore
)
from timefold.solver.score import (
    HardSoftScore, constraint_provider, Joiners, ConstraintFactory, Constraint
)

# ドメインクラス定義 - Problem Facts
@dataclass
class Timeslot:
    id: int
    day_of_week: str
    start_time: time
    end_time: time
    
    def __str__(self):
        return f"{self.day_of_week} {self.start_time.strftime('%H:%M')}-{self.end_time.strftime('%H:%M')}"

@dataclass
class Room:
    id: int
    name: str
    
    def __str__(self):
        return self.name

@dataclass
class Subject:
    id: int
    name: str
    
    def __str__(self):
        return self.name

@dataclass
class Teacher:
    id: int
    name: str
    
    def __str__(self):
        return self.name

@dataclass
class StudentGroup:
    id: int
    name: str
    
    def __str__(self):
        return self.name

# 🎯 Planning Entity - 公式ドキュメント準拠の正しい構文
@planning_entity
@dataclass
class Lesson:
    id: Annotated[int, PlanningId]
    subject: Subject
    teacher: Teacher
    student_group: StudentGroup
    
    # 🚀 正しいPlanningVariable構文（公式ドキュメントより）
    timeslot: Annotated[Timeslot | None, PlanningVariable] = field(default=None)
    room: Annotated[Room | None, PlanningVariable] = field(default=None)
    
    def __str__(self):
        return f"{self.subject} - {self.teacher} - {self.student_group}"

# 🧠 制約定義 - 強化版制約システム
@constraint_provider
def define_constraints(constraint_factory: ConstraintFactory):
    return [
        # Hard constraints (絶対条件)
        room_conflict(constraint_factory),
        teacher_conflict(constraint_factory),
        student_group_conflict(constraint_factory),
        
        # Soft constraints (最適化条件) - 強化版
        subject_distribution_across_days(constraint_factory),  # 最優先・強化
        daily_lesson_limit(constraint_factory),               # 新規追加
        encourage_subject_spread(constraint_factory),         # 新規追加
        avoid_consecutive_same_subject(constraint_factory),
        teacher_room_stability(constraint_factory),
        teacher_time_efficiency(constraint_factory),
    ]

def room_conflict(constraint_factory: ConstraintFactory) -> Constraint:
    """Hard: 同じ時間帯に同じ教室で複数の授業は不可"""
    return (constraint_factory
            .for_each_unique_pair(Lesson,
                Joiners.equal(lambda lesson: lesson.timeslot),
                Joiners.equal(lambda lesson: lesson.room))
            .filter(lambda lesson1, lesson2: 
                lesson1.timeslot is not None and lesson2.timeslot is not None and 
                lesson1.room is not None and lesson2.room is not None)
            .penalize(HardSoftScore.ONE_HARD)
            .as_constraint("Room conflict"))

def teacher_conflict(constraint_factory: ConstraintFactory) -> Constraint:
    """Hard: 同じ時間帯に同じ先生が複数の授業は不可"""
    return (constraint_factory
            .for_each_unique_pair(Lesson,
                Joiners.equal(lambda lesson: lesson.timeslot),
                Joiners.equal(lambda lesson: lesson.teacher))
            .filter(lambda lesson1, lesson2: lesson1.timeslot is not None and lesson2.timeslot is not None)
            .penalize(HardSoftScore.ONE_HARD)
            .as_constraint("Teacher conflict"))

def student_group_conflict(constraint_factory: ConstraintFactory) -> Constraint:
    """Hard: 同じ時間帯に同じクラスが複数の授業は不可"""
    return (constraint_factory
            .for_each_unique_pair(Lesson,
                Joiners.equal(lambda lesson: lesson.timeslot),
                Joiners.equal(lambda lesson: lesson.student_group))
            .filter(lambda lesson1, lesson2: lesson1.timeslot is not None and lesson2.timeslot is not None)
            .penalize(HardSoftScore.ONE_HARD)
            .as_constraint("Student group conflict"))

def subject_distribution_across_days(constraint_factory: ConstraintFactory) -> Constraint:
    """Soft: 同じ科目の授業は異なる曜日に分散させる（強化版）"""
    return (constraint_factory
            .for_each_unique_pair(Lesson,
                Joiners.equal(lambda lesson: lesson.subject.id),  # IDで比較に変更
                Joiners.equal(lambda lesson: lesson.student_group.id))  # IDで比較に変更
            .filter(lambda lesson1, lesson2:
                lesson1.timeslot is not None and lesson2.timeslot is not None and
                lesson1.timeslot.day_of_week == lesson2.timeslot.day_of_week and
                lesson1.id != lesson2.id)  # 同一授業除外
            .penalize(HardSoftScore.of(0, 10))  # ペナルティを10倍に強化
            .as_constraint("Subject distribution across days"))

def daily_lesson_limit(constraint_factory: ConstraintFactory) -> Constraint:
    """Soft: 1日の授業数制限（新規追加）"""
    return (constraint_factory
            .for_each_unique_pair(Lesson)
            .filter(lambda lesson1, lesson2:
                lesson1.timeslot is not None and lesson2.timeslot is not None and
                lesson1.student_group.id == lesson2.student_group.id and
                lesson1.timeslot.day_of_week == lesson2.timeslot.day_of_week and
                lesson1.id != lesson2.id)
            .penalize(HardSoftScore.of(0, 5))  # 1日複数授業にペナルティ
            .as_constraint("Daily lesson limit"))

def encourage_subject_spread(constraint_factory: ConstraintFactory) -> Constraint:
    """Soft: 科目を週全体に分散させる（新規追加）"""
    return (constraint_factory
            .for_each_unique_pair(Lesson,
                Joiners.equal(lambda lesson: lesson.subject.id),
                Joiners.equal(lambda lesson: lesson.student_group.id))
            .filter(lambda lesson1, lesson2:
                lesson1.timeslot is not None and lesson2.timeslot is not None and
                lesson1.timeslot.day_of_week != lesson2.timeslot.day_of_week and
                lesson1.id != lesson2.id)
            .reward(HardSoftScore.of(0, 8))  # 異なる日配置に大きな報酬
            .as_constraint("Encourage subject spread"))

def avoid_consecutive_same_subject(constraint_factory: ConstraintFactory) -> Constraint:
    """Soft: 同じ科目の連続授業を避ける（疲労軽減）"""
    return (constraint_factory
            .for_each_unique_pair(Lesson,
                Joiners.equal(lambda lesson: lesson.subject.id),  # IDで比較に変更
                Joiners.equal(lambda lesson: lesson.student_group.id))  # IDで比較に変更
            .filter(lambda lesson1, lesson2:
                lesson1.timeslot is not None and lesson2.timeslot is not None and
                lesson1.timeslot.day_of_week == lesson2.timeslot.day_of_week and
                abs(lesson1.timeslot.id - lesson2.timeslot.id) == 1 and  # 連続する時間帯
                lesson1.id != lesson2.id)  # 同一授業除外
            .penalize(HardSoftScore.of(0, 3))
            .as_constraint("Avoid consecutive same subject"))

def teacher_room_stability(constraint_factory: ConstraintFactory) -> Constraint:
    """Soft: 同じ先生はできるだけ同じ教室を使う（効率性向上）"""
    return (constraint_factory
            .for_each_unique_pair(Lesson,
                Joiners.equal(lambda lesson: lesson.teacher))
            .filter(lambda lesson1, lesson2: 
                lesson1.room is not None and lesson2.room is not None and 
                lesson1.room.id != lesson2.room.id)
            .penalize(HardSoftScore.ONE_SOFT)
            .as_constraint("Teacher room stability"))

def teacher_time_efficiency(constraint_factory: ConstraintFactory) -> Constraint:
    """Soft: 同じ先生の授業は連続する時間帯が理想的（移動効率）"""
    return (constraint_factory
            .for_each_unique_pair(Lesson,
                Joiners.equal(lambda lesson: lesson.teacher))
            .filter(lambda lesson1, lesson2:
                lesson1.timeslot is not None and lesson2.timeslot is not None and
                lesson1.timeslot.day_of_week == lesson2.timeslot.day_of_week and
                abs(lesson1.timeslot.id - lesson2.timeslot.id) > 1)
            .penalize(HardSoftScore.ONE_SOFT)
            .as_constraint("Teacher time efficiency"))

# 🎯 Planning Solution - 公式ドキュメント準拠の正しい構文
@planning_solution
@dataclass  
class TimeTable:
    timeslots: Annotated[List[Timeslot], ProblemFactCollectionProperty, ValueRangeProvider] = field(default_factory=list)
    rooms: Annotated[List[Room], ProblemFactCollectionProperty, ValueRangeProvider] = field(default_factory=list)
    lessons: Annotated[List[Lesson], PlanningEntityCollectionProperty] = field(default_factory=list)
    score: Annotated[HardSoftScore | None, PlanningScore] = field(default=None)