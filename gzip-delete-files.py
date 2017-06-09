#!/usr/bin/python
import os
import subprocess
import argparse
import time


def getargs():
    parser = argparse.ArgumentParser(description='zipping and deleteing old files.')

    parser.add_argument('-p', '--path', required=True, action='store', nargs='+',
                        help='Path to a folder to process, space separated for more than one path')
    parser.add_argument('-x', '--extension', required=True, action='store',
                        help='extension of files to compress')
    parser.add_argument('-dc', '--daysToCompress', required=True, action='store',
                        help='number of days to compress files')
    parser.add_argument('-dd', '--daysToDelete', required=True, action='store',
                        help='number of days to delete files')
    args = parser.parse_args()

    return args

app_args = getargs()
now = time.time()

for folder in app_args.path:
    if os.path.isdir(folder):
        os.chdir(folder)
        for x in os.listdir(folder):
            x = os.path.join(folder, x)
            if x.endswith(app_args.extension):
                if os.stat(x).st_mtime < now - int(app_args.daysToCompress) * 86400:
                    subprocess.call('/bin/gzip -f %s' % x, shell=True)
            if x.endswith('gz'):
                if os.stat(x).st_mtime < now - int(app_args.daysToDelete) * 86400:
                    subprocess.call('/bin/rm -f %s' % x, shell=True)

    else:
        print('Wrong path')




