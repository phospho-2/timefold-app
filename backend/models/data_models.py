"""TimefoldAI データモデル定義"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
import json

@dataclass
class Subject:
    """科目データクラス"""
    id: int
    name: str
    code: str = ""
    description: str = ""
    required_equipment: List[str] = field(default_factory=list)
    difficulty_level: str = "medium"  # easy, medium, hard
    category: str = "general"  # general, science, arts, sports
    weekly_hours: int = 1
    created_at: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "description": self.description,
            "required_equipment": self.required_equipment,
            "difficulty_level": self.difficulty_level,
            "category": self.category,
            "weekly_hours": self.weekly_hours,
            "created_at": self.created_at
        }

@dataclass
class Teacher:
    """教師データクラス"""
    id: int
    name: str
    email: str = ""
    subjects: List[str] = field(default_factory=list)
    max_daily_lessons: int = 6
    max_weekly_hours: int = 30
    available_days: List[str] = field(default_factory=lambda: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"])
    available_hours: List[str] = field(default_factory=list)
    preferred_times: List[str] = field(default_factory=list)
    unavailable_times: List[str] = field(default_factory=list)
    employment_type: str = "full_time"
    created_at: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "subjects": self.subjects,
            "max_daily_lessons": self.max_daily_lessons,
            "max_weekly_hours": self.max_weekly_hours,
            "available_days": self.available_days,
            "available_hours": self.available_hours,
            "preferred_times": self.preferred_times,
            "unavailable_times": self.unavailable_times,
            "employment_type": self.employment_type,
            "created_at": self.created_at
        }

@dataclass
class TimeSlot:
    """時間枠データクラス"""
    id: int
    day_of_week: str
    start_time: str
    end_time: str
    period_name: str = ""
    is_break: bool = False
    duration_minutes: int = 50
    created_at: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "day_of_week": self.day_of_week,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "period_name": self.period_name,
            "is_break": self.is_break,
            "duration_minutes": self.duration_minutes,
            "created_at": self.created_at
        }

@dataclass
class StudentGroup:
    """学生グループ（クラス）データクラス"""
    id: int
    name: str
    grade: int
    class_letter: str = "A"
    student_count: int = 30
    curriculum: List[str] = field(default_factory=list)
    special_needs: List[str] = field(default_factory=list)
    created_at: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "grade": self.grade,
            "class_letter": self.class_letter,
            "student_count": self.student_count,
            "curriculum": self.curriculum,
            "special_needs": self.special_needs,
            "created_at": self.created_at
        }

@dataclass
class Lesson:
    """授業データクラス - TimefoldAI用"""
    id: int
    subject: Optional[Subject] = None
    teacher: Optional[Teacher] = None
    student_group: Optional[StudentGroup] = None
    timeslot: Optional[TimeSlot] = None
    duration_minutes: int = 50
    lesson_type: str = "regular"
    requirements: List[str] = field(default_factory=list)
    created_at: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "subject": self.subject.to_dict() if self.subject else None,
            "teacher": self.teacher.to_dict() if self.teacher else None,
            "student_group": self.student_group.to_dict() if self.student_group else None,
            "timeslot": self.timeslot.to_dict() if self.timeslot else None,
            "duration_minutes": self.duration_minutes,
            "lesson_type": self.lesson_type,
            "requirements": self.requirements,
            "created_at": self.created_at
        }
