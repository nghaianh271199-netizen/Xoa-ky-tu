import streamlit as st
import re
import unicodedata

st.set_page_config(page_title="Text Cleaner", layout="centered")

def normalize_text(s: str) -> str:
    if not s:
        return ""

    # Xóa ngoặc kép
    s = s.replace('“', '').replace('”', '').replace('"', '')

    # Thay mọi loại dash bằng dấu chấm
    s = s.replace('-', '.').replace('–', '.').replace('—', '.')

    # Gom nhiều dấu chấm thành 1
    s = re.sub(r'\.{2,}', '.', s)

    # Giữ lại chữ, số, khoảng trắng và dấu câu cơ bản
    allowed_punct = set(['.', ',', ';', ':', '?', '!', '(', ')'])
    out_chars = []
    for ch in s:
        cat = unicodedata.category(ch)
        if cat[0] in ('L', 'N', 'Z'):  # Letter, Number, Separator
            out_chars.append(ch)
        elif ch in allowed_punct:
            out_chars.append(ch)
        else:
            out_chars.append(" ")  # thay ký tự lạ bằng khoảng trắng

    result = ''.join(out_chars)

    # Gom nhiều khoảng trắng thành 1
    result = re.sub(r'\s+', ' ', result)

    # Xóa khoảng trắng thừa trước dấu câu
    result = re.sub(r'\s+([.,;:?!])', r'\1', result)

    # Viết hoa sau dấu chấm + đầu văn bản
    def capitalize_after_dot(text):
        sentences = re.split('(\. )', text)
        fixed = []
        for i, seg in enumerate(sentences):
            if i == 0 and seg:
                fixed.append(seg.strip().capitalize())
            elif seg == '. ':
                fixed.append(seg)
            elif seg:
                fixed.append(seg.strip().capitalize())
        return ''.join(fixed)

    result = capitalize_after_dot(result)

    return result.strip()

st.title("📝 Text Cleaner")
st.write("Nhập văn bản cần chuẩn hóa, hệ thống sẽ loại bỏ ký tự đặc biệt, "
         "chuyển dấu `-` thành `.`, gom nhiều dấu `.` thành 1, "
         "và viết hoa sau dấu chấm.")

# Ô nhập văn bản
input_text = st.text_area("Nhập văn bản gốc tại đây:", height=200)

# Khi nhấn nút xử lý
if st.button("🔄 Xử lý văn bản"):
    cleaned = normalize_text(input_text)
    if cleaned:
        st.success("✅ Văn bản đã xử lý")

        # Hiển thị văn bản kết quả
        st.text_area("Kết quả:", cleaned, height=200, key="output")

        # Nút tải xuống file .txt
        st.download_button(
            label="📥 Tải kết quả .txt",
            data=cleaned,
            file_name="ket_qua.txt",
            mime="text/plain"
        )

        st.info("👉 Bạn có thể copy thủ công từ ô 'Kết quả' hoặc tải file .txt về máy.")
    else:
        st.warning("⚠️ Không có nội dung để xử lý.")
