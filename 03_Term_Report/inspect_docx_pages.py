import os
import sys
import win32com.client

docx_path = os.path.abspath("Report_Corrected.docx")
print("Target file:", docx_path)

word = win32com.client.Dispatch("Word.Application")
word.Visible = False

try:
    doc = word.Documents.Open(docx_path, ReadOnly=True)
    
    # Force pagination
    doc.Repaginate()
    
    total_pages = doc.ComputeStatistics(2) # 2 = wdStatisticPages
    print(f"Total Pages: {total_pages}")
    
    # Iterate through paragraphs to find Headings and page numbers
    # wdInformation: 3 = wdActiveEndPageNumber, 1 = wdActiveEndAdjustedPageNumber
    wdActiveEndPageNumber = 3
    
    headings_info = []
    
    for i, p in enumerate(doc.Paragraphs):
        style_name = str(p.Style.NameLocal)
        text = p.Range.Text.strip().replace('\u200b', '')
        if not text:
            continue
        
        # Check if heading or chapter or significant section
        is_heading = False
        if any(h in style_name for h in ["Heading", "หัวข้อ", "Title"]) or text.startswith("บทที่") or text.startswith("ภาคผนวก") or text.startswith("บรรณานุกรม") or text.startswith("สารบัญ") or text.startswith("คำนำ"):
            is_heading = True
        elif any(text.startswith(f"{ch}.") for ch in range(1, 11)):
            is_heading = True
            
        if is_heading:
            try:
                page_num = p.Range.Information(wdActiveEndPageNumber)
            except Exception:
                page_num = -1
            headings_info.append((page_num, style_name, text[:100]))
            
    doc.Close(False)
finally:
    word.Quit()

with open("headings_page_analysis.txt", "w", encoding="utf-8") as f:
    f.write(f"Total Pages: {total_pages}\n\n")
    for page_num, style, text in headings_info:
        f.write(f"[Page {page_num:3d}] ({style}) {text}\n")

print("Analysis saved to headings_page_analysis.txt")
