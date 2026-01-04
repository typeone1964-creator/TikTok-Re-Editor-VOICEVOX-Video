# Mac用インストールアプリのビルド手順

このドキュメントでは、`InstallApp.applescript`から`InstallApp.app`をビルドする方法を説明します。

## 📦 ビルド方法

### 方法1: コマンドラインでビルド（推奨）

ターミナルで以下のコマンドを実行：

```bash
cd /path/to/TikTok-Re-Editor-VOICEVOX-Video
osacompile -o InstallApp.app InstallApp.applescript
```

### 方法2: スクリプトエディタでビルド

1. `InstallApp.applescript` をダブルクリック
2. スクリプトエディタで開く
3. 「ファイル」→「書き出す」を選択
4. フォーマット: **アプリケーション**
5. 「コードサインなし」を選択（個人使用の場合）
6. 「保存」をクリック

## 🚀 ビルド後の確認

```bash
# アプリが正しく作成されたか確認
ls -la InstallApp.app

# 実行テスト（オプション）
open InstallApp.app
```

## 📤 配布方法

### GitHub Releasesで配布（推奨）

1. GitHubリポジトリの「Releases」ページに移動
2. 「Create a new release」をクリック
3. `InstallApp.app`を圧縮：
   ```bash
   zip -r InstallApp.app.zip InstallApp.app
   ```
4. ZIPファイルをReleasesに添付

### ダウンロード後のユーザー手順

1. `InstallApp.app.zip`をダウンロード
2. ZIPを解凍
3. `InstallApp.app`をダブルクリック
4. **セキュリティ警告が出た場合**: 右クリック→「開く」

## 🔒 コード署名（オプション）

より安全に配布したい場合は、Apple Developer Accountでコード署名できます：

```bash
codesign --force --deep --sign "Developer ID Application: Your Name" InstallApp.app
```

## 📝 注意事項

- `.app`ファイルはバイナリなので、Gitリポジトリには含まれません
- ソースコード（`.applescript`）はGitで管理されます
- ユーザーは自分で`.applescript`から`.app`をビルドすることもできます
