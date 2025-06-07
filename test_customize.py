"""カスタマイズ機能のテストスクリプト"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from backend.services.customize_service import CustomizeService

def test_customize_service():
    """カスタマイズサービスのテスト"""
    print("🧪 カスタマイズサービステスト開始")
    
    # サービスの初期化
    service = CustomizeService("backend/data")
    
    # 現在の設定取得
    config = service.get_current_config()
    print(f"⚙️  現在の設定:")
    print(f"  - 開始時刻: {config['start_hour']}時")
    print(f"  - 終了時刻: {config['end_hour']}時")
    print(f"  - 授業時間: {config['lesson_duration']}分")
    print(f"  - 休憩時間: {config['break_duration']}分")
    
    # 統計情報取得
    stats = service.get_customization_stats()
    print(f"📊 統計情報:")
    print(f"  - 科目数: {stats['total_subjects']}")
    print(f"  - 教師数: {stats['total_teachers']}")
    print(f"  - 時間枠数: {stats['total_timeslots']}")
    print(f"  - 1日の時間枠数: {stats['daily_timeslots']}")
    
    # カスタム科目追加テスト
    new_subject = {
        "name": "情報",
        "code": "INFO",
        "description": "情報技術の授業",
        "category": "technology",
        "weekly_hours": 2
    }
    
    result = service.add_custom_subject(new_subject)
    if result["status"] == "success":
        print(f"✅ {result['message']}")
    else:
        print(f"❌ {result['message']}")
    
    # カスタム教師追加テスト
    new_teacher = {
        "name": "山田先生",
        "email": "yamada@school.jp",
        "subjects": ["情報"],
        "employment_type": "full_time"
    }
    
    result = service.add_custom_teacher(new_teacher)
    if result["status"] == "success":
        print(f"✅ {result['message']}")
    else:
        print(f"❌ {result['message']}")
    
    # 設定更新テスト
    new_config = {
        "start_hour": 8,
        "end_hour": 17,
        "lesson_duration": 45
    }
    
    result = service.update_config(new_config)
    if result["status"] == "success":
        print(f"✅ {result['message']}")
        
        # 更新後の統計情報
        updated_stats = service.get_customization_stats()
        print(f"📊 更新後の時間枠数: {updated_stats['total_timeslots']}")
    else:
        print(f"❌ {result['message']}")
    
    print("✅ カスタマイズサービステスト完了")

if __name__ == "__main__":
    test_customize_service()
