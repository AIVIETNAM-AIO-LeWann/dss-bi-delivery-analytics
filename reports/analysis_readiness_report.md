# Dữ liệu bàn giao cho bốn cấp độ phân tích

Bảng chính: `data/processed/orders_analysis.csv`, **62,897 đơn × 26 cột**; thiếu ô: **0**. Không có giá trị số được gán hay nhãn bị sửa.

Các kết quả đạt quy tắc kỹ thuật đã công bố, không xác minh được tính đúng ngoài đời của các chỉ báo nguồn. `orders_clean.csv` là bảng trung gian giữ đầy đủ đơn; dùng bảng analysis cho mẫu logistics chính.

## Trước → sau

| Vấn đề | Trước | Sau | Xử lý |
| --- | --- | --- | --- |
| Đơn trong bảng trung gian | 65752 | 62897 | Loại khỏi mẫu chính các đơn không đạt điều kiện; lưu mã và lý do ở orders_excluded.csv |
| City/state hỏng hoặc thiếu | 143 | 0 chuỗi hỏng trong bảng chính | Đổi thành __UNKNOWN__ và cờ; số trước là số ô trên mọi đơn, không phải số đơn duy nhất |
| ZIP thiếu | Customer ZIP 3; Order ZIP 155679 dòng nguồn | Không có cột ZIP trong bảng chính | Loại trường không cần cho câu hỏi logistics; không xóa đơn vì ZIP |
| Duration lệch timestamp | 3571 | 3407 | Mẫu chính dùng duration nguồn; bỏ timestamp shipment/span để tránh hai định nghĩa; mẫu đối chiếu thời gian riêng |

## Đầu ra theo nhiệm vụ

- Mô tả/chẩn đoán: orders_analysis.csv; không suy diễn quan hệ nhân quả từ liên hệ quan sát. Các tên địa lý chưa khôi phục nằm trong nhóm __UNKNOWN__ có cờ.
- Dự báo: orders_model_features.csv, orders_model_labels.csv và orders_model_splits.csv. Chỉ FEATURES là đầu vào estimator; order_id và order_datetime chỉ để join/chia tập. Chưa huấn luyện/đánh giá mô hình. Tập này có điều kiện không hủy; không đại diện mọi đơn mới.
- Đề xuất cam kết: duration_distribution_by_mode_region.csv có phân vị và số đơn. Đây là phân phối lịch sử toàn mẫu để khám phá, không phải khuyến nghị hay feature huấn luyện; nếu đánh giá trên test phải tính lại phân vị chỉ từ train.
- Tối ưu tuyến: chưa đủ đầu vào. Phải bổ sung Solomon hoặc điểm dừng/xe/khung giờ phù hợp.

## Bất thường đã điều tra

First Class trễ 100% ở **37/37 tháng** có quan sát trong mẫu chính. Không tự sửa nhãn hay xóa nhóm. Xem anomalies_by_month_and_mode.csv và so sánh mô hình có/không Shipping Mode sau này.

Same Day có chênh lệch ±0,5 ngày giữa duration và khoảng timestamp. Dữ liệu không chứng minh cơ chế; không ép hai trường bằng nhau. Nếu chỉ giữ timestamp nhất quán thì mất toàn bộ Same Day, vì vậy bảng đó chỉ dùng độ nhạy, không thay mẫu chính.

| cohort | orders | late_count | late_rate | same_day_orders |
| --- | --- | --- | --- | --- |
| primary_source_duration | 62897 | 36048 | 0.573127 | 3407 |
| timestamp_consistent_only | 59490 | 34400 | 0.578248 | 0 |
| without_first_class_sensitivity | 53295 | 26446 | 0.496219 | 3407 |

## Chia tập lịch sử

| partition | orders | start | end |
| --- | --- | --- | --- |
| purged_boundary | 761 | 2016-12-25 00:02:00 | 2017-06-30 23:25:00 |
| test | 13071 | 2017-07-01 00:07:00 | 2018-01-31 23:38:00 |
| train | 39568 | 2015-01-01 00:00:00 | 2016-12-24 23:41:00 |
| validation | 9497 | 2017-01-01 00:33:00 | 2017-06-23 23:57:00 |

Các cut 01/01/2017 và 01/07/2017 được chốt trước huấn luyện. Chừa 7 ngày trước mỗi cut (lớn hơn duration tối đa 6 ngày của bản nguồn); dùng shipping timestamp làm proxy bổ sung. Thời điểm ghi nhận nhãn thật chưa được nguồn cung cấp nên đây chưa là chứng minh hết leakage. Mọi encoding/gán giá trị/scaling và tổng hợp lịch sử phải fit trên train. Không dùng dòng purged_boundary để fit hoặc chấm điểm.

Kiểm tra bàn giao: **24/24**. Xem analysis_validation.json; dictionary và allowlist tại docs/analysis_schema.json.
