#!/bin/bash

TZ=UTC-7 date -R;
cd ~/bash-monitoring-pid/
ps -ef | ./proc_check.py
