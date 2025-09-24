import streamlit as st
from docx import Document
from docx.oxml.ns import qn
import re
import io
import unicodedata

st.set_page_config(page_title="DOCX Cleaner", layout="centered")

# --- Hàm sửa spacing bị OCR tách rời ---
def fix_broken_spacing(text: str) -> str:
    if not text:
        return text
    words = text.split()
    fixed_words = [w.replace(" ", "") for w in words]
    return " ".join(fixed_words)

# --- Hàm chuẩn hóa văn bản ---
def normalize_text(s, was_bold=False):
    if not s:
        return s

    s = s.replace('“', '').replace('”', '').replace('"', '')
    s = s.replace('-', '.').replace('–', '.').replace('—', '.')
    s = re.sub(r"\.{2,}", ".", s)

    allowed_punct = set(['.', ',', ';', ':', '?', '!', '(', ')'])
    out_chars = []
    for ch in s:
        cat = unicodedata.category(ch)
        if cat[0] in ('L', 'N', 'Z'):  # Letter, Number, Space
            out_chars.append(ch)
        elif ch in allowed_punct:
            out_chars.append(ch)
    result = ''.join(out_chars)

    result = re.sub(r'([a-zà-ỹ])([A-ZÀ-Ỹ])', r'\1 \2', result)
    result = re.sub(r'([a-zA-ZÀ-ỹ])(\d)', r'\1 \2', result)
    result = re.sub(r'(\d)([a-zA-ZÀ-ỹ])', r'\1 \2', result)

    result = fix_broken_spacing(result)

    if was_bold:
        result = result.lower()

    return result

# --- Lấy toàn bộ text từ DOCX ---
def extract_text_from_docx(file_stream):
    doc = Document(file_stream)
    all_text = []

    def process_paragraph(para):
        texts = []
        for run in para.runs:
            was_bold = bool(run.bold)
            texts.append(normalize_text(run.text, was_bold))
        return " ".join(texts)

    for para in doc.paragraphs:
        all_text.append(process_paragraph(para))
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    all_text.append(process_paragraph(para))
    for section in doc.sections:
        for para in section.header.paragraphs:
            all_text.append(process_paragraph(para))
        for para in section.footer.paragraphs:
            all_text.append(process_paragraph(para))

    return "\n".join([p.strip() for p in all_text if p.strip()])

# --- Copy button custom ---
def copy_button(text, label="📋 Copy toàn bộ"):
    js = f"""
    <script>
    function copyText() {{
        const text = `{text}`;
        navigator.clipboard.writeText(text);
        alert("Đã copy vào clipboard!");
    }}
    </script>
    <button onclick="copyText()">{label}</button>
    """
    st.markdown(js, unsafe_allow_html=True)

# ---------------- STREAMLIT UI ---------------- #

st.title("📄 DOCX Cleaner (Bản Copy)")
st.write("Ứng dụng chuẩn hóa văn bản từ `.docx` hoặc nhập trực tiếp: "
         "loại bỏ ký tự đặc biệt, thay dấu `-` bằng `.`, gom nhiều dấu `.`, "
         "chuyển font Times New Roman, bỏ chữ in đậm (đổi thành chữ thường), "
         "tách chữ dính, và sửa lỗi chữ bị OCR tách rời. "
         "Kết quả cuối hiển thị trực tiếp để copy.")

tab1, tab2 = st.tabs(["📂 Upload DOCX", "✍️ Nhập văn bản"])

with tab1:
    uploaded_file = st.file_uploader("Chọn file .docx", type=["docx"])
    if uploaded_file is not None:
        if st.button("Xử lý file DOCX"):
            result_text = extract_text_from_docx(uploaded_file)
            st.success("✅ Xử lý xong! Văn bản kết quả:")
            st.text_area("Kết quả:", value=result_text, height=400)
            copy_button(result_text)

with tab2:
    input_text = st.text_area("Nhập hoặc dán văn bản tại đây:", height=200)
    if st.button("Xử lý văn bản"):
        if input_text.strip():
            result_text = normalize_text(input_text)
            st.success("✅ Xử lý xong! Văn bản kết quả:")
            st.text_area("Kết quả:", value=result_text, height=400)
            copy_button(result_text)
        else:
            st.warning("⚠️ Vui lòng nhập văn bản trước khi xử lý.")
