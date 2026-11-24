import sys, re, difflib, pathlib, jupytext

LOCAL = pathlib.Path('/Users/phil/repos/climlab_dirs/climate_students_eoas/content/courseware')
UP = pathlib.Path('/Users/phil/repos/ClimateLaboratoryBook/courseware')
OUT = pathlib.Path(sys.argv[1])
OUT.mkdir(exist_ok=True)

def norm(text):
    text = text.replace('http://www.atmos.albany.edu/facstaff/brose/index.html',
                        'https://www.atmos.albany.edu/facstaff/brose/')
    text = text.replace('github.com/brian-rose/climlab', 'github.com/climlab/climlab')
    text = re.sub(r'https://brian-rose\.github\.io/ClimateLaboratoryBook/courseware/([\w-]+)\.html', r'\1', text)
    lines = []
    for l in text.splitlines():
        l = l.rstrip()
        if not l or re.fullmatch(r'_+', l) or re.fullmatch(r'\(nb:[\w-]+\)=', l):
            continue
        lines.append(l)
    return lines

def flat(path):
    nb = jupytext.read(path)
    out = []
    for c in nb.cells:
        src = norm(c.source)
        if not src:
            continue
        out.append('#### [%s]' % c.cell_type)
        out += src
    return out

rows = []
for f in sorted(LOCAL.rglob('*.md')):
    if 'checkpoint' in str(f) or f.name.startswith('.#'):
        continue
    n = re.sub(r'^lab\d+(_\d+)?_', '', f.stem)
    n = re.sub(r'^assignment\d+-', 'assignment-', n)
    u = UP / (n + '.md')
    rel = f.relative_to(LOCAL)
    if not u.exists():
        rows.append((str(rel), '-', 'no upstream'))
        continue
    a, b = flat(f), flat(u)
    d = list(difflib.unified_diff(a, b, str(rel), u.name, n=1, lineterm=''))
    add = sum(1 for l in d if l.startswith('+') and not l.startswith('+++'))
    rem = sum(1 for l in d if l.startswith('-') and not l.startswith('---'))
    (OUT / (str(rel).replace('/', '__') + '.diff')).write_text('\n'.join(d))
    rows.append((str(rel), u.name, f'+{add} -{rem}'))
for r in rows:
    print('%-50s %-36s %s' % r)
