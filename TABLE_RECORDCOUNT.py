#Import your dependencies
# import platform
import configparser
from datetime import datetime
from hdbcli import dbapi
import os.path
import pandas as pd

#verify the architecture of Python
# print ("Platform architecture: " + platform.architecture()[0])

# 建立 ConfigParser, 讀取 INI 設定檔
config = configparser.ConfigParser()
config.read('config.ini')
path = config['output']['File']

#Initialize your connection
conn = dbapi.connect(
    address=config['database']['Server'],
    port=config['database']['Port'],
    user=config['database']['User'],
    password=config['database']['Password'],
)
#If no errors, print connected
print('connected')

sqlStr = open(f'./TABLE_RECORDCOUNT.sql', 'r', encoding="utf-8-sig").read()
sqlCommand = sqlStr.splitlines()

#Get and format the current date
current = datetime.now()
date = current.strftime('%Y-%m-%d %H:%M:%S')
headers = ['RECORD_COUNT']

cursor = conn.cursor()

output = []
for i in range(len(sqlCommand)):
    cursor.execute(sqlCommand[i])
    rows = cursor.fetchall()
    output.append(rows[0])

cursor.close()

# 建立Pandas DataFrame
df = pd.DataFrame(output, columns = headers)
df.insert(0,'DATETIME',current)
df.insert(1,'COMMAND',sqlCommand)
sqlComment = df['COMMAND'].str.split('--',1,expand=True)
df['SQL'] = sqlComment[0]
df['COMMENT'] = sqlComment[1]

print (df)

# 寫入TABLE_RECORDCOUNT.csv
if os.path.exists(path):
    df.to_csv(path, mode='a', index=False, header=False)
else:
    df.to_csv(path, index=False)