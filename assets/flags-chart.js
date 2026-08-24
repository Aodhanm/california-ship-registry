/* Flags at anchor, 1769–1821 — composition by year.
   Plain SVG: a five-series line chart on a linear scale does not need a 280KB
   library. Marks follow the house spec — 2px lines, >=8px end markers with a 2px
   surface ring, hairline solid gridlines, direct labels at the line ends only,
   and a legend that is always present. */
(function () {
  'use strict';
  var SLOT = { spain: 'var(--series-1)', usa: 'var(--series-2)',
               russia: 'var(--series-3)', britain: 'var(--series-4)',
               other: 'var(--series-other)' };
  var NS = 'http://www.w3.org/2000/svg';
  function el(n, a) { var e = document.createElementNS(NS, n); for (var k in a) if (a[k] != null) e.setAttribute(k, a[k]); return e; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]; }); }

  fetch('./data/flags-by-year.json').then(function (r) { return r.json(); }).then(draw)
    .catch(function (e) { document.getElementById('chart').outerHTML = '<p>Could not load the series: ' + esc(e.message) + '</p>'; });

  function draw(D) {
    window.__D = D;
    var lab = D.labels, years = D.years;
    var order = D.order.filter(function (k) { return k !== 'other'; });
    var W = 900, H = 520, ML = 52, MR = 152, MT = 64, MB = 116;
    var pw = W - ML - MR, ph = H - MT - MB;
    var STRIP_TOP = MT + ph + 52, STRIP_H = 26;
    var y0 = years[0], y1 = years[years.length - 1];
    var x = function (yr) { return ML + (yr - y0) / (y1 - y0) * pw; };
    var y = function (v) { return MT + ph - (v / 100) * ph; };

    var svg = document.getElementById('chart');
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
    svg.appendChild(el('rect', { x: 0, y: 0, width: W, height: H, fill: 'var(--surface-1)' }));

    var t = el('text', { x: 0, y: 20, class: 'g-title' });
    t.textContent = 'Whose ships were in California waters, 1769–1821'; svg.appendChild(t);
    var s2 = el('text', { x: 0, y: 38, class: 'g-sub' });
    s2.textContent = 'share of recorded arrivals · 5-year centred mean over ' + D.n_in_scope.toLocaleString() +
                     ' visits · annual values behind the line';
    svg.appendChild(s2);

    [0, 25, 50, 75, 100].forEach(function (v) {
      svg.appendChild(el('line', { x1: ML, x2: ML + pw, y1: y(v), y2: y(v), class: 'g-grid' }));
      var tx = el('text', { x: ML - 10, y: y(v) + 4, class: 'g-axis-text', 'text-anchor': 'end' });
      tx.textContent = v + (v === 100 ? '%' : ''); svg.appendChild(tx);
    });
    // decade ticks label the axis; every year is a position, not a label
    for (var yr = 1770; yr <= y1; yr += 10) {
      svg.appendChild(el('line', { x1: x(yr), x2: x(yr), y1: MT + ph, y2: MT + ph + 5, class: 'g-grid' }));
      var tx2 = el('text', { x: x(yr), y: MT + ph + 20, class: 'g-axis-text', 'text-anchor': 'middle' });
      tx2.textContent = yr; svg.appendChild(tx2);
    }

    // the two events the series is read against, marked once each
    [[1812, 'Ross founded', 12], [1810, 'war of independence begins', 28]].forEach(function (ev) {
      svg.appendChild(el('line', { x1: x(ev[0]), x2: x(ev[0]), y1: MT, y2: MT + ph, stroke: 'var(--grid)', 'stroke-width': 1 }));
      var a = el('text', { x: x(ev[0]) - 5, y: MT + ev[2], class: 'g-axis-text', 'text-anchor': 'end' });
      a.setAttribute('fill', 'var(--text-muted)'); a.setAttribute('font-size', '10');
      a.textContent = ev[1] + ' \u2192'; svg.appendChild(a);
    });

    // EVERY flag's first visit, marked and named. The whole point of a composition
    // series is when each party arrives, so it is drawn, not left to be inferred
    // from where a line lifts off the axis.
    var FV = (D.first_visits || []).filter(function (f) { return f.year >= y0 && f.year <= y1; });
    FV.forEach(function (f, i) {
      var ex = x(f.year), base = MT + ph;
      var col = SLOT[f.flag] || 'var(--text-secondary)';
      var lift = 22 + (i % 3) * 15;
      svg.appendChild(el('line', { x1: ex, x2: ex, y1: base, y2: base - lift,
        stroke: col, 'stroke-width': 1, opacity: .55, 'stroke-dasharray': '2 2' }));
      svg.appendChild(el('circle', { cx: ex, cy: base, r: 4, fill: col,
        stroke: 'var(--surface-1)', 'stroke-width': 2 }));
      var anchor = f.year > 1812 ? 'end' : (f.year < 1775 ? 'start' : 'middle');
      var dx = anchor === 'end' ? -5 : (anchor === 'start' ? 3 : 0);
      var a = el('text', { x: ex + dx, y: base - lift - 4, 'text-anchor': anchor });
      a.setAttribute('font-size', '10.5'); a.setAttribute('font-weight', '700');
      a.setAttribute('fill', col); a.textContent = f.who + ' ' + f.year;
      svg.appendChild(a);
      var b = el('text', { x: ex + dx, y: base - lift + 7, 'text-anchor': anchor });
      b.setAttribute('font-size', '9'); b.setAttribute('fill', 'var(--text-muted)');
      b.textContent = f.vessels.split(' \u00b7 ')[0]; svg.appendChild(b);
    });

    // annual scatter first, so the smoothed line sits on top of its own evidence
    order.forEach(function (k) {
      D.annual[k].forEach(function (p) {
        if (p.share == null || !p.n) return;
        svg.appendChild(el('circle', { cx: x(p.year), cy: y(p.share),
          r: Math.max(1.4, Math.min(4, Math.sqrt(p.n) * 0.62)),
          fill: SLOT[k], opacity: .2 }));
      });
    });

    var ends = [];
    order.forEach(function (k) {
      var seg = [], last = null;
      D.series[k].forEach(function (p) {
        if (p.share == null) { seg.push(null); return; }
        seg.push([x(p.year), y(p.share)]); last = p;
      });
      var dstr = '', pen = false;
      seg.forEach(function (pt) {
        if (!pt) { pen = false; return; }
        dstr += (pen ? 'L' : 'M') + pt[0].toFixed(1) + ',' + pt[1].toFixed(1); pen = true;
      });
      svg.appendChild(el('path', { d: dstr, class: 'g-line', stroke: SLOT[k] }));
      if (last) {
        svg.appendChild(el('circle', { cx: x(last.year), cy: y(last.share), r: 4.5,
          fill: SLOT[k], stroke: 'var(--surface-1)', 'stroke-width': 2 }));
        ends.push({ k: k, yy: y(last.share), xx: x(last.year), trueY: y(last.share),
                    text: lab[k] + '  ' + last.share + '%' });
      }
    });
    var GAP = 15;
    ends.sort(function (a, b) { return a.yy - b.yy; });
    for (var i = 1; i < ends.length; i++)
      if (ends[i].yy - ends[i - 1].yy < GAP) ends[i].yy = ends[i - 1].yy + GAP;
    var over = ends[ends.length - 1].yy - (MT + ph);
    if (over > 0) ends.forEach(function (e) { e.yy -= over; });
    ends.forEach(function (e) {
      if (Math.abs(e.trueY - e.yy) > 2)
        svg.appendChild(el('line', { x1: e.xx + 6, y1: e.trueY, x2: e.xx + 12, y2: e.yy,
          stroke: SLOT[e.k], 'stroke-width': 1, opacity: .55 }));
      var lt = el('text', { x: e.xx + 14, y: e.yy + 4, class: 'g-label', fill: SLOT[e.k] });
      lt.textContent = e.text; svg.appendChild(lt);
    });

    // annual denominator strip
    var maxN = Math.max.apply(null, years.map(function (yr) { return D.n_by_year[String(yr)] || 0; }));
    var st = el('text', { x: 0, y: STRIP_TOP - 8, class: 'g-axis-text' });
    st.setAttribute('fill', 'var(--text-muted)'); st.setAttribute('font-size', '10');
    st.textContent = 'records per year (n), peak ' + maxN; svg.appendChild(st);
    var bw = Math.max(2, pw / years.length - 2);
    years.forEach(function (yr) {
      var n = D.n_by_year[String(yr)] || 0;
      if (!n) return;
      var h = Math.max(1.5, (n / maxN) * STRIP_H);
      svg.appendChild(el('rect', { x: x(yr) - bw / 2, y: STRIP_TOP + (STRIP_H - h),
        width: bw, height: h, fill: 'var(--series-1)', opacity: .3, rx: 1 }));
    });
    var peakYear = years.reduce(function (a, b) {
      return (D.n_by_year[String(b)] || 0) > (D.n_by_year[String(a)] || 0) ? b : a; }, years[0]);
    var pk = el('text', { x: x(peakYear), y: STRIP_TOP + STRIP_H + 13, class: 'g-axis-text', 'text-anchor': 'middle' });
    pk.setAttribute('font-size', '10'); pk.setAttribute('fill', 'var(--text-secondary)');
    pk.textContent = peakYear + ': ' + maxN; svg.appendChild(pk);
    var gap = years.filter(function (yr) { return !(D.n_by_year[String(yr)] || 0); });
    if (gap.length) {
      var gt = el('text', { x: ML + pw, y: STRIP_TOP + STRIP_H + 30, class: 'g-axis-text', 'text-anchor': 'end' });
      gt.setAttribute('font-size', '10'); gt.setAttribute('fill', 'var(--text-muted)');
      gt.textContent = 'no records at all: ' + gap.join(', '); svg.appendChild(gt);
    }

    legend(order, lab);
    hover(svg, D, years, x, y, ML, MT, pw, ph);
    table(D);
    caveats(D);
  }

  function legend(order, lab) {
    document.getElementById('legend').innerHTML = order.filter(function (k) { return k !== 'other'; })
      .map(function (k) {
        return '<span><i style="background:' + SLOT[k] + '"></i>' + esc(lab[k]) +
               '<span style="opacity:.6;font-size:.9em">&nbsp;from ' + (window.__D.first_arrival[k] || '') + '</span></span>';
      }).join('') +
      '<span style="opacity:.75"><i style="background:var(--text-muted);height:7px;width:7px;border-radius:50%"></i>a single year</span>' +
      '<span style="opacity:.75"><i style="background:var(--text-secondary);height:7px;width:7px;border-radius:50%"></i>first visit under that flag</span>';
  }

  function hover(svg, D, years, x, y, ML, MT, pw, ph) {
    var tip = document.getElementById('tip');
    var cross = el('line', { y1: MT, y2: MT + ph, stroke: 'var(--text-muted)', 'stroke-width': 1, opacity: 0 });
    svg.appendChild(cross);
    var hit = el('rect', { x: ML, y: MT, width: pw, height: ph, fill: 'transparent' });
    svg.appendChild(hit);
    function show(evt) {
      var r = svg.getBoundingClientRect(), sx = (evt.clientX - r.left) * (900 / r.width);
      var yr = years.reduce(function (a, b) { return Math.abs(x(b) - sx) < Math.abs(x(a) - sx) ? b : a; }, years[0]);
      cross.setAttribute('x1', x(yr)); cross.setAttribute('x2', x(yr)); cross.setAttribute('opacity', .35);
      var n = D.n_by_year[String(yr)] || 0;
      var ev = (D.first_visits || []).filter(function (e) { return e.year === yr; })[0];
      var rows = D.order.filter(function (k) { return k !== 'other'; }).map(function (k) {
        var sm = D.series[k].filter(function (p) { return p.year === yr; })[0];
        var an = D.annual[k].filter(function (p) { return p.year === yr; })[0];
        return '<tr><td><i style="background:' + SLOT[k] + '"></i>' + esc(D.labels[k]) + '</td><td>' +
               (sm && sm.share != null ? sm.share + '%' : '—') +
               '<span class="muted"> (' + (an && an.n ? an.share + '% of ' + an.n : 'no records') + ')</span></td></tr>';
      }).join('');
      tip.innerHTML = '<b>' + yr + '</b><table>' + rows + '</table>' +
        (ev ? '<div style="margin-top:6px;padding-top:5px;border-top:1px solid var(--grid)">' +
              '<b>First visit under the flag of ' + esc(ev.label) + '</b><br>' +
              esc(ev.vessels) + ' \u00b7 ' + esc(ev.who) + '<br><span class="muted">' +
              esc(ev.date) + ', ' + esc(ev.place) + '<br>' + esc(ev.note) +
              '<br>attestation: ' + esc(ev.attestation) + '</span></div>' : '') +
        '<div class="muted" style="margin-top:5px">5-year mean, with that single year in brackets<br>n = ' + n + ' in ' + yr + '</div>';
      tip.style.opacity = 1;
      tip.style.left = Math.min(evt.pageX + 16, window.scrollX + document.documentElement.clientWidth - tip.offsetWidth - 10) + 'px';
      tip.style.top = (evt.pageY - 10) + 'px';
    }
    hit.addEventListener('mousemove', show);
    hit.addEventListener('mouseleave', function () { tip.style.opacity = 0; cross.setAttribute('opacity', 0); });
  }

  function table(D) {
    var ORD = D.order.filter(function (k) { return k !== 'other'; });
    var h = '<table><thead><tr><th>Year</th>' + ORD.map(function (k) { return '<th>' + esc(D.labels[k]) + '</th>'; }).join('') + '<th>n</th></tr></thead><tbody>';
    D.years.forEach(function (yr) {
      var n = D.n_by_year[String(yr)] || 0;
      h += '<tr><td>' + yr + '</td>';
      ORD.forEach(function (k) {
        var sm = D.series[k].filter(function (p) { return p.year === yr; })[0];
        var an = D.annual[k].filter(function (p) { return p.year === yr; })[0];
        h += '<td>' + (sm && sm.share != null ? sm.share + '%' : '<span class="muted">—</span>') +
             (an && an.n ? ' <span class="muted">(' + an.share + '%)</span>' : '') + '</td>';
      });
      h += '<td>' + (n || '<span class="muted">0</span>') + '</td></tr>';
    });
    h += '</tbody></table><p class="muted" style="font-size:.9em">Each cell gives the 5-year centred mean, with that single year’s own share in brackets. An em dash means the window held fewer than ' + D.min_window_n + ' records.</p>';
    document.getElementById('tableview').innerHTML = h;
  }

  function caveats(D) {
    document.getElementById('caveats').innerHTML =
      '<b>What this figure does not know.</b> ' + D.caveats.map(esc).join(' ');
  }
})();
