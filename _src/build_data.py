import json,re,sys
W=json.load(open('src/works.json'))
CAT={'Multi-disciplinary Projects':'Multidisciplinary','Electronic or Media':'Electronic & media',
'Opera and Music Theatre':'Opera & music theatre','Orchestral works (including string orchestra)':'Orchestral',
'Large Ensemble (7 or more players)':'Large ensemble','Works for 2-6 players':'Chamber',
'Solo Works (excluding keyboard) / Solo Works + tape/electronics':'Solo','Solo Keyboard(s) / Solo Keyboard + technology':'Keyboard',
'Chorus a cappella / Chorus plus 1 instrument':'Choral','Chorus and Orchestra/Ensemble, with or without soloists':'Choral',
'Solo voice and Large Ensemble (7 or more players)':'Voice','Solo Voice(s) and up to 6 players':'Voice'}
def mlabel(u):
    for k,v in [('youtu','YouTube'),('soundcloud','SoundCloud'),('vimeo','Vimeo'),('spotify','Spotify'),('instagram','Instagram'),('warwickmusic','Published score')]:
        if k in u: return v
    return 'Link'
FIX=[('06/15/2015','06/12/2015'),('Y Gros Fawr','Y Gors Fawr'),('Are in we love?','Are we in Love?'),('Sir Philip Sydney','Sir Philip Sidney'),('Ruth Mclees','Ruth McLees')]
def fx(s):
    for a,b in FIX: s=s.replace(a,b)
    return s
out={}
for w in W:
    key=(w['title'].lower().replace('…','...'),w['year'])
    c=CAT.get(w['cat'],w['cat'])
    forces=[f"{k}: {v}" for k,v in w['forces']]
    perfs=[]
    for p in w['perfs']:
        p=fx(p); m=re.match(r'([\d/,& \-]+?)\s+(.*)',p)
        perfs.append({'date':m.group(1).strip() if m else '','text':m.group(2) if m else p})
    if key in out:
        o=out[key]
        if c not in o['cats']: o['cats'].append(c)
        for f in forces:
            if f not in o['forces']: o['forces'].append(f)
        for u in w['media']:
            if u not in [x['url'] for x in o['media']]: o['media'].append({'url':u,'label':mlabel(u)})
        for p in perfs:
            if p not in o['perfs']: o['perfs'].append(p)
        if len(w['desc'])>len(o['desc']): o['desc']=fx(w['desc'])
    else:
        out[key]={'title':fx(w['title']).replace('...','…').replace(' -- ',' – ').replace(' - ',' – '),'year':w['year'],'dur':w['dur'].replace('Concerto for Orchestra ',''),
          'desc':fx(w['desc']).replace(' -- ',' – '),'cats':[c],'forces':forces,
          'media':[{'url':u,'label':mlabel(u)} for u in w['media']],'perfs':perfs}
works=list(out.values())
# subtitle fixes
for w in works:
    if w['title']=='The Mysterious Kiss': w['title']='The Mysterious Kiss: Concerto for Orchestra'
    if w['title']=='Manhattan Circus': w['desc']+=' With Chris Nash (coder).'
    if w['title']=='Piano Mapping': w['desc']='Developing an audio-visual piano using projection mapping, visualising improvisations, and exploring its potential for filmmaking and animation. Collaborators include Rahil Al Jassasi, Mic Palmer, Rhys Bruford, the UWE Design Enterprise Studio and UWE Foundry.'
works+= [
 {'title':'Tears, Idle Tears','year':'2026','dur':'','desc':'A setting of Tennyson whose melody and harmony are drawn, syllable by syllable, from the text itself.','cats':['Choral'],'forces':['Voices: SATB'],'media':[],'perfs':[],'new':True},
 {'title':'Vignettes','year':'2026','dur':'','desc':'Orchestral miniatures grown from the material of Tears, Idle Tears, stretched across Fibonacci proportions.','cats':['Orchestral'],'forces':['Orchestration: orchestra'],'media':[],'perfs':[],'new':True},
]
def yk(w):
    m=re.match(r'\d{4}',w['year']); return int(m.group(0)) if m else 0
works.sort(key=lambda w:(-yk(w),w['title']))
for i,w in enumerate(works): w['id']='w'+re.sub(r'[^a-z0-9]+','-',w['title'].lower()).strip('-')
json.dump(works,open('works.min.json','w'),ensure_ascii=False,separators=(',',':'))
print(len(works)); print(sorted({c for w in works for c in w['cats']}))
print([w['id'] for w in works][:12])
