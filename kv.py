import os
import json
import requests


class KV:
    """Class of CF KV storage api."""
    url: str = f'https://api.cloudflare.com/client/v4/accounts/{os.getenv("ACCOUNT_ID")}/storage/kv/' + \
               f'namespaces/{os.getenv("NAMESPACE_ID")}/values/{os.getenv("KEY_NAME")}'
    headers: dict = {
        "Authorization": f'Bearer {os.getenv("BEARER_TOKEN")}',
        "Content-Type": "application/json"
    }
    result: dict = {}

    def query(self) -> dict:
        res = requests.get(self.url, headers=self.headers)
        self.result = res.json()
        return self.result

    def update(self, value) -> dict:
        res = requests.put(self.url, headers=self.headers, data=json.dumps(value))
        return res.json()
