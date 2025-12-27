#!/usr/bin/env python3
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GLADIA_API_KEY")
print(f"APIキー: {api_key[:10]}...")

# シンプルなテストリクエスト
url = "https://api.gladia.io/v2/upload"
headers = {"x-gladia-key": api_key}

print("\nGladia APIテスト中...")
print(f"URL: {url}")
print(f"Headers: x-gladia-key: {api_key[:10]}...")

try:
    # 小さなテストファイルを作成
    test_file_path = "/tmp/test_audio.txt"
    with open(test_file_path, "w") as f:
        f.write("test")

    with open(test_file_path, "rb") as f:
        # ファイル名とコンテンツタイプを明示的に指定
        files = {"audio": ("test.mp4", f, "video/mp4")}
        response = requests.post(url, headers=headers, files=files)

    print(f"\nステータスコード: {response.status_code}")
    print(f"レスポンス: {response.text}")

except Exception as e:
    print(f"\nエラーが発生しました: {e}")
    import traceback
    traceback.print_exc()
