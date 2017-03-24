import requests
import sys

if len(sys.argv) < 2:
    print('usage: apache_scrape <url>')
    sys.exit(1)

    # the url should contain the server_status exp: http://127.0.0.1/server-status?auto

url = sys.argv[1]

p = requests.get(url)

my_data = {}

for line in p.iter_lines():
    if line:
        line = str(line).strip()
        if 'Scoreboard' not in line:
            line = line.split(':')
            line[1] = line[1][1:-1]
            line[0] = line[0][2:-1]
            my_data[line[0]] = line[1]


for metric in my_data:
    print(metric + '=' + my_data[metric])
