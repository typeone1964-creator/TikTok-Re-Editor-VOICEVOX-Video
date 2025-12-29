import streamlit as st
import os
import tempfile
import zipfile
import io
from dotenv import load_dotenv
from utils.transcription import GladiaAPI
from utils.text_formatter import GeminiFormatter
from utils.voicevox import VoiceVoxAPI
from utils.video_generator import VideoGenerator
from utils.text_segmenter import TextSegmenter

# 環境変数を読み込み
load_dotenv()

# ページ設定
st.set_page_config(
    page_title="TikTok Re-Editor Video",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# カスタムCSS - TikTokスタイルのボタンとUI
st.markdown("""
<style>
    /* TikTokカラー: シアン #00f2ea, ピンク #fe2c55, 黒背景 */

    /* ダークテーマの背景 */
    .stApp {
        background: #000000;
        color: #ffffff;
    }

    /* ヘッダースタイル */
    h1 {
        color: #ffffff !important;
        text-shadow:
            2px 2px 0px #fe2c55,
            -2px -2px 0px #00f2ea;
        font-weight: bold !important;
    }

    h2, h3 {
        color: #ffffff !important;
        text-shadow: 0 0 10px rgba(0, 242, 234, 0.5);
    }

    /* 全てのテキスト要素を白色に */
    p, span, div, label, caption, .stMarkdown, .stText {
        color: #ffffff !important;
    }

    /* キャプションも白色に */
    .stCaptionContainer, [data-testid="stCaptionContainer"] {
        color: #ffffff !important;
    }

    /* 全てのボタンを左寄せ・同じ大きさに統一（BROWSE FILES除く） */
    .stButton > button,
    .stButton button,
    .stDownloadButton > button,
    .stDownloadButton button,
    button[kind="primary"] {
        background: #000000 !important;
        color: white !important;
        border: 2px solid #00f2ea !important;
        border-radius: 10px !important;
        padding: 12px 30px !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        box-shadow: 0 0 15px rgba(0, 242, 234, 0.5) !important;
        transition: all 0.3s ease !important;
        width: 300px !important;
        max-width: 300px !important;
        min-height: 45px !important;
        height: 45px !important;
        line-height: 1.2 !important;
        margin-right: auto !important;
        margin-left: 0 !important;
        display: block !important;
    }

    .stButton > button:hover:not(:disabled),
    .stButton button:hover:not(:disabled),
    .stDownloadButton > button:hover,
    .stDownloadButton button:hover,
    button[kind="primary"]:hover {
        background: #1a1a1a !important;
        border: 3px solid #00f2ea !important;
        color: #00f2ea !important;
        box-shadow:
            0 0 40px rgba(0, 242, 234, 1),
            0 0 60px rgba(0, 242, 234, 0.6),
            inset 0 0 20px rgba(0, 242, 234, 0.2) !important;
        transform: translateY(-3px) scale(1.02) !important;
    }

    /* BROWSE FILESボタンのホバー時 */
    button[kind="secondary"]:hover {
        color: #00f2ea !important;
    }

    /* Disabledボタンのスタイル */
    .stButton > button:disabled,
    .stButton button:disabled {
        background: #000000 !important;
        color: #666666 !important;
        border: 2px solid #333333 !important;
        border-radius: 10px !important;
        padding: 12px 30px !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        box-shadow: 0 0 5px rgba(51, 51, 51, 0.3) !important;
        width: 100% !important;
        min-height: 45px !important;
        height: 45px !important;
        cursor: not-allowed !important;
        opacity: 0.5 !important;
    }

    /* テキストエリア - コンパクト版＋目立つカーソル */
    .stTextArea textarea {
        background: rgba(10, 10, 10, 0.9) !important;
        color: #ffffff !important;
        border: 2px solid rgba(0, 242, 234, 0.5) !important;
        border-radius: 8px !important;
        box-shadow: 0 0 15px rgba(0, 242, 234, 0.3) !important;
        caret-color: #00f2ea !important;
        padding: 10px !important;
        font-size: 14px !important;
        line-height: 1.6 !important;
    }

    /* テキストインプット - コンパクト版＋目立つカーソル */
    .stTextInput input {
        background: rgba(10, 10, 10, 0.9) !important;
        color: #ffffff !important;
        border: 2px solid rgba(0, 242, 234, 0.5) !important;
        border-radius: 8px !important;
        box-shadow: 0 0 15px rgba(0, 242, 234, 0.3) !important;
        caret-color: #00f2ea !important;
        padding: 8px 12px !important;
        font-size: 14px !important;
    }

    /* セレクトボックス */
    .stSelectbox > div > div {
        background: rgba(10, 10, 10, 0.9) !important;
        color: #ffffff !important;
        border: 2px solid rgba(0, 242, 234, 0.5) !important;
        border-radius: 10px !important;
    }

    /* スライダー */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #00f2ea 0%, #fe2c55 100%) !important;
    }

    /* 各種ラベルを白文字に */
    .stFileUploader label,
    [data-testid="stFileUploader"] label,
    .stFileUploader p,
    [data-testid="stFileUploader"] p,
    .stTextArea label,
    .stTextInput label,
    .stSelectbox label,
    .stSlider label {
        color: #ffffff !important;
    }

    /* インフォボックス */
    .stInfo {
        background: rgba(0, 242, 234, 0.1) !important;
        border: 2px solid rgba(0, 242, 234, 0.5) !important;
        border-radius: 10px !important;
        box-shadow: 0 0 15px rgba(0, 242, 234, 0.3) !important;
        color: #ffffff !important;
    }

    /* エキスパンダー（展開メニュー） */
    .streamlit-expanderHeader {
        background: rgba(0, 242, 234, 0.1) !important;
        border: 1px solid rgba(0, 242, 234, 0.3) !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        font-size: 13px !important;
        padding: 8px 12px !important;
    }

    .streamlit-expanderHeader:hover {
        background: rgba(0, 242, 234, 0.2) !important;
        border-color: rgba(0, 242, 234, 0.5) !important;
    }

    .streamlit-expanderContent {
        background: rgba(10, 10, 10, 0.8) !important;
        border: 1px solid rgba(0, 242, 234, 0.2) !important;
        border-radius: 0 0 8px 8px !important;
        padding: 12px !important;
        color: #ffffff !important;
    }

    /* ファイルアップローダー */
    .stFileUploader {
        background: rgba(10, 10, 10, 0.9) !important;
        border: 2px solid rgba(0, 242, 234, 0.5) !important;
        border-radius: 10px !important;
        padding: 20px !important;
    }

    /* オーディオプレイヤー */
    audio {
        width: 100% !important;
        filter:
            drop-shadow(0 0 10px rgba(0, 242, 234, 0.5))
            drop-shadow(0 0 20px rgba(254, 44, 85, 0.3));
    }

    /* タブスタイル - コンパクト版 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background: transparent !important;
        padding: 15px 10px 20px 10px;
        border: none !important;
        border-bottom: none !important;
        display: flex !important;
        flex-direction: row !important;
    }

    .stTabs [data-baseweb="tab"] {
        flex: 1 !important;
        width: 100% !important;
        min-width: 0 !important;
        max-width: none !important;
        height: 45px !important;
        min-height: 45px !important;
        padding: 12px 30px !important;
        background: #000000 !important;
        border: 2px solid #00f2ea !important;
        border-radius: 10px !important;
        color: white !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        box-shadow: 0 0 15px rgba(0, 242, 234, 0.5) !important;
        transition: all 0.25s ease !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: #1a1a1a !important;
        border: 3px solid #00f2ea !important;
        color: #00f2ea !important;
        box-shadow:
            0 0 40px rgba(0, 242, 234, 1),
            0 0 60px rgba(0, 242, 234, 0.6),
            inset 0 0 20px rgba(0, 242, 234, 0.2) !important;
        transform: translateY(-3px) scale(1.02) !important;
    }

    .stTabs [aria-selected="true"] {
        background: #000000 !important;
        border: 2px solid #00f2ea !important;
        color: white !important;
        box-shadow: 0 0 25px rgba(0, 242, 234, 0.7) !important;
    }

    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 30px;
    }

    /* すべてのボーダーと装飾を削除 */
    .stTabs [data-baseweb="tab-list"]::after,
    .stTabs [data-baseweb="tab-list"]::before,
    .stTabs [data-baseweb="tab"]::after,
    .stTabs [data-baseweb="tab"]::before,
    .stTabs [aria-selected="true"]::after,
    .stTabs [aria-selected="true"]::before {
        display: none !important;
        content: none !important;
    }

    .stTabs,
    .stTabs *,
    .stTabs [role="tablist"],
    .stTabs [role="tablist"] *,
    button[role="tab"],
    button[role="tab"] *,
    div[data-baseweb="tab-border"],
    div[data-baseweb="tab-highlight"] {
        border: none !important;
        border-bottom: none !important;
        border-top: none !important;
        border-left: none !important;
        border-right: none !important;
    }

    div[data-baseweb="tab-border"],
    div[data-baseweb="tab-highlight"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        width: 0 !important;
    }

    .stTabs > div,
    .stTabs > div > div,
    .stTabs > div > div > div {
        border-bottom: none !important;
    }

    /* サイドバー開閉ボタンのスタイル改善 - バー内に配置 */
    button[kind="header"] {
        background: #000000 !important;
        color: #00f2ea !important;
        border: 2px solid #00f2ea !important;
        border-radius: 8px !important;
        padding: 6px 14px !important;
        font-weight: 700 !important;
        box-shadow: 0 0 10px rgba(0, 242, 234, 0.5) !important;
        transition: all 0.3s ease !important;
        min-width: 110px !important;
        text-align: left !important;
        margin: 4px !important;
        height: auto !important;
        font-size: 13px !important;
    }

    button[kind="header"]:hover {
        background: #1a1a1a !important;
        color: #ffffff !important;
        box-shadow: 0 0 20px rgba(0, 242, 234, 0.8) !important;
        transform: scale(1.05) !important;
    }

    /* サイドバーボタンの後に「API設定」ラベルを追加 */
    button[kind="header"]::after {
        content: " API設定" !important;
        font-size: 12px !important;
        font-weight: 700 !important;
        letter-spacing: 1px !important;
        margin-left: 6px !important;
        color: #00f2ea !important;
        display: inline-block !important;
    }

    /* サイドバーが閉じている時のボタン */
    [data-testid="collapsedControl"] {
        top: 0 !important;
        margin-top: 8px !important;
    }

    [data-testid="collapsedControl"] button {
        background: #000000 !important;
        color: #00f2ea !important;
        border: 2px solid #00f2ea !important;
        border-radius: 8px !important;
        padding: 6px 14px !important;
        font-weight: 700 !important;
        box-shadow: 0 0 10px rgba(0, 242, 234, 0.5) !important;
        min-width: 110px !important;
        height: auto !important;
        font-size: 13px !important;
        margin: 4px !important;
    }

    [data-testid="collapsedControl"] button::after {
        content: " API設定" !important;
        font-size: 12px !important;
        font-weight: 700 !important;
        letter-spacing: 1px !important;
        margin-left: 6px !important;
        color: #00f2ea !important;
    }

    /* サイドバー内の全てのテキスト色を黒に変更 - 最強版 */
    .stSidebar {
        background-color: #f0f2f6 !important;
        color: #000000 !important;
    }

    /* 全ての要素を黒に */
    .stSidebar *,
    .stSidebar h1,
    .stSidebar h2,
    .stSidebar h3,
    .stSidebar h4,
    .stSidebar h5,
    .stSidebar h6,
    .stSidebar p,
    .stSidebar span,
    .stSidebar div,
    .stSidebar label,
    .stSidebar strong,
    .stSidebar em,
    .stSidebar li,
    .stSidebar ul,
    .stSidebar ol {
        color: #000000 !important;
    }

    /* Markdown要素 */
    .stSidebar .stMarkdown,
    .stSidebar .stMarkdown *,
    .stSidebar [data-testid="stMarkdownContainer"],
    .stSidebar [data-testid="stMarkdownContainer"] *,
    .stSidebar .element-container,
    .stSidebar .element-container * {
        color: #000000 !important;
    }

    /* ヘッダー要素 */
    .stSidebar [data-testid="stHeader"],
    .stSidebar [data-testid="stHeader"] *,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #000000 !important;
    }

    /* リンクをシアン色に（TikTokスタイル） */
    .stSidebar a,
    .stSidebar a * {
        color: #00f2ea !important;
        text-decoration: underline !important;
    }

    .stSidebar a:hover {
        color: #ffffff !important;
        text-shadow: 0 0 10px rgba(0, 242, 234, 0.8) !important;
    }

    /* インフォボックスのテキストも黒に */
    .stSidebar .stAlert,
    .stSidebar .stAlert *,
    .stSidebar .stInfo,
    .stSidebar .stInfo *,
    .stSidebar .stWarning,
    .stSidebar .stWarning * {
        color: #000000 !important;
    }

    /* 特定のStreamlit要素クラス */
    .stSidebar [class*="st-"],
    .stSidebar [class*="st-"] * {
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# セッションステートの初期化
if 'transcribed_text' not in st.session_state:
    st.session_state.transcribed_text = None
if 'formatted_text' not in st.session_state:
    st.session_state.formatted_text = None
if 'filename' not in st.session_state:
    st.session_state.filename = None
if 'generated_audio' not in st.session_state:
    st.session_state.generated_audio = None
if 'sample_audio' not in st.session_state:
    st.session_state.sample_audio = None
if 'generated_sns_content' not in st.session_state:
    st.session_state.generated_sns_content = None
if 'generated_video' not in st.session_state:
    st.session_state.generated_video = None
if 'combined_video' not in st.session_state:
    st.session_state.combined_video = None

# タイトル
st.title("🎬 TikTok Re-Editor Video")
st.markdown("動画をアップロードして、文字起こし → 整形 → 音声合成 → 動画生成を自動実行")

# サイドバー：API設定
with st.sidebar:
    # サイドバーのテキストを全て黒色にするカスタムCSS
    st.markdown("""
    <style>
    /* サイドバーの全てのラベルを黒色に */
    [data-testid="stSidebar"] label {
        color: #000000 !important;
    }
    /* サイドバーの段落テキストを黒色に */
    [data-testid="stSidebar"] p {
        color: #000000 !important;
    }
    /* サイドバーの見出しを黒色に */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4 {
        color: #000000 !important;
    }
    /* サイドバーのstrongタグを黒色に */
    [data-testid="stSidebar"] strong {
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<h2 style="color: #000000 !important;">⚙️ API設定</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: #000000 !important;">各APIキーを入力してください</p>', unsafe_allow_html=True)

    # .envファイルから読み込み（ローカル開発用）
    env_gladia = os.getenv("GLADIA_API_KEY", "")
    env_gemini = os.getenv("GEMINI_API_KEY", "")
    env_voicevox = os.getenv("VOICEVOX_API_URL", "http://localhost:50021")

    # APIキー入力
    gladia_api_key = st.text_input(
        "🎤 Gladia API Key",
        value=env_gladia,
        type="password",
        help="文字起こし用APIキー（動画アップロード時のみ必要）"
    )

    gemini_api_key = st.text_input(
        "✨ Gemini API Key",
        value=env_gemini,
        type="password",
        help="テキスト整形・ファイル名生成用APIキー（動画アップロード時のみ必要）"
    )

    voicevox_url = st.text_input(
        "🎙️ VOICEVOX URL",
        value=env_voicevox,
        help="通常は変更不要。あなたのPCでVOICEVOXを起動してください。"
    )

    st.markdown("---")
    st.markdown('<h3 style="color: #000000 !important;">📚 APIキーの取得方法</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color: #000000 !important;">- <strong style="color: #000000 !important;">Gladia API</strong>: <a href="https://www.gladia.io/" style="color: #00f2ea; text-decoration: underline;">gladia.io</a></p>', unsafe_allow_html=True)
    st.markdown('<p style="color: #000000 !important;">- <strong style="color: #000000 !important;">Gemini API</strong>: <a href="https://ai.google.dev/" style="color: #00f2ea; text-decoration: underline;">ai.google.dev</a></p>', unsafe_allow_html=True)
    st.markdown('<p style="color: #000000 !important;">- <strong style="color: #000000 !important;">VOICEVOX</strong>: <a href="https://voicevox.hiroshiba.jp/" style="color: #00f2ea; text-decoration: underline;">voicevox.hiroshiba.jp</a></p>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<p style="color: #000000 !important;">💡 テキストファイルから生成する場合、Gladia/Gemini APIは不要です</p>', unsafe_allow_html=True)

# APIクライアントの初期化
gladia = GladiaAPI(gladia_api_key) if gladia_api_key else None
gemini = GeminiFormatter(gemini_api_key) if gemini_api_key else None
voicevox = VoiceVoxAPI(voicevox_url)
video_gen = VideoGenerator()
text_segmenter = TextSegmenter(min_chars=10, max_chars=150)

# セクション1: 入力ソース選択
st.header("📥 1. 入力ソース選択")

# タブで動画とテキストを切り替え
tab1, tab2 = st.tabs(["📹 動画から生成", "📄 テキストから生成"])

with tab1:
    st.subheader("動画アップロード")

    uploaded_file = st.file_uploader(
        "動画ファイルを選択してください",
        type=["mp4", "mov", "avi", "mkv", "webm"],
        key="video_uploader"
    )

    if uploaded_file is not None:
        # 動画を一時ファイルとして保存
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name

        st.info(f"📁 アップロードされたファイル: {uploaded_file.name}")

        # 文字起こしボタン
        if st.button("START...", key="transcribe_btn"):
            # APIキーチェック
            if not gladia_api_key or not gemini_api_key:
                st.error("⚠️ サイドバーでGladia APIキーとGemini APIキーを入力してください")
                st.stop()

            with st.status("処理中...", expanded=True) as status:
                st.write("📤 動画をアップロード中...")
                audio_url = gladia.upload_file(tmp_file_path)

                if audio_url:
                    st.write("✅ アップロード完了")
                    st.write("🎤 文字起こし中... (数分かかる場合があります)")

                    transcribed = gladia.transcribe(audio_url, language="ja")

                    if transcribed:
                        st.session_state.transcribed_text = transcribed
                        st.write("✅ 文字起こし完了")

                        st.write("✏️ テキスト整形中...")
                        formatted = gemini.format_text(transcribed)

                        if formatted:
                            st.session_state.formatted_text = formatted
                            st.write("✅ テキスト整形完了")

                            st.write("📝 ファイル名生成中...")
                            filename = gemini.generate_filename(formatted)

                            if filename:
                                st.session_state.filename = filename
                                st.write("✅ ファイル名生成完了")
                                status.update(label="✅ すべての処理が完了しました！", state="complete")
                                # 整形済みテキストセクションに自動スクロール
                                st.components.v1.html("""
                                <script>
                                    setTimeout(function() {
                                        const section = window.parent.document.getElementById('formatted-text-section');
                                        if (section) {
                                            section.scrollIntoView({behavior: 'smooth', block: 'start'});
                                        }
                                    }, 500);
                                </script>
                                """, height=0)
                            else:
                                st.error("ファイル名生成に失敗しました")
                        else:
                            st.error("テキスト整形に失敗しました")
                    else:
                        st.error("文字起こしに失敗しました")
                else:
                    st.error("動画のアップロードに失敗しました")

        # 一時ファイルを削除
        if os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)

with tab2:
    st.subheader("テキストファイルアップロード")

    text_file = st.file_uploader(
        "テキストファイルを選択してください (.txt)",
        type=["txt"],
        key="text_file_uploader"
    )

    if text_file is not None:
        st.info(f"📁 アップロードされたファイル: {text_file.name}")

        # テキスト処理ボタン
        if st.button("START...", key="text_process_btn"):
            with st.status("処理中...", expanded=True) as status:
                st.write("📄 テキストファイルを読み込み中...")

                try:
                    # テキストファイルを読み込み
                    raw_text = text_file.read().decode('utf-8', errors='replace')

                    if not raw_text.strip():
                        st.error("⚠️ テキストファイルが空です")
                    else:
                        # テキストをそのまま整形済みとして扱う
                        st.session_state.transcribed_text = raw_text
                        st.session_state.formatted_text = raw_text
                        st.write("✅ テキスト読み込み完了")

                        # ファイル名から拡張子を除いたものを使用
                        import os
                        filename = os.path.splitext(text_file.name)[0]
                        st.session_state.filename = filename
                        st.write("✅ ファイル名設定完了")

                        status.update(label="✅ すべての処理が完了しました！", state="complete")
                        # 整形済みテキストセクションに自動スクロール
                        st.components.v1.html("""
                        <script>
                            setTimeout(function() {
                                const section = window.parent.document.getElementById('formatted-text-section');
                                if (section) {
                                    section.scrollIntoView({behavior: 'smooth', block: 'start'});
                                }
                            }, 500);
                        </script>
                        """, height=0)

                except Exception as e:
                    st.error(f"❌ テキスト読み込みエラー: {str(e)}")

# セクション2: 整形済みテキスト表示
st.markdown('<div id="formatted-text-section"></div>', unsafe_allow_html=True)
st.header("📝 2. 整形済みテキスト + クリップ分割（編集可能）")

if st.session_state.formatted_text:
    # テキストエリアの初期値を設定
    if "text_editor" not in st.session_state:
        st.session_state.text_editor = st.session_state.formatted_text

    # 編集可能なテキストエリア
    st.info("💡 **自動処理**: 14文字/行に整形 + 5〜10行ごとに空行を自動挿入してクリップ分割します。必要に応じて手動調整も可能です。")

    st.text_area(
        "整形 + クリップ分割済みテキスト（編集可能）",
        height=300,
        key="text_editor",
        help="空行で区切られた部分が1つの動画クリップになります。空行の位置を自由に調整できます。"
    )
else:
    st.info("💡 セクション1で入力ソースを選択し、テキストを生成してください。")

# セクション3: VOICEVOX設定（音声生成）
st.markdown('<div id="voice-synthesis-section"></div>', unsafe_allow_html=True)
st.header("🎙️ 3. 音声合成")

if st.session_state.formatted_text:

    # スピーカー一覧を取得
    speakers = voicevox.get_speakers()

    if speakers:
        # スピーカー名のリストを作成
        speaker_names = [speaker.get("name", "") for speaker in speakers]

        # 初期値を「青山流星」に設定（存在する場合）
        default_index = 0
        if "青山龍星" in speaker_names:
            default_index = speaker_names.index("青山龍星")
        elif "青山流星" in speaker_names:
            default_index = speaker_names.index("青山流星")

        col1, col2 = st.columns(2)

        with col1:
            selected_speaker_name = st.selectbox(
                "🎭 キャラクター選択",
                speaker_names,
                index=default_index
            )

        # 選択されたスピーカーのスタイルを取得
        selected_speaker = next(
            (s for s in speakers if s.get("name") == selected_speaker_name),
            None
        )

        if selected_speaker:
            styles = selected_speaker.get("styles", [])
            style_names = [style.get("name", "") for style in styles]

            with col2:
                selected_style_name = st.selectbox(
                "🎨 スタイル選択",
                style_names,
                index=0
                )

            # スピーカーIDを取得
            speaker_id = voicevox.find_speaker_id(
                speakers,
                selected_speaker_name,
                selected_style_name
            )

            # キャラクター試聴ボタン
            if st.button("PREVIEW VOICE", key="sample_btn"):
                with st.spinner("サンプル音声を生成中..."):
                    sample_audio = voicevox.generate_sample_voice(speaker_id)
                    if sample_audio:
                        st.session_state.sample_audio = sample_audio
                        st.success("✅ サンプル音声を生成しました")
                    else:
                        st.error("サンプル音声の生成に失敗しました")

            # サンプル音声プレイヤー
            if st.session_state.sample_audio:
                st.audio(st.session_state.sample_audio, format="audio/wav")

            # 話速設定
            speed = st.slider(
                "⚡ 話速（Speed）",
                min_value=0.5,
                max_value=2.0,
                value=1.0,
                step=0.1
            )

            # 音声生成ボタン
            if st.button("GENERATE AUDIO", key="generate_btn"):
                with st.spinner("音声を生成中... (時間がかかる場合があります)"):
                    # ユーザーが入力したテキスト（改行あり）を保存
                    original_text = st.session_state.text_editor

                    # 音声生成用：改行を削除して1行にする（VOICEVOXの精度向上）
                    voice_text_no_breaks = original_text.replace('\n', '')

                    st.info(f"💡 音声生成：改行を削除した1行テキストを使用（{len(voice_text_no_breaks)}文字）")

                    # 音声生成（改行なしテキスト）
                    audio_data = voicevox.generate_voice(
                        voice_text_no_breaks,
                        speaker_id,
                        speed
                    )

                    # タイミング情報を取得（改行なしテキスト）
                    timing_info = voicevox.get_timing_info(
                        voice_text_no_breaks,
                        speaker_id,
                        speed
                    )

                    if audio_data:
                        st.session_state.generated_audio = audio_data
                        st.session_state.timing_info = timing_info
                        st.session_state.voice_text = original_text  # 動画生成用：元のテキスト（改行あり）を保存
                        st.session_state.voice_text_no_breaks = voice_text_no_breaks  # デバッグ用
                        st.session_state.speaker_id = speaker_id
                        st.session_state.speed = speed
                        st.success("✅ 音声を生成しました！")
                    else:
                        st.error("音声生成に失敗しました")

            # 生成された音声のプレビュー
            if st.session_state.generated_audio:
                st.subheader("🎧 生成された音声")
                st.audio(st.session_state.generated_audio, format="audio/wav")

                # 音声ダウンロードボタン
                st.download_button(
                label="AUDIO DOWNLOAD",
                data=st.session_state.generated_audio,
                file_name=f"{st.session_state.get('filename', 'output')}.wav",
                mime="audio/wav",
                key="download_audio_inline"
                )

                # 動画生成セクション
                st.markdown("---")
                # 音声生成後にここにスクロール
                st.markdown('<div id="video-generation"></div>', unsafe_allow_html=True)
else:
    st.info("💡 セクション2で整形済みテキストを作成してください。")

# セクション4: 動画生成
st.header("🎥 4. 動画生成")

# 音声が生成されている場合のみ表示
if st.session_state.generated_audio:
    st.info("💡 **手動調整**: セクション2で空行の位置を調整できます。空行で区切られた部分が1つの動画クリップになります。")

    # 音声生成後に自動スクロール
    st.components.v1.html("""
    <script>
    setTimeout(function() {
        const element = window.parent.document.getElementById('video-generation');
        if (element) {
            const yOffset = -150;
            const y = element.getBoundingClientRect().top + window.parent.pageYOffset + yOffset;
            window.parent.scrollTo({top: y, behavior: 'smooth'});
        }
    }, 500);
    </script>
    """, height=0)

    # テキストを句読点で分割
    print(f"[DEBUG] 動画生成時のtext_editor長: {len(st.session_state.text_editor)}文字")
    print(f"[DEBUG] 動画生成時の空行確認: {'\\n\\n' in st.session_state.text_editor}")
    print(f"[DEBUG] 動画生成時のテキスト（最初の200文字）: {repr(st.session_state.text_editor[:200])}")
    segments = text_segmenter.split_by_punctuation(st.session_state.text_editor)
    print(f"[DEBUG] 分割後のクリップ数: {len(segments)}")
    segment_info = text_segmenter.get_segment_info(segments)
    estimated_durations = text_segmenter.estimate_duration(segments, chars_per_second=10.0 / st.session_state.speed if st.session_state.speed else 10.0)

    # クリップ情報を表示
    st.markdown("##### 📊 クリップ情報")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("クリップ数", segment_info['count'])
    with col2:
        st.metric("総文字数", segment_info['total_chars'])
    with col3:
        st.metric("平均文字数", f"{segment_info['avg_chars']:.1f}")
    with col4:
        total_est_duration = sum(estimated_durations)
        st.metric("推定時間", f"{total_est_duration:.1f}秒")

    # クリップ動画生成ボタン
    if st.button("GENERATE CLIP VIDEOS", key="generate_segment_videos_btn"):
        with st.spinner(f"{len(segments)}個のクリップ動画を生成中... (時間がかかります)"):
            try:
                # セッションステートに結果を保存するリストを初期化
                if 'segment_videos' not in st.session_state:
                    st.session_state.segment_videos = []
                if 'segment_audios' not in st.session_state:
                    st.session_state.segment_audios = []
                if 'segment_texts' not in st.session_state:
                    st.session_state.segment_texts = []

                st.session_state.segment_videos = []
                st.session_state.segment_audios = []
                st.session_state.segment_texts = []

                # プログレスバーを表示
                progress_bar = st.progress(0)
                status_text = st.empty()

                # 各クリップの音声と動画を生成
                for i, segment_text in enumerate(segments):
                    status_text.text(f"クリップ {i+1}/{len(segments)} を処理中...")

                    # 音声生成
                    audio_data = voicevox.generate_voice(
                        segment_text,
                        st.session_state.speaker_id,
                        st.session_state.speed
                    )

                    if audio_data:
                        # 動画生成
                        video_data = video_gen.create_segment_video(
                            segment_text,
                            audio_data,
                            segment_index=i
                        )

                        if video_data:
                            st.session_state.segment_videos.append(video_data)
                            st.session_state.segment_audios.append(audio_data)
                            st.session_state.segment_texts.append(segment_text)
                        else:
                            st.error(f"クリップ{i+1}の動画生成に失敗しました")
                    else:
                        st.error(f"クリップ{i+1}の音声生成に失敗しました")

                    # プログレスバーを更新
                    progress_bar.progress((i + 1) / len(segments))

                progress_bar.empty()
                status_text.empty()

                if len(st.session_state.segment_videos) == len(segments):
                    st.success(f"✅ {len(segments)}個のクリップ動画を生成しました！")

                    # 自動的に結合動画を生成
                    status_text.text("結合動画を生成中...")
                    try:
                        from moviepy.editor import VideoFileClip, concatenate_videoclips

                        # 一時ファイルにクリップを保存
                        temp_files = []
                        clips = []

                        for i, video_data in enumerate(st.session_state.segment_videos):
                            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
                            temp_file.write(video_data)
                            temp_file.close()
                            temp_files.append(temp_file.name)

                            clip = VideoFileClip(temp_file.name)
                            clips.append(clip)

                        # 全クリップを結合
                        final_clip = concatenate_videoclips(clips)

                        # 一時ファイルに書き出し
                        combined_temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
                        combined_path = combined_temp_file.name
                        combined_temp_file.close()

                        final_clip.write_videofile(
                            combined_path,
                            fps=30,
                            codec='libx264',
                            audio_codec='aac',
                            logger=None
                        )

                        # 結合動画を読み込み
                        with open(combined_path, 'rb') as f:
                            combined_data = f.read()

                        st.session_state.combined_video = combined_data

                        # クリーンアップ
                        for clip in clips:
                            clip.close()
                        final_clip.close()

                        for temp_file in temp_files:
                            os.unlink(temp_file)
                        os.unlink(combined_path)

                        status_text.empty()
                        st.success(f"✅ 結合動画も生成しました！")

                    except Exception as combine_error:
                        status_text.empty()
                        st.warning(f"⚠️ 結合動画の生成に失敗しました: {str(combine_error)}")
                else:
                    st.warning(f"⚠️ {len(st.session_state.segment_videos)}/{len(segments)} 個のクリップ動画を生成しました")

            except Exception as e:
                st.error(f"クリップ動画生成エラー: {str(e)}")
                import traceback
                st.code(traceback.format_exc())

    # 生成されたクリップ動画のプレビューとダウンロードセクション
    if 'segment_videos' in st.session_state and st.session_state.segment_videos:
        st.markdown("---")

        # 結合動画プレビュー（iPhone風フレーム）
        if 'combined_video' in st.session_state and st.session_state.combined_video:
            st.markdown(f"##### 📺 結合動画プレビュー（全{len(st.session_state.segment_videos)}クリップ）")

            # iPhone風フレームで中央に表示
            import base64
            video_base64 = base64.b64encode(st.session_state.combined_video).decode()

            st.markdown(f"""
            <div style="display: flex; justify-content: center; margin: 20px 0;">
                <div style="background: white; padding: 15px; border-radius: 30px; box-shadow: 0 8px 16px rgba(0,0,0,0.2); max-width: 360px;">
                    <video controls style="width: 100%; height: 640px; object-fit: contain; border-radius: 20px; background: black;">
                        <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                    </video>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("##### 📦 ダウンロード")

        # ZIP一括ダウンロード（動画のみ）
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for i, video_data in enumerate(st.session_state.segment_videos):
                # 動画を追加（MP4形式）
                zip_file.writestr(f"clip_{i+1:02d}.mp4", video_data)

        zip_buffer.seek(0)

        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                label="📦 ZIP DOWNLOAD",
                data=zip_buffer.getvalue(),
                file_name=f"{st.session_state.get('filename', 'output')}_clips.zip",
                mime="application/zip",
                key="download_all_segments_zip"
            )
            st.info(f"💡 {len(st.session_state.segment_videos)}個の個別クリップ")

        with col2:
            # 結合動画ダウンロードボタン（自動生成済み）
            if 'combined_video' in st.session_state and st.session_state.combined_video:
                st.download_button(
                    label="🎬 DOWNLOAD COMBINED",
                    data=st.session_state.combined_video,
                    file_name=f"{st.session_state.get('filename', 'output')}_combined.mp4",
                    mime="video/mp4",
                    key="download_combined_video"
                )
                st.success("💡 全クリップを結合した1つの動画")
            else:
                st.write("")

else:
    st.info("💡 セクション3で音声を生成してください。")

# セクション5: タイトル・紹介文・ハッシュタグ生成
st.markdown('<div id="sns-content-section"></div>', unsafe_allow_html=True)
st.header("📋 5. タイトル・紹介文・ハッシュタグ生成")
st.info("💡 音声生成後、SNS投稿用のタイトル・紹介文・ハッシュタグを作成できます")

# 生成ボタン
if st.button("GENERATE SNS CONTENT", key="generate_sns_content_btn"):
    # Gemini APIキーチェック
    if not gemini_api_key:
        st.error("⚠️ サイドバーでGemini APIキーを入力してください")
    elif not st.session_state.text_editor:
        st.error("⚠️ テキストが見つかりません")
    else:
        with st.spinner("タイトル・紹介文・ハッシュタグを生成中..."):
            sns_content = gemini.generate_metadata(st.session_state.text_editor)
            if sns_content:
                st.session_state.generated_sns_content = sns_content
                st.success("✅ タイトル・紹介文・ハッシュタグを生成しました！")
                # ダウンロードセクションに自動スクロール
                st.components.v1.html("""
                <script>
                    setTimeout(function() {
                        const section = window.parent.document.getElementById('download-section');
                        if (section) {
                            section.scrollIntoView({behavior: 'smooth', block: 'start'});
                        }
                    }, 100);
                </script>
                """, height=0)
            else:
                st.error("生成に失敗しました")

    # 生成されたコンテンツを表示・編集可能に
    if st.session_state.generated_sns_content:
        st.subheader("📝 生成されたコンテンツ（編集可能）")

        # コンテンツエディター
        if "sns_content_editor" not in st.session_state:
            st.session_state.sns_content_editor = st.session_state.generated_sns_content

        st.text_area(
            "タイトル・紹介文・ハッシュタグ",
            height=400,
            key="sns_content_editor"
        )

# セクション6: ダウンロード
st.markdown('<div id="download-section"></div>', unsafe_allow_html=True)
st.header("💾 6. ダウンロード")

# ファイル名の確認・編集
if "filename" not in st.session_state or not st.session_state.filename:
    st.session_state.filename = "output"

final_filename = st.text_input(
    "ファイル名（編集可能）",
    value=st.session_state.filename,
    key="filename_input"
)

# 2つのダウンロードボタンを横並びに配置
col1, col2 = st.columns(2)

with col1:
    # テキストダウンロード用の整形処理
    def format_text_for_download(text: str, target_length: int = 14) -> str:
        """
        テキストをダウンロード用に整形
        - 句読点（。、）を削除
        - 14文字程度で適切に改行（句読点の位置を基準に）
        """
        # 既存の改行で分割
        lines = text.split('\n')

        # 新しい行のリスト
        new_lines = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 句点・読点の位置を記録
            # 句点（。）と読点（、）を改行候補位置としてマーク
            chunks = []
            current_chunk = ""

            for char in line:
                if char in ['。', '、']:
                    # 句読点の前までをchunkに追加（句読点は含めない）
                    if current_chunk:
                        chunks.append(current_chunk)
                        current_chunk = ""
                else:
                    current_chunk += char

            # 残りがあれば追加
            if current_chunk:
                chunks.append(current_chunk)

            # chunksを14文字程度でまとめる（できるだけ14文字に近づける）
            current_line = ""
            for chunk in chunks:
                chunk = chunk.strip()
                if not chunk:
                    continue

                if not current_line:
                    # 最初のchunk
                    current_line = chunk
                    continue

                # 現在の行の長さと、chunkを追加した場合の長さ
                current_len = len(current_line)
                combined_len = len(current_line + chunk)

                # 14文字からの距離を計算
                current_distance = abs(target_length - current_len)
                combined_distance = abs(target_length - combined_len)

                # 18文字を超える場合は強制的に改行（上限）
                if combined_len > target_length + 4:
                    new_lines.append(current_line)
                    current_line = chunk
                # どちらが14文字に近いかで判断
                elif combined_distance <= current_distance:
                    # 追加した方が14に近い
                    current_line += chunk
                else:
                    # 追加しない方が14に近い
                    new_lines.append(current_line)
                    current_line = chunk

            # 残りがあれば追加
            if current_line:
                new_lines.append(current_line)

        return '\n'.join(new_lines)

    # テキストダウンロード（テキスト生成済みの場合のみ表示）
    if st.session_state.get("text_editor"):
        # テキストダウンロード（整形済み + タイトル・紹介文・ハッシュタグ）
        # 本文は句読点削除 + 14文字改行
        formatted_main_text = format_text_for_download(st.session_state.text_editor)

        text_download_data = formatted_main_text
        if st.session_state.generated_sns_content and st.session_state.get("sns_content_editor"):
            # SNSコンテンツはそのまま（句読点削除しない）
            text_download_data = formatted_main_text + "\n\n" + st.session_state.sns_content_editor

        st.download_button(
            label="TEXT DOWNLOAD",
            data=text_download_data,
            file_name=f"{final_filename}.txt",
            mime="text/plain",
            key="download_text"
        )
    else:
        # テキスト未生成の場合は何も表示しない（スペースのみ）
        st.write("")

with col2:
    # 動画ファイルをダウンロード（動画生成済みの場合のみ表示）
    if st.session_state.generated_video:
        st.download_button(
            label="VIDEO DOWNLOAD",
            data=st.session_state.generated_video,
            file_name=f"{final_filename}.mp4",
            mime="video/mp4",
            key="download_video"
        )
    else:
        # 動画未生成の場合は何も表示しない（スペースのみ）
        st.write("")

# フッター
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit, Gladia API, Gemini API, VOICEVOX, and MoviePy")
