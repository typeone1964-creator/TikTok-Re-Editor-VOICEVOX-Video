# 📦 GitHubで他の人と共有する方法

このガイドに従って、あなたのアプリをGitHubで公開しましょう！

---

## ✅ 準備完了チェックリスト

公開前に以下を確認してください：

- [x] `.env`ファイルに個人のAPIキーが入っている → **公開されません**（.gitignoreで除外済み）
- [x] `README.md`が最新の機能を反映している → **完了**
- [x] `.gitignore`が適切に設定されている → **完了**

---

## 🚀 GitHubで公開する手順

### ステップ1: GitHubアカウントを作成（まだの場合）

1. https://github.com/ にアクセス
2. **「Sign up」**をクリック
3. メールアドレス、パスワードを入力してアカウント作成

---

### ステップ2: 新しいリポジトリを作成

1. GitHubにログイン
2. 右上の **「+」** → **「New repository」**をクリック
3. 以下を入力：
   - **Repository name**: `TikTok-Re-Editor-VOICEVOX-Video`（任意の名前でOK）
   - **Description**: `TikTok形式の動画を自動生成するアプリ`
   - **Public** を選択（誰でも見られる）
   - ✅ **「Add a README file」のチェックは外す**（既にREADMEがあるため）
4. **「Create repository」**をクリック

---

### ステップ3: ローカルのコードをGitHubにアップロード

#### Gitがインストールされているか確認

**Windowsの場合：**
```bash
git --version
```

**Macの場合：**
```bash
git --version
```

表示されればOK。表示されない場合は https://git-scm.com/ からインストール。

---

#### アップロード手順

1. **ターミナル/PowerShell**を開く
2. アプリのフォルダに移動：
   ```bash
   cd /Users/hirumakazue/dev/miyabi_0.15/TikTok-Re-Editor-VOICEVOX-Video
   ```

3. 以下のコマンドを順番に実行：

   ```bash
   # Gitリポジトリを初期化（まだの場合）
   git init

   # すべてのファイルを追加（.gitignoreで除外されたファイルは自動で除外される）
   git add .

   # コミット（変更を記録）
   git commit -m "初回コミット: TikTok動画生成アプリ"

   # GitHubのリポジトリと接続（YOUR_USERNAMEとYOUR_REPOを自分のものに変更）
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

   # GitHubにアップロード
   git branch -M main
   git push -u origin main
   ```

4. GitHubのユーザー名とパスワード（またはトークン）を入力

---

### ステップ4: 公開完了！

GitHubのリポジトリページにアクセスすると、コードが公開されています！

**共有用URL:**
```
https://github.com/YOUR_USERNAME/YOUR_REPO
```

このURLを他の人に教えれば、誰でもダウンロードして使えます！

---

## 📤 コードを更新する方法

アプリに新機能を追加した場合、以下のコマンドで更新できます：

```bash
# 変更を記録
git add .
git commit -m "新機能を追加: 結合動画の自動生成"

# GitHubにアップロード
git push
```

---

## 🙋 よくある質問

### Q1: APIキーがGitHubに公開されませんか？

**A**: いいえ、`.gitignore`で`.env`ファイルが除外されているため、APIキーは公開されません。

確認方法：
```bash
git status
```
を実行して、`.env`が表示されなければOKです。

---

### Q2: 他の人が使うにはどうすればいい？

**A**: 以下のURLを共有してください：

```
https://github.com/YOUR_USERNAME/YOUR_REPO
```

相手は以下の手順で使えます：
1. そのURLにアクセス
2. 緑色の「Code」→「Download ZIP」
3. README.mdの手順に従ってセットアップ

---

### Q3: リポジトリを非公開にしたい

**A**: GitHubのリポジトリページで：
1. **Settings**タブをクリック
2. 一番下の**「Change visibility」**→**「Change to private」**

---

### Q4: 更新がうまくいかない

**A**: 以下を試してください：

```bash
# 現在の状態を確認
git status

# 競合がある場合
git pull origin main
git push
```

---

## 🎉 完了！

これで他の人もあなたのアプリを使えるようになりました！

**共有したら、このファイル（GITHUB_SETUP.md）は削除してOKです。**
