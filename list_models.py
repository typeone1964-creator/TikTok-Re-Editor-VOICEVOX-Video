#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

print("利用可能なGeminiモデル:\n")

try:
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"- {model.name}")
            print(f"  表示名: {model.display_name}")
            print(f"  説明: {model.description}")
            print()
except Exception as e:
    print(f"エラー: {e}")
    import traceback
    traceback.print_exc()
