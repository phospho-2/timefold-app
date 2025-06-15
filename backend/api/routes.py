"""API ルート定義"""
import os
from flask import Blueprint, request, jsonify
from ..models.database import JSONDataRepository
from ..models.data_models import Subject, Teacher
from backend.services.optimization_service import OptimizationService

# Blueprint の作成（最初に定義）
api_bp = Blueprint('api', __name__)

# 最適化サービスのインスタンス化
optimization_service = OptimizationService()

# グローバルなデータリポジトリ（シングルトン）
_data_repo = None

def get_data_repository():
    """データリポジトリのシングルトン取得"""
    global _data_repo
    if _data_repo is None:
        _data_repo = JSONDataRepository("backend/data")
    else:
        # 最新データを再読み込み
        _data_repo.load_all_data()
    return _data_repo

# 最適化関連のエンドポイント
@api_bp.route('/demo-data', methods=['GET'])
def get_demo_data():
    """デモデータを返す（最新データで生成）"""
    try:
        print("🎯 デモデータ生成中...")
        # 🔧 重要: 新しいインスタンスを作成して最新データを取得
        fresh_optimization_service = OptimizationService()
        timetable = fresh_optimization_service.generate_demo_data()
        result = fresh_optimization_service.convert_to_json(timetable)
        print("✅ デモデータ生成完了")
        return jsonify(result)
    except Exception as e:
        print(f"❌ デモデータ生成エラー: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@api_bp.route('/optimize', methods=['POST'])
def optimize_timetable():
    """🎯 Railway対応 軽量最適化エンドポイント"""
    try:
        print("🎯 最適化リクエスト受信")
        
        # Railway環境検出
        is_railway = 'RAILWAY_ENVIRONMENT' in os.environ
        
        if is_railway:
            # Railway環境では軽量版デモデータを返す
            print("🚂 Railway環境: 軽量デモデータを返送")
            return jsonify({
                "timeslots": [
                    {"id": 1, "day_of_week": "月曜日", "start_time": "09:00", "end_time": "10:00"},
                    {"id": 2, "day_of_week": "月曜日", "start_time": "10:15", "end_time": "11:15"},
                    {"id": 3, "day_of_week": "火曜日", "start_time": "09:00", "end_time": "10:00"},
                    {"id": 4, "day_of_week": "火曜日", "start_time": "10:15", "end_time": "11:15"}
                ],
                "rooms": [
                    {"id": 1, "name": "教室A"},
                    {"id": 2, "name": "教室B"}
                ],
                "lessons": [
                    {
                        "id": 1,
                        "subject": {"id": 1, "name": "数学"},
                        "teacher": {"id": 1, "name": "田中先生"},
                        "student_group": {"id": 1, "name": "1年A組"},
                        "timeslot": {"id": 1, "day_of_week": "月曜日", "start_time": "09:00", "end_time": "10:00"},
                        "room": {"id": 1, "name": "教室A"}
                    },
                    {
                        "id": 2,
                        "subject": {"id": 2, "name": "国語"},
                        "teacher": {"id": 2, "name": "佐藤先生"},
                        "student_group": {"id": 1, "name": "1年A組"},
                        "timeslot": {"id": 2, "day_of_week": "月曜日", "start_time": "10:15", "end_time": "11:15"},
                        "room": {"id": 1, "name": "教室A"}
                    }
                ],
                "score": "Perfect (Railway Demo)"
            })
        
        # ローカル環境では本格最適化
        print("🖥️ ローカル環境: 本格最適化実行")
        fresh_optimization_service = OptimizationService()
        
        data = request.get_json()
        if not data:
            timetable = fresh_optimization_service.generate_demo_data()
        else:
            timetable = fresh_optimization_service.convert_from_json(data)
        
        solution = fresh_optimization_service.optimize_timetable(timetable)
        result = fresh_optimization_service.convert_to_json(solution)
        
        print("🎉 最適化完了 - 結果を返送")
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ 最適化エラー: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@api_bp.route('/refresh-cache', methods=['POST'])
def refresh_cache():
    """キャッシュを強制更新（新規追加）"""
    try:
        # グローバルな最適化サービスを再作成
        global optimization_service
        optimization_service = OptimizationService()
        
        return jsonify({
            "status": "success",
            "message": "キャッシュを更新しました"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"キャッシュ更新エラー: {e}"
        }), 500

@api_bp.route('/optimization-status', methods=['GET'])
def get_optimization_status():
    """最適化機能の状態確認"""
    try:
        # TimefoldAIの動作確認
        from timefold.solver import SolverFactory
        return jsonify({
            "status": "ready",
            "message": "TimefoldAI最適化エンジン準備完了",
            "version": "TimefoldAI v6 本格版"
        })
    except ImportError as e:
        return jsonify({
            "status": "error", 
            "message": f"TimefoldAI未インストール: {e}"
        }), 500
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"最適化エンジンエラー: {e}"
        }), 500

# 既存のエンドポイント
@api_bp.route('/subjects', methods=['GET', 'POST'])
def manage_subjects():
    """科目管理API"""
    data_repo = get_data_repository()
    
    if request.method == 'GET':
        subjects = data_repo.get_subjects()
        print(f"📚 /api/subjects GET: {len(subjects)}件の科目を返します")
        return jsonify([s.to_dict() for s in subjects])
    
    elif request.method == 'POST':
        try:
            subject_data = request.get_json()
            subject = Subject(**subject_data)
            saved_subject = data_repo.save_subject(subject)
            print(f"📚 /api/subjects POST: 科目'{subject.name}'を保存しました")
            return jsonify(saved_subject.to_dict())
        except Exception as e:
            return jsonify({"error": str(e)}), 400

@api_bp.route('/teachers', methods=['GET', 'POST'])
def manage_teachers():
    """教師管理API"""
    data_repo = get_data_repository()
    
    if request.method == 'GET':
        teachers = data_repo.get_teachers()
        print(f"👨‍🏫 /api/teachers GET: {len(teachers)}件の教師を返します")
        return jsonify([t.to_dict() for t in teachers])
    
    elif request.method == 'POST':
        try:
            teacher_data = request.get_json()
            teacher = Teacher(**teacher_data)
            saved_teacher = data_repo.save_teacher(teacher)
            print(f"👨‍🏫 /api/teachers POST: 教師'{teacher.name}'を保存しました")
            return jsonify(saved_teacher.to_dict())
        except Exception as e:
            return jsonify({"error": str(e)}), 400

@api_bp.route('/timeslots', methods=['GET'])
def get_timeslots():
    """時間枠取得API"""
    data_repo = get_data_repository()
    timeslots = data_repo.get_timeslots()
    return jsonify([t.to_dict() for t in timeslots])

@api_bp.route('/student-groups', methods=['GET'])
def get_student_groups():
    """学生グループ取得API"""
    data_repo = get_data_repository()
    student_groups = data_repo.get_student_groups()
    return jsonify([sg.to_dict() for sg in student_groups])

@api_bp.route('/lessons', methods=['GET'])
def manage_lessons():
    """授業管理API"""
    data_repo = get_data_repository()
    lessons = data_repo.generate_lessons()
    return jsonify([l.to_dict() for l in lessons])

@api_bp.route('/test', methods=['GET'])
def test_api():
    """API動作テスト"""
    data_repo = get_data_repository()
    return jsonify({
        "status": "success",
        "message": "TimefoldAI API is working!",
        "data_summary": {
            "subjects": len(data_repo.get_subjects()),
            "teachers": len(data_repo.get_teachers()),
            "timeslots": len(data_repo.get_timeslots()),
            "student_groups": len(data_repo.get_student_groups())
        }
    })