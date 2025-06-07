"""システム設定管理"""
from dataclasses import dataclass, field
from typing import Dict, List, Any
import json
import os

@dataclass
class SystemConfig:
    """システム設定クラス"""
    # 時間設定
    start_hour: int = 9
    end_hour: int = 16
    lesson_duration: int = 50  # 分
    break_duration: int = 10   # 分
    lunch_break_start: str = "12:00"
    lunch_break_end: str = "13:00"
    
    # 制約設定
    max_daily_lessons_per_teacher: int = 6
    max_consecutive_lessons: int = 3
    min_break_between_lessons: int = 10
    
    # 科目設定
    preferred_morning_subjects: List[str] = field(default_factory=lambda: ["数学", "国語", "英語"])
    preferred_afternoon_subjects: List[str] = field(default_factory=lambda: ["体育", "音楽", "美術"])
    
    # その他設定
    school_name: str = "サンプル学校"
    academic_year: str = "2025"
    semester: str = "1学期"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "start_hour": self.start_hour,
            "end_hour": self.end_hour,
            "lesson_duration": self.lesson_duration,
            "break_duration": self.break_duration,
            "lunch_break_start": self.lunch_break_start,
            "lunch_break_end": self.lunch_break_end,
            "max_daily_lessons_per_teacher": self.max_daily_lessons_per_teacher,
            "max_consecutive_lessons": self.max_consecutive_lessons,
            "min_break_between_lessons": self.min_break_between_lessons,
            "preferred_morning_subjects": self.preferred_morning_subjects,
            "preferred_afternoon_subjects": self.preferred_afternoon_subjects,
            "school_name": self.school_name,
            "academic_year": self.academic_year,
            "semester": self.semester
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SystemConfig':
        return cls(**data)
    
    def save(self, file_path: str):
        """設定をファイルに保存"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
    
    @classmethod
    def load(cls, file_path: str) -> 'SystemConfig':
        """ファイルから設定を読み込み"""
        if not os.path.exists(file_path):
            # デフォルト設定を作成
            config = cls()
            config.save(file_path)
            return config
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return cls.from_dict(data)
    
    def generate_timeslots(self) -> List[Dict[str, Any]]:
        """設定に基づいて時間枠を生成"""
        timeslots = []
        days = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"]
        
        slot_id = 1
        
        for day in days:
            daily_hour = self.start_hour
            daily_minute = 0
            daily_period = 1
            
            while daily_hour < self.end_hour:
                # 昼休み時間をスキップ
                current_time = f"{daily_hour:02d}:{daily_minute:02d}"
                if self.lunch_break_start <= current_time < self.lunch_break_end:
                    # 昼休み終了時刻に進める
                    lunch_end_parts = self.lunch_break_end.split(":")
                    daily_hour = int(lunch_end_parts[0])
                    daily_minute = int(lunch_end_parts[1])
                    continue
                
                # 終了時刻の計算
                end_minute = daily_minute + self.lesson_duration
                end_hour = daily_hour
                
                if end_minute >= 60:
                    end_hour += end_minute // 60
                    end_minute = end_minute % 60
                
                # 終了時刻が営業時間を超えていないかチェック
                if end_hour > self.end_hour or (end_hour == self.end_hour and end_minute > 0):
                    break
                
                timeslot = {
                    "id": slot_id,
                    "day_of_week": day,
                    "start_time": f"{daily_hour:02d}:{daily_minute:02d}",
                    "end_time": f"{end_hour:02d}:{end_minute:02d}",
                    "period_name": f"{daily_period}限",
                    "is_break": False,
                    "duration_minutes": self.lesson_duration
                }
                timeslots.append(timeslot)
                
                # 次の時間枠へ
                daily_minute += self.lesson_duration + self.break_duration
                if daily_minute >= 60:
                    daily_hour += daily_minute // 60
                    daily_minute = daily_minute % 60
                
                slot_id += 1
                daily_period += 1
        
        return timeslots
