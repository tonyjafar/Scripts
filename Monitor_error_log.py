import os
import sys
import datetime


if len(sys.argv) < 2:
    print('usage :.%s file_path' % sys.argv[0])
    sys.exit(1)

log_file = sys.argv[1]
old_errors = False
today = str(datetime.datetime.today())


def create_error(append=False):
    if append:
        with open('/root/bin/errors', 'a') as e:
            e.write(today)
            e.write('\n')
    else:
        with open('/root/bin/errors', 'w') as e:
            e.write(today)
            e.write('\n')

if not os.path.isfile('/root/bin/pos'):
    with open('/root/bin/pos', 'w') as f:
        f.write('0')

if os.path.isfile('/root/bin/errors'):
    old_errors = True

with open('/root/bin/pos', 'r') as f:
    pos = int(f.read().strip())

with open(log_file) as f:
    f.seek(pos)
    with open('/root/bin/pos', 'w') as p:
        for line in f:
            pass
        new_pos = str(f.tell())
        p.write(new_pos)
    if int(pos) < os.path.getsize(log_file) and old_errors:
        print('Critical, New and Old Errors in Logs')
        create_error(append=True)
        sys.exit(2)
    elif int(pos) < os.path.getsize(log_file):
        print('Critical, New Errors in Logs')
        create_error()
    elif int(pos) > os.path.getsize(log_file):
        f.seek(0)
        for line in f:
            pass
        if f.tell() > 0 and old_errors:
            print('Critical, New and Old Errors in Logs')
            with open('/root/bin/pos', 'w') as p:
                p.write(str(f.tell()))
            create_error(append=True)
            sys.exit(2)
        elif f.tell() > 0:
            print('Critical, New Errors in Logs')
            with open('/root/bin/pos', 'w') as p:
                p.write(str(f.tell()))
            create_error()
        else:
            with open('/root/bin/pos', 'w') as p:
                p.write(str(f.tell()))
            print('OK')
            sys.exit(0)
    else:
        print('OK')
        sys.exit(0)

