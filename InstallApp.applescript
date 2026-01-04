-- TikTok Re-Editor VOICEVOX Video
-- Mac用 ワンクリックインストールアプリ
-- このスクリプトをアプリケーションとして保存すると、ダブルクリックで実行できます

on run
	try
		-- スクリプトのディレクトリを取得
		set scriptPath to POSIX path of (path to me)
		set scriptDir to do shell script "dirname " & quoted form of scriptPath

		-- ウェルカムダイアログ
		display dialog "TikTok Re-Editor VOICEVOX Video" & return & return & "Mac用インストーラーを開始します。" & return & return & "必要な環境：" & return & "• Python 3" & return & "• VOICEVOX" & return & return & "インストールには数分かかる場合があります。" buttons {"キャンセル", "インストール開始"} default button "インストール開始" with icon note with title "TikTok Re-Editor VOICEVOX Video"

		if button returned of result is "キャンセル" then
			return
		end if

		-- インストールスクリプトを実行
		set installScript to scriptDir & "/INSTALL_MAC.sh"

		-- ターミナルでスクリプトを実行
		tell application "Terminal"
			activate
			do script "cd " & quoted form of scriptDir & " && bash " & quoted form of installScript
		end tell

		-- 完了メッセージ（ターミナルで実行中なので、すぐには表示しない）
		delay 2
		display dialog "インストールスクリプトをターミナルで実行中です。" & return & return & "ターミナルに表示される指示に従ってください。" & return & return & "インストールが完了したら：" & return & "1. VOICEVOXを起動" & return & "2. ./run.sh を実行" buttons {"OK"} default button "OK" with icon note with title "インストール実行中"

	on error errMsg number errNum
		-- エラーハンドリング
		display dialog "エラーが発生しました：" & return & return & errMsg & return & "エラー番号：" & errNum & return & return & "README.mdを確認するか、手動でターミナルから以下を実行してください：" & return & "cd (フォルダパス)" & return & "bash INSTALL_MAC.sh" buttons {"OK"} default button "OK" with icon stop with title "エラー"
	end try
end run
