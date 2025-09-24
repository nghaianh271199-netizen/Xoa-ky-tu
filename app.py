import streamlit as st
import re

st.set_page_config(page_title="Text Cleaner", layout="centered")

def normalize_text(s: str) -> str:
    if not s:
        return ""

    # 1. Xóa ngoặc kép
    s = s.replace('“', '').replace('”', '').replace('"', '')

    # 2. Thay mọi loại dash bằng dấu chấm
    s = s.replace('-', '.').replace('–', '.').replace('—', '.')

    # 3. Gom nhiều dấu chấm thành 1
    s = re.sub(r'\.{2,}', '.', s)

    # 4. Loại bỏ ký tự không mong muốn (chỉ giữ chữ, số, dấu câu, khoảng trắng)
    # ⚠️ Không dùng unicodedata → tránh tách chữ tiếng Việt
    s = re.sub(r"[^0-9A-Za-zÀ-ỹ.,;:?!()\s]", " ", s)

    # 5. Gom nhiều khoảng trắng thành 1
    s = re.sub(r'\s+', ' ', s)

    # 6. Xóa khoảng trắng thừa trước dấu câu
    s = re.sub(r'\s+([.,;:?!])', r'\1', s)

    # 7. Viết hoa đầu câu
    def capitalize_sentences(text):
        text = text.strip()
        # Tách câu dựa trên dấu chấm + khoảng trắng
        parts = re.split('([.?!]\s*)', text)
        fixed = []
        for i, seg in enumerate(parts):
            if i % 2 == 0:  # đoạn văn
                fixed.append(seg.strip().capitalize())
            else:  # dấu câu
                fixed.append(seg)
        return ''.join(fixed).strip()

    s = capitalize_sentences(s)

    return s

st.title("📝 Text Cleaner")
st.write("Nhập văn bản cần chuẩn hóa: bỏ ký tự đặc biệt, thay '-' bằng '.', "
         "gom nhiều dấu '.' thành 1, viết hoa đầu câu.")

# Ô nhập văn bản
input_text = st.text_area("Nhập văn bản gốc tại đây:", height=200)

# Khi nhấn nút xử lý
if st.button("🔄 Xử lý văn bản"):
    cleaned = normalize_text(input_text)
    if cleaned:
        st.success("✅ Văn bản đã xử lý")
        st.text_area("Kết quả:", cleaned, height=200, key="output")

        # Nút tải file txt
        st.download_button(
            label="📥 Tải kết quả .txt",
            data=cleaned,
            file_name="ket_qua.txt",
            mime="text/plain"
        )

        st.info("👉 Bạn có thể copy thủ công từ ô 'Kết quả' hoặc tải file .txt về.")
    else:
        st.warning("⚠️ Không có nội dung để xử lý.")
