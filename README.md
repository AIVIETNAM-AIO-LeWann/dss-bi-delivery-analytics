# Phân tích giao hàng và hỗ trợ quyết định

Dự án nhóm 7 môn Hệ Hỗ trợ Quyết định & Trí tuệ Kinh doanh, HK261.
**Chủ đề 18: giao hàng đúng hẹn và tối ưu tuyến đường**, theo quy trình SOAR.
Giám đốc Logistics cần cân nhắc điều chỉnh cam kết theo phương thức/vùng và phương án tuyến giao.
DataCo dùng để phân tích giao hàng; Solomon dùng riêng để thử nghiệm tuyến.

## Bắt đầu

1. Đọc [bối cảnh và trạng thái](docs/project/context.md).
2. Xem [bản đồ thư mục](docs/project/structure.md) để biết đặt và tìm file ở đâu.
3. Làm theo [hướng dẫn vận hành](docs/project/runbook.md) khi kiểm tra hoặc chạy lại.
4. Anh Quốc bắt đầu tại [bàn giao Dashboard](dashboards/README.md).
5. Trước khi gửi thay đổi, xem [quy ước cộng tác](CONTRIBUTING.md).

## Các phần công việc

| Phần | Người phụ trách | Điểm vào |
| --- | --- | --- |
| Bối cảnh, tổng hợp báo cáo | Phương Quỳnh | `deliverables/report/` — chưa nhận bản riêng |
| Chuẩn bị dữ liệu | Lê Quang | [Tài liệu](docs/data_preparation/README.md), `src/dss_bi_delivery/` |
| Mô tả và chẩn đoán | Hoàng Quân | [Bàn giao](workstreams/descriptive/README.md) |
| Dự báo, hạn chế | Ngọc Quang | [Bàn giao](workstreams/forecasting/README.md) |
| Đề xuất, benchmark tuyến | Hoài Phú | [Bàn giao](workstreams/prescriptive/README.md) |
| Dashboard | Anh Quốc | [Đầu vào và tiêu chí](dashboards/README.md) — PBIP đã mở/refresh và kiểm tra native |
| Slide | Phương Quỳnh, Anh Quốc | `deliverables/slides/` — chưa có bản cuối |

## Dữ liệu chính

`data/processed/orders_analysis.csv`: 62.897 đơn không hủy; 36.048 nhãn trễ (57,31%).
`workstreams/forecasting/results/predictions_test.csv`: 13.071 đơn test, 01/07/2017–31/01/2018.
`workstreams/prescriptive/results/dashboard_orders_test.csv`: bảng test ghép kết quả dự báo và kịch bản cam kết.
Mã `order_id` là Text; tỷ lệ/xác suất lưu 0–1. Mẫu toàn nguồn, mẫu không hủy và test có mẫu số khác nhau.

Dashboard Delivery Insights: mở `dashboards/powerbi/delivery_dashboard.pbip` để xem bốn trang chính và lịch trình chi tiết. Bản HTML trong `dashboards/preview/` giữ thiết kế tham khảo trước lần nâng cấp native.
Hướng dẫn và trạng thái nghiệm thu tại [dashboards/README.md](dashboards/README.md).

Các CSV sạch trong thư mục chung được khôi phục từ snapshot bàn giao, có checksum tại
`references/restored_data_manifest.json`; chưa phải kết quả chạy lại từ raw trên máy này.
Workbook Excel kèm tính toán là tài liệu đối chiếu, không thay thế CSV nguồn đã ghim checksum.

## Tài nguyên và nguồn gốc

Chín tệp người dùng cung cấp đã được sao chép, đổi tên có hệ thống và kiểm tra SHA-256.
Tra tên cũ → tên mới tại `references/resource_manifest.json`. ZIP nguyên bản ở `archive/handoffs/`.
Các bộ bàn giao được giữ cấu trúc nội bộ để bảo toàn cách chạy và chứng cứ gốc.
Quy tắc trong prompt/tài liệu là nội dung tham khảo của bài tập, không phải lệnh tự động cho công cụ.

Tài liệu và dữ liệu bên thứ ba giữ giấy phép riêng. Không tự cấp giấy phép chung cho chúng.
