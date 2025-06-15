"""TimefoldAI アプリケーション起動スクリプト"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from backend.app import create_app

def main():
    """メイン実行関数"""
    print("🚀 TimefoldAI 分離版アプリケーション起動中...")
    
    # アプリケーション作成
    app = create_app({
        'DEBUG': True,
        'HOST': 'localhost',
        'PORT': 8000
    })
    
    print("📍 アクセス: http://localhost:8000")
    print("🧪 APIテスト: http://localhost:8000/api/test")
    print("🛑 終了: Ctrl+C")
    
    # サーバー起動
    app.run(
        host='localhost',
        port=8000,
        debug=True
    )

if __name__ == '__main__':
    main()
