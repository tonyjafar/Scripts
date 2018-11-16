#!/usr/bin/python
import json
from datetime import datetime
import argparse
import subprocess


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", "-H", help="Elasticsearch host with port", required=True)
    parser.add_argument("--template", "-p", help="Elasticsearch template EXP: filebeat-*", required=True)
    parser.add_argument("--field", "-p", help="Elasticsearch Field EXP: message", required=True)
    parser.add_argument("--count", "-c", help="Count of how many times the string appears in logs", type=int,
                        required=True)
    parser.add_argument("--string", "-s", help="String to search for", required=True)
    parser.add_argument("--time", "-t", help="Add time in minutes", type=int, required=True)
    args = parser.parse_args()
    return args


app_args = get_args()

command = 'curl -XGET -s -H \'Content-Type: application/json\' %s/%s/_search -d \'{"size": %s,"sort"\
: { "@timestamp": "desc"},"query": {"multi_match": {"query" : "%s","fields": ["%s"],"type": "phrase"}}}\'' \
          % (app_args.host, app_args.template, str(app_args.count), app_args.string, app_args.field)

try:
    get_data = subprocess.check_output(command, shell=True)
except Exception as e:
    print('Error - failed connecting to Elasticsearch')
    print(str(e))
    exit(2)

try:
    get_json = json.loads(get_data)
except Exception as e:
    print('Error - failed to get date from Elasticsearch')
    print(str(e))
    exit(2)

now = datetime.now()
errors = []
x = 0

try:
    while x < len(get_json):
        elk_time = get_json["hits"]['hits'][x]['_source']['@timestamp']
        elk_time = datetime.strptime(elk_time, '%Y-%m-%dT%H:%M:%S.000Z')
        diff = now - elk_time
        mins = diff.total_seconds() / 60
        correct_time = mins - 60
        if correct_time <= app_args.time:
            errors.append(correct_time)
        x += 1
except Exception as e:
    pass

if len(errors) >= app_args.count:
    print('Critical - There is %i Entries for %s' % (len(errors), app_args.string))
    exit(2)
else:
    print('OK')
    exit(0)
