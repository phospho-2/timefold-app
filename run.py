"""TimefoldAI アプリケーション起動スクリプト"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from backend.app import create_app

def main():
    """メイン実行関数"""
    print("🚀 TimefoldAI 分離版アプリケーション起動中...")
    
    # Railway環境判定
    is_railway = os.environ.get('RAILWAY_ENVIRONMENT') is not None
    port = int(os.environ.get('PORT', 8000))
    host = '0.0.0.0' if is_railway else 'localhost'
    debug = not is_railway
    
    # アプリケーション作成
    app = create_app({
        'DEBUG': debug,
        'HOST': host,
        'PORT': port
    })
    
    if is_railway:
        print("🚂 Railway環境で起動中...")
        print(f"📍 ポート: {port}")
        print(f"🧪 ヘルスチェック: /api/test")
    else:
        print("🖥️ ローカル環境で起動中...")
        print(f"📍 アクセス: http://localhost:{port}")
        print(f"🧪 APIテスト: http://localhost:{port}/api/test")
        print("🛑 終了: Ctrl+C")
    
    # サーバー起動
    app.run(
        host=host,
        port=port,
        debug=debug
    )

if __name__ == '__main__':
    main()
