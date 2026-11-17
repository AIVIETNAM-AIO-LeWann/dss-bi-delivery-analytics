# Nguyên tắc thiết kế Delivery Insights

Giao diện là một bảng điều khiển kho vận: mặt giấy ấm, các khối nổi và ô lọc lõm, một dải nhãn
kraft mang kết luận. Bản mockup tham chiếu nằm ở `dashboards/design/mockup_v6.html`; bản Power BI
giữ cấu trúc, màu và logic tương tác, bỏ các hiệu ứng mà Power BI không có.

## Canvas và bố cục

Mọi trang rộng 1440, cao 1000. Cột trái 100 là thanh bên (logo, bốn phím trang, bảng dữ liệu và
nhiệt kế tỷ lệ trễ toàn kỳ). Nội dung bắt đầu ở x=140, rộng 1272. Từ trên xuống: tiêu đề và ô lọc
(cao 72), dải kết luận (cao 38), rồi ba hàng khối cách nhau 16. Một trang đọc theo thứ tự: kết luận,
chỉ số chính, so sánh theo nhóm, diễn biến.

| Vai trò | Màu | Cách dùng |
| --- | --- | --- |
| Nền trang | #E4E0D7 | Giấy ấm, nền cho mọi khối |
| Mặt khối nổi | #EAE7DF | Khối nổi bằng hai lớp bóng |
| Ô lõm | #D7D3C8 | Ô lọc, thanh bên, rãnh |
| Chữ chính | #1D2A33 | Mực xanh đen |
| Chữ phụ | #5E6D76 | Mẫu số, phạm vi, đơn vị |
| Trễ, rủi ro | #D2472A | Đỏ chu sa, chỉ dùng cho điều xấu |
| Đúng hạn, ổn | #0E7C86 | Xanh dầu |
| Thận trọng | #B8860B | Vàng đồng, cảnh báo sai |
| Trung tính | #8E9AA3 | Tổng thể, chỉ số không phán xét |

Cặp đỏ và xanh dầu đã qua kiểm tra phân biệt cho người mù màu (ΔE 12,9). Màu không phải cách duy
nhất phân biệt: luôn có nhãn, chú giải hoặc số đi kèm. Font Segoe UI; số lớn dùng Segoe UI Light.

## Chất liệu: nổi và lõm

Ánh sáng đến từ góc trên trái. Khối nổi là hai hình chồng nhau, mỗi hình một bóng đổ native: lớp dưới
bóng sáng lệch lên trái, lớp trên bóng ấm lệch xuống phải. Ô lõm là một hình có bóng trong (Inner).
Các lớp này được đánh dấu `designRole = background` để bộ kiểm tra bỏ qua khi xét chồng chéo; mọi
visual có nội dung vẫn không được chồng nhau. Hằng số bóng nằm ở đầu `powerbi_report.py`
(`BIG_LIGHT`, `BIG_DARK`, `SMALL_*`, `INSET`), đổi một chỗ là đổi toàn báo cáo.

Phím trang hiện tại được vẽ lõm kèm đèn đỏ; ba phím còn lại nổi và bấm để chuyển trang. Mỗi trang
tự vẽ trạng thái này vì nút bấm native không biết trang đang mở.

## Nội dung động, không số cứng

Dải kết luận và các câu chữ dưới biểu đồ là measure DAX, nên đúng theo bộ lọc. Không viết số hay
nhận định cố định vào hộp chữ. Các hình trang trí có dữ liệu là measure SVG (dataCategory
ImageUrl, ẩn trong thư mục Hình ảnh), hiển thị bằng visual hình ảnh như bản đồ tuyến:

| Measure | Hình |
| --- | --- |
| Logo | Khối hộp hàng hóa và chấm tín hiệu đỏ |
| Vòng tỷ lệ trễ, Vòng độ chính xác, Vòng độ bao phủ, Vòng vượt hẹn | Vòng tiến độ lõm, có núm kéo |
| Thanh tỷ lệ trễ | Thanh nổi trong rãnh, vạch đứt là trung bình toàn kỳ |
| Nhiệt kế toàn kỳ | Nhiệt kế dọc ở thanh bên, không đổi theo bộ lọc |
| Bàn phím nhiệt | Phương thức × thị trường, màu từ xanh dầu qua giấy tới đỏ quanh trung bình |
| Phễu phát hiện | Từ đơn kiểm tra đến cảnh báo đúng và bỏ sót |

Mã sinh các measure này nằm ở `src/dss_bi_delivery/powerbi_svg.py`. Chuỗi đã mã hóa phần trăm;
số định dạng bằng `FORMAT(..., "en-US")` để dấu thập phân không phá URI.

## Luồng phân tích và những điều không được nói

Tổng quan đặt bốn phương thức làm trung tâm: tỷ lệ trễ, cam kết so với thực tế, phần đóng góp vào
tổng đơn trễ. Bong bóng ưu tiên đặt khối lượng cạnh tỷ lệ để thấy nhóm lớn nhưng trễ ít vẫn có nhiều
đơn trễ. Phím nhiệt chỉ ra thị trường ít làm đổi kết quả. Rủi ro đặt độ chính xác cạnh độ bao phủ và
nêu rõ số đơn bị bỏ sót. AP, ROC-AUC và log loss lấy trên toàn tập test; không giả vờ đổi theo vùng.

Cam kết luôn giữ đủ năm phương án; thẻ và biểu đồ đi theo phương án đang chọn. Giảm vượt hẹn phải
đi cùng số ngày khách chờ thêm. Không mô tả thay đổi cam kết như cải thiện tốc độ giao thực tế.

Tuyến giao dùng tọa độ Solomon, không phải km đường bộ. Nhiên liệu là giả định mô phỏng và được
ghi rõ như vậy ngay trên thẻ. Không có đối chứng khả thi thì để trống tỷ lệ giảm.

## Duy trì

Giữ mô đun dữ liệu, công thức, hình SVG, bản đồ tuyến và trình bày riêng. Nguồn thiết kế ở
`powerbi_report.py`, hình SVG ở `powerbi_svg.py`, model và measure ở `powerbi_model.py`. Cập nhật nguồn
sinh cùng thay đổi trong Desktop trước khi build lại: Desktop lưu lại file với phiên bản lược đồ mới
hơn, `scripts/build_powerbi.py` sẽ ghi đè toàn bộ file đã sinh.

Khi mở bản mới lần đầu, những điều cần kiểm tra trực tiếp trong Desktop vì bộ kiểm tra lược đồ không
chứng minh được: giá trị thuộc tính bóng đổ (`preset`, `position`, `angle`) cho ra đúng nổi và lõm;
mọi measure SVG và measure chữ tính được, không báo lỗi DAX; thuộc tính riêng của biểu đồ phân tán,
biểu đồ đường thu nhỏ và bảng; số liệu trên thẻ khớp mục Đối chiếu số liệu trong README; nhãn dài,
giá trị trống và bộ lọc đồng bộ giữa các trang.
