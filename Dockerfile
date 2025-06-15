# Python 3.12 with Java 17 support
FROM python:3.12-slim

# システムパッケージの更新とJava 17のインストール
RUN apt-get update && apt-get install -y \
    openjdk-17-jdk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Java環境変数の設定
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# Javaが正しくインストールされているか確認
RUN java -version

# 作業ディレクトリの設定
WORKDIR /app

# 依存関係のインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションファイルのコピー
COPY . .

# クラウド用の環境変数（Railway/Cloud Run対応）
ENV RAILWAY_ENVIRONMENT=true
ENV CLOUD_RUN_ENVIRONMENT=true

# ポートの公開（Cloud Runは8080、Railwayは8000）
EXPOSE 8000
EXPOSE 8080

# アプリケーションの起動
CMD ["python", "run.py"]