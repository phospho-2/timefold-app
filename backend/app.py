"""TimefoldAI Flask アプリケーション"""
from flask import Flask, render_template
from flask_cors import CORS
from .api.routes import api_bp
from .api.customize_routes import customize_bp

def create_app(config=None):
    """Flask アプリケーションファクトリ"""
    app = Flask(__name__, 
                static_folder='../frontend/static',
                template_folder='../frontend/templates')
    
    # CORS設定（開発用）
    CORS(app)
    
    # 設定
    if config:
        app.config.update(config)
    else:
        app.config.update({
            'DEBUG': True,
            'HOST': 'localhost',
            'PORT': 8000
        })
    
    # Blueprint登録
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(customize_bp)  # カスタマイズAPI追加
    
    @app.route('/')
    def index():
        """メインページ"""
        return render_template('index.html')
    
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Not Found"}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {"error": "Internal Server Error"}, 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
