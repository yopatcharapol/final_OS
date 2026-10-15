# 🎓 OS Final Exam Prep & Course Archive (Operating Systems)

คลังเนื้อหา สรุปบทเรียน และเว็บแอปพลิเคชันสำหรับเตรียมสอบปลายภาควิชาระบบปฏิบัติการ (Operating Systems) แบบโต้ตอบได้จริง (Interactive Web App)

🔗 **เข้าสู่ระบบติวสอบออนไลน์ผ่าน GitHub Pages:**  
👉 **[https://yopatcharapol.github.io/final_OS/](https://yopatcharapol.github.io/final_OS/)**

---

## 🌟 ฟีเจอร์เด่นในระบบติวสอบปลายภาค (`Final_Exam_Prep/`)

### 1. 🏦 Interactive Banker's Algorithm Visual Simulator (ใหม่!)
* **ก้าวทีละขั้นตอน (Step-by-Step):** กด `Next` หรือ `Prev` เพื่อดูการสแกนหา Safe Sequence ทีละโปรเซส
* **สูตรคณิตศาสตร์เวกเตอร์สด:** แสดงการเปรียบเทียบ $\text{Need} \le \text{Work}$ แยกแกน $A, B, C$ และสูตรคืนทรัพยากร $\text{Work}_{\text{new}} = \text{Work}_{\text{old}} + \text{Allocation}$
* **แอนิเมชันไฮไลท์แถว:** แถวที่กำลังตรวจ (`👉`), แถวที่ผ่าน (`✔`), และแถวที่พักไว้ก่อน (`⏳`)
* **รองรับ 4 สถานการณ์:**
  - โจทย์การบ้านจริง HW5 (Total: $[10, 6, 8]$)
  - โจทย์ตัวอย่างจากตำรา Silberschatz (Total: $[10, 5, 7]$)
  - ทดสอบ Resource-Request $P_2$ ขอเพิ่ม $[1, 0, 1]$ (อนุมัติได้ - Safe)
  - ทดสอบ Resource-Request $P_0$ ขอเพิ่ม $[0, 2, 0]$ (ปฏิเสธ - Deadlock / Unsafe)

### 2. ⚡ Live Calculators & Simulators
* **เครื่องคำนวณ EMAT แบบเรียลไทม์:** ปรับ Hit Ratio ($\alpha$), TLB Search Time, และ RAM Access Time แล้วดูผลลัพธ์พร้อมสูตรอัตโนมัติ
* **Page Replacement Simulator:** เปรียบเทียบ FIFO vs LRU พร้อมตารางเฟรมและ Page Fault Count แบบสดๆ

### 3. 🎯 Practice Quiz (20 ข้อเก็งข้อสอบจริง)
* ข้อสอบ 20 ข้อครอบคลุมทุกบท พร้อมเฉลยละเอียดและวิเคราะห์ตัวเลือก
* ระบบจับคะแนนและตัดเกรดประเมินความพร้อมสอบปลายภาค

---

## 📁 โครงสร้างโปรเจกต์ (Repository Structure)

```text
├── Final_Exam_Prep/          # เว็บแอปสรุปติวสอบปลายภาค (HTML5 / CSS3 / Vanilla JS)
│   ├── index.html            # โครงสร้างหน้าเว็บ บทที่ 5-8, Advanced, Calculators, Quiz
│   ├── style.css             # Glassmorphism Design System & Dark/Light Themes
│   └── app.js                # Interactive Engine, Banker Simulator, EMAT & Quiz Logic
├── 01_Lectures/              # สไลด์และเอกสารการบรรยายในห้องเรียน
├── 02_Homework/              # การบ้าน แบบฝึกหัด และเฉลย
├── 03_Term_Report/           # รายงาน Term Report ฉบับสมบูรณ์ พร้อมรูปภาพและผลการทดลอง
├── index.html                # หน้า Redirect หลักสำหรับ GitHub Pages
└── README.md                 # คู่มือและเอกสารประกอบโปรเจกต์
```
