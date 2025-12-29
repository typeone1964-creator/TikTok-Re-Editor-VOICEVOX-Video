"""
動画生成モジュール
テキストと音声を組み合わせてTikTok形式の動画を生成
"""
import tempfile
import os
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
import numpy as np
from PIL import Image, ImageDraw, ImageFont

class VideoGenerator:
    def __init__(self):
        self.width = 1080  # TikTok形式（9:16）
        self.height = 1920
        self.fps = 30
        self.font_path = '/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc'  # ヒラギノ角ゴシックW6

    def create_srt_file(self, text: str, duration: float) -> str:
        """
        SRT形式の字幕ファイルを生成（句読点で分割）

        Args:
            text: 元のテキスト
            duration: 音声の長さ（秒）

        Returns:
            SRT形式の文字列
        """
        # テキストを句読点で分割
        clean_text = text.replace('\n', '')
        segments = []
        current_segment = ""

        for char in clean_text:
            current_segment += char
            # 句読点で分割
            if char in '、。！？…':
                if current_segment.strip():
                    segments.append(current_segment.strip())
                current_segment = ""

        # 残りのテキストを追加
        if current_segment.strip():
            segments.append(current_segment.strip())

        if not segments:
            segments = [clean_text]

        # 各クリップの文字数を計算（句読点除去後）
        segment_lengths = []
        for seg in segments:
            clean_seg = seg.replace('、', '').replace('。', '').replace('，', '').replace('．', '').replace('！', '').replace('？', '').replace('…', '')
            segment_lengths.append(len(clean_seg))

        total_chars = sum(segment_lengths)

        # 文字数に応じて時間を配分
        segment_durations = []
        for length in segment_lengths:
            seg_duration = (length / total_chars) * duration if total_chars > 0 else duration / len(segments)
            segment_durations.append(seg_duration)

        # SRT形式で出力
        srt_content = ""
        current_time = 0
        for i, segment in enumerate(segments):
            start_time = current_time
            end_time = current_time + segment_durations[i]
            current_time = end_time

            # 時間をSRT形式に変換 (HH:MM:SS,mmm)
            start_str = self._format_srt_time(start_time)
            end_str = self._format_srt_time(end_time)

            # 句読点を除去
            segment_clean = segment.replace('、', '').replace('。', '').replace('，', '').replace('．', '').replace('！', '').replace('？', '').replace('…', '')

            srt_content += f"{i + 1}\n"
            srt_content += f"{start_str} --> {end_str}\n"
            srt_content += f"{segment_clean}\n\n"

        return srt_content

    def _format_srt_time(self, seconds: float) -> str:
        """
        秒数をSRT形式の時間文字列に変換

        Args:
            seconds: 秒数

        Returns:
            HH:MM:SS,mmm 形式の文字列
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)

        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    def _create_subtitle_layer(self, text_clips, duration):
        """
        透明背景の字幕レイヤー動画を生成（Premiere Pro互換）

        Args:
            text_clips: テキストクリップのリスト
            duration: 動画の長さ（秒）

        Returns:
            動画データ（MOVバイト列）
        """
        try:
            # 透明背景を作成
            transparent_bg = ColorClip(
                size=(self.width, self.height),
                color=(0, 0, 0),
                duration=duration
            ).set_opacity(0)

            # 字幕クリップを合成
            if text_clips:
                subtitle_clip = CompositeVideoClip([transparent_bg] + text_clips)
            else:
                subtitle_clip = transparent_bg

            # 一時ファイルに保存（MOV形式、PNG透過コーデック）
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mov') as subtitle_file:
                subtitle_path = subtitle_file.name

            print(f"[字幕レイヤー] MOV形式で生成中（Premiere Pro互換）...")

            # MOV形式で書き出し（PNG透過、Premiere Pro完全対応）
            subtitle_clip.write_videofile(
                subtitle_path,
                fps=self.fps,
                codec='png',  # PNG透過コーデック（Premiere Pro互換）
                logger=None
            )

            # 動画データを読み込み
            with open(subtitle_path, 'rb') as f:
                subtitle_data = f.read()

            print(f"[字幕レイヤー] 生成完了（MOV形式）")

            # クリーンアップ
            subtitle_clip.close()
            os.unlink(subtitle_path)

            return subtitle_data

        except Exception as e:
            import traceback
            print(f"字幕レイヤー生成エラー: {str(e)}")
            print(traceback.format_exc())
            return None

    def create_vertical_text_image(self, text, font_size=60, text_color='black', bg_color=(255, 255, 255, 255)):
        """
        白背景に縦書きテキストの画像を生成

        Args:
            text: 表示するテキスト（句読点は除去される）
            font_size: フォントサイズ
            text_color: テキスト色
            bg_color: 背景色（デフォルト：白）

        Returns:
            numpy array (RGBA画像)
        """
        try:
            font = ImageFont.truetype(self.font_path, font_size)
        except:
            font = ImageFont.load_default()

        # 句読点を除去
        text = text.replace('、', '').replace('。', '').replace('，', '').replace('．', '').replace('！', '').replace('？', '').replace('…', '')

        # 文字を1文字ずつリストに
        chars = list(text.replace('\n', ''))  # 改行を除去

        if not chars:
            # 空の画像を返す
            return np.zeros((100, 100, 4), dtype=np.uint8)

        # 各文字のサイズを計算
        char_height = font_size  # 文字間は標準
        char_width = font_size + 20

        # 画像サイズを計算（縦書き：幅は文字幅+余白、高さは文字数×文字高さ+余白）
        padding = 30
        img_width = char_width + padding * 2
        img_height = char_height * len(chars) + padding * 2

        # 画像を作成（白背景）
        image = Image.new('RGBA', (img_width, img_height), bg_color)
        draw = ImageDraw.Draw(image)

        # 文字色を設定
        if isinstance(text_color, str):
            if text_color == 'white':
                color = (255, 255, 255, 255)
            elif text_color == 'black':
                color = (0, 0, 0, 255)
            else:
                color = (0, 0, 0, 255)
        else:
            color = tuple(text_color) + (255,)

        # 縦書きで文字を描画
        y_position = padding
        x_position = padding + 10

        # 縦書きで回転が必要な文字
        rotate_chars = ['ー', '〜', '〰', '―', '─', '−']

        # 小さい文字（右寄せにする）
        small_chars = ['ぁ', 'ぃ', 'ぅ', 'ぇ', 'ぉ', 'ゃ', 'ゅ', 'ょ', 'ゎ', 'っ',
                       'ァ', 'ィ', 'ゥ', 'ェ', 'ォ', 'ャ', 'ュ', 'ョ', 'ヮ', 'ッ']

        for char in chars:
            if char in rotate_chars:
                # 長音記号などは90度回転させて描画
                # 一時的な画像に文字を描画（文字の境界ボックスを取得）
                temp_size = font_size * 3
                temp_img = Image.new('RGBA', (temp_size, temp_size), (0, 0, 0, 0))
                temp_draw = ImageDraw.Draw(temp_img)
                # 文字を中央に描画
                bbox = temp_draw.textbbox((0, 0), char, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                text_x = (temp_size - text_width) // 2 - bbox[0]
                text_y = (temp_size - text_height) // 2 - bbox[1]
                temp_draw.text((text_x, text_y), char, font=font, fill=color)
                # 90度回転
                rotated = temp_img.rotate(90, expand=True)
                # 行の中央に配置
                paste_x = x_position + (char_width - rotated.width) // 2
                paste_y = y_position + (char_height - rotated.height) // 2
                image.paste(rotated, (paste_x, paste_y), rotated)
            else:
                # 小さい文字は右寄せ＋上寄せ
                if char in small_chars:
                    offset_x = font_size // 6  # 文字サイズの1/6右にずらす（少しだけ右寄せ）
                    offset_y = -font_size // 6  # 文字サイズの1/6上にずらす（上寄せ）
                    draw.text((x_position + offset_x, y_position + offset_y), char, font=font, fill=color)
                else:
                    # 通常の文字はそのまま描画
                    draw.text((x_position, y_position), char, font=font, fill=color)
            y_position += char_height

        # numpy配列に変換
        return np.array(image)

    def create_video(
        self,
        text: str,
        audio_data: bytes,
        background_color=(0, 0, 0),  # 黒背景
        text_color='white',
        font_size=90,
        max_chars_per_subtitle=20,  # 1つの字幕あたりの最大文字数
        timing_info=None,  # VOICEVOXからのタイミング情報
        timing_offset=0.0  # タイミングオフセット（秒）：マイナスで早く、プラスで遅く
    ) -> bytes:
        """
        音声に合わせて縦書き字幕を表示する動画を生成

        Args:
            text: 表示するテキスト
            audio_data: 音声データ（WAVバイト列）
            background_color: 背景色（RGB）
            text_color: テキスト色
            font_size: フォントサイズ
            max_chars_per_subtitle: 1つの字幕あたりの最大文字数

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

            # タイミング情報の処理
            if timing_info and len(timing_info) > 0:
                # VOICEVOXの正確なタイミング情報を使用
                print(f"VOICEVOXタイミング情報を使用: {len(timing_info)}フレーズ")

                # デバッグ: 実際の音声の長さとタイミング情報の合計を比較
                timing_total = sum([t["duration"] for t in timing_info])
                print(f"[DEBUG] 実際の音声の長さ: {duration:.2f}秒")
                print(f"[DEBUG] タイミング情報の合計: {timing_total:.2f}秒")
                print(f"[DEBUG] 差分: {duration - timing_total:.2f}秒")

                # タイミング情報を実際の音声の長さに合わせてスケーリング（必須）
                scale_factor = duration / timing_total if timing_total > 0 else 1.0
                print(f"[DEBUG] タイミングをスケーリング: {scale_factor:.4f}倍")

                # すべてのタイミング情報をスケーリング
                scaled_timing_info = []
                for t in timing_info:
                    scaled_timing_info.append({
                        "text": t["text"],
                        "start": t["start"] * scale_factor,
                        "duration": t["duration"] * scale_factor
                    })

                # 再計算後の合計を確認
                timing_total_scaled = sum([t["duration"] for t in scaled_timing_info])
                print(f"[DEBUG] スケーリング後の合計: {timing_total_scaled:.2f}秒")

                # 新設計：シンプル＆予測可能
                # ユーザーの改行位置を尊重 + 文字数比例タイミング配分 + オフセット調整

                print(f"[新設計] ユーザー主導の改行 + 文字数比例タイミング")

                # ユーザーが入力したテキストを改行で分割
                lines = text.split('\n')
                user_segments = [line.strip() for line in lines if line.strip()]

                print(f"[INFO] ユーザー指定の行数: {len(user_segments)}行")
                print(f"[INFO] 推奨行数: 30〜60行（現在: {len(user_segments)}行）")

                if len(user_segments) < 10:
                    print(f"[WARNING] 行数が少なすぎます。もっと細かく改行することをお勧めします。")
                elif len(user_segments) > 100:
                    print(f"[WARNING] 行数が多すぎます。もう少しまとめることをお勧めします。")

                # 各行の文字数を計算
                segment_char_counts = [len(seg) for seg in user_segments]
                total_chars = sum(segment_char_counts)

                print(f"[INFO] 総文字数: {total_chars}文字")
                print(f"[INFO] 音声の長さ: {duration:.2f}秒")
                print(f"[INFO] 1文字あたり: {duration / total_chars:.3f}秒" if total_chars > 0 else "[INFO] 文字数0")

                # 文字数比例でタイミングを配分（シンプル＆確実）
                segments = user_segments
                segment_starts = []
                segment_durations = []

                current_time = 0.0
                for i, char_count in enumerate(segment_char_counts):
                    # この行の長さ = 全体の長さ × (この行の文字数 / 総文字数)
                    seg_duration = (char_count / total_chars) * duration if total_chars > 0 else duration / len(user_segments)

                    segment_starts.append(current_time)
                    segment_durations.append(seg_duration)

                    # デバッグ情報（最初の5個と最後の5個）
                    if i < 5 or i >= len(user_segments) - 5:
                        seg_preview = user_segments[i][:20] + "..." if len(user_segments[i]) > 20 else user_segments[i]
                        print(f"[行{i+1:02d}] '{seg_preview}' | {current_time:.2f}s-{current_time + seg_duration:.2f}s ({char_count}文字)")
                    elif i == 5:
                        print(f"[...] ({len(user_segments) - 10}行を省略)")

                    current_time += seg_duration

                print(f"[INFO] 最終行終了時刻: {current_time:.2f}秒（音声: {duration:.2f}秒）")
                print(f"[SUCCESS] 全{len(segments)}行が{duration:.2f}秒に配分されました")

                # タイミングオフセットを適用
                print(f"[DEBUG] タイミングオフセット値: {timing_offset:+.2f}秒")
                if timing_offset != 0.0 and segment_starts:
                    print(f"[DEBUG] オフセット適用前の最初のクリップ開始時刻: {segment_starts[0]:.2f}秒")
                    segment_starts = [max(0.0, start + timing_offset) for start in segment_starts]
                    print(f"[DEBUG] オフセット適用後の最初のクリップ開始時刻: {segment_starts[0]:.2f}秒")
                    # 動画の長さを超えないように調整
                    for i in range(len(segment_starts)):
                        if segment_starts[i] + segment_durations[i] > duration:
                            segment_durations[i] = max(0.1, duration - segment_starts[i])
                else:
                    print(f"[DEBUG] オフセット0.0のため、タイミング調整なし")
            else:
                # タイミング情報がない場合: 文字数比例配分（従来の方法）
                print("文字数比例配分でタイミング計算")
                lines = text.split('\n')
                segments = []

                for line in lines:
                    if line.strip():
                        segments.append(line.strip())

                if not segments:
                    segments = [text]

                # 各クリップの文字数を計算
                segment_lengths = []
                for seg in segments:
                    segment_lengths.append(len(seg))

                total_chars = sum(segment_lengths)

                # 文字数で時間を配分
                segment_durations = []
                segment_starts = []
                current_time = 0
                for length in segment_lengths:
                    seg_duration = (length / total_chars) * duration if total_chars > 0 else duration / len(segments)
                    segment_durations.append(seg_duration)
                    segment_starts.append(current_time)
                    current_time += seg_duration

                # タイミングオフセットを適用（文字数比例配分時）
                print(f"[DEBUG] タイミングオフセット値（フォールバック）: {timing_offset:+.2f}秒")
                if timing_offset != 0.0 and segment_starts:
                    print(f"[DEBUG] オフセット適用前の最初のクリップ開始時刻: {segment_starts[0]:.2f}秒")
                    segment_starts = [max(0.0, start + timing_offset) for start in segment_starts]
                    print(f"[DEBUG] オフセット適用後の最初のクリップ開始時刻: {segment_starts[0]:.2f}秒")
                    # 動画の長さを超えないように調整
                    for i in range(len(segment_starts)):
                        if segment_starts[i] + segment_durations[i] > duration:
                            segment_durations[i] = max(0.1, duration - segment_starts[i])
                else:
                    print(f"[DEBUG] オフセット0.0のため、タイミング調整なし（フォールバック）")

            # 縦書き字幕クリップを作成
            text_clips = []
            print(f"[DEBUG] 字幕クリップ作成開始（全{len(segments)}クリップ）")
            for i, segment in enumerate(segments):
                # 縦書きテキスト画像を生成（黒文字、白背景）
                text_img = self.create_vertical_text_image(segment, font_size, 'black')

                # ImageClipを作成
                img_clip = ImageClip(text_img, duration=segment_durations[i])

                # 開始時間を設定（VOICEVOXのタイミング情報を使用）
                img_clip = img_clip.set_start(segment_starts[i])
                print(f"[DEBUG] クリップ{i+1}: 開始={segment_starts[i]:.2f}秒, 長さ={segment_durations[i]:.2f}秒")

                # 画面配置：中央横、上から300px
                x_position = (self.width - text_img.shape[1]) // 2  # 中央
                y_position = 300  # 上から300px
                img_clip = img_clip.set_position((x_position, y_position))

                text_clips.append(img_clip)

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

            # 字幕レイヤー動画を生成（透明背景 + 字幕のみ）
            subtitle_layer_data = self._create_subtitle_layer(text_clips, duration)

            # SRT字幕ファイルを生成（句読点で分割）
            srt_data = self.create_srt_file(text, duration)

            # クリーンアップ
            audio_clip.close()
            final_clip.close()
            os.unlink(audio_path)
            os.unlink(video_path)

            # 動画、字幕レイヤー、SRTファイルを返す
            return {
                'video': video_data,
                'subtitle_layer': subtitle_layer_data,
                'srt': srt_data
            }

        except Exception as e:
            import traceback
            print(f"動画生成エラー: {str(e)}")
            print(traceback.format_exc())
            raise  # エラーを再スローしてStreamlitに表示

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
            try:
                # Macで利用可能なフォントをフルパスで指定
                txt_clip = TextClip(
                    full_text,
                    fontsize=font_size,
                    color=text_color,
                    font='/System/Library/Fonts/Hiragino Sans GB.ttc',  # Macの日本語フォント
                    method='caption',
                    size=(self.width - 100, None)
                ).set_duration(duration)
            except Exception as e:
                # フォントが見つからない場合は別のフォントを試行
                print(f"スクロール動画フォントエラー1: {e}")
                try:
                    txt_clip = TextClip(
                        full_text,
                        fontsize=font_size,
                        color=text_color,
                        font='Arial-Unicode-MS',
                        method='caption',
                        size=(self.width - 100, None)
                    ).set_duration(duration)
                except Exception as e2:
                    print(f"スクロール動画フォントエラー2: {e2}")
                    # 最終手段：デフォルトフォント
                    txt_clip = TextClip(
                        full_text,
                        fontsize=font_size,
                        color=text_color,
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
            import traceback
            print(f"スクロール動画生成エラー: {str(e)}")
            print(traceback.format_exc())
            raise  # エラーを再スローしてStreamlitに表示

    def create_segment_video(self, text: str, audio_data: bytes, segment_index: int = 0) -> bytes:
        """
        単一クリップの動画を生成（改行ごとに字幕を切り替え）

        Args:
            text: クリップのテキスト（改行区切り）
            audio_data: クリップの音声データ（WAV形式）
            segment_index: クリップ番号（表示用）

        Returns:
            動画データ（MP4バイト列）
        """
        try:
            print(f"\n[クリップ{segment_index + 1}] 動画生成開始")
            print(f"[クリップ{segment_index + 1}] テキスト: {text[:30]}..." if len(text) > 30 else f"[クリップ{segment_index + 1}] テキスト: {text}")

            # 音声ファイルを一時保存
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as audio_file:
                audio_path = audio_file.name
                audio_file.write(audio_data)

            # 音声クリップを作成
            audio_clip = AudioFileClip(audio_path)
            duration = audio_clip.duration

            print(f"[クリップ{segment_index + 1}] 音声の長さ: {duration:.2f}秒")

            # 背景動画を作成（黒背景）
            background = ColorClip(
                size=(self.width, self.height),
                color=(0, 0, 0),  # 黒背景
                duration=duration
            )

            # テキストを改行で分割
            lines = text.split('\n')
            user_segments = [line.strip() for line in lines if line.strip()]

            print(f"[クリップ{segment_index + 1}] 改行数: {len(user_segments)}行")
            print(f"[クリップ{segment_index + 1}] 受信したテキスト（改行あり）: {repr(text)}")
            print(f"[クリップ{segment_index + 1}] 分割後の各行: {user_segments}")

            # 各行の文字数を計算
            segment_char_counts = [len(seg) for seg in user_segments]
            total_chars = sum(segment_char_counts)

            # 文字数比例でタイミングを配分
            text_clips = []
            current_time = 0.0

            for i, seg_text in enumerate(user_segments):
                char_count = segment_char_counts[i]
                seg_duration = (char_count / total_chars) * duration if total_chars > 0 else duration / len(user_segments)

                # 縦書きテキスト画像を生成
                text_img = self.create_vertical_text_image(
                    seg_text,
                    font_size=100,
                    text_color='black',
                    bg_color=(255, 255, 255, 255)  # 白背景
                )

                # 画像クリップを作成
                img_clip = ImageClip(text_img).set_duration(seg_duration)
                img_clip = img_clip.set_start(current_time)

                # 画面配置：中央横、上から300px
                x_position = (self.width - text_img.shape[1]) // 2
                y_position = 300
                img_clip = img_clip.set_position((x_position, y_position))

                text_clips.append(img_clip)

                print(f"[クリップ{segment_index + 1}] 行{i+1}: {seg_text[:20]}... | {current_time:.2f}s-{current_time + seg_duration:.2f}s")
                current_time += seg_duration

            # 背景と字幕を合成
            if text_clips:
                final_clip = CompositeVideoClip([background] + text_clips).set_audio(audio_clip)
            else:
                final_clip = background.set_audio(audio_clip)

            # 一時ファイルに動画を保存（MP4形式）
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as video_file:
                video_path = video_file.name

            # 動画を書き出し（MP4形式、H.264コーデック）
            print(f"[クリップ{segment_index + 1}] 動画エンコード中（MP4形式）...")
            final_clip.write_videofile(
                video_path,
                fps=self.fps,
                codec='libx264',  # H.264コーデック
                audio_codec='aac',  # AAC音声コーデック
                logger=None
            )

            # 動画データを読み込み
            with open(video_path, 'rb') as f:
                video_data = f.read()

            print(f"[クリップ{segment_index + 1}] ✅ 動画生成完了 ({len(video_data) / 1024 / 1024:.2f}MB)")

            # クリーンアップ
            audio_clip.close()
            final_clip.close()
            os.unlink(audio_path)
            os.unlink(video_path)

            return video_data

        except Exception as e:
            import traceback
            print(f"[クリップ{segment_index + 1}] ❌ 動画生成エラー: {str(e)}")
            print(traceback.format_exc())
            raise
