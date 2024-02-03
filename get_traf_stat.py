#!/usr/bin/env python3

import subprocess
import glob
import csv
import sys
import os
from time import time

t1 = time()
files = sys.argv[1:]
if not files:
    print('empty argument list')
    sys.exit()
files.sort()
rows = []
#fields = [
#    'File (date format)',
#    'Host', 'In (bytes)',
#    'Out (bytes)',
#    'Total (bytes)',
#    'Total (human readable)'
#]
fields = [
    'File (date format)',
    'Sent (bytes)',
    'Received (bytes)',
    'Total (bytes)',
    'Total (human readable)'
]
for file in files:
    result = subprocess.run(["grep", "-E", "^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", file], capture_output=True, text=True)
    if result.returncode == 0:
        result_ls = result.stdout.split("\n")
        for st in result_ls:
            if st != '':
                st_list = st.split()
                hr = subprocess.run(['numfmt', '--to=iec-i', '--suffix=B', '--format=%9.2f', st_list[3]], capture_output=True, text=True).stdout.strip()
                st_list.append(hr)
                st_list.insert(0, os.path.basename(file))
                del st_list[1]
                rows.append(st_list)

with open('/home/ubuntu/webdav_dir/trafstat.csv', 'wt', encoding='UTF-8') as f:
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(rows)

t2 = time() - t1
print(f'time: {t2:.2f}')
