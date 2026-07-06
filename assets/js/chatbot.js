(() => {
  const API_BASE = window.__PM_CHAT_API_BASE__ || 'https://portfolio.jhm9507.com'; // ← replace before deploy

  /* ── marked.js (CDN, async) ── */
  function loadMarked() {
    if (window.marked) return Promise.resolve();
    return new Promise((resolve) => {
      const s = document.createElement('script');
      s.src = 'https://cdn.jsdelivr.net/npm/marked@12/marked.min.js';
      s.onload = resolve;
      s.onerror = resolve; // fail silently — plain text fallback used
      document.head.appendChild(s);
    });
  }

  /* ── session_id ── */
  function getSessionId() {
    try {
      let id = localStorage.getItem('pm_session_id');
      if (!id) {
        id = crypto.randomUUID();
        localStorage.setItem('pm_session_id', id);
      }
      return id;
    } catch {
      return crypto.randomUUID();
    }
  }

  /* ── DOM ── */
  function buildDOM() {
    const fab = document.createElement('button');
    fab.id = 'pm-chat-fab';
    fab.setAttribute('aria-label', 'Portfolio Assistant 열기');
    fab.textContent = '💬';

    const popup = document.createElement('div');
    popup.id = 'pm-chat-popup';
    popup.setAttribute('role', 'dialog');
    popup.setAttribute('aria-label', 'Portfolio Assistant');
    popup.setAttribute('aria-modal', 'true');
    popup.innerHTML = `
      <div id="pm-chat-header">
        <div id="pm-chat-avatar">🤖</div>
        <div>
          <div id="pm-chat-title">Portfolio Assistant</div>
          <div id="pm-chat-subtitle">무엇이든 물어보세요</div>
        </div>
        <button id="pm-chat-close" aria-label="챗봇 닫기">✕</button>
      </div>
      <div id="pm-chat-notice">⚠ 베타 서비스입니다 — 서버가 불안정하거나 답변이 부정확할 수 있습니다.</div>
      <div id="pm-chat-messages"></div>
      <div id="pm-chat-input-row">
        <input id="pm-chat-input" type="text" placeholder="메시지를 입력하세요..." maxlength="500" aria-label="챗봇에게 질문 입력" />
        <button id="pm-chat-send" aria-label="전송">➤</button>
      </div>
    `;

    document.body.appendChild(fab);
    document.body.appendChild(popup);
    return { fab, popup };
  }

  /* ── Simple message (user / welcome) ── */
  function appendMessage(messages, role, text) {
    const div = document.createElement('div');
    div.className = `pm-msg pm-${role}`;
    div.textContent = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
    return div;
  }

  /* ── Streaming bot message: stage pill + bubble + entity bar ── */
  function appendBotMessage(messages) {
    const wrapper = document.createElement('div');
    wrapper.className = 'pm-bot-wrapper';

    // Stage indicator
    const stageBar = document.createElement('div');
    stageBar.className = 'pm-stage-bar';
    stageBar.innerHTML = `
      <div class="pm-stage-pill">
        <span class="pm-pill-spinner"></span>
        <span class="pm-pill-label">준비 중...</span>
      </div>`;

    // Answer bubble (hidden until first token arrives)
    const bubble = document.createElement('div');
    bubble.className = 'pm-msg pm-bot pm-streaming pm-hidden';
    const content = document.createElement('div');
    content.className = 'pm-content';
    bubble.appendChild(content);

    // Entity chips bar (shown when entities are found)
    const entityBar = document.createElement('div');
    entityBar.className = 'pm-entity-bar';

    wrapper.appendChild(stageBar);
    wrapper.appendChild(bubble);
    wrapper.appendChild(entityBar);
    messages.appendChild(wrapper);
    messages.scrollTop = messages.scrollHeight;

    return { stageBar, bubble, content, entityBar };
  }

  /* ── SSE stream ── */
  async function streamAnswer(question, { stageBar, bubble, content, entityBar }, messages, input, send, popup, signal) {
    const sessionId = getSessionId();
    const entitySet = new Set();
    let accumulated = '';

    const STAGE_LABELS = {
      analyzing: '쿼리 분석 중...',
      searching: '정보 검색 중...',
      answering: '답변 작성 중...',
    };

    function updateStageLabel(stage, loop) {
      const el = stageBar.querySelector('.pm-pill-label');
      if (!el) return;
      const base = STAGE_LABELS[stage] || stage;
      el.textContent = (stage === 'searching' && loop > 1)
        ? `정보 검색 중... (${loop}회)`
        : base;
    }

    function addEntityChips(entities) {
      entities.forEach((e, idx) => {
        if (entitySet.has(e.name)) return;
        entitySet.add(e.name);
        const chip = document.createElement('span');
        chip.className = 'pm-chat-chip';
        chip.style.animationDelay = `${idx * 60}ms`;
        chip.dataset.name = e.name;
        chip.textContent = e.name;
        entityBar.appendChild(chip);
      });
      if (entitySet.size > 0) entityBar.style.display = 'flex';
    }

    function markChipsDone() {
      entityBar.querySelectorAll('.pm-chat-chip').forEach(c => c.classList.add('pm-chip-done'));
    }

    try {
      const res = await fetch(`${API_BASE}/ask/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId, question, top_k: 5 }),
        signal,
      });

      if (!res.ok) {
        stageBar.classList.add('pm-hidden');
        bubble.classList.remove('pm-hidden', 'pm-streaming');
        content.textContent = '오류가 발생했습니다. 잠시 후 다시 시도해 주세요.';
        return;
      }

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buf = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buf += decoder.decode(value, { stream: true });
        const lines = buf.split('\n');
        buf = lines.pop();

        for (const line of lines) {
          if (!line.startsWith('data: ')) continue;
          let ev;
          try { ev = JSON.parse(line.slice(6)); } catch { continue; }

          if (ev.type === 'status') {
            updateStageLabel(ev.stage, ev.loop || 1);
          } else if (ev.type === 'entity_update') {
            addEntityChips(ev.entities || []);
          } else if (ev.type === 'token') {
            if (!accumulated) {
              stageBar.classList.add('pm-hidden');
              bubble.classList.remove('pm-hidden');
            }
            accumulated += ev.text;
            content.textContent = accumulated;
            messages.scrollTop = messages.scrollHeight;
          } else if (ev.type === 'done') {
            markChipsDone();
            stageBar.classList.add('pm-hidden');
            bubble.classList.remove('pm-hidden', 'pm-streaming');
            content.innerHTML = window.marked
              ? marked.parse(accumulated || '(답변 없음)')
              : (accumulated || '(답변 없음)');
            messages.scrollTop = messages.scrollHeight;
          }
        }
      }
    } catch (err) {
      if (err.name !== 'AbortError') {
        stageBar.classList.add('pm-hidden');
        bubble.classList.remove('pm-hidden', 'pm-streaming');
        content.textContent = '서버에 연결할 수 없습니다. API URL을 확인해 주세요.';
      }
    } finally {
      input.disabled = false;
      send.disabled = false;
      if (popup.classList.contains('pm-open')) input.focus();
    }
  }

  /* ── Init ── */
  function init() {
    loadMarked();

    const { fab, popup } = buildDOM();
    const messages = popup.querySelector('#pm-chat-messages');
    const input = popup.querySelector('#pm-chat-input');
    const send = popup.querySelector('#pm-chat-send');
    const close = popup.querySelector('#pm-chat-close');
    let welcomed = false;
    let abortCtrl = null;

    function openPopup() {
      popup.classList.add('pm-open');
      fab.setAttribute('aria-expanded', 'true');
      if (!welcomed) {
        welcomed = true;
        appendMessage(messages, 'bot', '안녕하세요! 전현민의 포트폴리오에 대해 궁금한 점이 있으신가요?');
      }
      input.focus();
    }

    function closePopup() {
      popup.classList.remove('pm-open');
      fab.setAttribute('aria-expanded', 'false');
      if (abortCtrl) { abortCtrl.abort(); abortCtrl = null; }
    }

    fab.addEventListener('click', () => {
      popup.classList.contains('pm-open') ? closePopup() : openPopup();
    });
    close.addEventListener('click', closePopup);

    async function handleSend() {
      const question = input.value.trim();
      if (!question || input.disabled) return;
      input.value = '';
      input.disabled = true;
      send.disabled = true;
      appendMessage(messages, 'user', question);
      const refs = appendBotMessage(messages);
      abortCtrl = new AbortController();
      await streamAnswer(question, refs, messages, input, send, popup, abortCtrl.signal);
      abortCtrl = null;
    }

    send.addEventListener('click', handleSend);
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend(); }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
