import os
import sys

# Javaの設定（Railway環境対応）
if os.environ.get('RAILWAY_ENVIRONMENT'):
    # Railway環境では自動的にJavaが利用可能
    print("🚂 Railway環境で実行中...")
else:
    print("🖥️ ローカル環境で実行中...")

from backend.app import create_app

def main():
    app = create_app()
    
    # Railway用のポート設定
    port = int(os.environ.get('PORT', 8000))
    host = '0.0.0.0'  # Railway では 0.0.0.0 必須
    
    print("🚀 TimefoldAI 分離版アプリケーション起動中...")
    print(f"📍 アクセス: http://localhost:{port}")
    print(f"🧪 APIテスト: http://localhost:{port}/api/test")
    print("🛑 終了: Ctrl+C")
    print("")
    
    # Railway環境では debug=False
    debug_mode = not os.environ.get('RAILWAY_ENVIRONMENT')
    
    app.run(
        host=host,
        port=port,
        debug=debug_mode
    )

if __name__ == '__main__':
    main()