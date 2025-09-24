import streamlit as st
import re
from docx import Document

# === Hàm gom chữ OCR bị tách rời (d ượ c -> dược, tr ở -> trở) ===
def fix_ocr_spacing(text: str) -> str:
    if not text:
        return text

    def merge_chars(match):
        return match.group(0).replace(" ", "")

    # Gom các cụm chữ cái/dấu cách lặp lại thành một từ
    text = re.sub(r'(?:\b\w\s)+\w\b', merge_chars, text)

    return text


# === Hàm thêm khoảng trắng khi chữ bị dính liền (VD: ởđó -> ở đó) ===
def fix_missing_spacing(text: str) -> str:
    vowels = "àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễ" \
             "ìíịỉĩòóọỏõôồốộổỗơờớợởỡ" \
             "ùúụủũưừứựửữỳýỵỷỹđ"
    text = re.sub(rf'([{vowels}])([A-Za-z])', r'\1 \2', text)
    text = re.sub(rf'([A-Za-z])([{vowels}])', r'\1 \2', text)
    return text


# === Hàm sửa lỗi spacing nhỏ khác ===
def fix_broken_spacing(text: str) -> str:
    text = re.sub(r"\s+", " ", text)  # bỏ khoảng trắng thừa
    text = re.sub(r"\.{2,}", ".", text)  # nhiều dấu chấm -> 1 dấu
    return text.strip()


# === Hàm chuẩn hóa văn bản tổng hợp ===
def normalize_text(text: str) -> str:
    if not text:
        return ""

    # Xóa ký tự đặc biệt
    result = re.sub(r"[“”\"\'\*\~\^\%\$\#\@\!\?\[\]\{\}\<\>\\\/\=\+]", "", text)

    # Đổi dấu gạch ngang thành dấu chấm
    result = result.replace("-", ".")

    # Gộp dấu chấm liên tiếp
    result = re.sub(r"\.{2,}", ".", result)

    # Chuyển về chữ thường
    result = result.lower()

    # Fix spacing cơ bản
    result = fix_broken_spacing(result)

    # Fix OCR spacing (quan trọng nhất)
    result = fix_ocr_spacing(result)

    # Fix missing spacing (từ bị dính liền)
    result = fix_missing_spacing(result)

    return result


# === Giao diện Streamlit ===
st.set_page_config(page_title="Văn bản chuẩn hóa", layout="wide")
st.title("📑 Công cụ Chuẩn hóa Văn bản DOCX / Nhập trực tiếp")

option = st.radio("Chọn phương thức nhập:", ["📂 Tải file DOCX", "⌨️ Nhập văn bản"])

input_text = ""

if option == "📂 Tải file DOCX":
    uploaded_file = st.file_uploader("Tải lên file .docx", type=["docx"])
    if uploaded_file:
        doc = Document(uploaded_file)
        paragraphs = [p.text for p in doc.paragraphs]
        input_text = "\n".join(paragraphs)

elif option == "⌨️ Nhập văn bản":
    input_text = st.text_area("Nhập văn bản tại đây:", height=300)

# Chỉ xử lý khi bấm nút
if st.button("⚙️ Xử lý văn bản"):
    if input_text.strip():
        st.subheader("📌 Văn bản gốc:")
        st.text_area("Gốc", input_text, height=200)

        processed_text = normalize_text(input_text)

        st.subheader("✅ Văn bản đã chuẩn hóa:")
        st.text_area("Kết quả", processed_text, height=300)

        # Khung copy
        st.code(processed_text, language="markdown")
        st.button("📋 Copy toàn bộ", on_click=lambda: st.session_state.update({"copied": True}))

        if "copied" in st.session_state and st.session_state["copied"]:
            st.success("✅ Văn bản đã được copy! (Dùng Ctrl+C trong khung trên nếu chưa tự copy)")
    else:
        st.warning("⚠️ Vui lòng nhập hoặc tải lên văn bản trước khi xử lý.")
