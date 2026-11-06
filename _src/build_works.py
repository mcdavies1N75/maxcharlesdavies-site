# Runs inside build.py (uses t, d, head, header, footer, CSS, cut, re)
import json as _j
_W=_j.loads(open('works.min.json').read())
NW=len(_W); NP=sum(len(w['perfs']) for w in _W)
full=open('works_section_full.html').read()
full=full.replace('<span class="kicker">Catalogue</span><h2>Works</h2>','<span class="kicker">Catalogue</span><h2>All works</h2>')
assert 'All works' in full
WCSS=CSS+'''.yr-h{font-size:var(--step-1);margin:2rem 0 .3rem}
.plist{list-style:none;margin:0;padding:0}
.plist li{display:grid;grid-template-columns:6.5rem minmax(0,1fr);gap:1rem;padding:.65rem 0;border-top:1px solid var(--rule);font-size:var(--step--1);color:var(--muted)}
.plist .dt{font-variant-numeric:tabular-nums}
.plist a{font-family:var(--font-display);font-style:italic;font-size:1.08rem;color:var(--ink)}
.plist a:hover{color:var(--accent)}
.page-intro{max-width:var(--measure);margin:0 0 2rem}
@media (max-width:560px){.plist li{grid-template-columns:minmax(0,1fr);gap:.1rem}}
'''
whead=head.replace('<title>Max Charles Davies, Composer</title>','<title>Works and Performances, by Max Charles Davies</title>')
whead=re.sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="The complete catalogue of works by composer Max Charles Davies, with every performance.">',whead)
whead=whead.replace('</style>',WCSS+'</style>')
wheader=header.replace('href="#your-name"','href="name.html"').replace('>Your name</a>','>Hear your name</a>')
wheader=re.sub(r'href="#(?!works"|performances")(\w[\w-]*)"',lambda m:f'href="index.html#{m.group(1)}"',wheader).replace('href="index.html#top"','href="index.html"')
perf=f'''  <section id="performances" style="border-bottom:0">
    <div class="wrap">
      <div class="sec-head"><span class="kicker">Performances</span><h2>Every performance</h2></div>
      <div class="upcoming" hidden></div>
      <p class="page-intro">All <span class="nperf">{NP}</span> performances and broadcasts I have records of, newest first. Select a title to see the work in the catalogue above.</p>
      <div id="allperf"></div>
    </div>
  </section>
'''
ext_js=cut(t,'/* ---------- Links to other','/* ---------- Name to music')
up_js=cut(t,'/* ---------- Coming up','/* ---------- Links to other').replace('__UPCOMING__',open('upcoming.json').read().strip())
cat_js=cut(t,'/* ---------- Works catalogue','</script>')
perf_js=r'''/* ---------- Every performance ---------- */
(function(){
  const box = document.getElementById('allperf'); if (!box) return;
  const MON = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const all = [];
  WORKS.forEach(w => w.perfs.forEach(p => {
    const m = p.date.match(/(\d\d)\/(\d\d)\/(\d{4})/); if (!m) return;
    all.push({w, text: p.text, y: m[3], k: m[3] + m[2] + m[1], d: `${+m[1]} ${MON[+m[2] - 1]} ${m[3]}`});
  }));
  all.sort((a, b) => b.k.localeCompare(a.k));
  // Turn the work's title at the start of the entry into the link, or add it if the entry starts differently.
  function line(text, w){
    const t = text.replace(/ /g, ' ').replace(/ -- /g, ' – ');
    const a = t.toLowerCase(), b = w.title.toLowerCase();
    let n = 0; while (n < a.length && n < b.length && a[n] === b[n]) n++;
    if (n >= Math.min(10, b.length)) {
      const rest = t.slice(n), m = rest.search(/ \(| for |,|;|\. /), end = n + (m < 0 ? rest.length : m);
      return `<a href="#${w.id}" data-work>${esc(t.slice(0, end))}</a>${esc(t.slice(end))}`;
    }
    return `<a href="#${w.id}" data-work>${esc(w.title)}</a>: ${esc(t)}`;
  }
  let html = '', yr = '';
  all.forEach(p => {
    if (p.y !== yr) { html += (yr ? '</ul>' : '') + `<h3 class="yr-h">${p.y}</h3><ul class="plist">`; yr = p.y; }
    html += `<li><span class="dt">${p.d}</span><span>${line(p.text, p.w)}</span></li>`;
  });
  box.innerHTML = html + '</ul>';
})();

'''
works_page='\n'.join([whead+'</head>','<body>',wheader,'<main id="top">',full,perf,'</main>','<a class="float-back" href="index.html"><span aria-hidden="true">←</span> Back to the homepage</a>',footer,'<script>',"/* Arriving without a section link: start at the top of the page. */\nif ('scrollRestoration' in history) history.scrollRestoration = 'manual';\nif (!location.hash || location.hash === '#top') { const top = () => scrollTo(0, 0); top(); addEventListener('DOMContentLoaded', top); addEventListener('load', () => { top(); setTimeout(top, 60); setTimeout(top, 300); }); }",'const WORKS = '+d+';','',up_js,ext_js,perf_js,cat_js,'</script>','</body>','</html>'])
open('dist/works.html','w').write(works_page)
print('works.html',len(works_page),NW,NP)
