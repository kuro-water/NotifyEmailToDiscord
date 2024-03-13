from datetime import datetime
import time

from email_from_imap import Email_from_imap
from post_discord import Discord

# -------------------設定項目----------------
ACCOUNTS_LIST = [
    {
        "server": "imap.mail.yahoo.co.jp",
        "user": "********@yahoo.co.jp",
        "password": "********",
        "webhook_url": "https://discord.com/api/webhooks/********",
    },
    {
        # gmailの場合、imapの有効化（24年6月からデフォルトでオンになるらしい）と、
        # アプリパスワードにの設定が必要
        "server": "imap.gmail.com",
        "user": "********@gmail.com",
        "password": "********",
        "webhook_url": "https://discord.com/api/webhooks/********",
    },
    # 追加可能
]
NOTIFY_INTERVAL = 60 * 60  # 秒単位
# ------------------------------------------


def notify_new_mail(account: dict, notified_ids: list):
    # 新着メールの通知(起動時のみ未読メールを全て通知)
    print("getting new emails...")
    email = Email_from_imap(account["server"], account["user"], account["password"])
    mail_list = email.get("UNSEEN")

    mail_list = [mail for mail in mail_list if mail["id"] not in notified_ids]
    notified_ids.extend(mail["id"] for mail in mail_list)

    if len(mail_list) == 0:
        print(f"{account['user']}: There are no new emails.")
        return

    discord = Discord(account["webhook_url"])
    discord.post(
        f"# {account['user']}\n"
        f"Incomming {len(mail_list)} email{'' if len(mail_list) == 1 else 's'}.\n"
        f"----------------------------------------"
    )

    for mail in mail_list:
        discord.post(
            f"### Subject: {mail['subject']}\n"
            f"Date: {mail['date']}\n"
            f"From: {mail['from']}\n"
            f"To:{mail['to']}\n"
            f"----------------------------------------"
        )


def notify_unread(account: dict):
    # 未読メールの通知(一日一回)
    print("getting unread emails...")
    email = Email_from_imap(account["server"], account["user"], account["password"])
    mail_list = email.get("UNSEEN")

    discord = Discord(account["webhook_url"])
    discord.post(f"## {account['user']}")

    if len(mail_list) == 0:
        discord.post("There are no unread emails.")
        return

    is_multiple = len(mail_list) == 1
    discord.post(
        f"# There {'is' if is_multiple else 'are'} {len(mail_list)} unread email{'' if is_multiple else 's'}.\n"
        f"----------------------------------------"
    )

    for mail in mail_list:
        discord.post(
            f"### Subject: {mail['subject']}\n"
            f"Date: {mail['date']}\n"
            f"From: {mail['from']}\n"
            f"To:{mail['to']}\n"
            f"----------------------------------------"
        )


if __name__ == "__main__":
    print("starting...")
    notified_ids = []
    last_notified_day = datetime.now().day
    while True:
        now = datetime.now()
        for account in ACCOUNTS_LIST:
            notify_new_mail(account, notified_ids)
            if last_notified_day != now.day:
                notify_unread(account)
                last_notified_day = now.day
        time.sleep(NOTIFY_INTERVAL)
