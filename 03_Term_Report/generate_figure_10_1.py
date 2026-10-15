#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_figure_10_1.py
สร้างรูปภาพ รูปที่ 10.1 สำหรับรายงานวิชา OS
วงจรการลดลงของประสิทธิภาพเมื่อเกิดภาวะจัดสรรเธรดเกินพิกัด (Over-subscription Retrograde Cycle)
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, ArrowStyle
from matplotlib import rcParams

# กำหนดฟอนต์ให้รองรับภาษาไทยสวยงาม คมชัด
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Leelawadee UI', 'Tahoma', 'TH Sarabun New', 'Arial']
rcParams['axes.unicode_minus'] = False

def create_figure():
    fig = plt.figure(figsize=(15.2, 9.4), dpi=300, facecolor='#ffffff')
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 15.2)
    ax.set_ylim(0, 9.4)
    ax.axis('off')

    # 1. กรอบการ์ดใหญ่พื้นหลัง (Card Container)
    card = FancyBboxPatch(
        (0.4, 0.45), 14.4, 8.5,
        boxstyle="round,pad=0.1,rounding_size=0.25",
        facecolor='#fbfcfd',
        edgecolor='#cbd5e1',
        linewidth=1.6,
        zorder=1
    )
    ax.add_patch(card)

    # หัวข้อใหญ่ด้านบนการ์ด
    ax.text(0.8, 8.45, "รูปที่ 10.1 วงจรการลดลงของประสิทธิภาพเมื่อเกิดภาวะจัดสรรเธรดเกินพิกัด (Over-subscription)",
            fontsize=13.8, fontweight='bold', color='#0f172a', va='center')
    ax.text(0.8, 8.12, "การวิเคราะห์กลไกระดับฮาร์ดแวร์และระบบปฏิบัติการที่ทำให้เกิดปรากฏการณ์ความเร็วถดถอย (Retrograde Scalability)",
            fontsize=10.2, color='#64748b', va='center')
    ax.plot([0.8, 14.4], [7.92, 7.92], color='#e2e8f0', lw=1.2, zorder=2)

    # =========================================================================
    # กล่องกลาง (Center Core Hub): สรุปแบบจำลอง USL
    # =========================================================================
    hub_card = FancyBboxPatch(
        (5.1, 3.2), 5.0, 2.6,
        boxstyle="round,pad=0.08,rounding_size=0.2",
        facecolor='#f8fafc',
        edgecolor='#94a3b8',
        linewidth=1.5,
        linestyle='--',
        zorder=3
    )
    ax.add_patch(hub_card)

    ax.text(7.6, 5.35, "แก่นแท้ของปัญหาทางวิศวกรรม", fontsize=11.5, fontweight='bold',
            color='#1e293b', ha='center', va='center', zorder=4)
    ax.text(7.6, 4.88, "Universal Scalability Law (USL)", fontsize=11.0, fontweight='bold',
            color='#2563eb', ha='center', va='center', zorder=4)
    ax.text(7.6, 4.45, "C(N) = N / [ 1 + alpha·(N - 1) + beta·N(N - 1) ]", fontsize=10.2,
            fontfamily='monospace', fontweight='bold', color='#0f172a', ha='center', va='center', zorder=4)
    ax.text(7.6, 3.98, "เมื่อ N > 12: พจน์ Coherency Penalty (Beta)", fontsize=9.8,
            fontweight='bold', color='#dc2626', ha='center', va='center', zorder=4)
    ax.text(7.6, 3.60, "ส่งผลให้กราฟเกิด 'จุดหักเห' (Peak Inflection Point)\nกลายเป็นความเร็วถดถอย (Retrograde Scalability)",
            fontsize=9.0, color='#475569', ha='center', va='center', linespacing=1.2, zorder=4)

    # =========================================================================
    # ฟังก์ชันวาดโหนดแต่ละขั้นตอนในวงจร
    # =========================================================================
    def draw_node(x, y, w, h, title, subtitle, bullets, theme_color, bg_color, step_num):
        # กรอบโหนด
        node_box = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.06,rounding_size=0.18",
            facecolor=bg_color,
            edgecolor=theme_color,
            linewidth=1.8,
            zorder=3
        )
        ax.add_patch(node_box)

        # แถบสเต็ปเลข
        badge = Circle((x + 0.32, y + h - 0.35), 0.24, facecolor=theme_color, edgecolor='none', zorder=4)
        ax.add_patch(badge)
        ax.text(x + 0.32, y + h - 0.35, str(step_num), fontsize=10.5, fontweight='bold',
                color='#ffffff', ha='center', va='center', zorder=5)

        # หัวข้อ
        ax.text(x + 0.68, y + h - 0.25, title, fontsize=11.0, fontweight='bold',
                color=theme_color, ha='left', va='center', zorder=4)
        ax.text(x + 0.68, y + h - 0.52, subtitle, fontsize=8.8, fontweight='bold',
                color='#64748b', ha='left', va='center', zorder=4)

        # รายละเอียดในโหนด
        start_y = y + h - 0.85
        for i, text in enumerate(bullets):
            ax.text(x + 0.22, start_y - (i * 0.32), f"• {text}", fontsize=8.6,
                    color='#334155', ha='left', va='center', zorder=4)

    # =========================================================================
    # กำหนดโหนด 5 จุด วนรอบสี่เหลี่ยมตามเข็มนาฬิกา
    # =========================================================================
    # โหนด 1: บนซ้าย
    draw_node(
        x=0.9, y=5.5, w=4.2, h=2.1,
        title="เพิ่มเธรดเกินขนาดพิกัด",
        subtitle="(Over-subscription Trigger)",
        bullets=[
            "จำนวนเธรด (16) มากกว่าจำนวนคอร์กายภาพ (12)",
            "Run-Queue แน่นขนัด เธรดแย่งเวลา CPU",
            "เกิด Time-slice Starvation ทั่วระบบ"
        ],
        theme_color="#e11d48", bg_color="#fff1f2", step_num=1
    )

    # โหนด 2: บนขวา
    draw_node(
        x=10.1, y=5.5, w=4.2, h=2.1,
        title="Involuntary Context Switch พุ่งสูง",
        subtitle="(Kernel Preemption Storm)",
        bullets=[
            "Context Switch พุ่งก้าวกระโดดจาก 12 สู่ 4,210 ครั้ง",
            "เคอร์เนลต้องบังคับสลับเธรดบ่อยครั้งเมื่อหมดโควตา",
            "เสียเวลาบันทึก PCB และสลับ Stack Register มหาศาล"
        ],
        theme_color="#d97706", bg_color="#fffbeb", step_num=2
    )

    # โหนด 3: ขวาล่าง
    draw_node(
        x=10.1, y=1.2, w=4.2, h=2.1,
        title="Cache Thrashing ใน L3 / เมมโมรี",
        subtitle="(Cache Invalidation & Bus Storm)",
        bullets=[
            "แคช L1/L2 และ L3 ถูกเบียดทิ้ง (Cache Pollution)",
            "เกิด Bus Invalidation Storm แย่งสิทธิ์เขียน Cache Line",
            "ฮาร์ดแวร์เสียเวลารอข้อมูลใหม่จาก DRAM ช้าลง 100 เท่า"
        ],
        theme_color="#7c3aed", bg_color="#faf5ff", step_num=3
    )

    # โหนด 4: กลางล่าง
    draw_node(
        x=5.5, y=0.85, w=4.2, h=2.0,
        title="Pipeline ว่างเปล่า (IPC ตกต่ำ)",
        subtitle="(CPU Pipeline Stalls & Low Throughput)",
        bullets=[
            "คำสั่งต่อสัญญาณนาฬิกา (IPC) ลดฮวบอย่างรุนแรง",
            "ซีพียูเกิด Memory Stall ฟองสบู่ค้างใน Pipeline",
            "การคำนวณจริงสะดุดหยุดรอข้อมูลจากบัส"
        ],
        theme_color="#2563eb", bg_color="#eff6ff", step_num=4
    )

    # โหนด 5: ล่างซ้าย
    draw_node(
        x=0.9, y=1.2, w=4.2, h=2.1,
        title="ระบบช้าลงกว่าเดิมอย่างมาก",
        subtitle="(Negative Scalability / Retrograde)",
        bullets=[
            "เวลาเฉลี่ยพุ่งเป็น 0.513 วินาที (ช้ากว่าตอนใช้ 12 เธรด)",
            "ประสิทธิภาพถดถอยจนแย่กว่า Single-Thread ในบางงาน",
            "ยิ่งส่งเธรดเข้ามาอัด ยิ่งทำให้เครื่องทำงานช้าลง"
        ],
        theme_color="#dc2626", bg_color="#fef2f2", step_num=5
    )

    # =========================================================================
    # ลูกศรเชื่อมโยงการไหล (Cyclic Flow Arrows)
    # =========================================================================
    arrow_style = ArrowStyle("Simple,head_width=9,head_length=11,tail_width=3.2")

    # ลูกศร 1 -> 2 (บนซ้าย ไป บนขวา)
    a1 = FancyArrowPatch((5.15, 6.55), (10.05, 6.55), arrowstyle=arrow_style,
                         color='#e11d48', zorder=5)
    ax.add_patch(a1)
    ax.text(7.6, 6.85, "เคอร์เนลตัดตอนเธรดบ่อยขึ้น", fontsize=9.2, fontweight='bold',
            color='#be123c', ha='center', va='center')

    # ลูกศร 2 -> 3 (บนขวา ลง ขวาล่าง)
    a2 = FancyArrowPatch((12.2, 5.45), (12.2, 3.35), arrowstyle=arrow_style,
                         color='#d97706', zorder=5)
    ax.add_patch(a2)
    ax.text(12.35, 4.4, " สลับเธรดบ่อย\n แคชถูกล้างซ้ำซาก", fontsize=9.2, fontweight='bold',
            color='#b45309', ha='left', va='center', linespacing=1.2)

    # ลูกศร 3 -> 4 (ขวาล่าง ไป กลางล่าง)
    a3 = FancyArrowPatch((10.05, 2.1), (9.75, 1.95), arrowstyle=arrow_style,
                         color='#7c3aed', zorder=5)
    ax.add_patch(a3)

    # ลูกศร 4 -> 5 (กลางล่าง ไป ล่างซ้าย)
    a4 = FancyArrowPatch((5.45, 1.95), (5.15, 2.1), arrowstyle=arrow_style,
                         color='#2563eb', zorder=5)
    ax.add_patch(a4)

    # ลูกศร 5 -> 1 (ล่างซ้าย วนขึ้น บนซ้าย: ปิดวงจรอุบาทว์ Vicious Cycle)
    a5 = FancyArrowPatch((3.0, 3.35), (3.0, 5.45), arrowstyle=arrow_style,
                         color='#dc2626', zorder=5)
    ax.add_patch(a5)
    ax.text(2.85, 4.4, "วงจรอุบาทว์\n(Vicious Cycle) ", fontsize=9.5, fontweight='bold',
            color='#991b1b', ha='right', va='center', linespacing=1.2)

    # บันทึกไฟล์ภาพ
    output_path = os.path.join(os.path.dirname(__file__), "figure_10_1_oversubscription.png")
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"สร้างรูปภาพสำเร็จ: {output_path}")

if __name__ == "__main__":
    create_figure()
