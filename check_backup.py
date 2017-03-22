#!/usr/bin/python
import os
import sys
import datetime

cron_error = False
last_run_error = False

if os.path.isfile("/root/bin/last_backup.out"):
    cron_error = True

with open('/usr/bin/last_run', 'r') as f:
    for line in f:
        line = line.strip()
        now = datetime.datetime.strptime(str(datetime.datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d")
        last_run = datetime.datetime.strptime(str(line), "%Y-%m-%d")

if 'days' in str(now - last_run):
    last_run_error = True


if cron_error and last_run_error:
    print("Critical - Backup Job faild - last run " + str(line))
    print('Error File: /root/bin/last_backup.out')
    sys.exit(2)

if cron_error:
    print("Cron Backup Job faild")
    print('Error File: /root/bin/last_backup.out')
    sys.exit(2)

if last_run_error:
    print("Critical - Backup Job last run " + str(line))
    sys.exit(2)

if not cron_error and not last_run_error:
    print("OK - Backup job running without errors")
    sys.exit(0)
