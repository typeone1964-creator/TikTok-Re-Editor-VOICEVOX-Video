@echo off
chcp 65001 >nul
echo ================================
echo TikTok Re-Editor 自動セットアップ
echo ================================
echo.

REM Pythonがインストールされているか確認
echo [1/4] Pythonをチェック中...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Pythonがインストールされていません
    echo.
    echo 👉 https://www.python.org/downloads/ からPythonをインストールしてください
    echo    インストール時に「Add Python to PATH」にチェックを入れてください
    echo.
    pause
    exit /b 1
)
echo ✅ Pythonが見つかりました
echo.

REM 必要なパッケージをインストール
echo [2/4] 必要なパッケージをインストール中...
echo    (数分かかる場合があります)
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ パッケージのインストールに失敗しました
    pause
    exit /b 1
)
echo ✅ パッケージのインストール完了
echo.

REM VOICEVOXのチェック
echo [3/4] VOICEVOXをチェック中...
echo.
echo ⚠️  VOICEVOXがインストールされていない場合:
echo    👉 https://voicevox.hiroshiba.jp/ からダウンロードしてインストールしてください
echo.
timeout /t 3 >nul

REM .envファイルの作成
echo [4/4] 設定ファイルを作成中...
if not exist .env (
    (
        echo # API Keys (optional - only needed for video transcription)
        echo GLADIA_API_KEY=
        echo GEMINI_API_KEY=
    ) > .env
    echo ✅ .envファイルを作成しました
) else (
    echo ✅ .envファイルは既に存在します
)
echo.

echo ================================
echo ✅ セットアップ完了！
echo ================================
echo.
echo 次のステップ:
echo 1. VOICEVOXを起動してください
echo 2. run.bat をダブルクリックしてアプリを起動
echo.
echo ※ 動画から文字起こしをする場合は、.envファイルにAPIキーを設定してください
echo.
pause
