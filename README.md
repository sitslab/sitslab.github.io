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
- `content/team.json`: students, entry years and photo filenames.
- `content/alumni.json`: graduates and destinations.
- `content/publications.json`: shared publication catalogue with sources.
- `content/news.json`: bilingual news shown in the scrollable Home module.
- `content/analytics.json`: shared visitor counter URLs and counting start date.
- `static/images/`: photos and illustrations.
- `static/styles.css` and `templates/`: presentation.
- `static/carousel.js`: homepage photo carousel controls and autoplay.

Faculty photo filenames are stored in each `people` entry in both site JSON files. The homepage carousel displays `static/images/lab-group.webp` and `static/images/lab-group-2.webp` one at a time in a full-width 4:3 frame. It advances every five seconds, pauses on hover or focus, and offers previous/next, photo selection and pause/play buttons. Reduced-motion preference disables autoplay. Clicking a photo opens the complete original frame; without JavaScript both photos remain available. The header and page icon use `static/images/sitslab.png`. Faculty and student photos fill consistent 3:4 portrait frames without distortion; excess edges are cropped around the center. Web photos are optimized copies; original source photos are preserved. Research highlight figures use `usenix2024.png` (Eye of Sauron), `tmc2026.png` (Decoding Air Friction), and `imwut2025.png` (Amulet) at their original resolution. The full figures remain visible and can be opened by clicking them.

Update both languages. Use verified information; do not invent alumni, destinations, news or publication data. Faculty publications may predate the laboratory.

## Visitor statistics

Every content page in both languages includes the same free [Flag Counter](https://info.flagcounter.com/2xze) in its footer, displaying pageviews and visitor counts by country / region. Counting began on 2026-10-11; it cannot reconstruct earlier traffic. Keep the existing counter ID when updating its appearance so the collected statistics remain available. The provider may remove a free counter after 30 days without visitors.

The counter is a single HTTPS image, loaded eagerly even when the footer is below the viewport. No third-party JavaScript is included. Each image load adds a pageview; country / region visitor counts use Flag Counter's default daily repeat-visitor filter. These counts are visits, not an all-time number of distinct people, and include development checks. The public counter image may lag the detailed statistics page by about five minutes. Free counters show country / region totals, with subnational breakdowns limited to the United States and Canada.

Geolocation is estimated from the visitor's network address, so VPNs and proxies affect it. The browser sends its network address to Flag Counter to load the image, while the image's `no-referrer` policy withholds the referring page URL. See the provider's [privacy policy](https://www.flagcounter.com/privacy.html) and [counting FAQ](https://www.flagcounter.com/faq.html). Network blocks or filtering of this external image can prevent a visit from being recorded; the footer also links directly to the statistics page.

## GitHub Pages deployment

The laboratory organization owns this repository. In Settings → Pages select GitHub Actions. The workflow validates pull requests and builds/deploys pushes to `main`.

For routine updates, create a branch and open a pull request. The current maintenance policy requires a passing build and zero mandatory approvals, so the maintainer can merge their own pull request. Review by another maintainer remains optional. Keep organization ownership with the designated long-term administrators; grant students repository Maintain access when needed.

The website's source and content license has not yet been selected by the laboratory.
