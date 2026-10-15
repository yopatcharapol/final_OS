#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_figure_10_2.py
สร้างรูปภาพ รูปที่ 10.2 สำหรับรายงานวิชา OS
แผนผังการตัดสินใจเลือกใช้แบบจำลองภาวะพร้อมกัน (Concurrency Model Decision Flowchart)
(ปรับปรุงระบบพิกัดใหม่หมดจด: เส้นโยงสมมาตร กว้างขวาง สะอาดตา ไร้การทับซ้อน 100%)
"""

import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, FancyArrowPatch
from matplotlib import rcParams

# ตั้งค่าฟอนต์
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Leelawadee UI', 'Tahoma', 'TH Sarabun New', 'Arial']
rcParams['axes.unicode_minus'] = False

def create_figure():
    fig = plt.figure(figsize=(15.8, 11.8), dpi=300, facecolor='#ffffff')
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 15.8)
    ax.set_ylim(0, 11.8)
    ax.axis('off')

    # 1. กรอบพื้นหลังการ์ดใหญ่ (Main Container Card)
    card = FancyBboxPatch(
        (0.4, 0.4), 15.0, 11.0,
        boxstyle="round,pad=0.08,rounding_size=0.25",
        facecolor='#fbfcfd',
        edgecolor='#cbd5e1',
        linewidth=1.6,
        zorder=1
    )
    ax.add_patch(card)

    # หัวข้อใหญ่ด้านบน
    ax.text(0.8, 10.95, "รูปที่ 10.2 แผนผังการตัดสินใจเลือกใช้แบบจำลองภาวะพร้อมกัน (Concurrency Model Decision Flowchart)",
            fontsize=13.6, fontweight='bold', color='#0f172a', va='center')
    ax.text(0.8, 10.62, "กรอบแนวทางเชิงวิศวกรรมสำหรับเลือกสถาปัตยกรรม (Multiprocessing vs Thread Pool vs Lightweight M:N Threads)",
            fontsize=9.8, color='#64748b', va='center')
    ax.plot([0.8, 15.0], [10.40, 10.40], color='#e2e8f0', lw=1.2, zorder=2)

    # -------------------------------------------------------------------------
    # Helper Functions
    # -------------------------------------------------------------------------
    def draw_diamond(cx, cy, w, h, title, subtitle):
        pts = [
            [cx, cy + h/2],
            [cx + w/2, cy],
            [cx, cy - h/2],
            [cx - w/2, cy]
        ]
        diamond = Polygon(pts, closed=True, facecolor='#eff6ff', edgecolor='#2563eb',
                          linewidth=1.8, zorder=3)
        ax.add_patch(diamond)
        ax.text(cx, cy + 0.16, title, fontsize=9.8, fontweight='bold',
                color='#1e3a8a', ha='center', va='center', zorder=4)
        if subtitle:
            ax.text(cx, cy - 0.20, subtitle, fontsize=8.4, color='#3b82f6',
                    ha='center', va='center', zorder=4)

    def draw_badge(x, y, text, color, bg):
        badge = FancyBboxPatch(
            (x - 0.65, y - 0.20), 1.3, 0.40,
            boxstyle="round,pad=0.03,rounding_size=0.08",
            facecolor=bg, edgecolor=color, linewidth=1.2, zorder=6
        )
        ax.add_patch(badge)
        ax.text(x, y, text, fontsize=8.2, fontweight='bold', color=color,
                ha='center', va='center', zorder=7)

    def draw_arrow(p1, p2, color='#475569'):
        arrow = FancyArrowPatch(
            p1, p2,
            arrowstyle="Simple,head_width=8,head_length=9,tail_width=2.4",
            color=color, zorder=4
        )
        ax.add_patch(arrow)

    def draw_card(x, y, w, h, tag, title, bullets, theme_color, bg_color):
        box = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.06,rounding_size=0.16",
            facecolor=bg_color,
            edgecolor=theme_color,
            linewidth=1.8,
            zorder=3
        )
        ax.add_patch(box)
        
        # Tag header
        ax.text(x + w/2, y + h - 0.32, tag, fontsize=8.4, fontweight='bold',
                color=theme_color, ha='center', va='center', zorder=4)
        # Title
        ax.text(x + w/2, y + h - 0.65, title, fontsize=10.2, fontweight='bold',
                color='#0f172a', ha='center', va='center', zorder=4)
        ax.plot([x + 0.25, x + w - 0.25], [y + h - 0.88, y + h - 0.88],
                color=theme_color, lw=1.0, alpha=0.4, zorder=4)
        
        # Bullets
        start_y = y + h - 1.18
        for i, text in enumerate(bullets):
            ax.text(x + 0.22, start_y - (i * 0.32), f"• {text}", fontsize=8.4,
                    color='#334155', ha='left', va='center', zorder=4)

    # -------------------------------------------------------------------------
    # ระดับ 1: จุดเริ่มต้น (Start Pill: cy = 9.95)
    # -------------------------------------------------------------------------
    start_pill = FancyBboxPatch(
        (5.7, 9.67), 4.4, 0.56,
        boxstyle="round,pad=0.05,rounding_size=0.28",
        facecolor='#f8fafc', edgecolor='#334155', linewidth=1.8, zorder=3
    )
    ax.add_patch(start_pill)
    ax.text(7.9, 9.95, "จุดเริ่มต้น: วิเคราะห์สถาปัตยกรรมระบบ", fontsize=10.8,
            fontweight='bold', color='#0f172a', ha='center', va='center', zorder=4)

    # เส้นลงมาหา Decision 1
    draw_arrow((7.9, 9.67), (7.9, 9.05))

    # -------------------------------------------------------------------------
    # ระดับ 2: Decision 1 (Fault Isolation) -> cy = 8.35
    # -------------------------------------------------------------------------
    draw_diamond(
        cx=7.9, cy=8.35, w=4.8, h=1.40,
        title="ต้องการ Fault Isolation สูงสุด?",
        subtitle="หรือแยก Address Space & สิทธิ์เด็ดขาด?"
    )

    # สาขา 1 (ใช่ / YES): วิ่งซ้ายออกไปที่ x = 2.25 แล้วดิ่งลง Card 1
    ax.plot([5.50, 2.25], [8.35, 8.35], color='#dc2626', lw=2.2, zorder=4)
    draw_arrow((2.25, 8.35), (2.25, 3.42), color='#dc2626')
    draw_badge(3.85, 8.65, "ใช่ (YES)", '#dc2626', '#fee2e2')

    # สาขา 2 (ไม่ใช่ / NO): ดิ่งลงตรงๆ เข้าหา Decision 2
    draw_arrow((7.9, 7.65), (7.9, 7.15), color='#2563eb')
    draw_badge(8.75, 7.40, "ไม่ใช่ (NO)", '#2563eb', '#dbeafe')

    # -------------------------------------------------------------------------
    # ระดับ 3: Decision 2 (Workload Type: CPU vs I/O) -> cy = 6.45
    # -------------------------------------------------------------------------
    draw_diamond(
        cx=7.9, cy=6.45, w=3.8, h=1.40,
        title="ลักษณะภาระงานหลัก (Workload)?",
        subtitle="CPU-Bound หรือ I/O-Bound"
    )

    # สาขา 2A (CPU-Bound): วิ่งซ้ายออกไปที่ x = 5.85 แล้วดิ่งลง Card 2
    ax.plot([6.00, 5.85], [6.45, 6.45], color='#d97706', lw=2.2, zorder=4)
    draw_arrow((5.85, 6.45), (5.85, 3.42), color='#d97706')
    draw_badge(5.05, 6.75, "CPU-Bound", '#d97706', '#fef3c7')

    # สาขา 2B (I/O-Bound): วิ่งขวาออกไปที่ x = 11.75 แล้วดิ่งลงเข้าหา Decision 3
    ax.plot([9.80, 11.75], [6.45, 6.45], color='#7c3aed', lw=2.2, zorder=4)
    draw_arrow((11.75, 6.45), (11.75, 5.45), color='#7c3aed')
    draw_badge(10.75, 6.75, "I/O-Bound", '#7c3aed', '#f3e8ff')

    # -------------------------------------------------------------------------
    # ระดับ 4: Decision 3 (High Concurrency / C10K) -> cy = 4.75
    # -------------------------------------------------------------------------
    draw_diamond(
        cx=11.75, cy=4.75, w=3.4, h=1.40,
        title="รองรับ Concurrency สูง?",
        subtitle="พร้อมกันเกิน 10,000 ต่อวินาที (C10K)?"
    )

    # สาขา 3A (ไม่ใช่ / NO): วิ่งซ้ายออกไปที่ x = 9.95 แล้วดิ่งลง Card 3
    ax.plot([10.05, 9.95], [4.75, 4.75], color='#0284c7', lw=2.2, zorder=4)
    draw_arrow((9.95, 4.75), (9.95, 3.42), color='#0284c7')
    draw_badge(9.15, 5.05, "ไม่ใช่ (NO)", '#0284c7', '#e0f2fe')

    # สาขา 3B (ใช่ / YES): วิ่งขวาออกไปที่ x = 13.55 แล้วดิ่งลง Card 4
    ax.plot([13.45, 13.55], [4.75, 4.75], color='#16a34a', lw=2.2, zorder=4)
    draw_arrow((13.55, 4.75), (13.55, 3.42), color='#16a34a')
    draw_badge(14.35, 5.05, "ใช่ (YES)", '#16a34a', '#dcfce7')

    # -------------------------------------------------------------------------
    # ระดับล่างสุด: 4 การ์ดผลลัพธ์ เรียงสวยงาม 4 คอลัมน์ ไร้การทับซ้อน
    # ความสูง h = 2.75, ช่วง y = [0.60, 3.35]
    # -------------------------------------------------------------------------
    card_w = 3.25
    card_h = 2.75
    card_y = 0.60

    # Card 1: Multiprocessing (x = 0.65, center = 2.275)
    draw_card(
        x=0.65, y=card_y, w=card_w, h=card_h,
        tag="ทางเลือกที่ 1 : SEPARATE PROCESS",
        title="Multiprocessing Architecture",
        bullets=[
            "Chrome Model (Process-per-tab)",
            "แยกพื้นที่ Address Space เด็ดขาด",
            "หากแท็บใดแครช จะไม่กระทบแท็บอื่น",
            "สื่อสารข้ามโปรเซสผ่าน IPC",
            "ใช้แรมสูง (20 - 50 MB / แท็บ)"
        ],
        theme_color="#dc2626", bg_color="#fff1f2"
    )

    # Card 2: Fixed OS Thread Pool (x = 4.25, center = 5.875)
    draw_card(
        x=4.25, y=card_y, w=card_w, h=card_h,
        tag="ทางเลือกที่ 2 : CPU-BOUND WORKER",
        title="Fixed OS Thread Pool (1:1)",
        bullets=[
            "งานปั่นคำนวณหนัก (Render, ML, Math)",
            "จำกัด Threads = Physical Cores",
            "ป้องกัน Over-subscription เด็ดขาด",
            "ขจัด Involuntary Context Switch",
            "ตัวอย่าง: Rayon (Rust), OpenMP"
        ],
        theme_color="#d97706", bg_color="#fffbeb"
    )

    # Card 3: Standard OS Thread Pool (x = 8.35, center = 9.975)
    draw_card(
        x=8.35, y=card_y, w=card_w, h=card_h,
        tag="ทางเลือกที่ 3 : MODERATE I/O POOL",
        title="Standard OS Thread Pool",
        bullets=[
            "งานเว็บเซอร์วิสทั่วไป (100 - 1,000 req)",
            "แรมพอรับขนาดสแตก 1 - 2 MB / เธรด",
            "เขียนโค้ด Synchronous Blocking ง่าย",
            "ไม่ต้องพึ่งพารันไทม์พิเศษเพิ่มเติม",
            "ตัวอย่าง: Apache Tomcat, Spring Boot"
        ],
        theme_color="#0284c7", bg_color="#f0f9ff"
    )

    # Card 4: Lightweight M:N Threads (x = 11.95, center = 13.575)
    draw_card(
        x=11.95, y=card_y, w=card_w, h=card_h,
        tag="ทางเลือกที่ 4 : HIGH CONCURRENCY",
        title="Lightweight M:N Threads",
        bullets=[
            "รองรับพร้อมกันนับล้านการเชื่อมต่อ (C10K)",
            "สแตกเริ่มต้นจิ๋วเพียง 2 KB ต่อเธรด",
            "Context Switch ใน User-space (~10 ns)",
            "Non-blocking I/O ผ่าน Event Loop",
            "ตัวอย่าง: Go Goroutines, Java Loom, Tokio"
        ],
        theme_color="#16a34a", bg_color="#f0fdf4"
    )

    # บันทึกไฟล์ภาพ
    output_path = os.path.join(os.path.dirname(__file__), "figure_10_2_decision_flowchart.png")
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"สร้างรูปภาพสำเร็จสมบูรณ์: {output_path}")

if __name__ == "__main__":
    create_figure()
