"""Verify all generated HTML pages, anchors, resources and publication data."""
import json
import re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
class Check(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.refs = [], []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for k in ('href', 'src'):
            if k in attrs:
                self.refs.append(attrs[k])
parsed = {}
for page in OUT.glob('*.html'):
    text = page.read_text(encoding='utf-8')
    assert '{{' not in text, f'{page.name}: unresolved template field'
    c = Check(); c.feed(text)
    assert len(c.ids) == len(set(c.ids)), f'{page.name}: duplicate IDs'
    parsed[page.name] = c
for name, c in parsed.items():
    for ref in c.refs:
        assert ref, f'{name}: empty link'
        u = urlparse(ref)
        if u.scheme:
            assert u.scheme in ('https', 'mailto'), f'{name}: unsupported scheme: {ref}'
            continue
        target = (OUT / unquote(u.path)).resolve() if u.path else OUT / name
        assert target.is_file(), f'{name}: missing local target: {ref}'
        if u.fragment:
            assert target.name in parsed and unquote(u.fragment) in parsed[target.name].ids, f'{name}: broken anchor: {ref}'
assert (OUT / '.nojekyll').exists()
source = ROOT / 'content/publications.json'
if source.exists():
    papers = json.loads(source.read_text(encoding='utf-8'))
    keys = [(re.sub(r'\W+', '', p['title'].lower()),p['venue'].lower(),str(p['year'])) for p in papers]
    assert not [k for k,n in Counter(keys).items() if n>1], 'Duplicate publication record'
    html = (OUT/'publications.html').read_text(encoding='utf-8')
    assert html.count('class="publication"') == len(papers), 'Catalogue count mismatch'
print(f'PASS: {len(parsed)} pages, {sum(len(c.refs) for c in parsed.values())} links/resources; unique IDs and local targets valid')
