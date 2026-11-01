import re, json, sys
md=open(sys.argv[1]).read().split('\n')
# locate sections
start=[i for i,l in enumerate(md) if l.strip()=='# Multi-disciplinary Projects'][0]
end=[i for i,l in enumerate(md) if l.startswith('# **List of Works')][0]
ph=[i for i,l in enumerate(md) if l.startswith('# Performance Histories')][0]
def clean(s):
    s=re.sub(r'\[\]\{#[^}]*\}','',s)
    s=re.sub(r'\[([^\]]*)\]\(#[^)]*\)',r'\1',s)
    s=s.replace('\\','').replace('**','')
    return s.strip()
def links(s): return re.findall(r'<(https?://[^>]+)>|\]\((https?://[^)]+)\)',s)
works=[];cat=None;w=None
wre=re.compile(r'^(?:\[\]\{#(\S+) \.anchor\})?\s*\*([^*]+)\*\s*(\(\d{4}.*|\(with.*)$')
for l in md[start:end]:
    if l.startswith('# '):
        t=l[2:].strip().strip('*')
        if t: cat=t
        continue
    l=l.replace('* *(revised version)*',' (revised version)*')
    m=wre.match(l) or (wre.match(l[2:]) if l.startswith('> *') else None)
    if m:
        w={'cat':cat,'title':m.group(2).strip(),'meta':clean(m.group(3)),'desc':[],'forces':[],'media':[],'hist':None}
        works.append(w);continue
    if w is None: continue
    s=l.lstrip('> ').strip()
    if not s or s.startswith('[Back to top') : continue
    hm=re.match(r'\[Performance History\]\(#(\S+)\)',s)
    if hm: w['hist']=hm.group(1);continue
    if re.match(r'(Link( to)? media|Link to published score|Link media)',s):
        for a,b in links(s): w['media'].append(a or b)
        for t,u in re.findall(r'\[([^\]]+)\]\((https?://[^)]+)\)',s): pass
        continue
    fm=re.match(r'(Orchestration|Voices?|Instruments?)\s*:\s*(.*)',s)
    if fm: w['forces'].append((fm.group(1),clean(fm.group(2))));continue
    if s.startswith('-') or s.startswith('Collaborators'): continue
    w['desc'].append(clean(re.sub(r'\*','',s)))
# perf histories
hist={};cur=None
for l in md[ph:]:
    m=re.match(r'\[\]\{#(\S+) \.anchor\}(.*)',l)
    if m: cur=m.group(1);hist[cur]=[];continue
    if cur and l.startswith('-   '):
        hist[cur].append(clean(l[4:].replace('*','')))
for w in works:
    w['perfs']=hist.get(w['hist'],[]) if w['hist'] else []
    w['desc']=' '.join(w['desc'])
    y=re.search(r'\((\d{4}.*?)\)\s',w['meta']+' '); w['year']=y.group(1) if y else ''
    d=re.search(r'\)\s*([^()]*)$',w['meta']); w['dur']=d.group(1).strip() if d else ''
json.dump(works,open(sys.argv[2],'w'),indent=1,ensure_ascii=False)
print(len(works), sum(1 for w in works if w['hist'] and not w['perfs']))
for w in works: print(w['cat'][:18],'|',w['title'],'|',w['year'],'|',w['dur'],'|',len(w['perfs']),'|',w['media'][:1])
