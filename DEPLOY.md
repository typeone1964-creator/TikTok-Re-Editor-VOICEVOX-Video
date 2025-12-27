# 🚀 Streamlit Community Cloudへのデプロイ手順

このドキュメントでは、TikTok Re-Editor VOICEVOXをStreamlit Community Cloudに無料でデプロイする手順を説明します。

## 📋 必要なもの

- GitHubアカウント（無料）
- Streamlit Community Cloudアカウント（無料・GitHubと連携）

---

## ステップ1: GitHubリポジトリの作成

### 1-1. GitHubアカウントの作成（未登録の場合）

1. [github.com](https://github.com/)にアクセス
2. **「Sign up」**をクリック
3. メールアドレス、パスワードを入力
4. アカウントを作成

### 1-2. 新しいリポジトリを作成

1. GitHubにログイン
2. 右上の **「+」** → **「New repository」** をクリック
3. リポジトリ名を入力（例: `TikTok-Re-Editor-VOICEVOX`）
4. **Public**（公開）を選択
5. **「Create repository」** をクリック

### 1-3. コードをGitHubにアップロード

**方法A: GitHub Web UIを使う（初心者向け）**

1. 作成したリポジトリのページで **「uploading an existing file」** をクリック
2. 以下のファイル・フォルダをドラッグ&ドロップ：
   - `app.py`
   - `requirements.txt`
   - `.gitignore`
   - `README.md`
   - `utils/` フォルダ全体
   - `セットアップ手順.md`
   - `.env.example`
3. **「Commit changes」** をクリック

**方法B: Git コマンドを使う（上級者向け）**

```bash
# このフォルダで実行
cd /path/to/TikTok-Re-Editor-VOICEVOX

# Gitリポジトリを初期化
git init

# すべてのファイルを追加
git add .

# コミット
git commit -m "Initial commit"

# GitHubリポジトリと連携
git remote add origin https://github.com/yourusername/TikTok-Re-Editor-VOICEVOX.git

# プッシュ
git branch -M main
git push -u origin main
```

⚠️ **重要**: `.env`ファイルは`.gitignore`に含まれているため、アップロードされません。APIキーは安全です。

---

## ステップ2: Streamlit Community Cloudでデプロイ

### 2-1. Streamlit Community Cloudアカウント作成

1. [share.streamlit.io](https://share.streamlit.io/)にアクセス
2. **「Sign in with GitHub」** をクリック
3. GitHubアカウントでログイン
4. Streamlitに権限を許可

### 2-2. アプリをデプロイ

1. **「New app」** ボタンをクリック
2. 以下を設定：
   - **Repository**: 作成したリポジトリを選択（例: `yourusername/TikTok-Re-Editor-VOICEVOX`）
   - **Branch**: `main`
   - **Main file path**: `app.py`
3. **「Deploy!」** をクリック

### 2-3. デプロイ完了！

- 数分待つとアプリが起動します
- URLが発行されます（例: `https://yourusername-tiktok-re-editor-voicevox.streamlit.app`）
- このURLを共有すれば、誰でもアプリを使えます！

---

## ステップ3: 使い方を他の人に説明

デプロイ完了後、以下のURLを共有してください：

```
https://yourusername-tiktok-re-editor-voicevox.streamlit.app
```

### ユーザーへの説明

**アプリを使うには：**

1. **VOICEVOXをダウンロード・起動**
   - [voicevox.hiroshiba.jp](https://voicevox.hiroshiba.jp/)からダウンロード
   - 自分のPCで起動（必須）

2. **アプリにアクセス**
   - 上記URLをブラウザで開く

3. **APIキーを入力（動画から生成する場合のみ）**
   - サイドバーでGladia APIとGemini APIキーを入力
   - テキストファイルから生成する場合はAPIキー不要

4. **使い始める**
   - テキストファイルをアップロードして音声生成！

---

## 📚 補足情報

### アプリの更新方法

コードを更新した場合：

1. GitHubリポジトリにプッシュ
   ```bash
   git add .
   git commit -m "Update app"
   git push
   ```

2. Streamlit Community Cloudが自動的に再デプロイ
   - 数分で最新版に更新されます

### アプリの停止・削除

1. [share.streamlit.io](https://share.streamlit.io/)にログイン
2. アプリの設定（⚙️）→ **「Delete app」**

### よくある質問

**Q: 無料で使えますか？**
A: はい、Streamlit Community Cloudは完全無料です（2024年12月現在）。

**Q: VOICEVOXもクラウドで動きますか？**
A: いいえ、VOICEVOXは各ユーザーが自分のPCで起動する必要があります。

**Q: APIキーは安全ですか？**
A: はい、各ユーザーが自分のAPIキーを入力するため、あなたのAPIキーが共有されることはありません。

**Q: 同時に何人使えますか？**
A: Streamlit Community Cloudの無料プランでは、同時接続数に制限があります（通常5-10人程度）。

**Q: カスタムドメインを使えますか？**
A: 無料プランではできません。有料プラン（Streamlit for Teams）が必要です。

---

## 🎉 完了！

これでアプリがWebで公開され、URLを共有するだけで誰でも使えるようになりました！

質問があれば、GitHubのIssueで質問してください。
