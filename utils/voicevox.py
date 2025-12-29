import requests
import json
from typing import List, Dict, Optional


class VoiceVoxAPI:
    def __init__(self, base_url: str = "http://localhost:50021"):
        self.base_url = base_url

    def get_speakers(self) -> List[Dict]:
        """VOICEVOXのスピーカー一覧を取得"""
        try:
            response = requests.get(f"{self.base_url}/speakers")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"スピーカー取得エラー: {e}")
            return []

    def get_speaker_styles(self, speakers: List[Dict]) -> Dict[str, List[Dict]]:
        """スピーカーとスタイルの辞書を作成"""
        speaker_styles = {}
        for speaker in speakers:
            speaker_name = speaker.get("name", "")
            styles = speaker.get("styles", [])
            speaker_styles[speaker_name] = styles
        return speaker_styles

    def find_speaker_id(self, speakers: List[Dict], speaker_name: str, style_name: str = "ノーマル") -> Optional[int]:
        """指定されたスピーカー名とスタイル名からスピーカーIDを取得"""
        for speaker in speakers:
            if speaker.get("name") == speaker_name:
                for style in speaker.get("styles", []):
                    if style.get("name") == style_name:
                        return style.get("id")
        return None

    def generate_audio_query(self, text: str, speaker_id: int) -> Optional[Dict]:
        """テキストから音声クエリを生成"""
        try:
            response = requests.post(
                f"{self.base_url}/audio_query",
                params={"text": text, "speaker": speaker_id}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"音声クエリ生成エラー: {e}")
            return None

    def synthesize_voice(self, audio_query: Dict, speaker_id: int, speed: float = 1.2) -> Optional[bytes]:
        """音声クエリから音声を合成"""
        try:
            # 話速を設定
            audio_query["speedScale"] = speed

            response = requests.post(
                f"{self.base_url}/synthesis",
                params={"speaker": speaker_id},
                headers={"Content-Type": "application/json"},
                data=json.dumps(audio_query)
            )
            response.raise_for_status()
            return response.content
        except Exception as e:
            print(f"音声合成エラー: {e}")
            return None

    def generate_voice(self, text: str, speaker_id: int, speed: float = 1.2) -> Optional[bytes]:
        """テキストから直接音声を生成（便利メソッド）"""
        audio_query = self.generate_audio_query(text, speaker_id)
        if audio_query:
            return self.synthesize_voice(audio_query, speaker_id, speed)
        return None

    def generate_sample_voice(self, speaker_id: int) -> Optional[bytes]:
        """キャラクター試聴用のサンプル音声を生成"""
        sample_text = "こんにちは、VOICEVOXです。よろしくお願いします。"
        return self.generate_voice(sample_text, speaker_id, speed=1.0)

    def get_timing_info(self, text: str, speaker_id: int, speed: float = 1.2) -> Optional[List[Dict]]:
        """テキストの各セグメント（句読点区切り）のタイミング情報を取得"""
        try:
            # 音声クエリを生成
            audio_query = self.generate_audio_query(text, speaker_id)
            if not audio_query:
                return None

            # 話速を設定
            audio_query["speedScale"] = speed

            # accent_phrases から各フレーズの長さを計算
            accent_phrases = audio_query.get("accent_phrases", [])
            timing_info = []
            current_time = 0.0

            for phrase in accent_phrases:
                # フレーズの総時間を計算（各モーラの長さを合計）
                # vowel_lengthはそのままの値を使用（VOICEVOXが返す値を信頼）
                phrase_duration = 0.0
                for mora in phrase.get("moras", []):
                    phrase_duration += mora.get("vowel_length", 0.0)

                # ポーズの長さを追加
                pause_mora = phrase.get("pause_mora")
                if pause_mora:
                    phrase_duration += pause_mora.get("vowel_length", 0.0)

                # フレーズのテキストを取得
                phrase_text = ""
                for mora in phrase.get("moras", []):
                    phrase_text += mora.get("text", "")

                timing_info.append({
                    "text": phrase_text,
                    "start": current_time,
                    "duration": phrase_duration
                })

                current_time += phrase_duration

            # デバッグ情報を出力
            print(f"[VOICEVOX] Speed: {speed}, Total timing duration: {current_time:.2f}秒")

            return timing_info

        except Exception as e:
            print(f"タイミング情報取得エラー: {e}")
            return None
