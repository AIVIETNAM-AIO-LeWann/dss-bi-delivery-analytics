# 7. Dữ liệu bàn giao cho mô tả, chẩn đoán, dự báo và đề xuất

Đây là bước làm sạch bổ sung ngày **28/10/2026**. Chạy
`python -m dss_bi_delivery.prepare_data` để tạo cả bảng trung gian và các bảng dưới
đây. `python -m dss_bi_delivery.verify_data` kiểm tra lại các file đã xuất với nguồn.

## Phạm vi đạt được

Bảng chính `data/processed/orders_analysis.csv` có **62.897 đơn × 26 cột**,
không thiếu ô, không trùng mã đơn, không có số vô hạn và không còn tên địa lý chứa
dấu hỏi/ký tự thay thế/ký tự điều khiển. Nhãn trễ khớp chênh lệch ngày trên mẫu này;
không có nhãn bị sửa để đạt điều kiện.

Không khẳng định đã phục hồi mọi sự thật trong nguồn. Missing ở cột không cần cho
logistics được xử lý bằng cách không đưa cột đó vào bảng phân tích. Tên địa lý không
khôi phục được dùng `__UNKNOWN__` kèm cờ; đó là **nhóm không xác định**, không phải
giá trị thật được gán. Không điền số bằng trung bình/trung vị để làm đẹp dữ liệu.

Mọi đơn đều được giữ trong bảng trung gian `orders_clean.csv`. Có 2.855 đơn hủy
không thuộc mẫu logistics chính; mã và lý do nằm tại `orders_excluded.csv`.

## Mô tả

Dùng bảng `orders_analysis.csv`, cấp đơn. KPI trễ: **36.048/62.897 = 57,31%**.
Lọc theo `shipping_mode`, `order_region`, `market` hoặc lịch đặt hàng; luôn báo cáo
số đơn cạnh tỷ lệ. Tỷ lệ 54,82% trong bảng toàn nguồn gồm hủy=0 chỉ là tỷ lệ nhãn
nguồn, không gọi đó là tỷ lệ trễ trên các đơn đã giao.

`order_city_unknown_flag`/`order_state_unknown_flag` chỉ rõ các nhóm địa lý chưa
biết. Nếu báo cáo cấp thành phố, hiển thị nhóm `__UNKNOWN__` hoặc ghi rõ số đơn
không xác định đã loại; không âm thầm biến mất mẫu số.

## Chẩn đoán

Dùng cùng bảng chính để so sánh vùng/phương thức/ngày đặt và kiểm soát phân khúc,
số lượng, quy mô đơn theo số dòng. Tên thành phố trùng ở nhiều quốc gia không được
nối chỉ bằng tên thành phố. Các biến duration thực tế và delay được phép dùng để
mô tả kết quả hồi cứu nhưng không dùng làm “nguyên nhân biết trước” của nhãn trễ.

`reports/anomalies_by_month_and_mode.csv` xác nhận First Class có số ngày thực tế
bằng 2 và trễ 100% trong mẫu không hủy ở cả **37 tháng**. Đây là mẫu hình rất mạnh
của bản dữ liệu, chưa chứng minh đặc tính dịch vụ ngoài thực tế. Giữ dữ liệu thay
vì tự đổi nhãn; khi mô hình hóa cần baseline theo phương thức và đánh giá có/không
Shipping Mode để nhận ra mô hình chỉ học lại mẫu hình này.

`reports/analysis_sensitivity.csv` so sánh mẫu chính, mẫu timestamp nhất quán và
mẫu bỏ First Class. Hai mẫu sau phục vụ đánh giá độ nhạy, không mặc định là mẫu
“đúng” hơn. Các liên hệ quan sát chưa chứng minh nguyên nhân trễ.

## Dự báo

Ba file ghép theo `order_id`, không dựa vào vị trí dòng:

| File | Vai trò |
| --- | --- |
| orders_model_features.csv | Hai khóa order_id/order_datetime và 13 candidate |
| orders_model_labels.csv | order_id và nhãn late_delivery_risk gốc |
| orders_model_splits.csv | order_id/order_datetime và partition |

Allowlist và kiểu/thang nghĩa nằm tại `docs/analysis_schema.json`. Khi fit chỉ lấy
`model_feature_columns`; **không dùng order_id/order_datetime thô làm predictor**.
Không có duration thực tế, trạng thái kết quả, cờ duration, nhãn trễ, timestamp
shipment hay cờ chọn mẫu trong feature file.

Chia tập theo thời gian, không shuffle:

| Tập | Quy tắc |
| --- | --- |
| train | Đặt trước 25/12/2016, shipment proxy trước 01/01/2017 |
| validation | Từ 01/01/2017 đến trước 24/06/2017, shipment proxy trước 01/07/2017 |
| test | Từ 01/07/2017 đến hết nguồn |
| purged_boundary | Khoảng 7 ngày trước hai mốc cắt; không fit hoặc chấm điểm |

Các mốc là quy ước đánh giá lịch sử, không phải kết quả tối ưu. Bảy ngày lớn hơn
duration tối đa sáu ngày của bản nguồn; timestamp shipment chỉ là proxy vì nguồn
không cho thời điểm nhãn thực sự được ghi nhận. Chưa thể xác nhận hết rò rỉ nghiệp
vụ hoặc candidate đã biết lúc đặt hàng chỉ bằng kiểm tra kỹ thuật.

Chỉ fit encoding/scaling/imputation nếu cần trên train; dùng transform cho
validation/test, xử lý nhãn danh mục mới ngoài train. Mọi tỷ lệ trễ lịch sử theo
vùng hay phân vị SLA nếu trở thành đầu vào phải tính từ quá khứ/train. Chưa tạo
feature target-encoding hoặc thống kê toàn nguồn đưa vào mô hình.

Mẫu hiện tại dự báo **trễ với điều kiện không hủy** trong snapshot lịch sử. Nếu
quyết định dành cho mọi đơn vừa đặt, nhóm cần mở rộng thiết kế bằng nhãn hủy riêng
hoặc đánh giá ba trạng thái; không dùng kết quả mô hình trên mẫu này như xác suất
trễ vô điều kiện của mọi đơn mới. Dữ liệu chưa có tọa độ điểm nhận đủ để tạo
khoảng cách tuyến và chưa có bằng chứng xác nhận mốc biết từng candidate.

## Đề xuất

`reports/duration_distribution_by_mode_region.csv` có số đơn, tỷ lệ trễ, duration
trung bình và các phân vị 50/90/95% của duration nguồn. Phân vị lấy giá trị quan sát
kế tiếp (`higher`) để không tự sinh cam kết lẻ khi nguồn chỉ có ngày nguyên.

Đây là đầu vào khám phá cam kết theo nhóm; các mức 90/95% là thống kê mô tả, chưa
phải mục tiêu dịch vụ đã được chọn. Khi đánh giá chính sách, tính cam kết trên
train, cố định rồi đánh giá ngoài mẫu; không dùng bảng toàn lịch sử để tuyên bố
thành tích test. Báo cáo cả thời gian cam kết và thời gian thực tế: kéo dài cam
kết làm giảm nhãn trễ không đồng nghĩa vận hành giao nhanh hơn.

`orders_timestamp_consistent.csv` có 59.490 đơn, không còn chênh giữa duration và
khoảng timestamp. Bảng này loại toàn bộ Same Day nên chỉ là phân tích độ nhạy;
không dùng để đại diện đủ bốn phương thức. Mẫu chính dùng duration nguồn và giữ
cờ, không đồng thời sử dụng shipping timestamp/span như cùng một phép đo.

Chưa có dữ liệu để định lượng lợi ích can thiệp, chi phí nhiên liệu hoặc tối ưu
tuyến xe thực. Cần bổ sung nguồn phù hợp, ví dụ Solomon cho benchmark VRPTW. Các
giới hạn này là thiếu đầu vào bài toán, không thể xử lý bằng cách điền missing.

## Những quyết định xử lý được ghi lại ở đâu

- `reports/analysis_readiness_report.md`: trước/sau, mẫu phân tích, kết quả và giới hạn.
- `reports/analysis_geography_changes.csv`: chuỗi địa lý gốc không phục hồi và số đơn.
- `reports/analysis_exclusion_summary.csv`: số đơn theo lý do không thuộc mẫu chính.
- `reports/analysis_cleaning_changes.csv`: chuẩn hóa Unicode/khoảng trắng và nhóm unknown.
- `reports/analysis_validation.json`: kiểm tra tại bước tạo bảng.
- `reports/validation_results.json`: kiểm tra độc lập sau khi xuất.
- `tests/test_analysis_data.py`: kiểm tra các tình huống không được tự sửa/xóa tùy ý.
