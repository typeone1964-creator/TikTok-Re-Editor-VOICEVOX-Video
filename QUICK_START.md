# ⚡ 超簡単！3ステップで始める

**中学生でもできる！** コピペだけで完了します！

---

## 📥 ステップ1: ダウンロード（1分）

### Mac用ワンクリックインストーラー（推奨）

**こちらをクリック:**
[![Download](https://img.shields.io/badge/Download-InstallApp.app.zip-blue?style=for-the-badge&logo=apple)](https://github.com/typeone1964-creator/TikTok-Re-Editor-VOICEVOX-Video/releases/latest/download/InstallApp.app.zip)

ダウンロードしたら **ステップ2へ進んでください**

---

### または、リポジトリ全体をダウンロード

1. この画面の上にある **緑色の「Code」ボタン** をクリック
2. **「Download ZIP」** をクリック
3. ダウンロードしたファイルを **デスクトップに解凍**
   - Windows: 右クリック → 「すべて展開」
   - Mac: ダブルクリック

---

## 🛠️ ステップ2: セットアップ（5分）

### まず、2つの無料ソフトをインストール

#### A. Python（必須）
1. https://www.python.org/downloads/ を開く
2. **黄色い「Download Python」ボタン** をクリック
3. ダウンロードしたファイルを開く
4. ✅ **「Add Python to PATH」に必ずチェック！**（重要）
5. 「Install Now」をクリック
6. 完了！

#### B. VOICEVOX（必須）
1. https://voicevox.hiroshiba.jp/ を開く
2. **「ダウンロード」ボタン** をクリック
3. お使いのOS（Windows/Mac）を選んでダウンロード
4. ダウンロードしたファイルを開いてインストール
5. 完了！

### 次に、自動セットアップを実行

#### 🍎 Macの場合

**方法A: ワンクリックインストール（超簡単！推奨）**

1. `InstallApp.applescript` をダブルクリック
2. スクリプトエディタが開いたら、再生ボタン（▶️）をクリック
3. 「インストール開始」をクリック
4. ターミナルが開いて自動でインストール開始
5. 「✓ インストール完了！」と表示されたら成功！

**または、.appファイルから実行：**
1. [BUILD_APP.md](BUILD_APP.md) の手順で `InstallApp.app` を作成
2. `InstallApp.app` をダブルクリック
3. 完了！

**方法B: ターミナルからインストール**

1. **「アプリケーション」→「ユーティリティ」→「ターミナル」** を開く
2. 以下のコマンドを **1行ずつコピペして実行**：

```bash
# 1. デスクトップのフォルダに移動（フォルダ名を確認してください）
cd ~/Desktop/TikTok-Re-Editor-VOICEVOX-Video-main

# 2. インストールスクリプトを実行（これだけでOK！）
bash INSTALL_MAC.sh
```

3. 「✓ インストール完了！」と表示されたら成功！

**💡 ヒント:**
- フォルダ名が違う場合（例: `TikTok-Re-Editor-VOICEVOX-Video`）は、`cd`の後のフォルダ名を変更してください
- コピペの方法: コマンドをドラッグして選択 → `Command + C` → ターミナルに貼り付け `Command + V` → Enter

#### 🪟 Windowsの場合

1. 解凍したフォルダを開く
2. **`setup.bat`** をダブルクリック
3. 画面の指示に従う（自動で進みます）
4. 「セットアップ完了！」と表示されたら成功！

---

## 🚀 ステップ3: 起動（10秒）

### 毎回この手順で起動します

#### 1. VOICEVOXを起動（必ず最初に！）
VOICEVOXアプリを起動してください。

#### 2. アプリを起動

**🍎 Macの場合（ターミナルから）:**

セットアップで開いたターミナルで、以下を実行：

```bash
./run.sh
```

または、新しいターミナルを開いて：

```bash
cd ~/Desktop/TikTok-Re-Editor-VOICEVOX-Video-main
./run.sh
```

4秒後にブラウザが自動的に開きます！

**🪟 Windowsの場合:**

1. `run.bat` をダブルクリック
2. 4秒後にブラウザが自動的に開きます

**完成！🎉**

---

## 📝 使い方（超簡単）

1. **「テキストから生成」タブ** をクリック
2. テキストを入力（または .txt ファイルをアップロード）
3. **「FORMAT TEXT」** をクリック
4. キャラクターを選ぶ
5. **「GENERATE AUDIO」** をクリック
6. **「GENERATE VIDEO」** をクリック
7. 動画ができた！ダウンロードして完成！

---

## 🆘 うまくいかない時

### ❌ Mac: 「"run.command"は開いていません」と表示される
→ **解決方法:** ターミナルから実行してください
```bash
cd ~/Desktop/TikTok-Re-Editor-VOICEVOX-Video-main
bash INSTALL_MAC.sh
```
インストール後は `./run.sh` で起動できます

### ❌ Mac: 「アクセス権限がありません」と表示される
→ **解決方法:** ターミナルで以下を実行
```bash
cd ~/Desktop/TikTok-Re-Editor-VOICEVOX-Video-main
chmod +x *.sh
./run.sh
```

### ❌ 「Pythonがインストールされていません」と出る
→ Pythonをインストールする時に **「Add Python to PATH」にチェックを入れ忘れた**
→ Pythonをアンインストールして、もう一度インストール（今度はチェックを入れる）

### ❌ 「VOICEVOXが起動していません」と出る
→ VOICEVOXアプリを先に起動してから、`run.bat`/`run.sh` をクリック

### ❌ それでもダメな場合
→ 詳しい説明は **README.md** を見てください
→ それでもわからない場合は、GitHub の Issues で質問してください

---

## 💡 ヒント

- **動画の文字起こしは使わなくてOK**（APIキー不要で使えます）
- **テキストファイルさえあれば、すぐに動画が作れます**
- **オフラインでも動画生成できます**（音声と動画はPCで作成）

---

## 🎬 完成！

これで、あなたもTikTok形式の動画が作れるようになりました！

わからないことがあれば、**README.md** を見るか、GitHub で質問してください。

**楽しんでください！🎉**
