"""データベース抽象化レイヤー"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
import json
import os
from .data_models import Subject, Teacher, TimeSlot, StudentGroup, Lesson

class DataRepository(ABC):
    """データリポジトリの抽象基底クラス"""
    
    @abstractmethod
    def get_subjects(self) -> List[Subject]:
        pass
    
    @abstractmethod
    def get_teachers(self) -> List[Teacher]:
        pass
    
    @abstractmethod
    def get_timeslots(self) -> List[TimeSlot]:
        pass
    
    @abstractmethod
    def get_student_groups(self) -> List[StudentGroup]:
        pass
    
    @abstractmethod
    def save_subject(self, subject: Subject) -> Subject:
        pass
    
    @abstractmethod
    def save_teacher(self, teacher: Teacher) -> Teacher:
        pass

class JSONDataRepository(DataRepository):
    """JSONベースのデータリポジトリ"""
    
    def __init__(self, data_dir: str = "backend/data"):
        self.data_dir = data_dir
        self.ensure_data_dir()
        self._subjects = []
        self._teachers = []
        self._timeslots = []
        self._student_groups = []
        self.load_all_data()
    
    def ensure_data_dir(self):
        """データディレクトリの確保"""
        os.makedirs(self.data_dir, exist_ok=True)
    
    def load_all_data(self):
        """全データの読み込み"""
        self._subjects = self._load_subjects()
        self._teachers = self._load_teachers()
        self._timeslots = self._load_timeslots()
        self._student_groups = self._load_student_groups()
    
    def _load_subjects(self) -> List[Subject]:
        """科目データの読み込み"""
        file_path = os.path.join(self.data_dir, "subjects.json")
        if not os.path.exists(file_path):
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Subject(**item) for item in data]
        except Exception as e:
            print(f"科目データ読み込みエラー: {e}")
            return []
    
    def _load_teachers(self) -> List[Teacher]:
        """教師データの読み込み"""
        file_path = os.path.join(self.data_dir, "teachers.json")
        if not os.path.exists(file_path):
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Teacher(**item) for item in data]
        except Exception as e:
            print(f"教師データ読み込みエラー: {e}")
            return []
    
    def _load_timeslots(self) -> List[TimeSlot]:
        """時間枠データの読み込み（カスタマイズ設定から動的生成）"""
        # システム設定を読み込み
        config = self._load_system_config()
        
        # デフォルト設定
        start_hour = config.get('start_hour', 9)
        end_hour = config.get('end_hour', 16)
        lesson_duration = config.get('lesson_duration', 50)
        break_duration = config.get('break_duration', 10)
        
        # 昼休み設定
        lunch_start_hour = 12
        lunch_end_hour = 13
        
        print(f"⏰ 時間枠生成設定:")
        print(f"   開始時刻: {start_hour}時")
        print(f"   終了時刻: {end_hour}時")
        print(f"   授業時間: {lesson_duration}分")
        print(f"   休憩時間: {break_duration}分")
        
        timeslots = []
        days = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"]
        day_names = ["月曜日", "火曜日", "水曜日", "木曜日", "金曜日"]
        
        slot_id = 1
        
        for day_index, day in enumerate(days):
            current_hour = start_hour
            current_minute = 0
            period_num = 1
            
            while current_hour < end_hour:
                # 昼休み時間帯をスキップ
                if current_hour >= lunch_start_hour and current_hour < lunch_end_hour:
                    current_hour = lunch_end_hour
                    current_minute = 0
                    continue
                
                # 授業終了時刻を計算
                end_minute = current_minute + lesson_duration
                end_hour_calc = current_hour
                
                if end_minute >= 60:
                    end_hour_calc += end_minute // 60
                    end_minute = end_minute % 60
                
                # 終了時刻が設定範囲を超える場合は終了
                if end_hour_calc > end_hour or (end_hour_calc == end_hour and end_minute > 0):
                    break
                
                # 時間枠を作成
                start_time = f"{current_hour:02d}:{current_minute:02d}"
                end_time = f"{end_hour_calc:02d}:{end_minute:02d}"
                
                timeslot = TimeSlot(
                    id=slot_id,
                    day_of_week=day,
                    start_time=start_time,
                    end_time=end_time,
                    period_name=f"{period_num}限",
                    duration_minutes=lesson_duration
                )
                timeslots.append(timeslot)
                
                print(f"   🕒 {day_names[day_index]} {period_num}限: {start_time}-{end_time}")
                
                # 次の時間帯を計算（授業時間 + 休憩時間）
                next_minute = current_minute + lesson_duration + break_duration
                current_hour += next_minute // 60
                current_minute = next_minute % 60
                
                slot_id += 1
                period_num += 1
        
        print(f"📊 生成された時間枠数: {len(timeslots)}")
        return timeslots
    
    def _load_system_config(self) -> Dict[str, Any]:
        """システム設定の読み込み"""
        config_file = os.path.join(self.data_dir, "system_config.json")
        
        # デフォルト設定
        default_config = {
            "start_hour": 9,
            "end_hour": 16,
            "lesson_duration": 50,
            "break_duration": 10,
            "school_name": "サンプル学校"
        }
        
        if not os.path.exists(config_file):
            # デフォルト設定ファイルを作成
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, ensure_ascii=False, indent=2)
            print("📝 デフォルトのシステム設定ファイルを作成しました")
            return default_config
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                print(f"📋 システム設定読み込み: {config}")
                return config
        except Exception as e:
            print(f"⚠️ 設定ファイル読み込みエラー: {e}")
            return default_config
    
    def _load_student_groups(self) -> List[StudentGroup]:
        """学生グループの読み込み（デモ用：1クラスのみ）"""
        return [
            StudentGroup(
                id=1,
                name="1年A組",
                grade=1,
                class_letter="A", 
                student_count=30,
                curriculum=["数学", "国語", "英語"]
            )
        ]
    
    def _save_subjects(self, subjects: List[Subject]):
        """科目データの保存"""
        file_path = os.path.join(self.data_dir, "subjects.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump([s.to_dict() for s in subjects], f, ensure_ascii=False, indent=2)
        print(f"📚 科目データ保存完了: {len(subjects)}件")
    
    def _save_teachers(self, teachers: List[Teacher]):
        """教師データの保存"""
        file_path = os.path.join(self.data_dir, "teachers.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump([t.to_dict() for t in teachers], f, ensure_ascii=False, indent=2)
        print(f"👨‍🏫 教師データ保存完了: {len(teachers)}件")
    
    def save_system_config(self, config: Dict[str, Any]) -> bool:
        """システム設定の保存"""
        try:
            config_file = os.path.join(self.data_dir, "system_config.json")
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            print(f"💾 システム設定保存完了: {config}")
            # 設定変更後に時間枠を再生成
            self._timeslots = self._load_timeslots()
            return True
        except Exception as e:
            print(f"❌ 設定保存エラー: {e}")
            return False
    
    # 抽象メソッドの実装
    def get_subjects(self) -> List[Subject]:
        return self._subjects.copy()
    
    def get_teachers(self) -> List[Teacher]:
        return self._teachers.copy()
    
    def get_timeslots(self) -> List[TimeSlot]:
        return self._timeslots.copy()
    
    def get_student_groups(self) -> List[StudentGroup]:
        return self._student_groups.copy()
    
    def save_subject(self, subject: Subject) -> Subject:
        # 既存の科目を更新または新規追加
        found = False
        for i, s in enumerate(self._subjects):
            if s.id == subject.id:
                self._subjects[i] = subject
                found = True
                break
        
        if not found:
            self._subjects.append(subject)
        
        # ファイルに保存
        self._save_subjects(self._subjects)
        print(f"✅ 科目保存: {subject.name} (ID: {subject.id})")
        return subject
    
    def save_teacher(self, teacher: Teacher) -> Teacher:
        # 既存の教師を更新または新規追加
        found = False
        for i, t in enumerate(self._teachers):
            if t.id == teacher.id:
                self._teachers[i] = teacher
                found = True
                break
        
        if not found:
            self._teachers.append(teacher)
        
        # ファイルに保存
        self._save_teachers(self._teachers)
        print(f"✅ 教師保存: {teacher.name} (ID: {teacher.id})")
        return teacher
    
    def delete_subject(self, subject_id: int) -> bool:
        """科目を削除"""
        original_count = len(self._subjects)
        self._subjects = [s for s in self._subjects if s.id != subject_id]
        
        if len(self._subjects) < original_count:
            self._save_subjects(self._subjects)
            print(f"🗑️ 科目削除: ID {subject_id}")
            return True
        return False
    
    def delete_teacher(self, teacher_id: int) -> bool:
        """教師を削除"""
        original_count = len(self._teachers)
        self._teachers = [t for t in self._teachers if t.id != teacher_id]
        
        if len(self._teachers) < original_count:
            self._save_teachers(self._teachers)
            print(f"🗑️ 教師削除: ID {teacher_id}")
            return True
        return False
    
    def generate_lessons(self) -> List[Lesson]:
        """授業リストの生成（週時間数を考慮）"""
        lessons = []
        lesson_id = 1
        
        subjects = self.get_subjects()
        teachers = self.get_teachers()
        student_groups = self.get_student_groups()
        
        for student_group in student_groups:
            for subject in subjects:
                teacher = self._find_teacher_for_subject(teachers, subject.name)
                if teacher:
                    # 週時間数分だけ授業を生成
                    weekly_hours = getattr(subject, 'weekly_hours', 1)
                    for hour in range(weekly_hours):
                        lesson = Lesson(
                            id=lesson_id,
                            subject=subject,
                            teacher=teacher,
                            student_group=student_group,
                            lesson_type="regular"
                        )
                        lessons.append(lesson)
                        lesson_id += 1
        
        return lessons
    
    def _find_teacher_for_subject(self, teachers: List[Teacher], subject_name: str) -> Optional[Teacher]:
        """科目に対応する教師を検索"""
        for teacher in teachers:
            if subject_name in teacher.subjects:
                return teacher
        return None