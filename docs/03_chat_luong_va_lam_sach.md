# 3. Kiểm tra chất lượng và làm sạch

Đây là chính sách xử lý đã triển khai, không phải danh sách lời khuyên chung.
Số dòng bị ảnh hưởng của từng thao tác nằm trong `reports/preparation_log.csv`.
Kết quả thực chạy nằm trong `reports/data_quality_report.md`.

**Cập nhật 28/10/2026:** bốn bước dưới đây mô tả bảng trung gian giữ đầy đủ nguồn.
Bước làm sạch bổ sung tạo `orders_analysis.csv` để bàn giao cho phân tích; xem
[quy tắc và đầu ra](07_du_lieu_cho_phan_tich.md), [kết quả thực chạy](../reports/analysis_readiness_report.md).
Bảng chính có 62.897 đơn, không ô trống. Địa danh hỏng được chuyển thành nhóm không
xác định có cờ, không tự đoán lại; đơn hủy tách khỏi mẫu chính. Missing ZIP và các
trường không cần không xuất hiện trong bảng phân tích.

## Bước 1 — Đảm bảo chất lượng

- Đọc mọi cột CSV dưới dạng chuỗi trước để giữ mã; dùng CP1252 strict, không bỏ qua
  byte lỗi. UTF-8 không giải mã được nguồn. Latin-1 đọc được nhưng tạo 20 ký tự C1
  trong địa danh; CP1252 giải mã được toàn bộ file, không sinh C1 hoặc ký tự thay thế.
- Bỏ khoảng trắng đầu/cuối; ô chỉ có khoảng trắng chuyển thành NA. Không bỏ dấu,
  không đổi đồng loạt tên thành phố/quốc gia, không tự sửa chuỗi có dấu hỏi.
- Chuyển số theo schema; ngày dùng `%m/%d/%Y %H:%M`. Parse thất bại được ghi nhận
  và giữ raw để tra lại. Không suy diễn ngày theo cấu hình máy.
- Mã và ZIP giữ chuỗi. ZIP chỉ bỏ hậu tố `.0` do cách ghi nguồn, không thêm số 0 đầu.
  `603` chưa được xác minh là mã bưu chính chuẩn hay đã mất số 0 trong nguồn.
- Tỷ lệ giảm giá giữ thập phân 0–1. Lợi nhuận âm không mặc định là lỗi.

## Bước 2 — Xác thực

- Đối chiếu SHA-256 và schema 53 cột với bản đã tải.
- Đếm dòng trước/sau, thiếu, distinct, trùng hoàn toàn và khóa dòng hàng.
- Kiểm tra miền nhãn, ngày parse được, khoảng thời gian không âm, duration nguyên
  không âm, khóa bắt buộc và quan hệ nhãn/trạng thái/chênh lệch ngày.
- Kiểm tra tọa độ trong miền vĩ/kinh độ; miền hợp lệ không chứng minh đó là điểm giao.
- Kiểm tra từng cặp cột trùng trên toàn bộ dữ liệu trước khi loại cột.
- Kiểm tra nhất quán các trường header khi gom cùng `Order Id`. Nếu một trường
  mâu thuẫn, bảng đơn để trống trường đó và gắn `order_header_conflict=1`;
  đơn không được vào KPI chuẩn. Không tùy tiện chọn dòng đầu để che mâu thuẫn.
- Tính đầy đủ so với ERP gốc và tổng giao dịch đã kiểm toán **chưa xác minh được**,
  vì nguồn không cung cấp tổng kiểm soát độc lập.

## Bước 3 — Làm sạch

**Không xóa dòng nào của bản nguồn hiện tại.** Chỉ loại cột trong bảng xuất chuẩn;
CSV raw giữ nguyên. Mọi dòng vẫn truy nguyên được qua `source_row_number`.

| Nhóm | Quyết định | Căn cứ |
| --- | --- | --- |
| Tên/họ, email, password, địa chỉ đường khách | Loại 5 cột | Không cần cho câu hỏi logistics |
| Product Description | Loại | Thiếu 100%; không bịa mô tả |
| Product Image | Loại | Không dùng ảnh trong phạm vi hiện tại |
| Product Status | Loại | Hằng số 0; không có thông tin phân biệt |
| 6 cột có bản sao tương đương | Giữ một cột chuẩn | Đã so sánh toàn bộ giá trị; xem duplicate_columns.csv |
| Order Zipcode | Giữ NA, không dùng làm candidate mặc định | Thiếu 155.679 dòng, 86,24%; không gán hàng loạt |
| Customer Zipcode | Giữ 3 ô thiếu | Không thiết yếu cho KPI hiện tại |
| Customer Lname | Không gán 8 ô thiếu | Cột đã bị loại vì không cần |
| Duration lệch timestamp | Giữ hai trường và gắn cờ | Chưa rõ ngữ nghĩa/làm tròn; không tự “sửa đúng” |
| Đơn hủy | Giữ trong bảng chuẩn, loại khỏi mẫu KPI chính | Hủy không tương đương giao đúng hạn |
| Ngoại lai tiền/lợi nhuận | Giữ, thống kê | Chưa có quy tắc nghiệp vụ để xóa hoặc winsorize |

Không có gán giá trị thay thế nên hiện tại không có cột cờ imputation. Các cờ lỗi
parse/chất lượng không phải cờ gán dữ liệu. Nếu bổ sung imputation sau này phải
thêm cờ riêng và ghi lý do, không gán lại nguồn.

Bảng `order_items_clean.csv` có **180.519 dòng × 54 cột**: 39 cột nguồn giữ lại,
15 cột dẫn xuất/cờ. Bảng `orders_clean.csv` có **65.752 dòng × 36 cột**.
Giảm số dòng khi tổng hợp cấp đơn không phải thao tác loại dòng trùng.

## Bước 4 — Khám phá sơ bộ

- Thống kê số, phân vị, min/max tại `reports/numeric_summary.csv`.
- Phân phối số ngày thực tế/kế hoạch, chênh lệch ngày, vùng, phương thức và trạng
  thái ở **cấp đơn** tại `reports/initial_distributions.csv`.
- So sánh phương thức: `reports/shipping_mode_summary.csv`.
- KPI ba định nghĩa mẫu ở hai cấp dữ liệu: `reports/baseline_kpis.csv`.

Mẫu chính có **62.897 đơn**, **36.048 đơn trễ**, tỷ lệ **57,31%**. Mẫu
`COMPLETE`/`CLOSED` có **28.965 đơn**, tỷ lệ **57,42%**. Đây là kiểm tra độ nhạy
về chọn mẫu, chưa phải chứng minh trạng thái nguồn hoàn toàn đáng tin.

Một bất thường đáng kiểm tra: trong mẫu chính, **First Class trễ 100%** và số ngày
thực tế đều bằng 2, trong khi cam kết là 1. Không được chuyển điều này thành lời
khẳng định “First Class luôn trễ trong thực tế”. Cần xem đây là đặc tính phiên bản
dữ liệu, kiểm tra theo thời gian và xem lại nguồn trước khi khuyến nghị đổi dịch vụ.

## Hợp đồng bàn giao cho phần phân tích

1. Dùng `orders_analysis.csv` khi trả lời tỷ lệ trễ **theo đơn**. Đây là mẫu được
   kiểm tra bổ sung từ `orders_clean.csv` sau khi lọc eligibility; báo cáo mẫu số.
   Giữ thêm KPI toàn nguồn để đối chiếu đề.
2. Dùng `order_items_clean.csv` khi phân tích sản phẩm/danh mục; một đơn có nhiều
   danh mục có thể xuất hiện trong nhiều nhóm. Không cộng số đơn các nhóm rồi gọi
   đó là tổng đơn duy nhất; không tùy ý lấy một danh mục đại diện cho đơn.
3. Bảng chuẩn chứa cả biến kết quả. **Không đưa cả bảng vào mô hình**. Dùng
   `orders_model_features.csv`, `orders_model_labels.csv` và `orders_model_splits.csv`;
   chỉ lấy các cột trong `model_feature_columns` của `analysis_schema.json` khi fit.
   `role=candidate` chỉ là danh sách xem xét, không phải danh sách đã được chứng minh
   sẵn có tại thời điểm đặt hàng. ID, cờ chất lượng, trạng thái kết quả, lợi nhuận,
   timestamp shipment và các biến duration thực tế không được tự động thành feature.
4. Chia tập theo thời gian đặt hàng; mọi dòng cùng đơn nằm cùng tập. Sau này cần
   thêm khoảng đệm/kiểm tra nhãn đã quan sát đủ ở thời điểm cắt, vì đơn cuối kỳ có
   thể hoàn thành sau mốc chia. Fit phép gán/scaling/encoding chỉ trên tập train.
5. Quan hệ phương thức/vùng với trễ chỉ là liên hệ quan sát. Thay thời hạn cam kết
   có thể làm giảm tỷ lệ “trễ” theo định nghĩa mà chưa cải thiện vận hành.
