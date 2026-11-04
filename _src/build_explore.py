# Runs inside build.py (uses head, nheader, footer, nm_js, CSS, re)
XCSS = CSS + """.tools{display:flex;flex-wrap:wrap;gap:.5rem}
.btn.ghost{background:transparent;color:var(--ink);border:1px solid var(--rule)}
.btn.ghost:hover{border-color:var(--ink);background:transparent}
.count{font-size:var(--step--1);color:var(--muted);margin:0}
.cards{display:grid;gap:1.25rem}
.card-word{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:.6rem}
.card-word h3{grid-column:1/-1;font-size:1.15rem;margin:.4rem 0 0}
.card{border:1px solid var(--rule);border-radius:6px;padding:.6rem .7rem;display:grid;gap:.45rem}
.card.changed{border-color:var(--accent);background:var(--accent-soft)}
.card label{display:flex;align-items:baseline;justify-content:space-between;gap:.5rem}
.card .big{font-family:var(--font-display);font-size:1.7rem;line-height:1}
.card .n{font-size:.75rem;color:var(--muted)}
.card select{width:100%;font:inherit;font-size:.85rem;color:var(--ink);background:var(--paper);border:1px solid var(--rule);border-radius:4px;padding:.3rem .4rem}
"""
xhead = head.replace('<title>Max Charles Davies, Composer</title>', '<title>Inside the Constraint, by Max Charles Davies</title>')
xhead = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Explore every note each letter of your name can become, in composer Max Charles Davies\' letter-to-pitch system.">', xhead)
xhead = xhead.replace('</style>', XCSS + '</style>')
xsec = '''  <section id="explore" style="border-bottom:0">
    <div class="wrap namer">
      <div class="sec-head"><span class="kicker">Max Charles Davies, composer</span><h2>Inside the constraint</h2></div>
      <p class="intro">My rules give one answer, but most letters can be found in several note names. The table sets the limits; within them, I choose by ear.</p>
      <p class="lead">Each letter below lists the notes it can become. A to G always stay themselves, except that B can also be B♭, as in German, and K, R, T, U and Y each have one fixed note. Other letters count only if they begin a note name or are its second letter, as in <i>eS</i> or <i>mI</i>, and my own rules are always included. Change any of them and listen to the difference.</p>
      <label for="xname" class="field-label">Type a name here <span class="hint">(replace the example)</span></label>
      <div class="namer-row">
        <input id="xname" type="text" maxlength="40" autocomplete="off" spellcheck="false" value="Max Charles Davies">
        <button class="btn" id="xplay" type="button"><svg viewBox="0 0 10 10" aria-hidden="true"><path d="M1 0l9 5-9 5z"/></svg><span>Play</span></button>
      </div>
      <div class="tools"><button class="btn ghost" id="xshuffle" type="button">Surprise me</button><button class="btn ghost" id="xreset" type="button">Back to my rules</button></div>
      <p id="xcount" class="count" aria-live="polite"></p>
      <svg class="stave" id="stave3" role="img" aria-label="The name written as notes on a stave"><title>The name written as notes on a stave</title></svg>
      <div id="cards" class="cards"></div>
      <p class="back-simple"><a href="name.html">Back to the simple version</a></p>
      <div class="cta-wrap">
        <a class="cta" id="cta" href="index.html">Explore my music <span class="arr" aria-hidden="true">→</span></a>
        <p class="cta-note">Works, recordings and research on my homepage</p>
      </div>
    </div>
  </section>'''
xjs = open('explore.js').read()
explore = '\n'.join([xhead + '</head>', '<body>', nheader, '<main id="top">', xsec, '</main>', footer, '<script>', nm_js, xjs, '</script>', '</body>', '</html>'])
open('dist/explore.html', 'w').write(explore)
