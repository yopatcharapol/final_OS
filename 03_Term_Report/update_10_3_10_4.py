import docx
import os

condensed_text = [
    # 10.3
    ("10.3 ข้อจำกัดของการศึกษาและการทดลอง (Limitations of the Study)", "Heading 2"),
    ("เพื่อความโปร่งใสทางวิชาการ รายงานฉบับนี้มีข้อพึงระวังและข้อจำกัดทางสภาพแวดล้อม 3 ประการ:", "Normal"),
    ("1. สถาปัตยกรรมฮาร์ดแวร์ทดสอบ: ใช้ซีพียู Intel Core i7-12700H (สถาปัตยกรรมไฮบริด P/E-Core, หน่วยความจำ SMP, แคช L3 24 MB) แม้จะควบคุมด้วย Core Pinning แต่ผลลัพธ์อาจต่างจากเซิร์ฟเวอร์องค์กรขนาดใหญ่แบบ Multi-Socket NUMA ที่มีบัสสื่อสารข้ามซ็อกเก็ตซับซ้อนกว่า [Lameter, 2013]", "Normal"),
    ("2. สัญญาณรบกวนจากระบบปฏิบัติการ (OS Jitter): ทดสอบบน Ubuntu Linux ซึ่งเป็น General-Purpose OS จึงยังมีภาระเบื้องหลังของเคอร์เนล (เช่น Timer Ticks, Network Stack) ที่สร้างความแปรปรวนระดับไมโครวินาที ต่างจากระบบแบบ Real-time OS (RTOS) แท้จริง [Love, 2010]", "Normal"),
    ("3. ภาระงานทดสอบสังเคราะห์ (Synthetic Workloads): การคูณเมทริกซ์และจำลองอ่านไฟล์เป็นการทดสอบขีดจำกัดเชิงทฤษฎี ขณะที่งานจริงในอุตสาหกรรมมักมีภาระงานผสมผสานระหว่างการประมวลผล การรอคอย I/O และการเข้าถึงหน่วยความจำแบบสุ่มสลับซับซ้อน [Hennessy & Patterson, 2017]", "Normal"),
    # 10.4
    ("10.4 บทสรุปผลการศึกษาและการสังเคราะห์ทางวิศวกรรม (Conclusion)", "Heading 2"),
    ("จากการศึกษาเชิงทฤษฎีและการทดลองเชิงประจักษ์ สรุปผลสำคัญตามวัตถุประสงค์ 5 ประการได้ดังนี้:", "Normal"),
    ("1. ด้านสถาปัตยกรรมและกลไกการสลับบริบท: เธรดแชร์ Address Space, Heap และไฟล์ร่วมกัน แต่แยกเก็บ PC, Registers และ User Stack พร้อม Guard Page; การสลับบริบทของเธรดเร็วกว่าโพรเซสมากเพราะไม่ต้องสลับ Page Table และไม่สูญเสียข้อมูลในแคช TLB [Silberschatz et al., 2018; Bovet & Cesati, 2005]", "Normal"),
    ("2. ด้านการเปรียบเทียบระหว่างโพรเซสและเธรด: ยืนยัน Trade-off สำคัญ โดยมัลติเธรดสร้างและสลับงานได้เร็วกว่ามัลติโพรเซสหลายเท่าตัว แต่มี Fault Isolation ต่ำ ความผิดพลาดของเธรดเดียวอาจทำให้แครชทั้งโพรเซส [Saltzer et al., 1984; Reis & Gribble, 2009]", "Normal"),
    ("3. ด้านกลไกการประสานเวลา: Lock-Free Atomic CAS มี Throughput สูงสุดในทุกระดับการแย่งชิง ขณะที่ Spinlock เหมาะเฉพาะการแย่งชิงต่ำ เมื่อแย่งชิงสูงจะเกิด Bus Invalidation Storm ทำให้ช้ากว่า Mutex อย่างชัดเจน [Herlihy, 1991; Love, 2010]", "Normal"),
    ("4. ด้านผลการทดลองเชิงประจักษ์และแบบจำลองทฤษฎี: งาน CPU-Bound มีจุดคุ้มค่าสูงสุดเมื่อเธรดเท่ากับคอร์กายภาพ สอดคล้องกับแบบจำลอง USL ที่ทำนายจุดหักเหที่ 16 เธรดจาก Coherency Penalty (beta) และ LLC Misses ส่วนงาน I/O-Bound ขยายเธรดเกินคอร์ได้เพื่อซ่อน Latency [Gunther, 2007; Mytkowicz et al., 2009]", "Normal"),
    ("5. ด้านกรอบการตัดสินใจเชิงวิศวกรรม: ควรเลือกโมเดลตามภาระงาน โดยระบบ 1:1 เหมาะกับงานคำนวณหนัก, Non-blocking Event Loop เหมาะกับงานเครือข่าย I/O, และ Lightweight M:N Threads (Goroutines/Virtual Threads) เป็นทางเลือกที่รองรับ Concurrency สูงสุดควบคู่กับการพัฒนาที่เรียบง่าย [Kegel, 1999; Pressler & Bateman, 2023]", "Normal")
]

for doc_path in ["Report_Corrected_Condensed.docx", "Report_Corrected.docx"]:
    if not os.path.exists(doc_path):
        continue
    doc = docx.Document(doc_path)
    
    # หาตำแหน่ง 10.3 และ บรรณานุกรม
    idx_10_3 = None
    idx_ref = None
    for i, p in enumerate(doc.paragraphs):
        if "10.3" in p.text and "Limitations" in p.text:
            idx_10_3 = i
        if idx_10_3 is not None and ("เอกสารอ้างอิง" in p.text or "References & Bibliography" in p.text):
            idx_ref = i
            break
            
    print(f"{doc_path}: idx_10_3={idx_10_3}, idx_ref={idx_ref}")
    if idx_10_3 is not None and idx_ref is not None:
        # paragraphs ระหว่าง idx_10_3 ถึง idx_ref - 1 (ไม่รวม ref)
        # นำ paragraphs เก่าออก และใส่ condensed_text
        old_paras = [doc.paragraphs[k] for k in range(idx_10_3, idx_ref)]
        
        # นำ text ใหม่ใส่แทนที่ paragraph แรก
        p_anchor = old_paras[0]
        
        # แทรก paragraphs ใหม่ก่อน p_anchor
        for text, style in condensed_text:
            new_p = doc.add_paragraph(text)
            new_p.paragraph_format.line_spacing = 1.15
            new_p.paragraph_format.space_after = docx.shared.Pt(3)
            new_p.paragraph_format.space_before = docx.shared.Pt(3)
            # copy font styling
            for r in new_p.runs:
                r.font.name = "TH Sarabun New"
                r.font.size = docx.shared.Pt(14 if "Heading" not in style else 16)
                if "Heading" in style:
                    r.font.bold = True
            p_anchor._element.addprevious(new_p._element)
            
        # ลบ paragraphs เก่าออก
        for p in old_paras:
            if p.text.strip() != "":
                p._element.getparent().remove(p._element)
                
        doc.save(doc_path)
        print(f"Saved updated {doc_path}")

print("Update completed.")
