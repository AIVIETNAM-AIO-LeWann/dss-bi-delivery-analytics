# Data Dictionary

Tự sinh bởi `python scripts/prepare_data.py`. Sửa metadata tại `scripts/schema.py`.

Thang đo: nominal = định danh; nominal_binary = định danh nhị phân; interval = khoảng; ratio = tỷ lệ. Không có biến thứ bậc được xác lập trong bộ này. Mã số vẫn là định danh.

`assumed_at_order` là giả định cần kiểm chứng, không phải lịch sử sự kiện đã được nguồn xác nhận. Đơn vị tiền tệ chưa được xác minh; không tự đổi sang VND hoặc mặc định USD.

## 53 trường nguồn

| source_column | column | dtype | measurement_scale | unit | role | availability_at_prediction | treatment | description_vi |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Type | payment_type | string | nominal | nhãn | candidate | assumed_at_order | keep | Loại giao dịch thanh toán; không phải phương thức vận chuyển. |
| Days for shipping (real) | shipping_days_actual | Int64 | ratio | ngày | outcome | after_order | keep | Số ngày shipping thực tế theo chỉ báo nguồn; chưa xác thực là thời gian khách nhận hàng. |
| Days for shipment (scheduled) | shipping_days_scheduled | Int64 | ratio | ngày | candidate | assumed_at_order | keep | Số ngày shipping cam kết; Same Day bằng 0 là giá trị hợp lệ. |
| Benefit per order | benefit_per_order | Float64 | ratio | tiền nguồn chưa xác minh loại tiền | outcome | after_order | drop_duplicate | Trùng giá trị với Order Profit Per Order trong bản đã kiểm tra; không cộng cả hai. |
| Sales per customer | sales_per_customer | Float64 | ratio | tiền nguồn chưa xác minh loại tiền | duplicate | unverified | drop_duplicate | Trùng Order Item Total; không diễn giải thành tổng chi tiêu suốt đời khách hàng. |
| Delivery Status | delivery_status | string | nominal | nhãn | outcome | after_order | keep | Kết quả shipping: sớm; trễ; đúng hạn; hủy. Không phải đầu vào dự báo tại lúc đặt hàng. |
| Late_delivery_risk | late_delivery_risk | Int64 | nominal_binary | 0/1 | target | after_order | keep | Nhãn trễ ghi nhận trong dữ liệu; không phải xác suất dự báo. Đơn hủy có nhãn 0. |
| Category Id | category_id | string | nominal | mã | identifier | assumed_at_order | keep | Mã danh mục; không tính trung bình mã; không giả định tên danh mục là khóa duy nhất. |
| Category Name | category_name | string | nominal | nhãn | candidate | assumed_at_order | keep | Tên danh mục sản phẩm; chuẩn hóa khoảng trắng đầu cuối. |
| Customer City | customer_city | string | nominal | nhãn | context | unverified | keep | Thành phố nơi khách mua theo nguồn; khác Order City là thành phố đích. |
| Customer Country | customer_country | string | nominal | nhãn | context | unverified | keep | Quốc gia nơi khách mua theo nguồn; không dùng thay quốc gia đích. |
| Customer Email | customer_email | string | nominal | văn bản | excluded | unverified | drop_personal | Email trong nguồn; không cần cho câu hỏi logistics. |
| Customer Fname | customer_first_name | string | nominal | văn bản | excluded | unverified | drop_personal | Tên khách; không cần cho câu hỏi logistics. |
| Customer Id | customer_id | string | nominal | mã | identifier | assumed_at_order | keep | Mã khách; giữ để kiểm tra và liên kết; không đưa mã số thô vào mô hình. |
| Customer Lname | customer_last_name | string | nominal | văn bản | excluded | unverified | drop_personal | Họ khách; thiếu 8 dòng ở bản nguồn này; loại cột thay vì gán tên. |
| Customer Password | customer_password | string | nominal | văn bản | excluded | unverified | drop_personal | Trường khóa được che theo nguồn; không phục vụ phân tích. |
| Customer Segment | customer_segment | string | nominal | nhãn | candidate | assumed_at_order | keep | Phân khúc Consumer; Corporate; Home Office. Giả định phân khúc đã biết khi đặt hàng. |
| Customer State | customer_state | string | nominal | nhãn | context | unverified | keep | Bang gắn với nơi mua/cửa hàng theo mô tả nguồn; không thay cho Order State. |
| Customer Street | customer_street | string | nominal | văn bản | excluded | unverified | drop_personal | Địa chỉ đường trong thông tin khách; không cần cho bài hiện tại. |
| Customer Zipcode | customer_zipcode | string | nominal | mã bưu chính | context | unverified | keep_missing | Mã bưu chính; giữ dạng chuỗi và giá trị thiếu; không tự thêm số 0 đầu. |
| Department Id | department_id | string | nominal | mã | identifier | assumed_at_order | keep | Mã bộ phận hàng hóa. |
| Department Name | department_name | string | nominal | nhãn | candidate | assumed_at_order | keep | Tên bộ phận hàng hóa; bỏ khoảng trắng thừa ở hai đầu. |
| Latitude | store_latitude | Float64 | interval | độ | geographic_reference | unverified | keep | Vĩ độ cửa hàng theo từ điển gốc; không phải tọa độ điểm giao. |
| Longitude | store_longitude | Float64 | interval | độ | geographic_reference | unverified | keep | Kinh độ cửa hàng theo từ điển gốc; không đủ để tính tuyến đến khách. |
| Market | market | string | nominal | nhãn | candidate | assumed_at_order | keep | Thị trường đích; có 5 giá trị ở bản nguồn. |
| Order City | order_city | string | nominal | nhãn | candidate | assumed_at_order | keep | Thành phố đích; một số tên có dấu hỏi nên chưa dùng geocoding tự động. |
| Order Country | order_country | string | nominal | nhãn | candidate | assumed_at_order | keep | Quốc gia đích; không đồng nhất với Customer Country. |
| Order Customer Id | order_customer_id | string | nominal | mã | identifier | assumed_at_order | drop_duplicate | Bằng Customer Id ở toàn bộ bản nguồn; giữ Customer Id làm cột chuẩn. |
| order date (DateOrders) | order_datetime | datetime | interval | thời gian không có múi giờ | time_index | at_order | keep | Thời điểm đặt hàng; parse MM/DD/YYYY HH:MM; không tự gán UTC hay múi giờ Việt Nam. |
| Order Id | order_id | string | nominal | mã | identifier | at_order | keep | Mã đơn; lặp lại hợp lệ qua các dòng hàng; khóa của bảng orders. |
| Order Item Cardprod Id | order_item_product_id | string | nominal | mã | identifier | assumed_at_order | drop_duplicate | Mã sản phẩm trên dòng hàng; bằng Product Card Id ở bản nguồn. |
| Order Item Discount | item_discount | Float64 | ratio | tiền nguồn chưa xác minh loại tiền | candidate | assumed_at_order | keep | Tiền giảm giá dòng hàng; giữ nguyên giá trị và sai số số thực. |
| Order Item Discount Rate | item_discount_rate | Float64 | ratio | tỷ lệ 0–1 | candidate | assumed_at_order | keep | Tỷ lệ giảm giá ghi sẵn; không ép bằng item_discount chia sales khi chưa rõ cơ chế làm tròn. |
| Order Item Id | order_item_id | string | nominal | mã | identifier | at_order | keep | Khóa duy nhất của dòng hàng; dùng phát hiện bản ghi trùng. |
| Order Item Product Price | item_unit_price | Float64 | ratio | tiền nguồn chưa xác minh loại tiền | candidate | assumed_at_order | keep | Đơn giá trước giảm giá; trùng Product Price ở bản nguồn. |
| Order Item Profit Ratio | item_profit_ratio | Float64 | ratio | tỷ lệ có thể âm | outcome | unverified | keep | Tỷ lệ lợi nhuận do nguồn cung cấp; âm không mặc định là lỗi; chưa dùng làm predictor. |
| Order Item Quantity | item_quantity | Int64 | ratio | sản phẩm | candidate | assumed_at_order | keep | Số lượng sản phẩm của dòng hàng; phải nguyên dương. |
| Sales | sales_gross | Float64 | ratio | tiền nguồn chưa xác minh loại tiền | candidate | assumed_at_order | keep | Giá trị bán trước giảm giá cấp dòng; đối chiếu đơn giá nhân số lượng với dung sai số thực. |
| Order Item Total | item_total_net | Float64 | ratio | tiền nguồn chưa xác minh loại tiền | candidate | assumed_at_order | keep | Giá trị sau giảm giá cấp dòng theo đối chiếu thực nghiệm; không phải tổng đơn lặp trên từng dòng. |
| Order Profit Per Order | order_profit_per_order | Float64 | ratio | tiền nguồn chưa xác minh loại tiền | outcome | after_order | keep | Tên cột gợi lợi nhuận đơn nhưng giá trị biến thiên theo dòng; chưa khẳng định ngữ nghĩa kế toán hay dùng tổng lợi nhuận đơn. |
| Order Region | order_region | string | nominal | nhãn | candidate | assumed_at_order | keep | Vùng đích; chuẩn hóa khoảng trắng hai đầu. |
| Order State | order_state | string | nominal | nhãn | candidate | assumed_at_order | keep | Bang hoặc tỉnh đích; không nhầm với Order Status là trạng thái đơn. |
| Order Status | order_status | string | nominal | nhãn | outcome | snapshot_time_unknown | keep | Trạng thái snapshot của đơn; chưa chứng minh biết tại lúc đặt hàng nên loại khỏi tập predictor. |
| Order Zipcode | order_zipcode | string | nominal | mã bưu chính | context | unverified | keep_missing | Mã bưu chính đích; trường không có trong từ điển gốc được tham khảo; diễn giải theo tên cột. |
| Product Card Id | product_id | string | nominal | mã | identifier | assumed_at_order | keep | Mã sản phẩm chuẩn; không coi thứ tự mã là đại lượng số. |
| Product Category Id | product_category_id | string | nominal | mã | identifier | assumed_at_order | drop_duplicate | Bằng Category Id ở bản đã kiểm tra; giữ Category Id. |
| Product Description | product_description | string | nominal | văn bản | excluded | unverified | drop_empty | Mô tả sản phẩm; thiếu toàn bộ ở bản nguồn nên không gán nội dung. |
| Product Image | product_image | string | nominal | URL | excluded | unverified | drop_irrelevant | Đường dẫn ảnh; không phục vụ câu hỏi dữ liệu ban đầu. |
| Product Name | product_name | string | nominal | nhãn | candidate | assumed_at_order | keep | Tên sản phẩm; chuẩn hóa khoảng trắng đầu cuối. |
| Product Price | product_price | Float64 | ratio | tiền nguồn chưa xác minh loại tiền | duplicate | assumed_at_order | drop_duplicate | Bằng Order Item Product Price ở toàn bộ bản nguồn; giữ đơn giá dòng hàng. |
| Product Status | product_status | Int64 | nominal_binary | 0/1 | excluded | snapshot_time_unknown | drop_constant | Chỉ báo tồn khả dụng theo nguồn; toàn 0 ở bản này nên không tạo thông tin phân biệt. |
| shipping date (DateOrders) | shipping_datetime | datetime | interval | thời gian không có múi giờ | outcome | after_order | keep | Thời điểm shipment theo nguồn; không tự đổi tên thành ngày khách nhận hàng. |
| Shipping Mode | shipping_mode | string | nominal | nhãn | candidate | assumed_at_order | keep | Standard Class; First Class; Second Class; Same Day. Không mã hóa thành thứ bậc số tùy ý. |

## Biến dẫn xuất và biến tổng hợp cấp đơn

| column | dtype | measurement_scale | unit | role | formula_or_rule_vi | availability_at_prediction |
| --- | --- | --- | --- | --- | --- | --- |
| source_row_number | Int64 | nominal | dòng CSV | trace | Số dòng dữ liệu gốc + 2; số 1 là header | not_feature |
| order_year | Int64 | interval | năm | candidate | year(order_datetime) | at_order |
| order_month | Int64 | nominal_cyclic | tháng | candidate | month(order_datetime); 1–12 | at_order |
| order_weekday | Int64 | nominal_cyclic | thứ | candidate | dayofweek(order_datetime); thứ Hai=0 đến Chủ nhật=6 | at_order |
| order_is_weekend | Int64 | nominal_binary | 0/1 | candidate | 1 nếu weekday thuộc {5;6}; không coi là ngày nghỉ ở mọi quốc gia | at_order |
| delay_days | Int64 | interval | ngày | outcome | shipping_days_actual - shipping_days_scheduled; âm=sớm | after_order |
| late_days | Int64 | ratio | ngày | outcome | max(delay_days;0); không ép thành nhãn gốc | after_order |
| is_late_from_days | Int64 | nominal_binary | 0/1 | outcome | 1 nếu delay_days>0; NA nếu thiếu duration; vẫn có thể bằng 1 trên đơn hủy | after_order |
| is_shipping_canceled | Int64 | nominal_binary | 0/1 | outcome | 1 nếu delivery_status='Shipping canceled' | after_order |
| timestamp_span_days | Float64 | ratio | ngày | outcome | (shipping_datetime-order_datetime).total_seconds()/86400; chỉ là khoảng hai timestamp | after_order |
| duration_mismatch_flag | Int64 | nominal_binary | 0/1 | quality | 1 nếu timestamp_span_days khác shipping_days_actual quá 1e-8 hoặc thiếu đầu vào | after_order |
| order_date_parse_failed | Int64 | nominal_binary | 0/1 | quality | 1 nếu ngày gốc không rỗng nhưng parse thất bại | not_feature |
| shipping_date_parse_failed | Int64 | nominal_binary | 0/1 | quality | 1 nếu ngày gốc không rỗng nhưng parse thất bại | not_feature |
| invalid_logistics_flag | Int64 | nominal_binary | 0/1 | quality | 1 nếu logistics/khóa/ngày/nhãn không đạt quy tắc; xem script và nhật ký | not_feature |
| delivery_kpi_eligible | Int64 | nominal_binary | 0/1 | cohort | 1 nếu delivery_status sớm/đúng hạn/trễ và invalid_logistics_flag=0; không chứng minh khách đã nhận | after_order |
| line_count | Int64 | ratio | dòng hàng | candidate | count(order_item_id) trong đơn | assumed_at_order |
| total_quantity | Int64 | ratio | sản phẩm | candidate | sum(item_quantity); chỉ tính nếu không thiếu và nguyên dương toàn đơn | assumed_at_order |
| sales_gross_total | Float64 | ratio | tiền nguồn chưa xác minh loại tiền | candidate | sum(sales_gross); không cộng nếu có ô thiếu hoặc âm trong đơn | assumed_at_order |
| item_total_net_sum | Float64 | ratio | tiền nguồn chưa xác minh loại tiền | candidate | sum(item_total_net); không cộng nếu có ô thiếu hoặc âm trong đơn | assumed_at_order |
| order_header_conflict | Int64 | nominal_binary | 0/1 | quality | 1 nếu các dòng cùng order_id không nhất quán ở ORDER_FIELDS; các trường mâu thuẫn để trống | not_feature |
