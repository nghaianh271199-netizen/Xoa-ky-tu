# 📝 Text Cleaner

Ứng dụng trực tuyến để chuẩn hóa văn bản:

- Xóa dấu ngoặc kép “ ” và các ký tự đặc biệt.
- Thay dấu `-` thành dấu `.`.
- Gom từ 2 dấu `.` trở lên thành một dấu `.`.
- Giữ nguyên chữ, số, khoảng trắng, dấu câu cơ bản.
- Ký tự đặc biệt sẽ được thay bằng khoảng trắng để tránh dính chữ.
- Cho phép tải xuống văn bản kết quả dưới dạng `.txt`.

---

## 🚀 Cách sử dụng

### 1. Trực tuyến (khuyên dùng)
- Deploy ứng dụng trên **[Streamlit Cloud](https://share.streamlit.io/)**.
- Chỉ cần vào link → dán văn bản → bấm **Xử lý văn bản** → copy hoặc tải `.txt`.

### 2. Chạy trên máy tính
```bash
# Tạo môi trường ảo (tùy chọn)
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

# Cài thư viện
pip install -r requirements.txt

# Chạy app
streamlit run app.py
