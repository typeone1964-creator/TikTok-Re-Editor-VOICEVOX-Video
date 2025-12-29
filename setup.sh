#!/bin/bash

echo "================================"
echo "TikTok Re-Editor 自動セットアップ"
echo "================================"
echo ""

# Pythonがインストールされているか確認
echo "[1/4] Pythonをチェック中..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Pythonがインストールされていません"
    echo ""
    echo "👉 https://www.python.org/downloads/ からPythonをインストールしてください"
    echo ""
    exit 1
fi
echo "✅ Pythonが見つかりました"
echo ""

# 必要なパッケージをインストール
echo "[2/4] 必要なパッケージをインストール中..."
echo "   (数分かかる場合があります)"
python3 -m pip install --upgrade pip > /dev/null 2>&1
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ パッケージのインストールに失敗しました"
    exit 1
fi
echo "✅ パッケージのインストール完了"
echo ""

# VOICEVOXのチェック
echo "[3/4] VOICEVOXをチェック中..."
echo ""
echo "⚠️  VOICEVOXがインストールされていない場合:"
echo "   👉 https://voicevox.hiroshiba.jp/ からダウンロードしてインストールしてください"
echo ""
sleep 3

# .envファイルの作成
echo "[4/4] 設定ファイルを作成中..."
if [ ! -f .env ]; then
    cat > .env << EOF
# API Keys (optional - only needed for video transcription)
GLADIA_API_KEY=
GEMINI_API_KEY=
EOF
    echo "✅ .envファイルを作成しました"
else
    echo "✅ .envファイルは既に存在します"
fi
echo ""

# run.shに実行権限を付与
chmod +x run.sh 2>/dev/null

echo "================================"
echo "✅ セットアップ完了！"
echo "================================"
echo ""
echo "次のステップ:"
echo "1. VOICEVOXを起動してください"
echo "2. run.sh をダブルクリックしてアプリを起動"
echo "   (または、ターミナルで ./run.sh を実行)"
echo ""
echo "※ 動画から文字起こしをする場合は、.envファイルにAPIキーを設定してください"
echo ""
read -p "Enterキーを押して終了..."
