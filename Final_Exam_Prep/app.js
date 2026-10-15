/**
 * OS Final Exam Prep - Core Interactive Engine
 * Handles Navigation, Theme Toggling, Live Calculators, Simulators & Practice Quiz
 */

document.addEventListener('DOMContentLoaded', () => {
  initNavigation();
  initTheme();
  initEmatCalculator();
  initPageReplacementSimulator();
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
