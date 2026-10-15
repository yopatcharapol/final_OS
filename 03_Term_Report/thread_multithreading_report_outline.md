# โครงสร้างรายงานวิชา Operating Systems (OS)
## หัวข้อ: Thread & Multithreading ในระบบปฏิบัติการสมัยใหม่
### (Thread & Multithreading in Modern Operating Systems)

---

## 📌 ข้อมูลและเกณฑ์ของรายงาน
* **วิชา:** ระบบปฏิบัติการ (Operating Systems)
* **เกณฑ์การส่งงาน:**
  * **แบบที่ 1 (เขียนด้วยลายมือ):** จำนวนอย่างน้อย **60 หน้า** (คะแนนเต็ม 25/25)
  * **แบบที่ 2 (พิมพ์จากคอมพิวเตอร์):** จำนวนอย่างน้อย **80 หน้า** (คะแนนเต็ม 18/25)
* **รูปแบบรายงาน:** ขนาด A4 (ไม่ต้องมีหน้าปก คำนำ สารบัญ หรือหากมีจะไม่นับรวมในจำนวนหน้า)
* **กำหนดส่ง:** 15 ต.ค. 2569 เวลา 16.00 น.

---

## 🎯 แก่นกลาง วัตถุประสงค์ และระเบียบวิธีของรายงาน (Central Thesis & Academic Framework)

### แก่นกลางและสมมติฐานหลักของรายงาน (Central Thesis):
> **"การประมวลผลแบบมัลติเธรดช่วยยกระดับ Throughput และ Scalability ของระบบปฏิบัติการเมื่อใด ภายใต้เงื่อนไขใด และสร้างภาระต้นทุนแฝง (Synchronization Contention, Cache Invalidation, Context Switching Latency) ในระดับฮาร์ดแวร์และเคอร์เนลอย่างไร?"**

### วัตถุประสงค์ของรายงาน (Objectives):
1. เพื่อศึกษาสถาปัตยกรรมภายใน โครงสร้างข้อมูล และกลไกการสลับบริบทของเธรด (Thread Context Switch) ในระบบปฏิบัติการสมัยใหม่
2. เพื่อวิเคราะห์เปรียบเทียบต้นทุน Overhead และความปลอดภัยระหว่าง Multiprocessing และ Multithreading ในเชิงลึก
3. เพื่อศึกษาและวิเคราะห์กลไกการประสานเวลา (Synchronization Primitives) ตั้งแต่ระดับเคอร์เนล (Futex, Mutex, Semaphores) จนถึงระดับฮาร์ดแวร์ (Lock-Free Atomics, Memory Barriers)
4. เพื่อวัดผลประสิทธิภาพเชิงประจักษ์ (Empirical Performance Benchmarking) ด้วยเครื่องมือ Profiling ระดับฮาร์ดแวร์ และเปรียบเทียบผลลัพธ์กับแบบจำลองทางคณิตศาสตร์ (Amdahl's Law, Gustafson's Law, Universal Scalability Law)
5. เพื่อสังเคราะห์กรอบการตัดสินใจเชิงวิศวกรรม (Engineering Decision Framework) สำหรับการเลือกใช้โมเดล Concurrency ให้เหมาะสมกับลักษณะของภาระงาน

### ขอบเขตการศึกษา (Scope of Study):
* **ระบบปฏิบัติการหลักที่ใช้ศึกษาเชิงลึก:** **Linux Kernel (NPTL / clone / CFS / Futex)** ในฐานะระบบปฏิบัติการอ้างอิงมาตรฐานทางวิศวกรรม
* **ระบบปฏิบัติการเปรียบเทียบ:** **Windows Kernel (ETHREAD / KTHREAD / Fibers)** เพื่อเปรียบเทียบปรัชญาการออกแบบ
* **การอิมพลีเมนต์และการทดลองหลัก:** ภาษา C ด้วย **POSIX Threads (Pthreads)** บนสถาปัตยกรรม x86-64 Multi-Core
* **กรณีศึกษาเปรียบเทียบเฉพาะด้าน:**
  * **Python GIL vs Free-threaded build (Python 3.13 PEP 703):** ศึกษาผลกระทบของ Runtime-level Lock ต่องาน CPU-bound
  * **Java Virtual Threads (Project Loom) & Go Goroutines:** ศึกษาการปฏิวัติสถาปัตยกรรมสู่ Lightweight User-space Concurrency สำหรับงาน I/O-bound

---

## 📊 ตารางสรุปการจัดสรรจำนวนหน้า (Page Allocation Plan)

| บทที่ | ชื่อบท (Chapter Title) | หน้าโดยประมาณ (เขียนมือ) | หน้าโดยประมาณ (พิมพ์คอม) | จุดเน้นเชิงวิชาการและการวิเคราะห์เชิงลึก (Academic & Analytical Focus) |
|:---:|---|:---:|:---:|---|
| **1** | บทนำ ที่มา และกรอบการวิจัย | 5–6 หน้า | 7–8 หน้า | ที่มาและความสำคัญ, คำถามหลัก, วัตถุประสงค์, ขอบเขต, ระเบียบวิธี, ประโยชน์ที่ได้รับ, ตาราง Process vs Thread |
| **2** | สถาปัตยกรรมและโครงสร้างภายในของเธรด | 7–8 หน้า | 9–10 หน้า | Memory Layout, TCB vs PCB, State Transition, การวิเคราะห์เงื่อนไขที่ Context Switch ไม่ต้องเปลี่ยน Page Table |
| **3** | แบบจำลองมัลติเธรดและการจับคู่ระดับเคอร์เนล | 6–7 หน้า | 8–9 หน้า | ULT vs KLT, ไดอะแกรม Many-to-1, 1-to-1, Many-to-Many, การวิเคราะห์ Trade-offs ด้าน Concurrency vs Kernel Overhead |
| **4** | เธรดกับสถาปัตยกรรมฮาร์ดแวร์และทฤษฎีความเร็ว | 8–9 หน้า | 10–12 หน้า | Concurrency vs Parallelism, ทฤษฎี Amdahl vs Gustafson vs USL, SMT/Hyper-Threading, MESI Protocol & False Sharing |
| **5** | การประสานเวลาและกลไกระดับเคอร์เนล | 10–11 หน้า | 12–14 หน้า | Race Condition, Mutex vs Spinlock, กลไก Linux Futex (Fast path vs Slow path), Lock-Free CAS, Priority Inversion |
| **6** | การทดลองและวัดผลประสิทธิภาพเชิงประจักษ์ | 11–13 หน้า | 14–17 หน้า | สภาพแวดล้อมทดลอง, ตัวแปรควบคุม, CPU Governor Lockdown, Hardware Counters ด้วย `perf`, ผลวัดพร้อม Error Bars (95% CI) |
| **7** | กลไกขั้นสูงในการจัดการเธรดระดับระบบปฏิบัติการ | 6–7 หน้า | 8–9 หน้า | พฤติกรรม `fork()` ตาม POSIX, Mutex Deadlock ในโพรเซสลูก, Thread Cancellation, TLS, Thread Pool Architecture |
| **8** | กรณีศึกษาระดับเคอร์เนล: การวิเคราะห์เปรียบเทียบ Linux vs Windows | 7–8 หน้า | 9–10 หน้า | Linux `task_struct`/`clone()` vs Windows `ETHREAD`/`KTHREAD`, Windows Fibers, NUMA & CPU Affinity Pinning |
| **9** | อนาคตและวิวัฒนาการ: Concurrency ในระดับ User-Space | 5–6 หน้า | 6–7 หน้า | C10K/C1000K problem, ข้อจำกัด Stack OS Thread, Go Goroutines (2KB Dynamic), Java 21 Virtual Threads (Loom) |
| **10** | การอภิปรายผลเชิงวิพากษ์ กรอบการตัดสินใจ และบทสรุป | 5–6 หน้า | 6–8 หน้า | วิเคราะห์จุดหักเห (Inflection point), แผนผังและตารางตัดสินใจ (Decision Matrix), ข้อจำกัดของการศึกษา, สรุป |
| **ส่วนแยก** | **บรรณานุกรมและเอกสารอ้างอิง (References)** | 2–3 หน้า | 2–3 หน้า | ตำรามาตรฐาน, IEEE/ACM papers, POSIX Standard, Linux Kernel Documentation, Official RFCs |
| **ส่วนแยก** | **ภาคผนวก (Appendices)** | 6–10 หน้า | 8–12 หน้า | ซอร์สโค้ดฉบับสมบูรณ์, ตารางบันทึกผลการทดลองดิบ ($N=10$ รอบ) พร้อมค่าสถิติ, ข้อมูล System Profile Outputs |
| **รวม** | **ประมาณการความยาวเนื้อหาหลัก (บทที่ 1–10)** | **~70–81 หน้า** | **~89–104 หน้า** | *(ผ่านเกณฑ์ขั้นต่ำ 60 หน้าเขียนมือ / 80 หน้าพิมพ์คอม อย่างมั่นคงและมีคุณภาพสูง)* |
| **รวมสุทธิ** | **รวมเนื้อหาหลัก + บรรณานุกรม + ภาคผนวก** | **~78–94 หน้า** | **~99–119 หน้า** | *(ระยะเผื่อความปลอดภัยระดับสมบูรณ์แบบ รองรับทุกกติกาการนับจำนวนหน้า)* |

---

## 📖 รายละเอียดเนื้อหาแต่ละบท (Detailed Chapter Breakdown)

### บทที่ 1: บทนำ ที่มา และกรอบการวิจัย (Introduction & Research Framework)
* **1.1 ที่มาและความสำคัญของปัญหา (Background & Problem Statement):**
  * วิวัฒนาการจาก Monoprogramming สู่ Multiprogramming
  * ต้นทุน Overhead มหาศาลในการสร้าง สลับบริบท และทำลาย Process (Heavyweight Process Problem)
  * กำเนิดแนวคิด "เธรด" (Lightweight Process: LWP) ภายใต้ Shared Address Space
* **1.2 คำถามหลักของรายงาน (Core Research Questions):**
  1. *Speedup & Overhead:* การประมวลผลแบบมัลติเธรดช่วยเพิ่ม Throughput ได้จริงในสถานการณ์ใด และมีต้นทุนแฝงระดับฮาร์ดแวร์/เคอร์เนลอย่างไร?
  2. *Architectural Trade-offs:* แบบจำลองการจับคู่เธรด (1:1, M:1, M:N) สร้างความแตกต่างด้าน Latency, Throughput และ Kernel Complexity อย่างไร?
  3. *Synchronization Bottlenecks:* เมื่อเพิ่มจำนวนเธรดบนซีพียูหลายคอร์ จุดคอขวดที่แท้จริงเกิดจากซอฟต์แวร์ล็อก หรือเกิดจาก Memory Bus และ Cache Coherence?
  4. *Mathematical Modeling:* แบบจำลองทางคณิตศาสตร์ใด (Amdahl, Gustafson, USL) ที่สามารถทำนายพฤติกรรมของระบบมัลติเธรดในการทดลองจริงได้แม่นยำที่สุด?
* **1.3 วัตถุประสงค์ของรายงาน (Objectives):** ระบุวัตถุประสงค์ 5 ประการที่ชัดเจนและวัดผลได้
* **1.4 ขอบเขตการศึกษา (Scope of Study):** ระบุระบบปฏิบัติการ (Linux/Windows), ภาษา (C/Pthreads, Python, Java, Go) และสถาปัตยกรรมฮาร์ดแวร์ (x86-64 Multi-Core)
* **1.5 ภาพรวมของระเบียบวิธีวิจัย (Methodology Overview):** การผสานทฤษฎีระบบปฏิบัติการ การวิเคราะห์โค้ด และการวัดผลเชิงประจักษ์ด้วย Hardware Performance Counters
* **1.6 ประโยชน์ที่คาดว่าจะได้รับ (Expected Benefits):** ข้อคิดเห็นและแนวทางปฏิบัติเชิงวิศวกรรมสำหรับนักพัฒนาระบบและสถาปนิกซอฟต์แวร์
* **1.7 คุณลักษณะและประโยชน์พื้นฐานของเธรด:** Responsiveness, Resource Sharing, Economy, Scalability
* **1.8 การเปรียบเทียบเชิงวิเคราะห์: Process vs. Thread:**
  * 📊 **ตารางที่ 1.1:** ตารางเปรียบเทียบคุณสมบัติเชิงลึก (Address Space, Creation Latency, Context Switch Overhead, IPC Mechanism, Fault Isolation & Failure Domain) พร้อมบทวิเคราะห์ประกอบ

---

### บทที่ 2: สถาปัตยกรรมและโครงสร้างภายในของเธรด (Thread Architecture & Internals)
* **2.1 โครงสร้างหน่วยความจำของโพรเซสที่มีหลายเธรด (Memory Layout):**
  * ส่วนที่แบ่งปันร่วมกัน: Text/Code Segment, Data Segment, BSS, Heap, File Descriptor Table, Signal Disposition
  * ส่วนที่เป็นกรรมสิทธิ์ของแต่ละเธรด: Program Counter (PC), Register State, Thread-Local Storage (TLS), User Stack และ Kernel Stack
  * 🖼️ **ภาพที่ 2.1:** แผนภาพโครงสร้าง Virtual Address Space เปรียบเทียบ Single-threaded vs. Multi-threaded Process
* **2.2 บล็อกควบคุมเธรด (Thread Control Block: TCB):**
  * องค์ประกอบภายใน TCB: Thread Identifier (TID), Saved Context (CPU Registers, SP), Scheduling Attributes, State, Priority, Link Pointers ชี้กลับไปยัง PCB แม่
  * 📊 **ตารางที่ 2.1:** การเปรียบเทียบโครงสร้างข้อมูล PCB vs. TCB
* **2.3 วงจรชีวิตและสถานะของเธรด (Thread Lifecycle & State Transitions):**
  * วงจรสถานะ New, Ready, Running, Blocked/Waiting, Terminated
  * 🖼️ **ภาพที่ 2.2:** แผนภาพสถานะ (Thread State Transition Diagram) พร้อมวิเคราะห์เหตุการณ์ที่เป็นตัวกระตุ้น (System Call, I/O, Preemption)
* **2.4 กลไกการสลับบริบทของเธรด (Thread Context Switch Mechanics):**
  * ขั้นตอนการ Save และ Restore Execution Context ลงใน TCB
  * ⚠️ **การวิเคราะห์เงื่อนไขทางเทคนิค:** ทำไม Thread Context Switch จึงมักเร็วกว่า Process Context Switch?
    * เมื่อสลับระหว่างเธรดในโพรเซสเดียวกัน *ไม่จำเป็นต้องเปลี่ยน Page Table Register (เช่น `CR3` ใน x86)* และไม่ต้อง Flush Translation Lookaside Buffer (TLB)
    * หากสลับข้ามโพรเซส เคอร์เนลยังคงต้องเปลี่ยน Page Table และรับภาระ TLB Invalidation เสมือน Process Context Switch

---

### บทที่ 3: แบบจำลองมัลติเธรดและการจับคู่ระดับเคอร์เนล (Multithreading Models & Kernel Mapping)
* **3.1 ระดับชั้นของเธรด (Thread Hierarchy):**
  * **User-Level Threads (ULT):** ทำงานใน User Space จัดการโดย Runtime Library รวดเร็วมากแต่เคอร์เนลมองไม่เห็น
  * **Kernel-Level Threads (KLT):** เคอร์เนลเป็นผู้สร้างและจัดตารางเวลา รองรับการประมวลผลบนหลายคอร์แท้จริงแต่มี System Call Overhead
* **3.2 แบบจำลองการจับคู่เธรด (Thread Mapping Models):**
  * **Many-to-One Model (M:1):**
    * โครงสร้างและการทำงานใน User Space
    * ข้อจำกัดเชิงวิศวกรรม: หากเธรดหนึ่งเรียก Blocking System Call ทั้งโพรเซสจะถูกระงับการทำงาน (Process-wide blocking) และไม่สามารถใช้ประโยชน์จาก Multi-core ได้
    * 🖼️ **ภาพที่ 3.1:** แผนภาพ Many-to-One Model
  * **One-to-One Model (1:1):**
    * โครงสร้าง: ทุกลำดับการทำงานของผู้ใช้ผูกกับ Kernel Thread 1 ตัว
    * ข้อดี: Concurrency สมบูรณ์แบบ เธรดหนึ่งบล็อกไม่กระทบเธรดอื่น รันขนานบนฮาร์ดแวร์ได้จริง (มาตรฐานใน Linux NPTL, Windows, macOS)
    * ข้อจำกัด: สิ้นเปลืองทรัพยากรเคอร์เนล มีขีดจำกัดด้านความสามารถในการขยายขนาด (Scalability Limit)
    * 🖼️ **ภาพที่ 3.2:** แผนภาพ One-to-One Model
  * **Many-to-Many Model (M:N) และ Two-Level Model:**
    * การ Multiplexing ระหว่าง User Threads จำนวนมาก ลงบน Kernel Threads ที่มีจำนวนเหมาะสม
    * ปัญหาความซับซ้อนในการประสานงานระหว่างเคอร์เนลและ User Library (Scheduler Activations)
    * 🖼️ **ภาพที่ 3.3:** แผนภาพ Many-to-Many และ Two-Level Model
* **3.3 ตารางสรุปเปรียบเทียบเชิงวิศวกรรมของทั้ง 3 โมเดล (Throughput, Overhead, Complexity, Fault Tolerance)**

---

### บทที่ 4: เธรดกับสถาปัตยกรรมฮาร์ดแวร์และทฤษฎีความเร็ว (Hardware Architecture & Scalability Laws)
* **4.1 Concurrency กับ Parallelism:**
  * นิยามเชิงสถาปัตยกรรม:
    * **Concurrency:** การจัดการโครงสร้างโปรแกรมให้หลายงานสามารถก้าวหน้าได้ร่วมกัน (จัดการงานหลายอย่างในเวลาเดียวกัน) ทำได้ทั้งบน Single-Core (Interleaving) และ Multi-Core
    * **Parallelism:** การประมวลผลคำสั่งหลายคำสั่งให้เกิดขึ้นจริงในขณะเดียวกัน (ทำหลายงานพร้อมกันในเสี้ยววินาทีเดียวกัน) ต้องมีหน่วยประมวลผลหลายชุด
  * 🖼️ **ภาพที่ 4.1:** แผนผังไทม์ไลน์เปรียบเทียบ Interleaved Concurrency vs True Hardware Parallelism
* **4.2 รูปแบบการทำงานแบบขนาน (Parallelism Paradigms):** Data Parallelism vs. Task Parallelism
* **4.3 แบบจำลองทางคณิตศาสตร์ในการวัดความเร็วและการขยายขนาด (Scalability Models):**
  * **Amdahl’s Law (Fixed-Workload Speedup):**
    $$\text{Speedup}_{\text{Amdahl}} \le \frac{1}{S + \frac{1 - S}{N}}$$
  * 🌟 **Gustafson-Barsis’s Law (Scaled-Workload Speedup):**
    $$\text{Speedup}_{\text{Gustafson}} = s + N(1 - s) = N - s(N - 1)$$
    *(อธิบายพฤติกรรมของระบบเมื่อขนาดของปัญหาขยายตัวตามจำนวนคอร์ที่มี)*
  * 🌟 **Universal Scalability Law (USL โดย Neil Gunther):**
    $$C(N) = \frac{N}{1 + \alpha(N - 1) + \beta N(N - 1)}$$
    *(แบบจำลองที่คำนึงถึงทั้ง Contention Delay ($\alpha$) และ Coherency Delay ($\beta$) อธิบายสาเหตุของ Retrograde Speedup)*
  * 🔢 **การวิเคราะห์เปรียบเทียบผ่านกราฟ:** จำลองกราฟเส้นเปรียบเทียบทั้ง 3 ทฤษฎีเพื่อชี้ให้เห็นขีดจำกัดสูงสุดของการเพิ่มจำนวนคอร์
* **4.4 ปฏิสัมพันธ์ระหว่างเธรดกับฮาร์ดแวร์ซีพียู:**
  * **Simultaneous Multithreading (SMT) และ Intel Hyper-Threading:**
    * กลไกการแชร์ Execution Units ภายในคอร์กายภาพเดียวกัน
    * ⚠️ **ข้อเท็จจริงด้านประสิทธิภาพ:** SMT ไม่ได้เพิ่มพลังการประมวลผลเป็น 2 เท่า (โดยทั่วไปเพิ่ม Throughput ได้ 15–30%) และหากเกิดการแย่งแคช Latency ต่อเธรดจะเพิ่มขึ้น
  * **ลำดับชั้นแคชและโปรโตคอลความสอดคล้อง (Cache Hierarchy & Coherence):**
    * Private Cache (L1, L2) และ Shared Cache (L3)
    * โปรโตคอล **MESI (Modified, Exclusive, Shared, Invalid)**
    * ⚠️ **ปัญหา False Sharing:** เมื่อข้อมูลอิสระของสองเธรดตกอยู่ใน Cache Line ขนาด 64 Bytes เดียวกัน ทำให้เกิด Bus Invalidation พุ่งสูงอย่างรุนแรง พร้อมแนวทางการแก้ด้วย Data Alignment (`alignas(64)`)
  * **Memory Consistency Models & Memory Barriers:**
    * ปัญหา Hardware Instruction Reordering ในซีพียูแบบ Out-of-Order (x86 TSO vs ARM Weak Memory Ordering)
    * กลไก Memory Barriers (`mfence`, `acquire-release` semantics)

---

### บทที่ 5: การประสานเวลาและกลไกระดับเคอร์เนล (Thread Synchronization & Kernel Primitives)
* **5.1 ภาวะการแย่งชิงข้อมูล (Race Condition):**
  * การเกิด Race Condition ในระดับการเข้าถึงหน่วยความจำ
  * นิยามของ Critical Section และเกณฑ์ 3 ประการของ Dijkstra (Mutual Exclusion, Progress, Bounded Waiting)
* **5.2 กลไกการซิงโครไนซ์ระดับระบบปฏิบัติการ:**
  * **Mutex Locks (Mutual Exclusion):** หลักการทำงานและต้นทุนการสลับโหมดเข้าสู่เคอร์เนล
  * **Spinlocks:** การรอแบบ Busy-waiting vs Sleeping/Blocking กรณีที่ Spinlock มีประสิทธิภาพเหนือกว่า Mutex (งานสั้นมากบนระบบ Multi-core)
  * **Semaphores:** Counting Semaphore vs Binary Semaphore และการแก้ปัญหา Classic Producer-Consumer
  * **Condition Variables:** การใช้ `wait()` และ `signal()` / `broadcast()` ร่วมกับ Mutex เพื่อบริหารจัดการคิวการรอ
* **5.3 กลไกการซิงโครไนซ์ขั้นสูงในระดับเคอร์เนลสมัยใหม่:**
  * 🌟 **Linux Futex (Fast Userspace Mutex):**
    * สถาปัตยกรรมแบบไฮบริด: Fast-path ทำงานใน User Space ผ่าน Atomic Instruction เมื่อไม่มี Contention โดยไม่ต้องเกิด Trap/Context Switch
    * Slow-path เรียกใช้ System Call `sys_futex()` เพื่อนำเธรดเข้าคิวรอในเคอร์เนลเฉพาะเมื่อเกิดการแย่งชิง (Contended case)
  * 🌟 **การประสานเวลาแบบไร้ล็อก (Lock-Free Synchronization):**
    * คำสั่งฮาร์ดแวร์ระดับอะตอมิก: **Compare-And-Swap (CAS)** และ Load-Linked / Store-Conditional (LL/SC)
    * ปัญหา **ABA Problem** ใน Lock-free Data Structures และการแก้ไขด้วย Tagged Pointers / Version Counter
* **5.4 ปัญหาคลาสสิกและการป้องกันความผิดพลาดในระบบมัลติเธรด:**
  * **ภาวะติดตาย (Deadlock ในระดับเธรด):** เงื่อนไข 4 ประการของ Coffman และการป้องกันด้วยเทคนิค Lock Ordering
  * **Livelock & Starvation:** พฤติกรรม ข้อแตกต่าง และแนวทางแก้ไข
  * **Priority Inversion & Priority Inheritance Protocol:** กรณีศึกษาภารกิจยาน Mars Pathfinder

---

### บทที่ 6: การทดลองและวัดผลประสิทธิภาพเชิงประจักษ์ (Implementation & Empirical Benchmarking)
* **6.1 การอิมพลีเมนต์โปรแกรมทดสอบด้วยภาษา C (POSIX Pthreads):**
  * การเขียนโปรแกรมคำนวณการคูณเมทริกซ์ (Matrix Multiplication) ขนาดใหญ่
  * 📝 **การวิเคราะห์โค้ด:** การแบ่งชิ้นข้อมูล (Data Partitioning) แบบ Row-wise Striping เพื่อหลีกเลี่ยง False Sharing
* **6.2 กรณีศึกษาเปรียบเทียบ: ข้อจำกัดของ Runtime Lock (Python GIL):**
  * กลไก Global Interpreter Lock ใน CPython: เหตุใดเธรดจึงไม่สามารถรัน CPU-bound บนหลายคอร์ได้จริง
  * ⚠️ **การทดสอบโหมด Free-threaded build ใน Python 3.13 (PEP 703):** การวัดผลเปรียบเทียบระหว่าง Python Standard (มี GIL) vs Free-threaded Python (ปิด GIL)
* **6.3 ระเบียบวิธีดำเนินการทดลองอย่างเป็นระบบ (Experimental Methodology & Rigor):**
  * **การควบคุมตัวแปรและสภาพแวดล้อม (Controlled Environment):**
    * การล็อก CPU Frequency Governor ให้อยู่ในโหมด `performance` เพื่อปิดกั้นผลกระทบของ Dynamic Turbo Boost Jitter
    * การปิด Background Services และการทดลองบนคอร์ที่กำหนดผ่าน CPU Pinning
  * **เครื่องมือวัดผลระดับฮาร์ดแวร์ (Hardware Performance Profiling via Linux `perf`):**
    * การตรวจจับฮาร์ดแวร์เคาน์เตอร์จริง:
      * Last-Level Cache (LLC) Misses
      * Instructions Per Cycle (IPC)
      * Voluntary vs Involuntary Context Switches (ดึงจาก `/proc/[pid]/status`)
  * **การเลือกชนิดของภาระงาน (Workloads):**
    1. งานประมวลผลคำนวณ (CPU-bound Workload): Matrix Multiplication ($1024 \times 1024$)
    2. งานรอคอยข้อมูล (I/O-bound Workload): Concurrent File Read / Network Request Simulation
  * **ระเบียบวิธีทางสถิติ (Statistical Rigor):**
    * รันการทดลองซ้ำ $N = 10$ รอบต่อหนึ่งเงื่อนไข ทำการ Warm-up เพื่อเตรียม Cache
    * แสดงผลลัพธ์เป็นค่าเฉลี่ย ($\mu$) และส่วนเบี่ยงเบนมาตรฐาน ($\sigma$) พร้อมคำนวณช่วงความเชื่อมั่น 95% ($95\%\text{ CI}$)
* **6.4 ผลการทดลองและการวิเคราะห์เชิงประจักษ์ (Empirical Results):**
  * 📊 **ตารางบันทึกผลการทดลอง:** เปรียบเทียบระยะเวลาทำงาน, Throughput, LLC Misses ระหว่าง 1, 2, 4, 8, 16 เธรด
  * 📈 **กราฟเปรียบเทียบ Speedup พร้อม Error Bars:** พล็อตเทียบกับเส้นสมมติฐานทางทฤษฎีของ Amdahl, Gustafson และ USL

---

### บทที่ 7: กลไกขั้นสูงในการจัดการเธรดระดับระบบปฏิบัติการ (Advanced Threading Mechanics)
* **7.1 พฤติกรรมของ System Call `fork()` และ `exec()` ในมัลติเธรด:**
  * ⚠️ **ข้อเท็จจริงตามมาตรฐาน POSIX:** เมื่อเธรดหนึ่งเรียก `fork()` โพรเซสลูกจะมีเพียง **เธรดเดียว** คือเธรดที่เรียก `fork()`
  * อันตรายของ Mutex Deadlock ในโพรเซสลูก (เมื่อเธรดอื่นค้างล็อกไว้ก่อนการ fork) และการแก้ปัญหาด้วย `pthread_atfork()`
  * พฤติกรรมเมื่อเรียก `exec()`: การเคลียร์ Address Space เดิมและยกเลิกเธรดทั้งหมดเพื่อโหลดโปรแกรมใหม่
* **7.2 การยกเลิกเธรด (Thread Cancellation):**
  * **Asynchronous Cancellation:** ความเสี่ยงสูงเรื่อง Resource Leaks และ Deadlock
  * **Deferred Cancellation:** การยกเลิกอย่างเป็นระเบียบ ณ จุด Cancellation Points พร้อมการลงทะเบียน Cleanup Handlers
* **7.3 การจัดการสัญญาณในระบบมัลติเธรด (Signal Handling):**
  * Synchronous Signals (SIGSEGV, SIGFPE) ส่งตรงไปยังเธรดที่ก่อข้อผิดพลาด
  * Asynchronous Signals (SIGINT, SIGTERM) และแนวทางปฏิบัติด้านความปลอดภัยโดยใช้ Dedicated Signal Handling Thread (`sigwait()`)
* **7.4 หน่วยความจำเฉพาะเธรด (Thread-Local Storage: TLS):**
  * ความจำเป็นของตัวแปร Global ที่แยกเป็นอิสระสำหรับแต่ละเธรด
  * กลไกคอมไพเลอร์และเคอร์เนล: การจัดเก็บผ่าน Thread Pointer (เช่น FS/GS segment registers บน x86-64)
* **7.5 สถาปัตยกรรมเธรดพูล (Thread Pools):**
  * ปัญหา Unbounded Thread Creation และ Resource Exhaustion
  * การออกแบบ Work Queue, Worker Threads, และ Lifespan Management
  * 🖼️ **ภาพที่ 7.1:** สถาปัตยกรรมการทำงานของ Thread Pool

---

### บทที่ 8: กรณีศึกษาระดับเคอร์เนล: การวิเคราะห์เปรียบเทียบ Linux vs Windows (Kernel Case Studies)
* **8.1 มัลติเธรดในระบบปฏิบัติการ Linux:**
  * ปรัชญาการออกแบบ: มองทั้งโพรเซสและเธรดเป็น "Task" ภายใต้โครงสร้าง `task_struct`
  * ซิสเต็มคอล `clone()` และแฟล็กควบคุมการแชร์ (`CLONE_VM`, `CLONE_FS`, `CLONE_FILES`, `CLONE_SIGHAND`, `CLONE_THREAD`)
  * วิวัฒนาการสู่ **Native POSIX Thread Library (NPTL)** และโครงสร้างการจัดตารางเวลาของ Completely Fair Scheduler (CFS)
* **8.2 มัลติเธรดในระบบปฏิบัติการ Windows:**
  * การแยกโครงสร้างข้อมูล: `ETHREAD` (Executive Layer) และ `KTHREAD` (Microkernel Layer)
  * ⚠️ **แนวคิด Fibers ใน Windows:**
    * รูปแบบ User-mode Concurrency ที่ทำงานแบบ Cooperative (ผู้ใช้ต้องสลับบริบทเอง)
    * ข้อเท็จจริงเชิงสถาปัตยกรรม: แม้การสลับ Fiber จะทำใน User Mode แต่ **Thread ที่เป็นโฮสต์รัน Fiber เหล่านั้นยังคงถูกจัดตารางเวลาโดย Windows Kernel Scheduler ตามปกติ**
* **8.3 สถาปัตยกรรม NUMA และ CPU Affinity:**
  * 🌟 **Non-Uniform Memory Access (NUMA):** ผลกระทบของ Memory Latency ที่ไม่เท่ากันระหว่าง Local และ Remote Node ในซีพียูหลายซ็อกเก็ต
  * **CPU Pinning / Thread Affinity:** การล็อกเธรดให้อยู่กับคอร์กายภาพด้วย `pthread_setaffinity_np()` เพื่อรักษา Cache Warmth และลดการสลับคอร์ข้าม NUMA Node

---

### บทที่ 9: อนาคตและวิวัฒนาการ: Concurrency ในระดับ User-Space (Modern Concurrency Paradigms)
* **9.1 ปัญหาของ OS Threads กับแอปพลิเคชันยุค Web Scale (C10K และ C1000K Problem):**
  * ⚠️ **ขนาด Stack ของ OS Thread:** การจองพื้นที่ Virtual Memory ให้กับ Stack 1–2 MB ต่อเธรด แม้ Physical RAM จะถูกจัดสรรตามที่ใช้จริง แต่การจอง Virtual Address Space มหาศาลและ Kernel Overhead ทำให้ระบบไม่สามารถสร้าง OS Threads หลักแสนหรือหลักล้านพร้อมกันได้
* **9.2 การกลับมาของ User-space Lightweight Concurrency ยุคใหม่:**
  * **Goroutines ในภาษา Go:**
    * รูทีนที่เริ่มต้นด้วย Stack ขนาดเล็กมาก (ประมาณ 2 KB ในเวอร์ชันปัจจุบัน) และสามารถขยาย/หดได้แบบไดนามิก (Contiguous Stack)
    * สถาปัตยกรรม Go Runtime: แบบจำลอง M:N Scheduler พร้อมระบบ Work-stealing Algorithm
  * **Virtual Threads ใน Java 21 (Project Loom):**
    * บทบาทที่แท้จริง: ออกแบบมาเพื่อเพิ่ม Throughput ให้กับงานประเภท I/O-bound
    * ชี้แจงข้อเท็จจริง: Virtual Threads ไม่ได้ทำให้งาน CPU-bound ทำงานเร็วขึ้น แต่ช่วยให้เซิร์ฟเวอร์รองรับ Concurrent Tasks ได้นับล้านโดยใช้โค้ด Synchronous สไตล์เดิมที่อ่านและดีบักง่าย
* **9.3 Event-driven vs. Multithreading vs. Structured Concurrency:**
  * การเปรียบเทียบโมเดล Single-threaded Event Loop (Node.js) กับ Preemptive Multi-threaded Server และ Virtual Threading Model

---

### บทที่ 10: การอภิปรายผลเชิงวิพากษ์ กรอบการตัดสินใจ และบทสรุป (Critical Discussion, Decision Matrix & Conclusion)
* **10.1 การอภิปรายผลการศึกษาและการทดลองเชิงวิพากษ์ (Critical Discussion & Synthesis):**
  * **การวิเคราะห์จุดตัดของเส้นกราฟ (Inflection Point):** ทำไมการเพิ่มจำนวนเธรดเกินจำนวน Physical Cores จึงทำให้กราฟตกลง (Over-subscription, Time-slice Preemption, และ Cache Invalidation)
  * **การเปรียบเทียบผลลัพธ์จริงกับ 3 ทฤษฎีความเร็ว:** นำผลวัดจริงมา Fit กับสมการ Amdahl, Gustafson และ USL เพื่อหาค่าพารามิเตอร์ Contention ($\alpha$) และ Coherency ($\beta$)
  * **ต้นทุนแฝงที่มองไม่เห็น (The Hidden Overheads):** การวิเคราะห์ความสัมพันธ์ระหว่างจำนวนคอร์กับ Bus Saturation
* **10.2 กรอบการตัดสินใจทางวิศวกรรมสำหรับสถาปนิกซอฟต์แวร์ (Engineering Decision Framework):**
  * 📊 **แผนผังและตารางตัดสินใจ (Decision Matrix / Flowchart):** 
    * เมื่อใดควรเลือกใช้: Multiprocessing, OS Threads, Thread Pools, Event-driven Async (Epoll/Kqueue), หรือ Virtual Threads / Goroutines
    * การประเมินตามมิติ: Throughput, Latency, Memory Footprint, Fault Isolation, และ Debuggability
* **10.3 ข้อจำกัดของการศึกษาและการทดลอง (Limitations of the Study):**
  * ข้อจำกัดทางด้านสภาพแวดล้อมฮาร์ดแวร์ที่ใช้ทดสอบ (Desktop/Laptop testbed vs NUMA Multi-socket Server)
  * ข้อจำกัดของสัญญาณรบกวน (Jitter / Background Noise) จากระบบปฏิบัติการ
* **10.4 สรุปภาพรวมและแนวทางในอนาคต (Conclusion & Future Outlook):**
  * สรุปแก่นแท้ของวิวัฒนาการเธรดในระบบปฏิบัติการ และบทสรุปสำหรับวิศวกรคอมพิวเตอร์

---

## 📚 เอกสารอ้างอิงและบรรณานุกรม (References & Bibliography)
*(ส่วนแยกท้ายเล่มตามมาตรฐานสากล IEEE/ACM Style)*
1. **ตำราเรียนมาตรฐาน (Core Textbooks):**
   * Silberschatz, A., Galvin, P. B., & Gagne, G. (2018). *Operating System Concepts* (10th ed.). John Wiley & Sons.
   * Arpaci-Dusseau, R. H., & Arpaci-Dusseau, A. C. (2018). *Operating Systems: Three Easy Pieces*. Arpaci-Dusseau Books.
   * Tanenbaum, A. S., & Bos, H. (2014). *Modern Operating Systems* (4th ed.). Pearson.
   * Love, R. (2010). *Linux Kernel Development* (3rd ed.). Addison-Wesley Professional.
   * Russinovich, M., Solomon, D. A., & Ionescu, A. (2017). *Windows Internals* (7th ed.). Microsoft Press.
2. **เอกสารมาตรฐานและเปเปอร์วิชาการระดับคลาสสิก (Seminal Academic Papers):**
   * Amdahl, G. M. (1967). *Validity of the single processor approach to achieving large scale computing capabilities*. AFIPS.
   * Gustafson, J. L. (1988). *Reevaluating Amdahl's law*. Communications of the ACM.
   * Gunther, N. J. (2007). *Guerrilla Capacity Planning: A Metric Approach to Designing and Managing Computing Systems*. Springer.
   * Anderson, T. E., Bershad, B. N., Lazowska, E. D., & Levy, H. M. (1992). *Scheduler Activations: Effective Kernel Support for the User-Level Management of Parallelism*. ACM TOCS.
   * Drepper, U. (2007). *What Every Programmer Should Know About Memory*. Red Hat, Inc.
3. **เอกสารทางการและซอร์สโค้ด (Official Documentation & Source):**
   * Linux Kernel Documentation: `futex(2)`, `clone(2)`, `sched(7)`, `pthread_setaffinity_np(3)`.
   * Microsoft Learn: Process and Thread Architecture, Fibers, User-Mode Scheduling.
   * Oracle Java SE 21 Documentation: JEP 444: Virtual Threads.
   * Python Documentation: PEP 703 – Making the Global Interpreter Lock Optional in CPython.
   * The Go Authors: Go Runtime Hacking Notes and Work-Stealing Scheduler Specification.

---

## 📎 ภาคผนวก (Appendices)
*(ส่วนแยกสำหรับโค้ดฉบับเต็มและข้อมูลดิบ เพื่อไม่ให้รบกวนความต่อเนื่องของเนื้อหาหลัก)*
* **ภาคผนวก ก: ซอร์สโค้ดโปรแกรมฉบับสมบูรณ์ (Complete Source Codes):**
  * โค้ด C (Pthreads) Matrix Multiplication พร้อม Memory Alignment ป้องกัน False Sharing
  * โค้ด C แสดงการใช้ GCC Atomics (`__atomic_compare_exchange`) สำหรับ Lock-Free Stack
  * โค้ด Python เปรียบเทียบ CPython Standard vs Free-threaded (Python 3.13 PEP 703)
  * โค้ด Java เปรียบเทียบ Platform Threads vs Virtual Threads
* **ภาคผนวก ข: ตารางข้อมูลดิบจากการทดลองและสถิติ (Raw Benchmark Datasets & Statistics):**
  * ผลลัพธ์เวลาการทำงานของทุกรอบการทดสอบ ($N=10$ รอบ) พร้อมค่า Mean, SD, Variance และ 95% Confidence Intervals
  * บันทึกผลลัพธ์ฮาร์ดแวร์เคาน์เตอร์จริงจากคำสั่ง `perf stat`
* **ภาคผนวก ค: รายละเอียดสเปกเครื่องและการตั้งค่าระบบ (System Profile Outputs):**
  * ผลลัพธ์คำสั่งตรวจสอบระบบ (`lscpu`, `uname -a`, `cat /proc/cpuinfo`, `numactl --hardware`, `gcc --version`)

---

## 🛠️ แนวทางเชิงปฏิบัติการในการเขียนรายงานตามมาตรฐานวิชาการ:
1. **การตั้งสมมติฐานและการพิสูจน์ (Hypothesis-Driven Writing):** ในทุกบทต้องมีคำถามนำและคำตอบเชิงวิเคราะห์ เช่น ทำไมการทดลองจริงจึงเบี่ยงเบนจาก Amdahl's Law หรือทำไมระบบจึงเกิด Inflection Point เมื่อเธรดเกินจำนวนคอร์
2. **การวาดภาพและไดอะแกรมระดับสถาปัตยกรรม:** วาดไดอะแกรมที่มีรายละเอียดทางเทคนิคสูง เช่น แผนผังโครงสร้าง Virtual Address Space, แผนภาพ State Diagram, ไดอะแกรม Cache Line 64 Bytes พร้อมสถานะ MESI, และแผนผังการไหลของข้อมูลใน Linux Futex
3. **การนำเสนอกราฟด้วยมาตรฐานเปเปอร์วิชาการ:** มีชื่อแกน หน่วยวัดที่ชัดเจน พร้อมพล็อต Error Bar (95% CI) กำกับทุกจุดข้อมูล และมีการเขียนวิเคราะห์แนวโน้มใต้กราฟอย่างละเอียด
4. **ความประณีตในการจัดทำเล่ม:**
   * **กรณีเขียนลายมือ (เป้าหมาย 25/25):** ใช้ปากกาสองสีอย่างเป็นระบบ (สีน้ำเงินสำหรับเนื้อหา สีดำสำหรับโค้ด/สูตร สีแดงสำหรับหัวข้อ/จุดเน้น), ตีเส้นตารางและวาดกรอบด้วยไม้บรรทัดอย่างประณีต, เว้นขอบซ้าย 1.5 นิ้ว ขวา 1 นิ้วอย่างสม่ำเสมอ
   * **กรณีพิมพ์คอมพิวเตอร์ (เป้าหมาย 18/25):** จัดหน้าแบบสองคอลัมน์ (Two-Column Format) สไตล์ IEEE Transactions หรือ ACM Journal พร้อมกำหนดฟอนต์และขนาดตัวอักษรที่เป็นระเบียบ มีการอ้างอิงรูปภาพและตารางในเนื้อหาทุกจุด (Cross-referencing)
