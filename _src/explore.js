/* ---------- Explore every option ---------- */
(function(){
  // The chromatic naming table, row by row. Accidental columns (1,3,6,8,10) are spelled as each tradition names them.
  const SH = {1:'C#',3:'D#',6:'F#',8:'G#',10:'A#'}, FL = {1:'Db',3:'Eb',6:'Gb',8:'Ab',10:'Bb'};
  const NAT = {0:'C',2:'D',4:'E',5:'F',7:'G',9:'A',11:'B'};
  const full = (names, acc) => names.map((n, i) => [n, NAT[i] || acc[i]]);
  const flatRow = names => names.map((n, k) => [n, FL[[1,3,6,8,10][k]]]);
  const TABLE = [
    ['English', full(['C','C sharp','D','D sharp','E','F','F sharp','G','G sharp','A','A sharp','B'], SH)],
    ['English', flatRow(['D flat','E flat','G flat','A flat','B flat'])],
    ['German', full(['C','Cis','D','Dis','E','F','Fis','G','Gis','A','Ais','H'], SH).map(([n,p]) => [n, n === 'H' ? 'B' : p])],
    ['German', flatRow(['Des','Es','Ges','As','B'])],
    ['Swedish', full(['C','Ciss','D','Diss','E','F','Fiss','G','Giss','A','Aiss','H'], SH).map(([n,p]) => [n, n === 'H' ? 'B' : p])],
    ['Swedish', flatRow(['Dess','Ess','Gess','Ass','Bess'])],
    ['Dutch', full(['C','Cis','D','Dis','E','F','Fis','G','Gis','A','Ais','B'], SH)],
    ['Dutch', flatRow(['Des','Es','Ges','As','Bes'])],
    ['Solfège', full(['do','do diesis','re','re diesis','mi','fa','fa diesis','sol','sol diesis','la','la diesis','si'], SH)],
    ['Solfège', flatRow(['re bemolle','mi bemolle','sol bemolle','la bemolle','si bemolle'])],
    ['Byzantine', full(['Ni','Ni diesis','Pa','Pa diesis','Vu','Ga','Ga diesis','Di','Di diesis','Ke','Ke diesis','Zo'], SH)],
    ['Byzantine', flatRow(['Pa hyphesis','Vu hyphesis','Di hyphesis','Ke hyphesis','Zo hyphesis'])],
    // The table stops here: by the Byzantine row every letter that can appear has appeared.
  ];
  const EXTRA = [['ti','B','English solfège'],['soh','G','Tonic sol-fa'],['ut','C','Medieval'],['rey','D','My addition']];
  const PROXY = {J:'I', Q:'K', W:'U'}; // J began as I; Q sounds as K; W is a double U
  const norm = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '');

  // The full note name, lower case, with the matched letter in capitals.
  function mark(name, L){
    const lo = L.toLowerCase(); let done = false;
    return [...name.toLowerCase()].map(c => { if (!done && norm(c)[0] === lo) { done = true; return L; } return c; }).join('');
  }
  const cache = {};
  function options(ch){
    if (cache[ch]) return cache[ch];
    const out = [], seen = new Set();
    // One option per pitch, gathering every note name that gives it.
    const add = (p, label, source, kind) => { const o = out.find(x => x.p === p); if (o) { if (!o.labels.includes(label)) { o.labels.push(label); o.sources.push(source); } return; } out.push({p, labels:[label], sources:[source], kind}); };
    if (ch === 'X') {
      // A double sharp is written as a small x, so X takes a sharpened note.
      ['F#','C#','G#','D#','A#'].forEach(p => add(p, NameMusic.pretty(p), 'the double-sharp sign', 'Sharpened notes'));
      return cache[ch] = out;
    }
    const L = PROXY[ch] || ch;
    // A to G stay themselves: the Western letter names. The one exception is B, which can also be B-flat (the German B).
    if ('ACDEFG'.includes(L)) { add(L, L, 'Letter name', 'The letter itself'); return cache[ch] = out; }
    // Fixed letters: one note only.
    const FIXED = {T:['B','Ti'], K:['A','Ke'], R:['D','Re'], U:['C','Ut'], Y:['D','reY']};
    if (FIXED[L]) { add(FIXED[L][0], FIXED[L][1], 'My rule' + (PROXY[ch] ? `, ${ch} as ${L}` : ''), 'Fixed'); return cache[ch] = out; }
    if (L === 'B') { add('B', 'B', 'Letter name', 'The letter itself'); add('Bb', 'B', 'German', 'The letter itself'); return cache[ch] = out; }
    const via = PROXY[ch] ? ` (${ch} as ${L})` : '';
    const begins = [], inside = [];
    // A letter counts only if it is one of the first two letters of the note name's first word.
    const head = name => norm(name).toUpperCase().split(/[\s-]+/)[0].slice(0, 2);
    TABLE.forEach(([trad, cells]) => cells.forEach(([name, p]) => {
      const h = head(name);
      if (h[0] === L) begins.push([name, p, trad]);
      else if (h[1] === L) inside.push([name, p, trad]);
    }));
    EXTRA.forEach(([name, p, trad]) => { const h = head(name); if (h[0] === L) begins.push([name, p, trad]); else if (h[1] === L) inside.push([name, p, trad]); });
    begins.forEach(([n, p, trad]) => add(p, mark(n, L), trad + via, `Begins with ${L}`));
    inside.forEach(([n, p, trad]) => add(p, mark(n, L), trad + via, `${L} as the second letter`));
    // My own rules always stay available (reY, for example, isn't in the first two letters).
    const rule = NameMusic.MAP[L];
    if (rule && !out.some(o => o.p === rule[0])) out.push({p:rule[0], labels:[rule[1]], sources:['My rule'], kind:'My rules'});
    return cache[ch] = out;
  }

  const input = document.getElementById('xname'), svg = document.getElementById('stave3');
  const cards = document.getElementById('cards'), count = document.getElementById('xcount');
  const narrow = matchMedia('(max-width: 560px)');
  let picks = {}, lastText = null, items = [], notes = [];

  function ruleDefault(r){
    // My rules (as on the simple page); an undecided I or J defaults to tI.
    const p = r.p || 'B';
    return p;
  }
  function update(){
    const ws = NameMusic.words(input.value);
    const key = ws.join(' ');
    if (key !== lastText) { picks = {}; lastText = key; }
    const an = NameMusic.analyse(ws, {});
    items = []; let idx = 0;
    an.forEach(w => w.notes.forEach(r => {
      const opts = options(r.ch);
      const def = ruleDefault(r);
      const di = Math.max(0, opts.findIndex(o => o.p === def));
      const k = idx++;
      const sel = picks[k] != null ? picks[k] : di;
      const o = opts[sel];
      const label = sel === di && r.label && r.label !== '?' ? r.label : (sel === di && (r.ch === 'I' || r.ch === 'J') ? 'tI' : o.labels[0]);
      items.push({k, ch:r.ch, word:w.word, opts, di, sel, p:o.p, label});
    }));
    // stave
    const grouped = []; let n = 0;
    an.forEach(w => { grouped.push({word:w.word, notes: items.slice(n, n + w.notes.length).map(it => ({p:it.p, label:it.label, ch:it.ch, chosen: it.sel !== it.di}))}); n += w.notes.length; });
    if (items.length) notes = NameMusic.draw(svg, grouped, narrow.matches ? 8 : 20);
    else { notes = []; [...svg.querySelectorAll(':scope > :not(title)')].forEach(x => x.remove()); }
    // cards
    let html = '', curWord = null;
    items.forEach(it => {
      if (it.word !== curWord) { if (curWord !== null) html += '</div>'; html += `<div class="card-word"><h3>${it.word.charAt(0) + it.word.slice(1).toLowerCase()}</h3>`; curWord = it.word; }
      const groups = {}; it.opts.forEach((o, j) => (groups[o.kind] = groups[o.kind] || []).push([o, j]));
      html += `<div class="card${it.sel !== it.di ? ' changed' : ''}"><label for="opt-${it.k}"><span class="big">${it.ch}</span><span class="n">${it.opts.length} option${it.opts.length === 1 ? '' : 's'}</span></label>
        <select id="opt-${it.k}" data-k="${it.k}">${Object.entries(groups).map(([g, list]) => `<optgroup label="${g}">${list.map(([o, j]) => `<option value="${j}"${j === it.sel ? ' selected' : ''}>${NameMusic.pretty(o.p)} · ${o.labels.slice(0, 4).join(', ')}${o.labels.length > 4 ? '…' : ''} (${[...new Set(o.sources)].slice(0, 3).join(', ')})${j === it.di ? ' ★' : ''}</option>`).join('')}</optgroup>`).join('')}</select></div>`;
    });
    if (curWord !== null) html += '</div>';
    cards.innerHTML = html;
    const total = items.reduce((a, it) => a * BigInt(it.opts.length), 1n);
    count.textContent = items.length ? `Your name can be heard ${total.toLocaleString('en-GB')} different ways. ★ marks the note my rules would choose.` : '';
    document.getElementById('xplay').disabled = !items.length;
  }
  // Pick up the name from the simple page (?name=...) or from earlier in this visit, and carry it back.
  function carry(){
    const v = input.value.trim();
    document.querySelectorAll('a[href^="name.html"]').forEach(a => a.href = v ? 'name.html?name=' + encodeURIComponent(v) : 'name.html');
    try { sessionStorage.setItem('mcd-name', v); } catch (e) {}
  }
  try { const q = new URLSearchParams(location.search).get('name') || sessionStorage.getItem('mcd-name'); if (q) input.value = q.slice(0, 40); } catch (e) {}
  input.addEventListener('input', carry);
  input.addEventListener('focus', () => input.select());
  cards.addEventListener('change', e => { const s = e.target.closest('select'); if (!s) return; picks[s.dataset.k] = +s.value; update(); const again = document.getElementById(s.id); if (again) again.focus(); });
  input.addEventListener('input', update);
  narrow.addEventListener('change', update);
  document.getElementById('xplay').addEventListener('click', e => NameMusic.play(() => notes, e.currentTarget, 'Play'));
  document.getElementById('xshuffle').addEventListener('click', () => { items.forEach(it => picks[it.k] = Math.floor(Math.random() * it.opts.length)); update(); });
  document.getElementById('xreset').addEventListener('click', () => { picks = {}; update(); });
  update(); carry();
})();
