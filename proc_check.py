#!/usr/bin/env python3
from initial import logger
from kv import KV
import sys
import json
from typing import List, Union
from datetime import datetime


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


def main():
    # should have no arguments
    if len(sys.argv) > 1:
        return
    data = sys.stdin.read()
    if not data:
        return
    proc = Proc(data)
    kv = KV()
    print(f'Total processes num: {len(proc.info)}')
    now = datetime.now()
    now_ts = int(now.timestamp())
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    processes = [
        'redis-server',
        'portainer',
        'promtail',
        'mongodb',
        'grafana',
    ]

    # read previus status
    status = kv.query()
    # check new status
    for p in processes:
        try:
            pid = int(proc.pid(p))
            status[p] = {"pid": pid, "ts": now_ts, "last_seen": now_str}
            logger.info(f'pve.{p} - pid: {pid}, ts: {now_ts}, last_seen: {now_str}')
        except ValueError:
            print(f'{p} not found.')
    # update KV with new status
    new_status = {k: v for k, v in status.items() if k in processes}
    print(f'current status: {json.dumps(new_status, indent=2)}')
    res = kv.update(value=new_status)


if __name__ == "__main__":
    main()
