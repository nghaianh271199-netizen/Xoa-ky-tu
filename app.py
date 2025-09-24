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

    # Xóa ký tự đặc biệt, chỉ giữ lại chữ, số, khoảng trắng và dấu câu cơ bản
    allowed_punct = set(['.', ',', ';', ':', '?', '!', '(', ')'])
    out_chars = []
    for ch in s:
        cat = unicodedata.category(ch)
        if cat[0] in ('L', 'N', 'Z'):  # Letter, Number, Separator
            out_chars.append(ch)
        elif ch in allowed_punct:
            out_chars.append(ch)
        # các ký tự khác bỏ qua
    result = ''.join(out_chars)

    return result.strip()

st.title("📝 Text Cleaner")
st.write("Nhập văn bản cần chuẩn hóa, hệ thống sẽ loại bỏ ký tự đặc biệt, "
         "chuyển dấu `-` thành `.`, gom nhiều dấu `.` thành 1, "
         "và hiển thị kết quả để copy.")

# Ô nhập văn bản
input_text = st.text_area("Nhập văn bản gốc tại đây:", height=200)

# Khi nhấn nút xử lý
if st.button("🔄 Xử lý văn bản"):
    cleaned = normalize_text(input_text)
    if cleaned:
        st.success("✅ Văn bản đã xử lý")
        st.text_area("Kết quả:", cleaned, height=200, key="output")

        # Nút copy ra clipboard (Streamlit hỗ trợ bằng markdown + JS trick)
        copy_js = f"""
        <script>
        function copyText() {{
            navigator.clipboard.writeText(`{cleaned}`);
            alert("Đã copy văn bản!");
        }}
        </script>
        <button onclick="copyText()">📋 Copy văn bản</button>
        """
        st.markdown(copy_js, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Không có nội dung để xử lý.")
