#!/usr/bin/env python3
"""Fictional work sample. No network access or external dependencies.
Usage: python3 sample-cleanup.py input.csv new-output.csv
"""
import csv
import sys
from pathlib import Path

def clean(source, destination):
    source, destination = Path(source), Path(destination)
    if source.stat().st_size > 20_000_000:
        raise ValueError('Input exceeds 20 MB')
    rows = {}
    with source.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ['order_id', 'gross_cents', 'refund_cents']:
            raise ValueError('Unexpected columns')
        for number, raw in enumerate(reader, 1):
            if number > 100_000:
                raise ValueError('Input exceeds 100,000 rows')
            if None in raw or any(value is None for value in raw.values()):
                raise ValueError('Malformed row')
            order = raw['order_id'].strip()
            if not order or len(order) > 80 or order[0] in '=+-@' or any(ord(c)<32 for c in order):
                raise ValueError('Missing or unsafe order ID')
            amounts = [raw['gross_cents'].strip(), raw['refund_cents'].strip()]
            if not all(value.isascii() and value.isdigit() for value in amounts):
                raise ValueError('Amounts must be nonnegative integer cents')
            gross, refund = map(int, amounts)
            if refund > gross or gross > 10**12:
                raise ValueError('Amount outside supported range')
            values = (gross, refund)
            if order in rows and rows[order] != values:
                raise ValueError('Conflicting duplicate: ' + order)
            rows[order] = values
    if not rows:
        raise ValueError('Empty input')
    # Validate the whole input before creating the output. Never overwrite.
    with destination.open('x', encoding='utf-8', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(['order_id','gross_cents','refund_cents','net_after_refunds_cents'])
        for order, (gross, refund) in rows.items():
            writer.writerow([order, gross, refund, gross-refund])
    return {'orders':len(rows),'gross_cents':sum(v[0] for v in rows.values()),
            'refund_cents':sum(v[1] for v in rows.values()),
            'net_after_refunds_cents':sum(v[0]-v[1] for v in rows.values())}

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    try:
        print(clean(sys.argv[1], sys.argv[2]))
    except (OSError, ValueError, csv.Error) as exc:
        raise SystemExit(str(exc))
