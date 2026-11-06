import re
SLOTS=[('flute','flutes'),('oboe','oboes'),('clarinet','clarinets'),('bassoon','bassoons'),('horn','horns'),('trumpet','trumpets'),('trombone','trombones'),('tuba','tubas')]
AB={'fl':('flute','flutes'),'afl':('alto flute','alto flutes'),'picc':('piccolo','piccolos'),'ob':('oboe','oboes'),'ca':('cor anglais','cors anglais'),'c.a':('cor anglais','cors anglais'),
'cl':('clarinet','clarinets'),'bcl':('bass clarinet','bass clarinets'),'b.cl':('bass clarinet','bass clarinets'),'eb':('E♭ clarinet','E♭ clarinets'),'cbn':('contrabassoon','contrabassoons'),
'asax':('alto saxophone','alto saxophones'),'tsax':('tenor saxophone','tenor saxophones'),'ssax':('soprano saxophone','soprano saxophones'),
'hn':('horn','horns'),'tpt':('trumpet','trumpets'),'d':('D trumpet','D trumpets'),'tbn':('trombone','trombones'),'ttbn':('tenor trombone','tenor trombones'),'btbn':('bass trombone','bass trombones'),'tba':('tuba','tubas'),
'timp':('timpani','timpani'),'perc':('percussionist','percussionists'),'hp':('harp','harps'),'pno':('piano','pianos'),'cel':('celesta','celestas'),'hpsd':('harpsichord','harpsichords'),
'vln':('violin','violins'),'vla':('viola','violas'),'vcl':('cello','cellos'),'db':('double bass','double basses'),'gtr':('guitar','guitars'),'bgtr':('bass guitar','bass guitars'),'dr':('drum kit','drum kits'),
'soloaugpno':('solo augmented piano',None),'solopno':('solo piano',None),'s.cym':('suspended cymbal','suspended cymbals')}
ORD={1:'1st',2:'2nd',3:'3rd',4:'4th'}
def split_top(s):
    out,depth,cur=[],0,''
    for ch in s:
        if ch=='(':depth+=1
        if ch==')':depth-=1
        if ch=='.' and depth==0:
            out.append(cur);cur=''
        else: cur+=ch
    if cur: out.append(cur)
    return [t for t in out if t.strip()]
def noun(key,n=1):
    s,p=AB[key]; return s if n==1 or p is None else p
def counted(n,key):
    return (noun(key) if n==1 else f'{n} {noun(key,2)}')
def doublings(inner):
    parts=[]
    for m in re.finditer(r'(\d)?=([A-Za-z.]+?)(?=\.?\d=|\.?$|\.\d)',inner):
        k=m.group(2).strip('.').lower()
        if k not in AB: return None
        parts.append((f'{ORD[int(m.group(1))]} doubling ' if m.group(1) else 'doubling ')+noun(k))
    return ', '.join(parts) if parts else None
def strings(tok):
    m=re.fullmatch(r'str(?:\((.*)\))?',tok.strip())
    if not m: return None
    if not m.group(1): return 'strings'
    inner=m.group(1)
    mm=re.match(r'\s*min\.\s*([\d.]+?)\s*(?:(ideal|preferred)\s*([\d.]+))?\s*$',inner)
    if not mm: return None
    a=mm.group(1).strip('.').split('.')
    s=f'strings (at least {a[0]} first violins, {a[1]} second violins, {a[2]} violas, {a[3]} cellos and {a[4]} double bass{"es" if a[4]!="1" else ""}'
    if mm.group(3):
        b=mm.group(3).strip('.').split('.'); s+=f'; ideally {", ".join(b[:-1])} and {b[-1]}'
    return s+')'
def item(tok):
    tok=tok.strip()
    st=strings(tok)
    if st: return st
    m=re.fullmatch(r'(\d*)([A-Za-z.]+?)(?:\((.*)\))?',tok)
    if not m: return None
    n=int(m.group(1)) if m.group(1) else 1; k=m.group(2).lower().strip('.')
    if k not in AB: return None
    s=counted(n,k)
    if m.group(3):
        d=doublings(m.group(3))
        if d is None:
            if k=='timp' and m.group(3).startswith('='): d='doubling '+noun(m.group(3)[1:].lower().strip('.'))
            else: return None
        s+=f' ({d})'
    return s
def expand(line):
    m=re.match(r'(Orchestration|Instruments):\s*(.*)$',line)
    if not m: return None
    body=m.group(2).strip().rstrip('.')
    toks=split_top(body)
    if len(toks)<2: return None
    out=[];slot=0
    for t in toks:
        mm=re.fullmatch(r'(\d)(?:\((.*)\))?',t.strip())
        if mm and slot<8:
            n=int(mm.group(1)); name=SLOTS[slot]; slot+=1
            if n==0: continue
            s=name[0] if n==1 else f'{n} {name[1]}'
            if mm.group(2):
                d=doublings(mm.group(2))
                if d is None: return None
                s+=f' ({d})'
            out.append(s); continue
        e=item(t)
        if e is None: return None
        out.append(e)
    return ', '.join(out)

MANUAL={
 'Orchestration: String Octet (4vln.2vla.vcl.db)':'String octet (4 violins, 2 violas, cello, double bass)',
 'Orchestration: double brass dectet (dectet 1: 4tpt.1hn.3ttbn.1btbn.1tba; dectet 2: 4tpt(1=picc.tpt).1hn.3ttbn.1btbn.1tba)':'Two brass dectets, each with 4 trumpets, horn, 3 tenor trombones, bass trombone and tuba (in the second, the 1st trumpet doubles piccolo trumpet)',
 'Orchestration: fl(=picc & afl).cl(=bcl).vln.vcl.pno':'flute (doubling piccolo and alto flute), clarinet (doubling bass clarinet), violin, cello, piano',
 'Orchestration: cl(or vln).vcl.pno':'clarinet (or violin), cello, piano',
 'Orchestration: ssax (or cl) and string quartet (2vln.vla.vcl)':'soprano saxophone (or clarinet) and string quartet (2 violins, viola, cello)',
}
def plain(line):
    r=_plain(line)
    return r[0].upper()+r[1:] if r else r
def _plain(line):
    if line in MANUAL: return MANUAL[line]
    e=expand(line)
    if e: return e
    # Words with an abbreviated list in brackets, e.g. "string quintet (2vln.vla.2vcl)"
    m=re.match(r'(Orchestration|Instruments):\s*(.*)$',line)
    if not m: return None
    body=m.group(2); changed=False
    def sub(mm):
        nonlocal changed
        inner=mm.group(1)
        if ':' in inner or ';' in inner:
            parts=re.split(r'(;\s*|:\s*)',inner); res=[]
            for p in parts:
                e=expand('Orchestration: '+p) if '.' in p else None
                if e: changed=True
                res.append(e or p)
            return '('+''.join(res)+')'
        e=expand('Orchestration: '+inner)
        if e: changed=True; return '('+e+')'
        return mm.group(0)
    out=re.sub(r'\(([^()]*(?:\([^()]*\)[^()]*)*)\)',sub,body)
    if not changed: return None
    return out
