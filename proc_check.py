#!/usr/bin/env python
import os
import sys
from typing import List, Union
from datetime import datetime
import requests
from dotenv import load_dotenv
load_dotenv()


class Proc:
    data: str
    info: Union[List, None] = None

    def __init__(self, data):
        self.data = data
        info = data.split('\n')
        self.info = [i.strip() for i in info if i.strip()]

    def grep(self, s):
        return [line for line in self.info if s in line]
    
    def pid(self, s):
        res = self.grep(s)
        try:
            return "".join(res).strip().split()[1]
        except IndexError:
            return ""


class KV:
    """Class of CF KV storage api."""
    url: str = f'https://api.cloudflare.com/client/v4/accounts/{os.getenv("ACCOUND_ID")}/storage/kv/' +\
            f'namespaces/{os.getenv("NAMESPACE_ID")}/values/{os.getenv("KEY_NAME")}'
    headers: dict = {
                "Authorization": f'Bearer {os.getenv("BEARER_TOKEN")}',
                "Accept": "application/json"
            }
    result: dict = {}

    def query(self) -> dict:
        res = requests.get(self.url, headers=self.headers)
        self.result = res.json()
        return self.result
    
    def update(self, value) -> dict:
        res = requests.put(self.url, headers=self.headers, data=value)
        return res.json()


def main():
    # should have no arguments
    if len(sys.argv) > 1:
        return
    data = sys.stdin.read()
    if not data:
        return
    proc = Proc(data)
    kv = KV()
    # print(f'Num line of input: {len(proc.info)}')
    now = datetime.now()
    now_ts = int(now.timestamp())
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    processes = [
        'promtail', 
        'grafana-server', 
        'redis-server',
        'cadvisor',
        'portainer',
    ]

    # read previus status
    status = kv.query()
    # check new status
    for p in processes:
        try:
            pid = int(proc.pid(p))
            status[p] = [pid, now_ts, now_str]
        except ValueError:
            print(f'{p} not found.')
    # update KV with new status
    print(f'current status: {status}')
    res = kv.update(value=status)
    

if __name__ == "__main__":
    main()
