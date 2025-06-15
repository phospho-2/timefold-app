from flask import Blueprint, request, jsonify
import logging
import threading
import time

api_bp = Blueprint('api', __name__)
logger = logging.getLogger(__name__)

# 最適化状態管理
optimization_status = {
    "running": False,
    "result": None,
    "error": None,
    "progress": 0
}

@api_bp.route('/optimize', methods=['POST'])
def optimize():
    """最適化を非同期で実行"""
    global optimization_status
    
    try:
        if optimization_status["running"]:
            return jsonify({
                "success": False,
                "message": "最適化が既に実行中です",
                "status": "running"
            }), 400
        
        # リクエストデータを取得
        data = request.get_json()
        
        # 最適化状態をリセット
        optimization_status = {
            "running": True,
            "result": None,
            "error": None,
            "progress": 0
        }
        
        # 非同期で最適化を実行
        def run_optimization():
            try:
                from backend.services.optimization_service import OptimizationService
                service = OptimizationService()
                
                logger.info("🚀 最適化処理開始（非同期）")
                optimization_status["progress"] = 10
                
                result = service.optimize_timetable(data)
                
                optimization_status["running"] = False
                optimization_status["result"] = result
                optimization_status["progress"] = 100
                
                logger.info("✅ 最適化処理完了（非同期）")
                
            except Exception as e:
                logger.error(f"❌ 最適化エラー（非同期）: {str(e)}")
                optimization_status["running"] = False
                optimization_status["error"] = str(e)
                optimization_status["progress"] = 0
        
        # バックグラウンドで実行
        thread = threading.Thread(target=run_optimization)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            "success": True,
            "message": "最適化処理を開始しました",
            "status": "started"
        })
        
    except Exception as e:
        logger.error(f"❌ 最適化開始エラー: {str(e)}")
        optimization_status["running"] = False
        optimization_status["error"] = str(e)
        
        return jsonify({
            "success": False,
            "error": f"最適化の開始に失敗しました: {str(e)}"
        }), 500

@api_bp.route('/optimization-status', methods=['GET'])
def get_optimization_status():
    """最適化の状態を取得"""
    global optimization_status
    
    return jsonify({
        "running": optimization_status["running"],
        "progress": optimization_status["progress"],
        "result": optimization_status["result"],
        "error": optimization_status["error"]
    })