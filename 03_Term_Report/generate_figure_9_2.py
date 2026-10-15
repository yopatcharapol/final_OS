#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_figure_9_2.py
สร้างรูปภาพ รูปที่ 9.2 สำหรับรายงานวิชา OS
สถาปัตยกรรม Go M-P-G Work-Stealing Scheduler
(ปรับปรุงความสวยงาม ทิศทางลูกศร และลบสัญลักษณ์ที่ฟอนต์ไม่รองรับ)
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch
from matplotlib import rcParams

# กำหนดฟอนต์ให้รองรับภาษาไทยสวยงาม คมชัด
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Leelawadee UI', 'Tahoma', 'TH Sarabun New', 'Arial']
rcParams['axes.unicode_minus'] = False

def create_figure():
    fig = plt.figure(figsize=(15.2, 8.8), dpi=300, facecolor='#ffffff')
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 15.2)
    ax.set_ylim(0, 8.8)
    ax.axis('off')

    # 1. กรอบการ์ดใหญ่พื้นหลัง (Card Container)
    card = FancyBboxPatch(
        (0.35, 0.65), 14.5, 7.75,
        boxstyle="round,pad=0.1,rounding_size=0.25",
        facecolor='#fbfcfd',
        edgecolor='#cbd5e1',
        linewidth=1.5,
        zorder=1
    )
    ax.add_patch(card)

    # หัวข้อใหญ่ด้านบนการ์ด
    ax.text(0.75, 8.05, "สถาปัตยกรรม Go M-P-G Work-Stealing Scheduler (User-Space Concurrency Engine)",
            fontsize=13.5, fontweight='bold', color='#0f172a', va='center')
    ax.plot([0.75, 14.45], [7.82, 7.82], color='#e2e8f0', lw=1.2, zorder=2)

    # =========================================================================
    # ชั้นที่ 1: Kernel Space (OS Threads & Physical Cores) -> y = 6.4 ถึง 7.6
    # =========================================================================
    # ป้ายระบุพื้นที่ Kernel Space
    k_badge = FancyBboxPatch(
        (0.75, 6.45), 2.7, 1.15,
        boxstyle="round,pad=0.04,rounding_size=0.12",
        facecolor='#f1f5f9',
        edgecolor='#94a3b8',
        linewidth=1.4,
        zorder=3
    )
    ax.add_patch(k_badge)
    ax.text(2.1, 7.15, "Kernel Space", fontsize=11.5, fontweight='bold',
            color='#334155', ha='center', va='center', zorder=4)
    ax.text(2.1, 6.72, "(OS Threads &\nHardware Cores)", fontsize=9.2,
            color='#64748b', ha='center', va='center', zorder=4)

    # กล่อง OS Thread M 0 (รันบน Core 0)
    m0_box = FancyBboxPatch(
        (4.4, 6.45), 4.2, 1.15,
        boxstyle="round,pad=0.04,rounding_size=0.12",
        facecolor='#fee2e2',
        edgecolor='#ef4444',
        linewidth=1.6,
        zorder=3
    )
    ax.add_patch(m0_box)
    ax.text(6.5, 7.15, "OS Thread: M 0", fontsize=12, fontweight='bold',
            color='#991b1b', ha='center', va='center', zorder=4)
    ax.text(6.5, 6.72, "ผูกกับ Hardware CPU Core 0 (Kernel Thread)", fontsize=9.5,
            color='#b91c1c', ha='center', va='center', zorder=4)

    # กล่อง OS Thread M 1 (รันบน Core 1)
    m1_box = FancyBboxPatch(
        (9.8, 6.45), 4.2, 1.15,
        boxstyle="round,pad=0.04,rounding_size=0.12",
        facecolor='#fee2e2',
        edgecolor='#ef4444',
        linewidth=1.6,
        zorder=3
    )
    ax.add_patch(m1_box)
    ax.text(11.9, 7.15, "OS Thread: M 1", fontsize=12, fontweight='bold',
            color='#991b1b', ha='center', va='center', zorder=4)
    ax.text(11.9, 6.72, "ผูกกับ Hardware CPU Core 1 (Kernel Thread)", fontsize=9.5,
            color='#b91c1c', ha='center', va='center', zorder=4)

    # เส้นประแบ่งเขต Kernel Space กับ User Space (Go Runtime)
    ax.plot([0.75, 14.45], [6.18, 6.18], color='#cbd5e1', lw=1.2, linestyle='--', zorder=2)
    ax.text(14.35, 6.28, "เส้นแบ่ง Kernel / User-Space", fontsize=8.5, color='#94a3b8', ha='right', va='bottom')

    # ลูกศรเชื่อม M 0 -> P 0
    arrow_m0_p0 = FancyArrowPatch(
        (6.5, 6.45), (6.5, 5.75),
        arrowstyle="->,head_width=4,head_length=6",
        color='#dc2626', lw=2.2, zorder=5
    )
    ax.add_patch(arrow_m0_p0)
    ax.text(6.65, 6.1, "ยึดครอง", fontsize=9, fontweight='bold', color='#dc2626', va='center')

    # ลูกศรเชื่อม M 1 -> P 1
    arrow_m1_p1 = FancyArrowPatch(
        (11.9, 6.45), (11.9, 5.75),
        arrowstyle="->,head_width=4,head_length=6",
        color='#dc2626', lw=2.2, zorder=5
    )
    ax.add_patch(arrow_m1_p1)
    ax.text(12.05, 6.1, "ยึดครอง", fontsize=9, fontweight='bold', color='#dc2626', va='center')

    # =========================================================================
    # ชั้นที่ 2: User Space / Go Runtime -> y = 2.4 ถึง 5.7
    # =========================================================================
    # ป้ายระบุพื้นที่ Go Runtime
    rt_badge = FancyBboxPatch(
        (0.75, 3.1), 2.7, 2.6,
        boxstyle="round,pad=0.04,rounding_size=0.12",
        facecolor='#ecfeff',
        edgecolor='#0891b2',
        linewidth=1.4,
        zorder=3
    )
    ax.add_patch(rt_badge)
    ax.text(2.1, 5.25, "Go Runtime", fontsize=12, fontweight='bold',
            color='#0e7490', ha='center', va='center', zorder=4)
    ax.text(2.1, 4.45, "M:N Scheduler\n(Work-Stealing)\n\nGOMAXPROCS = 2\n(2 Logical Processors)",
            fontsize=9.2, color='#0891b2', ha='center', va='center', linespacing=1.25, zorder=4)
    ax.text(2.1, 3.45, "จัดสรร Goroutines\nลง OS Thread อิสระ\nไม่ต้องพึ่งพาเคอร์เนล",
            fontsize=8.5, color='#0e7490', ha='center', va='center', linespacing=1.2, zorder=4)

    # ------------------ คอลัมน์ซ้าย: Processor P 0 ------------------
    # กล่อง Processor: P 0
    p0_box = FancyBboxPatch(
        (4.4, 4.6), 4.2, 1.1,
        boxstyle="round,pad=0.04,rounding_size=0.1",
        facecolor='#e0f2fe',
        edgecolor='#0284c7',
        linewidth=1.6,
        zorder=3
    )
    ax.add_patch(p0_box)
    ax.text(6.5, 5.35, "Processor: P 0 (Logical Context)", fontsize=11, fontweight='bold',
            color='#0369a1', ha='center', va='center', zorder=4)
    
    # Goroutine ที่กำลังประมวลผลอยู่ (Running G) บน P 0
    run_g0 = FancyBboxPatch(
        (4.65, 4.75), 3.7, 0.42,
        boxstyle="round,pad=0.02,rounding_size=0.06",
        facecolor='#dcfce7',
        edgecolor='#16a34a',
        linewidth=1.2,
        zorder=4
    )
    ax.add_patch(run_g0)
    ax.text(6.5, 4.96, "[Running] กำลังประมวลผล: G 0", fontsize=9.5, fontweight='bold',
            color='#15803d', ha='center', va='center', zorder=5)

    # กล่องคิวงานของ P 0: Local Runqueue
    lrq0_box = FancyBboxPatch(
        (4.4, 3.0), 4.2, 1.45,
        boxstyle="round,pad=0.04,rounding_size=0.1",
        facecolor='#f8fafc',
        edgecolor='#0284c7',
        linewidth=1.3,
        zorder=3
    )
    ax.add_patch(lrq0_box)
    ax.text(6.5, 4.18, "Local Runqueue ของ P 0 (คิวงานในตัว)", fontsize=10, fontweight='bold',
            color='#0284c7', ha='center', va='center', zorder=4)
    
    # องค์ประกอบ Goroutines ในคิว P 0: [G 1] [G 2] [G 3]
    g_items = [
        {"name": "G 1", "desc": "(รอรัน)"},
        {"name": "G 2", "desc": "(จะถูกขโมย)"},
        {"name": "G 3", "desc": "(จะถูกขโมย)"}
    ]
    gx_start = 4.65
    for i, g in enumerate(g_items):
        bg_col = '#bae6fd' if i == 0 else '#f3e8ff'
        border_col = '#0284c7' if i == 0 else '#a855f7'
        text_col = '#0369a1' if i == 0 else '#7e22ce'
        
        g_box = FancyBboxPatch(
            (gx_start + i * 1.25, 3.32), 1.15, 0.65,
            boxstyle="round,pad=0.02,rounding_size=0.06",
            facecolor=bg_col,
            edgecolor=border_col,
            linewidth=1.2,
            zorder=4
        )
        ax.add_patch(g_box)
        ax.text(gx_start + i * 1.25 + 0.57, 3.70, g["name"], fontsize=10.5, fontweight='bold',
                color=text_col, ha='center', va='center', zorder=5)
        ax.text(gx_start + i * 1.25 + 0.57, 3.46, g["desc"], fontsize=7.6,
                color=text_col, ha='center', va='center', zorder=5)

    ax.text(6.5, 3.12, "(มี Goroutines รอคิวอยู่ 3 ตัว: งานล้นคิว)", fontsize=8.8,
            color='#64748b', ha='center', va='center', zorder=4)

    # ------------------ คอลัมน์ขวา: Processor P 1 ------------------
    # กล่อง Processor: P 1
    p1_box = FancyBboxPatch(
        (9.8, 4.6), 4.2, 1.1,
        boxstyle="round,pad=0.04,rounding_size=0.1",
        facecolor='#e0f2fe',
        edgecolor='#0284c7',
        linewidth=1.6,
        zorder=3
    )
    ax.add_patch(p1_box)
    ax.text(11.9, 5.35, "Processor: P 1 (Logical Context)", fontsize=11, fontweight='bold',
            color='#0369a1', ha='center', va='center', zorder=4)

    # Goroutine ที่กำลังประมวลผลอยู่บน P 1 (กำลังจะเสร็จ)
    run_g4 = FancyBboxPatch(
        (10.05, 4.75), 3.7, 0.42,
        boxstyle="round,pad=0.02,rounding_size=0.06",
        facecolor='#dcfce7',
        edgecolor='#16a34a',
        linewidth=1.2,
        zorder=4
    )
    ax.add_patch(run_g4)
    ax.text(11.9, 4.96, "[Running] กำลังประมวลผล: G 4 (กำลังเสร็จ)", fontsize=9.5, fontweight='bold',
            color='#15803d', ha='center', va='center', zorder=5)

    # กล่องคิวงานของ P 1: Local Runqueue (ว่างเปล่า!)
    lrq1_box = FancyBboxPatch(
        (9.8, 3.0), 4.2, 1.45,
        boxstyle="round,pad=0.04,rounding_size=0.1",
        facecolor='#fffbeb',
        edgecolor='#f59e0b',
        linewidth=1.4,
        linestyle='--',
        zorder=3
    )
    ax.add_patch(lrq1_box)
    ax.text(11.9, 4.18, "Local Runqueue ของ P 1 (คิวงานในตัว)", fontsize=10, fontweight='bold',
            color='#b45309', ha='center', va='center', zorder=4)
    
    # กล่องว่างเปล่าในคิว P 1 (เป้าหมายของการขโมยงาน)
    empty_box = FancyBboxPatch(
        (10.15, 3.32), 3.5, 0.65,
        boxstyle="round,pad=0.02,rounding_size=0.06",
        facecolor='#fef3c7',
        edgecolor='#f59e0b',
        linewidth=1.3,
        zorder=4
    )
    ax.add_patch(empty_box)
    ax.text(11.9, 3.70, "[Empty] คิวว่างเปล่า (ไม่มีงานรอ)", fontsize=10, fontweight='bold',
            color='#92400e', ha='center', va='center', zorder=5)
    ax.text(11.9, 3.46, "รอรับงานจากการขโมย (Steal Target)", fontsize=8.0,
            color='#b45309', ha='center', va='center', zorder=5)

    ax.text(11.9, 3.12, "(หากไม่ขโมยงาน M 1 จะว่างงาน: Idle Starvation)", fontsize=8.8,
            color='#b45309', ha='center', va='center', zorder=4)

    # =========================================================================
    # หัวใจสำคัญ: ลูกศร Work-Stealing (การขโมยงานจาก LRQ 0 -> LRQ 1)
    # =========================================================================
    # ลูกศรชี้จากการขโมยงาน โค้งด้านล่างเข้าสู่คิวว่างของ P 1
    stealing_arrow = FancyArrowPatch(
        (7.8, 3.0), (10.15, 3.4),
        connectionstyle="arc3,rad=-0.25",
        arrowstyle="->,head_width=6,head_length=8",
        color='#9333ea', lw=2.8, zorder=6
    )
    ax.add_patch(stealing_arrow)

    # ป้ายข้อความไฮไลต์บนลูกศรขโมยงาน
    steal_badge = FancyBboxPatch(
        (7.4, 2.05), 4.2, 0.72,
        boxstyle="round,pad=0.03,rounding_size=0.08",
        facecolor='#faf5ff',
        edgecolor='#a855f7',
        linewidth=1.5,
        zorder=7
    )
    ax.add_patch(steal_badge)
    ax.text(9.5, 2.52, ">> ขโมยงาน (Work Stealing) <<", fontsize=10.5, fontweight='bold',
            color='#6b21a8', ha='center', va='center', zorder=8)
    ax.text(9.5, 2.22, "P 1 สแกนพบว่าคิวว่าง จึงขโมยงานครึ่งหนึ่ง (G 2, G 3) มาทำต่อทันที!",
            fontsize=8.8, fontweight='bold', color='#7e22ce', ha='center', va='center', zorder=8)

    # =========================================================================
    # กล่องสรุปนิยามสถาปัตยกรรม 3 ตัวอักษร (M-P-G Framework Summary: y = 0.85 ถึง 1.8)
    # =========================================================================
    summary_card = FancyBboxPatch(
        (0.75, 0.88), 13.7, 0.95,
        boxstyle="round,pad=0.03,rounding_size=0.08",
        facecolor='#f8fafc',
        edgecolor='#cbd5e1',
        linewidth=1.0,
        zorder=3
    )
    ax.add_patch(summary_card)
    
    ax.text(1.0, 1.62, "สรุปแบบจำลอง M-P-G ใน Go Runtime Scheduler:", fontsize=10, fontweight='bold', color='#1e293b')
    ax.text(1.0, 1.34, "• G (Goroutine): หน่วยประมวลผลขนาดเริ่มต้น 2 KB มี Stack และ Program Counter เป็นของตนเอง", fontsize=8.8, color='#334155')
    ax.text(1.0, 1.14, "• M (Machine): OS Kernel Thread จริง ทำหน้าที่ดึงรหัสคำสั่งไปประมวลผลบนคอร์ของฮาร์ดแวร์ซีพียู", fontsize=8.8, color='#334155')
    ax.text(1.0, 0.94, "• P (Processor): บริบทตรรกะ (Logical Context) ตามจำนวนคอร์ CPU (GOMAXPROCS) ถือครองคิวงานท้องถิ่น (Local Runqueue)", fontsize=8.8, color='#334155')
    
    # ข้อดีของการขโมยงาน
    ax.text(14.2, 1.48, "ข้อได้เปรียบของการขโมยงาน:", fontsize=9.2, fontweight='bold', color='#0284c7', ha='right')
    ax.text(14.2, 1.25, "1. ลดการล็อก: คิวงานแยกอิสระ (Lock-Free)", fontsize=8.5, color='#0369a1', ha='right')
    ax.text(14.2, 1.05, "2. โหลดบาลานซ์อัตโนมัติ: ซีพียูทำงานเต็ม 100%", fontsize=8.5, color='#0369a1', ha='right')

    # =========================================================================
    # คำบรรยายใต้ภาพ (Caption below card: y = 0.28)
    # =========================================================================
    caption = "รูปที่ 9.2 สถาปัตยกรรม Go M-P-G Work-Stealing Scheduler"
    ax.text(7.6, 0.32, caption, fontsize=12, fontweight='bold', color='#1e293b', ha='center', va='center')

    # บันทึกไฟล์ภาพ
    out_path = os.path.abspath("figure_9_2_work_stealing.png")
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Figure 9.2 generated successfully: {out_path}")

if __name__ == "__main__":
    create_figure()
