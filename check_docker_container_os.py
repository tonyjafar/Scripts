#!/usr/bin/python
import subprocess

docker_list = subprocess.check_output('docker ps | awk \'{if (NR!=1) {print $NF}}\'', shell=True).split('\n')
docker_names = []

for line in docker_list[:-1]:
    docker_names.append(line.strip())

for name in docker_names:
    for line in str(subprocess.check_output('docker exec -i --user root %s cat /etc/os-release' % name, shell=True)).split('\n'):
        if 'PRETTY_NAME' in str(line):
            line = line.split('=')
            print(name + ' is ' + line[1])

