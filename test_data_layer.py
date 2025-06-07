"""データレイヤーのテストスクリプト"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from backend.models.database import JSONDataRepository
from backend.models.data_models import Subject, Teacher

def test_data_repository():
    """データリポジトリのテスト"""
    print("🧪 データリポジトリテスト開始")
    
    # リポジトリの初期化
    repo = JSONDataRepository("backend/data")
    
    # データの取得テスト
    subjects = repo.get_subjects()
    teachers = repo.get_teachers()
    timeslots = repo.get_timeslots()
    student_groups = repo.get_student_groups()
    
    print(f"📚 科目数: {len(subjects)}")
    for subject in subjects:
        print(f"  - {subject.name} ({subject.category})")
    
    print(f"👨‍🏫 教師数: {len(teachers)}")
    for teacher in teachers:
        print(f"  - {teacher.name}: {', '.join(teacher.subjects)}")
    
    print(f"⏰ 時間枠数: {len(timeslots)}")
    print(f"👥 学生グループ数: {len(student_groups)}")
    
    # 授業生成テスト
    lessons = repo.generate_lessons()
    print(f"📖 生成された授業数: {len(lessons)}")
    
    for lesson in lessons[:5]:  # 最初の5つだけ表示
        if lesson.subject and lesson.teacher and lesson.student_group:
            print(f"  - {lesson.subject.name} by {lesson.teacher.name} for {lesson.student_group.name}")
    
    print("✅ データリポジトリテスト完了")
    return True

if __name__ == "__main__":
    test_data_repository()
