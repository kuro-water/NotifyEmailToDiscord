import json
from urllib.request import Request, urlopen
import time

WEBHOOK_POST_LIMIT = 2000


class Discord:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def _on_error(self, e: Exception):
        raise e

    def _post(
        self, message: str, webhook_url: str = "default"
    ):  # webhookを用いてdiscordに投稿
        if webhook_url == "default":
            webhook_url = self.webhook_url

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "DiscordBot (private use) Python-urllib/3.10",
        }
        data = {"content": message}
        request = Request(
            webhook_url,
            data=json.dumps(data).encode(),
            headers=headers,
        )
        with urlopen(request) as res:
            assert res.getcode() == 204
        print("sent '" + message + "'")
        time.sleep(1)

    def post(self, message: str, webhook_url: str = "default"):
        # メッセージがDISCORD_POST_LIMITを超える場合は分割して投稿
        # webhookにおいては、2000字を超過するとエラーとなる
        try:
            while message:
                if WEBHOOK_POST_LIMIT < len(message):
                    self._post(message[:WEBHOOK_POST_LIMIT], webhook_url)
                    message = message[WEBHOOK_POST_LIMIT:]
                else:
                    self._post(message, webhook_url)
                    message = ""
        except Exception as e:
            self._on_error(e)
