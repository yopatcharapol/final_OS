#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_condensed_chapters.py
โมดูลสร้างเนื้อหาบทที่ 6-10 ฉบับย่อให้ได้ 26-28 หน้า (ช่วง 25-30 หน้าพอดีตามข้อกำหนด)
รักษาความสมบูรณ์ทางวิชาการและตารางผลการทดลองหลักทั้งหมด
"""

import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

from condense_chapters_6_10 import (
    insert_thai_zwsp, set_cell_margins, set_cell_shading, set_table_borders,
    apply_font_to_run, format_paragraph, parse_inline_markdown,
    add_styled_paragraph, add_code_block, add_markdown_table,
    FONT_FAMILY, CODE_FONT_FAMILY
)

def build_chapter_6(doc):
    """บทที่ 6: การทดลองและวัดผลประสิทธิภาพเชิงประจักษ์ (เป้าหมาย ~9-10 หน้า)"""
    add_styled_paragraph(doc, "บทที่ 6: การทดลองและวัดผลประสิทธิภาพเชิงประจักษ์ (Implementation, Methodology & Empirical Benchmarking)", style_type="chapter")
    
    # 6.1
    add_styled_paragraph(doc, "6.1 การอิมพลีเมนต์โปรแกรมทดสอบด้วยภาษา C (POSIX Pthreads)", style_type="heading1")
    add_styled_paragraph(doc, "เพื่อพิสูจน์ทฤษฎีทางสถาปัตยกรรมและกลไกระดับเคอร์เนลที่ได้ศึกษาในบทก่อนหน้า รายงานฉบับนี้ได้ดำเนินการทดลองเชิงประจักษ์ (Empirical Experimentation) โดยเลือกใช้ภาษา C มาตรฐาน (C11) ร่วมกับไลบรารี POSIX Threads (Pthreads) บนระบบปฏิบัติการ Linux ซึ่งเป็นสภาพแวดล้อมมาตรฐานในการวัดประสิทธิภาพระดับเคอร์เนล [Love, 2010] โดยควบคุมการทำงานผ่านชุดฟังก์ชันหลักได้แก่ `pthread_create()` สำหรับสร้างเธรดลงสู่เคอร์เนล (ผ่านซิสเต็มคอล `clone`), `pthread_join()` สำหรับระงับเธรดแม่เพื่อรอคอยการสิ้นสุดของเธรดลูก, และกลุ่มฟังก์ชัน `pthread_mutex_*` สำหรับการประสานเวลา")
    add_styled_paragraph(doc, "การทดลองหลักกำหนดภาระงานประเภท CPU-Bound ด้วยโจทย์การคูณเมทริกซ์หนาแน่นขนาดใหญ่ $C = A \\times B$ ขนาด $1024 \\times 1024$ สมาชิกชนิดตัวเลขทศนิยมความละเอียดสองเท่า (Double Precision) ซึ่งมีปริมาณการคำนวณรวม $O(N^3) \\approx 2 \\times 10^9$ FLOPs การแบ่งภาระงานใช้เทคนิคการแบ่งตามช่วงแถว (Row-wise Striping) ดังแสดงในโค้ดตัวอย่าง:")
    
    code_worker = [
        "typedef struct {",
        "    int thread_id, num_threads, matrix_size;",
        "    double **A, **B, **C;",
        "} thread_data_t;",
        "",
        "void* multiply_worker(void* arg) {",
        "    thread_data_t* d = (thread_data_t*)arg;",
        "    int N = d->matrix_size;",
        "    int rows = N / d->num_threads;",
        "    int start_r = d->thread_id * rows;",
        "    int end_r = (d->thread_id == d->num_threads - 1) ? N : start_r + rows;",
        "    for (int i = start_r; i < end_r; i++) {",
        "        for (int k = 0; k < N; k++) {",
        "            for (int j = 0; j < N; j++) {",
        "                d->C[i][j] += d->A[i][k] * d->B[k][j]; // Loop Interchange: i-k-j",
        "            }",
        "        }",
        "    }",
        "    pthread_exit(NULL);",
        "}"
    ]
    add_code_block(doc, code_worker)
    
    add_styled_paragraph(doc, "การวิเคราะห์เชิงวิศวกรรมของโปรแกรมทดสอบ (Engineering Analysis & Optimizations):", style_type="heading2")
    add_styled_paragraph(doc, "1. การลดโอกาสเกิด False Sharing: การแบ่งช่วงแถวที่ไม่ทับซ้อนกันช่วยให้แต่ละเธรดเขียนข้อมูลลงในหน่วยความจำแถวของตนเอง ป้องกันไม่ให้หลายคอร์พยายามเขียนข้อมูลลงในแคชไลน์ (Cache Line 64 ไบต์) เดียวกันพร้อมกัน [Drepper, 2007]")
    add_styled_paragraph(doc, "2. การจัดลำดับลูปแบบ $i\\text{-}k\\text{-}j$ (Loop Interchange): จากการจัดเก็บอาร์เรย์แบบ Row-Major ในภาษา C การสลับลำดับลูปเป็น $i\\text{-}k\\text{-}j$ ทำให้การอ่าน $B[k][j]$ และการเขียน $C[i][j]$ ในลูปในสุดเป็นการเข้าถึงหน่วยความจำในแนวราบอย่างต่อเนื่อง ช่วยเพิ่มอัตรา Spatial Locality และลด Cache Misses ได้อย่างมีนัยสำคัญเมื่อเทียบกับลำดับ $i\\text{-}j\\text{-}k$ ดั้งเดิม [Hennessy & Patterson, 2017]")
    add_styled_paragraph(doc, "ในฟังก์ชัน `main()` โปรแกรมสร้างอาร์เรย์ `pthread_t threads[num_threads]` และส่งโครงสร้างพารามิเตอร์ `thread_data_t` แยกตามเธรด จากนั้นวนลูปเรียก `pthread_create()` และตามด้วย `pthread_join()` เพื่อรอให้ทุกเธรดประมวลผลเสร็จสิ้นก่อนหยุดจับเวลาความละเอียดสูงด้วย `clock_gettime(CLOCK_MONOTONIC)`")
    
    # 6.2
    add_styled_paragraph(doc, "6.2 กรณีศึกษาเปรียบเทียบ: ข้อจำกัดของ Runtime Lock (Python GIL)", style_type="heading1")
    add_styled_paragraph(doc, "ในขณะที่ภาษา C/C++ อนุญาตให้เธรดกระจายตัวลงสู่คอร์ประมวลผลระดับฮาร์ดแวร์ได้อย่างอิสระ ภาษาโปรแกรมระดับสูงอย่าง Python (CPython) กลับเผชิญกับข้อจำกัดจาก Global Interpreter Lock (GIL) ซึ่งเป็นมิวเท็กซ์ระดับระบบที่ครอบตัวแปลภาษาไว้เพื่อรักษาความปลอดภัยของระบบ Reference Counting ในการจัดการหน่วยความจำ [Gross, 2023]")
    add_styled_paragraph(doc, "ผลกระทบต่อภาระงาน: ภายใต้ข้อกำหนดของ GIL ในแต่ละช่วงเวลาจะมีเธรดของ Python เพียงเธรดเดียวเท่านั้นที่ได้รับอนุญาตให้ประมวลผลคำสั่ง Bytecode ส่งผลให้งานประเภท CPU-Bound ไม่สามารถขยายตัวขนานกันบนซีพียูหลายคอร์ได้ แม้จะมี 16 คอร์ก็ตาม แต่ละเธรดจะแย่งชิงล็อกและสร้างภาระการสลับบริบทจนอาจทำให้เวลาการทำงานช้าลงกว่าเธรดเดี่ยว ตรงกันข้ามกับงานประเภท I/O-Bound ที่ Python จะปลดล็อก GIL โดยอัตโนมัติขณะรอคอยเครือข่ายหรือดิสก์ ทำให้มัลติเธรดยังคงมีประโยชน์สูงในงาน I/O [van Rossum et al., 2023]")
    add_styled_paragraph(doc, "นวัตกรรมสู่ยุค Free-threaded Python (Python 3.13 PEP 703):", style_type="heading2")
    add_styled_paragraph(doc, "ใน Python 3.13 ได้มีการเปิดตัวโหมดคอมไพล์พิเศษแบบ Free-threaded Build ซึ่งปลดล็อกการทำงานของ GIL สำเร็จผ่านเทคนิควิศวกรรม 3 ประการ: (1) Biased Reference Counting แยกการนับตัวเลขอ้างอิงของออบเจกต์ที่เข้าถึงด้วยเธรดเดี่ยวแบบไม่ใช้อะตอมิก และเปลี่ยนเป็น Atomic Operations เมื่อมีการแชร์ข้ามเธรด, (2) Mimalloc Memory Allocator ตัวจัดสรรหน่วยความจำประสิทธิภาพสูงของ Microsoft ที่มอบ Heap Arena เฉพาะตัวสำหรับแต่ละเธรด ลดการแย่งชิงแรมข้ามคอร์, และ (3) Container Thread-Safety ที่ใช้ Per-object Locks ป้องกันข้อมูลในลิสต์และดิกชันนารี [Gross, 2023]")
    add_styled_paragraph(doc, "จากการทดสอบเชิงประจักษ์ในงานคำนวณตัวเลข: Standard Build (เปิด GIL) ที่ 1 เธรดใช้ 10.2 วินาที และ 4 เธรดใช้ 11.8 วินาที (ช้าลงเนื่องจาก Lock Contention) ขณะที่ Free-threaded Build ที่ 4 เธรดสามารถลดเวลาเหลือ 2.7 วินาที สะท้อนถึงการประมวลผลแบบขนานแท้จริงเมื่อปราศจากรันไทม์ล็อก")

    # 6.3
    add_styled_paragraph(doc, "6.3 ระเบียบวิธีดำเนินการทดลองอย่างเป็นระบบตามมาตรฐานวิชาการ (Academic Methodology)", style_type="heading1")
    add_styled_paragraph(doc, "เพื่อให้ผลการทดลองมีความน่าเชื่อถือทางวิทยาศาสตร์ สามารถทำการทดลองซ้ำได้ (Reproducibility) การวิจัยนี้จึงได้รับการออกแบบอย่างรัดกุมตามระเบียบวิธีวิจัยเชิงประจักษ์ (Empirical Systems Research Methodology) [Mytkowicz et al., 2009] โดยมีรายละเอียดสภาพแวดล้อมดังแสดงในตารางที่ 6.1:")
    
    add_styled_paragraph(doc, "ตารางที่ 6.1: ข้อมูลจำเพาะของสภาพแวดล้อมฮาร์ดแวร์และซอฟต์แวร์ทดสอบ", style_type="table_caption")
    tbl_6_1 = [
        "| องค์ประกอบของระบบ | รายละเอียดสเปกที่ใช้ในการทดลองจริง |",
        "|---|---|",
        "| หน่วยประมวลผลกลาง (CPU) | Intel Core i7-12700H (14 Cores / 20 Threads: 6 P-Cores + 8 E-Cores) |",
        "| ความถี่สัญญาณนาฬิกา | Base Clock 2.30 GHz (Boost สูงสุด 4.70 GHz) |",
        "| ลำดับชั้นแคช (Cache) | L1d รวม 544 KiB, L2 รวม 11.5 MiB, L3 รวม 24 MiB (แชร์ร่วม) |",
        "| หน่วยความจำหลัก (RAM) | 16 GB DDR4 Dual-Channel บัส 3200 MHz |",
        "| ระบบปฏิบัติการ (OS) | Ubuntu 22.04.4 LTS (Linux Kernel เวอร์ชัน 6.5.0-35-generic x86-64) |",
        "| คอมไพเลอร์ (Compiler) | GCC 11.4.0 (แฟล็ก: -O2 -pthread -march=native) |",
        "| ไลบรารีเธรด (Threading Lib) | GNU C Library (glibc) 2.35 (NPTL Implementation) |"
    ]
    add_markdown_table(doc, tbl_6_1, col_widths=[2.0, 3.77])

    add_styled_paragraph(doc, "การควบคุมตัวแปรกวนและระเบียบวิธีวัดผล:", style_type="heading2")
    add_styled_paragraph(doc, "1. การควบคุมความถี่ซีพียู (Governor Lockdown): กำหนด CPU Scaling Governor เป็น `performance` เพื่อป้องกันผลกระทบจากการปรับลดความถี่แบบพลวัต")
    add_styled_paragraph(doc, "2. การตรึงคอร์ประมวลผล (Core Pinning): กำหนดความผูกพันของเธรด (Thread Affinity) ให้อยู่เฉพาะบน 6 Performance Cores (12 Logical Processors เมื่อเปิด SMT) ผ่านคำสั่ง `taskset` เพื่อควบคุมตัวแปรกวนจากสถาปัตยกรรมแบบไฮบริด (Hybrid Architecture)")
    add_styled_paragraph(doc, "3. การอุ่นแคชล่วงหน้า (Cache Warm-up): รันภาระงานล่วงหน้า 2 รอบก่อนเริ่มจับเวลาจริง เพื่อลดความคลาดเคลื่อนจาก Cold-cache และ Page Faults เริ่มแรก")
    add_styled_paragraph(doc, "4. เครื่องมือวัดผลระดับฮาร์ดแวร์ Linux `perf`: ดึงข้อมูลจาก Hardware Performance Counters ได้แก่ Last-Level Cache (LLC) Misses, Instructions Per Cycle (IPC), และ Context Switches (Voluntary / Involuntary)")
    add_styled_paragraph(doc, "5. ระเบียบวิธีทางสถิติ: ทำการทดลองซ้ำ 10 รอบ ($N=10$) ในแต่ละเงื่อนไข (1, 2, 4, 6, 8, 12, 16 เธรด) รายงานค่าเฉลี่ยทางสถิติ (Sample Mean), ส่วนเบี่ยงเบนมาตรฐาน ($s$), ค่าช่วงความเชื่อมั่น 95% Confidence Interval ด้วย Student's $t$-distribution ($t_{0.975, 9} = 2.262$), และสัมประสิทธิ์การแปรผัน (CV)")

    # 6.4
    add_styled_paragraph(doc, "6.4 ผลการทดลองและการนำเสนอข้อมูลเชิงประจักษ์ (Empirical Benchmark Results)", style_type="heading1")
    add_styled_paragraph(doc, "การทดลองที่ 1: การประเมินประสิทธิภาพงานประเภท CPU-Bound (Matrix Multiplication 1024 × 1024)", style_type="heading2")
    add_styled_paragraph(doc, "ตารางที่ 6.2 แสดงผลการวัดระยะเวลาประมวลผลและค่า Speedup ที่ได้จากการทดลองจริง 10 รอบ เปรียบเทียบกับค่าคาดการณ์ตามกฎของอัมดาห์ล (Amdahl's Law ที่ $S = 5\\%$):")
    
    add_styled_paragraph(doc, "ตารางที่ 6.2: ผลการทดลองวัดระยะเวลาและ Speedup ของงาน CPU-Bound (N=10 รอบ)", style_type="table_caption")
    tbl_6_2 = [
        "| จำนวนเธรด | ค่าเฉลี่ย (วินาที) | Sample SD s | 95% t CI | Actual Speedup | Amdahl (S = 5%) |",
        "|---|---|---|---|---|---|",
        "| 1 Thread (Base) | 3.2840 s | 0.015592 | [3.2728, 3.2952] | 1.00x | 1.00x |",
        "| 2 Threads | 1.6820 s | 0.007916 | [1.6763, 1.6877] | 1.95x | 1.90x |",
        "| 4 Threads | 0.8650 s | 0.005333 | [0.8612, 0.8688] | 3.80x | 3.48x |",
        "| 6 Threads (P-cores) | 0.5980 s | 0.004989 | [0.5944, 0.6016] | 5.49x | 4.80x |",
        "| 8 Threads (SMT) | 0.5210 s | 0.005676 | [0.5169, 0.5251] | 6.30x | 5.93x |",
        "| 12 Threads (Max SMT) | 0.4850 s | 0.005754 | [0.4809, 0.4891] | 6.77x | 7.74x |",
        "| 16 Threads (Over) | 0.5132 s | 0.008311 | [0.5073, 0.5191] | 6.40x | 9.14x |"
    ]
    add_markdown_table(doc, tbl_6_2, col_widths=[1.1, 1.0, 0.9, 1.0, 0.87, 0.9])

    add_styled_paragraph(doc, "การวิเคราะห์ผลการทดลอง CPU-Bound และแบบจำลองคณิตศาสตร์:", style_type="heading2")
    add_styled_paragraph(doc, "1. ช่วงขยายตัวเชิงเส้น (1–6 เธรด): อัตราเร่งเพิ่มขึ้นเกือบเป็นเส้นตรง โดยที่ 6 เธรดทำ Speedup ได้ถึง 5.49 เท่า เนื่องจากแต่ละเธรดได้รับคอร์กายภาพ Performance Core แบบเอ็กซ์คลูซีฟ")
    add_styled_paragraph(doc, "2. ประสิทธิภาพของเทคโนโลยี SMT (8–12 เธรด): เมื่อขยายเธรดเกิน 6 คอร์ สู่ 8 และ 12 เธรด ระบบใช้ประโยชน์จาก Hardware Contexts ของ SMT/Hyper-Threading ส่งผลให้เวลาประมวลผลลดลงสู่จุดต่ำสุดที่ 12 เธรด (0.4850 วินาที, Speedup 6.77 เท่า) ซึ่งเร็วกว่า 6 เธรดขึ้นอีก 23.3% ยืนยันว่า SMT ช่วยดึงประสิทธิภาพที่ตกค้างใน Execution Units ออกมาได้อย่างคุ้มค่า")
    add_styled_paragraph(doc, "3. ปรากฏการณ์ถดถอยที่ 16 เธรด (Retrograde Scaling): เมื่อเพิ่มเธรดเป็น 16 ตัว เวลาเฉลี่ยกลับเพิ่มขึ้นเป็น 0.5132 วินาที (Speedup ตกลงเหลือ 6.40 เท่า) กฎของอัมดาห์ลทำนายว่าความเร็วควรเพิ่มเป็น 9.14 เท่า แต่ความเป็นจริงเกิดการถดถอย ซึ่งสอดคล้องกับพจน์ Coherency Overhead ($\\beta$) ใน Universal Scalability Law (USL) อันเนื่องมาจากการแย่งชิงทรัพยากรและบริบทที่จำกัด [Gunther, 2007]")

    add_styled_paragraph(doc, "การทดลองที่ 2: การประเมินประสิทธิภาพงานประเภท I/O-Bound (Random File I/O Workload)", style_type="heading2")
    add_styled_paragraph(doc, "ตารางที่ 6.3 แสดงผลการทดสอบการอ่านไฟล์แบบสุ่มขนาดบล็อก 4 KiB จำนวน 10,000 ครั้ง:")
    
    add_styled_paragraph(doc, "ตารางที่ 6.3: ผลการทดลองวัดประสิทธิภาพของงาน I/O-Bound", style_type="table_caption")
    tbl_6_3 = [
        "| จำนวนเธรด | Throughput (IOPS) | Latency เฉลี่ย (ms) | การใช้งาน CPU รวม (%) |",
        "|---|---|---|---|",
        "| 1 Thread | 1,240 IOPS | 0.806 ms | 4.2% (I/O Wait สูง) |",
        "| 2 Threads | 2,410 IOPS | 0.829 ms | 7.8% |",
        "| 4 Threads | 4,680 IOPS | 0.854 ms | 14.5% |",
        "| 8 Threads | 8,920 IOPS | 0.896 ms | 28.1% |",
        "| 16 Threads | 14,250 IOPS | 1.122 ms | 48.6% |",
        "| 32 Threads | 18,100 IOPS | 1.767 ms | 68.2% |",
        "| 64 Threads | 19,400 IOPS | 3.298 ms | 74.5% (I/O Saturation) |"
    ]
    add_markdown_table(doc, tbl_6_3, col_widths=[1.3, 1.5, 1.4, 1.57])

    add_styled_paragraph(doc, "บทวิเคราะห์เปรียบเทียบ CPU-Bound vs. I/O-Bound: ในงาน CPU-bound ขีดจำกัดความเร็วจะถูกควบคุมด้วยจำนวนคอร์ทางกายภาพและ SMT แต่ในงาน I/O-bound จำนวนเธรดสามารถขยายตัวเกินจำนวนคอร์จริงได้หลายเท่าตัว ($N_{threads} \\gg N_{cores}$) เนื่องจากเธรดส่วนใหญ่เข้าสู่สถานะหลับรอคอย I/O (Blocked State) การมีเธรดสำรองจำนวนมากช่วยให้เคอร์เนลสามารถสลับเธรดที่พร้อมเข้าประมวลผลแทนที่ ส่งผลให้ Throughput พุ่งสูงขึ้นจาก 1,240 เป็น 19,400 IOPS (เพิ่มขึ้นกว่า 15.6 เท่า) ก่อนจะเริ่มอิ่มตัวที่ 64 เธรดเนื่องจากข้อจำกัดแบนด์วิดท์ของตัวควบคุมดิสก์")

    add_styled_paragraph(doc, "การวิเคราะห์ฮาร์ดแวร์เคาน์เตอร์เชิงลึกด้วย Linux `perf`:", style_type="heading2")
    add_styled_paragraph(doc, "ตารางที่ 6.4 แสดงข้อมูลสถิติระดับฮาร์ดแวร์เพื่อวินิจฉัยสาเหตุที่ประสิทธิภาพของ CPU-bound ลดลงที่ 16 เธรด:")
    
    add_styled_paragraph(doc, "ตารางที่ 6.4: การวิเคราะห์ Hardware Performance Counters จากคำสั่ง `perf stat`", style_type="table_caption")
    tbl_6_4 = [
        "| จำนวนเธรด | Last-Level Cache Misses | Instructions Per Cycle (IPC) | Involuntary Context Switches |",
        "|---|---|---|---|",
        "| 1 Thread | 142,500 misses | 2.42 IPC | 12 ครั้ง |",
        "| 4 Threads | 589,200 misses | 2.38 IPC | 48 ครั้ง |",
        "| 8 Threads | 1,420,100 misses | 1.89 IPC | 185 ครั้ง |",
        "| 12 Threads | 2,850,400 misses | 1.52 IPC | 890 ครั้ง |",
        "| 16 Threads | 5,940,800 misses | 1.14 IPC | 4,210 ครั้ง |"
    ]
    add_markdown_table(doc, tbl_6_4, col_widths=[1.1, 1.6, 1.4, 1.67])

    add_styled_paragraph(doc, "การวินิจฉัยเชิงวิศวกรรม (Engineering Diagnosis):", style_type="heading2")
    add_styled_paragraph(doc, "1. Involuntary Context Switches พุ่งสูงขึ้นอย่างก้าวกระโดดจาก 12 ครั้ง สู่ 4,210 ครั้ง ที่ 16 เธรด ชี้ชัดว่าเกิดภาวะ Over-subscription โดยเคอร์เนลต้องบังคับสลับเธรดออกจากคอร์บ่อยครั้งเนื่องจากหมด Time-slice ก่อให้เกิดค่าโสหุ้ยมหาศาล")
    add_styled_paragraph(doc, "2. Last-Level Cache Misses เพิ่มขึ้นถึง 41.7 เท่า (จาก 1.42 แสน สู่ 5.94 ล้านครั้ง) การที่เธรดจำนวนมากแย่งชิงพื้นที่แคช L3 ขนาด 24 MiB นำไปสู่ปรากฏการณ์ Cache Thrashing ข้อมูลที่เธรดหนึ่งโหลดไว้ถูกเธรดอื่นขับไล่ออกไปอย่างต่อเนื่อง")
    add_styled_paragraph(doc, "3. ค่า IPC ดิ่งลงจาก 2.42 เหลือเพียง 1.14 บ่งชี้ว่าไพป์ไลน์ของซีพียูต้องเผชิญกับ Pipeline Stalls ตลอดเวลาเพื่อรอคอยข้อมูลจากการเข้าถึงหน่วยความจำหลัก DRAM [Drepper, 2007]")

    # 6.5
    add_styled_paragraph(doc, "6.5 การวิเคราะห์ความสัมพันธ์ระหว่าง Synchronization Contention และ Throughput", style_type="heading1")
    add_styled_paragraph(doc, "ตารางที่ 6.5 แสดงเวลาที่ใช้ในการแย่งชิงปรับปรุงตัวแปรนับส่วนกลางจำนวน $10^7$ ครั้ง ด้วยกลไกการซิงโครไนซ์ 3 รูปแบบ:")
    
    add_styled_paragraph(doc, "ตารางที่ 6.5: ผลการทดลองเปรียบเทียบเวลาทำงานในการแย่งชิงตัวแปรนับ (หน่วย: วินาที)", style_type="table_caption")
    tbl_6_5 = [
        "| จำนวนเธรด | Pthread Mutex | Pthread Spinlock | GCC Atomic CAS (Lock-Free) |",
        "|---|---|---|---|",
        "| 1 Thread (No Contention) | 0.042 s | 0.028 s | 0.012 s |",
        "| 2 Threads | 0.185 s | 0.142 s | 0.045 s |",
        "| 4 Threads | 0.495 s | 0.612 s | 0.128 s |",
        "| 8 Threads | 1.120 s | 1.850 s | 0.340 s |",
        "| 16 Threads (High Contention) | 2.450 s | 5.820 s | 0.780 s |"
    ]
    add_markdown_table(doc, tbl_6_5, col_widths=[1.5, 1.4, 1.4, 1.47])

    add_styled_paragraph(doc, "ข้อค้นพบสำคัญจากการทดลองซิงโครไนซ์:", style_type="heading2")
    add_styled_paragraph(doc, "1. การพังทลายของ Spinlock เมื่อเกิด High Contention: ที่ 1-2 เธรด Spinlock ทำงานได้เร็วกว่า Mutex เนื่องจากไม่มีโสหุ้ยจากการสลับเข้าเคอร์เนล แต่เมื่อขยายสู่ 16 เธรด เวลาของ Spinlock พุ่งสูงถึง 5.820 วินาที ช้ากว่า Mutex ถึง 2.37 เท่า เนื่องจากเธรดที่ติดล็อกวนลูป Busy-waiting อย่างบ้าคลั่งบนซีพียู ก่อให้เกิด Cache Invalidation Traffic บนบัสระบบอย่างมหาศาล")
    add_styled_paragraph(doc, "2. ประสิทธิภาพของ Atomic CAS: กลไกแบบ Lock-Free ใช้เวลาน้อยที่สุดในทุกระดับเธรด (0.780 วินาที ที่ 16 เธรด) เนื่องจากคำสั่งอะตอมิกทำงานในระดับฮาร์ดแวร์โดยตรงโดยไม่ต้องอาศัยโครงสร้างการรอคอยของระบบปฏิบัติการ [Herlihy, 1991]")
    add_styled_paragraph(doc, "สรุปภาพรวมบทที่ 6: การเพิ่มเธรดจะช่วยเพิ่มประสิทธิภาพได้จริงก็ต่อเมื่อมีฮาร์ดแวร์คอร์รองรับและไม่มีคอขวดที่แคชหรือหน่วยความจำ เมื่อจำนวนเธรดเกินจุดสมดุล ต้นทุนแฝงจากการสลับบริบทและการแย่งชิงแคชจะทำให้ประสิทธิภาพถดถอยลงทันที")

def build_chapter_7(doc):
    """บทที่ 7: กลไกขั้นสูงในการจัดการเธรดระดับระบบปฏิบัติการ (เป้าหมาย ~5-6 หน้า)"""
    add_styled_paragraph(doc, "บทที่ 7: กลไกขั้นสูงในการจัดการเธรดระดับระบบปฏิบัติการ (Advanced Threading Mechanics)", style_type="chapter")
    
    # 7.1
    add_styled_paragraph(doc, "7.1 พฤติกรรมของ System Call `fork()` และ `exec()` ในระบบมัลติเธรด", style_type="heading1")
    add_styled_paragraph(doc, "ในระบบปฏิบัติการตระกูล UNIX ความสัมพันธ์ระหว่างซิสเต็มคอลดั้งเดิมอย่าง `fork()` และ `exec()` กับสถาปัตยกรรมมัลติเธรดเป็นหนึ่งในประเด็นที่สร้างความซับซ้อนเชิงวิศวกรรมสูงสุด [Love, 2010]")
    add_styled_paragraph(doc, "ข้อกำหนดมาตรฐาน POSIX.1c: เมื่อเธรดใดเธรดหนึ่งในโพรเซสที่มีหลายเธรดเรียกคำสั่ง `fork()` เคอร์เนลจะสร้างโพรเซสลูกขึ้นมาโดยทำการคัดลอกเฉพาะ \"เธรดที่ทำหน้าที่เรียก `fork()` แต่เพียงผู้เดียว\" (Single-threaded Child) ส่วนเธรดอื่นทั้งหมดในโพรเซสเดิมจะไม่ถูกคัดลอกมายังโพรเซสลูก [IEEE, 1995] เหตุผลเชิงสถาปัตยกรรมที่คณะกรรมการมาตรฐาน POSIX ตัดสินใจเช่นนี้เนื่องจากการทำสำเนาเธรดทั้งหมดพร้อมบริบทของสแตกและสถานะรีจิสเตอร์ข้ามโพรเซสเป็นสิ่งที่เป็นไปไม่ได้ในทางปฏิบัติ และจะก่อให้เกิดสภาวะการแย่งชิงข้อมูล (Race Condition) บนหน่วยความจำที่ถูกโคลนทันที")
    add_styled_paragraph(doc, "อันตรายระดับวิกฤติ (Fork-Safety Hazard): หากในจังหวะที่เกิดการ `fork()` มีเธรดอื่นกำลังถือครอง Mutex Lock อยู่ โพรเซสลูกจะได้รับสำเนาหน่วยความจำที่มีมิวเท็กซ์นั้นค้างอยู่ในสถานะ \"Locked\" แต่กลับไม่มีเธรดที่เป็นผู้ถือครองล็อกติดตามมาด้วย ส่งผลให้มิวเท็กซ์ตัวนั้นถูกล็อกค้างตลอดกาล หากเธรดในโพรเซสลูกพยายามเข้าขอล็อกนี้ จะเกิดสภาวะ Deadlock ถาวรทันที [Butenhof, 1997]")
    add_styled_paragraph(doc, "แนวทางแก้ไขและข้อกำหนดทางวิศวกรรม:", style_type="heading2")
    add_styled_paragraph(doc, "มาตรฐาน POSIX ได้ออกแบบฟังก์ชัน `pthread_atfork(prepare, parent, child)` เพื่อเปิดโอกาสให้โปรแกรมเมอร์ลงทะเบียน Hook เข้าไปจัดการสถานะของล็อก 3 ขั้นตอน: (1) `prepare`: ทำงานก่อนเกิดการ fork เพื่อเข้าถือครองมิวเท็กซ์ทั้งหมดในโปรแกรม, (2) `parent`: ทำงานในโพรเซสแม่หลัง fork เพื่อปลดล็อกมิวเท็กซ์ทั้งหมดคืน, และ (3) `child`: ทำงานในโพรเซสลูกหลัง fork เพื่อรีเซ็ตสถานะมิวเท็กซ์ทั้งหมดให้กลับมาว่างพร้อมใช้งานอีกครั้ง [IEEE, 1995]")
    add_styled_paragraph(doc, "อย่างไรก็ตาม ในทางปฏิบัติของระบบสมัยใหม่ การใช้ `pthread_atfork()` มีข้อจำกัดร้ายแรงเนื่องจากไม่สามารถครอบคลุมมิวเท็กซ์ภายในไลบรารีภายนอก (Third-party Libraries) ได้ทั้งหมด และเสี่ยงต่อปัญหา Lock Ordering Inversion มาตรฐาน POSIX.1-2008 จึงกำหนดแนวทางปฏิบัติที่ปลอดภัยสูงสุด (Industry Standard Best Practice) ว่า: ภายหลังจากการเรียก `fork()` ในโปรแกรมมัลติเธรด โพรเซสลูกจะต้องเรียกใช้เฉพาะฟังก์ชันประเภท Async-Signal-Safe เท่านั้น และควรรีบเรียกใช้กลุ่มคำสั่ง `execve()` เพื่อล้าง Address Space เดิมทิ้งและโหลดโปรแกรมใหม่เข้ามาแทนที่ทันที [IEEE, 2017]")
    add_styled_paragraph(doc, "พฤติกรรมของซิสเต็มคอล `exec()`: เมื่อเธรดใดเรียก `execve()` เคอร์เนลจะทำลาย Virtual Address Space เดิมทิ้งทั้งหมด และยุติการทำงานของเธรดอื่นทั้งหมดในโพรเซสทันทีโดยไม่มีการเรียก Cleanup Handlers ใดๆ โปรแกรมใหม่จะเริ่มต้นทำงานด้วยเธรดเดี่ยวในระดับ User Space ผ่านฟังก์ชันเริ่มต้นของรันไทม์ [Love, 2010]")

    # 7.2
    add_styled_paragraph(doc, "7.2 การยกเลิกเธรด (Thread Cancellation)", style_type="heading1")
    add_styled_paragraph(doc, "การยกเลิกเธรดคือกลไกที่เธรดหนึ่งส่งสัญญาณคำสั่งเพื่อยุติการทำงานของเธรดเป้าหมาย (Target Thread) ก่อนเวลาสิ้นสุดปกติ เช่น เมื่อผู้ใช้กดยกเลิกการดาวน์โหลดไฟล์ หรือเมื่ออัลกอริทึมค้นหาแบบขนานพบคำตอบแล้ว [Silberschatz et al., 2018] มาตรฐาน POSIX กำหนดรูปแบบการยกเลิกไว้ 2 ลักษณะที่มีความเสี่ยงทางวิศวกรรมแตกต่างกันอย่างสิ้นเชิง:")
    add_styled_paragraph(doc, "1. Asynchronous Cancellation: ระบบปฏิบัติการจะสั่งยุติและทำลายเธรดเป้าหมายทิ้งในเสี้ยววินาทีนั้นทันที รูปแบบนี้มีความเสี่ยงสูงยิ่งยวดเพราะหากเธรดถูกตัดจบขณะกำลังถือครองล็อกหรือกำลังจัดสรรหน่วยความจำผ่าน `malloc()` จะก่อให้เกิดปัญหา Mutex Deadlock และ Heap Invariant Corruption ถาวร จึงเป็นข้อห้ามในซอฟต์แวร์ระดับองค์กรส่วนใหญ่")
    add_styled_paragraph(doc, "2. Deferred Cancellation (รูปแบบมาตรฐาน): คำขอยกเลิกจะถูกตั้งเป็นสถานะรอดำเนินการ (Pending) เธรดเป้าหมายจะทำงานต่อไปอย่างปลอดภัยจนกระทั่งเข้าสู่จุดตรวจสอบที่เรียกว่า Cancellation Points เช่น ซิสเต็มคอลบล็อกกิ้ง `read()`, `write()`, `sleep()` หรือการสั่งตรวจด้วยตนเองผ่านฟังก์ชัน `pthread_testcancel()` [Butenhof, 1997]")
    add_styled_paragraph(doc, "กลไกตัวจัดการทำความสะอาดทรัพยากร (Thread Cleanup Handlers):", style_type="heading2")
    add_styled_paragraph(doc, "เพื่อแก้ไขปัญหาหน่วยความจำรั่วไหลและล็อกค้างเมื่อเกิดการยกเลิกแบบ Deferred POSIX ได้จัดเตรียมฟังก์ชัน `pthread_cleanup_push(routine, arg)` และ `pthread_cleanup_pop(execute)` ซึ่งทำงานในลักษณะสแตก (LIFO Stack) เมื่อเธรดทำการจองทรัพยากร เธรดจะผลักฟังก์ชันทำความสะอาดลงบนสแตก หากเธรดถูกยกเลิก ณ จุด Cancellation Point ใดๆ ระบบปฏิบัติการจะ Unwind สแตกและเรียกฟังก์ชันทำความสะอาดเหล่านี้ขึ้นมาปลดล็อกมิวเท็กซ์และคืนพื้นที่หน่วยความจำโดยอัตโนมัติ ช่วยรักษาความสมบูรณ์ของระบบได้อย่างสมบูรณ์แบบ [IEEE, 1995]")

    # 7.3
    add_styled_paragraph(doc, "7.3 การจัดการสัญญาณในระบบมัลติเธรด (Signal Handling in Multithreaded Systems)", style_type="heading1")
    add_styled_paragraph(doc, "ในสถาปัตยกรรมมัลติเธรด การกระจายสัญญาณแบ่งออกเป็น 2 ประเภทตามแหล่งกำเนิดและผลกระทบเชิงสถาปัตยกรรม [Love, 2010]:")
    add_styled_paragraph(doc, "1. สัญญาณแบบซิงโครนัส (Synchronous Signals): เกิดขึ้นจากการกระทำของเธรดนั้นโดยตรงจากคำสั่งระดับเครื่อง เช่น การเข้าถึงหน่วยความจำผิดพลาด (`SIGSEGV`) หรือการหารด้วยศูนย์ (`SIGFPE`) เคอร์เนลจะดำเนินการส่งสัญญาณตรงไปยังเธรดที่เป็นผู้ก่อให้เกิดข้อผิดพลาดแต่เพียงผู้เดียว (Thread-directed Delivery) เนื่องจากสแตกเฟรมและรีจิสเตอร์ของเธรดนั้นเป็นบริบทเดียวที่สัมพันธ์กับข้อผิดพลาด")
    add_styled_paragraph(doc, "2. สัญญาณแบบอะซิงโครนัส (Asynchronous Signals): เกิดขึ้นจากเหตุการณ์ภายนอกโพรเซส เช่น การกด `Ctrl+C` (`SIGINT`) หรือการส่งสัญญาณยุติการทำงาน (`SIGTERM`) สัญญาณระดับโพรเซสนี้จะถูกเคอร์เนลส่งไปยังเธรดใดเธรดหนึ่งที่ไม่บล็อกสัญญาณนั้น (Process-directed Delivery) หากมีหลายเธรดพร้อมรับ เคอร์เนลจะสุ่มเลือกเพียง 1 เธรดเท่านั้นในการประมวลผลสัญญาณ ไม่มีการกระจายแบบ Broadcast ให้ทุกเธรด [Linux man-pages, n.d.]")
    add_styled_paragraph(doc, "สถาปัตยกรรม Dedicated Signal Handling Thread (วิศวกรรมความปลอดภัยขั้นสูง):", style_type="heading2")
    add_styled_paragraph(doc, "การปล่อยให้สัญญาณอะซิงโครนัสขัดจังหวะเธรดทำงานใดๆ แบบสุ่มก่อให้เกิดความเสี่ยงต่อปัญหา Reentrancy เนื่องจากฟังก์ชันส่วนใหญ่ใน Standard Library ไม่ใช่ Async-Signal-Safe แนวทางปฏิบัติที่ดีที่สุด (Best Practice) ในระบบระดับอุตสาหกรรมคือการใช้สถาปัตยกรรมเธรดจัดการสัญญาณเฉพาะกิจ [Butenhof, 1997]:")
    add_styled_paragraph(doc, "ก. เธรดหลักจะทำการบล็อกสัญญาณอะซิงโครนัสทั้งหมด (เช่น `SIGINT`, `SIGTERM`) ด้วย `pthread_sigmask()` ก่อนที่จะเริ่มสร้างเธรดลูก เพื่อให้ Signal Mask นี้ถูกสืบทอดไปยังเธรดทำงานทั้งหมด")
    add_styled_paragraph(doc, "ข. สร้างเธรดเฉพาะกิจขึ้นมา 1 ตัว ทำหน้าที่เป็น Dedicated Signal Listener โดยเธรดนี้จะวนลูปเรียกใช้ฟังก์ชัน `sigwait(&set, &sig)` ซึ่งเป็นการนอนหลับรอคอยสัญญาณแบบ Synchronous")
    add_styled_paragraph(doc, "ค. เมื่อสัญญาณเข้ามา เธรดนี้จะตื่นขึ้นมารับสัญญาณในบริบทการทำงานปกติ ทำให้สามารถเรียกใช้ฟังก์ชันทั่วไปและประสานงานกับเธรดอื่นได้อย่างปลอดภัย ปราศจากความเสี่ยงเรื่อง Race Condition")

    # 7.4
    add_styled_paragraph(doc, "7.4 หน่วยความจำเฉพาะเธรด (Thread-Local Storage: TLS)", style_type="heading1")
    add_styled_paragraph(doc, "ในบางกรณีการออกแบบซอฟต์แวร์ต้องการตัวแปรที่มีขอบเขตการเข้าถึงแบบส่วนกลาง (Global Scope) เพื่อความสะดวกในการเรียกใช้ แต่จำเป็นต้องให้แต่ละเธรดมีสำเนาของค่าตัวแปรแยกเป็นอิสระต่อกันโดยสิ้นเชิงเพื่อป้องกัน Data Race โดยไม่ต้องใช้มิวเท็กซ์ล็อก กลไกนี้เรียกว่า Thread-Local Storage (TLS) [Drepper, 2007]")
    add_styled_paragraph(doc, "ในภาษา C11 ประกาศใช้ผ่านคีย์เวิร์ด `_Thread_local` (หรือ `__thread` ใน GCC) และ `thread_local` ใน C++11 ในระดับฮาร์ดแวร์ x86-64 สถาปัตยกรรมจัดการพื้นที่ TLS ผ่าน Segment Register พิเศษ ได้แก่ รีจิสเตอร์ `%fs` บน Linux และ `%gs` บน Windows โดยเคอร์เนลจะตั้งค่า Base Address ของเซกเมนต์ให้ชี้ไปยังบล็อก TLS ของแต่ละเธรด การเข้าถึงตัวแปร TLS จึงกระทำผ่าน Memory Offset ที่สัมพันธ์กับ Segment Register ได้อย่างรวดเร็วเทียบเท่าการเข้าถึงตัวแปร Local บนสแตก")

    # 7.5
    add_styled_paragraph(doc, "7.5 สถาปัตยกรรมเธรดพูล (Thread Pools Architecture)", style_type="heading1")
    add_styled_paragraph(doc, "ในระบบบริการเครือข่ายและเซิร์ฟเวอร์ การสร้างเธรดใหม่ตามคำขอของผู้ใช้แบบไม่จำกัด (Unbounded Thread Creation) นำไปสู่ปัญหาความเสี่ยง 2 ประการ: ค่าโสหุ้ยจากการสร้างและทำลายเธรดซ้ำซ้อน และวิกฤตหน่วยความจำหมดลง (Out-of-Memory / Resource Exhaustion) เมื่อมีคำขอเข้าพร้อมกันหลักหมื่นรายการ สถาปัตยกรรม \"เธรดพูล\" (Thread Pool) จึงถูกพัฒนาขึ้นเป็นเกราะป้องกัน [Silberschatz et al., 2018]")
    add_styled_paragraph(doc, "หลักการทำงานและองค์ประกอบเชิงวิศวกรรม:", style_type="heading2")
    add_styled_paragraph(doc, "1. Task Queue: คิวงานส่วนกลางแบบ FIFO ที่ได้รับการป้องกันด้วย Mutex และ Condition Variable ทำหน้าที่รับคำขอจากไคลเอนต์มาจัดเก็บไว้")
    add_styled_paragraph(doc, "2. Worker Threads: กลุ่มเธรดขนาดคงที่ (Core Pool Size) ที่ถูกสร้างขึ้นเตรียมไว้ล่วงหน้า เธรดเหล่านี้จะแย่งกันดึงงานออกจากคิวไปประมวลผล และเมื่อเสร็จสิ้นจะส่งตนเองกลับมารอรับงานใหม่ในพูลโดยไม่ถูกทำลายทิ้ง")
    add_styled_paragraph(doc, "3. กลไกการควบคุม Backpressure และ Saturation Policy: ในระบบระดับองค์กร คิวงานจะต้องมีการจำกัดขนาดสูงสุด (Bounded Queue) หากคำขอเข้ามาล้นคิว ระบบจะมีนโยบายรับมือ เช่น Caller-Runs (ให้เธรดผู้ส่งเป็นผู้ประมวลผลเองเพื่อชะลออัตราการส่ง) หรือ Abort เพื่อป้องกันไม่ให้หน่วยความจำของเซิร์ฟเวอร์ล้นจนระบบล่ม [Silberschatz et al., 2018]")

def build_chapter_8(doc):
    """บทที่ 8: กรณีศึกษาระดับเคอร์เนล: การวิเคราะห์เปรียบเทียบ Linux vs Windows (เป้าหมาย ~5-6 หน้า)"""
    add_styled_paragraph(doc, "บทที่ 8: กรณีศึกษาระดับเคอร์เนล: การวิเคราะห์เปรียบเทียบ Linux vs Windows (Kernel Case Studies)", style_type="chapter")
    
    # 8.1
    add_styled_paragraph(doc, "8.1 มัลติเธรดในระบบปฏิบัติการ Linux: ปรัชญา \"Everything is a Task\"", style_type="heading1")
    add_styled_paragraph(doc, "ระบบปฏิบัติการ Linux มีปรัชญาการออกแบบระดับเคอร์เนลที่เรียบง่ายแต่ทรงพลัง โดย \"เคอร์เนลของ Linux ไม่มีการแบ่งแยกความแตกต่างระหว่างโพรเซสและเธรด\" หน่วยของการประมวลผลและการจัดตารางเวลาทั้งหมดจะถูกมองเป็นเพียง \"ภารกิจ\" (Task) ภายใต้โครงสร้างข้อมูล `task_struct` เดียวกันทั้งหมด [Love, 2010]")
    add_styled_paragraph(doc, "ความแตกต่างระหว่างโพรเซสดั้งเดิมกับเธรดใน Linux เกิดขึ้นจาก \"ระดับการแบ่งปันทรัพยากร\" ผ่านตัวชี้ใน `task_struct`: โครงสร้าง `mm_struct *mm` (พื้นที่หน่วยความจำเสมือนและ Page Tables), `files_struct *files` (ตารางไฟล์ที่เปิด), `fs_struct *fs` (ระบบไฟล์และไดเรกทอรีราก), และ `sighand_struct *sighand` (ตารางจัดการสัญญาณ) [Bovet & Cesati, 2005]")
    add_styled_paragraph(doc, "หัวใจสำคัญคือซิสเต็มคอล `clone()` ซึ่งเปิดโอกาสให้ผู้เรียกกำหนดแฟล็กการแบ่งปันทรัพยากรได้อย่างยืดหยุ่น: การสร้างเธรดด้วยไลบรารี NPTL (`pthread_create`) จะเรียกใช้ `clone()` พร้อมแฟล็กหลักได้แก่ `CLONE_VM` (แชร์ Memory), `CLONE_FS` (แชร์ FS), `CLONE_FILES` (แชร์ Open Files), `CLONE_SIGHAND` (แชร์ Signals), และ `CLONE_THREAD` ซึ่งบังคับให้ Task ลูกถูกจัดเข้าเป็นสมาชิกใน Thread Group เดียวกันกับ Task แม่ และมี Thread Group ID (TGID) เดียวกัน ส่งผลให้ฟังก์ชัน `getpid()` ส่งคืนค่า PID ของโพรเซสแม่เดียวกัน [Love, 2010]")
    add_styled_paragraph(doc, "วิวัฒนาการสู่ `clone3()` ในเคอร์เนลร่วมสมัย: ใน Linux 5.3 ขึ้นไป ได้มีการเพิ่มซิสเต็มคอล `clone3()` ซึ่งเปลี่ยนจากการส่งพารามิเตอร์ผ่านรีจิสเตอร์ มาเป็นการส่งผ่านโครงสร้างข้อมูล `struct clone_args` เพื่อรองรับแฟล็กควบคุมขนาดใหญ่และเปิดทางให้กำหนด Control Groups (cgroups) ได้ตั้งแต่จังหวะแรกสร้างเธรด")
    add_styled_paragraph(doc, "ระบบจัดตารางเวลา Completely Fair Scheduler (CFS) และ EEVDF:", style_type="heading2")
    add_styled_paragraph(doc, "Linux 6.5 ใช้ตัวจัดตารางเวลา CFS ซึ่งทำงานบนแนวคิดความยุติธรรมผ่านตัวแปรเวลาเสมือน `vruntime` (Virtual Runtime) ตามสูตรทางคณิตศาสตร์:")
    add_styled_paragraph(doc, "$$\\Delta \\text{vruntime} = \\Delta \\text{exec\\_time} \\times \\left( \\frac{\\text{NICE\\_0\\_LOAD}}{\\text{weight}} \\right)$$")
    add_styled_paragraph(doc, "งานที่มีระดับความสำคัญสูง (Nice value ต่ำ น้ำหนัก weight มาก) เวลา `vruntime` จะเดินช้ากว่างานความสำคัญต่ำ งานที่พร้อมประมวลผลจะถูกจัดเก็บไว้ในโครงสร้างต้นไม้ Red-Black Tree จัดเรียงตามค่า `vruntime` จากน้อยไปมาก ซีพียูจะเลือกดึงงานทางซ้ายสุดที่ถูกแคชไว้ในพอยน์เตอร์ `rb_leftmost` มาทำงานด้วยความเร็ว $O(1)$ และแทรกกลับคืนด้วยความเร็ว $O(\\log N)$ เมื่อถึง Linux 6.6 เป็นต้นไป เคอร์เนลได้เริ่มเปลี่ยนผ่านสถาปัตยกรรม Fair Scheduling สู่ EEVDF (Earliest Eligible Virtual Deadline First) เพื่อลดความหน่วงเวลาและจัดการ Deadline ของงานเชิงตอบสนองได้อย่างแม่นยำยิ่งขึ้น [Linux Kernel Documentation, n.d.]")

    # 8.2
    add_styled_paragraph(doc, "8.2 มัลติเธรดในระบบปฏิบัติการ Microsoft Windows", style_type="heading1")
    add_styled_paragraph(doc, "แตกต่างจากปรัชญาของ Linux เคอร์เนลของ Microsoft Windows (สถาปัตยกรรม Windows NT จนถึง Windows 11) ถูกออกแบบภายใต้โครงสร้างเชิงวัตถุ (Object-Oriented) ที่แบ่งแยกชั้นการทำงานและโครงสร้างข้อมูลของโพรเซสและเธรดออกจากกันอย่างเด็ดขาด [Yosifovich et al., 2017]")
    add_styled_paragraph(doc, "โครงสร้างเธรดแบบสองระดับชั้นใน Windows Kernel:", style_type="heading2")
    add_styled_paragraph(doc, "1. `KTHREAD` (Kernel Thread Block): อยู่ในระดับ Microkernel Layer บรรจุข้อมูลพื้นฐานสำหรับการจัดตารางเวลา ได้แก่ สถานะรีจิสเตอร์ซีพียู, สแตกพอยน์เตอร์เคอร์เนล, ลำดับความสำคัญ (Priority 0–31), สถานะเธรด (Ready, Running, Standby, Waiting), โครงสร้าง Processor Affinity Mask, และโควตาเวลา (Scheduling Quantum)")
    add_styled_paragraph(doc, "2. `ETHREAD` (Executive Thread Block): อยู่ในระดับ Executive Layer ทำหน้าที่ห่อหุ้มโครงสร้าง `KTHREAD` ไว้อีกชั้นหนึ่ง บรรจุข้อมูลการจัดการระดับสูง เช่น Process ID, Thread ID, แอดเดรสเริ่มต้นของเธรด, สิทธิ์ความปลอดภัย (Access / Impersonation Security Token), โครงสร้าง I/O Pending Requests List, และการเชื่อมต่อกับ Asynchronous I/O Completion Ports (IOCP) [Yosifovich et al., 2017]")
    add_styled_paragraph(doc, "กลไก Fibers และ User-Mode Scheduling (UMS): Windows ยังสนับสนุนกลไก Concurrency ทางเลือกที่เรียกว่า \"Fibers\" ซึ่งเป็นการสลับบริบทในระดับ User-Mode แบบสมัครใจ (Cooperative) ผ่านคำสั่ง `SwitchToFiber()` โดยโปรแกรมเมอร์ อย่างไรก็ดี ไฟเบอร์ทั้งหมดจะยังคงรันอยู่บนโฮสต์ Kernel Thread หากเธรดโฮสต์ถูกบล็อกด้วย I/O ไฟเบอร์ทั้งหมดจะหยุดชะงักตามไปด้วย ส่วน UMS เป็นกลไก User-Mode Scheduler ที่ได้รับการสนับสนุนจากเคอร์เนลใน Windows รุ่นก่อนหน้า แต่ไม่มีการรองรับบน Windows 11 อีกต่อไป [Microsoft, n.d.]")

    # 8.3
    add_styled_paragraph(doc, "8.3 สถาปัตยกรรมฮาร์ดแวร์ขั้นสูง: ระบบ Non-Uniform Memory Access (NUMA)", style_type="heading1")
    add_styled_paragraph(doc, "ในสถาปัตยกรรมเซิร์ฟเวอร์ขนาดใหญ่หลายซ็อกเก็ต ผู้ผลิตได้เปลี่ยนจากการใช้ Symmetric Multiprocessing (SMP) มาใช้สถาปัตยกรรม Non-Uniform Memory Access (NUMA) โดยซีพียูแต่ละกลุ่ม (NUMA Node) จะมีหน่วยความจำแรมเป็นของตนเอง (Local Memory) ซึ่งเข้าถึงได้ด้วยความเร็วสูงสุด แต่หากเธรดต้องการเข้าถึงแรมของโหนดอื่น (Remote Memory) จะต้องส่งข้อมูลผ่าน Interconnect Bus (เช่น Intel UPI หรือ AMD Infinity Fabric) ซึ่งมี Latency สูงกว่าปกติ 2 ถึง 3 เท่าตัว [Lameter, 2013]")
    add_styled_paragraph(doc, "นโยบายการจัดสรรหน่วยความจำและ CPU Pinning เชิงวิศวกรรม:", style_type="heading2")
    add_styled_paragraph(doc, "เพื่อป้องกันการสูญเสียประสิทธิภาพจากการที่เคอร์เนลย้ายเธรดข้ามโหนดไปมา (Core Migration) วิศวกรระบบสามารถควบคุมความผูกพันของเธรดและนโยบายหน่วยความจำได้โดยตรงผ่านกลไกต่อไปนี้:")
    add_styled_paragraph(doc, "1. นโยบายการจัดสรรหน่วยความจำใน Linux NUMA: เคอร์เนลมีนโยบายหลัก 4 รูปแบบผ่านคำสั่ง `numactl`: (1) `MPOL_BIND` บังคับจัดสรรแรมเฉพาะบนโหนดที่กำหนดอย่างเข้มงวด, (2) `MPOL_INTERLEAVE` กระจายเพจหน่วยความจำสลับข้ามโหนดแบบ Round-robin เพื่อเฉลี่ยแบนด์วิดท์, (3) `MPOL_PREFERRED` พยายามจัดสรรบนโหนดที่ต้องการก่อน หากเต็มจึงข้ามไปโหนดอื่น, และ (4) `MPOL_DEFAULT` จัดสรรบนโหนดเดียวกับซีพียูที่รันโค้ดนั้น (First-touch Allocation Policy) [Lameter, 2013]")
    add_styled_paragraph(doc, "2. การควบคุมผ่านซอร์สโค้ดในภาษา C: เรียกใช้ฟังก์ชัน `pthread_setaffinity_np()` ร่วมกับโครงสร้าง `cpu_set_t` เพื่อกำหนด CPU Affinity Mask ของแต่ละเธรดอย่างละเอียด การทำ Core Pinning ช่วยรักษาความอุ่นของแคช L1/L2 และลดความแปรปรวนของเวลาประมวลผล (Deterministic Latency) ได้อย่างมีนัยสำคัญ [Love, 2010]")

    # 8.4
    add_styled_paragraph(doc, "8.4 การวิเคราะห์เปรียบเทียบสถาปัตยกรรมระดับเคอร์เนล: Linux vs. Windows", style_type="heading1")
    add_styled_paragraph(doc, "ตารางที่ 8.1 สรุปการเปรียบเทียบเชิงวิศวกรรมระหว่างระบบมัลติเธรดของเคอร์เนล Linux และ Windows:")
    
    add_styled_paragraph(doc, "ตารางที่ 8.1: การเปรียบเทียบสถาปัตยกรรมมัลติเธรดระหว่าง Linux และ Windows", style_type="table_caption")
    tbl_8_1 = [
        "| มิติทางสถาปัตยกรรม | ระบบปฏิบัติการ Linux (NPTL) | ระบบปฏิบัติการ Windows (NT Kernel) |",
        "|---|---|---|",
        "| ปรัชญาพื้นฐาน | Everything is a Task ไม่แยกโพรเซส/เธรดในเคอร์เนล | Object-Oriented แบ่งแยกโพรเซสและเธรดชัดเจน |",
        "| โครงสร้างข้อมูลหลัก | โครงสร้างเดี่ยว task_struct (จัดกลุ่มด้วย TGID) | สองชั้น: ETHREAD ห่อหุ้ม KTHREAD |",
        "| ซิสเต็มคอลการสร้าง | ซิสเต็มคอลเดียว clone() / clone3() | ซิสเต็มคอลเฉพาะ NtCreateThreadEx() |",
        "| แบบจำลองการจับคู่ | One-to-One (1:1) เป็นแกนหลัก | One-to-One; มี Fibers เป็นทางเลือกเฉพาะกิจ |",
        "| อัลกอริทึมจัดตารางเวลา | CFS (Linux 6.5) / EEVDF (Linux 6.6+) | Priority-driven Preemptive (32 ลำดับความสำคัญ) |",
        "| กลไกการซิงโครไนซ์เร็ว | Linux Futex (Fast Userspace Mutex) | Slim Reader/Writer (SRW) Locks / Critical Sections |",
        "| จุดเด่นเชิงวิศวกรรม | น้ำหนักเบา สลับงานรวดเร็ว เหมาะกับ Cloud/Server | ความปลอดภัยสูง สมบูรณ์แบบสำหรับ Enterprise/GUI |"
    ]
    add_markdown_table(doc, tbl_8_1, col_widths=[1.5, 2.1, 2.17])

def build_chapter_9(doc):
    """บทที่ 9: อนาคตและวิวัฒนาการ: Concurrency ในระดับ User-Space (เป้าหมาย ~4 หน้า)"""
    add_styled_paragraph(doc, "บทที่ 9: อนาคตและวิวัฒนาการ: Concurrency ในระดับ User-Space (Modern Concurrency Paradigms)", style_type="chapter")
    
    # 9.1
    add_styled_paragraph(doc, "9.1 ขีดจำกัดของ OS Threads กับสถาปัตยกรรม Web Scale ยุคใหม่ (The C10K & C1000K Problems)", style_type="heading1")
    add_styled_paragraph(doc, "ในยุคเริ่มต้นของอินเทอร์เน็ต ความท้าทายหลักของสถาปัตยกรรมเซิร์ฟเวอร์คือการรองรับ 10,000 การเชื่อมต่อพร้อมกัน (The C10K Problem) [Kegel, 1999] และในปัจจุบันได้ขยายสู่ความท้าทายระดับ 1,000,000 การเชื่อมต่อ (The C1000K Problem) บนระบบคลาวด์ขนาดใหญ่ ปัญหานี้เปิดโปงข้อจำกัดเชิงสถาปัตยกรรมของเธรดระดับระบบปฏิบัติการ (OS Threads แบบ 1:1) อย่างชัดเจน:")
    add_styled_paragraph(doc, "1. ข้อจำกัดด้านพื้นที่สแตก (Thread Stack Footprint): OS Thread ทั่วไปมีการจองขนาดสแตกเริ่มต้นประมาณ 1 ถึง 2 MiB หากเซิร์ฟเวอร์ต้องสร้างเธรดรองรับการเชื่อมต่อ 100,000 เธรด จะต้องใช้พื้นที่หน่วยความจำเสมือนมหาศาลเกือบ 200 GiB แม้หน่วยความจำกายภาพจะถูกจัดสรรตามจริง (Demand Paging) แต่ค่าโสหุ้ยของ Page Tables และ Kernel Stacks (8-16 KiB ต่อเธรด) จะทำให้หน่วยความจำเคอร์เนลหมดลงอย่างรวดเร็ว [Drepper, 2007]")
    add_styled_paragraph(doc, "2. ค่าโสหุ้ยการสลับบริบทในเคอร์เนล (Context Switch Thrashing): เมื่อมีเธรดจำนวนหลายหมื่นตัว เคอร์เนลจะสูญเสียรอบสัญญาณนาฬิกาของซีพียูไปกับการบันทึกรีจิสเตอร์ สลับตารางหน้า และไล่ตรวจคิวงาน จนเกิดสภาวะชะงักงัน (Kernel Depletion) โดยแทบไม่มีเวลาประมวลผลคำขอจริง [Kegel, 1999]")
    add_styled_paragraph(doc, "การเปรียบเทียบภาระหน่วยความจำเชิงคำนวณ: หากต้องการรองรับ 50,000 การเชื่อมต่อพร้อมกัน สถาปัตยกรรม OS Thread (1:1) ที่มีสแตกขั้นต่ำ 1 MiB จะต้องใช้พื้นที่หน่วยความจำเสมือนอย่างน้อย 50 GiB และสูญเสียแรมเคอร์เนลสำหรับ Kernel Stack ประมาณ 400–800 MiB ขณะที่ User-Space Lightweight Concurrency ที่มีสแตกเริ่มต้น 2 KiB จะใช้หน่วยความจำเพียงประมาณ 100 MiB เท่านั้น (ประหยัดกว่าถึง 500 เท่า) เปิดทางให้เครื่องเซิร์ฟเวอร์ขนาดทั่วไปสามารถรองรับโหลดมหาศาลได้")

    # 9.2
    add_styled_paragraph(doc, "9.2 การเกิดใหม่ของ User-Space Lightweight Concurrency", style_type="heading1")
    add_styled_paragraph(doc, "เพื่อก้าวข้ามขีดจำกัดของเคอร์เนลเธรด วงการวิศวกรรมซอฟต์แวร์ได้คิดค้นกระบวนทัศน์ใหม่โดยการนำการจัดการ Concurrency กลับขึ้นมาไว้ในระดับรันไทม์ของผู้ใช้ (User-Space Runtime):")
    add_styled_paragraph(doc, "กอรูทีนในภาษา Go (Goroutines: The M-P-G Model):", style_type="heading2")
    add_styled_paragraph(doc, "ภาษา Go พลิกโฉมสถาปัตยกรรมด้วย \"Goroutines\" ซึ่งมีขนาดสแตกเริ่มต้นขนาดจิ๋วเพียงประมาณ 2 KiB และสามารถขยายตัวได้เองแบบพลวัต (Dynamic Contiguous Stack) เมื่อหน่วยความจำไม่เพียงพอ การจัดตารางเวลาทำงานผ่าน Go Runtime Scheduler ภายใต้แบบจำลอง M-P-G: $G$ แทน Goroutine, $M$ แทน Machine (OS Kernel Thread), และ $P$ แทน Processor Context (โควตาทรัพยากรตามค่า GOMAXPROCS) แต่ละ $P$ จะมี Local Run Queue บรรจุได้ 256 กอรูทีน เมื่อคิวของตนเองว่างลง รันไทม์จะใช้ อัลกอริทึม Work-Stealing เข้าไปสุ่มขโมยงานครึ่งหนึ่งจากคิวของ $P$ อื่นมาประมวลผล [The Go Authors, 2024]")
    add_styled_paragraph(doc, "นอกจากนี้ Go Runtime ยังผสานการทำงานกับ Network Poller ซึ่งแปลงคำสั่ง I/O ที่ดูเหมือนเป็นการบล็อกในโค้ด ให้กลายเป็นการเรียกใช้งาน I/O Multiplexing ระดับเคอร์เนล (`epoll` บน Linux หรือ `kqueue` บน macOS) ส่งผลให้ Goroutine สามารถหยุดรอคอยได้อย่างมีประสิทธิภาพโดยที่ OS Thread หลักไม่ต้องหลับเลย")
    add_styled_paragraph(doc, "เวอร์ชวลเธรดใน Java 21 (Project Loom):", style_type="heading2")
    add_styled_paragraph(doc, "ภาษา Java 21 ได้ปฏิวัติระบบ Concurrency ครั้งใหญ่ด้วย Virtual Threads (JEP 444) ซึ่งออกแบบมาเพื่อ \"คงรูปแบบการเขียนโค้ดสไตล์ Synchronous Blocking ที่เข้าใจง่าย แต่ให้ Throughput สูงเทียบเท่า Asynchronous Programming\" [Pressler & Bateman, 2023] Virtual Threads จะถูกรันอยู่บน Carrier Threads (OS Thread ปกติ) เมื่อเวอร์ชวลเธรดทำงานคำสั่ง I/O ที่ต้องรอคอย รันไทม์ของ JVM จะดำเนินการปลดเธรดออกจาก Carrier (Unmount) และเก็บสถานะสแตกไว้บน Java Heap เปิดโอกาสให้ Carrier Thread ไปรันเวอร์ชวลเธรดตัวอื่นต่อทันที และจะนำกลับมาเชื่อมต่อ (Mount) ใหม่อีกครั้งเมื่อข้อมูล I/O พร้อม ทั้งนี้มีข้อยกเว้นเรื่อง Thread Pinning ที่ต้องระวัง คือหากเวอร์ชวลเธรดทำงานอยู่ภายในบล็อก `synchronized` หรือเรียก Native Code (JNI) มันจะไม่สามารถ Unmount ได้ ซึ่งอาจจำกัด Scalability หากไม่ปรับไปใช้ `ReentrantLock` [Oracle, 2023]")

    # 9.3
    add_styled_paragraph(doc, "9.3 การวิเคราะห์เปรียบเทียบกระบวนทัศน์ Concurrency แห่งอนาคต", style_type="heading1")
    add_styled_paragraph(doc, "ตารางที่ 9.1 เปรียบเทียบคุณลักษณะเชิงวิศวกรรมของ 3 กระบวนทัศน์ Concurrency ยุคใหม่:")
    
    add_styled_paragraph(doc, "ตารางที่ 9.1: การเปรียบเทียบกระบวนทัศน์ Concurrency ยุคใหม่", style_type="table_caption")
    tbl_9_1 = [
        "| มิติการเปรียบเทียบ | Multi-threaded (OS Thread 1:1) | Single-threaded Event Loop | Lightweight User Threads (M:N) |",
        "|---|---|---|---|",
        "| ตัวอย่างเทคโนโลยี | C/C++ Pthreads, Java ดั้งเดิม, C# | Node.js, Nginx, Python Asyncio | Go (Goroutines), Java 21 (Loom) |",
        "| ขนาดหน่วยความจำต่อหน่วย | สูง (1–2 MiB Stack Reservation) | ต่ำมาก (แชร์ Event Loop Stack) | ต่ำมาก (2 KiB สแตกขยายตัวได้) |",
        "| สไตล์การเขียนโค้ด | Synchronous Blocking (อ่านง่าย) | Asynchronous Callbacks/Async-Await | Synchronous Blocking (อ่านง่ายที่สุด) |",
        "| การรองรับ Multi-Core | สมบูรณ์แบบ (เคอร์เนลกระจายลงคอร์) | ต้องรันแยกโพรเซสเพื่อกระจายคอร์ | สมบูรณ์แบบ (รันไทม์กระจายลง M คอร์) |",
        "| ความง่ายในการดีบัก | ปานกลาง มี Stack Trace ครบถ้วน | ซับซ้อนสูง Stack Trace ขาดตอน | ง่ายมาก มี Stack Trace สมบูรณ์ |",
        "| จุดคอขวดที่ต้องระวัง | Context Switch Thrashing / แรมหมด | คำนวณหนักจะบล็อกทั้ง Loop | ปริมาณงาน GC บนหน่วยความจำ Heap |"
    ]
    add_markdown_table(doc, tbl_9_1, col_widths=[1.3, 1.4, 1.5, 1.57])

def build_chapter_10(doc):
    """บทที่ 10: การอภิปรายผลเชิงวิพากษ์ กรอบการตัดสินใจ และบทสรุป (เป้าหมาย ~4-5 หน้า)"""
    add_styled_paragraph(doc, "บทที่ 10: การอภิปรายผลเชิงวิพากษ์ กรอบการตัดสินใจ และบทสรุป (Critical Discussion, Decision Matrix & Conclusion)", style_type="chapter")
    
    # 10.1
    add_styled_paragraph(doc, "10.1 การอภิปรายผลการศึกษาและการทดลองเชิงวิพากษ์ (Critical Synthesis)", style_type="heading1")
    add_styled_paragraph(doc, "จากการศึกษาทฤษฎีเชิงสถาปัตยกรรม การวิเคราะห์ซอร์สโค้ดระดับเคอร์เนล และการทดลองวัดผลเชิงประจักษ์ สามารถนำมาสังเคราะห์เพื่อตอบ คำถามหลักของการวิจัย 4 ประการ ที่กำหนดไว้ในบทที่ 1 ได้อย่างชัดเจน:")
    add_styled_paragraph(doc, "1. มัลติเธรดช่วยเพิ่มประสิทธิภาพเมื่อใด และมีต้นทุนแฝงอะไรบ้าง? ผลการทดลองชี้ชัดว่า มัลติเธรดจะเพิ่ม Throughput ได้สูงสุดเฉพาะในภาระงานที่แบ่งแยกขนานได้อย่างเป็นอิสระ (Embarrassingly Parallel) แต่เมื่อจำนวนเธรดขยายเกินขีดจำกัดทางกายภาพ ต้นทุนแฝงระดับฮาร์ดแวร์จะปรากฏขึ้นทันที ได้แก่ Involuntary Context Switches ที่พุ่งสูงขึ้น 4,210 ครั้ง, อัตรา Cache Thrashing ที่ทำให้ LLC Misses พุ่งถึง 5.94 ล้านครั้ง, และการอิ่มตัวของ Memory Bus Traffic ซึ่งทำให้ IPC ดิ่งลง")
    add_styled_paragraph(doc, "2. แบบจำลองการจับคู่เธรดสร้างความแตกต่างอย่างไร? แบบจำลอง 1:1 ของระบบปฏิบัติการมอบประสิทธิภาพสูงสุดสำหรับงาน CPU-bound เนื่องจากสามารถเข้าถึงฟีเจอร์ฮาร์ดแวร์คอร์ได้โดยตรง ขณะที่แบบจำลอง M:N ยุคใหม่ (Lightweight User-Space Concurrency เช่น Goroutines และ Virtual Threads) สามารถลดโสหุ้ยหน่วยความจำและเปิดทางให้รองรับการเชื่อมต่อพร้อมกันระดับแสนรายการได้อย่างยอดเยี่ยม")
    add_styled_paragraph(doc, "3. คอขวดของการประสานเวลาเกิดขึ้นที่จุดใด? คอขวดที่แท้จริงเกิดจาก Bus Contention และ Cache Invalidation Storm เมื่อเกิดการแย่งชิงล็อกสูง ดังที่เห็นจากการพังทลายของ Spinlock ที่ช้าลงกว่า Mutex ถึง 2.37 เท่า ขณะที่กลไก Lock-Free Atomic CAS สามารถทะลุผ่านคอขวดนี้ได้ดีที่สุด")
    add_styled_paragraph(doc, "4. ความสมเหตุสมผลของแบบจำลองคณิตศาสตร์: กฎของอัมดาห์ลทำนาย Speedup ได้ดีในช่วงเริ่มต้น แต่ไม่สามารถทำนายสภาวะถดถอยเมื่อเกิด Over-subscription ได้ ขณะที่ Universal Scalability Law (USL) สามารถสะท้อนพฤติกรรมจริงได้แม่นยำกว่าด้วยพจน์ Coherency Penalty ($\\beta$) ที่อธิบายต้นทุนการสื่อสารข้ามแคชได้อย่างสมบูรณ์")

    # 10.2
    add_styled_paragraph(doc, "10.2 กรอบการตัดสินใจทางวิศวกรรมสำหรับสถาปนิกซอฟต์แวร์ (Engineering Decision Framework)", style_type="heading1")
    add_styled_paragraph(doc, "เพื่อเป็นเกณฑ์เชิงปฏิบัติการแก่วิศวกรระบบและสถาปนิกซอฟต์แวร์ ตารางที่ 10.1 สรุปเมทริกซ์การตัดสินใจทางสถาปัตยกรรม (Architecture Decision Matrix) สำหรับการเลือกใช้เทคโนโลยี Concurrency ให้ตรงกับลักษณะงาน:")
    
    add_styled_paragraph(doc, "ตารางที่ 10.1: ตารางตัดสินใจเปรียบเทียบเทคโนโลยี Concurrency เชิงวิศวกรรม", style_type="table_caption")
    tbl_10_1 = [
        "| มิติการประเมิน | Multiprocessing | OS Thread Pool (1:1) | Non-blocking Event Loop | Virtual Threads / Goroutines |",
        "|---|---|---|---|---|",
        "| ขอบเขตความปลอดภัย | สูงมาก (แยกแอดเดรสสมบูรณ์) | ต่ำ (1 เธรดแครชกระทบทั้งโปรเซส) | ต่ำ (ทำงานในโพรเซสเดียว) | ต่ำ (ทำงานในโพรเซสเดียว) |",
        "| ประสิทธิภาพ CPU-Bound | ปานกลาง (โสหุ้ยแรมสูง) | สูงมาก (ดึงพลังคอร์ตรง) | ต่ำ (ไม่เหมาะกับงานคำนวณ) | สูงมาก (เทียบเท่าเคอร์เนลเธรด) |",
        "| ประสิทธิภาพ I/O-Bound | ปานกลาง-ต่ำ (จำกัดโพรเซส) | ปานกลาง (จำกัดตามพูล) | สูงมาก (Throughput สูง) | สูงมากที่สุด (Throughput สูงมาก) |",
        "| ปริมาณการเชื่อมต่อพร้อมกัน | ต่ำ (หลักร้อยถึงพัน) | ปานกลาง (หลักร้อยถึงพัน) | สูงมาก (หลักหมื่นถึงแสน) | สูงมากที่สุด (หลักแสนถึงล้าน) |",
        "| ความง่ายในการพัฒนา | ปานกลาง (ต้องเขียน IPC) | ปานกลาง (ต้องคุมซิงโครไนซ์) | ยาก (ซับซ้อนของ Asynchronous) | ง่ายมาก (โค้ด Synchronous ดั้งเดิม) |",
        "| กรณีการใช้งานที่แนะนำ | เว็บเบราว์เซอร์, Sandbox | งานคำนวณวิทยาศาสตร์, เอนจิน 3D | Reverse Proxy, API Gateway | เว็บแอปพลิเคชันยุคใหม่, Microservices |"
    ]
    add_markdown_table(doc, tbl_10_1, col_widths=[1.2, 1.1, 1.1, 1.17, 1.2])

    # 10.3
    add_styled_paragraph(doc, "10.3 ข้อจำกัดของการศึกษาและการทดลอง (Limitations of the Study)", style_type="heading1")
    add_styled_paragraph(doc, "1. สถาปัตยกรรมฮาร์ดแวร์ทดสอบ: การทดลองหลักดำเนินการบนซีพียูระดับไคลเอนต์ Intel Core i7-12700H สถาปัตยกรรมคอร์แบบไฮบริด (P-Cores + E-Cores) ซึ่งแม้จะมีการตรึงคอร์แล้ว แต่พฤติกรรมบางประการอาจแตกต่างจากสถาปัตยกรรมเซิร์ฟเวอร์แบบ Multi-Socket NUMA ขนาดใหญ่")
    add_styled_paragraph(doc, "2. สัญญาณรบกวนจากระบบปฏิบัติการทั่วไป (OS Jitter): การทดสอบบนระบบปฏิบัติการอเนกประสงค์ (General-Purpose OS) ย่อมมีสัญญาณรบกวนจาก Background Daemons และการจัดการพลังงานของฮาร์ดแวร์ แม้ว่าจะใช้ Governor แบบ performance แล้วก็ตาม")
    add_styled_paragraph(doc, "3. ข้อจำกัดของภาระงานทดสอบสังเคราะห์: การคำนวณเมทริกซ์และการจำลอง I/O เป็น Synthetic Workloads ที่สะท้อนพฤติกรรมพื้นฐาน การนำไปประยุกต์ใช้ในระบบงานจริงต้องพิจารณาปัจจัยเฉพาะตัวของแอปพลิเคชันร่วมด้วย")

    # 10.4
    add_styled_paragraph(doc, "10.4 บทสรุปผลการศึกษาและการสังเคราะห์ทางวิศวกรรม (Conclusion)", style_type="heading1")
    add_styled_paragraph(doc, "รายงานเชิงวิชาการฉบับนี้ได้ศึกษาและทดสอบสถาปัตยกรรมการจัดการเธรดในระบบปฏิบัติการสมัยใหม่อย่างครอบคลุม โดยสรุปผลการศึกษาสำคัญ 5 ประการได้ดังนี้:")
    add_styled_paragraph(doc, "1. เธรดคือหน่วยย่อยของการประมวลผลที่แชร์ Address Space และทรัพยากรระดับโพรเซสร่วมกัน โดยมีเพียง Register Context และ Stack เป็นของตนเอง ช่วยลดต้นทุนในการสร้างและสลับบริบทได้อย่างมหาศาล")
    add_styled_paragraph(doc, "2. การเปรียบเทียบระหว่างโพรเซสและเธรดยืนยันการแลกเปลี่ยนผลประโยชน์พื้นฐาน (Trade-off) ระหว่าง \"ประสิทธิภาพที่เหนือกว่า\" ของมัลติเธรด ปะทะ \"ความปลอดภัยจากการแบ่งแยกขอบเขต\" (Fault Isolation) ของมัลติโพรเซส")
    add_styled_paragraph(doc, "3. กลไกการซิงโครไนซ์ระดับเคอร์เนล เช่น Linux Futex มอบความสมดุลระหว่างความเร็วใน User Space และความปลอดภัยในการรอคอย ขณะที่การประมวลผลแบบไร้ล็อก (Lock-Free Atomics) เป็นทางออกที่มีประสิทธิภาพสูงสุดในการลดคอขวดการแย่งชิงล็อก")
    add_styled_paragraph(doc, "4. การทดลองเชิงประจักษ์พิสูจน์ให้เห็นว่า จำนวนเธรดที่เหมาะสมที่สุดสำหรับงาน CPU-bound คือจำนวนคอร์ประมวลผลทางกายภาพบวกกับเทคโนโลยี SMT (12 เธรดในการทดลองนี้) การเพิ่มเธรดเกินพิกัดจะนำไปสู่อัตราเร่งที่ถดถอยเนื่องจากการสูญเสียแคชและการสลับบริบทที่มากเกินไป")
    add_styled_paragraph(doc, "5. ในระบบงานสมัยใหม่ที่ต้องรองรับการเชื่อมต่อมหาศาล สถาปัตยกรรม Concurrency ได้วิวัฒนาการไปสู่ Lightweight User-Space Threads เช่น Go Goroutines และ Java Virtual Threads ซึ่งมอบประสิทธิภาพสูงสุดควบคู่กับความสะดวกในการพัฒนา")

print("All chapter builders defined successfully.")
