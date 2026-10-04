(() => {
  function slugify(text) {
    const slug = text.trim().toLowerCase()
      .replace(/[^\p{L}\p{N}\s-]/gu, '')
      .replace(/\s+/g, '-');
    return slug || 'section';
  }

  function ensureHeadingIds(headings) {
    const used = new Set();
    headings.forEach((h) => {
      const base = h.id || slugify(h.textContent);
      let candidate = base;
      let n = 2;
      while (used.has(candidate) || (document.getElementById(candidate) && document.getElementById(candidate) !== h)) {
        candidate = `${base}-${n}`;
        n += 1;
      }
      h.id = candidate;
      used.add(candidate);
    });
  }

  function buildToc(headings, nav) {
    headings.forEach((h) => {
      const a = document.createElement('a');
      a.className = 'toc-link';
      a.href = `#${h.id}`;
      a.textContent = h.textContent.trim();
      nav.appendChild(a);
    });
  }

  function spyOnSections(headings, nav) {
    const links = new Map([...nav.querySelectorAll('a.toc-link')].map((a) => [a.getAttribute('href').slice(1), a]));
    const setActive = (id) => links.forEach((a, key) => a.classList.toggle('active', key === id));
    if (headings[0]) setActive(headings[0].id);
    if (!('IntersectionObserver' in window)) return;
    const observer = new IntersectionObserver((entries) => {
      entries.filter((e) => e.isIntersecting).forEach((e) => setActive(e.target.id));
    }, { rootMargin: '0px 0px -70% 0px' });
    headings.forEach((h) => observer.observe(h));
  }

  function openChat(question, attempts = 50) {
    const fab = document.getElementById('pm-chat-fab');
    const popup = document.getElementById('pm-chat-popup');
    if (!fab || !popup) {
      if (attempts > 0) setTimeout(() => openChat(question, attempts - 1), 100);
      return;
    }
    if (!popup.classList.contains('pm-open')) fab.click();
    const input = document.getElementById('pm-chat-input');
    if (input && question) {
      input.value = question;
      input.focus();
    }
  }

  function mountDemo(body) {
    const tpl = document.getElementById('demo-template');
    if (!tpl) return;
    let slot = document.getElementById('demo-slot');
    if (!slot) {
      slot = document.createElement('div');
      slot.id = 'demo-slot';
      body.prepend(slot);
    }
    slot.appendChild(tpl.content.cloneNode(true));
    slot.querySelectorAll('[data-open-chat]').forEach((btn) => {
      btn.addEventListener('click', () => openChat(btn.dataset.question || ''));
    });
  }

  // mermaid(약 1MB)는 목차·데모·챗봇 초기화를 막지 않도록, 다이어그램이 있을 때만 async로 불러온다.
  // 로드에 실패하거나 응답이 없으면 원본 코드 블록이 그대로 남는다.
  const MERMAID_SRC = 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js';

  function renderMermaid(body) {
    const found = [...body.querySelectorAll('div.language-mermaid, pre > code.language-mermaid')];
    const blocks = found.filter((b) => !found.some((o) => o !== b && o.contains(b)));
    if (!blocks.length) return;
    const script = document.createElement('script');
    script.src = MERMAID_SRC;
    script.async = true;
    script.onload = () => {
      if (!window.mermaid) return;
      const nodes = blocks.map((el) => {
        const container = el.matches('code') ? el.parentElement : el;
        const code = (el.matches('code') ? el : el.querySelector('code') || el).textContent;
        const div = document.createElement('div');
        div.className = 'mermaid';
        div.textContent = code;
        container.replaceWith(div);
        return div;
      });
      // useMaxWidth: false — 좁은 화면에서 축소하지 않고 .mermaid 영역 안에서 가로 스크롤한다.
      window.mermaid.initialize({ startOnLoad: false, theme: 'dark', securityLevel: 'strict', flowchart: { useMaxWidth: false } });
      window.mermaid.run({ nodes });
    };
    document.head.appendChild(script);
  }

  function init() {
    const body = document.querySelector('.project-body');
    const nav = document.getElementById('project-toc');
    if (!body || !nav) return;
    mountDemo(body);
    const headings = [...body.querySelectorAll('h2')];
    ensureHeadingIds(headings);
    buildToc(headings, nav);
    spyOnSections(headings, nav);
    renderMermaid(body);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
