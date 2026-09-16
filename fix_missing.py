#!/usr/bin/env python3
"""Fix incomplete shade records: fill missing hex by sampling the CDN swatch image."""
import io
import json
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

import requests
import urllib3
from PIL import Image

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ROOT = Path(__file__).resolve().parent
SRC = ROOT / 'data' / 'shades.jsonl'
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}


def sample_swatch(code):
    url = f'https://static.asianpaints.com/content/dam/asian_paints/colours/swatches/{code}.png'
    r = requests.get(url, headers=UA, timeout=25, verify=False)
    r.raise_for_status()
    im = Image.open(io.BytesIO(r.content)).convert('RGB')
    w, h = im.size
    # median of center region to dodge any edge artifacts
    px = [im.getpixel((x, y)) for x in (w // 4, w // 2, 3 * w // 4)
          for y in (h // 4, h // 2, 3 * h // 4)]
    px.sort()
    r_, g_, b_ = px[len(px) // 2]
    return '#%02X%02X%02X' % (r_, g_, b_)


def main():
    recs = [json.loads(l) for l in SRC.read_text(encoding='utf-8').splitlines() if l.strip()]
    broken = [r for r in recs if not (r.get('complete') and r.get('hex'))]
    print(f'total={len(recs)} incomplete={len(broken)}')
    fixed = 0
    for r in broken:
        if r.get('code') and not r.get('hex'):
            try:
                r['hex'] = sample_swatch(r['code'])
                r['complete'] = True
                fixed += 1
                print('fixed hex', r['code'], r['hex'])
            except Exception as e:
                print('FAILED', r.get('url'), e)
    SRC.write_text('\n'.join(json.dumps(r, ensure_ascii=False) for r in recs) + '\n', encoding='utf-8')
    print(f'fixed={fixed} still_broken={len(broken) - fixed}')


if __name__ == '__main__':
    main()
