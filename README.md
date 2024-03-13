# NotifyEmailToDiscord
新着メールが来たらDiscordにwebhook経由でメッセージを送ってくれるpythonプログラムです。<br>
メールの取得のためimapサーバーにreadonlyでアクセスします。<br>
一日一回未読メールを全て通知する機能も付いています。<br>
広告など未読メールを無視していると、大量に通知が送られたり、リクエストが多すぎてエラーを吐いたりします。<br>
email_to_discord_open.py内にメアドやwebhookURLを設定し、実行してください。<br>
単純な作りなので好きに味付けして使ってね<br>
<br>
また、製作にあたり以下の記事を参考にさせていただきました。<br>
DiscordにPythonで投稿する方法(bot/Webhook)<br>
https://zenn.dev/karaage0703/articles/926f18ba04e093<br>
Python の標準ライブラリでメールをデコードする<br>
https://qiita.com/jsaito/items/a058611cf9386addbc12<br>

p.s.
スマホのgmailに通知が来たり来なかったりして困ってます。
何か解決法知りませんか？
