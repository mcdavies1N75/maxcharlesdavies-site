import re
t=open('template.html').read(); d=open('works.min.json').read().replace('</','<\\/')
def cut(s,a,b):
    i=s.index(a); j=s.index(b,i); return s[i:j]
head=t[:t.index('</head>')]
header=cut(t,'<header class="top">','</header>')+'</header>'
yn=cut(t,'  <section id="your-name">','  <section id="performances">')
nm_js=cut(t,'/* ---------- Name to music','/* Hero: my own name')
visitor_js=cut(t,"/* Visitor's name */",'/* ---------- Works catalogue')
footer=cut(t,'<footer>','</footer>')+'</footer>'
CSS='''.cta-wrap{display:grid;gap:.6rem;justify-items:start;margin-top:2.5rem;padding-top:2rem;border-top:1px solid var(--rule)}
.cta{display:inline-flex;align-items:center;gap:.9rem;font-family:var(--font-display);font-size:var(--step-2);line-height:1.1;color:var(--paper);background:var(--accent);text-decoration:none;border-radius:999px;padding:1.1rem 2.2rem}
.cta:hover{background:var(--ink);color:var(--paper)}
.cta .arr{font-family:var(--font-body);font-size:.8em;transition:transform .2s}
.cta:hover .arr{transform:translateX(4px)}
.cta-note{font-size:var(--step--1);color:var(--muted);margin:0}
@media (max-width:560px){.cta{width:100%;justify-content:center;padding:1rem 1.2rem}}
@media (prefers-reduced-motion: no-preference){.cta.nudge{animation:nudge 1.2s ease 2}@keyframes nudge{0%,100%{transform:none}50%{transform:scale(1.04)}}}
.back-simple{margin:1.5rem 0 0;font-size:var(--step--1)}
.intro{font-family:var(--font-display);font-style:italic;font-size:var(--step-1);max-width:40ch;margin:0 0 1rem;line-height:1.35}
'''
# ---------- index.html ----------
idx=t.replace(yn,'').replace(visitor_js,'')
idx=idx.replace('href="#your-name"','href="name.html"')
idx=idx.replace('<a href="name.html">Your name</a>','<a href="name.html">Hear your name</a>')
import json as _jj
_WW=_jj.loads(open('works.min.json').read())
idx=idx.replace('__NWORKS__',str(len(_WW))).replace('__NPERF__',str(sum(len(w['perfs']) for w in _WW)))
open('dist/index.html','w').write(idx.replace('__WORKS__',d))
# ---------- name.html ----------
nhead=head.replace('<title>Max Charles Davies, Composer</title>','<title>Hear Your Name, by Max Charles Davies</title>')
nhead=re.sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="Type your name and hear its letters mapped to musical pitches, using composer Max Charles Davies\' method.">',nhead)
nhead=nhead.replace('</style>',CSS+'</style>')
nheader=re.sub(r'href="#(\w[\w-]*)"',lambda m:f'href="index.html#{m.group(1)}"',header).replace('href="index.html#top"','href="index.html"')
nheader=nheader.replace('<a href="name.html">Hear your name</a>','').replace('<a href="index.html#your-name">Your name</a>','')
sec=yn.replace('<span class="kicker">Try it</span><h2>Hear your own name</h2>','<span class="kicker">Max Charles Davies, composer</span><h2>Hear your own name</h2>')
sec=sec.replace('<p class="lead">Type your name','<p class="intro">Many of my pieces begin with something that already exists, such as a name or a line of poetry. Here is the first step: mapping letters to pitches.</p>\n      <p class="lead">Type your name')
sec=sec.replace('      </div>\n    </div>\n  </section>','''      </div>
      <p class="back-simple"><a href="explore.html">Go deeper: every note each letter could become →</a></p>
      <div class="cta-wrap">
        <a class="cta" id="cta" href="index.html">Explore my music <span class="arr" aria-hidden="true">→</span></a>
        <p class="cta-note">Works, recordings and research on my homepage</p>
      </div>
    </div>
  </section>''')
assert 'id="cta"' in sec
vjs=visitor_js.replace("btn.addEventListener('click', e => NameMusic.play(() => notes, e.currentTarget, 'Play'));",
 "btn.addEventListener('click', e => { NameMusic.play(() => notes, e.currentTarget, 'Play'); const c = document.getElementById('cta'); setTimeout(() => { c.classList.remove('nudge'); void c.offsetWidth; c.classList.add('nudge'); }, notes.length * 360 + 600); });")
assert vjs!=visitor_js
name='\n'.join([nhead+'</head>','<body>',nheader,'<main id="top">',sec.replace('<section id="your-name">','<section id="your-name" style="border-bottom:0">'),'</main>',footer,'<script>',nm_js,vjs,'</script>','</body>','</html>'])
open('dist/name.html','w').write(name)
exec(open('build_explore.py').read())
exec(open('build_works.py').read())
print(len(idx),len(name), 'your-name' in idx, idx.count('name.html'))
