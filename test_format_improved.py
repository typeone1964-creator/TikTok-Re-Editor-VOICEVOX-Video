#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from utils.text_formatter import GeminiFormatter

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
formatter = GeminiFormatter(api_key)

# テストテキスト（参考例と同じ）
test_text = "職場の嫌な奴はこう扱えば大丈夫職場に嫌いな人は一人はいますよねそんな人の対処法を5つ紹介しますこの動画はもう二度とおすすめに表示されませんので忘れないよういいねと保存をお願いします"

print("=== テキスト整形テスト（改善版） ===")
print(f"入力: {test_text}\n")

result = formatter.format_text(test_text)

if result:
    print(f"✅ 成功！\n")
    print("出力:")
    print(result)
    print("\n各行の文字数チェック:")
    for i, line in enumerate(result.split('\n'), 1):
        char_count = len(line)
        ends_with_punctuation = line.endswith('。') or line.endswith('、')
        status = "✅" if char_count <= 14 and ends_with_punctuation else "❌"
        print(f"{status} {i}行目: {char_count}文字 | 句読点: {'○' if ends_with_punctuation else '×'} | {line}")
else:
    print(f"❌ 失敗")
