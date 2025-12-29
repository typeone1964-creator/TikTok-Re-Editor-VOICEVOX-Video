"""
テキストクリップ分割ユーティリティ
句読点ベースで自然な区切りを作成
"""
import re
from typing import List, Dict


class TextSegmenter:
    def __init__(self, min_chars: int = 10, max_chars: int = 150):
        """
        Args:
            min_chars: 最小文字数（これより短いクリップは前のクリップと結合）
            max_chars: 推奨最大文字数（警告表示用）
        """
        self.min_chars = min_chars
        self.max_chars = max_chars

    def split_by_punctuation(self, text: str) -> List[str]:
        """
        句読点で分割し、5〜10行になるよう自動グループ化

        Args:
            text: 入力テキスト（改行を含む）

        Returns:
            クリップのリスト（改行を保持、5〜10行程度）
        """
        # まず空行で分割されているかチェック
        if '\n\n' in text:
            # 空行がある場合は、空行で分割（ユーザーが意図的に入れた区切り）
            segments = re.split(r'\n\s*\n+', text)
            result = []
            for segment in segments:
                segment = segment.strip()
                if segment:
                    result.append(segment)

            # クリップ数と行数の情報を出力
            for i, seg in enumerate(result):
                line_count = len(seg.split('\n'))
                print(f"[クリップ{i+1}] {line_count}行, {len(seg)}文字 (空行区切り)")

            return result

        # 空行がない場合は、句読点で分割してグループ化
        # 句読点で分割（句読点を含めて分割）
        segments = re.split(r'([。！？])', text)

        # 句読点を前のクリップに結合
        sentences = []
        for i in range(0, len(segments) - 1, 2):
            sentence = segments[i]
            if i + 1 < len(segments):
                sentence += segments[i + 1]  # 句読点を追加
            sentence = sentence.strip()
            if sentence:
                sentences.append(sentence)

        # 最後のクリップ（句読点なし）を追加
        if len(segments) % 2 == 1:
            last_seg = segments[-1].strip()
            if last_seg:
                sentences.append(last_seg)

        # 5〜10行になるようにグループ化
        target_min_lines = 5
        target_max_lines = 10

        result = []
        current_group = []
        current_lines = 0

        for sentence in sentences:
            # 句読点の後の改行も考慮
            sentence_lines = len(sentence.split('\n'))

            # グループに追加
            current_group.append(sentence)
            current_lines += sentence_lines

            # 5〜10行の範囲に達したら、新しいグループを開始
            if current_lines >= target_min_lines:
                # グループを結合（改行で連結）
                result.append('\n'.join(current_group))
                current_group = []
                current_lines = 0

        # 残りのグループを追加
        if current_group:
            remaining_text = '\n'.join(current_group)
            remaining_lines = len(remaining_text.split('\n'))

            # 最後のグループが3行以下の場合は、前のグループと結合
            if remaining_lines <= 3 and result:
                result[-1] = result[-1] + '\n' + remaining_text
            else:
                result.append(remaining_text)

        # クリップ数と行数の情報を出力
        for i, seg in enumerate(result):
            line_count = len(seg.split('\n'))
            print(f"[クリップ{i+1}] {line_count}行, {len(seg)}文字 (自動グループ化)")

        return result

    def _merge_short_segments(self, segments: List[str]) -> List[str]:
        """
        短すぎるクリップを前のクリップと結合

        Args:
            segments: クリップのリスト

        Returns:
            結合後のクリップリスト
        """
        if not segments:
            return []

        merged = [segments[0]]

        for seg in segments[1:]:
            if len(seg) < self.min_chars and merged:
                # 前のクリップと結合（改行を挿入）
                merged[-1] += '\n' + seg
            else:
                merged.append(seg)

        return merged

    def get_segment_info(self, segments: List[str]) -> Dict:
        """
        クリップ情報を取得

        Args:
            segments: クリップのリスト

        Returns:
            クリップ情報の辞書
        """
        total_chars = sum(len(seg) for seg in segments)
        avg_chars = total_chars / len(segments) if segments else 0

        # 長すぎるクリップを検出
        long_segments = [i for i, seg in enumerate(segments) if len(seg) > self.max_chars]

        return {
            "count": len(segments),
            "total_chars": total_chars,
            "avg_chars": avg_chars,
            "min_chars": min(len(seg) for seg in segments) if segments else 0,
            "max_chars": max(len(seg) for seg in segments) if segments else 0,
            "long_segments": long_segments  # 長すぎるクリップのインデックス
        }

    def estimate_duration(self, segments: List[str], chars_per_second: float = 10.0) -> List[float]:
        """
        各クリップの推定時間を計算

        Args:
            segments: クリップのリスト
            chars_per_second: 1秒あたりの文字数（VOICEVOX速度1.0の場合: 約10文字/秒）

        Returns:
            各クリップの推定時間（秒）のリスト
        """
        return [len(seg) / chars_per_second for seg in segments]
