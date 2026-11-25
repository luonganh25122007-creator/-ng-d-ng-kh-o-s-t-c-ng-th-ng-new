# Ứng dụng Khảo sát và Phân tích Mức độ Căng thẳng của Học sinh

## Cài đặt và chạy

Mở PowerShell tại thư mục dự án:

```powershell
python -m pip install -r requirements.txt
$env:ADMIN_PASSWORD = "mat-khau-quan-tri"
python -m streamlit run app.py
```

Nếu không đặt `ADMIN_PASSWORD`, tab **Quản lý** sẽ bị khóa. Hãy dùng mật khẩu
riêng, không chia sẻ mật khẩu cho học sinh và không đưa mật khẩu vào mã nguồn.

## Dữ liệu và quyền riêng tư

Kết quả được lưu trong `stress_data.csv` cạnh `app.py`. Tệp này chứa họ tên/mã
số, lớp và câu trả lời khảo sát; chỉ nên lưu trên máy được nhà trường cho phép,
giới hạn người truy cập và tuân thủ quy định bảo vệ dữ liệu của nhà trường.
Không đưa CSV lên kho mã nguồn hoặc chia sẻ công khai. Tệp CSV không được mã hóa
bởi ứng dụng.

Đây là khảo sát tham khảo, không chẩn đoán sức khỏe. Học sinh cần trao đổi với
người lớn đáng tin cậy hoặc nhân viên tư vấn khi gặp khó khăn; trường hợp không
an toàn cần báo ngay cho người lớn ở gần và dịch vụ khẩn cấp tại địa phương.
