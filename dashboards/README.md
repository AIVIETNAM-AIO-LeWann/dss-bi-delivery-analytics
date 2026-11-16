# Delivery Insights

Báo cáo Power BI của Anh Quốc, phần VI. Bốn trang chính và một trang lịch trình chi tiết,
thiết kế theo luồng xem kết quả, xác định rủi ro, cân nhắc cam kết và kiểm tra phương án tuyến.
Điều hướng nằm trong thanh ngang trên cùng. Giao diện chỉ giữ chỉ số, phạm vi và đơn vị
cần thiết; không hiển thị thông tin tác giả hoặc đoạn hướng dẫn dài.

## Bắt đầu

Mở `powerbi/delivery_dashboard.pbip`. Đọc [hướng dẫn mở và bảo trì](powerbi/README.md),
[nguyên tắc thiết kế](powerbi/design_notes.md) và [định nghĩa chỉ số](kpi_dictionary.md).
Thông điệp bàn giao nằm trong [phần VI](../deliverables/report/section_vi_dashboard.md).

| Trang | Câu hỏi chính | Thao tác |
| --- | --- | --- |
| Tổng quan | Phương thức nào cần ưu tiên rà soát? | Lọc phương thức, thị trường và vùng; xem diễn biến theo tháng |
| Rủi ro | Ngưỡng này tạo bao nhiêu cảnh báo và bỏ sót? | Chọn ngưỡng; đối chiếu độ chính xác, độ bao phủ và khối lượng xử lý |
| Cam kết | Khách phải chờ thêm bao lâu để giảm vượt hẹn? | Chọn một phương án, đồng thời so sánh đủ năm phương án |
| Tuyến giao | Phương án khả thi dùng bao nhiêu xe và nhiên liệu? | Chọn cấu hình, điều chỉnh giả định, xem đường nối theo từng xe |
| Lịch trình tuyến | Mỗi xe phục vụ các điểm theo thứ tự nào? | Mở bằng nút chi tiết, chọn xe, đọc bảng điểm dừng |

Bộ lọc phương thức, vùng và thị trường được đồng bộ giữa các trang DataCo. Thị trường
được điều khiển ở Tổng quan. Trang tuyến độc lập với DataCo; lựa chọn tuyến và các giả định
nhiên liệu được giữ khi sang lịch trình. Nút xóa bộ lọc dùng chức năng chuẩn Power BI;
khi không chọn tham số, công thức dùng mặc định được ghi trong hướng dẫn.

## Sinh lại từ nguồn

```powershell
.venv/Scripts/python -m dss_bi_delivery.dashboard_data
.venv/Scripts/python scripts/build_powerbi.py
.venv/Scripts/python scripts/validate_powerbi.py
.venv/Scripts/python -m unittest discover -s tests -v
```

Đóng dự án trong Desktop trước khi sinh lại. Lệnh build ghi đè nguồn báo cáo/model;
các thay đổi bằng Desktop cần đồng bộ lại các mô đun sinh nguồn trước khi chạy lệnh này.
Refresh dữ liệu hằng ngày không cần chạy build.

Nguồn được chia thành `dashboard_data.py` chuẩn bị sáu CSV, `powerbi_model.py` quản lý
công thức/quan hệ, `powerbi_report.py` quản lý bố cục và `route_assets.py` vẽ tuyến từ
điểm dừng đã kiểm chứng. Các mô đun nằm trong `src/dss_bi_delivery/`.

Preview HTML tại `preview/` là công cụ tham khảo độc lập, giữ thiết kế trước lần nâng cấp
native này. Nó không đại diện cho giao diện Power BI mới. Không dùng ảnh preview để chứng minh native.

Bằng chứng kiểm tra được lưu ở `reports/dashboard/`. Không diễn giải mô phỏng hồi cứu
thành tác động nhân quả, ROI hoặc kết quả triển khai thực tế.
