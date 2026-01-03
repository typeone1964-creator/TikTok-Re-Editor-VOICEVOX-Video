#!/bin/bash

# ========================================
# TikTok Re-Editor VOICEVOX Video
# Mac用 超簡単インストールスクリプト
# ========================================

set -e  # エラーが発生したら停止

# 色の設定
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# スクリプトのディレクトリに移動
cd "$(dirname "$0")"
SCRIPT_DIR="$(pwd)"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  TikTok Re-Editor VOICEVOX Video${NC}"
echo -e "${BLUE}  Mac用インストールスクリプト${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# ステップ1: quarantine属性を削除
echo -e "${YELLOW}[1/4] セキュリティ属性を削除中...${NC}"
if command -v xattr &> /dev/null; then
    xattr -dr com.apple.quarantine "$SCRIPT_DIR" 2>/dev/null || true
    echo -e "${GREEN}✓ セキュリティ属性を削除しました${NC}"
else
    echo -e "${YELLOW}⚠ xattrコマンドが見つかりません（スキップ）${NC}"
fi
echo ""

# ステップ2: 実行権限を付与
echo -e "${YELLOW}[2/4] 実行権限を設定中...${NC}"
chmod +x "$SCRIPT_DIR/setup.sh" 2>/dev/null || true
chmod +x "$SCRIPT_DIR/run.sh" 2>/dev/null || true
chmod +x "$SCRIPT_DIR/setup.command" 2>/dev/null || true
chmod +x "$SCRIPT_DIR/run.command" 2>/dev/null || true
chmod +x "$SCRIPT_DIR/INSTALL_MAC.sh" 2>/dev/null || true
echo -e "${GREEN}✓ 実行権限を設定しました${NC}"
echo ""

# ステップ3: Pythonのバージョン確認
echo -e "${YELLOW}[3/4] Python環境を確認中...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓ Python ${PYTHON_VERSION} が見つかりました${NC}"
else
    echo -e "${RED}✗ Python3が見つかりません${NC}"
    echo ""
    echo -e "${YELLOW}Pythonをインストールしてください：${NC}"
    echo "  1. https://www.python.org/downloads/ にアクセス"
    echo "  2. 'Download Python' をクリックしてダウンロード"
    echo "  3. インストール後、このスクリプトを再度実行してください"
    echo ""
    exit 1
fi
echo ""

# ステップ4: 依存関係のインストール
echo -e "${YELLOW}[4/4] 必要なパッケージをインストール中...${NC}"
if [ -f "requirements.txt" ]; then
    python3 -m pip install --upgrade pip --quiet
    python3 -m pip install -r requirements.txt --quiet
    echo -e "${GREEN}✓ パッケージのインストールが完了しました${NC}"
else
    echo -e "${RED}✗ requirements.txtが見つかりません${NC}"
    exit 1
fi
echo ""

# 完了メッセージ
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  ✓ インストール完了！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}次のステップ:${NC}"
echo ""
echo -e "${YELLOW}1. VOICEVOXアプリを起動してください${NC}"
echo "   → https://voicevox.hiroshiba.jp/ からダウンロード"
echo ""
echo -e "${YELLOW}2. アプリを起動するには：${NC}"
echo "   ${GREEN}./run.sh${NC}"
echo ""
echo "   または、以下をダブルクリック："
echo "   ${GREEN}run.command${NC}"
echo ""
echo -e "${BLUE}問題が発生した場合：${NC}"
echo "  README.md を参照してください"
echo ""
