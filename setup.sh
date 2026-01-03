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
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ .envファイルを作成しました (.env.exampleから)"
    else
        cat > .env << EOF
# Gladia API Key
GLADIA_API_KEY=your_gladia_api_key_here

# Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# VOICEVOX API URL (default: http://localhost:50021)
VOICEVOX_API_URL=http://localhost:50021
EOF
        echo "✅ .envファイルを作成しました"
    fi
else
    echo "✅ .envファイルは既に存在します"
fi
echo ""

# 実行権限を付与
chmod +x run.sh run.command 2>/dev/null

echo "================================"
echo "✅ セットアップ完了！"
echo "================================"
echo ""
echo "次のステップ:"
echo "1. VOICEVOXを起動してください"
echo ""
echo "2. アプリを起動（どちらか選択）:"
echo "   【Mac】 run.command をダブルクリック（簡単！）"
echo "   【他】  ターミナルで ./run.sh を実行"
echo ""
echo "※ テキストから音声・動画を作るだけなら、APIキーは不要です"
echo "※ 動画から文字起こしをする場合のみ、.envファイルにAPIキーを設定してください"
echo ""
read -p "Enterキーを押して終了..."
