#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_figure_9_1.py
สร้างรูปภาพ รูปที่ 9.1 สำหรับรายงานวิชา OS
เปรียบเทียบขนาดหน่วยความจำเริ่มต้นระหว่างเคอร์เนลเธรดกับ Goroutine
และแสดงกลไก Dynamic Contiguous Stack Allocation
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle, ArrowStyle, FancyArrowPatch
from matplotlib import rcParams

# กำหนดฟอนต์ให้รองรับภาษาไทยสวยงาม
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Leelawadee UI', 'Tahoma', 'TH Sarabun New', 'Arial']
rcParams['axes.unicode_minus'] = False

def create_figure():
    fig = plt.figure(figsize=(15, 8.2), dpi=300, facecolor='#ffffff')
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 8.2)
    ax.axis('off')

    # 1. กรอบการ์ดใหญ่พื้นหลัง (Card Container)
    card = FancyBboxPatch(
        (0.35, 0.65), 14.3, 7.15,
        boxstyle="round,pad=0.1,rounding_size=0.25",
        facecolor='#fbfcfd',
        edgecolor='#cbd5e1',
        linewidth=1.5,
        zorder=1
    )
    ax.add_patch(card)

    # =========================================================================
    # ส่วนที่ 1: การเปรียบเทียบขนาดสแตกเริ่มต้น (Top Section: y = 4.7 ถึง 7.4)
    # =========================================================================
    # หัวข้อส่วนที่ 1
    ax.text(0.7, 7.35, "ส่วนที่ 1: การเปรียบเทียบขนาดสแตกเริ่มต้น (Initial Stack Footprint Comparison)",
            fontsize=13.5, fontweight='bold', color='#1e293b', va='center')
    ax.plot([0.7, 14.3], [7.12, 7.12], color='#e2e8f0', lw=1.2, zorder=2)

    # 1.1 OS Kernel Thread
    ax.text(0.7, 6.55, "OS Kernel Thread\n(Linux / Windows)", fontsize=11.5, fontweight='bold',
            color='#991b1b', va='center', ha='left', linespacing=1.2)
    
    # บาร์แสดงสแตกของ OS Thread (ขนาดยาวมาก 1,024 - 2,048 KB)
    os_bar = FancyBboxPatch(
        (3.3, 6.22), 10.8, 0.68,
        boxstyle="round,pad=0.03,rounding_size=0.08",
        facecolor='#fee2e2',
        edgecolor='#dc2626',
        linewidth=1.8,
        zorder=3
    )
    ax.add_patch(os_bar)
    ax.text(8.7, 6.56, "1,024 KB ถึง 2,048 KB (1 – 2 MB Fixed Virtual Memory Reservation)",
            fontsize=11.5, fontweight='bold', color='#991b1b', va='center', ha='center', zorder=4)
    
    # คำอธิบายย่อยของ OS Thread
    ax.text(3.35, 5.96, "• ขนาดคงที่ตายตัว (Fixed Stack) ไม่ว่าจะรันฟังก์ชันสั้นเพียงใดก็ตาม | 10,000 เธรด กินแรมขั้นต่ำ 10 – 20 GB (C10K Problem)",
            fontsize=9.8, color='#64748b', va='center')

    # 1.2 Go Goroutine
    ax.text(0.7, 5.25, "Go Goroutine\n(User-Space)", fontsize=11.5, fontweight='bold',
            color='#0e7490', va='center', ha='left', linespacing=1.2)
    
    # บาร์แสดงสแตกของ Goroutine (ขนาดจิ๋วเริ่มต้น 2 KB)
    go_bar = FancyBboxPatch(
        (3.3, 4.95), 0.9, 0.62,
        boxstyle="round,pad=0.03,rounding_size=0.08",
        facecolor='#cffafe',
        edgecolor='#0891b2',
        linewidth=1.8,
        zorder=3
    )
    ax.add_patch(go_bar)
    ax.text(3.75, 5.26, "2 KB", fontsize=11, fontweight='bold', color='#0e7490', va='center', ha='center', zorder=4)

    # วงเล็บปีกกา/เส้นชี้เปรียบเทียบอัตราส่วน
    arrow_ratio = FancyArrowPatch((4.3, 5.26), (5.1, 5.26),
                                  arrowstyle="->,head_width=3,head_length=5",
                                  color='#0891b2', lw=1.5, zorder=3)
    ax.add_patch(arrow_ratio)
    
    # กล่องไฮไลต์ข้อดีของ Goroutine
    highlight_box = FancyBboxPatch(
        (5.2, 4.95), 8.9, 0.62,
        boxstyle="round,pad=0.05,rounding_size=0.08",
        facecolor='#ecfeff',
        edgecolor='#a5f3fc',
        linewidth=1.2,
        zorder=3
    )
    ax.add_patch(highlight_box)
    ax.text(5.4, 5.37, "ขนาดเริ่มต้นเพียง 2 KB (เล็กกว่า OS Thread ประมาณ 500 – 1,000 เท่า)",
            fontsize=10.5, fontweight='bold', color='#0e7490', va='center')
    ax.text(5.4, 5.12, "ทำให้สามารถสร้าง 1,000,000 Goroutines พร้อมกันโดยใช้แรมเริ่มต้นเพียง ~2 GB (แก้ปัญหา C1000K สำเร็จ)",
            fontsize=9.8, color='#0891b2', va='center')

    # =========================================================================
    # ส่วนที่ 2: กลไก Dynamic Contiguous Stack Allocation (Bottom Section: y = 1.0 ถึง 4.5)
    # =========================================================================
    ax.text(0.7, 4.38, "ส่วนที่ 2: กลไกการขยายตัวแบบต่อเนื่อง (Dynamic Contiguous Stack Allocation)",
            fontsize=13.5, fontweight='bold', color='#1e293b', va='center')
    ax.plot([0.7, 14.3], [4.15, 4.15], color='#e2e8f0', lw=1.2, zorder=2)

    # ขั้นตอน 4 กล่อง (Pipeline Step Boxes)
    box_w = 2.75
    box_h = 2.45
    y_box = 1.35
    
    steps = [
        {
            "x": 0.75,
            "num": "ขั้นที่ 1",
            "title": "เริ่มต้นขนาดจิ๋ว (2 KB)",
            "header_color": "#0284c7",
            "bg_color": "#f0f9ff",
            "border_color": "#bae6fd",
            "stack_h": 0.5,
            "stack_txt": "Stack: 2 KB",
            "desc": "เมื่อ Goroutine ถูกสร้างขึ้น\nระบบจัดสรรสแตกเริ่มต้น 2 KB\nเพียงพอสำหรับรันฟังก์ชันขนาดเล็ก"
        },
        {
            "x": 4.25,
            "num": "ขั้นที่ 2",
            "title": "สแตกเต็ม (Stack Overflow)",
            "header_color": "#d97706",
            "bg_color": "#fffbeb",
            "border_color": "#fde68a",
            "stack_h": 0.9,
            "stack_txt": "Stack: 2 KB (เต็ม!)",
            "desc": "Function Prologue ตรวจพบว่า\nพื้นที่เหลือไม่พอเรียกฟังก์ชันถัดไป\nจึงส่งสัญญาณแจ้ง Go Runtime"
        },
        {
            "x": 7.75,
            "num": "ขั้นที่ 3",
            "title": "จัดสรรขนาด 2x & ย้ายข้อมูล",
            "header_color": "#059669",
            "bg_color": "#f0fdf4",
            "border_color": "#bbf7d0",
            "stack_h": 1.3,
            "stack_txt": "Stack ใหม่: 4 KB / 8 KB",
            "desc": "Runtime จองหน่วยความจำก้อนใหม่ 4 KB\nคัดลอกข้อมูลเดิมไปวางอย่างต่อเนื่อง\nและอัปเดต Pointers ไร้รอยต่อ"
        },
        {
            "x": 11.25,
            "num": "ขั้นที่ 4",
            "title": "หดขนาดกลับอัตโนมัติ",
            "header_color": "#4f46e5",
            "bg_color": "#eef2ff",
            "border_color": "#c7d2fe",
            "stack_h": 0.6,
            "stack_txt": "หดกลับเหลือ 2 KB",
            "desc": "เมื่อฟังก์ชัน Return คืนค่ากลับ\nตัว GC / Runtime จะหดขนาดสแตก\nเพื่อคืนแรมที่ไม่ได้ใช้สู่ระบบ"
        }
    ]

    for s in steps:
        bx = s["x"]
        # กล่องหลัก
        box = FancyBboxPatch(
            (bx, y_box), box_w, box_h,
            boxstyle="round,pad=0.04,rounding_size=0.12",
            facecolor=s["bg_color"],
            edgecolor=s["border_color"],
            linewidth=1.4,
            zorder=3
        )
        ax.add_patch(box)
        
        # หัวข้อกล่อง
        ax.text(bx + box_w/2, y_box + box_h - 0.25, f"{s['num']}: {s['title']}",
                fontsize=10.5, fontweight='bold', color=s["header_color"],
                ha='center', va='center', zorder=4)
        
        # เส้นคั่นหัวกล่อง
        ax.plot([bx + 0.15, bx + box_w - 0.15], [y_box + box_h - 0.45, y_box + box_h - 0.45],
                color=s["border_color"], lw=1.0, zorder=4)
        
        # รูปจำลอง Stack ภายในกล่อง
        stack_patch = FancyBboxPatch(
            (bx + 0.35, y_box + 1.15), box_w - 0.7, s["stack_h"] * 0.45,
            boxstyle="round,pad=0.02,rounding_size=0.05",
            facecolor='#ffffff',
            edgecolor=s["header_color"],
            linewidth=1.2,
            zorder=4
        )
        ax.add_patch(stack_patch)
        ax.text(bx + box_w/2, y_box + 1.15 + (s["stack_h"] * 0.45)/2, s["stack_txt"],
                fontsize=9.5, fontweight='bold', color=s["header_color"],
                ha='center', va='center', zorder=5)

        # ข้อความอธิบายด้านล่างกล่อง
        ax.text(bx + box_w/2, y_box + 0.55, s["desc"],
                fontsize=8.8, color='#334155', ha='center', va='center',
                linespacing=1.3, zorder=4)

    # ลูกศรเชื่อมระหว่างกล่องขั้นที่ 1 -> 2 -> 3
    for i in range(2):
        x_start = steps[i]["x"] + box_w + 0.08
        x_end = steps[i+1]["x"] - 0.08
        y_mid = y_box + box_h / 2
        arrow = FancyArrowPatch(
            (x_start, y_mid), (x_end, y_mid),
            arrowstyle="->,head_width=4,head_length=6",
            color='#64748b', lw=2.0, zorder=5
        )
        ax.add_patch(arrow)

    # ลูกศรขั้นที่ 3 -> 4 (เป็นเส้นประ แสดงการหดกลับเมื่อฟังก์ชัน return)
    arrow_return = FancyArrowPatch(
        (steps[2]["x"] + box_w + 0.08, y_box + box_h / 2),
        (steps[3]["x"] - 0.08, y_box + box_h / 2),
        arrowstyle="->,head_width=4,head_length=6",
        linestyle="--",
        color='#4f46e5', lw=2.0, zorder=5
    )
    ax.add_patch(arrow_return)
    ax.text(10.87, y_box + box_h / 2 + 0.22, "Return", fontsize=8.8,
            fontweight='bold', color='#4f46e5', ha='center', va='center')

    # =========================================================================
    # คำบรรยายใต้ภาพ (Caption below card: y = 0.25)
    # =========================================================================
    caption = "รูปที่ 9.1 การเปรียบเทียบขนาดหน่วยความจำเริ่มต้นระหว่างเคอร์เนลเธรดกับ Goroutine และกลไก Dynamic Contiguous Stack Allocation"
    ax.text(7.5, 0.28, caption, fontsize=12, fontweight='bold', color='#1e293b', ha='center', va='center')

    # บันทึกไฟล์ภาพ
    out_path = os.path.abspath("figure_9_1_stack_allocation.png")
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Figure 9.1 generated successfully: {out_path}")

if __name__ == "__main__":
    create_figure()
