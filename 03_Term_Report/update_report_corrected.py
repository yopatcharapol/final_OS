#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
update_report_corrected.py
คัดลอก Report_Corrected_Condensed.docx ทับ Report_Corrected.docx ทันทีที่ผู้ใช้ปิดโปรแกรม Word
"""
import shutil
import time
import os

src = "Report_Corrected_Condensed.docx"
dst = "Report_Corrected.docx"

if not os.path.exists(src):
    print(f"Error: {src} not found.")
    exit(1)

success = False
for attempt in range(1, 6):
    try:
        shutil.copyfile(src, dst)
        print(f"[{attempt}] คัดลอก {src} ทับ {dst} สำเร็จสมบูรณ์!")
        success = True
        break
    except PermissionError:
        print(f"[{attempt}] ไฟล์ {dst} ยังคงถูกเปิดอยู่ใน Microsoft Word กำลังรอ 2 วินาที...")
        time.sleep(2)

if not success:
    print(f"\nคำแนะนำ: กรุณาปิดโปรแกรม Microsoft Word ที่เปิดไฟล์ {dst} แล้วรันสคริปต์นี้อีกครั้ง หรือเปิดใช้งานไฟล์ {src} ได้ทันที")
