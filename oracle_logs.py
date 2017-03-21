import sys, cx_Oracle

if len(sys.argv) < 6:
    print('Usage: Oracle_logs <Server IP> <port> <SID> <username> <password>')
    sys.exit()

server = sys.argv[1]
port = sys.argv[2]
sid = sys.argv[3]
username = sys.argv[4]
password = sys.argv[5]


dsn_tns = cx_Oracle.makedsn(server, port, sid)
con_ora = cx_Oracle.connect(username, password, dsn_tns, mode=cx_Oracle.SYSDBA)
cur = con_ora.cursor()
cur.execute('SELECT originating_timestamp, message_text, filename FROM \
v$diag_alert_ext WHERE upper(message_text) LIKE \'%ORA-%\' AND originati\
ng_timestamp > (sysdate-1/24) ORDER BY originating_timestamp')

row = cur.fetchall()

cur.close()
con_ora.close()

if len(row) == 0:
    print("No Errors in Log File")
    sys.exit(0)
else:
    print(row)
    sys.exit(2)
