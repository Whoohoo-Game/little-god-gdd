/*
 * Little God — trang đọc GDD / Tech Doc. Không có bước build: trang đọc thẳng các file Markdown trong Docs/.
 * Danh sách chương lấy từ bảng "Mục lục" trong README.md của mỗi tài liệu (dòng có số ở cột đầu và link tới file .md),
 * nên thêm một chương vào bảng đó là trang tự có chương mới.
 * Địa chỉ một mục: #<tài liệu>:<file không đuôi>[:<slug của tiêu đề kiểu GitHub>], ví dụ #gdd:14-hang-tho-va-san-moi:5-hiển-thị
 */
(() => {
  'use strict';

  const BOOKS = {
    gdd: { dir: 'GDD/', sub: 'Game design document', intro: 'Giới thiệu' },
    tech: { dir: 'Tech Doc/', sub: 'Technical document', intro: 'Giới thiệu' },
  };
  const COLORS = 8;

  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  const panel = $('#panel'), toc = $('#toc'), rail = $('#rail'), q = $('#q'), resultsBox = $('#results'), clr = $('#clr');
  const loaded = {};          // tài liệu → { doc, chapters, index }
  let current = null;         // tài liệu đang xem
  let spy = null;

  // ------------------------------------------------------------------ chuỗi

  /** Slug tiêu đề như GitHub (github-slugger): chữ thường, bỏ dấu câu và emoji, khoảng trắng → "-". */
  function slug(text) {
    return text.trim().toLowerCase().replace(/[^\p{L}\p{M}\p{N}\p{Pc} -]/gu, '').replace(/ /g, '-');
  }

  /**
   * GDD dùng "~" nghĩa là "khoảng" (~30 thỏ). GFM coi hai dấu "~" đơn là gạch ngang, nên thoát dấu "~" đơn ngoài code;
   * chỉ "~~…~~" mới là gạch ngang.
   */
  function keepTildes(md) {
    let fenced = false;
    return md.split('\n').map(line => {
      if (/^\s*(```|~~~)/.test(line)) { fenced = !fenced; return line; }
      if (fenced) return line;
      return line.split(/(`+[^`]*`+)/).map((part, i) => i % 2 ? part : part.replace(/(?<!~)~(?!~)/g, '\\~')).join('');
    }).join('\n');
  }

  /** Chữ của tiêu đề, bỏ dấu "#" của link neo thêm vào cuối. */
  const headingText = h => h.textContent.replace(/#$/, '').trim();

  /** Bỏ dấu tiếng Việt để tìm kiếm không dấu: "Hang thỏ" ~ "hang tho". */
  function fold(text) {
    return text.normalize('NFD').replace(/\p{M}/gu, '').replace(/đ/g, 'd').replace(/Đ/g, 'D').toLowerCase();
  }

  /** Nhãn ngắn cho trạng thái trong bảng Mục lục (✅ / 💡 …). */
  function statusPill(status) {
    const s = status.toLowerCase();
    let cls = 'gray', label = status.replace(/[✅💡❓⚠️↻]/gu, '').trim().split(/[,(]/)[0].trim();
    if (status.includes('✅')) { cls = 'ok'; label = /xong/.test(s) ? 'Xong' : 'Chốt'; }
    else if (status.includes('💡')) {
      cls = /kiểm chứng/.test(s) ? 'info' : 'warn';
      label = /kiểm chứng/.test(s) ? 'Kiểm chứng' : /đặc tả/.test(s) ? 'Đặc tả' : /đang làm/.test(s) ? 'Đang làm'
        : /đề xuất/.test(s) ? 'Đề xuất' : 'Nháp';
    }
    if (label.length > 14) label = label.slice(0, 13) + '…';
    return label ? `<span class="pill ${cls}" title="${esc(status)}">${esc(label)}</span>` : '';
  }

  // ------------------------------------------------------------------ đọc tài liệu

  async function fetchText(path) {
    const res = await fetch(encodeURI(path), { cache: 'no-cache' });
    if (!res.ok) throw new Error(`${path}: ${res.status}`);
    return res.text();
  }

  /** Các chương trong bảng Mục lục của README: | 01 | [Tên](01-file.md) | mô tả | trạng thái | */
  function parseIndex(readme) {
    const chapters = [];
    for (const line of readme.split('\n')) {
      const cells = line.split('|').slice(1, -1).map(c => c.trim());
      if (cells.length < 3 || !/^\d+$/.test(cells[0])) continue;
      const m = cells[1].match(/\[([^\]]+)\]\(([^)]+\.md)\)/);
      if (!m) continue;
      chapters.push({ num: String(+cells[0]), title: m[1], file: decodeURI(m[2]), status: cells[cells.length - 1] });
    }
    return chapters;
  }

  async function load(book) {
    if (loaded[book]) return loaded[book];
    const dir = BOOKS[book].dir;
    const readme = await fetchText(dir + 'README.md');
    const chapters = [{ num: '0', title: BOOKS[book].intro, file: 'README.md', status: '', intro: true }, ...parseIndex(readme)];
    const texts = await Promise.all(chapters.map(c => c.intro ? readme : fetchText(dir + c.file).catch(e => `> ⚠️ Không đọc được ${c.file}: ${e.message}`)));

    const doc = document.createElement('div');
    doc.className = 'doc';
    doc.dataset.book = book;
    chapters.forEach((c, i) => {
      c.stem = c.file.replace(/\.md$/, '');
      c.id = `${book}:${c.stem}`;
      c.color = c.intro ? 0 : (i - 1) % COLORS + 1;
      doc.appendChild(renderChapter(book, c, texts[i]));
    });
    const data = { doc, chapters, index: null };
    loaded[book] = data;
    return data;
  }

  function renderChapter(book, c, md) {
    const sec = document.createElement('section');
    sec.className = 'chapter' + (c.intro ? ' intro' : '');
    sec.id = c.id;
    sec.innerHTML = marked.parse(keepTildes(md), { gfm: true });

    // tiêu đề chương: h1 đầu tiên, kèm số chương có màu như trang mẫu
    const h1 = $('h1', sec);
    const head = document.createElement('div');
    head.className = 'chapter-head';
    head.innerHTML = `<span class="cap c${c.color}">${c.intro ? '★' : esc(c.num)}</span>`;
    if (h1) {
      h1.textContent = h1.textContent.replace(/^\d+\s*·\s*/, '');
      head.appendChild(h1);
    }
    head.insertAdjacentHTML('beforeend', statusPill(c.status));
    sec.prepend(head);

    // id tiêu đề như GitHub (trùng thì thêm -1, -2…), để link "file.md#mục" trong Markdown dùng được
    const seen = {};
    c.subs = [];
    $$('h2, h3, h4', sec).forEach(h => {
      let s = slug(h.textContent);
      if (seen[s] != null) s = `${s}-${++seen[s]}`; else seen[s] = 0;
      h.id = `${c.id}:${s}`;
      h.insertAdjacentHTML('beforeend', `<a class="anchor" href="#${esc(h.id)}" aria-label="Link tới mục này">#</a>`);
      if (h.tagName === 'H2') {
        const text = headingText(h);
        const m = text.match(/^(\d+[a-z]?(?:\.\d+)*)\.?\s+(.*)$/);
        c.subs.push({ id: h.id, n: m ? m[1] : '', text: m ? m[2] : text });
      }
    });

    // bảng rộng cuộn ngang trong khung riêng
    $$('table', sec).forEach(t => {
      const wrap = document.createElement('div');
      wrap.className = 'tbl';
      t.replaceWith(wrap);
      wrap.appendChild(t);
    });

    $$('a[href]', sec).forEach(a => rewriteLink(a, book, c));
    return sec;
  }

  /** Link giữa các file Markdown → nhảy trong trang; link tới file khác (sim/*.py, json) mở file đó. */
  function rewriteLink(a, book, c) {
    const href = a.getAttribute('href');
    if (/^[a-z]+:/i.test(href)) { a.target = '_blank'; a.rel = 'noopener'; return; }
    if (href.startsWith('#')) { a.setAttribute('href', `#${c.id}:${decodeURIComponent(href.slice(1))}`); return; }
    const base = new URL(BOOKS[book].dir, location.href);
    const url = new URL(href, base);
    const path = decodeURIComponent(url.pathname);
    const frag = decodeURIComponent(url.hash.slice(1));
    for (const [key, b] of Object.entries(BOOKS)) {
      const dir = decodeURIComponent(new URL(b.dir, location.href).pathname);
      if (path.startsWith(dir) && path.endsWith('.md') && !path.slice(dir.length).includes('/')) {
        const stem = path.slice(dir.length, -3);
        a.setAttribute('href', `#${key}:${stem}${frag ? ':' + frag : ''}`);
        return;
      }
    }
    a.href = url.href;
    a.target = '_blank';
    a.rel = 'noopener';
  }

  // ------------------------------------------------------------------ mục lục bên trái

  function renderToc(book, chapters) {
    toc.innerHTML = chapters.map(c => `
      <div class="ch" data-id="${esc(c.id)}">
        <a class="ch-link" href="#${esc(c.id)}"><span class="cap c${c.color}">${c.intro ? '★' : esc(c.num)}</span>
          <span>${esc(c.title)}</span>${statusPill(c.status)}</a>
        <div class="subs">${c.subs.map(s => `<a class="sub" href="#${esc(s.id)}" data-id="${esc(s.id)}"><span class="n">${esc(s.n)}</span><span>${esc(s.text)}</span></a>`).join('')}</div>
      </div>`).join('');
  }

  function setActive(id) {
    const chapterId = id.split(':').slice(0, 2).join(':');
    $$('.ch', toc).forEach(ch => {
      const on = ch.dataset.id === chapterId;
      ch.classList.toggle('active', on);
      ch.classList.toggle('open', on);
    });
    $$('.sub', toc).forEach(s => s.classList.toggle('active', s.dataset.id === id));
    const link = $(`.sub.active`, toc) || $(`.ch.active .ch-link`, toc);
    if (link) {
      const r = link.getBoundingClientRect(), box = toc.getBoundingClientRect();
      if (r.top < box.top || r.bottom > box.bottom) link.scrollIntoView({ block: 'nearest' });
    }
  }

  /** Đánh dấu mục đang đọc theo vị trí cuộn. */
  function watch(doc) {
    if (spy) spy.disconnect();
    const visible = new Map();
    spy = new IntersectionObserver(entries => {
      for (const e of entries) visible.set(e.target, e.isIntersecting);
      const heads = $$('.chapter, h2', doc);
      let best = null;
      for (const h of heads) {
        if (h.getBoundingClientRect().top <= 120) best = h; else break;
      }
      if (best) setActive(best.id);
    }, { rootMargin: '0px 0px -60% 0px' });
    $$('.chapter, h2', doc).forEach(h => spy.observe(h));
  }

  // ------------------------------------------------------------------ chuyển tài liệu, điều hướng

  async function show(book, targetId) {
    if (current !== book) {
      current = book;
      $$('.switch button').forEach(b => b.setAttribute('aria-selected', String(b.dataset.book === book)));
      $('#brand-sub').textContent = BOOKS[book].sub;
      panel.innerHTML = '<div class="loading">Đang tải tài liệu…</div>';
      let data;
      try { data = await load(book); } catch (e) {
        panel.innerHTML = `<div class="error">Không tải được tài liệu (${esc(e.message)}). Nếu đang mở file trực tiếp, hãy chạy một web server trong thư mục Docs/.</div>`;
        return;
      }
      if (current !== book) return;
      panel.replaceChildren(data.doc);
      renderToc(book, data.chapters);
      watch(data.doc);
      runSearch();
    }
    const el = targetId && document.getElementById(targetId);
    if (el) {
      const go = () => el.scrollIntoView({ behavior: 'instant', block: 'start' });
      go();
      // phông chữ tải xong làm dòng chữ đổi cao: cuộn lại cho đúng chỗ
      document.fonts?.ready.then(() => requestAnimationFrame(go));
      setActive(el.closest('h2') ? el.id : (el.closest('.chapter')?.id || el.id));
    } else if (!targetId) window.scrollTo({ top: 0, behavior: 'instant' });
    closeRail();
  }

  function route() {
    const hash = decodeURIComponent(location.hash.slice(1));
    const book = BOOKS[hash.split(':')[0]] ? hash.split(':')[0] : current || 'gdd';
    show(book, hash.includes(':') ? hash : null);
  }

  $$('.switch button').forEach(b => b.addEventListener('click', () => {
    if (b.dataset.book !== current) location.hash = b.dataset.book;
  }));
  window.addEventListener('hashchange', route);

  // ------------------------------------------------------------------ tìm kiếm

  function buildIndex(book) {
    const data = loaded[book];
    if (data.index) return data.index;
    const nodes = $$('h1, h2, h3, h4, p, li, th, td, pre', data.doc).filter(el =>
      !(el.tagName === 'P' && el.closest('li, td, th')) && !$('p, ul, ol', el.tagName === 'LI' ? el : document.createElement('i')));
    data.index = nodes.map(el => {
      const chapter = data.chapters.find(c => c.id === el.closest('.chapter').id);
      const head = el.closest('section') && headingBefore(el);
      return { el, text: el.textContent, folded: fold(el.textContent), where: `${chapter.intro ? '★' : chapter.num} · ${chapter.title}${head ? ' › ' + head : ''}` };
    });
    return data.index;
  }

  /** Tiêu đề h2 gần nhất phía trên một đoạn (để hiện "Chương › Mục" trong kết quả). */
  function headingBefore(el) {
    let n = el.closest('.chapter > *') || el;
    while (n) {
      if (n.tagName === 'H2') return headingText(n);
      n = n.previousElementSibling;
    }
    return '';
  }

  /** Một từ khoá chỉ khớp ở đầu từ ("tho" khớp "thỏ", không khớp giữa "thong"). */
  const termRe = t => new RegExp('(?<![\\p{L}\\p{N}])' + t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gu');

  /** Bọc các đoạn khớp (so không dấu) trong một phần tử bằng <mark>. */
  function highlight(el, terms) {
    const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    const texts = [];
    while (walker.nextNode()) if (!walker.currentNode.parentElement.closest('.anchor, mark')) texts.push(walker.currentNode);
    for (const node of texts) {
      const src = node.data;
      // vị trí ký tự gốc của từng ký tự sau khi bỏ dấu
      let folded = '';
      const map = [];
      for (let i = 0; i < src.length; i++) {
        const f = fold(src[i]);
        for (let k = 0; k < f.length; k++) { folded += f[k]; map.push(i); }
      }
      const spans = [];
      for (const t of terms) {
        for (const m of folded.matchAll(termRe(t))) spans.push([map[m.index], map[m.index + t.length - 1] + 1]);
      }
      if (!spans.length) continue;
      spans.sort((a, b) => a[0] - b[0]);
      const frag = document.createDocumentFragment();
      let pos = 0;
      for (const [s, e] of spans) {
        if (s < pos) continue;
        frag.append(src.slice(pos, s));
        const m = document.createElement('mark');
        m.className = 'hit';
        m.textContent = src.slice(s, e);
        frag.append(m);
        pos = e;
      }
      frag.append(src.slice(pos));
      node.replaceWith(frag);
    }
  }

  function clearMarks() {
    $$('mark.hit', panel).forEach(m => m.replaceWith(m.textContent));
    panel.normalize();
  }

  let hits = [], cursor = -1, timer = 0;

  function runSearch() {
    if (!current || !loaded[current]) return;
    clearMarks();
    const raw = q.value.trim();
    clr.hidden = !raw;
    $('.search .key').hidden = !!raw;
    const terms = fold(raw).split(/\s+/).filter(t => t.length >= 2);
    if (!terms.length) { resultsBox.hidden = true; hits = []; return; }
    const res = terms.map(termRe);
    hits = buildIndex(current).filter(r => res.every(re => { re.lastIndex = 0; return re.test(r.folded); }));
    cursor = -1;
    const shown = hits.slice(0, 80);
    resultsBox.hidden = false;
    resultsBox.innerHTML = `<div class="count">${hits.length ? `${hits.length} kết quả${hits.length > shown.length ? ` · hiện ${shown.length} đầu tiên` : ''} · Enter để nhảy tiếp` : `Không có kết quả cho “${esc(raw)}”`}</div>`
      + shown.map((r, i) => `<button data-i="${i}"><span class="where">${esc(r.where)}</span>${snippet(r, terms)}</button>`).join('');
    shown.slice(0, 200).forEach(r => highlight(r.el, terms));
  }

  function snippet(r, terms) {
    const t = r.text.replace(/\s+/g, ' ').trim();
    const f = fold(t);
    const first = f.search(termRe(terms[0]));
    const at = Math.max(0, first - 40);
    let s = (at > 0 ? '…' : '') + t.slice(at, at + 140) + (t.length > at + 140 ? '…' : '');
    s = esc(s);
    // tô từ khoá trong đoạn trích (so không dấu từng từ)
    return s.replace(/[\p{L}\p{M}\p{N}]+/gu, w => terms.some(term => fold(w).startsWith(term)) ? `<mark>${w}</mark>` : w);
  }

  function jump(i) {
    if (!hits.length) return;
    cursor = (i + hits.length) % hits.length;
    const el = hits[cursor].el;
    el.scrollIntoView({ block: 'center' });
    el.classList.remove('flash');
    void el.offsetWidth;
    el.classList.add('flash');
    $$('button', resultsBox).forEach(b => b.classList.toggle('on', +b.dataset.i === cursor));
    closeRail();
  }

  q.addEventListener('input', () => { clearTimeout(timer); timer = setTimeout(runSearch, 120); });
  q.addEventListener('keydown', e => {
    if (e.key === 'Enter') { e.preventDefault(); jump(cursor + (e.shiftKey ? -1 : 1)); }
    if (e.key === 'Escape') { q.value = ''; runSearch(); q.blur(); }
  });
  resultsBox.addEventListener('click', e => {
    const b = e.target.closest('button[data-i]');
    if (b) jump(+b.dataset.i);
  });
  clr.addEventListener('click', () => { q.value = ''; runSearch(); q.focus(); });
  document.addEventListener('keydown', e => {
    if (e.key === '/' && document.activeElement !== q && !e.metaKey && !e.ctrlKey) { e.preventDefault(); openRail(); q.focus(); q.select(); }
  });

  // ------------------------------------------------------------------ thanh bên trên điện thoại

  const menuBtn = $('#menu-btn'), scrim = $('#scrim');
  function openRail() {
    if (getComputedStyle(menuBtn).display === 'none') return;
    rail.classList.add('open'); scrim.hidden = false; menuBtn.setAttribute('aria-expanded', 'true');
  }
  function closeRail() { rail.classList.remove('open'); scrim.hidden = true; menuBtn.setAttribute('aria-expanded', 'false'); }
  menuBtn.addEventListener('click', () => rail.classList.contains('open') ? closeRail() : openRail());
  scrim.addEventListener('click', closeRail);
  toc.addEventListener('click', e => { if (e.target.closest('a')) closeRail(); });

  if (typeof marked === 'undefined') {
    panel.innerHTML = '<div class="error">Không tải được thư viện Markdown (marked). Kiểm tra kết nối mạng.</div>';
    return;
  }
  route();
})();
