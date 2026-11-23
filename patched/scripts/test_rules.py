"""Apply each `field` xpath in a scraper YAML to HTML files (naive YAML read, lxml = libxml2)."""
import sys, re
from lxml import html
sys.stdout.reconfigure(encoding='utf-8')
yml, pages = sys.argv[1], sys.argv[2:]
rules, field = [], None
for line in open(yml, encoding='utf-8'):
    m = re.match(r'\s*- field: (\w+)', line)
    if m: field = m.group(1)
    m = re.match(r'\s*(?:- )?(?:xpath|detail_xpath):\s*(\S.*)$', line) or (field and re.match(r'\s{8}- (//.*|\(//.*)$', line))
    if m: rules.append((field if 'detail_xpath' not in line else 'SEARCH', m.group(1).strip()))
for p in pages:
    d = html.parse(p)
    print('=====', p)
    for f, xp in rules:
        r = d.xpath(xp)
        print(f'{f:16} {len(r):3}  {[str(x).strip()[:60] for x in r[:4]]}')
