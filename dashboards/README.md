# Dashboard hỗ trợ quyết định giao hàng

Phụ trách: Anh Quốc, phần VI. Đã có bộ nguồn Power BI bốn trang, sáu bảng dữ liệu đã đối chiếu
và bản xem trước tương tác ngoại tuyến. **Đã mở và refresh bằng Power BI Desktop bản Microsoft Store**, thực thi 21 kiểm tra DAX native.
Đã chụp/rà bốn trang native. Trước khi nộp, Anh Quốc cần kiểm tra lại lựa chọn và thông điệp theo yêu cầu chung của nhóm.

## Mở và xem

- Power BI: `powerbi/delivery_dashboard.pbip`; đọc [hướng dẫn Power BI](powerbi/README.md).
- Xem tương tác ngay: mở `preview/delivery_dashboard.html` bằng Edge/Chrome sau khi tạo.
  Đây là bản xem trước độc lập dùng dữ liệu đã kiểm tra; không phải ảnh render hay kết quả thực thi Power BI.
- Định nghĩa chỉ số: [kpi_dictionary.md](kpi_dictionary.md).
- Bàn giao thông điệp cho báo cáo: [phần VI](../deliverables/report/section_vi_dashboard.md).

## Tạo dữ liệu và bản xem trước từ gốc repo

```powershell
.venv/Scripts/python -m dss_bi_delivery.dashboard_data
.venv/Scripts/python scripts/build_dashboard_preview.py
.venv/Scripts/python -m unittest discover -s tests -v
```

Thiếu đầu vào thì khôi phục tài nguyên theo runbook; không tải một phiên bản khác rồi ghép tùy ý.
`scripts/build_powerbi.py` tái sinh toàn bộ nguồn báo cáo/model từ thiết kế trong script.
Lệnh này sẽ ghi đè các file đã sinh, nên sau khi sửa bằng Desktop phải đối chiếu và đồng bộ lại script
trước khi chạy. Không dùng để refresh dữ liệu; refresh không cần tái sinh thiết kế.

## Các trang

| Trang | Phạm vi | Tương tác |
| --- | --- | --- |
| Tổng quan | 62.897 đơn không hủy, 2015–2018 | Phương thức, vùng, tháng; KPI và xu hướng |
| Rủi ro | Chỉ 13.071 đơn test | Ngưỡng cảnh báo, precision/recall, số bỏ sót |
| Cam kết | Cùng tập test, 5 chính sách | So sánh vượt hẹn và tăng thời gian cam kết |
| Tuyến | Solomon, độc lập với DataCo | Chọn cấu hình đã tính; quy đổi km, tiêu hao và giá nhiên liệu |

Preview có bản đồ nối tuyến theo xe. Báo cáo Power BI dùng scatter điểm dừng và bảng thứ tự;
chưa có đường nối tuyến native. Bản preview dùng chung bộ lọc cho ba trang DataCo;
Power BI hiện dùng slicer riêng từng trang, chưa bật sync slicers.
Chọn số xe/sức chở ở Power BI bằng case đã được TV5 giải; không gọi bộ giải trực tiếp khi đổi bộ lọc.

## Kiểm tra đã chạy

- 11/11 unittest (7 TV2, 4 kiểm tra hợp đồng dữ liệu Dashboard).
- 81 kiểm tra đầu vào; nhãn, khóa, kịch bản và quãng đường được tính lại.
- 68 file qua schema Microsoft; 56 visual qua kiểm tra tham chiếu và bố cục container.
- 21 kiểm tra DAX native; công cụ authoring Microsoft xác nhận không lỗi/cảnh báo.
- 18 kiểm tra preview trong Edge, gồm ngưỡng, lọc, chính sách, nhiên liệu, không có lời giải và màn hình nhỏ.
- Đã xem ảnh bốn trang preview và màn hình nhỏ; đã kiểm tra riêng các trang render trong Power BI.

Bằng chứng: `reports/dashboard/` từ gốc repo; tách riêng kiểm tra dữ liệu, schema, preview và native.
Việc báo cáo chạy được không chứng minh tác động nhân quả, ROI hoặc hiệu quả vận hành thực tế.
