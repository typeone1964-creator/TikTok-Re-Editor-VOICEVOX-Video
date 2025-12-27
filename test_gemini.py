#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from utils.text_formatter import GeminiFormatter

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"Gemini APIキー: {api_key[:10]}...")

formatter = GeminiFormatter(api_key)

# テストテキスト
test_text = "こんにちはこれはテストです今日はいい天気ですね"

print("\n=== テキスト整形テスト ===")
print(f"入力: {test_text}")

result = formatter.format_text(test_text)

if result:
    print(f"\n✅ 成功！")
    print(f"出力:\n{result}")
else:
    print(f"\n❌ 失敗")
