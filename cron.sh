#!/bin/bash

TZ=UTC-7 date -R;
cd ~/bash-monitor-pid/
ps -ef | ./proc_check.py
