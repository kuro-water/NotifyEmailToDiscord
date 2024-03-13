import email
import imaplib
from email.header import decode_header


class Email_from_imap:
    def __init__(self, server: str, user: str, password: str):
        self.server = server
        self.user = user
        self.password = password

    def get(self, serach_str: str = "ALL"):
        # 参考:https://qiita.com/jsaito/items/a058611cf9386addbc12
        def get_header(msg, name):
            header = "none"
            if msg[name]:
                header = ""
                for tup in decode_header(str(msg[name])):
                    if type(tup[0]) is bytes:
                        charset = tup[1]
                        if charset:
                            header += tup[0].decode(tup[1])
                        else:
                            header += tup[0].decode()
                    elif type(tup[0]) is str:
                        header += tup[0]
            return header

        imap = imaplib.IMAP4_SSL(self.server)
        imap.login(self.user, self.password)
        imap.select(
            "INBOX", readonly=True
        )  # 読み取り専用にしないと、未読メールが既読に代わってしまう

        _, data = imap.search(None, serach_str)
        datas = data[0].split()

        mail_list = []
        for num in datas:
            _, data = imap.fetch(num, "(RFC822)")
            msg = email.message_from_bytes(data[0][1])
            date = get_header(msg, "Date")
            _from = get_header(msg, "From")
            to = get_header(msg, "To")
            subject = get_header(msg, "Subject")
            id = get_header(msg, "Message-ID")
            mail_list.append(
                {"date": date, "from": _from, "to": to, "subject": subject, "id": id}
            )

        imap.close()
        imap.logout()
        return mail_list


if __name__ == "__main__":
    SERVER = "imap.mail.yahoo.co.jp"
    USER = "********@yahoo.co.jp"
    PASSWORD = "********"
    SERACH_STR = "UNSEEN"

    e = Email_from_imap(SERVER, USER, PASSWORD)
    mail_list = e.get(SERACH_STR)
    print(mail_list)
