"""カスタマイズサービス"""
from typing import Dict, List, Any, Optional
from ..models.config import SystemConfig
from ..models.database import JSONDataRepository
from ..models.data_models import Subject, Teacher, TimeSlot

class CustomizeService:
    """カスタマイズ機能のサービスクラス"""
    
    def __init__(self, data_dir: str = "backend/data"):
        self.data_repo = JSONDataRepository(data_dir)
        self.config_file = f"{data_dir}/system_config.json"
        self.config = SystemConfig.load(self.config_file)
    
    def get_current_config(self) -> Dict[str, Any]:
        """現在の設定を取得"""
        return self.config.to_dict()
    
    def update_config(self, config_data: Dict[str, Any]) -> Dict[str, str]:
        """設定を更新"""
        try:
            # 既存設定を更新
            for key, value in config_data.items():
                if hasattr(self.config, key):
                    setattr(self.config, key, value)
            
            # 設定を保存
            self.config.save(self.config_file)
            
            # 時間枠を再生成
            self._regenerate_timeslots()
            
            return {"status": "success", "message": "設定が更新されました"}
            
        except Exception as e:
            return {"status": "error", "message": f"設定更新エラー: {str(e)}"}
    
    def _regenerate_timeslots(self):
        """設定に基づいて時間枠を再生成"""
        try:
            new_timeslots_data = self.config.generate_timeslots()
            
            # TimeSlotオブジェクトに変換
            new_timeslots = []
            for ts_data in new_timeslots_data:
                timeslot = TimeSlot(**ts_data)
                new_timeslots.append(timeslot)
            
            # データリポジトリの時間枠を更新
            self.data_repo._timeslots = new_timeslots
            
        except Exception as e:
            print(f"時間枠再生成エラー: {e}")
    
    def add_custom_subject(self, subject_data: Dict[str, Any]) -> Dict[str, Any]:
        """カスタム科目の追加"""
        try:
            # データリポジトリを再読み込みして最新の状態を取得
            self.data_repo.load_all_data()
            
            # IDの自動採番
            existing_subjects = self.data_repo.get_subjects()
            new_id = max([s.id for s in existing_subjects], default=0) + 1
            
            subject_data['id'] = new_id
            subject = Subject(**subject_data)
            
            saved_subject = self.data_repo.save_subject(subject)
            
            return {
                "status": "success",
                "message": f"科目 '{subject.name}' が追加されました",
                "subject": saved_subject.to_dict()
            }
            
        except Exception as e:
            print(f"科目追加エラー詳細: {e}")
            return {"status": "error", "message": f"科目追加エラー: {str(e)}"}
    
    def add_custom_teacher(self, teacher_data: Dict[str, Any]) -> Dict[str, Any]:
        """カスタム教師の追加"""
        try:
            # データリポジトリを再読み込みして最新の状態を取得
            self.data_repo.load_all_data()
            
            # IDの自動採番
            existing_teachers = self.data_repo.get_teachers()
            new_id = max([t.id for t in existing_teachers], default=0) + 1
            
            teacher_data['id'] = new_id
            teacher = Teacher(**teacher_data)
            
            saved_teacher = self.data_repo.save_teacher(teacher)
            
            return {
                "status": "success",
                "message": f"教師 '{teacher.name}' が追加されました",
                "teacher": saved_teacher.to_dict()
            }
            
        except Exception as e:
            print(f"教師追加エラー詳細: {e}")
            return {"status": "error", "message": f"教師追加エラー: {str(e)}"}
    
    def delete_subject(self, subject_id: int) -> Dict[str, str]:
        """科目の削除"""
        try:
            success = self.data_repo.delete_subject(subject_id)
            
            if success:
                return {"status": "success", "message": "科目が削除されました"}
            else:
                return {"status": "error", "message": "指定された科目が見つかりません"}
            
        except Exception as e:
            return {"status": "error", "message": f"科目削除エラー: {str(e)}"}
    
    def delete_teacher(self, teacher_id: int) -> Dict[str, str]:
        """教師の削除"""
        try:
            success = self.data_repo.delete_teacher(teacher_id)
            
            if success:
                return {"status": "success", "message": "教師が削除されました"}
            else:
                return {"status": "error", "message": "指定された教師が見つかりません"}
            
        except Exception as e:
            return {"status": "error", "message": f"教師削除エラー: {str(e)}"}
    
    def preview_timeslots(self, temp_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """設定変更のプレビュー用時間枠生成"""
        try:
            # 一時的な設定オブジェクトを作成
            temp_system_config = SystemConfig.from_dict({
                **self.config.to_dict(),
                **temp_config
            })
            
            return temp_system_config.generate_timeslots()
            
        except Exception as e:
            print(f"プレビュー生成エラー: {e}")
            return []
    
    def get_customization_stats(self) -> Dict[str, Any]:
        """カスタマイズ統計情報"""
        # 最新データを読み込み
        self.data_repo.load_all_data()
        
        subjects = self.data_repo.get_subjects()
        teachers = self.data_repo.get_teachers()
        timeslots = self.data_repo.get_timeslots()
        
        return {
            "total_subjects": len(subjects),
            "total_teachers": len(teachers),
            "total_timeslots": len(timeslots),
            "daily_timeslots": len(timeslots) // 5 if len(timeslots) > 0 else 0,
            "config": self.config.to_dict(),
            "subjects_by_category": self._group_subjects_by_category(subjects),
            "teachers_by_type": self._group_teachers_by_type(teachers)
        }
    
    def _group_subjects_by_category(self, subjects: List[Subject]) -> Dict[str, int]:
        """科目をカテゴリ別にグループ化"""
        categories = {}
        for subject in subjects:
            category = subject.category
            categories[category] = categories.get(category, 0) + 1
        return categories
    
    def _group_teachers_by_type(self, teachers: List[Teacher]) -> Dict[str, int]:
        """教師を雇用形態別にグループ化"""
        types = {}
        for teacher in teachers:
            emp_type = teacher.employment_type
            types[emp_type] = types.get(emp_type, 0) + 1
        return types
