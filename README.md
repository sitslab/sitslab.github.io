# SITS Lab — Hunan University

Spatial Intelligence & Trusted Sensing Lab / 空间智能与可信感知实验室。

English-first bilingual laboratory website. Chinese is available from the language switch. Homepage target: https://sitslab.github.io/ .

## Local preview

Requires Python 3.9+ with no third-party dependencies.

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 4173 --directory dist --bind 127.0.0.1
```

Open http://127.0.0.1:4173/ . Generated files in `dist/` are not edited or committed.

## Content maintenance

- `content/site.en.json` and `content/site.json`: lab introduction, research, faculty, grants and contact.
- `content/team.json`: students and entry years.
- `content/alumni.json`: graduates and destinations.
- `content/publications.json`: shared publication catalogue with sources.
- `content/news.json`: bilingual news shown in the scrollable Home module.
- `static/images/`: photos and illustrations.
- `static/styles.css` and `templates/`: presentation.

Update both languages. Use verified information; do not invent alumni, destinations, news or publication data. Faculty publications may predate the laboratory.

## GitHub Pages deployment

The laboratory organization owns this repository. In Settings → Pages select GitHub Actions. The workflow validates pull requests and builds/deploys pushes to `main`.

For routine updates, create a branch and open a pull request. A website maintainer reviews it before merging. Keep organization ownership with the designated long-term administrators; grant students repository Maintain access when needed.

The website's source and content license has not yet been selected by the laboratory.
