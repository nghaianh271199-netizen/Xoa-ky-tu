import streamlit as st
import re

st.set_page_config(page_title="Text Cleaner", layout="centered")

# ========================
# Danh sách ký tự đặc biệt cần thay bằng khoảng trắng
# ========================
SPECIAL_CHARS = [
    "★","☆","✡","✦","✧","✩","✪","✫","✬","✭","✮","✯","✰",
    "⁂","⁎","⁑","✢","✣","✤","✥","✱","✲","✳","✴","✵","✶","✷",
    "✸","✹","✺","✻","✼","✽","✾","✿","❀","❁","❂","❃","❇","❈",
    "❉","❊","❋","❄","❆","❅","⋆","≛","↕","↖","↗","↘","↙","↚",
    "↛","↜","↝","↞","↟","↠","↡","↢","↣","↤","↥","↦","↧","↨",
    "↩","↪","↫","↬","↭","↮","↯","↰","↱","↲","↳","↴","↶","↷",
    "↸","↹","↺","↻","⇎","⇍","⇌","⇋","⇊","⇉","⇈","⇇","⇆","⇅",
    "⇄","⇃","⇂","⇁","⇀","↿","↾","↽","↼","⇏","⇕","⇖","⇗","⇘",
    "⇙","⇚","⇛","⇜","⇝","⇞","⇟","⇠","⇡","⇢","⇣","⇤","⇥","⇦",
    "➚","➙","➘","➔","☍","☌","☋","☊","☈","☇","▶","⏎","⌤","⌆",
    "$","€","£","¥","₮","฿","₩","₫","₪","₨","❤","❣","♡","♥","❥","❦","❧"
]

# ========================
# Hàm xử lý văn bản
# ========================
def clean_text(text: str) -> str:
    # Thay ký tự đặc biệt bằng khoảng trắng
    for ch in SPECIAL_CHARS:
        text = text.replace(ch, " ")

    # Xóa ngoặc kép đặc biệt
    text = text.replace("“", "").replace("”", "")

    # Thay "…" bằng "."
    text = text.replace("…", ".")

    # Thay dấu - bằng dấu chấm
    text = text.replace("-", ".")

    # Gom nhiều dấu chấm liên tiếp -> 1 dấu chấm
    text = re.sub(r"\.{2,}", ".", text)

    # Sau dấu chấm phải có 1 khoảng trắng
    text = re.sub(r"\.(\S)", r". \1", text)

    # Bỏ in đậm -> thường
    text = text.lower()

    # Chuẩn hóa khoảng trắng
    text = re.sub(r"\s+", " ", text).strip()

    return text

# ========================
# Giao diện Streamlit
# ========================
st.title("📝 Text Cleaner")

input_text = st.text_area("Nhập văn bản gốc:", height=200)

if st.button("Xử lý văn bản"):
    if input_text.strip():
        cleaned = clean_text(input_text)

        st.subheader("📌 Kết quả sau xử lý:")
        st.text_area("Văn bản đã làm sạch:", value=cleaned, height=200, key="output")

        # Nút copy
        st.code(cleaned, language="text")
        st.markdown(
            f"""
            <button onclick="navigator.clipboard.writeText(`{cleaned}`)" 
            style="padding:8px 16px; border:none; background:#4CAF50; color:white; border-radius:6px; cursor:pointer;">
            📋 Copy văn bản
            </button>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning("⚠️ Vui lòng nhập văn bản trước khi xử lý.")
