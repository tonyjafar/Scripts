import time
import tarfile
import os
import sys

now = time.time()

if len(sys.argv) < 3:
    print('Usage: ./script <path to folder to gzip> <path were to save backup>')
    sys.exit(1)

monthly = False
weekly = False
daily = False
backup_path = sys.argv[1]
backup_dir = sys.argv[2]

if time.strftime('%d') == '01':
    monthly = True

if time.strftime('%A') == 'Sunday' and not monthly:
    weekly = True

if not weekly and not monthly:
    daily = True


if monthly:
    try:
        backup_name = "monthly-" + str(time.strftime('%Y-%m-%d')) + '.tar.gz'
        if not os.path.isdir(backup_dir + '/monthly'):
            os.mkdir(backup_dir + '/monthly')
        os.chdir(backup_dir + '/monthly')
        tar = tarfile.open(backup_name, "w:gz")
        tar.add(backup_path, arcname='my_backup')
        tar.close()
    except Exception as e:
        with open('/root/bin/last_backup.out', 'w') as er:
            er.write(str(e))
        exit(2)

if weekly:
    try:
        backup_name = "weekly-" + str(time.strftime('%Y-%m-%d')) + '.tar.gz'
        if not os.path.isdir(backup_dir + '/weekly'):
            os.mkdir(backup_dir + '/weekly')
        os.chdir(backup_dir + '/weekly')
        tar = tarfile.open(backup_name, "w:gz")
        tar.add(backup_path, arcname='my_backup')
        tar.close()
        for x in os.listdir(backup_dir + '/weekly'):
            x = os.path.join(backup_dir + '/weekly', x)
            if os.stat(x).st_mtime < now - 14 * 86400:
                if os.path.isfile(x):
                    os.remove(x)
    except Exception as e:
        with open('/root/bin/last_backup.out', 'w') as er:
            er.write(str(e))
        exit(2)

if daily:
    try:
        backup_name = "daily-" + str(time.strftime('%Y-%m-%d')) + '.tar.gz'
        if not os.path.isdir(backup_dir + '/daily'):
            os.mkdir(backup_dir + '/daily')
        os.chdir(backup_dir + '/daily')
        tar = tarfile.open(backup_name, "w:gz")
        tar.add(backup_path, arcname='my_backup')
        tar.close()
        for x in os.listdir(backup_dir + '/daily'):
            x = os.path.join(backup_dir + '/daily', x)
            if os.stat(x).st_mtime < now - 7 * 86400:
                if os.path.isfile(x):
                    os.remove(x)
    except Exception as e:
        with open('/root/bin/last_backup.out', 'w') as er:
            er.write(str(e))
        exit(2)

with open('/root/bin/last_run', 'w') as t:
    t.write(str(time.strftime('%Y-%m-%d')))

