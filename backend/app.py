from flask import Flask, render_template
from flask_cors import CORS
import logging

def create_app():
    app = Flask(__name__, 
                static_folder='../frontend/static',
                template_folder='../frontend/templates')
    
    # CORS設定
    CORS(app)
    
    # ログ設定
    logging.basicConfig(level=logging.INFO)
    
    # Blueprint登録
    try:
        from backend.api.routes import api_bp
        app.register_blueprint(api_bp, url_prefix='/api')
        app.logger.info("✅ API Blueprint 登録成功")
    except Exception as e:
        app.logger.error(f"❌ API Blueprint 登録失敗: {e}")
        import traceback
        traceback.print_exc()
    
    # メインページルート
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # ヘルスチェック用の追加ルート（念のため）
    @app.route('/health')
    def health():
        return {"status": "ok", "message": "App is running"}
    
    # 登録されたルートを確認（デバッグ用）
    @app.before_first_request
    def log_routes():
        for rule in app.url_map.iter_rules():
            app.logger.info(f"📍 登録ルート: {rule.endpoint} -> {rule.rule}")
    
    return app