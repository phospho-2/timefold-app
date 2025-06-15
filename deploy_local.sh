#!/bin/bash
# ローカルサーバー + ngrok デプロイメントスクリプト

echo "🚀 TimefoldAI ローカルサーバー + ngrok デプロイメント開始"

# サーバーを起動（バックグラウンド）
echo "📚 サーバー起動中..."
python run.py &
SERVER_PID=$!

# サーバー起動待機
sleep 5

# ngrokでトンネル開始
echo "🌐 ngrok トンネル開始..."
ngrok http 8000 --log=stdout &
NGROK_PID=$!

# 終了処理
cleanup() {
    echo "🛑 サーバー停止中..."
    kill $SERVER_PID 2>/dev/null
    kill $NGROK_PID 2>/dev/null
    echo "✅ 停止完了"
    exit 0
}

# Ctrl+C で終了処理
trap cleanup SIGINT SIGTERM

echo "🎉 デプロイメント完了！"
echo "📍 ローカル: http://localhost:8000"
echo "🌍 外部アクセス: ngrok URLを確認してください"
echo "🛑 終了: Ctrl+C"

# 待機
wait