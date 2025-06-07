"""カスタマイズ機能のAPIルート"""
from flask import Blueprint, request, jsonify
from ..services.customize_service import CustomizeService

# Blueprint の作成
customize_bp = Blueprint('customize', __name__, url_prefix='/api/customize')

# グローバルなカスタマイズサービス
_customize_service = None

def get_customize_service():
    """カスタマイズサービスのシングルトン取得"""
    global _customize_service
    if _customize_service is None:
        _customize_service = CustomizeService("backend/data")
    return _customize_service

@customize_bp.route('/config', methods=['GET', 'POST'])
def manage_config():
    """設定管理API"""
    service = get_customize_service()
    
    if request.method == 'GET':
        config = service.get_current_config()
        return jsonify(config)
    
    elif request.method == 'POST':
        config_data = request.get_json()
        result = service.update_config(config_data)
        return jsonify(result)

@customize_bp.route('/stats', methods=['GET'])
def get_stats():
    """カスタマイズ統計情報API"""
    service = get_customize_service()
    stats = service.get_customization_stats()
    return jsonify(stats)

@customize_bp.route('/subject', methods=['POST', 'DELETE'])
def manage_subject():
    """科目管理API"""
    service = get_customize_service()
    
    if request.method == 'POST':
        subject_data = request.get_json()
        result = service.add_custom_subject(subject_data)
        print(f"📚 カスタマイズ科目追加結果: {result}")
        
        # メインAPIのデータリポジトリも強制再読み込み
        from .routes import get_data_repository
        main_repo = get_data_repository()
        main_repo.load_all_data()
        print(f"📚 メインリポジトリ再読み込み完了: {len(main_repo.get_subjects())}件")
        
        return jsonify(result)
    
    elif request.method == 'DELETE':
        subject_id = request.args.get('id', type=int)
        if not subject_id:
            return jsonify({"status": "error", "message": "科目IDが必要です"}), 400
        
        result = service.delete_subject(subject_id)
        
        # メインAPIのデータリポジトリも強制再読み込み
        from .routes import get_data_repository
        main_repo = get_data_repository()
        main_repo.load_all_data()
        
        return jsonify(result)

@customize_bp.route('/teacher', methods=['POST', 'DELETE'])
def manage_teacher():
    """教師管理API"""
    service = get_customize_service()
    
    if request.method == 'POST':
        teacher_data = request.get_json()
        result = service.add_custom_teacher(teacher_data)
        print(f"👨‍🏫 カスタマイズ教師追加結果: {result}")
        
        # メインAPIのデータリポジトリも強制再読み込み
        from .routes import get_data_repository
        main_repo = get_data_repository()
        main_repo.load_all_data()
        print(f"👨‍🏫 メインリポジトリ再読み込み完了: {len(main_repo.get_teachers())}件")
        
        return jsonify(result)
    
    elif request.method == 'DELETE':
        teacher_id = request.args.get('id', type=int)
        if not teacher_id:
            return jsonify({"status": "error", "message": "教師IDが必要です"}), 400
        
        result = service.delete_teacher(teacher_id)
        
        # メインAPIのデータリポジトリも強制再読み込み
        from .routes import get_data_repository
        main_repo = get_data_repository()
        main_repo.load_all_data()
        
        return jsonify(result)

@customize_bp.route('/preview-timeslots', methods=['POST'])
def preview_timeslots():
    """時間枠プレビューAPI"""
    service = get_customize_service()
    temp_config = request.get_json()
    preview_slots = service.preview_timeslots(temp_config)
    return jsonify(preview_slots)

@customize_bp.route('/test', methods=['GET'])
def test_customize():
    """カスタマイズ機能テストAPI"""
    return jsonify({
        "status": "success",
        "message": "Customize API is working!",
        "features": [
            "動的時間設定",
            "科目・教師管理",
            "設定プレビュー",
            "統計情報"
        ]
    })
