'use strict';
/* Delivery Insights - bảng điều khiển chạy trong trình duyệt.
   Dữ liệu là các khối đã tổng hợp từ data/dashboard/*.csv (xem scripts/build_dashboard_web.py);
   mọi con số được tính lại theo bộ lọc ở đây, không có số cố định. */
(function () {
const D = window.__DATA__;
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const cs = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const nz = v => v == null || Number.isNaN(v);
const pct = (v, d = 1) => nz(v) ? '–' : (v * 100).toFixed(d).replace('.', ',') + '%';
const num = v => nz(v) ? '–' : Math.round(v).toLocaleString('vi-VN');
const dec = (v, d = 2) => nz(v) ? '–' : v.toFixed(d).replace('.', ',');
const dec1 = v => nz(v) ? '–' : v.toLocaleString('vi-VN', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
const monthText = m => m.slice(5, 7) + '/' + m.slice(0, 4);
const hex = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
const toHex = a => '#' + a.map(v => Math.round(Math.max(0, Math.min(255, v))).toString(16).padStart(2, '0')).join('');
const mix = (a, b, t) => { t = Math.max(0, Math.min(1, t)); const A = hex(a), B = hex(b); return toHex(A.map((v, i) => v + (B[i] - v) * t)); };
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

const MODES = D.modes, MARKETS = D.markets, REG = D.regions, MONTHS = D.months, POL = D.policies, CASES = D.cases;
const POL_DEFAULT = (POL.find(p => p.id === 'bounded_plus1_keep_same_day') || POL[1]).id;
const CASE_DEFAULT = (CASES.find(c => c.id === 'c101|base|ortools') || CASES[0]).id;
const GLOBAL = (() => { let n = 0, late = 0; for (const r of D.A) { n += r[4]; late += r[5]; } return { n, late, rate: late / n }; })();
const AVG = GLOBAL.rate;

const S = { page: 'p1', mode: null, market: null, region: null, thr: 0.5, policy: POL_DEFAULT, cas: CASE_DEFAULT, km: 1, lit: 10, price: 22000, hover: null };
const iMode = () => S.mode == null ? null : MODES.indexOf(S.mode);
const iMkt = () => S.market == null ? null : MARKETS.indexOf(S.market);
const iReg = () => S.region == null ? null : REG.findIndex(r => r.name === S.region);
const fAll = () => ({ m: iMode(), k: iMkt(), r: iReg() });
const fX = () => ({ m: null, k: iMkt(), r: iReg() });
const fK = () => ({ m: null, k: null, r: iReg() });

/* ------------------------------------------------------------------ tổng hợp */
const ok = (r, f, o) => (f.m == null || r[o] === f.m) && (f.k == null || r[o + 1] === f.k) && (f.r == null || r[o + 2] === f.r);
function aggA(f) { let n = 0, late = 0, ss = 0, sa = 0; for (const r of D.A) if (ok(r, f, 0)) { n += r[4]; late += r[5]; ss += r[6]; sa += r[7]; } return { n, late, ss, sa }; }
function seriesA(f) { const o = MONTHS.map(() => ({ n: 0, late: 0, ss: 0, sa: 0 })); for (const r of D.A) if (ok(r, f, 0)) { const x = o[r[3]]; x.n += r[4]; x.late += r[5]; x.ss += r[6]; x.sa += r[7]; } return o; }
function aggB(f, thr) { let n = 0, late = 0, alerts = 0, tp = 0; for (const r of D.B) if (ok(r, f, 0)) { n += r[4]; late += r[5]; if (r[3] >= thr - 1e-9) { alerts += r[4]; tp += r[5]; } } return { n, late, alerts, tp, fp: alerts - tp, fn: late - tp }; }
function aggC(f, pi) { let n = 0, ex = 0, sp = 0, sa = 0, fb = 0; for (const r of D.C) if (r[0] === pi && ok(r, f, 1)) { n += r[4]; ex += r[5]; sp += r[6]; sa += r[7]; fb += r[8]; } return { n, ex, sp, sa, fb, rate: n ? ex / n : null, prop: n ? sp / n : null, add: n ? sa / n : null, fbr: n ? fb / n : null }; }

/* ------------------------------------------------------------------ vòng tiến độ */
function dial(id, val, color, uid, cap) {
  const el = document.getElementById(id), W = el.clientWidth || parseInt(el.style.width) || 300, cx = W / 2, cy = 107, R = 70, sw = 24, C = 2 * Math.PI * R;
  const v = nz(val) ? 0 : Math.max(0, Math.min(1, val)), a = 360 * v, ro = R + sw / 2, ri = R - sw / 2;
  let s = `<svg width="${W}" height="214" viewBox="0 0 ${W} 214"><defs>
   <linearGradient id="rg${uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${mix(color, '#ffffff', .42)}"/><stop offset=".5" stop-color="${color}"/><stop offset="1" stop-color="${mix(color, '#000000', .25)}"/></linearGradient>
   <radialGradient id="rk${uid}" cx=".35" cy=".3" r=".9"><stop offset="0" stop-color="${cs('--face1')}"/><stop offset="1" stop-color="${cs('--face2')}"/></radialGradient></defs>`;
  for (let i = 0; i < 40; i++) {
    const th = i * 9 * Math.PI / 180 - Math.PI / 2, major = i % 10 === 0, r1 = ro + 6, r2 = ro + (major ? 15 : i % 5 === 0 ? 11 : 9);
    s += `<line x1="${cx + r1 * Math.cos(th)}" y1="${cy + r1 * Math.sin(th)}" x2="${cx + r2 * Math.cos(th)}" y2="${cy + r2 * Math.sin(th)}" stroke="${cs('--ink2')}" stroke-width="${major ? 1.8 : 1}" opacity="${major ? .7 : .35}"/>`;
  }
  s += `<circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="${cs('--well1')}" stroke-width="${sw}"/>
   <circle cx="${cx}" cy="${cy}" r="${ro - 1}" fill="none" stroke="${cs('--lo')}" stroke-width="2.2" opacity=".55"/>
   <circle cx="${cx}" cy="${cy}" r="${ri + 1}" fill="none" stroke="${cs('--hi')}" stroke-width="2.2"/>`;
  if (v > 0) {
    s += `<g style="filter:drop-shadow(2px 3px 3px ${cs('--lo')})"><circle class="sweep" cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="url(#rg${uid})" stroke-width="${sw - 8}" stroke-linecap="round" transform="rotate(-90 ${cx} ${cy})" style="stroke-dasharray:${(C * v).toFixed(1)} ${C.toFixed(1)}"/></g>
   <circle class="sweep" cx="${cx}" cy="${cy}" r="${R + sw / 2 - 6}" fill="none" stroke="#fff" stroke-opacity=".38" stroke-width="1.4" stroke-linecap="round" transform="rotate(-90 ${cx} ${cy})" style="stroke-dasharray:${Math.max(0, 2 * Math.PI * (R + sw / 2 - 6) * v - 4).toFixed(1)} ${(2 * Math.PI * (R + sw / 2 - 6)).toFixed(1)}"/>`;
  }
  s += `<g class="knobg" style="transform-origin:${cx}px ${cy}px;transform:rotate(${a}deg)"><g style="filter:drop-shadow(3px 4px 3px ${cs('--lo')})"><circle cx="${cx}" cy="${cy - R}" r="${sw / 2 + 1}" fill="url(#rk${uid})"/></g><circle cx="${cx}" cy="${cy - R}" r="4" fill="${color}"/></g>
   <g style="filter:drop-shadow(5px 6px 6px ${cs('--lo')}) drop-shadow(-4px -4px 5px ${cs('--hi')})"><circle cx="${cx}" cy="${cy}" r="${ri - 9}" fill="url(#rk${uid})"/></g></svg>`;
  el.innerHTML = s + `<div class="rc"><b class="num" style="color:${color}">${pct(nz(val) ? null : val)}</b><span>${cap || ''}</span></div>`;
}
function spark(vals, color, w = 92, h = 32) {
  const pts = vals.map((v, i) => [i, v]).filter(p => !nz(p[1]));
  if (pts.length < 2) return '';
  const lo = Math.min(...pts.map(p => p[1])), hi = Math.max(...pts.map(p => p[1])), n = vals.length - 1;
  const x = i => 2 + i * (w - 4) / n, y = v => 3 + (hi - v) / (hi - lo || 1) * (h - 7);
  const d = pts.map((p, k) => (k ? 'L' : 'M') + x(p[0]).toFixed(1) + ' ' + y(p[1]).toFixed(1)).join('');
  const last = pts[pts.length - 1];
  return `<svg width="${w}" height="${h}"><path class="spl" pathLength="1" d="${d}" fill="none" stroke="${color}" stroke-width="1.7" stroke-linejoin="round"/><circle cx="${x(last[0])}" cy="${y(last[1])}" r="2.6" fill="${color}"/></svg>`;
}
function sphereDefs(prefix, items) {
  return items.map((c, i) => `<radialGradient id="${prefix}${i}" cx=".32" cy=".28" r=".85"><stop offset="0" stop-color="${mix(c, '#ffffff', .55)}"/><stop offset=".5" stop-color="${c}"/><stop offset="1" stop-color="${mix(c, '#000000', .38)}"/></radialGradient>`).join('');
}
function tileHTML(cls, c, name, big, unit, bd, lines, trackW, notch, extra = '') {
  return `<div class="raise tile ${cls}" style="--c:${c}" ${extra}>
   <div><div class="nm">${name}</div><div class="big num">${big}<small style="font-size:18px;font-weight:400;letter-spacing:0;margin-left:5px;opacity:.8">${unit}</small></div><div class="bd">${bd}</div></div>
   <div>${lines.map((l, i) => `<div class="ln" ${i === lines.length - 1 && trackW == null ? 'style="border:0"' : ''}><span>${l[0]}</span><b class="num">${l[1]}</b></div>`).join('')}
   ${trackW != null ? `<div class="track well"><i style="width:calc(${Math.max(0, Math.min(1, trackW)) * 100}% - 6px)"></i>${notch != null ? `<u style="left:${notch * 100}%"></u>` : ''}</div>` : ''}</div></div>`;
}
const barRow = (v, w, c, wd = 110) => `<span class="apb well" style="width:${wd}px"><i style="width:calc(${Math.max(0, Math.min(1, v / w)) * 100}% - 6px);background:linear-gradient(180deg,${mix(c, '#ffffff', .25)},${c})"></i></span><span class="apv num" style="width:52px">${pct(v)}</span>`;

/* ------------------------------------------------------------------ rail */
function renderRail() {
  $('#rn').textContent = num(GLOBAL.n); $('#rm').textContent = num(MONTHS.length); $('#rk').textContent = num(MARKETS.length);
  $('#rrate').textContent = pct(AVG); $('#rtube').style.height = `calc(${AVG * 100}% - 6px)`;
}

/* ------------------------------------------------------------------ 1. tổng quan */
function render1() {
  const red = cs('--red'), teal = cs('--teal'), steel = cs('--steel');
  const g = aggA(fAll()), tot = aggA(fX());
  $('#sub1').textContent = `DataCo · đơn không hủy · ${monthText(MONTHS[0])} – ${monthText(MONTHS[MONTHS.length - 1])} · ${num(g.n)} đơn`;
  const rate = g.n ? g.late / g.n : null;
  dial('dial1', rate, red, 'a', 'đơn giao trễ hạn');
  $('#ring1sub').textContent = S.mode || 'toàn bộ đơn';
  $('#f1a').innerHTML = `<b class="num">${num(g.late)}</b> đơn trễ`; $('#f1b').innerHTML = `<b class="num">${num(g.n - g.late)}</b> đúng hạn`;
  const per = MODES.map((name, i) => { const a = aggA({ m: i, k: iMkt(), r: iReg() }); return { name, i, ...a, rate: a.n ? a.late / a.n : null, sched: a.n ? a.ss / a.n : null, act: a.n ? a.sa / a.n : null, share: tot.late ? a.late / tot.late : null }; })
    .sort((a, b) => (b.rate ?? -1) - (a.rate ?? -1));
  $('#tiles').innerHTML = per.map(m => {
    const above = !nz(m.rate) && m.rate > AVG, hot = !nz(m.rate) && m.rate >= .95, c = above ? red : teal;
    return `<div class="raise tile ${hot ? 'hot' : ''}" data-mode="${m.name}" style="--c:${c}">
     <div><div class="nm">${m.name}</div><div class="big num">${nz(m.rate) ? '–' : pct(m.rate, m.rate === 1 ? 0 : 1)}</div><div class="bd">${nz(m.rate) ? 'KHÔNG CÓ ĐƠN' : above ? '▲ TRÊN TRUNG BÌNH' : '▼ DƯỚI TRUNG BÌNH'}</div></div>
     <div><div class="ln"><span>Cam kết → thực tế</span><b class="num">${nz(m.sched) ? '–' : dec(m.sched) + ' → ' + dec(m.act) + ' ngày'}</b></div>
      <div class="ln"><span>Đơn / đơn trễ</span><b class="num">${num(m.n)} / ${num(m.late)}</b></div>
      <div class="ln" style="border:0"><span>Chiếm tổng đơn trễ</span><b class="num">${pct(m.share)}</b></div>
      <div class="track well"><i style="width:calc(${(m.rate || 0) * 100}% - 6px)"></i><u style="left:${AVG * 100}%"></u></div></div></div>`;
  }).join('');
  /* bong bóng */
  const live = per.filter(m => m.n > 0);
  const W = 560, H = 176, L = 40, R = 16, T = 10, B = 22;
  const xmax = Math.max(10000, Math.ceil(Math.max(1, ...live.map(m => m.n)) * 1.12 / 10000) * 10000), ylo = Math.min(.2, Math.floor(Math.min(1, ...live.map(m => m.rate)) * 10) / 10 - .1), yhi = 1.04;
  const X = v => L + v / xmax * (W - L - R), Y = v => T + (yhi - v) / (yhi - ylo) * (H - T - B);
  const cols = live.map(m => m.rate > AVG ? red : teal);
  let b = `<svg viewBox="0 0 ${W} ${H}" width="100%" style="margin-top:4px"><defs>${sphereDefs('sp', cols)}</defs><rect x="${L}" y="${T}" width="${W - L - R}" height="${Math.max(0, Y(AVG) - T)}" fill="${red}" opacity=".08"/>`;
  [.25, .5, .75, 1].filter(v => v > ylo).forEach(v => b += `<line x1="${L}" x2="${W - R}" y1="${Y(v)}" y2="${Y(v)}" stroke="${cs('--rule')}"/><text x="${L - 6}" y="${Y(v) + 3.5}" text-anchor="end" font-size="10" fill="${cs('--muted')}">${v * 100}%</text>`);
  for (let v = 0; v <= xmax; v += 10000) b += `<text x="${X(v)}" y="${H - 6}" text-anchor="middle" font-size="10" fill="${cs('--muted')}">${v ? num(v) : '0'}</text>`;
  b += `<line x1="${L}" x2="${W - R}" y1="${Y(AVG)}" y2="${Y(AVG)}" stroke="${cs('--ink')}" stroke-dasharray="4 4" opacity=".45"/><text x="${W - R}" y="${Y(AVG) - 4}" text-anchor="end" font-size="10" fill="${cs('--ink2')}">trung bình toàn kỳ ${pct(AVG)}</text>`;
  live.forEach((m, i) => {
    const r = 7 + Math.sqrt(m.late) / Math.sqrt(Math.max(1, ...live.map(q => q.late))) * 15, left = m.n > xmax * .72 || m.rate > .95, lx = X(m.n) + (left ? -r - 7 : r + 7), an = left ? 'end' : 'start';
    b += `<g class="bb" data-mode="${m.name}" data-tip="<b>${m.name}</b><br>Tỷ lệ trễ ${pct(m.rate)}<br>${num(m.n)} đơn · ${num(m.late)} trễ<br>Cam kết ${dec(m.sched)} → thực tế ${dec(m.act)} ngày"><g style="filter:drop-shadow(3px 4px 3px ${cs('--lo')})"><circle cx="${X(m.n)}" cy="${Y(m.rate)}" r="${r}" fill="url(#sp${i})"/></g>
     <text x="${lx}" y="${Y(m.rate) - 1}" text-anchor="${an}" font-size="11.5" font-weight="650" fill="${cs('--ink')}">${m.name}</text><text x="${lx}" y="${Y(m.rate) + 11}" text-anchor="${an}" font-size="10.5" fill="${cs('--muted')}">${num(m.late)} đơn trễ</text></g>`;
  });
  $('#bubble').innerHTML = live.length ? b + '</svg>' : '<div class="nodata">Không có đơn ở bộ lọc này</div>';
  /* phím nhiệt */
  const shortName = { 'Pacific Asia': 'P. Asia' };
  let k = '<div></div>' + MARKETS.map(c => `<div class="hd" data-col="${c}">${shortName[c] || c}</div>`).join('');
  per.forEach(m => {
    k += `<div class="rl" data-mode="${m.name}">${m.name}</div>`;
    MARKETS.forEach((c, ci) => {
      const a = aggA({ m: m.i, k: ci, r: iReg() }), v = a.n ? a.late / a.n : null, base = cs('--face1');
      if (v == null) { k += `<div class="kk num" data-mode="${m.name}" data-col="${c}" style="background:${cs('--well1')};color:${cs('--muted')}">–</div>`; return; }
      const col = v < AVG ? mix(base, teal, (AVG - v) / (AVG - .38) * .85) : mix(base, red, (v - AVG) / (1 - AVG) * .95), strong = v > .7 || v < .45;
      k += `<div class="kk num" data-mode="${m.name}" data-col="${c}" data-tip="<b>${m.name} · ${c}</b><br>Tỷ lệ trễ ${pct(v)}<br>${num(a.n)} đơn" style="background:linear-gradient(145deg,${mix(col, '#ffffff', .18)},${mix(col, '#000000', .1)});color:${strong ? '#fff' : cs('--ink')}">${(v * 100).toFixed(0)}%</div>`;
    });
  });
  $('#keypad').innerHTML = k;
  $('#lgbar').style.background = `linear-gradient(90deg,${teal},${cs('--face1')},${red})`;
  /* nhịp độ theo tháng */
  const ser = seriesA(fAll()), valid = ser.filter(x => x.n > 0).length || 1;
  const rows = [['Đơn mỗi tháng', num(g.n / valid), '', ser.map(x => x.n || null), steel, v => num(v)],
    ['Giao thực tế trung bình', dec(g.n ? g.sa / g.n : null), 'ngày', ser.map(x => x.n ? x.sa / x.n : null), teal, v => dec(v)],
    ['Chênh so với cam kết', g.n ? (g.sa - g.ss) / g.n >= 0 ? '+' + dec((g.sa - g.ss) / g.n) : dec((g.sa - g.ss) / g.n) : '–', 'ngày', ser.map(x => x.n ? (x.sa - x.ss) / x.n : null), red, v => dec(v)]];
  const range = (a, f) => { const z = a.filter(v => !nz(v)); return z.length ? `${f(Math.min(...z))} – ${f(Math.max(...z))}` : '–'; };
  $('#kpis').innerHTML = `<h3>Nhịp độ theo tháng</h3><div class="sub" style="margin-bottom:2px">trung bình theo bộ lọc · đường nhỏ là ${MONTHS.length} tháng</div>` +
    rows.map(r => `<div class="eng"><div><span>${r[0]}</span><b class="num">${r[1]}<small>${r[2]}</small></b></div><div class="sp">${spark(r[3], r[4])}<small>${range(r[3], r[5])}</small></div></div>`).join('');
  /* xu hướng */
  const pts = ser.map((x, i) => x.n ? { i, v: x.late / x.n, n: x.n, act: x.sa / x.n, gap: (x.sa - x.ss) / x.n } : null).filter(Boolean);
  const w = 1228, hh = 150, Lm = 40, Rm = 10, Tm = 12, Bm = 20;
  if (pts.length < 2) { $('#trend').innerHTML = '<div class="nodata">Không đủ dữ liệu để vẽ xu hướng</div>'; window.__tr = null; }
  else {
    const mn = Math.min(...pts.map(p => p.v)), mxv = Math.max(...pts.map(p => p.v));
    let lo = Math.max(0, Math.floor((mn - .01) * 50) / 50), hi = Math.min(1, Math.ceil((mxv + .01) * 50) / 50);
    if (hi - lo < .08) { const mid = (hi + lo) / 2; lo = Math.max(0, mid - .04); hi = Math.min(1, mid + .04); }
    const step = (w - Lm - Rm) / (MONTHS.length - 1), Xt = i => Lm + i * step, Yt = v => Tm + (hi - v) / (hi - lo) * (hh - Tm - Bm);
    let t = `<svg viewBox="0 0 ${w} ${hh}" width="100%"><defs><linearGradient id="ar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${steel}" stop-opacity=".35"/><stop offset="1" stop-color="${steel}" stop-opacity="0"/></linearGradient></defs>`;
    for (let q = 0; q <= 3; q++) { const v = lo + (hi - lo) * q / 3; t += `<line x1="${Lm}" x2="${w - Rm}" y1="${Yt(v)}" y2="${Yt(v)}" stroke="${cs('--rule')}"/><text x="${Lm - 6}" y="${Yt(v) + 3.5}" text-anchor="end" font-size="10" fill="${cs('--muted')}">${(v * 100).toFixed(0)}%</text>`; }
    const path = pts.map((p, q) => (q ? 'L' : 'M') + Xt(p.i).toFixed(1) + ' ' + Yt(p.v).toFixed(1)).join('');
    t += `<path d="${path}L${Xt(pts[pts.length - 1].i)} ${Yt(lo)}L${Xt(pts[0].i)} ${Yt(lo)}Z" fill="url(#ar)"/>`;
    if (AVG >= lo && AVG <= hi) t += `<line x1="${Lm}" x2="${w - Rm}" y1="${Yt(AVG)}" y2="${Yt(AVG)}" stroke="${cs('--ink')}" stroke-dasharray="4 4" opacity=".4"/>`;
    t += `<path class="spl" pathLength="1" d="${path}" fill="none" stroke="${cs('--ink')}" stroke-width="2.2" stroke-linejoin="round" style="filter:drop-shadow(0 2px 2px ${cs('--lo')})"/>`;
    [0, 12, 24, 36].filter(i => i < MONTHS.length).forEach(i => { t += `<line x1="${Xt(i)}" x2="${Xt(i)}" y1="${Tm}" y2="${hh - Bm}" stroke="${cs('--rule')}" stroke-dasharray="2 4"/><text x="${Xt(i)}" y="${hh - 4}" text-anchor="${i === MONTHS.length - 1 ? 'end' : i === 0 ? 'start' : 'middle'}" font-size="10" fill="${cs('--muted')}">${MONTHS[i]}</text>`; });
    const hiP = pts.reduce((a, p) => p.v > a.v ? p : a), loP = pts.reduce((a, p) => p.v < a.v ? p : a);
    [[hiP, 'cao nhất', -10], [loP, 'thấp nhất', 17]].forEach(([p, nme, dy]) => { t += `<circle cx="${Xt(p.i)}" cy="${Yt(p.v)}" r="5" fill="${red}" stroke="${cs('--face1')}" stroke-width="2"/><text x="${Xt(p.i)}" y="${Yt(p.v) + dy}" text-anchor="middle" font-size="11" font-weight="650" fill="${red}">${pct(p.v)} ${nme}</text>`; });
    const lp = pts[pts.length - 1]; t += `<text x="${Xt(lp.i) - 8}" y="${Yt(lp.v) - 9}" text-anchor="end" font-size="10.5" fill="${cs('--ink2')}">gần nhất ${pct(lp.v)}</text>`;
    t += `<g id="xh" style="opacity:0;transition:opacity .15s"><line id="xhl" y1="${Tm}" y2="${hh - Bm}" stroke="${red}" stroke-width="1.2"/><circle id="xhc" r="5.5" fill="${red}" stroke="${cs('--face1')}" stroke-width="2"/></g>`;
    window.__tr = { w, hh, Lm, Rm, Tm, Bm, lo, hi, step, pts };
    $('#trend').innerHTML = t + '</svg>';
    $('#trendsub').textContent = `trục thu hẹp ${(lo * 100).toFixed(0)}–${(hi * 100).toFixed(0)}% · vạch đứt là trung bình toàn kỳ ${pct(AVG)}`;
  }
  /* kết luận */
  const liveR = per.filter(m => m.n > 0), byLate = [...liveR].sort((a, b) => b.late - a.late);
  $('#tape1').textContent = !g.n ? 'Không có đơn ở bộ lọc đang chọn.' : liveR.length < 2
    ? `${liveR[0].name}: ${pct(liveR[0].rate)} đơn giao trễ (${num(liveR[0].late)} / ${num(liveR[0].n)}).`
    : `${liveR[0].name} có tỷ lệ trễ cao nhất (${pct(liveR[0].rate)}); ${byLate[0].name} có nhiều đơn trễ nhất (${pct(byLate[0].share)} số đơn trễ).`;
}

/* ------------------------------------------------------------------ 2. rủi ro */
function render2() {
  const red = cs('--red'), teal = cs('--teal'), brass = cs('--brass'), steel = cs('--steel');
  const a = aggB(fAll(), S.thr), tot = aggB(fX(), S.thr);
  $('#sub2').textContent = `Tập kiểm tra · ${num(a.n)} đơn · ${monthText(D.testRange[0])} – ${monthText(D.testRange[1])} · ngưỡng cảnh báo ${dec(S.thr)}`;
  const precision = a.alerts ? a.tp / a.alerts : null, recall = a.late ? a.tp / a.late : null;
  dial('dial2', precision, teal, 'b', 'đúng trong số cảnh báo'); dial('dial3', recall, red, 'c', 'bắt được trong đơn trễ');
  $('#f2a').innerHTML = `<b class="num">${num(a.tp)}</b> đúng`; $('#f2b').innerHTML = `<b class="num">${num(a.alerts)}</b> được báo`;
  $('#f3a').innerHTML = `<b class="num">${num(a.tp)}</b> bắt được`; $('#f3b').innerHTML = `<b class="num">${num(a.late)}</b> đơn trễ`;
  $('#funsub').textContent = `Từ toàn bộ đơn kiểm tra đến cảnh báo đúng · thêm ${num(a.fp)} cảnh báo sai`;
  const F = [[num(a.n), 'đơn kiểm tra', a.n, steel], [num(a.late), 'đơn trễ thực tế', a.late, brass], [num(a.tp), 'cảnh báo đúng', a.tp, teal], [num(a.fn), 'bỏ sót', a.fn, red]];
  $('#funnel').innerHTML = F.map(f => `<div class="fn"><div class="t"><b class="num">${f[0]}</b>${f[1]}</div><div class="track well" data-tip="<b>${f[1]}</b><br>${f[0]} đơn · ${pct(a.n ? f[2] / a.n : null)} số đơn kiểm tra" style="--c:${f[3]};height:26px;margin:0;border-radius:9px"><i style="width:calc(${a.n ? f[2] / a.n * 100 : 0}% - 6px);top:4px;bottom:4px;border-radius:6px"></i><span class="fp num" style="color:${f[3] === steel || f[3] === brass ? '#1D2A33' : '#fff'}">${pct(a.n ? f[2] / a.n : null)}</span></div></div>`).join('');
  [[a.tp, 's1'], [a.fp, 's2'], [a.fn, 's3'], [a.late, 's4']].forEach(([v, id], i) => { $('#c' + (i + 1)).textContent = num(v); $('#' + id).innerHTML = `${pct(a.n ? v / a.n : null)}<br>tổng đơn kiểm tra`; });
  $('#stkleg').innerHTML = [['Cảnh báo đúng', teal], ['Cảnh báo sai', brass], ['Bỏ sót', red]].map(x => `<span style="margin-left:14px"><i style="display:inline-block;width:10px;height:10px;border-radius:3px;background:${x[1]};margin-right:5px;vertical-align:-1px"></i>${x[0]}</span>`).join('');
  const st = MODES.map((name, i) => { const q = aggB({ m: i, k: iMkt(), r: iReg() }, S.thr); return { name, tp: q.tp, fp: q.fp, fn: q.fn, total: q.tp + q.fp + q.fn }; }).filter(x => x.total > 0).sort((p, q) => q.total - p.total);
  const mx = Math.max(1, ...st.map(x => x.total));
  $('#stack').innerHTML = st.length ? st.map(x => `<div class="fn" data-mode="${x.name}" style="grid-template-columns:120px 1fr;margin-top:24px"><div class="t"><b style="font-size:13.5px">${x.name}</b></div>
   <div class="well" style="height:44px;border-radius:12px;padding:6px;display:flex;gap:3px">${[[x.tp, teal, 'Cảnh báo đúng'], [x.fp, brass, 'Cảnh báo sai'], [x.fn, red, 'Bỏ sót']].filter(z => z[0]).map(([v, kc, lb]) => `<i class="num gw" data-tip="<b>${x.name}</b><br>${lb}: ${num(v)} đơn" style="height:32px;width:${v / mx * 100}%;min-width:44px;border-radius:8px;display:grid;place-items:center;color:#fff;font-style:normal;font-weight:700;font-size:12px;background:linear-gradient(180deg,${mix(kc, '#ffffff', .25)},${kc} 55%,${mix(kc, '#000000', .2)});box-shadow:2px 3px 5px ${cs('--lo')},inset 0 1px 0 rgba(255,255,255,.4)">${num(v)}</i>`).join('')}</div></div>`).join('') : '<div class="nodata">Không có đơn kiểm tra ở bộ lọc này</div>';
  const bestAp = Math.max(...D.models.map(m => m.ap));
  $('#models').innerHTML = `<table class="table" style="margin-top:8px"><tr><th>Mô hình</th><th>ROC-AUC</th><th style="text-align:left;padding-left:12px">AP</th><th>Log loss</th></tr>` +
    D.models.map(m => `<tr><td>${m.label}</td><td class="num">${dec(m.auc, 3)}</td><td style="text-align:left"><span class="apb well" style="width:104px"><i style="width:calc(${m.ap * 100}% - 6px)"></i></span><span class="apv num" style="${m.ap === bestAp ? '' : 'font-weight:500'}">${dec(m.ap, 3)}</span></td><td class="num">${dec(m.ll, 3)}</td></tr>`).join('') + '</table>';
  const worst = st.length ? [...st].sort((p, q) => q.fn - p.fn)[0] : null;
  $('#tape2').textContent = !a.alerts ? 'Không có cảnh báo ở ngưỡng đang chọn.'
    : `Cảnh báo đúng ${pct(precision)} nhưng chỉ bắt được ${pct(recall)} đơn trễ; ${num(a.fn)} đơn trễ chưa được báo${worst && worst.fn > 0 && st.length > 1 ? `, nhiều nhất ở ${worst.name} (${num(worst.fn)})` : ''}.`;
}

/* ------------------------------------------------------------------ 3. cam kết */
function render3() {
  const red = cs('--red'), teal = cs('--teal'), brass = cs('--brass'), steel = cs('--steel');
  const curI = POL.findIndex(p => p.id === 'current'), selI = POL.findIndex(p => p.id === S.policy), sel = POL[selI];
  const fa = fAll(), cur = aggC(fa, curI), sl = aggC(fa, selI), cut = nz(cur.rate) || nz(sl.rate) ? null : cur.rate - sl.rate;
  $('#sub3').textContent = `Mô phỏng · ${num(sl.n)} đơn kiểm tra · giữ nguyên thời gian giao thực tế`;
  $('#selname').textContent = sel.label;
  dial('dial4', sl.rate, red, 'd', 'đơn vượt hẹn tính lại');
  $('#f4a').innerHTML = `hiện tại <b class="num">${pct(cur.rate)}</b>`; $('#f4b').innerHTML = `<b class="num">${num(sl.ex)}</b> đơn vượt hẹn`;
  const sdI = MODES.indexOf('Same Day'), sdA = aggC({ m: sdI, k: iMkt(), r: iReg() }, selI);
  let oSa = 0, oN = 0; MODES.forEach((_, i) => { if (i !== sdI) { const q = aggC({ m: i, k: iMkt(), r: iReg() }, selI); oSa += q.sa; oN += q.n; } });
  const oth = oN ? oSa / oN : null;
  const byMode = MODES.map((name, i) => ({ name, i, c: aggC({ m: i, k: iMkt(), r: iReg() }, curI), s: aggC({ m: i, k: iMkt(), r: iReg() }, selI) }));
  const worstGrp = [...byMode].filter(m => m.s.n > 0).sort((p, q) => q.s.rate - p.s.rate)[0];
  $('#ptiles').innerHTML =
    tileHTML('good', teal, 'Giảm vượt hẹn', nz(cut) ? '–' : (cut >= 0 ? '' : '+') + dec(Math.abs(cut) * 100, 1), 'điểm %', cut >= 0 ? '▼ SO VỚI HIỆN TẠI' : '▲ SO VỚI HIỆN TẠI', [['Hiện tại', pct(cur.rate)], ['Phương án', pct(sl.rate)], ['Đơn hết vượt hẹn', num(cur.ex - sl.ex)]], sl.rate, cur.rate) +
    tileHTML('', steel, 'Cam kết mới (TB)', dec(sl.prop), 'ngày', '▲ TĂNG CAM KẾT', [['Hiện tại', dec(cur.prop) + ' ngày'], ['Phương án', dec(sl.prop) + ' ngày'], ['Dùng dự phòng', pct(sl.fbr)]], null) +
    tileHTML('', brass, 'Khách chờ thêm', (sl.add > 0 ? '+' : '') + dec(sl.add), 'ngày', '▲ CHI PHÍ PHƯƠNG ÁN', [['Same Day', sdA.add ? '+' + dec(sdA.add) + ' ngày' : 'giữ nguyên'], ['Ba phương thức còn lại', oth ? '+' + dec(oth) + ' ngày' : 'giữ nguyên'], ['Thời gian giao thực tế', 'không đổi']], null) +
    tileHTML('', steel, 'Đơn trễ thực tế', num(cur.ex), '', 'TẬP KIỂM TRA', [['Giai đoạn', `${monthText(D.testRange[0])} – ${monthText(D.testRange[1])}`], ['Nhóm vượt hẹn cao nhất', worstGrp ? worstGrp.name : '–'], ['Đơn mô phỏng', num(sl.n)]], null);
  /* đánh đổi */
  const all = POL.map((p, i) => ({ p, a: aggC(fa, i), i })).filter(x => x.a.n > 0);
  const groups = []; all.forEach(x => { const g = groups.find(q => Math.abs(q.a.rate - x.a.rate) < 1e-6 && Math.abs(q.a.add - x.a.add) < 1e-6); if (g) g.members.push(x); else groups.push({ a: x.a, members: [x] }); });
  const W = 500, H = 176, L = 44, R = 120, T = 12, B = 26, xmax = Math.max(1, ...all.map(x => x.a.add)) * 1.1, ymax = Math.max(.1, ...all.map(x => x.a.rate)) * 1.1;
  const X = v => L + 22 + v / xmax * (W - L - R - 22), Y = v => T + (ymax - v) / ymax * (H - T - B);
  const colr = r => r > .4 ? red : r > .1 ? brass : teal;
  let s = `<svg viewBox="0 0 ${W} ${H}" width="100%" style="margin-top:6px"><defs>${sphereDefs('tp', groups.map(g => colr(g.a.rate)))}</defs>`;
  [0, .25, .5, .75, 1].map(f => f * ymax).forEach(v => s += `<line x1="${L}" x2="${W - R + 30}" y1="${Y(v)}" y2="${Y(v)}" stroke="${cs('--rule')}"/><text x="${L - 6}" y="${Y(v) + 3.5}" text-anchor="end" font-size="10" fill="${cs('--muted')}">${(v * 100).toFixed(0)}%</text>`);
  for (let v = 0; v <= xmax; v += 1) s += `<text x="${X(v)}" y="${H - 8}" text-anchor="middle" font-size="10" fill="${cs('--muted')}">+${v} ngày</text>`;
  const sorted = [...groups].sort((p, q) => p.a.add - q.a.add);
  s += `<path d="${sorted.map((g, i) => (i ? 'L' : 'M') + X(g.a.add).toFixed(1) + ' ' + Y(g.a.rate).toFixed(1)).join('')}" fill="none" stroke="${cs('--ink')}" stroke-dasharray="3 5" opacity=".35"/>`;
  groups.forEach((g, i) => {
    const x = X(g.a.add), y = Y(g.a.rate), isSel = g.members.some(m => m.i === selI), r = isSel ? 13 : 10, below = sorted.length >= 3 && sorted.indexOf(g) === sorted.length - 2, names = g.members.map(m => m.p.label.replace(/ đúng hẹn$/, '')), nm = names[0] + names.slice(1).map(n => ' / ' + (n.replace(/^\D+/, '') || n)).join('');
    s += (isSel ? `<circle cx="${x}" cy="${y}" r="${r + 6}" fill="none" stroke="${cs('--ink')}" stroke-width="1.5" stroke-dasharray="2 3" opacity=".6"/>` : '') +
      `<g class="sb" data-tip="<b>${esc(nm)}</b><br>Vượt hẹn ${pct(g.a.rate)}<br>Cam kết ${dec(g.a.prop)} ngày (+${dec(g.a.add)})"><g style="filter:drop-shadow(3px 4px 3px ${cs('--lo')})"><circle cx="${x}" cy="${y}" r="${r}" fill="url(#tp${i})"/></g>
      <text x="${below ? x - r - 6 : x + r + 8}" y="${below ? y - 14 : y - 1}" text-anchor="${below ? 'end' : 'start'}" font-size="11.5" font-weight="650" fill="${cs('--ink')}">${esc(nm)}</text><text x="${below ? x - r - 6 : x + r + 8}" y="${below ? y - 2 : y + 11}" text-anchor="${below ? 'end' : 'start'}" font-size="10.5" fill="${cs('--muted')}">${pct(g.a.rate)} · +${dec(g.a.add)} ngày</text></g>`;
  });
  $('#trade').innerHTML = all.length ? s + '</svg>' : '<div class="nodata">Không có đơn ở bộ lọc này</div>';
  /* bảng phương án */
  $('#poltable').innerHTML = `<table class="table cp"><tr><th>Phương án</th><th style="text-align:left;padding-left:12px">Vượt hẹn tính lại</th><th>Cam kết TB</th><th>Tăng thêm</th></tr>` +
    POL.map((p, i) => { const q = aggC(fa, i), on = i === selI; return `<tr class="clickrow ${on ? 'selrow' : ''}" data-pol="${p.id}"><td>${p.label}${on ? ' <span style="font-size:10px;font-weight:700;color:var(--red);letter-spacing:.06em;margin-left:6px">ĐANG XEM</span>' : ''}</td><td style="text-align:left;padding-left:12px">${barRow(q.rate || 0, Math.max(.001, ymax / 1.1 * 1.02), colr(q.rate || 0))}</td><td class="num">${dec(q.prop)} ngày</td><td class="num">${q.add ? '+' + dec(q.add) + ' ngày' : '—'}</td></tr>`; }).join('') + '</table>';
  $('#modetable').innerHTML = `<table class="table cp"><tr><th>Phương thức</th><th style="text-align:left;padding-left:12px">Vượt hẹn hiện tại</th><th style="text-align:left;padding-left:12px">Vượt hẹn phương án</th><th>Cam kết hiện tại</th><th>Cam kết mới</th><th>Tăng thêm</th></tr>` +
    [...byMode].sort((p, q) => (q.c.rate ?? -1) - (p.c.rate ?? -1)).map(m => `<tr data-mode="${m.name}"><td><b style="font-weight:600">${m.name}</b></td><td style="text-align:left;padding-left:12px">${barRow(m.c.rate || 0, 1.02, red)}</td><td style="text-align:left;padding-left:12px">${barRow(m.s.rate || 0, 1.02, (m.s.rate || 0) > .5 ? red : (m.s.rate || 0) > .1 ? brass : teal)}</td><td class="num">${dec(m.c.prop)} ngày</td><td class="num">${dec(m.s.prop)} ngày</td><td class="num">${m.s.add ? '+' + dec(m.s.add) + ' ngày' : '—'}</td></tr>`).join('') + '</table>';
  $('#tape3').textContent = !sl.n ? 'Không có đơn ở bộ lọc đang chọn.' : S.policy === 'current'
    ? `Đang xem phương án hiện tại (${pct(cur.rate)} đơn vượt hẹn); chọn một phương án khác để so sánh đánh đổi.`
    : `${sel.label} đưa tỷ lệ vượt hẹn từ ${pct(cur.rate)} xuống ${pct(sl.rate)} (${nz(cut) ? '' : (cut >= 0 ? '−' : '+') + dec(Math.abs(cut) * 100, 1) + ' điểm %'}), đổi lại khách chờ thêm trung bình ${dec(sl.add)} ngày; đây là đổi cam kết, thời gian giao thực tế không đổi.`;
}

/* ------------------------------------------------------------------ 4. tuyến giao */
const PALETTE = ['#D2472A', '#0E7C86', '#B8860B', '#4A6FB5', '#9B59B6', '#3E9B55', '#D17B2C', '#C23B7A', '#6B7A8F', '#2E9CA6'];
const configKey = c => c.instance + '|' + c.scenario;
function caseOf(key, method) { return CASES.find(c => configKey(c) === key && c.method === method); }
function render4() {
  const red = cs('--red'), teal = cs('--teal'), brass = cs('--brass'), steel = cs('--steel'), dark = document.documentElement.dataset.theme === 'dark';
  const c = CASES.find(x => x.id === S.cas), ci = CASES.indexOf(c), ok1 = c.status === 'feasible';
  const key = configKey(c), orC = caseOf(key, 'ortools'), ngC = caseOf(key, 'nearest_feasible');
  const fe = x => x && x.status === 'feasible';
  const dist = ok1 ? c.dist : null, fuel = ok1 ? dist * S.km * S.lit / 100 * S.price : null;
  const red4 = ok1 && fe(ngC) ? (ngC.dist - c.dist) / ngC.dist : null;
  const tileV = (cls, col, name, big, unit, bd, lines) => tileHTML('v ' + cls, col, name, big, unit, bd, lines, null);
  $('#rtiles1').innerHTML =
    tileV('', brass, 'Nhiên liệu mô phỏng', ok1 ? num(fuel) : 'Chưa có', ok1 ? 'VND' : '', 'GIẢ ĐỊNH, KHÔNG PHẢI SỐ ĐO', [['Tiêu hao', S.lit + ' lít / 100 km'], ['Giá nhiên liệu', num(S.price) + ' VND / lít'], ['Quy đổi', dec(S.km, 1) + ' km / đơn vị']]) +
    tileV('', steel, 'Xe sử dụng', ok1 ? num(c.veh) : 'Chưa có', ok1 ? 'xe' : '', 'XE TRONG PHƯƠNG ÁN', [['Tải trọng', num(c.cap) + ' / xe'], ['Giới hạn', num(c.maxv) + ' xe']]);
  $('#rtiles2').innerHTML =
    tileV('', steel, 'Quãng đường chuẩn', ok1 ? dec(c.dist) : 'Chưa có', '', 'ĐƠN VỊ TỌA ĐỘ SOLOMON', [['Lưu ý', 'không phải km đường bộ']]) +
    tileV('good', teal, 'Giảm quãng đường', nz(red4) ? 'Chưa có' : dec(red4 * 100, 1), nz(red4) ? '' : '%', '▼ SO VỚI ĐIỂM GẦN NHẤT', [['Đối chứng', fe(ngC) ? 'cùng cấu hình' : 'chưa có lời giải khả thi']]);
  /* bản đồ */
  const stops = D.stops[ci] || [];
  if (!ok1 || !stops.length) { $('#rmap').innerHTML = '<div class="nodata">Chưa tìm được lời giải khả thi cho phương án này.<br>Không quy kết quả thiếu thành quãng đường bằng 0.</div>'; }
  else {
    const xs = stops.map(s => s[3]), ys = stops.map(s => s[4]), mnx = Math.min(...xs), mxx = Math.max(...xs), mny = Math.min(...ys), mxy = Math.max(...ys);
    const MW = 608, MH = 372, pad = 22, sc = Math.min((MW - 2 * pad) / (mxx - mnx || 1), (MH - 2 * pad) / (mxy - mny || 1)), ox = (MW - (mxx - mnx) * sc) / 2, oy = (MH - (mxy - mny) * sc) / 2;
    const MX = x => ox + (x - mnx) * sc, MY = y => MH - (oy + (y - mny) * sc);
    const pal = PALETTE.map(p => dark ? mix(p, '#ffffff', .28) : p), veh = {};
    stops.forEach(s => { (veh[s[0]] = veh[s[0]] || []).push(s); });
    let m = `<svg viewBox="0 0 ${MW} ${MH}" width="100%" height="100%">`;
    for (let g = 0; g <= 100; g += 10) m += `<line x1="${MX(g)}" x2="${MX(g)}" y1="0" y2="${MH}" stroke="${cs('--rule')}" stroke-width=".6" opacity=".7"/><line x1="0" x2="${MW}" y1="${MY(g)}" y2="${MY(g)}" stroke="${cs('--rule')}" stroke-width=".6" opacity=".7"/>`;
    Object.keys(veh).map(Number).sort((p, q) => p - q).forEach((v, i) => {
      const pts = veh[v].sort((p, q) => p[1] - q[1]), col = pal[i % pal.length]; let dd = 0;
      for (let k = 1; k < pts.length; k++) dd += Math.hypot(pts[k][3] - pts[k - 1][3], pts[k][4] - pts[k - 1][4]);
      m += `<g class="vh" data-veh="${v}" data-tip="<b>Xe ${v}</b><br>${pts.length - 2} điểm giao<br>Quãng đường ${dec1(dd)} đơn vị"><polyline class="spl" pathLength="1" points="${pts.map(p => MX(p[3]).toFixed(1) + ',' + MY(p[4]).toFixed(1)).join(' ')}" fill="none" stroke="${col}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" opacity=".92" style="filter:drop-shadow(1px 2px 1.5px ${cs('--lo')})"/>`;
      pts.forEach(p => { if (p[2] !== 0) m += `<circle cx="${MX(p[3])}" cy="${MY(p[4])}" r="3.2" fill="${col}" stroke="${cs('--face1')}" stroke-width="1"/>`; });
      const f = pts[1] || pts[0]; m += `<g><circle cx="${MX(f[3])}" cy="${MY(f[4]) - 11}" r="7.5" fill="${col}"/><text x="${MX(f[3])}" y="${MY(f[4]) - 7.6}" text-anchor="middle" font-size="9.5" font-weight="700" fill="#fff">${v}</text></g></g>`;
    });
    const dp = stops.find(s => s[2] === 0);
    m += `<g style="filter:drop-shadow(2px 3px 2px ${cs('--lo')})"><rect x="${MX(dp[3]) - 8}" y="${MY(dp[4]) - 8}" width="16" height="16" rx="3.5" fill="${cs('--ink')}"/></g><text x="${MX(dp[3])}" y="${MY(dp[4]) + 3.8}" text-anchor="middle" font-size="9.5" font-weight="700" fill="${cs('--face1')}">K</text>`;
    $('#rmap').innerHTML = m + '</svg>';
  }
  /* so sánh cùng cấu hình */
  const rowsCmp = [['Điểm gần nhất', ngC, red], ['OR Tools', orC, teal]], mxd = Math.max(1, ...rowsCmp.filter(r => fe(r[1])).map(r => r[1].dist));
  $('#rcmp').innerHTML = rowsCmp.map(r => `<div class="fn" style="grid-template-columns:110px 1fr;margin-top:16px"><div class="t"><b class="num">${fe(r[1]) ? dec1(r[1].dist) : 'Chưa có'}</b>${r[0]}<br><span style="font-size:11px;color:var(--muted)">${fe(r[1]) ? r[1].veh + ' xe' : 'chưa có lời giải'}</span></div>
    <div class="track well" style="--c:${r[2]};height:30px;margin:0;border-radius:10px"><i style="width:calc(${fe(r[1]) ? r[1].dist / mxd * 100 : 0}% - 6px);top:4px;bottom:4px;border-radius:7px"></i></div></div>`).join('') +
    `<div class="callout2">${fe(orC) && fe(ngC) ? `OR Tools ngắn hơn <b class="num">${dec1(ngC.dist - orC.dist)}</b> đơn vị (<b>${pct((ngC.dist - orC.dist) / ngC.dist)}</b>) và ít hơn <b>${ngC.veh - orC.veh}</b> xe.` : 'Chỉ so sánh khi cả hai phương pháp có lời giải khả thi.'}</div>`;
  /* bảng cấu hình */
  const keys = [...new Set(CASES.map(configKey))];
  const cell = x => fe(x) ? `<b class="num" style="font-weight:600">${dec1(x.dist)}</b> <span style="color:var(--muted)">· ${x.veh} xe</span>` : `<span style="color:var(--red);font-weight:600">Chưa có lời giải</span>`;
  $('#rtable').innerHTML = `<table class="table cp"><tr><th>Cấu hình</th><th>OR Tools</th><th>Điểm gần nhất</th><th>Giảm quãng đường</th></tr>` + keys.map(k => {
    const o = caseOf(k, 'ortools'), n = caseOf(k, 'nearest_feasible'), base = o || n, on = k === key, g = fe(o) && fe(n) ? (n.dist - o.dist) / n.dist : null;
    return `<tr class="clickrow ${on ? 'selrow' : ''}" data-case="${(o || n).id}"><td>${base.instance.toUpperCase()} · tải ${base.cap} · tối đa ${base.maxv} xe${on ? ' <span style="font-size:10px;font-weight:700;color:var(--red);letter-spacing:.06em;margin-left:6px">ĐANG XEM</span>' : ''}</td><td>${cell(o)}</td><td>${cell(n)}</td><td class="num">${nz(g) ? '<span style="color:var(--muted)">chưa có đối chứng</span>' : `<b style="color:var(--teal);font-weight:700">${pct(g)}</b>`}</td></tr>`;
  }).join('') + '</table>';
  $('#tape4').textContent = ok1
    ? `Phương án này dùng ${c.veh} xe và ${dec1(c.dist)} đơn vị quãng đường${nz(red4) ? '' : `, ngắn hơn ${pct(red4)} so với điểm gần nhất cùng cấu hình`}; nhiên liệu mô phỏng ${num(fuel)} VND theo giả định đã chọn.`
    : 'Chưa tìm được lời giải khả thi cho phương án này; không quy về quãng đường hay chi phí bằng 0.';
}

/* ------------------------------------------------------------------ ngăn lịch trình */
function openDrawer(vehicle) {
  const c = CASES.find(x => x.id === S.cas), ci = CASES.indexOf(c), stops = D.stops[ci] || [], vs = [...new Set(stops.map(s => s[0]))].sort((a, b) => a - b);
  const v = vehicle ?? 'all', list = stops.filter(s => v === 'all' || s[0] === v).sort((a, b) => a[0] - b[0] || a[1] - b[1]);
  $('#drawer').innerHTML = `<h2>Lịch trình tuyến</h2><div class="sub">${esc(c.label)} · điểm 0 là kho · tọa độ Solomon</div>
    <div class="chips"><span class="chip2 ${v === 'all' ? 'on' : ''}" data-veh-chip="all">Tất cả xe</span>${vs.map(x => `<span class="chip2 ${v === x ? 'on' : ''}" data-veh-chip="${x}">Xe ${x}</span>`).join('')}</div>
    ${list.length ? `<table class="table cp"><tr><th>Xe</th><th>Thứ tự</th><th>Điểm dừng</th><th>X</th><th>Y</th></tr>${list.map(s => `<tr><td>${s[0]}</td><td class="num">${s[1]}</td><td class="num">${s[2]}</td><td class="num">${dec(s[3], 1)}</td><td class="num">${dec(s[4], 1)}</td></tr>`).join('')}</table>` : '<div class="nodata">Chưa có lịch trình cho phương án này</div>'}`;
  $('#drawer').classList.add('on'); $('#dbg').classList.add('on');
}
const closeDrawer = () => { $('#drawer').classList.remove('on'); $('#dbg').classList.remove('on'); };

/* ------------------------------------------------------------------ bộ lọc */
const fmtThr = v => dec(v);
function filterSpec(page) {
  const regs = () => ['Tất cả', ...REG.filter(r => S.market == null || r.market === MARKETS.indexOf(S.market)).map(r => r.name)];
  const F = {
    mode: { label: 'Phương thức', w: 172, cur: () => S.mode || 'Tất cả', opts: () => ['Tất cả', ...MODES], set: v => { S.mode = v === 'Tất cả' ? null : v; } },
    market: { label: 'Thị trường', w: 172, cur: () => S.market || 'Tất cả', opts: () => ['Tất cả', ...MARKETS], set: v => { S.market = v === 'Tất cả' ? null : v; if (S.region && !REG.find(r => r.name === S.region && r.market === MARKETS.indexOf(S.market)) && S.market) S.region = null; } },
    region: { label: 'Vùng giao', w: 200, cur: () => S.region || 'Tất cả', opts: regs, set: v => { S.region = v === 'Tất cả' ? null : v; } },
    thr: { label: 'Ngưỡng cảnh báo', w: 172, cur: () => fmtThr(S.thr), opts: () => D.thresholds.map(fmtThr), set: v => { S.thr = parseFloat(v.replace(',', '.')); } },
    policy: { label: 'Phương án đang xem', w: 210, cur: () => POL.find(p => p.id === S.policy).label, opts: () => POL.map(p => p.label), set: v => { S.policy = POL.find(p => p.label === v).id; } },
    cas: { label: 'Phương án tuyến', w: 300, cur: () => CASES.find(c => c.id === S.cas).label, opts: () => CASES.map(c => c.label), set: v => { S.cas = CASES.find(c => c.label === v).id; } },
    km: { label: 'Km / đơn vị', w: 112, cur: () => dec(S.km, 1), opts: () => D.params.km.map(v => dec(v, 1)), set: v => { S.km = parseFloat(v.replace(',', '.')); } },
    lit: { label: 'Lít / 100 km', w: 112, cur: () => String(S.lit), opts: () => D.params.lit.map(String), set: v => { S.lit = parseFloat(v); } },
    price: { label: 'VND / lít', w: 136, cur: () => num(S.price), opts: () => D.params.price.map(num), set: v => { S.price = parseInt(v.replace(/\./g, ''), 10); } },
  };
  const per = { p1: ['mode', 'market', 'region'], p2: ['thr', 'mode', 'region'], p3: ['policy', 'mode', 'region'], p4: ['cas', 'km', 'lit', 'price'] };
  return per[page].map(k => ({ key: k, ...F[k] }));
}
let FILTERS = {};
function renderFilters() {
  const host = $('#fb' + S.page.slice(1)); FILTERS = {};
  const specs = filterSpec(S.page);
  host.innerHTML = specs.map(s => { FILTERS[s.key] = s; return `<div class="fil well" data-f="${s.key}" style="width:${s.w}px"><span>${s.label}</span><b>${esc(s.cur())}</b></div>`; }).join('') + (S.page === 'p4' ? '' : '<div class="reset">Xóa bộ lọc</div>');
}
function closeMenus(except) { $$('.fil.open').forEach(f => { if (f === except) return; f.classList.remove('open'); const m = f.querySelector('.menu'); if (m) { m.classList.add('out'); setTimeout(() => m.remove(), 170); } }); }
function toast(t) { let el = $('.toast'); if (!el) { el = document.createElement('div'); el.className = 'toast raise small'; document.documentElement.appendChild(el); } el.textContent = t; el.classList.add('on'); clearTimeout(el._t); el._t = setTimeout(() => el.classList.remove('on'), 2200); }

/* ------------------------------------------------------------------ làm mới, đếm số, chuyển trang */
function runCountUps(root) {
  if (!root || matchMedia('(prefers-reduced-motion:reduce)').matches) return;
  $$('.big,.eng b,.cnt b,.rc b,.fn .t b,.dialfoot b,.pl-r b,.tl b', root).forEach(el => {
    const node = [...el.childNodes].find(n => n.nodeType === 3 && n.nodeValue.trim());
    if (!node) return;
    const txt = node.nodeValue.trim(), m = txt.match(/^([+\-−]?)(\d{1,3}(?:\.\d{3})+|\d+)(?:,(\d+))?(%?)$/);
    if (!m) return;
    const dd = m[3] ? m[3].length : 0, target = parseFloat(m[2].replace(/\./g, '') + (m[3] ? '.' + m[3] : '')), t0 = performance.now() + 120;
    cancelAnimationFrame(el._raf);
    (function f(now) { const p = Math.max(0, Math.min(1, (now - t0) / 1100)), v = target * (1 - Math.pow(1 - p, 4)); node.nodeValue = m[1] + v.toLocaleString('vi-VN', { minimumFractionDigits: dd, maximumFractionDigits: dd }) + m[4]; if (p < 1) el._raf = requestAnimationFrame(f); else node.nodeValue = txt; })(performance.now());
  });
}
function applyFocus() {
  const m = S.hover || S.mode;
  $$('[data-mode]').forEach(el => { el.classList.toggle('dim', !!m && el.dataset.mode !== m); el.classList.toggle('foc', !!m && el.dataset.mode === m && el.classList.contains('tile')); });
  $$('[data-col]').forEach(el => el.classList.toggle('dimc', !!S.market && el.dataset.col !== S.market));
}
const RENDER = { p1: render1, p2: render2, p3: render3, p4: render4 };
function render(animate = true) {
  renderRail(); renderFilters(); RENDER[S.page]();
  $$('.kk').forEach((el, i) => { el.style.animationDelay = (150 + i * 24) + 'ms'; });
  applyFocus();
  if (animate) runCountUps($('.page.on'));
}
function stagger(pg) { [...pg.children].forEach((row, r) => { row.style.animationDelay = (r * 70) + 'ms'; }); $$('.tile,.cnt', pg).forEach((el, k) => { el.style.animationDelay = (240 + k * 60) + 'ms'; }); }
function showPage(id) {
  S.page = id; closeDrawer();
  $$('.key[data-p]').forEach(k => k.classList.toggle('on', k.dataset.p === id));
  $$('.page').forEach(p => p.classList.toggle('on', p.id === id));
  stagger($('#' + id)); tipHide(); closeMenus(); render();
  try { history.replaceState(null, '', '#' + id); } catch (e) { /* mở từ file thì bỏ qua */ }
}

/* ------------------------------------------------------------------ chuột: gợi ý, nghiêng, gợn */
const tip = document.createElement('div'); tip.className = 'tip raise small'; document.documentElement.appendChild(tip);
function tipShow(html, x, y) { tip.innerHTML = html; tip.classList.add('on'); const w = tip.offsetWidth, h = tip.offsetHeight; let px = x + 16, py = y + 18; if (px + w > innerWidth - 8) px = x - w - 16; if (py + h > innerHeight - 8) py = y - h - 14; tip.style.transform = `translate(${px}px,${py}px)`; }
function tipHide() { tip.classList.remove('on'); }
let tiltEl = null; const resetTilt = el => { el.style.setProperty('--ry', '0deg'); el.style.setProperty('--rx', '0deg'); };
document.addEventListener('pointerover', e => {
  const t = e.target.closest && e.target.closest('[data-mode]'), v = e.target.closest && e.target.closest('[data-veh]');
  const nm = t ? t.dataset.mode : null; if (nm !== S.hover) { S.hover = nm; applyFocus(); }
  $$('.vh').forEach(g => g.classList.toggle('dim', !!v && g.dataset.veh !== v.dataset.veh));
});
document.addEventListener('pointermove', e => {
  const tg = e.target.closest && e.target.closest('[data-tip]'), sv = e.target.closest && e.target.closest('#trend svg'), xh = $('#xh');
  if (tg) tipShow(tg.dataset.tip, e.clientX, e.clientY);
  else if (sv && window.__tr) {
    const T = window.__tr, r = sv.getBoundingClientRect(), xv = (e.clientX - r.left) / (r.width / T.w), idx = (xv - T.Lm) / T.step;
    const p = T.pts.reduce((a, q) => Math.abs(q.i - idx) < Math.abs(a.i - idx) ? q : a), x = T.Lm + p.i * T.step, y = T.Tm + (T.hi - p.v) / (T.hi - T.lo) * (T.hh - T.Tm - T.Bm);
    $('#xhl').setAttribute('x1', x); $('#xhl').setAttribute('x2', x); $('#xhc').setAttribute('cx', x); $('#xhc').setAttribute('cy', y); xh.style.opacity = 1;
    tipShow(`<b>${monthText(MONTHS[p.i])}</b><br>Tỷ lệ trễ ${pct(p.v)}<br>${num(p.n)} đơn<br>Giao thực tế ${dec(p.act)} ngày · chênh ${p.gap >= 0 ? '+' : ''}${dec(p.gap)}`, e.clientX, e.clientY);
  } else tipHide();
  if (xh && !sv) xh.style.opacity = 0;
  const el = e.target.closest && e.target.closest('.tile,.cnt,.plate');
  if (tiltEl && tiltEl !== el) resetTilt(tiltEl);
  if (!el) { tiltEl = null; return; }
  tiltEl = el; const r = el.getBoundingClientRect(), px = (e.clientX - r.left) / r.width, py = (e.clientY - r.top) / r.height, deg = 5 * 300 / Math.max(300, r.width);
  el.style.setProperty('--ry', ((px - .5) * 2 * deg).toFixed(2) + 'deg'); el.style.setProperty('--rx', ((.5 - py) * 2 * deg).toFixed(2) + 'deg');
  el.style.setProperty('--mx', (px * 100).toFixed(1) + '%'); el.style.setProperty('--my', (py * 100).toFixed(1) + '%');
});
document.documentElement.addEventListener('pointerleave', () => { tipHide(); if (tiltEl) resetTilt(tiltEl); S.hover = null; applyFocus(); });
document.addEventListener('pointerdown', e => {
  const t = e.target.closest && e.target.closest('.key,.reset,.knob,.btn'); if (!t) return;
  const r = t.getBoundingClientRect(), d = Math.max(r.width, r.height) * 2.2, s = document.createElement('span'); s.className = 'ripple';
  s.style.cssText = `width:${d}px;height:${d}px;left:${e.clientX - r.left - d / 2}px;top:${e.clientY - r.top - d / 2}px`; t.appendChild(s); setTimeout(() => s.remove(), 700);
});
document.addEventListener('click', e => {
  const tg = e.target;
  const it = tg.closest && tg.closest('.menu div'), f = tg.closest && tg.closest('.fil');
  if (it) { const f2 = it.closest('.fil'), spec = FILTERS[f2.dataset.f]; e.stopPropagation(); spec.set(it.textContent); closeMenus(); render(); return; }
  closeMenus(f);
  if (f) {
    if (f.classList.contains('open')) { closeMenus(); return; }
    const spec = FILTERS[f.dataset.f], cur = spec.cur(); f.classList.add('open');
    const m = document.createElement('div'); m.className = 'menu'; m.innerHTML = spec.opts().map(x => `<div class="${x === cur ? 'sel' : ''}">${esc(x)}</div>`).join(''); f.appendChild(m);
    const sel = m.querySelector('.sel'); if (sel) m.scrollTop = Math.max(0, sel.offsetTop - 80); return;
  }
  if (tg.closest && tg.closest('.reset')) { S.mode = null; S.market = null; S.region = null; S.thr = .5; S.policy = POL_DEFAULT; render(); toast('Đã xóa bộ lọc'); return; }
  if (tg.closest && tg.closest('#openStops')) { openDrawer(); return; }
  const chip = tg.closest && tg.closest('[data-veh-chip]'); if (chip) { const v = chip.dataset.vehChip; openDrawer(v === 'all' ? 'all' : parseInt(v, 10)); return; }
  if (tg.closest && tg.closest('#dbg')) { closeDrawer(); return; }
  const pr = tg.closest && tg.closest('[data-pol]'); if (pr) { S.policy = pr.dataset.pol; render(); return; }
  const cr = tg.closest && tg.closest('[data-case]'); if (cr) { S.cas = cr.dataset.case; render(); return; }
  const md = tg.closest && tg.closest('[data-mode]'); if (md && S.page !== 'p4') { const m = md.dataset.mode; S.mode = S.mode === m ? null : m; render(false); }
});
document.addEventListener('keydown', e => { if (e.key === 'Escape') { closeMenus(); closeDrawer(); } });
$$('.key[data-p]').forEach(k => { k.onclick = () => showPage(k.dataset.p); });
$('#tog').onclick = e => {
  const kn = e.currentTarget; kn.classList.toggle('spin');
  const apply = () => { const h = document.documentElement; h.dataset.theme = h.dataset.theme === 'dark' ? 'light' : 'dark'; render(); };
  if (!document.startViewTransition || matchMedia('(prefers-reduced-motion:reduce)').matches) { apply(); return; }
  const r = kn.getBoundingClientRect(), x = r.left + r.width / 2, y = r.top + r.height / 2, R = Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y));
  const vt = document.startViewTransition(apply);
  vt.ready.then(() => document.documentElement.animate({ clipPath: [`circle(0px at ${x}px ${y}px)`, `circle(${R}px at ${x}px ${y}px)`] }, { duration: 800, easing: 'cubic-bezier(.2,.8,.2,1)', pseudoElement: '::view-transition-new(root)' }));
};
const fit = () => { document.body.style.zoom = Math.min(1.6, Math.max(.4, innerWidth / 1440)); };
fit(); addEventListener('resize', fit);

/* khởi động */
const start = (location.hash || '').slice(1);
if (RENDER[start]) { S.page = start; $$('.key[data-p]').forEach(k => k.classList.toggle('on', k.dataset.p === start)); $$('.page').forEach(p => p.classList.toggle('on', p.id === start)); }
stagger($('.page.on')); render();
window.__api = { S, aggA, aggB, aggC, render, showPage, D };
})();
