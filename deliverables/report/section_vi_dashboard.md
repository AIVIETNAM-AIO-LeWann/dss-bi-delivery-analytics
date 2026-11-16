# Phần VI — Kết quả và thông điệp hỗ trợ quyết định

Bản nháp để Phương Quỳnh, Lê Quang và Hoàng Quân biên tập chung.
Số liệu được đối chiếu từ các đầu ra bàn giao; Dashboard đã được mở và refresh trong Power BI Desktop; 26 kiểm tra DAX native đã đạt.
Power BI native có sơ đồ nối tuyến theo xe và trang lịch trình chi tiết. Bản preview HTML giữ thiết kế tham khảo trước lần nâng cấp.

## Phát hiện chính

Mẫu phân tích gồm 62.897 đơn không hủy, trong đó 36.048 đơn có nhãn trễ (57,31%).
Thời gian cam kết trung bình khoảng 2,94 ngày, thực tế khoảng 3,50 ngày.
First Class có mẫu hình 100% trễ trong snapshot, nhưng không phải bảo đảm cho dữ liệu ngoài mẫu.
Nhóm cần phân biệt liên hệ thống kê với nguyên nhân, và phân biệt mẫu không hủy với toàn nguồn.

Baseline theo phương thức do TV4 chọn bằng log loss validation cho bốn mức P_Late.
Trên 13.071 đơn test, ngưỡng 0,50 tạo 4.560 cảnh báo: 4.057 đúng và 503 sai;
bỏ sót 3.467 đơn trễ. Precision 88,97% và recall 53,92% cho thấy cần cân nhắc
năng lực xử lý cùng chi phí bỏ sót/cảnh báo sai, thay vì dùng một ngưỡng như mặc định kinh doanh.

Với cùng tập test, chính sách giới hạn +1 ngày và giữ Same Day làm tỷ lệ vượt hẹn tính lại
từ 57,56% xuống 26,82% (giảm 30,75 điểm phần trăm), đổi lại cam kết tăng trung bình 0,94 ngày.
Thời gian giao thực tế được giữ nguyên. Second Class vẫn vượt hẹn khoảng 60,52% với chính sách này,
nên KPI toàn mẫu chưa đủ làm căn cứ áp dụng đồng loạt.

## Khuyến nghị có trực quan hóa hỗ trợ

1. Thí điểm điều chỉnh cam kết theo phương thức, xem đồng thời tỷ lệ vượt hẹn và số ngày khách chờ.
   Căn cứ: trang Cam kết, bảng chính sách và biểu đồ theo phương thức. Không diễn giải KPI cải thiện
   sau đổi cam kết thành giao hàng nhanh hơn; theo dõi thêm trải nghiệm khách và duration thực.
2. Dùng cảnh báo như tín hiệu nhóm ban đầu; chọn ngưỡng sau khi có chi phí/năng lực xử lý
   và thiết kế thử nghiệm kiểm chứng. Căn cứ: trang Rủi ro với tham số ngưỡng và precision/recall.
   Cần xác minh khả năng biết biến lúc đặt và xử lý khả năng hủy trước khi vận hành cho mọi đơn mới.
3. Với tuyến, chỉ đối chiếu cùng instance/cấu hình có đối chứng khả thi.
   C101/base/OR-Tools đạt 10 xe và 828,94 đơn vị, so với nearest feasible 21 xe và 1.870,69 đơn vị
   (giảm khoảng 55,69% quãng đường benchmark). Căn cứ: trang Tuyến và dữ liệu TV5.
   Không gọi đây là km đường bộ hoặc khoản tiết kiệm doanh nghiệp; chi phí nhiên liệu là giả định.

## Nguồn đối chiếu trong repo

- data/dashboard/orders.csv; reports/dashboard/input_validation.json.
- workstreams/descriptive/tables/01_shipping_mode_detailed.csv.
- workstreams/forecasting/results/model_comparison.csv và predictions_test.csv.
- workstreams/prescriptive/results/promise_summary.csv và pilot_by_mode_test.csv.
- workstreams/prescriptive/results/routing_summary.csv và các route_stops tương ứng.
- dashboards/kpi_dictionary.md ghi công thức, mẫu số và phạm vi.

Chưa công bố tác động nhân quả, ROI, chi phí thực tế DHL hoặc khả năng tối ưu toàn cục của tuyến.
