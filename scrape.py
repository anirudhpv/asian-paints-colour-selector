#!/usr/bin/env python3
"""Scrape Asian Paints shade pages: name, code, family, hex. Checkpointed JSONL."""
import re
import json
import time
import random
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ROOT = Path(__file__).resolve().parent
URLS_FILE = ROOT / 'data' / 'shade_urls.txt'
OUT = ROOT / 'data' / 'shades.jsonl'
FAIL = ROOT / 'data' / 'failures.jsonl'
CONCURRENCY = 25
RETRIES = 4
TIMEOUT = 25

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
}

TITLE_RE = re.compile(r'<title>([^<]+)</title>')
TITLE_PARSE_RE = re.compile(r'^(.*?)\s*\(([^()]+)\)\s*(?:House Wall Painting Colour|Wall Colour)?', re.S)
FAMILY_RE = re.compile(r'/colour-catalogue/([a-z-]+)-wall-colours/[a-z0-9-]+\.html$')
# skucode-adjacent inline background-color, both attribute orders
PAIR_A = re.compile(r'data-skucode="([^"]+)"[^>]*?style="background-color:\s*(#[0-9a-fA-F]{6})"', re.I)
PAIR_B = re.compile(r'style="background-color:\s*(#[0-9a-fA-F]{6})"[^>]*?data-skucode="([^"]+)"', re.I)
ENTITY_CODE_RE = re.compile(r'data-attr-entitycode="([^"]+)"')
LD_NAME_RE = re.compile(r'"@type":\s*"Product",\s*"name":\s*"([^"]+)"')
HEX_OK = re.compile(r'^#[0-9a-fA-F]{6}$')

local = threading.local()


def get_session():
    if not hasattr(local, 's'):
        s = requests.Session()
        s.headers.update(HEADERS)
        local.s = s
    return local.s


def parse_page(url, html):
    fam_m = FAMILY_RE.search(url)
    family = fam_m.group(1) if fam_m else 'unknown'

    name = code = None
    t = TITLE_RE.search(html)
    if t:
        raw = t.group(1).split('|')[0].strip()
        m = TITLE_PARSE_RE.match(raw)
        if m:
            name, code = m.group(1).strip(), m.group(2).strip()
    if not code:
        m = ENTITY_CODE_RE.search(html)
        if m:
            code = m.group(1)
    if not name:
        m = LD_NAME_RE.search(html)
        if m:
            name = m.group(1).strip().title()

    pairs = {}
    for c, h in PAIR_A.findall(html):
        pairs[c] = h
    for h, c in PAIR_B.findall(html):
        pairs.setdefault(c, h)
    hexv = pairs.get(code) if code else None
    if hexv and not HEX_OK.match(hexv):
        hexv = None

    ok = bool(name and code and hexv and family != 'unknown')
    return {'family': family, 'name': name, 'code': code, 'hex': hexv,
            'url': url, 'complete': ok}


def fetch(url):
    last_err = None
    for attempt in range(RETRIES):
        try:
            r = get_session().get(url, timeout=TIMEOUT, verify=False)
            if r.status_code == 200 and len(r.text) > 20000:
                return r.text
            last_err = f'http {r.status_code} len {len(r.text)}'
        except Exception as e:
            last_err = type(e).__name__
        time.sleep((2 ** attempt) + random.uniform(0, 1.5))
    raise RuntimeError(last_err)


def main():
    urls = [u for u in URLS_FILE.read_text().splitlines() if u.strip()]
    done = set()
    if OUT.exists():
        for line in OUT.read_text().splitlines():
            try:
                rec = json.loads(line)
                if rec.get('url'):
                    done.add(rec['url'])
            except json.JSONDecodeError:
                pass
    todo = [u for u in urls if u not in done]
    print(f'total={len(urls)} done={len(done)} todo={len(todo)} conc={CONCURRENCY}', flush=True)
    if not todo:
        print('ALL DONE', flush=True)
        return

    lock = threading.Lock()
    n_ok = n_partial = n_fail = 0
    t0 = time.time()
    out_f = OUT.open('a', encoding='utf-8')
    fail_f = FAIL.open('a', encoding='utf-8')

    with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
        futs = {ex.submit(fetch, u): u for u in todo}
        for fut in as_completed(futs):
            url = futs[fut]
            try:
                html = fut.result()
                rec = parse_page(url, html)
                with lock:
                    out_f.write(json.dumps(rec, ensure_ascii=False) + '\n')
                    out_f.flush()
                    if rec['complete']:
                        n_ok += 1
                    else:
                        n_partial += 1
                        print(f'PARTIAL {url}: name={rec["name"]} code={rec["code"]} hex={rec["hex"]}', flush=True)
            except Exception as e:
                with lock:
                    n_fail += 1
                    fail_f.write(json.dumps({'url': url, 'error': str(e)}) + '\n')
                    fail_f.flush()
            done_n = n_ok + n_partial + n_fail
            if done_n % 100 == 0:
                el = time.time() - t0
                print(f'progress {done_n}/{len(todo)} ok={n_ok} partial={n_partial} fail={n_fail} '
                      f'elapsed={el:.0f}s rate={done_n/el:.1f}/s eta={(len(todo)-done_n)/max(done_n/el,0.01):.0f}s', flush=True)

    out_f.close()
    fail_f.close()
    el = time.time() - t0
    print(f'FINISHED run={len(todo)} ok={n_ok} partial={n_partial} fail={n_fail} elapsed={el:.0f}s', flush=True)


if __name__ == '__main__':
    main()
