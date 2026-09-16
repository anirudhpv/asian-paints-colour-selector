#!/usr/bin/env bash
# Self-driving pipeline: wait for main scrape, mop up failures, fix hex, build PDF.
set -uo pipefail
cd "$(dirname "$0")"

echo "[driver] waiting for main scrape to finish..."
while pgrep -f "python3 scrape.py" >/dev/null; do sleep 10; done
echo "[driver] main scrape exited at $(date)"

echo "[driver] mop-up pass (retry failed urls)..."
python3 scrape.py 2>&1 | tail -3
echo "[driver] fixing incomplete records..."
python3 fix_missing.py 2>&1 | tail -5

echo "[driver] building PDF..."
python3 make_pdf.py 2>&1

echo "[driver] verifying PDF..."
PDF=/home/apv/.openclaw/workspace/asian_paints_complete_shade_book.pdf
ls -lh "$PDF"
pdfinfo "$PDF" 2>/dev/null | grep -E "Pages|Page size" || echo "pdfinfo unavailable"
echo "[driver] DONE $(date)"
