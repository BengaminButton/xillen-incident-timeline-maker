import os
import sys
import json
import time
from datetime import datetime

def read_lines(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            v = line.strip('\n')
            yield v

def parse_kv(line):
    parts = [p.strip() for p in line.split('|')]
    data = {}
    for p in parts:
        if '=' in p:
            k, v = p.split('=', 1)
            data[k.strip()] = v.strip()
    return data

def detect_ts(v):
    fmts = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%SZ', '%d.%m.%Y %H:%M:%S']
    for f in fmts:
        try:
            return int(datetime.strptime(v, f).timestamp())
        except Exception:
            pass
    try:
        return int(float(v))
    except Exception:
        return None

def collect(directory):
    items = []
    for root, _, files in os.walk(directory):
        for fn in files:
            fp = os.path.join(root, fn)
            for line in read_lines(fp):
                if not line or line.startswith('#'):
                    continue
                kv = parse_kv(line)
                if not kv:
                    continue
                ts = detect_ts(kv.get('ts') or kv.get('time') or kv.get('date') or '')
                if ts is None:
                    ts = int(time.time())
                items.append({
                    'ts': ts,
                    'file': fp,
                    'host': kv.get('host',''),
                    'user': kv.get('user',''),
                    'type': kv.get('type','event'),
                    'msg': kv.get('msg',''),
                    'authors': 't.me/Bengamin_Button t.me/XillenAdapter'
                })
    items.sort(key=lambda x: (x['ts'], x['host'], x['type']))
    return items

def write_json(path, obj):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def main():
    if len(sys.argv) < 2:
        print('t.me/Bengamin_Button t.me/XillenAdapter')
        print('usage: main.py <artifacts_dir> [out.json]')
        sys.exit(1)
    src = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else 'timeline.json'
    items = collect(src)
    write_json(out, {'generated_at': int(time.time()), 'count': len(items), 'items': items})
    print(out)

if __name__ == '__main__':
    main()

print("t.me/Bengamin_Button t.me/XillenAdapter")
