# Nguyên tắc thiết kế Delivery Insights

## Bố cục và nhận diện

Canvas rộng 1440, cao 884; riêng Cam kết cao 936 để đủ chỗ cho tám thanh có nhãn. Thanh điều hướng ngang cao 72, gộp tên báo cáo và bốn trang chính.
Không có cột trái hoặc thông tin người phụ trách trong giao diện. Nội dung cách mép 28,
khoảng cách giữa các khối 16–20. Segoe UI dùng thống nhất; tiêu đề trang 26 pt, tiêu đề
biểu đồ 13 pt và nội dung 10–13 pt. Một thẻ chính nền đậm tạo điểm bắt đầu cho mỗi trang.
Ba thẻ còn lại bổ sung quy mô, mức đánh đổi hoặc nguồn lực cần thiết.

| Vai trò | Màu | Cách dùng |
| --- | --- | --- |
| Chữ chính, thanh điều hướng | #142D3B | Nền đậm chỉ dùng ở thanh trên và thẻ trọng tâm |
| Dữ liệu chính, thao tác | #087E7C | Màu ngọc nhất quán giữa các trang |
| Điểm cần cân nhắc | #AE6A3C | Dùng tiết chế, không biến mọi chỉ số thành cảnh báo |
| Chữ phụ | #627780 | Giải thích mẫu số, phạm vi và đơn vị |
| Nền trang | #F3F6F6 | Phân tách các khối trắng mà không cần bóng đổ |

Không dùng ảnh trang trí, hiệu ứng phát sáng hay biểu tượng không có chức năng. Chữ mô tả
ngắn, trực tiếp; số liệu và biểu đồ tạo điểm nhấn. Màu không phải cách duy nhất phân biệt
trạng thái: luôn giữ nhãn, tiêu đề hoặc chú giải đi cùng.

## Luồng phân tích

Tổng quan xếp tỷ lệ trễ theo phương thức, cạnh diễn biến tháng; bảng dưới đối chiếu cam kết
với thời gian thực tế. Rủi ro đặt độ chính xác cạnh độ bao phủ, cảnh báo và bỏ sót để thấy
khối lượng xử lý cùng hạn chế của mô hình. AP, ROC-AUC và log loss được đối chiếu trên
toàn tập test; không giả vờ thay đổi theo vùng.

Cam kết luôn giữ đủ năm phương án trong bảng, trong khi thẻ và biểu đồ đi theo lựa chọn
đang xem. Giảm vượt hẹn phải đi cùng số ngày khách chờ thêm. Không mô tả thay đổi cam kết
như cải thiện tốc độ giao thực tế.

Tuyến giao trình bày đường đi có thứ tự và màu theo xe. Biểu đồ so sánh chỉ dùng cùng cấu
hình; lịch trình được chuyển sang trang riêng để kiểm tra chi tiết mà không chiếm trang chính.
Không có đối chứng khả thi thì để trống tỷ lệ giảm. Các tham số nhiên liệu vẫn là giả định.

## Nội dung hiển thị

Giữ tên chỉ số, mẫu số cần thiết, phạm vi dữ liệu và đơn vị. Bỏ tên người phụ trách,
khẩu hiệu, hướng dẫn thao tác hiển nhiên, đoạn khuyến nghị chung và footer dài. Các lưu ý
phương pháp vẫn được giữ trong README và tài liệu chỉ số; giao diện chỉ giữ phần tránh
hiểu nhầm trực tiếp, như AP không đổi theo vùng hoặc sơ đồ Solomon không phải đường bộ.
Trang Cam kết dùng bảng thời gian cam kết theo phương thức thay đoạn khuyến nghị chung.

## Duy trì

Giữ mô đun dữ liệu, công thức, bản đồ tuyến và trình bày riêng. Định dạng thẻ số không thay
đổi measures số dùng cho biểu đồ. Cập nhật nguồn sinh cùng thay đổi trong Desktop trước khi
build lại. Kiểm tra trực tiếp nhãn dài, giá trị trống, tất cả trang, bộ lọc đồng bộ và nút chi tiết.


## Chống chồng lấn và sử dụng diện tích

Ô chỉ số có ba vùng độc lập: tiêu đề, định nghĩa ngắn và số. Native card chỉ vẽ số,
không dùng cơ chế tự căn chung với title/subtitle. Vùng số cao 60, đủ chiều cao dòng font
thực tế; luôn giữ khoảng cách với phần chữ trên. Bộ lọc cũng tách tiêu đề khỏi dropdown,
dropdown native cao 48 và có padding 8 mỗi phía. Các lớp nền được đánh dấu riêng;
chỉ lớp nền được phép nằm sau nội dung.

Bảng dùng độ rộng cột cố định theo tổng chiều rộng nội dung, không co theo chữ sau refresh.
Dữ liệu chữ căn trái, số căn phải trong cột riêng. Các bảng dùng khoảng 97% chiều rộng
khung ở các bảng rộng; các bảng nhỏ dùng khoảng 92–94%, phần còn lại là lề. Bỏ ba ô kết luận lớn bị lặp ở cuối Tổng quan, Rủi ro và Cam kết.
Bảng ở cuối các trang này trải hết hàng. Hai cột tuyến và lịch trình được cân theo tỷ lệ ảnh.
Nhãn thanh đơn và nhóm nằm ngoài đầu thanh, có khoảng dự phòng bên phải. Ở biểu đồ
thanh nhóm, mỗi hàng được cấp đủ chiều cao cho hai nhãn số, kể cả khi chúng bằng nhau.
Giữ đủ cả tám nhãn mặc định; không giải quyết chồng chữ bằng cách ẩn giá trị. Nhãn biểu đồ
xếp chồng nằm trong từng đoạn. Không kéo giãn hình học tuyến để lấp khung.

Kiểm tra nguồn bằng scripts/validate_powerbi.py và CLI Microsoft. Kiểm tra geometry thực
bằng scripts/check_powerbi_layout.cjs trên Desktop đã refresh: đo text so với vùng riêng,
các vùng tiền cảnh so với nhau, nhãn biểu đồ và độ phủ cột bảng. Bằng chứng nằm trong
reports/dashboard/native_layout_validation.json. Thực hiện lại sau thay font, kích thước,
nhãn hoặc cấu trúc bảng; ảnh chụp cần được xem thêm để đánh giá tính dễ đọc.
