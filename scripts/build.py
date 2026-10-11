"""Generate the SITS Lab website using only the Python standard library."""
import json
import hashlib
import re
import shutil
from html import escape
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
pub_file = ROOT / 'content/publications.json'
papers = json.loads(pub_file.read_text(encoding='utf-8'))


def e(value):
    return escape(str(value), quote=True)


def url(value):
    if urlparse(value).scheme != 'https' or not urlparse(value).netloc:
        raise ValueError('Expected an absolute HTTPS URL: ' + value)
    return e(value)


def link(href, label, cls='text-link'):
    return f'<a class="{cls}" href="{url(href)}">{e(label)} <span aria-hidden="true">↗</span></a>'


EN_UI = {'SITS Lab 首页': 'SITS Lab home',
 '空间智能与可信感知</small>': 'Hunan University</small>',
 'aria-label="主导航"': 'aria-label="Main navigation"',
 '>实验室</a>': '>About</a>',
 '>首页</a>': '>Home</a>',
 '>动态</a>': '>News</a>',
 '>研究方向</a>': '>Research</a>',
 '>代表研究</a>': '>Highlights</a>',
 '>团队</a>': '>Team</a>',
 '>学术成果</a>': '>Publications</a>',
 '>科研课题</a>': '>Grants</a>',
 '>联系</a>': '>Contact</a>',
 '个人学术主页': 'Academic homepage',
 '研究代码': 'Code',
 '项目仓库': 'Project repository',
 '查看详情': 'Learn more',
 '研究代码与系统资源将按项目独立维护。如需了解已有成果的代码或数据获取方式，欢迎联系论文作者。': 'Code and system resources are maintained per project. Please '
                                                   'contact the authors for information about available research '
                                                   'artifacts and datasets.',
 '项目编号：': 'Grant number: ',
 '实验室动态': 'Lab news',
 '导师原始论文列表': 'Faculty publication list',
 '返回首页 ↑': 'Back to home ↑',
 '空间智能与可信感知实验室<br>湖南大学 · Hunan University': 'Spatial Intelligence & Trusted Sensing<br>Hunan University',
 '论文详情': 'Publication',
 '论文与报告': 'Paper & presentation',
 '官方论文': 'Official paper',
 '2025 年接收/在线发表；按正式卷期 IEEE TMC 25(4) 归入 2026。': 'Accepted / published online in 2025; included in IEEE TMC 25(4), '
                                                '2026.',
 'CWSN 2025 会议论文；Springer 论文集于 2026-07-02 出版，按出版年归入 2026。': 'Presented at CWSN 2025; the Springer proceedings were '
                                                            'published on July 2, 2026.',
 '2026-05-19 在线发表；出版商标注 Just Accepted，尚未分配卷期页码。': 'Published online May 19, 2026; listed as Just Accepted, with no '
                                                  'volume, issue, or pages assigned.',
 'ACM TIOT 期刊论文；入选 MobiCom 2025 展示，不作为 MobiCom 主会论文。': 'An ACM TIOT journal article selected for presentation at '
                                                       'MobiCom 2025.',
 'Crossref 保留 2020 年 Early Access 元数据；按导师列出的正式卷期 29(1): 410–422 (2021) 归年。': 'Early Access in 2020; listed under the '
                                                                             'final issue, 29(1): 410–422 (2021).',
 'IMWUT 5(4) 于 2021 年发表，在 UbiComp 2022 展示；按期刊发表年归入 2021。': 'Published in IMWUT 5(4), 2021; presented at UbiComp 2022.',
 '作者按出版物署名保留 Hongbo Jinag；导师列表与出版元数据的作者名单不同，引用以出版记录为准。': 'The author spelling Hongbo Jinag is retained as it appears '
                                                         'in the publication.',
 '导师列表未列年份；按 Crossref 正式卷期 57(15) 补为 2012。': 'Published in Chinese Science Bulletin 57(15), 2012.'}

PAGES = ('index', 'research', 'team', 'publications', 'grants', 'contact')

for locale in ('en', 'zh'):
    content_name = 'site.en.json' if locale == 'en' else 'site.json'
    data = json.loads((ROOT / 'content' / content_name).read_text(encoding='utf-8'))
    for key in ('name', 'name_zh', 'full_name', 'university', 'headline', 'intro', 'email', 'people', 'research', 'projects', 'news', 'about', 'grants'):
        if key not in data:
            raise ValueError('Missing required field: ' + key)
    if not re.fullmatch(r'[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+', data['email']):
        raise ValueError('Invalid contact email')
    for p in papers:
        for field in ('year', 'title', 'authors', 'venue', 'url', 'link_label'):
            if not p.get(field):
                raise ValueError(f'Missing publication field {field}: {p}')
        if not re.fullmatch(r'\d{4}', str(p['year'])):
            raise ValueError('Publication year must have four digits')
        url(p['url'])
    papers = sorted(papers, key=lambda p: str(p['year']), reverse=True)
    years = sorted({str(p['year']) for p in papers}, reverse=True)


    def paper_html(p):
        code = link(p['code_url'], '研究代码') if p.get('code_url') else ''
        note = f'<p class="pub-note">{e(p["year_note"])}</p>' if p.get('year_note') else ''
        authors = e(p['authors']).replace('Daibo Liu', '<strong>Daibo Liu</strong>')
        return f'<article class="publication"><div class="pub-year">{e(p["year"])}</div><div><span class="venue">{e(p["venue"])}</span><h3 lang="en">{e(p["title"])}</h3><p class="authors" lang="en">{authors}</p>{note}<div class="pub-links">{link(p["url"], p["link_label"])}{code}</div></div></article>'


    research = ''.join(f'<article class="research-card"><span class="index">0{i+1}</span><h3>{e(r["title"])}</h3><p>{e(r["description"])}</p><div class="tags">{e(r["tags"])}</div></article>' for i, r in enumerate(data['research']))
    people = ''
    for p in data['people']:
        academic = link(p['academic_url'], '个人学术主页') if p.get('academic_url') else ''
        display_name, second_name = (p['name'], p['name_zh']) if locale == 'en' else (p['name_zh'], p['name'])
        portrait_alt = display_name + (' portrait' if locale == 'en' else '的照片')
        photo = p.get('photo', 'portrait-template.svg')
        if not re.fullmatch(r'[a-zA-Z0-9_.-]+', photo) or not (ROOT / 'static/images' / photo).is_file():
            raise ValueError('Missing or invalid faculty photo: ' + photo)
        people += f'<article class="person"><figure class="portrait"><img src="./images/{e(photo)}" width="360" height="480" alt="{e(portrait_alt)}"></figure><div class="person-name"><span class="eyebrow">{e(p["role"])}</span><h3>{e(display_name)} <span>{e(second_name)}</span></h3><p>{e(p["title"])}</p></div><div class="person-bio"><p>{e(p["bio"])}</p><div class="pub-links">{link(p["url"], p["url_label"])}{academic}</div></div></article>'
    students = ''
    team_members = json.loads((ROOT / 'content/team.json').read_text(encoding='utf-8'))
    for group, en_heading, zh_heading in (('phd', 'PhD students', '博士生'), ('masters', "Master’s students", '硕士生')):
        heading = en_heading if locale == 'en' else zh_heading
        cards = ''
        for member in (m for m in team_members if m['group'] == group):
            primary = member['name_en'] if locale == 'en' else member['name_zh']
            secondary = member['name_zh'] if locale == 'en' else member['name_en']
            year_label = 'Entry year' if locale == 'en' else '入学年份'
            photo = member['photo']
            alt = '' if photo == 'portrait-template.svg' else primary + (' portrait' if locale == 'en' else '的照片')
            if not re.fullmatch(r'[a-zA-Z0-9_.-]+', photo) or not (ROOT / 'static/images' / photo).is_file():
                raise ValueError('Missing or invalid team photo: ' + photo)
            cards += f'<article class="member"><figure><img src="./images/{e(photo)}" width="360" height="480" alt="{e(alt)}"></figure><h3>{e(primary)}</h3><p class="member-secondary">{e(secondary)}</p><p class="entry-year">{year_label} · {e(member["entry_year"])}</p></article>'
        students += f'<section class="section student-group"><div class="section-heading"><h2>{heading}</h2></div><div class="member-grid">{cards}</div></section>'
    alumni_members = json.loads((ROOT / 'content/alumni.json').read_text(encoding='utf-8'))
    alumni_heading = 'Alumni' if locale == 'en' else '已毕业成员'
    columns = ('Name', 'Degree', 'Graduation year', 'Destination after graduation') if locale == 'en' else ('姓名', '学位', '毕业年份', '毕业去向')
    alumni_rows = ''
    for member in sorted(alumni_members, key=lambda m: str(m.get('graduation_year', '')), reverse=True):
        if not member.get('name_zh') or member.get('group') not in ('phd', 'masters'):
            raise ValueError('Alumni must have a name and degree group')
        primary = member.get('name_en') or member['name_zh'] if locale == 'en' else member['name_zh']
        secondary = member['name_zh'] if locale == 'en' and member.get('name_en') else member.get('name_en', '') if locale == 'zh' else ''
        degree = ('PhD' if member['group'] == 'phd' else "Master’s") if locale == 'en' else ('博士' if member['group'] == 'phd' else '硕士')
        pending = 'To be updated' if locale == 'en' else '待补充'
        year = member.get('graduation_year') or pending
        destination = member.get('destination_en' if locale == 'en' else 'destination_zh') or member.get('destination_zh') or pending
        alumni_rows += f'<tr><th scope="row">{e(primary)}<span class="alumni-secondary">{e(secondary)}</span></th><td>{e(degree)}</td><td>{e(year)}</td><td>{e(destination)}</td></tr>'
    if not alumni_rows:
        pending = 'Alumni names and destinations will be added once confirmed.' if locale == 'en' else '毕业成员名单与去向待补充。'
        alumni_rows = f'<tr><td colspan="4" class="alumni-empty">{pending}</td></tr>'
    alumni = f'<section id="alumni" class="section"><div class="section-heading"><h2>{alumni_heading}</h2></div><table class="alumni-table"><thead><tr>{"".join(f"<th scope=column>{e(c)}</th>" for c in columns)}</tr></thead><tbody>{alumni_rows}</tbody></table></section>'
    featured = [p for p in papers if p.get('featured')][:6] or papers[:6]
    publications = ''.join(paper_html(p) for p in featured)
    recent_publications = '<ul class="recent-list">' + ''.join(f'<li><span class="venue">{e(p["year"])} · {e(p["venue"])}</span><a href="{url(p["url"])}">{e(p["title"])}</a></li>' for p in papers[:3]) + '</ul>'
    highlight_specs = [
        ('Eye of Sauron', 'emr-template.svg', 'Hidden-device detection', '隐蔽设备检测', 'Detecting and locating hidden cameras through memory electromagnetic radiation.', '利用内存电磁辐射检测与定位隐蔽摄像头。'),
        ('Decoding Air Friction', 'wearable-template.svg', 'Sensing with everyday wearables', '日常可穿戴设备感知', 'Exploring user identification with out-ear microphones in commercial earphones.', '利用商用耳机外置麦克风开展用户身份识别研究。'),
        ('Amulet:', 'mobile-template.svg', 'Mobile privacy & authentication', '移动隐私与身份认证', 'Integrating sensitive information access with identity authentication on mobile devices.', '将移动设备敏感信息访问与身份认证相结合。')]
    highlights = ''
    for prefix, image, title_en, title_zh, desc_en, desc_zh in highlight_specs:
        paper = next(p for p in papers if p['title'].startswith(prefix))
        title, desc = (title_en, desc_en) if locale == 'en' else (title_zh, desc_zh)
        caption = title + (' illustration' if locale == 'en' else '示意图')
        highlights += f'<article class="highlight"><figure><img src="./images/{image}" width="800" height="450" alt="{e(caption)}"></figure><span class="venue">{e(paper["venue"])} · {e(paper["year"])}</span><h3>{e(title)}</h3><p>{e(desc)}</p>{link(paper["url"], "Paper" if locale == "en" else "论文详情")}</article>'
    archive = ''
    count_label = 'papers' if locale == 'en' else '篇'
    for year in years:
        items = [p for p in papers if str(p['year']) == year]
        archive += f'<section class="year-section" id="year-{year}"><h2>{year}<span>{len(items)} {count_label}</span></h2>{"".join(paper_html(p) for p in items)}</section>'
    projects = ''.join(f'<article class="project"><h3>{e(p["title"])}</h3><p>{e(p["description"])}</p>{link(p["url"], "项目仓库")}</article>' for p in data['projects'])
    if not projects:
        projects = '<p class="empty-note">研究代码与系统资源将按项目独立维护。如需了解已有成果的代码或数据获取方式，欢迎联系论文作者。</p>'
    grants = ''.join(f'<article class="grant"><div class="grant-year">{e(g["period"])}</div><div><span class="venue">{e(g["type"])} · {e(g["role"])}</span><h3>{e(g["title"])}</h3><p>项目编号：{e(g["number"])}</p></div></article>' for g in data['grants'])
    service = ''.join(f'<article><h3>{e(s["title"])}</h3><p>{e(s["text"])}</p>{link(s["url"], "查看详情")}</article>' for s in data['academic_service'])
    news_items = json.loads((ROOT / 'content/news.json').read_text(encoding='utf-8'))
    news_items = sorted(news_items, key=lambda item: item['date'], reverse=True)
    def news_html(items):
        rows = ''
        for item in items:
            if not re.fullmatch(r'\d{4}-\d{2}', item['date']):
                raise ValueError('News date must use YYYY-MM')
            text = item['text_en'] if locale == 'en' else item['text_zh']
            source_label = 'Source' if locale == 'en' else '来源'
            rows += f'<li><time datetime="{e(item["date"])}">{e(item["date"])}</time><div><span class="news-tag">{e(item["tag"])}</span><p>{e(text)}</p>{link(item["source_url"], source_label)}</div></li>'
        return '<ul class="news-timeline">' + rows + '</ul>'
    news = news_html(news_items)
    header = f'''<header class="header"><div class="header-inner">
    <a class="brand" href="./index.html" aria-label="SITS Lab 首页"><img class="brand-logo" src="./images/sitslab.png" width="711" height="593" alt=""><span>{e(data['name'])}<small>空间智能与可信感知</small></span></a>
    <nav aria-label="主导航"><a href="./index.html">首页</a><a href="./research.html">研究方向</a><a href="./team.html">团队</a><a href="./publications.html">学术成果</a><a href="./grants.html">科研课题</a><a href="./contact.html">联系</a></nav></div></header>'''
    footer = f'''<footer class="container footer"><div><strong>{e(data['name'])}</strong><br>{e(data['full_name'])}</div><span>{e(data['name_zh'])}<br>湖南大学 · Hunan University</span><a href="./index.html">返回首页 ↑</a></footer>'''
    values = {k: e(v) for k, v in data.items() if isinstance(v, str)}
    values['full_name_marked'] = re.sub(r'\b(Spatial|Intelligence|Trusted|Sensing)\b', lambda m: '<strong class="acronym-initial">' + m[0][0] + '</strong>' + m[0][1:], e(data['full_name']))
    values.update(header=header, footer=footer, research=research, people=people, students=students, alumni=alumni, publications=publications,
                  publication_count=str(len(papers)), year_range=f'{years[-1]}–{years[0]}' if years else '',
                  publication_archive=archive, highlights=highlights, recent_publications=recent_publications, year_nav=''.join(f'<a href="#year-{year}">{year}</a>' for year in years),
                  about=''.join(f'<p>{e(p)}</p>' for p in data['about']), grants=grants, academic_service=service,
                  projects=projects, news=news, headline='<br>'.join(e(data['headline']).split('\n')),
                  profile_link=link(data['profile_url'], '导师原始论文列表'),
                  github_link=link(data['github_url'], 'GitHub') if data['github_url'] else '')
    out = ROOT / 'dist'
    out.mkdir(exist_ok=True)
    for page in PAGES:
        filename = page + ('.zh' if locale == 'zh' else '') + '.html'
        template = (ROOT / 'templates' / filename).read_text(encoding='utf-8')
        html = re.sub(r'\{\{(\w+)\}\}', lambda m: values[m[1]], template)
        if locale == 'en':
            for original, translated in sorted(EN_UI.items(), key=lambda item: len(item[0]), reverse=True):
                html = html.replace(original, translated)
        else:
            for target_page in PAGES:
                html = html.replace(f'./{target_page}.html', f'./{target_page}.zh.html')
        current_href = './' + filename
        html = html.replace(f'<a href="{current_href}">', f'<a href="{current_href}" aria-current="page">', 1)
        english_page = f'./{page}.html'
        chinese_page = f'./{page}.zh.html'
        toggle = f'<nav class="language-switch" aria-label="Language"><a href="{english_page}" lang="en" hreflang="en"' + (' aria-current="page"' if locale == 'en' else '') + '>EN</a><a href="' + chinese_page + '" lang="zh-CN" hreflang="zh-CN"' + (' aria-current="page"' if locale == 'zh' else '') + '>中文</a></nav>'
        html = html.replace('</nav></div></header>', '</nav>' + toggle + '</div></header>')
        def version_image(match):
            asset_name = match[1]
            asset_path = ROOT / 'static/images' / asset_name
            digest = hashlib.sha256(asset_path.read_bytes()).hexdigest()[:10]
            return f'src="./images/{asset_name}?v={digest}"'
        html = re.sub(r'src="\./images/([^"?]+)"', version_image, html)
        style_version = hashlib.sha256((ROOT / 'static/styles.css').read_bytes()).hexdigest()[:10]
        html = html.replace('./styles.css"', f'./styles.css?v={style_version}"')
        html = html.replace('</head>', f'<link rel="alternate" hreflang="en" href="{english_page}"><link rel="alternate" hreflang="zh-CN" href="{chinese_page}"></head>')
        (out / filename).write_text(html, encoding='utf-8')
    legacy_filename = 'people' + ('.zh' if locale == 'zh' else '') + '.html'
    team_filename = 'team' + ('.zh' if locale == 'zh' else '') + '.html'
    legacy_lang = 'en' if locale == 'en' else 'zh-CN'
    (out / legacy_filename).write_text(f'<!doctype html><html lang="{legacy_lang}"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=./{team_filename}"><title>Team · SITS Lab</title></head><body><a href="./{team_filename}">Team / 研究团队</a></body></html>', encoding='utf-8')
    legacy_news = 'news' + ('.zh' if locale == 'zh' else '') + '.html'
    home_news = 'index' + ('.zh' if locale == 'zh' else '') + '.html#news'
    (out / legacy_news).write_text(f'<!doctype html><html lang="{legacy_lang}"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=./{home_news}"><title>News · SITS Lab</title></head><body><a href="./{home_news}">News / 实验室动态</a></body></html>', encoding='utf-8')
    for asset in ('styles.css', 'favicon.svg'):
        shutil.copyfile(ROOT / 'static' / asset, out / asset)
    shutil.copytree(ROOT / 'static/images', out / 'images', dirs_exist_ok=True)
    (out / '.nojekyll').touch()
    print(f'Built {len(PAGES)} {locale} pages: {len(papers)} publications ({len(featured)} featured), {len(data["research"])} research areas, {len(data["grants"])} grants')
