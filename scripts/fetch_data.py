import csv
import json
import io
import urllib.request
import os
import sys
from datetime import datetime

sheet_id = os.environ['SHEET_ID']
sheet_name = 'Main Database'
url = (
    f'https://docs.google.com/spreadsheets/d/{sheet_id}'
    f'/gviz/tq?tqx=out:csv&sheet={sheet_name.replace(" ", "+")}'
)

print(f'Fetching: {url}')

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read().decode('utf-8')
except Exception as e:
    print(f'ERROR fetching sheet: {e}')
    sys.exit(1)

reader = csv.reader(io.StringIO(raw))
rows = list(reader)

if len(rows) < 2:
    print('ERROR: No data rows found')
    sys.exit(1)

headers = rows[0]
data_rows = [row for row in rows[1:] if row and row[0].strip()]

output = {
    'headers': headers,
    'rows': data_rows,
    'fetched_at': datetime.utcnow().isoformat() + 'Z',
    'row_count': len(data_rows)
}

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False)

print(f'Success: {len(data_rows)} rows written to data.json')
