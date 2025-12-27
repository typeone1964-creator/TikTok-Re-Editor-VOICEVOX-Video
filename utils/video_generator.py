"""
動画生成モジュール
テキストと音声を組み合わせてTikTok形式の動画を生成
"""
import tempfile
import os
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
import numpy as np

class VideoGenerator:
    def __init__(self):
        self.width = 1080  # TikTok形式（9:16）
        self.height = 1920
        self.fps = 30

    def create_video(
        self,
        text: str,
        audio_data: bytes,
        background_color=(0, 0, 0),  # 黒背景
        text_color='white',
        font_size=60,
        max_chars_per_line=14
    ) -> bytes:
        """
        テキストと音声から動画を生成

        Args:
            text: 表示するテキスト
            audio_data: 音声データ（WAVバイト列）
            background_color: 背景色（RGB）
            text_color: テキスト色
            font_size: フォントサイズ
            max_chars_per_line: 1行あたりの最大文字数

        Returns:
            動画データ（MP4バイト列）
        """
        try:
            # 一時ファイルに音声を保存
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as audio_file:
                audio_file.write(audio_data)
                audio_path = audio_file.name

            # 音声クリップを作成
            audio_clip = AudioFileClip(audio_path)
            duration = audio_clip.duration

            # 背景クリップを作成
            background = ColorClip(
                size=(self.width, self.height),
                color=background_color,
                duration=duration
            )

            # テキストを行に分割
            lines = text.split('\n')

            # テキストクリップを作成（中央配置）
            text_clips = []
            y_position = self.height // 2 - (len(lines) * (font_size + 10)) // 2

            for line in lines:
                if line.strip():
                    txt_clip = TextClip(
                        line.strip(),
                        fontsize=font_size,
                        color=text_color,
                        font='Yu-Gothic-Bold',  # 日本語フォント
                        method='caption',
                        size=(self.width - 100, None)
                    ).set_position(('center', y_position)).set_duration(duration)

                    text_clips.append(txt_clip)
                    y_position += font_size + 10

            # すべてのクリップを合成
            if text_clips:
                final_clip = CompositeVideoClip([background] + text_clips).set_audio(audio_clip)
            else:
                final_clip = background.set_audio(audio_clip)

            # 一時ファイルに動画を保存
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as video_file:
                video_path = video_file.name

            # 動画を書き出し
            final_clip.write_videofile(
                video_path,
                fps=self.fps,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile=tempfile.mktemp(suffix='.m4a'),
                remove_temp=True,
                logger=None  # ログを抑制
            )

            # 動画データを読み込み
            with open(video_path, 'rb') as f:
                video_data = f.read()

            # クリーンアップ
            audio_clip.close()
            final_clip.close()
            os.unlink(audio_path)
            os.unlink(video_path)

            return video_data

        except Exception as e:
            print(f"動画生成エラー: {str(e)}")
            return None

    def create_scrolling_video(
        self,
        text: str,
        audio_data: bytes,
        background_color=(0, 0, 0),
        text_color='white',
        font_size=60
    ) -> bytes:
        """
        テキストがスクロールする動画を生成

        Args:
            text: 表示するテキスト
            audio_data: 音声データ（WAVバイト列）
            background_color: 背景色（RGB）
            text_color: テキスト色
            font_size: フォントサイズ

        Returns:
            動画データ（MP4バイト列）
        """
        try:
            # 一時ファイルに音声を保存
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as audio_file:
                audio_file.write(audio_data)
                audio_path = audio_file.name

            # 音声クリップを作成
            audio_clip = AudioFileClip(audio_path)
            duration = audio_clip.duration

            # 背景クリップを作成
            background = ColorClip(
                size=(self.width, self.height),
                color=background_color,
                duration=duration
            )

            # テキストを行に分割
            lines = text.split('\n')
            full_text = '\n'.join([line.strip() for line in lines if line.strip()])

            # テキストクリップを作成（大きめに）
            txt_clip = TextClip(
                full_text,
                fontsize=font_size,
                color=text_color,
                font='Yu-Gothic-Bold',
                method='caption',
                size=(self.width - 100, None)
            ).set_duration(duration)

            # スクロール効果を追加
            txt_height = txt_clip.h

            def scroll_position(t):
                # 上から下へスクロール
                progress = t / duration
                y = self.height - (progress * (txt_height + self.height))
                return ('center', y)

            txt_clip = txt_clip.set_position(scroll_position)

            # 合成
            final_clip = CompositeVideoClip([background, txt_clip]).set_audio(audio_clip)

            # 一時ファイルに動画を保存
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as video_file:
                video_path = video_file.name

            # 動画を書き出し
            final_clip.write_videofile(
                video_path,
                fps=self.fps,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile=tempfile.mktemp(suffix='.m4a'),
                remove_temp=True,
                logger=None
            )

            # 動画データを読み込み
            with open(video_path, 'rb') as f:
                video_data = f.read()

            # クリーンアップ
            audio_clip.close()
            final_clip.close()
            os.unlink(audio_path)
            os.unlink(video_path)

            return video_data

        except Exception as e:
            print(f"スクロール動画生成エラー: {str(e)}")
            return None
