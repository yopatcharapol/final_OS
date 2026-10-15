/**
 * OS Final Exam Prep - Core Interactive Engine
 * Handles Navigation, Theme Toggling, Live Calculators, Simulators & Practice Quiz
 */

document.addEventListener('DOMContentLoaded', () => {
  initNavigation();
  initTheme();
  initEmatCalculator();
  initPageReplacementSimulator();
  initBankersAlgorithmSimulator();
  initQuiz();
  initSearch();
});

/* ==========================================================================
   1. NAVIGATION & TAB SWITCHING
   ========================================================================== */
function initNavigation() {
  const navItems = document.querySelectorAll('.nav-item');
  const sections = document.querySelectorAll('.chapter-section');
  const mobileMenuBtn = document.getElementById('mobileMenuBtn');
  const sidebar = document.getElementById('sidebar');

  window.switchTab = function(targetTabId) {
    navItems.forEach(item => {
      if (item.getAttribute('data-tab') === targetTabId) {
        item.classList.add('active');
      } else {
        item.classList.remove('active');
      }
    });

    sections.forEach(sec => {
      if (sec.id === `tab-${targetTabId}`) {
        sec.classList.add('active');
      } else {
        sec.classList.remove('active');
      }
    });

    window.scrollTo({ top: 0, behavior: 'smooth' });

    if (sidebar && sidebar.classList.contains('open')) {
      sidebar.classList.remove('open');
    }
  };

  navItems.forEach(item => {
    item.addEventListener('click', (e) => {
      e.preventDefault();
      const target = item.getAttribute('data-tab');
      if (target) switchTab(target);
    });
  });

  if (mobileMenuBtn && sidebar) {
    mobileMenuBtn.addEventListener('click', () => {
      sidebar.classList.toggle('open');
    });
  }

  const quickQuizBtn = document.getElementById('quickQuizBtn');
  if (quickQuizBtn) {
    quickQuizBtn.addEventListener('click', () => switchTab('quiz'));
  }
}

/* ==========================================================================
   2. THEME TOGGLING (DARK / LIGHT)
   ========================================================================== */
function initTheme() {
  const themeBtn = document.getElementById('themeToggleBtn');
  const root = document.documentElement;

  const savedTheme = localStorage.getItem('os_prep_theme') || 'dark';
  root.setAttribute('data-theme', savedTheme);
  updateThemeIcon(savedTheme);

  if (themeBtn) {
    themeBtn.addEventListener('click', () => {
      const current = root.getAttribute('data-theme');
      const nextTheme = current === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', nextTheme);
      localStorage.setItem('os_prep_theme', nextTheme);
      updateThemeIcon(nextTheme);
    });
  }

  function updateThemeIcon(theme) {
    if (!themeBtn) return;
    const icon = themeBtn.querySelector('i');
    if (!icon) return;
    if (theme === 'light') {
      icon.className = 'fa-solid fa-sun';
      icon.style.color = '#f59e0b';
    } else {
      icon.className = 'fa-solid fa-moon';
      icon.style.color = 'var(--text-muted)';
    }
  }
}

/* ==========================================================================
   3. SEARCH & KEYWORD HIGHLIGHTING
   ========================================================================== */
function initSearch() {
  const searchInput = document.getElementById('searchInput');
  if (!searchInput) return;

  const topicKeywords = {
    'deadlock': 'ch5',
    'banker': 'ch5',
    'rag': 'ch5',
    'coffman': 'ch5',
    'circular': 'ch5',
    'prevention': 'ch5',
    'avoidance': 'ch5',
    'scheduling': 'ch6',
    'sjf': 'ch6',
    'srtf': 'ch6',
    'fcfs': 'ch6',
    'round robin': 'ch6',
    'gantt': 'ch6',
    'aging': 'ch6',
    'starvation': 'ch6',
    'priority': 'ch6',
    'memory': 'ch7',
    'paging': 'ch7',
    'tlb': 'ch7',
    'emat': 'ch7',
    'fragmentation': 'ch7',
    'first-fit': 'ch7',
    'best-fit': 'ch7',
    'worst-fit': 'ch7',
    'virtual': 'ch8',
    'page fault': 'ch8',
    'thrashing': 'ch8',
    'fifo': 'ch8',
    'lru': 'ch8',
    'belady': 'ch8',
    'working set': 'ch8',
    'work-stealing': 'advanced',
    'heap': 'advanced',
    'stack': 'advanced',
    'quiz': 'quiz',
    'calculator': 'calculators',
    'simulator': 'calculators'
  };

  searchInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      const q = searchInput.value.trim().toLowerCase();
      if (!q) return;

      for (const [key, tab] of Object.entries(topicKeywords)) {
        if (q.includes(key)) {
          window.switchTab(tab);
          searchInput.blur();
          return;
        }
      }

      window.switchTab('overview');
      searchInput.blur();
    }
  });
}

/* ==========================================================================
   4. EMAT INTERACTIVE CALCULATOR
   ========================================================================== */
function initEmatCalculator() {
  const hitInput = document.getElementById('calc-hit-ratio');
  const tlbInput = document.getElementById('calc-tlb-time');
  const ramInput = document.getElementById('calc-ram-time');

  const resultVal = document.getElementById('ematResultVal');
  const explanation = document.getElementById('ematExplanation');

  function calculateEMAT() {
    if (!hitInput || !tlbInput || !ramInput || !resultVal) return;

    let hitPercent = parseFloat(hitInput.value);
    let tlbTime = parseFloat(tlbInput.value);
    let ramTime = parseFloat(ramInput.value);

    if (isNaN(hitPercent) || hitPercent < 0) hitPercent = 0;
    if (hitPercent > 100) hitPercent = 100;
    if (isNaN(tlbTime) || tlbTime < 0) tlbTime = 0;
    if (isNaN(ramTime) || ramTime < 0) ramTime = 0;

    const alpha = hitPercent / 100;
    const hitComponent = alpha * (tlbTime + ramTime);
    const missComponent = (1 - alpha) * (tlbTime + 2 * ramTime);
    const emat = hitComponent + missComponent;

    resultVal.textContent = `${emat.toFixed(2)} ns`;

    if (explanation) {
      explanation.innerHTML = `
        <strong>สูตร:</strong> EMAT = α(t_tlb + t_mem) + (1 - α)(t_tlb + 2 × t_mem)<br>
        = ${alpha.toFixed(2)} × (${tlbTime} + ${ramTime}) + ${(1 - alpha).toFixed(2)} × (${tlbTime} + 2 × ${ramTime})<br>
        = ${hitComponent.toFixed(2)} + ${missComponent.toFixed(2)} = <span style="color: var(--accent-cyan); font-weight: 700;">${emat.toFixed(2)} ns</span>
      `;
    }
  }

  [hitInput, tlbInput, ramInput].forEach(inp => {
    if (inp) inp.addEventListener('input', calculateEMAT);
  });

  calculateEMAT();
}

/* ==========================================================================
   5. PAGE REPLACEMENT SIMULATOR (FIFO vs LRU)
   ========================================================================== */
function initPageReplacementSimulator() {
  const refInput = document.getElementById('sim-ref-string');
  const framesInput = document.getElementById('sim-frames');
  const runBtn = document.getElementById('runSimBtn');

  if (!runBtn) return;

  function runSimulation() {
    const rawStr = refInput.value;
    const numFrames = parseInt(framesInput.value, 10) || 3;

    // Parse reference string
    const tokens = rawStr.split(/[\s,]+/).filter(t => t.trim().length > 0);
    const refPages = tokens.map(t => parseInt(t, 10)).filter(n => !isNaN(n));

    if (refPages.length === 0) {
      alert('กรุณาป้อน Reference String ที่ถูกต้องอย่างน้อย 1 หน้า');
      return;
    }

    // Run FIFO
    const fifoResult = simulateFIFO(refPages, numFrames);
    renderSimResult('fifo', fifoResult);

    // Run LRU
    const lruResult = simulateLRU(refPages, numFrames);
    renderSimResult('lru', lruResult);
  }

  function simulateFIFO(pages, maxFrames) {
    const frames = [];
    let faults = 0;
    const history = [];

    pages.forEach((page, step) => {
      const hit = frames.includes(page);
      if (!hit) {
        faults++;
        if (frames.length < maxFrames) {
          frames.push(page);
        } else {
          frames.shift(); // Remove oldest
          frames.push(page);
        }
      }
      history.push({ step: step + 1, page, hit, frames: [...frames] });
    });

    return {
      faults,
      total: pages.length,
      hitRate: ((pages.length - faults) / pages.length) * 100,
      history
    };
  }

  function simulateLRU(pages, maxFrames) {
    const frames = [];
    const lastUsed = new Map();
    let faults = 0;
    const history = [];

    pages.forEach((page, step) => {
      const hit = frames.includes(page);
      lastUsed.set(page, step);

      if (!hit) {
        faults++;
        if (frames.length < maxFrames) {
          frames.push(page);
        } else {
          // Find page with lowest step in lastUsed
          let lruPage = frames[0];
          let minTime = lastUsed.get(frames[0]);
          for (let i = 1; i < frames.length; i++) {
            const t = lastUsed.get(frames[i]);
            if (t < minTime) {
              minTime = t;
              lruPage = frames[i];
            }
          }
          const replaceIdx = frames.indexOf(lruPage);
          frames[replaceIdx] = page;
        }
      }
      history.push({ step: step + 1, page, hit, frames: [...frames] });
    });

    return {
      faults,
      total: pages.length,
      hitRate: ((pages.length - faults) / pages.length) * 100,
      history
    };
  }

  function renderSimResult(type, res) {
    const faultEl = document.getElementById(`${type}FaultCount`);
    const hitRateEl = document.getElementById(`${type}HitRate`);
    const timelineEl = document.getElementById(`${type}Timeline`);

    if (faultEl) faultEl.textContent = `Page Faults: ${res.faults} ครั้ง`;
    if (hitRateEl) hitRateEl.textContent = `Hit Ratio: ${res.hitRate.toFixed(1)}% (Hits: ${res.total - res.faults} / ${res.total})`;

    if (timelineEl) {
      let html = '<div style="display: flex; flex-direction: column; gap: 0.35rem;">';
      res.history.forEach(item => {
        const badgeColor = item.hit ? '#34d399' : '#fb7185';
        const badgeText = item.hit ? 'HIT' : 'FAULT';
        html += `
          <div style="display: flex; align-items: center; justify-content: space-between; padding: 0.2rem 0.4rem; border-bottom: 1px solid var(--border-color);">
            <span>#${item.step} [Page <strong>${item.page}</strong>] : [${item.frames.join(', ')}]</span>
            <span style="font-weight: 700; color: ${badgeColor}; font-size: 0.75rem;">${badgeText}</span>
          </div>
        `;
      });
      html += '</div>';
      timelineEl.innerHTML = html;
    }
  }

  runBtn.addEventListener('click', runSimulation);
  runSimulation();
}

/* ==========================================================================
   5.5. INTERACTIVE BANKER'S ALGORITHM VISUAL SIMULATOR
   ========================================================================== */
function initBankersAlgorithmSimulator() {
  const presetSelect = document.getElementById('bankerPresetSelect');
  const prevBtn = document.getElementById('bankerPrevBtn');
  const nextBtn = document.getElementById('bankerNextBtn');
  const autoBtn = document.getElementById('bankerAutoBtn');
  const resetBtn = document.getElementById('bankerResetBtn');

  const workVal = document.getElementById('bankerWorkVal');
  const workSub = document.getElementById('bankerWorkSub');
  const seqVal = document.getElementById('bankerSeqVal');
  const progressSub = document.getElementById('bankerProgressSub');
  const tableBody = document.getElementById('bankerTableBody');

  const stepBox = document.getElementById('bankerStepBox');
  const stepBadge = document.getElementById('bankerStepBadge');
  const stepTitle = document.getElementById('bankerStepTitle');
  const stepStatus = document.getElementById('bankerStepStatus');
  const stepContent = document.getElementById('bankerStepContent');

  if (!presetSelect || !tableBody) return;

  let currentPresetKey = 'hw5';
  let currentStepIndex = 0;
  let autoPlayTimer = null;

  // Preset Datasets with complete step-by-step vector arithmetic and explanations
  const presets = {
    hw5: {
      name: 'โจทย์จริงการบ้าน HW5 (Total: [10, 6, 8]) — Safe State',
      total: [10, 6, 8],
      processes: ['P0', 'P1', 'P2', 'P3', 'P4'],
      alloc: [[0, 1, 1], [2, 0, 2], [3, 1, 3], [2, 1, 1], [1, 1, 0]],
      max: [[7, 4, 3], [3, 2, 2], [9, 1, 4], [4, 2, 2], [5, 3, 3]],
      need: [[7, 3, 2], [1, 2, 0], [6, 0, 1], [2, 1, 1], [4, 2, 3]],
      steps: [
        {
          stepNum: 0,
          title: 'จุดเริ่มต้น: คำนวณเงินสดในตู้เซฟว่าง (Available ณ เวลา T0)',
          statusBadge: 'พร้อมทำงาน',
          statusBadgeClass: 'badge-eval',
          boxClass: 'eval-init',
          work: [2, 2, 1],
          workSub: 'คำนวณจาก Total [10, 6, 8] ลบยอดแจก [8, 4, 7] = [2, 2, 1]',
          finish: [false, false, false, false, false],
          safeSeq: [],
          evalIdx: -1,
          rowStatus: ['waiting', 'waiting', 'waiting', 'waiting', 'waiting'],
          rowResults: ['-', '-', '-', '-', '-'],
          mathGrid: [
            { label: 'ทรัพยากรทั้งหมด (Total)', val: '[ A: 10, B: 6, C: 8 ]' },
            { label: 'ผลรวมที่แจกไปแล้ว (∑ Allocation)', val: '[ A: 8, B: 4, C: 7 ]' },
            { label: 'Available เริ่มต้น (Total - ∑ Alloc)', val: '[ A: 2, B: 2, C: 1 ]' }
          ],
          thought: 'ระบบเริ่มต้นด้วยเงินสดในตู้เซฟ <code>Available = [2, 2, 1]</code> ทุกโปรเซสยังมีสถานะ <code>Finish = False</code> ต่อไประบบจะกวาดสายตาหาโปรเซสที่เงินที่ยังขาดอยู่ (<code>Need</code>) ไม่เกินเงินในตู้เซฟ (<code>Work</code>) เพื่อปล่อยกู้ให้ทำงานจนเสร็จ!'
        },
        {
          stepNum: 1,
          title: 'รอบที่ 1: ตรวจสอบ P0 — ทรัพยากรไม่เพียงพอ (Need > Work ข้ามก่อน)',
          statusBadge: 'ของไม่พอ (ข้ามก่อน)',
          statusBadgeClass: 'badge-skipped',
          boxClass: 'eval-fail',
          work: [2, 2, 1],
          workSub: 'ตู้เซฟยังคงเดิม [2, 2, 1] (ไม่มีโปรเซสคืนของ)',
          finish: [false, false, false, false, false],
          safeSeq: [],
          evalIdx: 0,
          rowStatus: ['skipped', 'waiting', 'waiting', 'waiting', 'waiting'],
          rowResults: ['❌ Need > Work (ไม่พอ)', '-', '-', '-', '-'],
          proc: 'P0',
          need: [7, 3, 2],
          workBefore: [2, 2, 1],
          comp: [
            { res: 'A', need: 7, work: 2, pass: false },
            { res: 'B', need: 3, work: 2, pass: false },
            { res: 'C', need: 2, work: 1, pass: false }
          ],
          thought: 'ธนาคารมองลูกค้า P0 พบว่า P0 ต้องการเงินเพิ่มอีก <code>[7, 3, 2]</code> แต่เงินสดในตู้เซฟมีเพียง <code>[2, 2, 1]</code> (ขาด A อีก 5, ขาด B อีก 1, ขาด C อีก 1) ทรัพยากรไม่พอทุกแกน! ถ้าปล่อยกู้ไปตอนนี้ P0 ก็ยังสร้างบ้านไม่เสร็จ แถมเงินในเซฟจะติดลบ/หมดเกลี้ยง → ธนาคารจึง <strong>"พัก P0 ไว้ก่อน"</strong> แล้วเลื่อนไปดูลูกค้ารายถัดไป'
        },
        {
          stepNum: 2,
          title: 'รอบที่ 2: ตรวจสอบ P1 — ทรัพยากรพอ! ได้รับจัดสรรและคืนของเข้าเซฟ',
          statusBadge: 'ผ่านเกณฑ์! (Need ≤ Work)',
          statusBadgeClass: 'badge-finished',
          boxClass: 'eval-pass',
          work: [4, 2, 3],
          workSub: 'Work ใหม่ = [2, 2, 1] + Allocation(P1) [2, 0, 2] = [4, 2, 3]',
          finish: [false, true, false, false, false],
          safeSeq: ['P1'],
          evalIdx: 1,
          rowStatus: ['skipped', 'passed', 'waiting', 'waiting', 'waiting'],
          rowResults: ['❌ Need > Work (ไม่พอ)', '✔ Need ≤ Work (ผ่าน!)', '-', '-', '-'],
          proc: 'P1',
          need: [1, 2, 0],
          workBefore: [2, 2, 1],
          alloc: [2, 0, 2],
          workAfter: [4, 2, 3],
          comp: [
            { res: 'A', need: 1, work: 2, pass: true },
            { res: 'B', need: 2, work: 2, pass: true },
            { res: 'C', need: 0, work: 1, pass: true }
          ],
          thought: 'ยอดเยี่ยม! ลูกค้า P1 ขาดเงินเพิ่มเพียง <code>[1, 2, 0]</code> ซึ่งตู้เซฟเรามี <code>[2, 2, 1]</code> จัดสรรให้ได้ครบทุกทรัพยากร! เมื่อ P1 ได้เงินครบเขาก็ทำงานจนเสร็จสมบูรณ์ และ <strong>"คืนเงินที่เคยกู้ไว้ทั้งหมด (Allocation = [2, 0, 2]) กลับเข้าตู้เซฟ"</strong> ส่งผลให้ตู้เซฟเรามีเงินพุ่งขึ้นเป็น <code>[4, 2, 3]</code>! บันทึกลำดับปลอดภัย: ⟨ P1 ⟩'
        },
        {
          stepNum: 3,
          title: 'รอบที่ 3: ตรวจสอบ P2 — ทรัพยากร A ยังไม่เพียงพอ (ข้ามไปก่อน)',
          statusBadge: 'ของไม่พอ (ข้ามก่อน)',
          statusBadgeClass: 'badge-skipped',
          boxClass: 'eval-fail',
          work: [4, 2, 3],
          workSub: 'ตู้เซฟยังคงเดิม [4, 2, 3] (พัก P2 ไว้ก่อน)',
          finish: [false, true, false, false, false],
          safeSeq: ['P1'],
          evalIdx: 2,
          rowStatus: ['skipped', 'passed', 'skipped', 'waiting', 'waiting'],
          rowResults: ['❌ Need > Work (ไม่พอ)', '✔ Need ≤ Work (ผ่าน!)', '❌ Need > Work (A ขาด 2)', '-', '-'],
          proc: 'P2',
          need: [6, 0, 1],
          workBefore: [4, 2, 3],
          comp: [
            { res: 'A', need: 6, work: 4, pass: false },
            { res: 'B', need: 0, work: 2, pass: true },
            { res: 'C', need: 1, work: 3, pass: true }
          ],
          thought: 'ลูกค้า P2 ต้องการทรัพยากร A ถึง 6 ชิ้น แต่ในตู้เซฟมี A แค่ 4 ชิ้น (แม้ว่า B และ C จะพอ แต่กฎเกณฑ์ของ Safety Algorithm คือ <strong>"ต้องผ่านทุกแกนพร้อมกัน 100%"</strong>) → ธนาคารจึง <strong>"พัก P2 ไว้ก่อน"</strong> เพื่อไปหาลูกค้ารายอื่นที่ต้องการของน้อยกว่า'
        },
        {
          stepNum: 4,
          title: 'รอบที่ 4: ตรวจสอบ P3 — ทรัพยากรพอ! จัดสรรและรับคืน Allocation',
          statusBadge: 'ผ่านเกณฑ์! (Need ≤ Work)',
          statusBadgeClass: 'badge-finished',
          boxClass: 'eval-pass',
          work: [6, 3, 4],
          workSub: 'Work ใหม่ = [4, 2, 3] + Allocation(P3) [2, 1, 1] = [6, 3, 4]',
          finish: [false, true, false, true, false],
          safeSeq: ['P1', 'P3'],
          evalIdx: 3,
          rowStatus: ['skipped', 'passed', 'skipped', 'passed', 'waiting'],
          rowResults: ['❌ Need > Work (ไม่พอ)', '✔ Need ≤ Work (ผ่าน!)', '❌ Need > Work (A ขาด 2)', '✔ Need ≤ Work (ผ่าน!)', '-'],
          proc: 'P3',
          need: [2, 1, 1],
          workBefore: [4, 2, 3],
          alloc: [2, 1, 1],
          workAfter: [6, 3, 4],
          comp: [
            { res: 'A', need: 2, work: 4, pass: true },
            { res: 'B', need: 1, work: 2, pass: true },
            { res: 'C', need: 1, work: 3, pass: true }
          ],
          thought: 'ลูกค้า P3 ต้องการเพียง <code>[2, 1, 1]</code> ซึ่งในตู้เซฟมี <code>[4, 2, 3]</code> เหลือเฟือ! P3 ได้รับจัดสรรจนเสร็จและคืน Allocation <code>[2, 1, 1]</code> กลับเข้าตู้เซฟ ทำให้เงินในเซฟพุ่งขึ้นเป็น <code>[6, 3, 4]</code> ทันที! ลำดับปลอดภัยสะสม: ⟨ P1, P3 ⟩'
        },
        {
          stepNum: 5,
          title: 'รอบที่ 5: วนกลับมาตรวจ P2 — ครั้งนี้ผ่านฉลุยเพราะเซฟรวยขึ้นแล้ว!',
          statusBadge: 'ผ่านเกณฑ์! (Need ≤ Work)',
          statusBadgeClass: 'badge-finished',
          boxClass: 'eval-pass',
          work: [9, 4, 7],
          workSub: 'Work ใหม่ = [6, 3, 4] + Allocation(P2) [3, 1, 3] = [9, 4, 7]',
          finish: [false, true, true, true, false],
          safeSeq: ['P1', 'P3', 'P2'],
          evalIdx: 2,
          rowStatus: ['skipped', 'passed', 'passed', 'passed', 'waiting'],
          rowResults: ['❌ Need > Work (ไม่พอ)', '✔ Need ≤ Work (ผ่าน!)', '✔ Need ≤ Work (ผ่านแล้ว!)', '✔ Need ≤ Work (ผ่าน!)', '-'],
          proc: 'P2',
          need: [6, 0, 1],
          workBefore: [6, 3, 4],
          alloc: [3, 1, 3],
          workAfter: [9, 4, 7],
          comp: [
            { res: 'A', need: 6, work: 6, pass: true },
            { res: 'B', need: 0, work: 3, pass: true },
            { res: 'C', need: 1, work: 4, pass: true }
          ],
          thought: 'นี่คือหัวใจของ Banker\'s Algorithm! ก่อนหน้านี้ P2 ขาดทรัพยากร A เพราะเรามีแค่ 4 แต่ตอนนี้หลังจาก P1 และ P3 ทยอยคืนของมา เซฟเรามี A ถึง 6 ตัวแล้ว (6 ≤ 6 พอดีเป๊ะ!) P2 จึงรันเสร็จและคืนก้อนใหญ่ <code>[3, 1, 3]</code> เซฟเรากลายเป็น <code>[9, 4, 7]</code> มหาศาล! ลำดับปลอดภัย: ⟨ P1, P3, P2 ⟩'
        },
        {
          stepNum: 6,
          title: 'รอบที่ 6: วนกลับมาตรวจ P0 — ทรัพยากรเหลือเฟือ ผ่านสบาย!',
          statusBadge: 'ผ่านเกณฑ์! (Need ≤ Work)',
          statusBadgeClass: 'badge-finished',
          boxClass: 'eval-pass',
          work: [9, 5, 8],
          workSub: 'Work ใหม่ = [9, 4, 7] + Allocation(P0) [0, 1, 1] = [9, 5, 8]',
          finish: [true, true, true, true, false],
          safeSeq: ['P1', 'P3', 'P2', 'P0'],
          evalIdx: 0,
          rowStatus: ['passed', 'passed', 'passed', 'passed', 'waiting'],
          rowResults: ['✔ Need ≤ Work (ผ่านแล้ว!)', '✔ Need ≤ Work (ผ่าน!)', '✔ Need ≤ Work (ผ่านแล้ว!)', '✔ Need ≤ Work (ผ่าน!)', '-'],
          proc: 'P0',
          need: [7, 3, 2],
          workBefore: [9, 4, 7],
          alloc: [0, 1, 1],
          workAfter: [9, 5, 8],
          comp: [
            { res: 'A', need: 7, work: 9, pass: true },
            { res: 'B', need: 3, work: 4, pass: true },
            { res: 'C', need: 2, work: 7, pass: true }
          ],
          thought: 'ลูกค้า P0 ที่เคยขอเยอะมาก <code>[7, 3, 2]</code> จนตอนแรกสุดเราต้องข้าม คราวนี้ตู้เซฟเรามี <code>[9, 4, 7]</code> เหลือล้นแล้ว! P0 จึงทำงานเสร็จและคืนของ <code>[0, 1, 1]</code> เซฟกลายเป็น <code>[9, 5, 8]</code>! ลำดับปลอดภัย: ⟨ P1, P3, P2, P0 ⟩'
        },
        {
          stepNum: 7,
          title: 'รอบที่ 7: ตรวจสอบ P4 — โปรเซสสุดท้ายจบสมบูรณ์ คืนทรัพยากรครบ 100%',
          statusBadge: 'ผ่านเกณฑ์! ครบทุกโปรเซส',
          statusBadgeClass: 'badge-finished',
          boxClass: 'eval-pass',
          work: [10, 6, 8],
          workSub: 'Work ใหม่ = [9, 5, 8] + Allocation(P4) [1, 1, 0] = Total [10, 6, 8]',
          finish: [true, true, true, true, true],
          safeSeq: ['P1', 'P3', 'P2', 'P0', 'P4'],
          evalIdx: 4,
          rowStatus: ['passed', 'passed', 'passed', 'passed', 'passed'],
          rowResults: ['✔ Finish = True', '✔ Finish = True', '✔ Finish = True', '✔ Finish = True', '✔ Need ≤ Work (ผ่าน!)'],
          proc: 'P4',
          need: [4, 2, 3],
          workBefore: [9, 5, 8],
          alloc: [1, 1, 0],
          workAfter: [10, 6, 8],
          comp: [
            { res: 'A', need: 4, work: 9, pass: true },
            { res: 'B', need: 2, work: 5, pass: true },
            { res: 'C', need: 3, work: 8, pass: true }
          ],
          thought: 'โปรเซสสุดท้าย P4 ต้องการ <code>[4, 2, 3]</code> เซฟมี <code>[9, 5, 8]</code> ผ่านฉลุย! เมื่อ P4 ทำงานเสร็จและคืนของ <code>[1, 1, 0]</code> ทรัพยากรทั้งหมดในระบบจะกลับคืนสู่คลังครบ <code>[10, 6, 8]</code> เท่ากับ Total เริ่มต้น 100% เต็ม!'
        },
        {
          stepNum: 8,
          title: '🎉 สำเร็จ! ยืนยันสถานะปลอดภัย (Safe State 100% ไร้ Deadlock แน่นอน)',
          statusBadge: 'Safe State ยืนยันแล้ว',
          statusBadgeClass: 'badge-finished',
          boxClass: 'eval-complete',
          work: [10, 6, 8],
          workSub: 'ทรัพยากรทุกชิ้นถูกคืนเข้าสู่ตู้เซฟครบถ้วนสมบูรณ์',
          finish: [true, true, true, true, true],
          safeSeq: ['P1', 'P3', 'P2', 'P0', 'P4'],
          evalIdx: -1,
          rowStatus: ['passed', 'passed', 'passed', 'passed', 'passed'],
          rowResults: ['✔ Finish = True', '✔ Finish = True', '✔ Finish = True', '✔ Finish = True', '✔ Finish = True'],
          mathGrid: [
            { label: 'ผลรวมโปรเซสที่เสร็จสิ้น', val: 'Finish[i] = True ครบ 5/5 โปรเซส' },
            { label: 'ลำดับปลอดภัยที่ได้ (Safe Sequence)', val: '⟨ P1, P3, P2, P0, P4 ⟩' },
            { label: 'สถานะความปลอดภัยของระบบ', val: 'Safe State (ปลอดภัย 100%)' }
          ],
          thought: 'เนื่องจากอัลกอริทึมสามารถค้นพบลำดับการรันที่ทำให้ทุกโปรเซสทำงานเสร็จสิ้นสมบูรณ์ได้โดยไม่มีใครต้องรอค้างคอยตลอดกาล นั่นคือ <strong>Safe Sequence: ⟨ P1, P3, P2, P0, P4 ⟩</strong> ระบบนี้จึงการันตีว่าอยู่ใน <strong>"Safe State"</strong> และจะไม่มีวันเกิดสภาวะ Deadlock อย่างแน่นอนตามหลักวิชาการ!'
        }
      ]
    },

    silberschatz: {
      name: 'โจทย์ในสไลด์ Silberschatz (Total: [10, 5, 7]) — Safe State',
      total: [10, 5, 7],
      processes: ['P0', 'P1', 'P2', 'P3', 'P4'],
      alloc: [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]],
      max: [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]],
      need: [[7, 4, 3], [1, 2, 2], [6, 0, 0], [0, 1, 1], [4, 3, 1]],
      steps: [
        {
          stepNum: 0,
          title: 'จุดเริ่มต้น: คลัง Silberschatz Available = [3, 3, 2]',
          statusBadge: 'พร้อมทำงาน',
          statusBadgeClass: 'badge-eval',
          boxClass: 'eval-init',
          work: [3, 3, 2],
          workSub: 'คำนวณจาก Total [10, 5, 7] ลบยอดแจก [7, 2, 5] = [3, 3, 2]',
          finish: [false, false, false, false, false],
          safeSeq: [],
          evalIdx: -1,
          rowStatus: ['waiting', 'waiting', 'waiting', 'waiting', 'waiting'],
          rowResults: ['-', '-', '-', '-', '-'],
          mathGrid: [
            { label: 'Total Resources', val: '[ A: 10, B: 5, C: 7 ]' },
            { label: '∑ Allocation', val: '[ A: 7, B: 2, C: 5 ]' },
            { label: 'Available (T0)', val: '[ A: 3, B: 3, C: 2 ]' }
          ],
          thought: 'โจทย์ตัวอย่างคลาสสิกจากตำรา Silberschatz: Available เริ่มต้นคือ <code>[3, 3, 2]</code> เริ่มสแกนโปรเซสเพื่อค้นหา Safe Sequence'
        },
        {
          stepNum: 1,
          title: 'รอบที่ 1: ตรวจ P0 (Need: [7, 4, 3] vs Work: [3, 3, 2]) → ไม่พอ ข้ามก่อน',
          statusBadge: 'ของไม่พอ (ข้ามก่อน)',
          statusBadgeClass: 'badge-skipped',
          boxClass: 'eval-fail',
          work: [3, 3, 2],
          workSub: 'เซฟยังคงเดิม [3, 3, 2]',
          finish: [false, false, false, false, false],
          safeSeq: [],
          evalIdx: 0,
          rowStatus: ['skipped', 'waiting', 'waiting', 'waiting', 'waiting'],
          rowResults: ['❌ Need > Work (ไม่พอ)', '-', '-', '-', '-'],
          proc: 'P0',
          need: [7, 4, 3],
          workBefore: [3, 3, 2],
          comp: [
            { res: 'A', need: 7, work: 3, pass: false },
            { res: 'B', need: 4, work: 3, pass: false },
            { res: 'C', need: 3, work: 2, pass: false }
          ],
          thought: 'P0 ขาด [7, 4, 3] แต่เซฟมีแค่ [3, 3, 2] ไม่พอทุกทรัพยากร → พัก P0 ไว้ก่อน'
        },
        {
          stepNum: 2,
          title: 'รอบที่ 2: ตรวจ P1 (Need: [1, 2, 2] vs Work: [3, 3, 2]) → ผ่านฉลุย!',
          statusBadge: 'ผ่านเกณฑ์! (Need ≤ Work)',
          statusBadgeClass: 'badge-finished',
          boxClass: 'eval-pass',
          work: [5, 3, 2],
          workSub: 'Work ใหม่ = [3, 3, 2] + Allocation(P1) [2, 0, 0] = [5, 3, 2]',
          finish: [false, true, false, false, false],
          safeSeq: ['P1'],
          evalIdx: 1,
          rowStatus: ['skipped', 'passed', 'waiting', 'waiting', 'waiting'],
          rowResults: ['❌ Need > Work (ไม่พอ)', '✔ Need ≤ Work (ผ่าน!)', '-', '-', '-'],
          proc: 'P1',
          need: [1, 2, 2],
          workBefore: [3, 3, 2],
          alloc: [2, 0, 0],
          workAfter: [5, 3, 2],
          comp: [
            { res: 'A', need: 1, work: 3, pass: true },
            { res: 'B', need: 2, work: 3, pass: true },
            { res: 'C', need: 2, work: 2, pass: true }
          ],
          thought: 'P1 ต้องการ [1, 2, 2] ตู้เซฟมี [3, 3, 2] เพียงพอ! P1 คืน Allocation [2, 0, 0] เซฟกลายเป็น [5, 3, 2]! บันทึก ⟨ P1 ⟩'
        },
        {
          stepNum: 3,
          title: 'รอบที่ 3: ตรวจ P3 (Need: [0, 1, 1] vs Work: [5, 3, 2]) → ผ่านสบาย!',
          statusBadge: 'ผ่านเกณฑ์! (Need ≤ Work)',
          statusBadgeClass: 'badge-finished',
          boxClass: 'eval-pass',
          work: [7, 4, 3],
          workSub: 'Work ใหม่ = [5, 3, 2] + Allocation(P3) [2, 1, 1] = [7, 4, 3]',
          finish: [false, true, false, true, false],
          safeSeq: ['P1', 'P3'],
          evalIdx: 3,
          rowStatus: ['skipped', 'passed', 'skipped', 'passed', 'waiting'],
          rowResults: ['❌ Need > Work (ไม่พอ)', '✔ Need ≤ Work (ผ่าน!)', '-', '✔ Need ≤ Work (ผ่าน!)', '-'],
          proc: 'P3',
          need: [0, 1, 1],
          workBefore: [5, 3, 2],
          alloc: [2, 1, 1],
          workAfter: [7, 4, 3],
          comp: [
            { res: 'A', need: 0, work: 5, pass: true },
            { res: 'B', need: 1, work: 3, pass: true },
            { res: 'C', need: 1, work: 2, pass: true }
          ],
          thought: 'ข้าม P2 ไปก่อนเพราะ Need[P2] = [6, 0, 0] > Work_A(5) มาตรวจ P3 ต้องการเพียง [0, 1, 1] ผ่านทันที! คืน Allocation [2, 1, 1] เซฟเพิ่มเป็น [7, 4, 3]! ลำดับปลอดภัย: ⟨ P1, P3 ⟩'
        },
        {
          stepNum: 4,
          title: 'รอบที่ 4: ตรวจ P4 (Need: [4, 3, 1] vs Work: [7, 4, 3]) → ผ่านฉลุย!',
          statusBadge: 'ผ่านเกณฑ์! (Need ≤ Work)',
          statusBadgeClass: 'badge-finished',
          boxClass: 'eval-pass',
          work: [7, 4, 5],
          workSub: 'Work ใหม่ = [7, 4, 3] + Allocation(P4) [0, 0, 2] = [7, 4, 5]',
          finish: [false, true, false, true, true],
          safeSeq: ['P1', 'P3', 'P4'],
          evalIdx: 4,
          rowStatus: ['skipped', 'passed', 'skipped', 'passed', 'passed'],
          rowResults: ['❌ Need > Work (ไม่พอ)', '✔ Need ≤ Work (ผ่าน!)', '-', '✔ Need ≤ Work (ผ่าน!)', '✔ Need ≤ Work (ผ่าน!)'],
          proc: 'P4',
          need: [4, 3, 1],
          workBefore: [7, 4, 3],
          alloc: [0, 0, 2],
          workAfter: [7, 4, 5],
          comp: [
            { res: 'A', need: 4, work: 7, pass: true },
            { res: 'B', need: 3, work: 4, pass: true },
            { res: 'C', need: 1, work: 3, pass: true }
          ],
          thought: 'P4 ต้องการ [4, 3, 1] ในเซฟมี [7, 4, 3] ผ่านหมด! P4 คืน [0, 0, 2] เซฟเพิ่มเป็น [7, 4, 5]! ลำดับปลอดภัย: ⟨ P1, P3, P4 ⟩'
        },
        {
          stepNum: 5,
          title: 'รอบที่ 5: วนกลับมาตรวจ P0 (Need: [7, 4, 3] vs Work: [7, 4, 5]) → ผ่านแล้ว!',
          statusBadge: 'ผ่านเกณฑ์! (Need ≤ Work)',
          statusBadgeClass: 'badge-finished',
          boxClass: 'eval-pass',
          work: [7, 5, 5],
          workSub: 'Work ใหม่ = [7, 4, 5] + Allocation(P0) [0, 1, 0] = [7, 5, 5]',
          finish: [true, true, false, true, true],
          safeSeq: ['P1', 'P3', 'P4', 'P0'],
          evalIdx: 0,
          rowStatus: ['passed', 'passed', 'skipped', 'passed', 'passed'],
          rowResults: ['✔ Need ≤ Work (ผ่านแล้ว!)', '✔ Need ≤ Work (ผ่าน!)', '-', '✔ Need ≤ Work (ผ่าน!)', '✔ Need ≤ Work (ผ่าน!)'],
          proc: 'P0',
          need: [7, 4, 3],
          workBefore: [7, 4, 5],
          alloc: [0, 1, 0],
          workAfter: [7, 5, 5],
          comp: [
            { res: 'A', need: 7, work: 7, pass: true },
            { res: 'B', need: 4, work: 4, pass: true },
            { res: 'C', need: 3, work: 5, pass: true }
          ],
          thought: 'P0 ที่เคยไม่ผ่าน คราวนี้เซฟมี [7, 4, 5] เพียงพอพอดีเป๊ะ! คืนของ [0, 1, 0] เซฟเป็น [7, 5, 5]! ลำดับปลอดภัย: ⟨ P1, P3, P4, P0 ⟩'
        },
        {
          stepNum: 6,
          title: 'รอบที่ 6: ตรวจ P2 (Need: [6, 0, 0] vs Work: [7, 5, 5]) → จบสมบูรณ์!',
          statusBadge: 'ผ่านเกณฑ์! ครบทุกโปรเซส',
          statusBadgeClass: 'badge-finished',
          boxClass: 'eval-pass',
          work: [10, 5, 7],
          workSub: 'Work ใหม่ = [7, 5, 5] + Allocation(P2) [3, 0, 2] = Total [10, 5, 7]',
          finish: [true, true, true, true, true],
          safeSeq: ['P1', 'P3', 'P4', 'P0', 'P2'],
          evalIdx: 2,
          rowStatus: ['passed', 'passed', 'passed', 'passed', 'passed'],
          rowResults: ['✔ Finish = True', '✔ Finish = True', '✔ Need ≤ Work (ผ่าน!)', '✔ Finish = True', '✔ Finish = True'],
          proc: 'P2',
          need: [6, 0, 0],
          workBefore: [7, 5, 5],
          alloc: [3, 0, 2],
          workAfter: [10, 5, 7],
          comp: [
            { res: 'A', need: 6, work: 7, pass: true },
            { res: 'B', need: 0, work: 5, pass: true },
            { res: 'C', need: 0, work: 5, pass: true }
          ],
          thought: 'P2 ต้องการ [6, 0, 0] เซฟมี [7, 5, 5] ผ่านฉลุย! คืน [3, 0, 2] ทรัพยากรกลับคืนคลังครบ [10, 5, 7] เท่ากับ Total 100%!'
        },
        {
          stepNum: 7,
          title: '🎉 สำเร็จ! ปลอดภัย Safe Sequence = ⟨ P1, P3, P4, P0, P2 ⟩',
          statusBadge: 'Safe State ยืนยันแล้ว',
          statusBadgeClass: 'badge-finished',
          boxClass: 'eval-complete',
          work: [10, 5, 7],
          workSub: 'คืนทรัพยากรครบทุกตัว 100%',
          finish: [true, true, true, true, true],
          safeSeq: ['P1', 'P3', 'P4', 'P0', 'P2'],
          evalIdx: -1,
          rowStatus: ['passed', 'passed', 'passed', 'passed', 'passed'],
          rowResults: ['✔ Finish = True', '✔ Finish = True', '✔ Finish = True', '✔ Finish = True', '✔ Finish = True'],
          mathGrid: [
            { label: 'ผลรวมโปรเซส', val: 'Finish = True ครบ 5/5' },
            { label: 'Safe Sequence จากตำรา', val: '⟨ P1, P3, P4, P0, P2 ⟩' },
            { label: 'สถานะความปลอดภัย', val: 'Safe State 100%' }
          ],
          thought: 'ระบบยืนยันสภาวะปลอดภัย ค้นพบ Safe Sequence ตรงตามเฉลยของ Silberschatz ทุกประการ!'
        }
      ]
    },

    req_p2_safe: {
      name: 'ทดสอบคำขอ: P2 ขอเพิ่ม [1, 0, 1] — อนุมัติได้ (Safe State)',
      total: [10, 6, 8],
      processes: ['P0', 'P1', 'P2', 'P3', 'P4'],
      alloc: [[0, 1, 1], [2, 0, 2], [4, 1, 4], [2, 1, 1], [1, 1, 0]],
      max: [[7, 4, 3], [3, 2, 2], [9, 1, 4], [4, 2, 2], [5, 3, 3]],
      need: [[7, 3, 2], [1, 2, 0], [5, 0, 0], [2, 1, 1], [4, 2, 3]],
      steps: [
        {
          stepNum: 0,
          title: 'ขั้นที่ 1-2 ตรวจสอบคำขอ: P2 ขอ [1, 0, 1] (ผ่านกฎทั้ง 2 ข้อ!)',
          statusBadge: 'สมมุติจัดสรรชั่วคราว',
          statusBadgeClass: 'badge-eval',
          boxClass: 'eval-init',
          work: [1, 2, 0],
          workSub: 'Available เหลือ [2, 2, 1] - [1, 0, 1] = [1, 2, 0]',
          finish: [false, false, false, false, false],
          safeSeq: [],
          evalIdx: -1,
          rowStatus: ['waiting', 'waiting', 'waiting', 'waiting', 'waiting'],
          rowResults: ['-', '-', '-', '-', '-'],
          mathGrid: [
            { label: 'เช็คสิทธิ์ (Request ≤ Need)', val: '[1, 0, 1] ≤ [6, 0, 1] ✔ ผ่าน' },
            { label: 'เช็คคลัง (Request ≤ Available)', val: '[1, 0, 1] ≤ [2, 2, 1] ✔ มีของพอ' },
            { label: 'คลังหลังสมมุติแจก (Available - Request)', val: '[2, 2, 1] - [1, 0, 1] = [1, 2, 0]' }
          ],
          thought: '1. Request[P2] = [1, 0, 1] ≤ Need[P2] [6, 0, 1] (ไม่เกินสิทธิ์)<br>2. Request[P2] ≤ Available [2, 2, 1] (คลังมีของพอ)<br>3. <strong>สมมุติจัดสรรชั่วคราว:</strong> Available เหลือ [1, 2, 0], Allocation[P2] เพิ่มเป็น [4, 1, 4], Need[P2] ลดเหลือ [5, 0, 0] แล้วเริ่มรัน Safety Algorithm ทดสอบความปลอดภัย!'
        },
        {
          stepNum: 1,
          title: 'รอบที่ 1: ตรวจ P0 (Need: [7, 3, 2] vs Work: [1, 2, 0]) → ข้ามก่อน',
          statusBadge: 'ของไม่พอ (ข้ามก่อน)',
          statusBadgeClass: 'badge-skipped',
          boxClass: 'eval-fail',
          work: [1, 2, 0],
          workSub: 'เซฟเหลือ [1, 2, 0]',
          finish: [false, false, false, false, false],
          safeSeq: [],
          evalIdx: 0,
          rowStatus: ['skipped', 'waiting', 'waiting', 'waiting', 'waiting'],
          rowResults: ['❌ Need > Work (ไม่พอ)', '-', '-', '-', '-'],
          proc: 'P0',
          need: [7, 3, 2],
          workBefore: [1, 2, 0],
          comp: [
            { res: 'A', need: 7, work: 1, pass: false },
            { res: 'B', need: 3, work: 2, pass: false },
            { res: 'C', need: 2, work: 0, pass: false }
          ],
          thought: 'P0 ของไม่พอ พักไว้ก่อน'
        },
        {
          stepNum: 2,
          title: 'รอบที่ 2: ตรวจ P1 (Need: [1, 2, 0] vs Work: [1, 2, 0]) → พอดีเป๊ะ ผ่านฉลุย!',
          statusBadge: 'ผ่านเกณฑ์! (Need ≤ Work)',
          statusBadgeClass: 'badge-finished',
          boxClass: 'eval-pass',
          work: [3, 2, 2],
          workSub: 'Work ใหม่ = [1, 2, 0] + Allocation(P1) [2, 0, 2] = [3, 2, 2]',
          finish: [false, true, false, false, false],
          safeSeq: ['P1'],
          evalIdx: 1,
          rowStatus: ['skipped', 'passed', 'waiting', 'waiting', 'waiting'],
          rowResults: ['❌ Need > Work (ไม่พอ)', '✔ Need ≤ Work (1≤1, 2≤2, 0≤0)', '-', '-', '-'],
          proc: 'P1',
          need: [1, 2, 0],
          workBefore: [1, 2, 0],
          alloc: [2, 0, 2],
          workAfter: [3, 2, 2],
          comp: [
            { res: 'A', need: 1, work: 1, pass: true },
            { res: 'B', need: 2, work: 2, pass: true },
            { res: 'C', need: 0, work: 0, pass: true }
          ],
          thought: 'แม้เซฟจะเหลือแค่ [1, 2, 0] แต่ P1 ต้องการเพียง [1, 2, 0] พอดีเป๊ะทุกแกน! P1 คืน Allocation [2, 0, 2] เซฟเพิ่มเป็น [3, 2, 2]! บันทึก ⟨ P1 ⟩'
        },
        {
          stepNum: 3,
          title: 'รอบที่ 3: ตรวจ P3 (Need: [2, 1, 1] vs Work: [3, 2, 2]) → ผ่านสบาย!',
          statusBadge: 'ผ่านเกณฑ์! (Need ≤ Work)',
          statusBadgeClass: 'badge-finished',
          boxClass: 'eval-pass',
          work: [5, 3, 3],
          workSub: 'Work ใหม่ = [3, 2, 2] + Allocation(P3) [2, 1, 1] = [5, 3, 3]',
          finish: [false, true, false, true, false],
          safeSeq: ['P1', 'P3'],
          evalIdx: 3,
          rowStatus: ['skipped', 'passed', 'skipped', 'passed', 'waiting'],
          rowResults: ['❌ Need > Work (ไม่พอ)', '✔ Need ≤ Work (ผ่าน!)', '-', '✔ Need ≤ Work (ผ่าน!)', '-'],
          proc: 'P3',
          need: [2, 1, 1],
          workBefore: [3, 2, 2],
          alloc: [2, 1, 1],
          workAfter: [5, 3, 3],
          comp: [
            { res: 'A', need: 2, work: 3, pass: true },
            { res: 'B', need: 1, work: 2, pass: true },
            { res: 'C', need: 1, work: 2, pass: true }
          ],
          thought: 'P3 ต้องการ [2, 1, 1] ในเซฟมี [3, 2, 2] ผ่านฉลุย! คืน Allocation [2, 1, 1] เซฟพุ่งเป็น [5, 3, 3]! ลำดับปลอดภัย: ⟨ P1, P3 ⟩'
        },
        {
          stepNum: 4,
          title: 'รอบที่ 4: ตรวจ P2 (Need ใหม่: [5, 0, 0] vs Work: [5, 3, 3]) → ผ่านแล้ว!',
          statusBadge: 'ผ่านเกณฑ์! (Need ≤ Work)',
          statusBadgeClass: 'badge-finished',
          boxClass: 'eval-pass',
          work: [9, 4, 7],
          workSub: 'Work ใหม่ = [5, 3, 3] + Allocation(P2) [4, 1, 4] = [9, 4, 7]',
          finish: [false, true, true, true, false],
          safeSeq: ['P1', 'P3', 'P2'],
          evalIdx: 2,
          rowStatus: ['skipped', 'passed', 'passed', 'passed', 'waiting'],
          rowResults: ['❌ Need > Work (ไม่พอ)', '✔ Need ≤ Work (ผ่าน!)', '✔ Need ≤ Work (5≤5 ผ่าน!)', '✔ Need ≤ Work (ผ่าน!)', '-'],
          proc: 'P2',
          need: [5, 0, 0],
          workBefore: [5, 3, 3],
          alloc: [4, 1, 4],
          workAfter: [9, 4, 7],
          comp: [
            { res: 'A', need: 5, work: 5, pass: true },
            { res: 'B', need: 0, work: 3, pass: true },
            { res: 'C', need: 0, work: 3, pass: true }
          ],
          thought: 'P2 ผู้ขอเงิน Need ใหม่ลดเหลือเพียง [5, 0, 0] เมื่อเทียบกับเซฟ [5, 3, 3] ปรากฏว่าผ่านพอดี! P2 คืนของทั้งหมด [4, 1, 4] เซฟพุ่งทะลุเป็น [9, 4, 7]! ลำดับปลอดภัย: ⟨ P1, P3, P2 ⟩'
        },
        {
          stepNum: 5,
          title: 'รอบที่ 5: ตรวจ P0 (Need: [7, 3, 2] vs Work: [9, 4, 7]) → ผ่านสบาย!',
          statusBadge: 'ผ่านเกณฑ์! (Need ≤ Work)',
          statusBadgeClass: 'badge-finished',
          boxClass: 'eval-pass',
          work: [9, 5, 8],
          workSub: 'Work ใหม่ = [9, 4, 7] + Allocation(P0) [0, 1, 1] = [9, 5, 8]',
          finish: [true, true, true, true, false],
          safeSeq: ['P1', 'P3', 'P2', 'P0'],
          evalIdx: 0,
          rowStatus: ['passed', 'passed', 'passed', 'passed', 'waiting'],
          rowResults: ['✔ Need ≤ Work (ผ่านแล้ว!)', '✔ Need ≤ Work (ผ่าน!)', '✔ Need ≤ Work (ผ่าน!)', '✔ Need ≤ Work (ผ่าน!)', '-'],
          proc: 'P0',
          need: [7, 3, 2],
          workBefore: [9, 4, 7],
          alloc: [0, 1, 1],
          workAfter: [9, 5, 8],
          comp: [
            { res: 'A', need: 7, work: 9, pass: true },
            { res: 'B', need: 3, work: 4, pass: true },
            { res: 'C', need: 2, work: 7, pass: true }
          ],
          thought: 'P0 ผ่านฉลุย คืนของ [0, 1, 1] เซฟเพิ่มเป็น [9, 5, 8]! ลำดับปลอดภัย: ⟨ P1, P3, P2, P0 ⟩'
        },
        {
          stepNum: 6,
          title: 'รอบที่ 6: ตรวจ P4 (Need: [4, 2, 3] vs Work: [9, 5, 8]) → จบครบ 100%!',
          statusBadge: 'ผ่านเกณฑ์! ครบทุกโปรเซส',
          statusBadgeClass: 'badge-finished',
          boxClass: 'eval-pass',
          work: [10, 6, 8],
          workSub: 'Work ใหม่ = [9, 5, 8] + Allocation(P4) [1, 1, 0] = Total [10, 6, 8]',
          finish: [true, true, true, true, true],
          safeSeq: ['P1', 'P3', 'P2', 'P0', 'P4'],
          evalIdx: 4,
          rowStatus: ['passed', 'passed', 'passed', 'passed', 'passed'],
          rowResults: ['✔ Finish = True', '✔ Finish = True', '✔ Finish = True', '✔ Finish = True', '✔ Need ≤ Work (ผ่าน!)'],
          proc: 'P4',
          need: [4, 2, 3],
          workBefore: [9, 5, 8],
          alloc: [1, 1, 0],
          workAfter: [10, 6, 8],
          comp: [
            { res: 'A', need: 4, work: 9, pass: true },
            { res: 'B', need: 2, work: 5, pass: true },
            { res: 'C', need: 3, work: 8, pass: true }
          ],
          thought: 'P4 คืนของครบ ทรัพยากรกลับคืนคลังเต็ม [10, 6, 8] ครบ 5/5 โปรเซส!'
        },
        {
          stepNum: 7,
          title: '🎉 การตัดสินใจของ OS: "อนุมัติคำขอให้ P2 ทันที (APPROVED)"',
          statusBadge: 'คำขอปลอดภัย อนุมัติทันที!',
          statusBadgeClass: 'badge-finished',
          boxClass: 'eval-complete',
          work: [10, 6, 8],
          workSub: 'พบ Safe Sequence ⟨ P1, P3, P2, P0, P4 ⟩ ยืนยันความปลอดภัย',
          finish: [true, true, true, true, true],
          safeSeq: ['P1', 'P3', 'P2', 'P0', 'P4'],
          evalIdx: -1,
          rowStatus: ['passed', 'passed', 'passed', 'passed', 'passed'],
          rowResults: ['✔ Finish = True', '✔ Finish = True', '✔ Finish = True', '✔ Finish = True', '✔ Finish = True'],
          mathGrid: [
            { label: 'คำร้องขอ P2', val: 'Request = [1, 0, 1]' },
            { label: 'Safe Sequence ที่พบ', val: '⟨ P1, P3, P2, P0, P4 ⟩' },
            { label: 'คำสั่งระบบปฏิบัติการ', val: 'อนุมัติจัดสรรทรัพยากรให้จริง (GRANT)' }
          ],
          thought: 'เนื่องจากเมื่อจำลองจัดสรรทรัพยากรให้ P2 แล้ว ระบบยังคงค้นพบ Safe Sequence ครบทุกโปรเซส <strong>ระบบไม่เสี่ยงต่อ Deadlock</strong> ดังนั้นระบบปฏิบัติการจึง <strong>"อนุมัติ (Grant)"</strong> ให้ P2 ได้รับทรัพยากรไปใช้งานจริงทันที!'
        }
      ]
    },

    req_p0_unsafe: {
      name: 'ทดสอบคำขอ: P0 ขอเพิ่ม [0, 2, 0] — ปฏิเสธ (Unsafe / Deadlock!)',
      total: [10, 6, 8],
      processes: ['P0', 'P1', 'P2', 'P3', 'P4'],
      alloc: [[0, 3, 1], [2, 0, 2], [3, 1, 3], [2, 1, 1], [1, 1, 0]],
      max: [[7, 4, 3], [3, 2, 2], [9, 1, 4], [4, 2, 2], [5, 3, 3]],
      need: [[7, 1, 2], [1, 2, 0], [6, 0, 1], [2, 1, 1], [4, 2, 3]],
      steps: [
        {
          stepNum: 0,
          title: 'ขั้นที่ 1-2 ตรวจสอบคำขอ: P0 ขอ [0, 2, 0] (ผ่านกฎเบื้องต้น แต่ส่งผลให้ B หมดเกลี้ยง!)',
          statusBadge: 'สมมุติจัดสรรชั่วคราว',
          statusBadgeClass: 'badge-eval',
          boxClass: 'eval-init',
          work: [2, 0, 1],
          workSub: 'Available เหลือ [2, 2, 1] - [0, 2, 0] = [2, 0, 1] (B เหลือ 0!)',
          finish: [false, false, false, false, false],
          safeSeq: [],
          evalIdx: -1,
          rowStatus: ['waiting', 'waiting', 'waiting', 'waiting', 'waiting'],
          rowResults: ['-', '-', '-', '-', '-'],
          mathGrid: [
            { label: 'เช็คสิทธิ์ (Request ≤ Need)', val: '[0, 2, 0] ≤ [7, 3, 2] ✔ ผ่าน' },
            { label: 'เช็คคลัง (Request ≤ Available)', val: '[0, 2, 0] ≤ [2, 2, 1] ✔ มีของพอ' },
            { label: 'คลังหลังสมมุติแจก (B เหลือ 0!)', val: '[2, 2, 1] - [0, 2, 0] = [2, 0, 1]' }
          ],
          thought: '1. Request[P0] = [0, 2, 0] ≤ Need[P0] [7, 3, 2] ✔ ไม่เกินสิทธิ์<br>2. Request[P0] ≤ Available [2, 2, 1] ✔ มีของพอแจก<br>3. <strong>สมมุติจัดสรรชั่วคราว:</strong> Available เหลือ <code>[2, 0, 1]</code> (สังเกตว่า <strong>ทรัพยากร B เหลือ 0 ตัว!</strong>) ต่อไประบบจะรัน Safety Algorithm เพื่อดูว่าจะรอดไหม...'
        },
        {
          stepNum: 1,
          title: 'รอบที่ 1: ตรวจ P0 (Need: [7, 1, 2] vs Work: [2, 0, 1]) → ไม่พอ! (B เหลือ 0)',
          statusBadge: 'ของไม่พอ (ข้ามก่อน)',
          statusBadgeClass: 'badge-skipped',
          boxClass: 'eval-fail',
          work: [2, 0, 1],
          workSub: 'เซฟยังคงเดิม [2, 0, 1] (B = 0)',
          finish: [false, false, false, false, false],
          safeSeq: [],
          evalIdx: 0,
          rowStatus: ['skipped', 'waiting', 'waiting', 'waiting', 'waiting'],
          rowResults: ['❌ Need > Work (B ขาด: 1 > 0)', '-', '-', '-', '-'],
          proc: 'P0',
          need: [7, 1, 2],
          workBefore: [2, 0, 1],
          comp: [
            { res: 'A', need: 7, work: 2, pass: false },
            { res: 'B', need: 1, work: 0, pass: false },
            { res: 'C', need: 2, work: 1, pass: false }
          ],
          thought: 'P0 ต้องการ B อีก 1 แต่เซฟมี B เป็น 0! พัก P0 ไว้ก่อน'
        },
        {
          stepNum: 2,
          title: 'รอบที่ 2: ตรวจ P1 (Need: [1, 2, 0] vs Work: [2, 0, 1]) → ไม่พอ! (B ต้องการ 2 แต่เซฟมี 0)',
          statusBadge: 'ของไม่พอ (ข้ามก่อน)',
          statusBadgeClass: 'badge-skipped',
          boxClass: 'eval-fail',
          work: [2, 0, 1],
          workSub: 'เซฟยังคงเดิม [2, 0, 1] (B = 0)',
          finish: [false, false, false, false, false],
          safeSeq: [],
          evalIdx: 1,
          rowStatus: ['skipped', 'skipped', 'waiting', 'waiting', 'waiting'],
          rowResults: ['❌ Need > Work (B ขาด)', '❌ Need > Work (B ขาด: 2 > 0)', '-', '-', '-'],
          proc: 'P1',
          need: [1, 2, 0],
          workBefore: [2, 0, 1],
          comp: [
            { res: 'A', need: 1, work: 2, pass: true },
            { res: 'B', need: 2, work: 0, pass: false },
            { res: 'C', need: 0, work: 1, pass: true }
          ],
          thought: 'พระเอกเดิมของเรา P1 คราวนี้ไม่ผ่าน! เพราะ P1 ต้องการ B จำนวน 2 ตัว แต่ในตู้เซฟ B หมดเกลี้ยง (Work_B = 0) ทำให้ P1 ติดขัด รันไม่ได้!'
        },
        {
          stepNum: 3,
          title: 'รอบที่ 3: ตรวจ P2 (Need: [6, 0, 1] vs Work: [2, 0, 1]) → ไม่พอ! (A ต้องการ 6 แต่เซฟมี 2)',
          statusBadge: 'ของไม่พอ (ข้ามก่อน)',
          statusBadgeClass: 'badge-skipped',
          boxClass: 'eval-fail',
          work: [2, 0, 1],
          workSub: 'เซฟยังคงเดิม [2, 0, 1] (A = 2, B = 0)',
          finish: [false, false, false, false, false],
          safeSeq: [],
          evalIdx: 2,
          rowStatus: ['skipped', 'skipped', 'skipped', 'waiting', 'waiting'],
          rowResults: ['❌ Need > Work', '❌ Need > Work', '❌ Need > Work (A ขาด: 6 > 2)', '-', '-'],
          proc: 'P2',
          need: [6, 0, 1],
          workBefore: [2, 0, 1],
          comp: [
            { res: 'A', need: 6, work: 2, pass: false },
            { res: 'B', need: 0, work: 0, pass: true },
            { res: 'C', need: 1, work: 1, pass: true }
          ],
          thought: 'P2 ไม่ต้องการ B แต่ต้องการ A ถึง 6 ตัว ซึ่งเซฟมี A แค่ 2 ตัว → P2 รันไม่ได้!'
        },
        {
          stepNum: 4,
          title: 'รอบที่ 4: ตรวจ P3 (Need: [2, 1, 1] vs Work: [2, 0, 1]) → ไม่พอ! (B ต้องการ 1 แต่เซฟมี 0)',
          statusBadge: 'ของไม่พอ (ข้ามก่อน)',
          statusBadgeClass: 'badge-skipped',
          boxClass: 'eval-fail',
          work: [2, 0, 1],
          workSub: 'เซฟยังคงเดิม [2, 0, 1]',
          finish: [false, false, false, false, false],
          safeSeq: [],
          evalIdx: 3,
          rowStatus: ['skipped', 'skipped', 'skipped', 'skipped', 'waiting'],
          rowResults: ['❌ Need > Work', '❌ Need > Work', '❌ Need > Work', '❌ Need > Work (B ขาด: 1 > 0)', '-'],
          proc: 'P3',
          need: [2, 1, 1],
          workBefore: [2, 0, 1],
          comp: [
            { res: 'A', need: 2, work: 2, pass: true },
            { res: 'B', need: 1, work: 0, pass: false },
            { res: 'C', need: 1, work: 1, pass: true }
          ],
          thought: 'P3 ต้องการ B จำนวน 1 ตัว แต่ตู้เซฟไม่มี B เหลือเลย → P3 ติดขัด รันไม่ได้!'
        },
        {
          stepNum: 5,
          title: 'รอบที่ 5: ตรวจ P4 (Need: [4, 2, 3] vs Work: [2, 0, 1]) → ไม่พอทุกตัว!',
          statusBadge: 'ของไม่พอ (ข้ามก่อน)',
          statusBadgeClass: 'badge-skipped',
          boxClass: 'eval-fail',
          work: [2, 0, 1],
          workSub: 'เซฟยังคงเดิม [2, 0, 1]',
          finish: [false, false, false, false, false],
          safeSeq: [],
          evalIdx: 4,
          rowStatus: ['skipped', 'skipped', 'skipped', 'skipped', 'skipped'],
          rowResults: ['❌ Need > Work', '❌ Need > Work', '❌ Need > Work', '❌ Need > Work', '❌ Need > Work (ไม่พอสักตัว)'],
          proc: 'P4',
          need: [4, 2, 3],
          workBefore: [2, 0, 1],
          comp: [
            { res: 'A', need: 4, work: 2, pass: false },
            { res: 'B', need: 2, work: 0, pass: false },
            { res: 'C', need: 3, work: 1, pass: false }
          ],
          thought: 'P4 ต้องการ [4, 2, 3] แต่เซฟมีแค่ [2, 0, 1] ขาดทุกแกน → P4 รันไม่ได้!'
        },
        {
          stepNum: 6,
          title: '🚨 ตรวจพบอันตราย! เกิดภาวะติดตาย (DEADLOCK / UNSAFE STATE)',
          statusBadge: 'Unsafe State (อันตราย!)',
          statusBadgeClass: 'badge-skipped',
          boxClass: 'eval-fail',
          work: [2, 0, 1],
          workSub: 'ไม่มีโปรเซสใดสามารถรันต่อได้เลยแม้แต่ตัวเดียว!',
          finish: [false, false, false, false, false],
          safeSeq: [],
          evalIdx: -1,
          rowStatus: ['skipped', 'skipped', 'skipped', 'skipped', 'skipped'],
          rowResults: ['❌ ติด Deadlock', '❌ ติด Deadlock', '❌ ติด Deadlock', '❌ ติด Deadlock', '❌ ติด Deadlock'],
          mathGrid: [
            { label: 'ผลการตรวจสอบทุกโปรเซส', val: 'ไม่มีโปรเซสใดที่ Need ≤ Work ได้เลย' },
            { label: 'Safe Sequence', val: 'หาไม่ได้ (Safe Sequence = ∅)' },
            { label: 'คำสั่งชี้ขาดของ OS', val: 'ปฏิเสธคำขอ (REJECT / WAIT) ห้ามแจกเด็ดขาด!' }
          ],
          thought: '<strong>💥 บทเรียนสำคัญที่สุดของ Banker\'s Algorithm:</strong> แม้ว่าในตอนแรกคลังจะมี Available [2, 2, 1] ซึ่งเพียงพอจะแจก [0, 2, 0] ให้ P0 ได้ แต่เมื่อแจกไปแล้วจะทำให้ทรัพยากร B เหลือ 0 และส่งผลให้ <strong>"ทุกโปรเซสในระบบติดขัดพร้อมกัน (Circular Wait / Deadlock)"</strong><br><br><strong>การตัดสินใจของ OS:</strong> คืนค่าเดิมทั้งหมด ปฏิเสธคำขอของ P0 และสั่งให้ P0 <strong>"เข้าสู่สถานะรอ (Wait)"</strong> ห้ามอนุมัติเด็ดขาด!'
        }
      ]
    }
  };

  // Render Step Function
  function renderStep(idx) {
    const preset = presets[currentPresetKey];
    if (!preset || !preset.steps || idx < 0 || idx >= preset.steps.length) return;

    currentStepIndex = idx;
    const step = preset.steps[idx];

    // 1. Update Work Card
    workVal.textContent = `[ A: ${step.work[0]}, B: ${step.work[1]}, C: ${step.work[2]} ]`;
    workSub.textContent = step.workSub;

    // 2. Update Safe Sequence Card
    if (step.safeSeq && step.safeSeq.length > 0) {
      seqVal.innerHTML = step.safeSeq
        .map((p, i) => `${i > 0 ? '<span class="seq-arrow"><i class="fa-solid fa-arrow-right"></i></span>' : ''}<span class="seq-item-badge">${p}</span>`)
        .join('');
    } else {
      seqVal.innerHTML = '<span style="font-size: 0.95rem; color: var(--text-dim); font-weight: normal;">(ยังไม่มีโปรเซสผ่านเกณฑ์)</span>';
    }

    const finishedCount = step.finish.filter(Boolean).length;
    progressSub.textContent = `สเต็ปที่ ${idx} / ${preset.steps.length - 1} • Finish: ${finishedCount}/5 โปรเซส`;

    // 3. Update Table Rows
    let tableHtml = '';
    preset.processes.forEach((procName, i) => {
      const isEvaluating = (step.evalIdx === i);
      const isPassed = step.finish[i];
      const isSkipped = (step.rowStatus[i] === 'skipped');

      let rowClass = '';
      if (isEvaluating) {
        rowClass = 'row-evaluating';
      } else if (isPassed) {
        rowClass = 'row-passed';
      } else if (isSkipped) {
        rowClass = 'row-failed';
      }

      let finishBadge = '';
      if (isPassed) {
        finishBadge = '<span class="banker-badge badge-finished"><i class="fa-solid fa-check"></i> True</span>';
      } else if (isEvaluating) {
        finishBadge = '<span class="banker-badge badge-eval"><i class="fa-solid fa-spinner fa-spin"></i> ตรวจสอบ</span>';
      } else if (isSkipped) {
        finishBadge = '<span class="banker-badge badge-skipped"><i class="fa-solid fa-clock"></i> False (ข้าม)</span>';
      } else {
        finishBadge = '<span class="banker-badge badge-waiting"><i class="fa-regular fa-circle"></i> False</span>';
      }

      let resBadge = '';
      const rawRes = step.rowResults[i] || '-';
      if (rawRes.includes('✔') || rawRes.includes('ผ่าน')) {
        resBadge = `<span class="comp-res-pass">${rawRes}</span>`;
      } else if (rawRes.includes('❌') || rawRes.includes('ไม่พอ') || rawRes.includes('Deadlock')) {
        resBadge = `<span class="comp-res-fail">${rawRes}</span>`;
      } else {
        resBadge = `<span style="color: var(--text-dim);">${rawRes}</span>`;
      }

      tableHtml += `
        <tr class="${rowClass}">
          <td><strong>${procName}</strong></td>
          <td><span class="vector-pill" style="color: #cbd5e1;">[ ${preset.alloc[i].join(', ')} ]</span></td>
          <td><span class="vector-pill" style="color: #94a3b8;">[ ${preset.max[i].join(', ')} ]</span></td>
          <td><span class="vector-pill" style="color: var(--accent-cyan); font-weight: 700;">[ ${preset.need[i].join(', ')} ]</span></td>
          <td>${finishBadge}</td>
          <td>${resBadge}</td>
        </tr>
      `;
    });
    tableBody.innerHTML = tableHtml;

    // 4. Update Step Detail Box
    stepBadge.textContent = step.stepNum;
    stepTitle.textContent = step.title;
    stepStatus.textContent = step.statusBadge;
    stepStatus.className = `banker-badge ${step.statusBadgeClass}`;
    stepBox.className = `banker-step-box ${step.boxClass}`;

    // Construct Detailed Math HTML
    let mathHtml = '';
    if (step.comp && step.comp.length > 0) {
      const compPills = step.comp.map(c => {
        const icon = c.pass ? '<span style="color: var(--accent-emerald);">✔</span>' : '<span style="color: var(--accent-rose);">❌</span>';
        const color = c.pass ? 'var(--accent-emerald)' : 'var(--accent-rose)';
        return `<span style="display: inline-block; margin-right: 0.75rem; color: ${color}; font-weight: 700;">${c.res}: ${c.need} ${c.need <= c.work ? '≤' : '>'} ${c.work} ${icon}</span>`;
      }).join('');

      let allocReturnHtml = '';
      if (step.alloc && step.workAfter) {
        allocReturnHtml = `
          <div class="math-item" style="border-left: 3px solid var(--accent-emerald); background: rgba(16, 185, 129, 0.08);">
            <div class="math-label" style="color: var(--accent-emerald);"><i class="fa-solid fa-hand-holding-dollar"></i> สูตรรับคืนทรัพยากร (Work ใหม่ = Work เดิม + Allocation)</div>
            <div style="font-size: 0.95rem;">
              [ ${step.workBefore.join(', ')} ] + [ ${step.alloc.join(', ')} ] = <strong style="color: var(--accent-emerald); font-size: 1.1rem;">[ ${step.workAfter.join(', ')} ]</strong>
            </div>
          </div>
        `;
      }

      mathHtml = `
        <div class="banker-math-grid">
          <div class="math-item">
            <div class="math-label"><i class="fa-solid fa-crosshairs"></i> สิ่งที่โปรเซส ${step.proc} ต้องการ (Need)</div>
            <div>[ A: ${step.need[0]}, B: ${step.need[1]}, C: ${step.need[2]} ]</div>
          </div>
          <div class="math-item">
            <div class="math-label"><i class="fa-solid fa-vault"></i> เงินสดในตู้เซฟปัจจุบัน (Work)</div>
            <div>[ A: ${step.workBefore[0]}, B: ${step.workBefore[1]}, C: ${step.workBefore[2]} ]</div>
          </div>
          <div class="math-item">
            <div class="math-label"><i class="fa-solid fa-scale-balanced"></i> ผลเปรียบเทียบทีละทรัพยากร (Need ≤ Work)</div>
            <div>${compPills}</div>
          </div>
        </div>
        ${allocReturnHtml}
      `;
    } else if (step.mathGrid && step.mathGrid.length > 0) {
      mathHtml = `
        <div class="banker-math-grid">
          ${step.mathGrid.map(m => `
            <div class="math-item">
              <div class="math-label">${m.label}</div>
              <div style="color: var(--accent-cyan); font-weight: 700;">${m.val}</div>
            </div>
          `).join('')}
        </div>
      `;
    }

    // Append Banker Thought Box
    const thoughtHtml = `
      <div style="margin-top: 1rem; padding: 1rem 1.25rem; background: rgba(255, 255, 255, 0.04); border: 1px solid var(--border-color); border-radius: 8px; border-left: 3px solid var(--accent-cyan);">
        <div style="font-weight: 700; color: var(--accent-cyan); display: flex; align-items: center; gap: 0.45rem; margin-bottom: 0.45rem; font-size: 0.95rem;">
          <i class="fa-solid fa-lightbulb"></i> วิธีคิดของระบบและตรรกะแบบนายธนาคาร (Banker's Logic):
        </div>
        <div style="font-size: 0.92rem; line-height: 1.7; color: var(--text-main);">
          ${step.thought}
        </div>
      </div>
    `;

    stepContent.innerHTML = mathHtml + thoughtHtml;

    // 5. Update Navigation Buttons
    prevBtn.disabled = (idx === 0);
    nextBtn.disabled = (idx === preset.steps.length - 1);

    if (idx === preset.steps.length - 1 && autoPlayTimer) {
      stopAutoPlay();
    }
  }

  function stopAutoPlay() {
    if (autoPlayTimer) {
      clearInterval(autoPlayTimer);
      autoPlayTimer = null;
    }
    if (autoBtn) {
      autoBtn.innerHTML = '<i class="fa-solid fa-play"></i> เล่นอัตโนมัติ';
      autoBtn.style.background = 'rgba(255,255,255,0.08)';
    }
  }

  function startAutoPlay() {
    stopAutoPlay();
    const preset = presets[currentPresetKey];
    if (currentStepIndex >= preset.steps.length - 1) {
      currentStepIndex = 0;
      renderStep(0);
    }
    autoBtn.innerHTML = '<i class="fa-solid fa-pause"></i> หยุดเล่น';
    autoBtn.style.background = 'rgba(56, 189, 248, 0.25)';

    autoPlayTimer = setInterval(() => {
      const p = presets[currentPresetKey];
      if (currentStepIndex < p.steps.length - 1) {
        renderStep(currentStepIndex + 1);
      } else {
        stopAutoPlay();
      }
    }, 1800);
  }

  // Event Listeners
  if (presetSelect) {
    presetSelect.addEventListener('change', () => {
      stopAutoPlay();
      currentPresetKey = presetSelect.value;
      renderStep(0);
    });
  }

  if (prevBtn) {
    prevBtn.addEventListener('click', () => {
      stopAutoPlay();
      if (currentStepIndex > 0) renderStep(currentStepIndex - 1);
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      stopAutoPlay();
      const preset = presets[currentPresetKey];
      if (currentStepIndex < preset.steps.length - 1) renderStep(currentStepIndex + 1);
    });
  }

  if (autoBtn) {
    autoBtn.addEventListener('click', () => {
      if (autoPlayTimer) {
        stopAutoPlay();
      } else {
        startAutoPlay();
      }
    });
  }

  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
      stopAutoPlay();
      renderStep(0);
    });
  }

  // Initial Load
  renderStep(0);
}

/* ==========================================================================
   6. INTERACTIVE PRACTICE QUIZ (20 REAL EXAM QUESTIONS)
   ========================================================================== */
function initQuiz() {
  const quizData = [
    {
      question: "1. ภาวะติดตาย (Deadlock) จะเกิดขึ้นได้ก็ต่อเมื่อมีเงื่อนไขจำเป็นตามข้อใดเกิดขึ้นพร้อมกันในเวลาเดียวกัน?",
      options: [
        "A. Mutual Exclusion, Hold and Wait, Preemption, Circular Wait",
        "B. Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait",
        "C. Shared Memory, No Preemption, Semaphore, Aging",
        "D. Paging, Virtual Memory, Thrashing, Belady's Anomaly"
      ],
      correct: 1,
      explanation: "เงื่อนไขจำเป็น 4 ประการ (Coffman Conditions) ได้แก่: 1. Mutual Exclusion (ไม่เกิดร่วมกัน), 2. Hold and Wait (ถือครองและรอคอย), 3. No Preemption (ไม่สามารถยึดทรัพยากรคืนได้), และ 4. Circular Wait (การรอแบบวงรอบ) ทั้ง 4 ข้อต้องเกิดขึ้นพร้อมกันเท่านั้นจึงจะเกิด Deadlock"
    },
    {
      question: "2. ในกราฟจัดสรรทรัพยากร (Resource Allocation Graph: RAG) หากทรัพยากรแต่ละชนิดมีเพียง 1 หน่วย (Single Instance) การเกิดวงรอบ (Cycle) ในกราฟหมายความว่าอย่างไร?",
      options: [
        "A. เกิด Deadlock ขึ้นแน่นอน 100%",
        "B. อาจจะเกิดหรือไม่เกิด Deadlock ก็ได้ ต้องดูว่ามี Free Frame หรือไม่",
        "C. ระบบอยู่ใน Safe State เสมอ",
        "D. เกิดปัญหา Thrashing ขึ้นในหน่วยความจำ"
      ],
      correct: 0,
      explanation: "ตามทฤษฎี RAG: หากทรัพยากรทุกชนิดมีเพียง 1 Instance การมี Cycle เป็น 'เงื่อนไขที่ทั้งจำเป็นและเพียงพอ' (Necessary and Sufficient Condition) นั่นคือเกิด Deadlock แน่นอน 100% ต่างจากกรณี Multiple Instances ที่อาจไม่เกิด Deadlock หากมีโปรเซสนอกวงรอบช่วยปล่อยทรัพยากรคืน"
    },
    {
      question: "3. ในการทำงานของ Banker's Algorithm เมทริกซ์ Need คำนวณได้จากสูตรใด?",
      options: [
        "A. Need = Allocation - Available",
        "B. Need = Max + Allocation",
        "C. Need = Max - Allocation",
        "D. Need = Available - Request"
      ],
      correct: 2,
      explanation: "Need[i, j] = Max[i, j] - Allocation[i, j] ซึ่งหมายถึงจำนวนทรัพยากรประเภท j ที่โปรเซส i ยังคงต้องการเพิ่มเติมจากที่ถือครองอยู่ เพื่อให้งานสำเร็จสมบูรณ์"
    },
    {
      question: "4. ความหมายของสถานะปลอดภัย (Safe State) ในระบบป้องกัน Deadlock คือข้อใด?",
      options: [
        "A. มีลำดับโปรเซส (Safe Sequence) ที่สามารถจัดสรรทรัพยากรให้ทุกโปรเซสจนเสร็จสิ้นได้โดยไม่เกิด Deadlock",
        "B. ไม่มีการใช้หน่วยความจำเกิน 80%",
        "C. ไม่มีโปรเซสใดร้องขอ I/O เลยในขณะนั้น",
        "D. ระบบปิดการทำงานของ Round Robin ทั้งหมด"
      ],
      correct: 0,
      explanation: "Safe State หมายถึงสภาวะที่มีลำดับที่ปลอดภัย (Safe Sequence <P1, P2, ..., Pn>) ที่การร้องขอทรัพยากรสูงสุดของแต่ละโปรเซสสามารถตอบสนองได้ด้วย Available ปัจจุบันรวมกับทรัพยากรที่โปรเซสก่อนหน้าจะปล่อยคืนมา"
    },
    {
      question: "5. อัลกอริทึมการจัดลำดับซีพียู (CPU Scheduling) ข้อใดที่ได้รับการพิสูจน์ทางคณิตศาสตร์แล้วว่าให้ค่าเฉลี่ยเวลารอ (Average Waiting Time) ต่ำที่สุดเสมอ?",
      options: [
        "A. First-Come, First-Served (FCFS)",
        "B. Round Robin (RR)",
        "C. Shortest Job First (SJF) / Shortest Remaining Time First (SRTF)",
        "D. Multilevel Queue Scheduling"
      ],
      correct: 2,
      explanation: "SJF (หรือ SRTF ในกรณี Preemptive) ได้รับการพิสูจน์แล้วว่าเป็น Optimal Scheduling Algorithm ที่ให้ค่าเฉลี่ยเวลารอน้อยที่สุด เพราะนำโปรเซสสั้นมาทำก่อน ทำให้เวลารอสะสมของคิวสั้นลงมากที่สุด"
    },
    {
      question: "6. ปัญหาการอดตาย (Starvation หรือ Indefinite Blocking) ใน Priority Scheduling สามารถแก้ไขได้อย่างมีประสิทธิภาพด้วยเทคนิคใด?",
      options: [
        "A. Compaction",
        "B. Aging (การค่อยๆ เพิ่มค่าความสำคัญของโปรเซสที่รอนานขึ้นตามเวลา)",
        "C. Demand Paging",
        "D. Priority Inversion"
      ],
      correct: 1,
      explanation: "Aging เป็นเทคนิคที่ระบบจะค่อยๆ ปรับเพิ่มระดับ Priority ของโปรเซสที่ต้องรอคอยใน Ready Queue เป็นเวลานานขึ้นเรื่อยๆ จนในที่สุดจะมี Priority สูงพอที่จะได้รับการจัดสรรซีพียูแน่นอน"
    },
    {
      question: "7. ในอัลกอริทึม Round Robin (RR) หากผู้ดูแลระบบกำหนดค่า Time Quantum (q) สั้นเกินไปอย่างยิ่ง จะส่งผลเสียตามข้อใด?",
      options: [
        "A. เกิด Convoy Effect คล้ายกับ FCFS",
        "B. เกิด Context Switch บ่อยเกินไป ทำให้เสีย Overhead ของระบบมหาศาล",
        "C. เกิด Deadlock ระหว่าง Ready Queue",
        "D. ทำให้เกิด External Fragmentation ในหน่วยความจำ"
      ],
      correct: 1,
      explanation: "ถ้า Time Quantum เล็กเกินไป ซีพียูจะเสียเวลาส่วนใหญ่ไปกับการสลับงาน (Context Switching Overhead) และบันทึกสถานะโปรเซส ทำให้ประสิทธิภาพการทำงานจริงลดลงอย่างมาก"
    },
    {
      question: "8. ปัญหา Priority Inversion ซึ่งโปรเซสความสำคัญสูงต้องรอนานกว่าปกติเนื่องจากโปรเซสความสำคัญต่ำถือครองล็อกอยู่ แก้ไขได้ด้วยโปรโตคอลใด?",
      options: [
        "A. Banker's Algorithm",
        "B. Priority Inheritance Protocol (PIP)",
        "C. Working-Set Model",
        "D. Belady Protocol"
      ],
      correct: 1,
      explanation: "Priority Inheritance Protocol (PIP) จะทำการยกระดับความสำคัญของโปรเซสระดับต่ำที่ถือครองล็อก ให้มี Priority ชั่วคราวเท่ากับโปรเซสระดับสูงที่กำลังรออยู่ เพื่อป้องกันไม่ให้โปรเซสระดับกลางเข้ามาแทรกซีพียูได้"
    },
    {
      question: "9. ในการจัดสรรหน่วยความจำแบบต่อเนื่อง (Contiguous Allocation) วิธีการใดจะค้นหาช่องว่างทั้งหมดในรายการเพื่อเลือกช่องว่างที่มีขนาดเล็กที่สุดที่พอดีกับโปรเซส?",
      options: [
        "A. First-Fit",
        "B. Best-Fit",
        "C. Worst-Fit",
        "D. Next-Fit"
      ],
      correct: 1,
      explanation: "Best-Fit จะทำการค้นหาช่องว่างทั้งหมดเพื่อเลือกช่องที่เล็กที่สุดที่โปรเซสสามารถใส่ได้ ข้อเสียคือทำให้เกิดช่องว่างขนาดเล็กจิ๋วที่ไม่สามารถนำไปใช้งานต่อได้ทิ้งไว้"
    },
    {
      question: "10. ข้อแตกต่างสำคัญระหว่าง Internal Fragmentation และ External Fragmentation คือข้อใด?",
      options: [
        "A. Internal เกิดภายในบล็อก/เฟรมที่จัดสรร ส่วน External เกิดภายนอกระหว่างช่องว่างในหน่วยความจำ",
        "B. Internal แก้ได้ด้วย Compaction ส่วน External แก้ไม่ได้",
        "C. Internal เกิดขึ้นในฮาร์ดดิสก์เท่านั้น ส่วน External เกิดในแคช L1",
        "D. ทั้งสองอย่างเหมือนกันทุกประการ ไม่มีข้อแตกต่าง"
      ],
      correct: 0,
      explanation: "Internal เกิดขึ้นภายในบล็อกที่จัดสรรให้แต่โปรเซสใช้ไม่หมด (เช่น Page ขนาด 4KB แต่โปรเซสใช้ 1KB เหลือเศษ 3KB ภายใน) ส่วน External เกิดจากช่องว่างภายนอกกระจัดกระจายไม่ต่อเนื่องกัน"
    },
    {
      question: "11. ถ้า TLB มี Hit Ratio = 85%, เวลาค้นหา TLB = 15 ns และเวลาเข้าถึง RAM = 90 ns ค่าเวลาเข้าถึงเฉลี่ย (EMAT) จะมีค่าเท่าใด (ตรงตามการบ้านข้อ 1.5)?",
      options: [
        "A. 105.00 ns",
        "B. 118.50 ns",
        "C. 140.00 ns",
        "D. 195.00 ns"
      ],
      correct: 1,
      explanation: "EMAT = 0.85 × (15 + 90) + (1 - 0.85) × (15 + 90 + 90) = 0.85 × 105 + 0.15 × 195 = 89.25 + 29.25 = 118.50 ns"
    },
    {
      question: "12. ในระบบการแบ่งหน้า (Paging) แอดเดรสตรรกะ (Logical Address) ถูกแบ่งออกเป็น 2 ส่วนย่อยใด?",
      options: [
        "A. Base Register และ Limit Register",
        "B. Page Number (p) และ Page Offset (d)",
        "C. Segment Number (s) และ Track Number (t)",
        "D. Valid Bit และ Dirty Bit"
      ],
      correct: 1,
      explanation: "Logical Address ถูกแบ่งเป็น Page Number (p) สำหรับนำไปค้นหาใน Page Table เพื่อหา Frame Number และ Page Offset (d) ซึ่งระบุตำแหน่งย่อยภายในหน้า"
    },
    {
      question: "13. ในขั้นตอนการเกิด Page Fault มีขั้นตอนหลักตามลำดับกี่ขั้นตอน และขั้นตอนใดใช้เวลาประมวลผลนานที่สุด?",
      options: [
        "A. 3 ขั้นตอน และขั้นตอนเปลี่ยน Valid Bit ช้าที่สุด",
        "B. 5 ขั้นตอน และขั้นตอนส่ง Trap ช้าที่สุด",
        "C. 8 ขั้นตอน และขั้นตอนอ่านข้อมูลจากดิสก์ (Disk I/O) ช้าที่สุด",
        "D. 12 ขั้นตอน และขั้นตอน Restart คำสั่งช้าที่สุด"
      ],
      correct: 2,
      explanation: "การจัดการ Page Fault มี 8 ขั้นตอนมาตรฐาน และขั้นตอนที่ 5 (การอ่านดิสก์เข้าสู่แรม) ใช้เวลานานที่สุดในระบบ คิดเป็นสัดส่วนกว่า 99.9% ของเวลาทั้งหมด เนื่องจากดิสก์ทำงานในระดับมิลลิวินาที ขณะที่แรมทำงานในระดับนาโนวินาที"
    },
    {
      question: "14. ปรากฏการณ์ Belady's Anomaly (การเพิ่มจำนวน Page Frames ในหน่วยความจำ แต่กลับทำให้เกิด Page Faults มากขึ้น) เกิดขึ้นกับอัลกอริทึมใด?",
      options: [
        "A. FIFO (First-In, First-Out)",
        "B. Optimal Page Replacement (OPT)",
        "C. Least Recently Used (LRU)",
        "D. LFU (Least Frequently Used)"
      ],
      correct: 0,
      explanation: "Belady's Anomaly เกิดขึ้นกับอัลกอริทึม FIFO เนื่องจาก FIFO ไม่ได้จัดอยู่ในกลุ่ม Stack Algorithm ขณะที่ OPT และ LRU มีคุณสมบัติ Stack Algorithm จึงรับประกันว่าจะไม่เกิด Belady's Anomaly แน่นอน"
    },
    {
      question: "15. ปัญหาการเกิด Thrashing ในระบบปฏิบัติการ มีสาเหตุหลักมาจากสิ่งใด?",
      options: [
        "A. มีโปรเซสมากเกินไปจนผลรวมขนาดของ Working Sets เกินหน่วยความจำจริง ทำให้ระบบเสียเวลาส่วนใหญ่ไปกับการทำ Paging I/O สลับหน้าเข้า-ออก",
        "B. ซีพียูร้อนจัดจนต้องหยุดประมวลผล",
        "C. ขนาด Page Table เล็กเกินกว่า 1KB",
        "D. ฮาร์ดแวร์แคช TLB มี Hit Ratio สูงเกิน 99%"
      ],
      correct: 0,
      explanation: "Thrashing เกิดเมื่อ Degree of Multiprogramming สูงเกินไป ทำให้แต่ละโปรเซสได้เฟรมน้อยกว่า Working Set ส่งผลให้เกิด Page Fault ถี่ขึ้นตลอดเวลา ระบบจึงมัวแต่ทำ I/O สลับหน้าจน CPU Utilization ตกลงเกือบเป็นศูนย์"
    },
    {
      question: "16. ใน Banker's Algorithm หากโปรเซส P0 ร้องขอทรัพยากรเพิ่ม [0, 2, 0] และคลังมี Available = [2, 2, 1] เหตุใดระบบจึงต้องปฏิเสธคำขอ ทั้งที่ทรัพยากรในคลังมีเพียงพอแจกจ่าย?",
      options: [
        "A. เพราะฮาร์ดแวร์ดิสก์เกิดความเสียหาย",
        "B. เพราะ P0 ร้องขอเกินสิทธิ์ Need[P0]",
        "C. เพราะการจัดสรรจะทำให้ทรัพยากร B เหลือ 0 และระบบตกสู่ Unsafe State ไม่มีโปรเซสใดรันต่อได้เลย",
        "D. เพราะโปรเซส P0 มีระดับ Priority ต่ำที่สุดในระบบ"
      ],
      correct: 2,
      explanation: "แม้ว่า B จะมี 2 หน่วยพอให้ยืม แต่ถ้าให้ไปแล้ว ทรัพยากร B จะเหลือ 0 เมื่อตรวจสอบ Need ของทุกโปรเซสจะพบว่าไม่มีโปรเซสใดรันจบได้เลย ระบบจะติดหล่มและตกสู่ Unsafe State ทันที แบงก์จึงปฏิเสธเพื่อหลีกเลี่ยง Deadlock ล่วงหน้า (Safety Avoidance)"
    },
    {
      question: "17. Dispatch Latency คืออะไร และเหตุใดจึงถือเป็นค่าใช้จ่ายสูญเปล่า (Overhead) ของระบบปฏิบัติการ?",
      options: [
        "A. เวลาที่ใช้ในการอ่านเขียนไฟล์จาก SSD",
        "B. เวลาที่ตัวส่งงาน (Dispatcher) ต้องใช้ในการหยุดโปรเซสเก่า สลับบริบท และโหลดโปรเซสใหม่ ซึ่งซีพียูไม่ได้ทำงานที่เป็นประโยชน์แก่ผู้ใช้เลย",
        "C. เวลาที่แคช L1 ใช้ในการค้นหาแท็กแอดเดรส",
        "D. เวลาที่บัส PCIe ใช้ในการส่งภาพขึ้นหน้าจอ"
      ],
      correct: 1,
      explanation: "Dispatch Latency เป็นเวลาที่ Dispatcher ต้องใช้ในการเซฟ PCB เก่า, สลับ Context, โหลด PCB ใหม่ และ Flash TLB ในช่วงเวลานี้ระบบไม่ได้รันโค้ดของผู้ใช้เลย จึงถือเป็น System Overhead โดยตรง"
    },
    {
      question: "18. ในระบบที่ใช้ Relocation Register (Base) = 24,600 และ Limit Register = 2,048 หากโปรเซสอ้างอิงตำแหน่งตรรกะที่ 2,300 จะเกิดผลลัพธ์ตามข้อใด?",
      options: [
        "A. แปลงเป็นตำแหน่งทางกายภาพ 26,900",
        "B. แปลงเป็นตำแหน่งทางกายภาพ 22,300",
        "C. เกิดข้อผิดพลาด Addressing Error / Trap (Segmentation Fault) เพราะ 2,300 เกินกว่า Limit Register",
        "D. ระบบจะขยายขนาด Limit Register ให้โดยอัตโนมัติ"
      ],
      correct: 2,
      explanation: "ฮาร์ดแวร์ MMU จะตรวจสอบก่อนว่า Logical Address < Limit Register หรือไม่ เมื่อ 2,300 < 2,048 เป็นเท็จ (เกินขอบเขตที่ได้รับอนุญาต) ฮาร์ดแวร์จะส่งสัญญาณ Trap สั่งตัดตอนโปรเซสทันทีเพื่อป้องกันการบุกรุกหน่วยความจำ"
    },
    {
      question: "19. ในระบบแบ่งหน้าแบบ 2 ระดับ (Two-Level Paging) ที่มี Page Size 4 KB เมื่อแบ่งหมายเลขหน้าเป็น p1 = 10 บิต และ p2 = 10 บิต และแต่ละเอนทรีมีขนาด 4 ไบต์ ขนาดของ Outer Table และ Inner Table แต่ละตารางจะมีขนาดเท่าใด?",
      options: [
        "A. 1 KB ต่อตาราง",
        "B. 4 KB ต่อตาราง (พอดีกับขนาด 1 หน้าเพจ)",
        "C. 16 KB ต่อตาราง",
        "D. 4 MB ต่อตาราง"
      ],
      correct: 1,
      explanation: "ขนาดของตาราง = 2^10 เอนทรี × 4 ไบต์ = 1,024 × 4 ไบต์ = 4,096 ไบต์ = 4 KB ซึ่งมีขนาดพอดีกับ 1 เฟรมหน้าเพจ ทำให้สามารถจัดสรรลงในหน่วยความจำได้อย่างลงตัวพอดี"
    },
    {
      question: "20. หากผู้ใช้ 60 คนเปิดโปรแกรมแก้ไขข้อความเดียวกัน ซึ่งมีรหัสคำสั่งแบบ Reentrant Code ขนาด 120 KB และมีพื้นที่ข้อมูลส่วนตัวคนละ 40 KB การใช้เพจร่วมกัน (Shared Pages) จะช่วยประหยัดหน่วยความจำได้กี่เปอร์เซ็นต์ (ตรงตาม HW5 ข้อ 1.6)?",
      options: [
        "A. 25.00%",
        "B. 50.00%",
        "C. 73.75%",
        "D. 90.50%"
      ],
      correct: 2,
      explanation: "กรณีไม่แชร์เพจ: ใช้ 60 × (120 + 40) = 9,600 KB; กรณีแชร์เพจ: ใช้โค้ดแชร์ 120 KB + ข้อมูลส่วนตัว (60 × 40 = 2,400 KB) = 2,520 KB; เปอร์เซ็นต์ที่ประหยัดได้ = ((9,600 - 2,520) / 9,600) × 100 = 73.75%"
    }
  ];

  let currentIdx = 0;
  let userAnswers = new Array(quizData.length).fill(null);
  let score = 0;

  const questionText = document.getElementById('questionText');
  const optionsGrid = document.getElementById('optionsGrid');
  const explanationCard = document.getElementById('explanationCard');
  const explanationText = document.getElementById('explanationText');
  const progressText = document.getElementById('quizProgressText');
  const scoreText = document.getElementById('quizScoreText');
  const progressFill = document.getElementById('quizProgressFill');
  const prevBtn = document.getElementById('prevQuestionBtn');
  const nextBtn = document.getElementById('nextQuestionBtn');
  const resetBtn = document.getElementById('resetQuizBtn');

  if (!questionText || !optionsGrid) return;

  function loadQuestion(idx) {
    currentIdx = idx;
    const q = quizData[idx];

    // Update Progress
    if (progressText) progressText.textContent = `ข้อ ${idx + 1} จากทั้งหมด ${quizData.length} ข้อ`;
    if (progressFill) progressFill.style.width = `${((idx + 1) / quizData.length) * 100}%`;
    if (prevBtn) prevBtn.disabled = idx === 0;
    if (nextBtn) {
      nextBtn.innerHTML = idx === quizData.length - 1 ? 'สรุปคะแนน <i class="fa-solid fa-flag-checkered"></i>' : 'ข้อถัดไป <i class="fa-solid fa-arrow-right"></i>';
    }

    questionText.textContent = q.question;
    optionsGrid.innerHTML = '';

    const answered = userAnswers[idx] !== null;

    q.options.forEach((opt, optIdx) => {
      const btn = document.createElement('button');
      btn.className = 'option-btn';
      btn.textContent = opt;

      if (answered) {
        btn.disabled = true;
        if (optIdx === q.correct) {
          btn.classList.add('correct');
        } else if (optIdx === userAnswers[idx]) {
          btn.classList.add('wrong');
        }
      } else {
        btn.addEventListener('click', () => handleOptionClick(optIdx));
      }

      optionsGrid.appendChild(btn);
    });

    if (answered) {
      showExplanation(q.explanation);
    } else {
      hideExplanation();
    }

    updateScoreDisplay();
  }

  function handleOptionClick(selectedOptIdx) {
    if (userAnswers[currentIdx] !== null) return;

    userAnswers[currentIdx] = selectedOptIdx;
    const q = quizData[currentIdx];

    if (selectedOptIdx === q.correct) {
      score++;
    }

    // Refresh current question with highlights
    loadQuestion(currentIdx);
  }

  function showExplanation(text) {
    if (!explanationCard || !explanationText) return;
    explanationText.innerHTML = text;
    explanationCard.classList.add('show');
  }

  function hideExplanation() {
    if (explanationCard) explanationCard.classList.remove('show');
  }

  function updateScoreDisplay() {
    if (scoreText) scoreText.textContent = `${score} / ${quizData.length}`;
  }

  if (prevBtn) {
    prevBtn.addEventListener('click', () => {
      if (currentIdx > 0) loadQuestion(currentIdx - 1);
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      if (currentIdx < quizData.length - 1) {
        loadQuestion(currentIdx + 1);
      } else {
        showFinalSummary();
      }
    });
  }

  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
      if (confirm('คุณต้องการรีเซ็ตคำตอบและเริ่มทำแบบทดสอบใหม่ทั้งหมดหรือไม่?')) {
        currentIdx = 0;
        userAnswers = new Array(quizData.length).fill(null);
        score = 0;
        loadQuestion(0);
      }
    });
  }

  function showFinalSummary() {
    const percent = Math.round((score / quizData.length) * 100);
    let gradeMsg = '';

    if (percent >= 80) {
      gradeMsg = 'ยอดเยี่ยมมาก! คุณพร้อมลุยข้อสอบปลายภาค OS เกรด A แน่นอน 🌟';
    } else if (percent >= 60) {
      gradeMsg = 'ทำได้ดีมาก! ทบทวนข้อที่พลาดและสูตร EMAT อีกรอบจะยิ่งมั่นใจขึ้น 👍';
    } else {
      gradeMsg = 'ยังต้องทบทวนเพิ่มอีกนิด ลองกลับไปอ่านสรุปบทที่ 5 และ 8 อีกรอบนะ สู้ๆ! 💪';
    }

    alert(`🎉 สรุปผลการทดสอบ OS Final Exam\n\nคะแนนที่ได้: ${score} จาก ${quizData.length} ข้อ (${percent}%)\n\n${gradeMsg}`);
  }

  // Load first question
  loadQuestion(0);
}
