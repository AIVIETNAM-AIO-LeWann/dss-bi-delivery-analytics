# 4. Biến chuyển đổi và định nghĩa KPI

Không dùng Compa-Ratio: chỉ số đó thuộc bài toán nhân sự, không phù hợp DataCo.
Danh mục đầy đủ, kiểu và thang đo ở [derived_variables.csv](derived_variables.csv).

## Nhóm biết tại lúc đặt hàng theo giả định dự án

| Biến | Quy tắc | Lưu ý |
| --- | --- | --- |
| order_year | Năm của order_datetime | Biến năm có thang khoảng |
| order_month | Tháng 1–12 | Có chu kỳ; không coi tháng 12 “gấp đôi” tháng 6 |
| order_weekday | Thứ Hai=0 đến Chủ nhật=6 | Mã nhãn có chu kỳ |
| order_is_weekend | 1 nếu thứ Bảy/Chủ nhật | Chỉ là quy ước lịch; không mặc định nghỉ làm ở mọi quốc gia |
| line_count | Số dòng hàng trong đơn | Chỉ có ở bảng orders; khác tổng số sản phẩm |
| total_quantity | Tổng item_quantity trong đơn | NA nếu một dòng thiếu hoặc không dương |
| sales_gross_total | Tổng Sales cấp dòng | Giả định đơn vị tiền nhất quán trong đơn; NA nếu thiếu/âm |
| item_total_net_sum | Tổng Order Item Total cấp dòng | Không cộng thêm Sales per customer là cột bản sao |

Các tổng cấp đơn chỉ được coi là biết lúc đặt hàng nếu snapshot dòng hàng/giá trị
là thông tin đã có khi đặt, không phải giá trị đã cập nhật sau đó. Giả định này
chưa được xác minh bằng nhật ký sự kiện của nguồn.

## Nhóm kết quả — chỉ phân tích hồi cứu hoặc tạo nhãn

```text
delay_days = shipping_days_actual - shipping_days_scheduled
late_days = max(delay_days, 0)
is_late_from_days = 1 nếu delay_days > 0, ngược lại 0
timestamp_span_days = (shipping_datetime - order_datetime) / 1 ngày
```

- `delay_days < 0`: sớm; `= 0`: khớp số ngày kế hoạch; `> 0`: vượt kế hoạch.
- Không có đầu vào thì kết quả tương ứng để thiếu; không coi thiếu là 0 ngày.
- `is_late_from_days` giữ độc lập với `late_delivery_risk`; đặc biệt **4.423 dòng hủy**
  có biến tính lại bằng 1 nhưng nhãn nguồn bằng 0.
- `timestamp_span_days` là khoảng giữa hai timestamp nguồn, chưa xác thực là thời
  gian vận chuyển đến tận tay khách hay thời gian xử lý kho.
- **9.737 dòng** có khoảng timestamp lệch số ngày thực tế, đều thuộc Same Day ở bản
  hiện tại; chênh lệch ±0,5 ngày. Không thay cột thực tế bằng phép trừ timestamp.

## Cờ quản lý mẫu và chất lượng

`is_shipping_canceled`, `delivery_kpi_eligible`, `invalid_logistics_flag`,
`duration_mismatch_flag`, hai cờ parse ngày và `order_header_conflict` phục vụ chọn
mẫu hoặc kiểm tra. Chúng không được đưa vào predictor tại lúc đặt hàng, vì có
thể chứa thông tin sau sự kiện hoặc làm lộ cách chọn mẫu.

`source_row_number` chỉ để tìm về dòng trong CSV raw. Không dùng làm biến giải thích.

## KPI được thống nhất trong repo

```text
Tỷ lệ trễ nguồn = sum(late_delivery_risk) / số đơn có nhãn hợp lệ trong toàn nguồn
Tỷ lệ trễ mẫu chính = số đơn trễ và delivery_kpi_eligible=1 / số đơn eligible
Thời gian trung bình = mean(shipping_days_actual) trên cùng mẫu và cùng cấp dữ liệu
```

Tỷ lệ đúng hạn, nếu dùng, là `1 - tỷ lệ trễ` **trên mẫu không hủy có nhãn hợp lệ**,
gồm cả sớm và đúng ngày. Không tính đơn hủy thành giao đúng hạn.

| Cấp đơn | Tử số | Mẫu số | Tỷ lệ trễ |
| --- | --- | --- | --- |
| Toàn nguồn | 36.048 | 65.752 | 54,82% |
| Mẫu chính không hủy, hợp lệ | 36.048 | 62.897 | 57,31% |
| Độ nhạy chỉ COMPLETE/CLOSED | 16.633 | 28.965 | 57,42% |

Các tỷ lệ theo nhóm luôn lấy tổng tử số chia tổng mẫu số; không trung bình giản
đơn các tỷ lệ vùng có quy mô khác nhau. Tỷ lệ dạng 0–1 trong CSV được định dạng
phần trăm khi trình bày, không nhân 100 hai lần.

## Chưa tạo

Khoảng cách kho–khách, tuyến xe, lít nhiên liệu, chi phí giao, ngày lễ và thiệt hại
do trễ chưa có căn cứ đầu vào. Không sinh ngẫu nhiên để làm biến giải thích.
One-hot encoding/scaling và tỷ lệ lịch sử theo vùng chưa thực hiện ở bước O;
nếu làm sau phải fit trên train và chỉ dùng thông tin quá khứ để tránh leakage.
