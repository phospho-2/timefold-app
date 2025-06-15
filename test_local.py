#!/usr/bin/env python3
"""ローカルでの動作テスト"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from backend.app import create_app

def test_app_creation():
    """アプリケーション作成テスト"""
    print("🧪 アプリケーション作成テスト開始")
    try:
        app = create_app()
        print("✅ アプリケーション作成成功")
        return app
    except Exception as e:
        print(f"❌ アプリケーション作成失敗: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_api_routes(app):
    """APIルートテスト"""
    print("🧪 APIルートテスト開始")
    try:
        with app.test_client() as client:
            # Health check
            response = client.get('/api/test')
            print(f"📍 /api/test: {response.status_code}")
            print(f"   Response: {response.get_json()}")
            
            # Demo data
            response = client.get('/api/demo-data')
            print(f"📍 /api/demo-data: {response.status_code}")
            
            # Subjects
            response = client.get('/api/subjects')
            print(f"📍 /api/subjects: {response.status_code}")
            
            # Teachers
            response = client.get('/api/teachers')
            print(f"📍 /api/teachers: {response.status_code}")
            
            print("✅ APIルートテスト完了")
            return True
    except Exception as e:
        print(f"❌ APIルートテスト失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_data_layer():
    """データレイヤーテスト"""
    print("🧪 データレイヤーテスト開始")
    try:
        from backend.models.database import JSONDataRepository
        repo = JSONDataRepository()
        
        subjects = repo.get_subjects()
        teachers = repo.get_teachers()
        timeslots = repo.get_timeslots()
        student_groups = repo.get_student_groups()
        
        print(f"📚 科目数: {len(subjects)}")
        print(f"👨‍🏫 教師数: {len(teachers)}")
        print(f"⏰ 時間枠数: {len(timeslots)}")
        print(f"👥 学生グループ数: {len(student_groups)}")
        
        print("✅ データレイヤーテスト完了")
        return True
    except Exception as e:
        print(f"❌ データレイヤーテスト失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🚀 ローカル動作テスト開始")
    
    # アプリケーション作成テスト
    app = test_app_creation()
    if not app:
        print("❌ アプリケーション作成に失敗したため、テストを中止")
        return False
    
    # データレイヤーテスト
    if not test_data_layer():
        print("❌ データレイヤーテストに失敗")
        return False
    
    # APIルートテスト
    if not test_api_routes(app):
        print("❌ APIルートテストに失敗")
        return False
    
    print("🎉 全テスト完了")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)