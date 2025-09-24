import streamlit as st
from docx import Document
from docx.oxml.ns import qn
import re
import io
import unicodedata

st.set_page_config(page_title="DOCX Cleaner", layout="centered")

def normalize_text(s, was_bold=False):
    if not s:
        return s
    s = s.replace('“', '').replace('”', '').replace('"', '')
    s = s.replace('-', '.').replace('–', '.').replace('—', '.')
    s = re.sub(r'\.{2,}', '.', s)
    allowed_punct = set(['.', ',', ';', ':', '?', '!', '(', ')'])
    out_chars = []
    for ch in s:
        cat = unicodedata.category(ch)
        if cat[0] in ('L', 'N', 'Z'):
            out_chars.append(ch)
        elif ch in allowed_punct:
            out_chars.append(ch)
    result = ''.join(out_chars)
    if was_bold:
        result = result.lower()
    return result

def process_paragraph(paragraph):
    for run in paragraph.runs:
        was_bold = bool(run.bold)
        text = run.text
        new_text = normalize_text(text, was_bold=was_bold)
        run.text = new_text
        run.bold = False
        try:
            run.font.name = "Times New Roman"
            rFonts = run._element.rPr.rFonts
            rFonts.set(qn('w:ascii'), 'Times New Roman')
            rFonts.set(qn('w:hAnsi'), 'Times New Roman')
            rFonts.set(qn('w:eastAsia'), 'Times New Roman')
        except Exception:
            pass

def process_docx(file_stream):
    doc = Document(file_stream)
    for para in doc.paragraphs:
        process_paragraph(para)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    process_paragraph(para)
    for section in doc.sections:
        for para in section.header.paragraphs:
            process_paragraph(para)
        for para in section.footer.paragraphs:
            process_paragraph(para)
    out = io.BytesIO()
    doc.save(out)
    out.seek(0)
    return out

st.title("📄 DOCX Cleaner")
st.write("Upload file `.docx` để chuẩn hóa: \
loại bỏ ký tự đặc biệt, thay dấu `-` bằng `.`, gom nhiều dấu `.` thành một, \
font Times New Roman, bỏ chữ in đậm (đổi thành chữ thường).")

uploaded_file = st.file_uploader("Chọn file .docx", type=["docx"])

if uploaded_file is not None:
    if st.button("Xử lý file"):
        result = process_docx(uploaded_file)
        st.success("✅ Xử lý xong! Nhấn nút dưới để tải xuống.")
        st.download_button(
            label="📥 Tải file đã xử lý",
            data=result,
            file_name="processed.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
