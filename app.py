import streamlit as st
import re
from docx import Document

# === Hàm xử lý khoảng cách chữ bị lỗi OCR (tách rời từng ký tự) ===
def fix_ocr_spacing(text: str) -> str:
    if not text:
        return text

    tokens = text.split()
    merged_tokens = []
    buffer = ""

    for tok in tokens:
        if len(tok) == 1:  # nếu là ký tự đơn lẻ
            buffer += tok
        else:
            if buffer:
                merged_tokens.append(buffer + tok)
                buffer = ""
            else:
                merged_tokens.append(tok)

    if buffer:
        merged_tokens.append(buffer)

    return " ".join(merged_tokens)


# === Hàm sửa lỗi spacing nhỏ khác ===
def fix_broken_spacing(text: str) -> str:
    text = re.sub(r"\s+", " ", text)  # bỏ khoảng trắng thừa
    text = re.sub(r"\.{2,}", ".", text)  # từ 2 dấu chấm trở lên -> 1 dấu chấm
    return text.strip()


# === Hàm chuẩn hóa văn bản ===
def normalize_text(text: str) -> str:
    if not text:
        return ""

    # Xóa ký tự đặc biệt, giữ lại chữ, số, khoảng trắng và dấu câu cơ bản
    result = re.sub(r"[“”\"\'\*\~\^\%\$\#\@\!\?\[\]\{\}\<\>\\\/\=\+]", "", text)

    # Đổi dấu gạch ngang thành dấu chấm
    result = result.replace("-", ".")

    # Gộp dấu chấm liên tiếp
    result = re.sub(r"\.{2,}", ".", result)

    # Bỏ in đậm -> chuyển về chữ thường (giả lập vì DOCX không giữ inline style khi đọc)
    result = result.lower()

    # Fix spacing
    result = fix_broken_spacing(result)

    # Fix OCR spacing (quan trọng nhất)
    result = fix_ocr_spacing(result)

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

        # Hiển thị khung copy
        st.code(processed_text, language="markdown")
        st.button("📋 Copy toàn bộ", on_click=lambda: st.session_state.update({"copied": True}))

        if "copied" in st.session_state and st.session_state["copied"]:
            st.success("✅ Văn bản đã được copy! (Dùng Ctrl+C trong khung trên nếu chưa tự copy)")
    else:
        st.warning("⚠️ Vui lòng nhập hoặc tải lên văn bản trước khi xử lý.")
