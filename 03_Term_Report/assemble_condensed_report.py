#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
assemble_condensed_report.py
ประกอบเอกสาร Report_Corrected.docx ฉบับย่อบทที่ 6-10
และวัดผลจำนวนหน้าด้วย Microsoft Word COM อย่างแม่นยำ
"""

import os
import sys
import copy
import docx
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from build_condensed_chapters import (
    build_chapter_6, build_chapter_7, build_chapter_8,
    build_chapter_9, build_chapter_10
)
from condense_chapters_6_10 import setup_document_defaults

def assemble_report():
    input_docx = os.path.abspath("Report_Final.docx")
    output_docx = os.path.abspath("Report_Corrected_Condensed.docx")
    
    print(f"Loading {input_docx}...")
    doc = Document(input_docx)
    body = doc._body._element
    
    # 1. ค้นหาจุดตัด: บทที่ 6 เริ่มต้นที่ paragraph 388 (element 404)
    # และหน้าแบ่งก่อนเอกสารอ้างอิงอยู่ที่ element 779
    ch6_elm = doc.paragraphs[388]._element
    ref_elm = doc.paragraphs[741]._element
    
    elms = list(body)
    idx_ch6 = elms.index(ch6_elm)
    idx_ref = elms.index(ref_elm)
    
    # element ก่อน ref_elm ที่เป็น page break
    # เราจะแทนที่ตั้งแต่ idx_ch6 จนถึง idx_ref - 1 (เพราะ idx_ref-1 คือ page break ก่อนบรรณานุกรม)
    print(f"Original Ch6 element index: {idx_ch6}")
    print(f"Original Ref element index: {idx_ref}")
    
    # 2. สร้างเอกสารชั่วคราวสำหรับสร้างบทที่ 6-10
    temp_doc = Document()
    setup_document_defaults(temp_doc)
    
    # ดึง Elements ของบทที่ 9 และบทที่ 10 ฉบับเต็มจาก Report_Final.docx
    base_final = Document("Report_Final.docx")
    base_elms = list(base_final._body._element)
    idx_orig_ch9 = base_elms.index(base_final.paragraphs[652]._element)
    idx_orig_ref = base_elms.index(base_final.paragraphs[741]._element)
    # idx_orig_ref - 1 คือ page break ท้ายบทที่ 10 ก่อนขึ้นบรรณานุกรม
    ch9_10_orig_elements = base_elms[idx_orig_ch9:idx_orig_ref - 1]
    
    print("Building condensed chapters 6 to 8...")
    build_chapter_6(temp_doc)
    temp_doc.add_page_break()
    
    build_chapter_7(temp_doc)
    temp_doc.add_page_break()
    
    build_chapter_8(temp_doc)
    temp_doc.add_page_break()
    
    print("Restoring full original Chapter 9 and Chapter 10...")
    sectPr = temp_doc._body._element.xpath('./w:sectPr')[0]
    for e in ch9_10_orig_elements:
        sectPr.addprevious(copy.deepcopy(e))
    
    # 3. นำ elements จาก temp_doc เข้าไปแทนที่ใน doc
    temp_elms = list(temp_doc._body._element)
    new_elms = [e for e in temp_elms if not e.tag.endswith('sectPr')]
    print(f"Generated {len(new_elms)} new body elements for Chapters 6-10.")
    
    # แทรก elements ใหม่ไว้ก่อน element ที่ตำแหน่ง idx_ref - 1 (ซึ่งเป็น page break ก่อนบรรณานุกรม)
    insert_target = elms[idx_ref - 1] # page break ก่อนบรรณานุกรม
    for new_e in new_elms:
        insert_target.addprevious(copy.deepcopy(new_e))
        
    # ลบ elements เดิมของบทที่ 6-10 (ตั้งแต่ idx_ch6 ถึงก่อนหน้า insert_target)
    old_elms = elms[idx_ch6:idx_ref - 1]
    print(f"Removing {len(old_elms)} old body elements...")
    for old_e in old_elms:
        body.remove(old_e)
        
    # 4. แทนที่ตาราง ASCII Art รูปที่ 9.1 ด้วยรูปภาพจริง
    img_path = os.path.abspath("figure_9_1_stack_allocation.png")
    if os.path.exists(img_path):
        for t in doc.tables:
            txt = "".join(c.text for row in t.rows for c in row.cells)
            if "OS Thread Stack" in txt and "Goroutine" in txt:
                p_img = doc.add_paragraph()
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = p_img.add_run()
                run.add_picture(img_path, width=Inches(5.8))
                t._element.addprevious(p_img._element)
                doc._body._element.remove(t._element)
                print("Replaced ASCII Table with figure_9_1_stack_allocation.png successfully!")
    # 5. แทนที่ตาราง ASCII Art รูปที่ 9.2 ด้วยรูปภาพจริง
    img92_path = os.path.abspath("figure_9_2_work_stealing.png")
    if os.path.exists(img92_path):
        for t in doc.tables:
            txt = "".join(c.text for row in t.rows for c in row.cells)
            if "OS Thread: M 0" in txt and "Work Stealing" in txt:
                p_img = doc.add_paragraph()
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = p_img.add_run()
                run.add_picture(img92_path, width=Inches(5.8))
                t._element.addprevious(p_img._element)
                doc._body._element.remove(t._element)
                print("Replaced ASCII Table with figure_9_2_work_stealing.png successfully!")
                break

    # 6. แทนที่ตาราง ASCII Art รูปที่ 10.1 ด้วยรูปภาพจริง
    img101_path = os.path.abspath("figure_10_1_oversubscription.png")
    if os.path.exists(img101_path):
        for t in doc.tables:
            txt = "".join(c.text for row in t.rows for c in row.cells)
            if "Involuntary Context Switch" in txt and ("Pipeline" in txt or "Thrashing" in txt):
                p_img = doc.add_paragraph()
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = p_img.add_run()
                run.add_picture(img101_path, width=Inches(5.8))
                t._element.addprevious(p_img._element)
                doc._body._element.remove(t._element)
                print("Replaced ASCII Table with figure_10_1_oversubscription.png successfully!")
                break

    # 7. แทนที่ตาราง ASCII Art รูปที่ 10.2 ด้วยรูปภาพจริง
    img102_path = os.path.abspath("figure_10_2_decision_flowchart.png")
    if os.path.exists(img102_path):
        for t in doc.tables:
            txt = "".join(c.text for row in t.rows for c in row.cells)
            if "Fault Isolation" in txt and ("Multiprocessing" in txt or "Chrome Model" in txt or "Virtual Threads" in txt):
                p_img = doc.add_paragraph()
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = p_img.add_run()
                run.add_picture(img102_path, width=Inches(5.8))
                t._element.addprevious(p_img._element)
                doc._body._element.remove(t._element)
                print("Replaced ASCII Table with figure_10_2_decision_flowchart.png successfully!")
                break

    print(f"Saving to {output_docx}...")
    doc.save(output_docx)
    print("Saved successfully!")
    return output_docx

def measure_pages_with_word(docx_path):
    print("\nMeasuring pages with Microsoft Word COM...")
    import win32com.client
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    try:
        doc = word.Documents.Open(os.path.abspath(docx_path), ReadOnly=True, ConfirmConversions=False)
        doc.Repaginate()
        total_pages = doc.ComputeStatistics(2) # 2 = wdStatisticPages
        
        wdActiveEndPageNumber = 3
        ch_pages = {}
        for p in doc.Paragraphs:
            t = p.Range.Text.strip().replace('\u200b', '')
            for ch_num in range(1, 11):
                prefix = f"บทที่ {ch_num}:"
                if t.startswith(prefix) and f"บทที่ {ch_num}" not in ch_pages:
                    ch_pages[f"บทที่ {ch_num}"] = p.Range.Information(wdActiveEndPageNumber)
            if "เอกสารอ้างอิงและบรรณานุกรม" in t and "เอกสารอ้างอิง" not in ch_pages:
                ch_pages["เอกสารอ้างอิง"] = p.Range.Information(wdActiveEndPageNumber)
                
        doc.Close(False)
        return total_pages, ch_pages
    finally:
        word.Quit()

if __name__ == "__main__":
    out_file = assemble_report()
    total_pages, ch_pages = measure_pages_with_word(out_file)
    print("\n" + "="*50)
    print(f"TOTAL PAGES: {total_pages}")
    print("="*50)
    for k, v in ch_pages.items():
        print(f"  {k:15s} -> หน้า {v}")
    print("="*50)
    
    if "บทที่ 6" in ch_pages and "เอกสารอ้างอิง" in ch_pages:
        ch6_start = ch_pages["บทที่ 6"]
        ref_start = ch_pages["เอกสารอ้างอิง"]
        ch6_10_pages = ref_start - ch6_start
        print(f"จำนวนหน้ารวมของ บทที่ 6 - 10: {ch6_10_pages} หน้า (จากหน้า {ch6_start} ถึงหน้า {ref_start - 1})")
        if 25 <= ch6_10_pages <= 30:
            print(">>> สำเร็จสมบูรณ์! จำนวนหน้ารวมอยู่ในช่วง 25 - 30 หน้าตามเกณฑ์ที่กำหนด <<<")
        else:
            print(f">>> คำเตือน: จำนวนหน้าคือ {ch6_10_pages} (เป้าหมายคือ 25 - 30 หน้า) <<<")
