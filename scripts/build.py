"""Build the static portfolio and PDF from the original Markdown documents."""
from pathlib import Path
import re, shutil, argparse, os
from datetime import date
from urllib.parse import unquote
from urllib.parse import urlparse
import yaml
from markdown_it import MarkdownIt
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup, escape
from weasyprint import HTML

ROOT = Path(__file__).resolve().parents[1]
MD = MarkdownIt('commonmark', {'html': False}).enable('table')
ENV = Environment(loader=FileSystemLoader(ROOT/'src/templates'), autoescape=select_autoescape(['html']))
TYPES = {'individual':'개인 프로젝트','team':'팀 프로젝트','collaborative':'공동 연구'}
STATES = {'planned':'기획 단계','in-progress':'개발 중','prototype':'프로토타입','completed':'완료','released':'공개','archived':'기록 보존','unknown':''}

# Semantic emphasis, independent of theme and Markdown presentation.
CORE_SECTIONS = frozenset((
    '문제 정의', '역할 및 기여', '설계 및 구현',
    '플레이 및 실행 구조 설계', '결과 및 검증', '인사이트 및 한계',
))

def highlight_terms(value, terms):
    """Escape the entire source; wrap only explicitly designated terms."""
    if not terms:
        return escape(value)
    pattern = re.compile('(' + '|'.join(re.escape(t) for t in sorted(terms, key=len, reverse=True)) + ')')
    return Markup('').join(
        Markup('<span class="headline-accent">{}</span>').format(part) if i % 2 else escape(part)
        for i, part in enumerate(pattern.split(value))
    )

ENV.filters['highlight_terms'] = highlight_terms

def require(condition, message):
    if not condition: raise ValueError(message)

def nonempty(value):
    return isinstance(value, str) and bool(value.strip()) and value.strip() not in ('TODO', 'TBD', '[미작성]')

def strings(value, *, allow_empty=False):
    return isinstance(value, list) and (allow_empty or bool(value)) and all(nonempty(v) for v in value)

def valid_date(value, partial=False):
    if not isinstance(value, str): return False
    if partial and re.fullmatch(r'\d{4}(?:-\d{2})?', value):
        try: date.fromisoformat(value + ('-01-01' if len(value)==4 else '-01')); return True
        except ValueError: return False
    try: return bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}',value)) and bool(date.fromisoformat(value))
    except ValueError: return False

def render_md(body):
    # Section headings get stable IDs for the in-page navigation; source text is not changed.
    tokens = MD.parse(body)
    toc = []
    previous=1
    for i,t in enumerate(tokens):
        if t.type=='heading_open':
            level=int(t.tag[1:]); title=tokens[i+1].content.strip()
            require(2<=level<=previous+1, f'Invalid heading hierarchy: {title}')
            require(nonempty(title) and not (title.startswith('[') and title.endswith(']')), f'Empty/placeholder heading: {title}')
            previous=level
        if t.type=='heading_open' and t.tag=='h2':
            ident = f'section-{len(toc)+1}'
            t.attrSet('id',ident)
            if title in CORE_SECTIONS:
                t.attrJoin('class','section-accent')
            toc.append({'id':ident,'title':tokens[i+1].content})
    return Markup(MD.renderer.render(tokens,MD.options,{})), toc

def read(path):
    text = path.read_text(encoding='utf-8')
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n?(.*)$',text,re.S)
    require(m, f'{path}: missing front matter')
    data = yaml.safe_load(m[1]); require(isinstance(data,dict), f'{path}: invalid metadata')
    body,toc=render_md(m[2]); data.update(body=body,toc=toc)
    require(valid_date(data.get('updated_at')), f'{path}: invalid updated_at')
    require(not re.search(r'^\s*(?:TODO|TBD|\[미작성\])\s*$',m[2],re.M), f'{path}: unfinished placeholder')
    return data

def valid_url(url):
    return isinstance(url,str) and urlparse(url).scheme in ('https','http') and bool(urlparse(url).netloc)

def asset_path(src,prefix):
    if valid_url(src): return src
    return prefix+src.lstrip('/')
ENV.globals.update(asset_path=asset_path,types=TYPES,states=STATES)

def load():
    profile=read(ROOT/'content/profile.md'); resume=read(ROOT/'content/resume.md')
    for k in ('nickname','interests','headline','summary','updated_at'):
        require(profile.get(k),f'profile: missing {k}')
    require(all(nonempty(profile.get(k)) for k in ('nickname','headline','summary')), 'profile: invalid text')
    require(strings(profile['interests']) and strings(profile.get('focus_technologies',[]),allow_empty=True),'profile: invalid lists')
    emphasis=profile.get('headline_emphasis',[])
    require(strings(emphasis,allow_empty=True),'profile: invalid headline_emphasis')
    require(len(emphasis)==len(set(emphasis)) and all(t in profile['headline'] for t in emphasis),'profile: duplicate or missing headline emphasis term')
    require(not any(a != b and a in b for a in emphasis for b in emphasis),'profile: overlapping headline emphasis terms')
    require(isinstance(profile.get('links'),dict) and valid_url(profile['links'].get('github')),'profile: invalid github')
    for k in ('portfolio','linkedin'):
        require(k not in profile['links'] or valid_url(profile['links'][k]), f'profile: invalid {k} URL')
    require(nonempty(resume.get('title')) and strings(resume.get('projects')), 'resume: invalid title or projects')
    projects=[]; ids=set(); orders=set()
    for f in sorted((ROOT/'content/projects').glob('*.md')):
        p=read(f)
        for k in ('id','title','category','project_type','status','role','summary','updated_at'):
            require(p.get(k),f'{f}: missing {k}')
        require(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',p['id']) and p['id'] not in ids,f'{f}: invalid or duplicate id')
        require(nonempty(p['title']) and strings(p['category']) and strings(p['role']), f'{f}: invalid title/category/role')
        require(type(p.get('featured')) is bool, f'{f}: featured must be boolean')
        order=p.get('order')
        if order is not None:
            require(type(order) is int and order>0 and order not in orders, f'{f}: invalid/duplicate order'); orders.add(order)
        if p.get('period') is not None:
            require(isinstance(p['period'],dict),f'{f}: invalid period')
            for k in ('start','end'):
                require(p['period'].get(k) is None or valid_date(p['period'][k],partial=True),f'{f}: invalid period.{k}')
            start,end=p['period'].get('start'),p['period'].get('end')
            require(not(start and end) or start<=end or start.startswith(end),f'{f}: period reversed')
        require(isinstance(p['summary'],dict),f'{f}: summary must be a mapping')
        ids.add(p['id']); require(p['project_type'] in TYPES and p['status'] in STATES,f'{f}: invalid classification')
        for k in ('overview','problem','contribution','result'):
            require(nonempty(p['summary'].get(k)),f'{f}: missing/invalid summary.{k}')
        require('display_label' not in p or isinstance(p['display_label'], str),f'{f}: invalid display_label')
        require(strings(p.get('technologies'),allow_empty=True),f'{f}: invalid technologies')
        require(strings(p.get('implementation_techniques',[]),allow_empty=True),f'{f}: invalid techniques')
        headings=[h['title'] for h in p['toc']]
        for alternatives in [('문제 정의',),('역할 및 기여',),('설계 및 구현','플레이 및 실행 구조 설계'),('결과 및 검증',)]:
            require(any(h in headings for h in alternatives),f'{f}: missing section {alternatives}')
        # Every required H2 section must have actual text, not just an empty heading.
        from html.parser import HTMLParser
        section_text=re.split(r'<h2[^>]*>.*?</h2>',str(p['body']),flags=re.S)[1:]
        require(all(re.sub(r'<[^>]+>','',x).strip() for x in section_text),f'{f}: empty section')
        pub=p.get('publication')
        if pub is not None:
            require(isinstance(pub,dict), f'{f}: invalid publication')
            require(all(nonempty(pub.get(k)) for k in ('title','journal','pages','author_role','doi')), f'{f}: missing publication text')
            require(all(type(pub.get(k)) is int and pub[k]>0 for k in ('year','month','volume','issue')) and pub['month']<=12,f'{f}: invalid publication numbers')
            require(re.fullmatch(r'10\.\d{4,9}/\S+',pub['doi']), f'{f}: invalid DOI')
        media={}
        for item in p.get('media',[]):
            require(isinstance(item,dict) and nonempty(item.get('id')) and item['id'] not in media and nonempty(item.get('alt')) and nonempty(item.get('src')),f'{f}: invalid media')
            src=item['src']; local=(ROOT/src).resolve()
            require(valid_url(src) or (local.is_relative_to(ROOT/'assets') and local.is_file()),f'{f}: missing/unsafe asset {src}')
            media[item['id']]=item
        require(not p.get('cover') or p['cover'] in media,f'{f}: invalid cover')
        p['cover_media']=media.get(p.get('cover'))
        for link in p.get('links',[]): require(valid_url(link['url']) and link.get('label'),f'{f}: invalid link')
        projects.append(p)
    projects.sort(key=lambda p:(p.get('order') or float('inf'),p['id']))
    require(projects and any(p.get('featured') for p in projects),'No featured projects')
    require(len(set(resume['projects']))==len(resume['projects']) and all(x in ids for x in resume['projects']),'Resume references duplicate/unknown project')
    if resume.get('experiences'):
        raise ValueError('Optional experiences are not implemented in this version.')
    return profile,projects,resume

def write(path,template,**ctx):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(ENV.get_template(template).render(**ctx),encoding='utf-8')

def build(out):
    profile,projects,resume=load()
    require(out.resolve().is_relative_to(ROOT) and out.resolve()!=ROOT and out.name=='site','Output must be a site directory inside repository')
    if out.exists(): shutil.rmtree(out)
    out.mkdir(); shutil.copytree(ROOT/'assets',out/'assets'); shutil.copytree(ROOT/'src/static',out/'static')
    (out/'.nojekyll').touch()
    featured=[p for p in projects if p.get('featured')]
    common={'profile':profile,'projects':projects,'featured':featured}
    write(out/'index.html','index.html',prefix='./',page_title=f"{profile['nickname']} | 포트폴리오",description=profile['headline'],**common)
    for p in projects:
        write(out/'projects'/p['id']/'index.html','project.html',prefix='../../',page_title=f"{p['title']} | {profile['nickname']}",description=p['summary']['overview'],p=p,**common)
    # The project order is shared by all outputs; resume.projects selects membership only.
    chosen=[p for p in projects if p['id'] in resume['projects']]
    portfolio_url=os.environ.get('PORTFOLIO_URL') or profile['links'].get('portfolio')
    require(not portfolio_url or valid_url(portfolio_url),'Invalid PORTFOLIO_URL')
    resume_html=ENV.get_template('resume.html').render(profile=profile,resume=resume,chosen=chosen,portfolio_url=portfolio_url)
    HTML(string=resume_html,base_url=str(ROOT)).write_pdf(out/'resume.pdf')
    # Check every relative HTML link, stylesheet, script and asset; external links are not verified here.
    from html.parser import HTMLParser
    class LinkChecker(HTMLParser):
        def __init__(self,path): super().__init__(); self.path=path; self.ids=set(); self.links=[]
        def handle_starttag(self,tag,attrs):
            for k,v in attrs:
                if k=='id':
                    require(v not in self.ids,f'{self.path}: duplicate ID {v}'); self.ids.add(v)
                if k in ('href','src') and v: self.links.append(v)
    pages={}
    for f in out.rglob('*.html'):
        checker=LinkChecker(f); checker.feed(f.read_text(encoding='utf-8')); pages[f.resolve()]=checker
    for path,checker in pages.items():
        for v in checker.links:
            url=urlparse(v)
            if url.scheme or url.netloc: continue
            target=(path.parent/unquote(url.path)).resolve() if url.path else path
            if target.is_dir(): target=target/'index.html'
            require(target.is_relative_to(out) and target.is_file(),f'{path}: broken/unsafe local link {v}')
            if url.fragment and target in pages:
                require(unquote(url.fragment) in pages[target].ids,f'{path}: missing anchor {v}')
    print(f'Built {len(projects)+1} HTML pages, resume PDF; local links passed.')
    for p in projects:
        if not p.get('technologies'): print(f"NOTE: {p['title']} technologies not confirmed; techniques displayed separately.")

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--out',type=Path,default=ROOT/'site'); args=parser.parse_args(); build(args.out.resolve())
