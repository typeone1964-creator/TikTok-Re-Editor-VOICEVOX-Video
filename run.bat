@echo off
chcp 65001 >nul
echo ================================
echo TikTok Re-Editor 起動中...
echo ================================
echo.

REM VOICEVOXが起動しているかチェック
echo VOICEVOXの接続をチェック中...
curl -s http://localhost:50021/version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  VOICEVOXが起動していません！
    echo.
    echo 👉 VOICEVOXアプリを先に起動してください
    echo    起動後、もう一度このファイルをダブルクリックしてください
    echo.
    pause
    exit /b 1
)
echo ✅ VOICEVOXが起動しています
echo.

REM Streamlitアプリを起動
echo アプリを起動中...
echo.
echo ※ ブラウザが自動的に開きます
echo ※ もしブラウザが開かない場合は、以下のURLを手動で開いてください:
echo    http://localhost:8501
echo.
echo ※ 終了するには、このウィンドウを閉じてください
echo.

REM バックグラウンドでブラウザを開く（4秒後）
start /B cmd /c "timeout /t 4 /nobreak >nul && start http://localhost:8501"

REM Streamlitを起動
streamlit run app.py

pause
