#!/bin/bash

echo "================================"
echo "TikTok Re-Editor 起動中..."
echo "================================"
echo ""

# VOICEVOXが起動しているかチェック
echo "VOICEVOXの接続をチェック中..."
if ! curl -s http://localhost:50021/version > /dev/null 2>&1; then
    echo ""
    echo "⚠️  VOICEVOXが起動していません！"
    echo ""
    echo "👉 VOICEVOXアプリを先に起動してください"
    echo "   起動後、もう一度このファイルをダブルクリックしてください"
    echo ""
    read -p "Enterキーを押して終了..."
    exit 1
fi
echo "✅ VOICEVOXが起動しています"
echo ""

# Streamlitアプリを起動
echo "アプリを起動中..."
echo ""
echo "※ ブラウザが自動的に開きます"
echo "※ もしブラウザが開かない場合は、以下のURLを手動で開いてください:"
echo "   http://localhost:8501"
echo ""
echo "※ 終了するには、Ctrl+C を押してください"
echo ""

# ブラウザを開くヘルパー関数
open_browser() {
    sleep 4
    if command -v open > /dev/null 2>&1; then
        # macOSの場合
        open http://localhost:8501
    elif command -v xdg-open > /dev/null 2>&1; then
        # Linuxの場合
        xdg-open http://localhost:8501
    elif command -v start > /dev/null 2>&1; then
        # Windowsの場合（Git Bash）
        start http://localhost:8501
    fi
}

# バックグラウンドでブラウザを開く
open_browser &

# Streamlitを起動（フォアグラウンドで）
streamlit run app.py
