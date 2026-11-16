# 5. Sổ giả định

Bảng có thể cập nhật tại [assumption_log.csv](assumption_log.csv). “Đã đối chiếu
nội bộ” chỉ xác nhận đặc tính file, không xác nhận quy trình vận hành ngoài đời.

| Mã | Giả định/quy ước | Căn cứ | Ảnh hưởng và cách kiểm tra |
| --- | --- | --- | --- |
| A01 | KPI logistics chính tính cấp đơn | Khóa Order Item Id duy nhất; Order Id lặp; header đã kiểm tra nhất quán | So sánh KPI cấp dòng và cấp đơn; không xóa dòng lặp mã đơn |
| A02 | Mẫu KPI chính loại Shipping canceled; giữ các trạng thái khác khi chỉ báo logistics hợp lệ | Đơn hủy mang nhãn 0; các trạng thái pending vẫn có outcome trong snapshot | Đã so sánh toàn nguồn và COMPLETE/CLOSED; không coi non_canceled là đã giao được xác thực |
| A03 | Dùng nhãn Late_delivery_risk gốc, không thay bằng delay_days>0 trên toàn nguồn | Hai đại lượng khác nhau ở các dòng hủy | Đã đối chiếu bảng chéo; 4.423 dòng hủy khác nhãn tính lại |
| A04 | Dùng Days for shipping (real) làm chỉ báo duration chính của nguồn | Trường được nguồn cung cấp; timestamp span khác ±0,5 ngày ở Same Day | Chưa xác minh cơ chế; giữ cờ và cần độ nhạy nếu phân tích Same Day hoặc đổi cam kết |
| A05 | Mốc dự báo dự kiến là lúc đặt hàng | Mục tiêu hỗ trợ cam kết/cảnh báo sớm, phù hợp hướng chủ đề 18 | Mọi trường outcome, snapshot chưa rõ thời điểm và cờ chọn mẫu không là predictor |
| A06 | Một số trường candidate đã có khi đặt hàng | Hợp lý về nghiệp vụ nhưng không có lịch sử sự kiện chứng minh | Chưa xác minh; rà lại từng trường trước huấn luyện, không công bố là đã hết leakage |
| A07 | Thời gian nguồn chưa có timezone; cuối tuần quy ước là thứ Bảy/Chủ nhật | Chuỗi ngày không có offset; dữ liệu nhiều quốc gia | Không đổi giờ; không diễn giải weekend là ngày nghỉ; kiểm tra lại nếu phân tích theo múi giờ |
| A08 | Giá trị tiền cùng đơn có cùng đơn vị | Cần để cộng giá trị cấp dòng; chưa có mã tiền trong dữ liệu | Chưa xác minh; không ghi USD/VND hoặc cộng thành báo cáo tài chính toàn cầu được xác thực |
| A09 | CP1252 là cách giải mã làm việc cho bản CSV đã tải | UTF-8 lỗi; CP1252 strict thành công; Latin-1 tạo 20 C1, CP1252 không tạo C1 | Đã đối chiếu byte/giải mã; địa danh chứa dấu hỏi vẫn chưa được phục hồi |
| A10 | Bảng đơn lấy header chung sau kiểm tra và cộng quantity/giá trị dòng | Không có xung đột ở toàn bộ trường header đã chọn trong bản này | Nếu có xung đột trong bản khác thì để thiếu/gắn cờ; không lấy một dòng tùy ý |
| A11 | Tọa độ là cửa hàng; không có mạng tuyến được quan sát | Từ điển gốc Latitude/Longitude; đề môn học trang 41 | Chưa tính khoảng cách/tuyến/chi phí; bổ sung dataset thích hợp nếu làm tối ưu tuyến |
| A12 | Các cặp cột bản sao chỉ cần một cột chuẩn | So sánh toàn bộ giá trị của bản đang dùng | Pipeline dừng nếu cặp cột không còn bằng nhau; không suy rộng sang bản mới |
| A13 | Địa danh hỏng không được đoán lại; dùng nhóm __UNKNOWN__ có cờ trong bảng phân tích | Không thể đảo ngược dấu hỏi thành tên duy nhất từ nguồn | 37 đơn thiếu độ tin cậy cấp city; 100 đơn cấp state trong mẫu chính; không gọi placeholder là giá trị đã sửa |
| A14 | Bảng chính dùng duration nguồn; bảng timestamp nhất quán chỉ là độ nhạy | Mọi Same Day đều lệch ±0,5 ngày | Bảng đối chiếu 59.490 đơn mất Same Day; không dùng làm mẫu chính để tránh mất cả phương thức |
| A15 | Train trước 2017; validation nửa đầu 2017; test từ 01/07/2017; chừa 7 ngày trước cut | Thiết kế đánh giá lịch sử trước huấn luyện; gap lớn hơn duration tối đa nguồn 6 ngày | 761 đơn ở purged_boundary; chưa có thời điểm nhãn thật, shipment chỉ là proxy |
| A16 | Mô hình dự kiến có điều kiện không hủy; candidate chỉ được giả định biết lúc đặt | Cohort tạo từ snapshot lịch sử có outcome | Chưa xác minh cho vận hành thực; cần mở rộng hủy/ba trạng thái nếu dự báo mọi đơn mới |
| A17 | Phân vị toàn mẫu chỉ phục vụ khám phá chính sách | Tính từ lịch sử theo vùng/phương thức | Đánh giá ngoài mẫu phải tính lại từ train; chưa đặt chi phí hoặc mục tiêu dịch vụ |

## Những giả định chưa cần đặt ở bước này

Chưa chọn mục tiêu dịch vụ 90%/95%, số xe, sức chở, tiêu hao nhiên liệu, giá nhiên
liệu, chi phí một ngày trễ hay mức tiết kiệm kỳ vọng. Chọn các số này bây giờ sẽ
là đặt đầu vào tùy ý trước khi nhóm chốt câu hỏi quyết định và nguồn bổ sung.

Khi bổ sung một giả định định lượng, ghi giá trị, đơn vị, nguồn/ngày tham chiếu,
KPI chịu ảnh hưởng và khoảng kiểm tra độ nhạy. Đánh dấu “chưa kiểm tra” thay vì ghi
“không ảnh hưởng” khi chưa chạy thử.
