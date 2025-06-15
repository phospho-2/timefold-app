import os
import sys
import logging
import gc

# メモリ使用量を抑制
os.environ['JAVA_OPTS'] = '-Xmx400m -XX:+UseG1GC -XX:MaxGCPauseMillis=100'

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Javaの設定（Railway環境対応）
if os.environ.get('RAILWAY_ENVIRONMENT'):
    logger.info("🚂 Railway環境で実行中...")
    # Railway環境でのメモリ制限設定
    os.environ['JVM_OPTS'] = '-Xmx400m'
else:
    logger.info("🖥️ ローカル環境で実行中...")

try:
    from backend.app import create_app
    logger.info("✅ アプリケーションモジュールの読み込み成功")
except Exception as e:
    logger.error(f"❌ アプリケーションモジュールの読み込み失敗: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

def main():
    try:
        # ガベージコレクション実行
        gc.collect()
        
        app = create_app()
        logger.info("✅ アプリケーション作成成功")
        
        # Railway用のポート設定
        port = int(os.environ.get('PORT', 8000))
        host = '0.0.0.0'
        
        logger.info("🚀 TimefoldAI 分離版アプリケーション起動中...")
        logger.info(f"📍 アクセス: http://localhost:{port}")
        logger.info(f"🧪 APIテスト: http://localhost:{port}/api/test")
        logger.info("🛑 終了: Ctrl+C")
        
        # Railway環境では debug=False
        debug_mode = not os.environ.get('RAILWAY_ENVIRONMENT')
        
        app.run(
            host=host,
            port=port,
            debug=debug_mode,
            threaded=True  # メモリ効率向上
        )
        
    except Exception as e:
        logger.error(f"❌ アプリケーション起動失敗: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()