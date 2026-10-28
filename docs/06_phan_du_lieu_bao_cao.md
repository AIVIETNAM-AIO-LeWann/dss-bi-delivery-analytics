# Bản thảo phần O — Dữ liệu

Nội dung này phản ánh phạm vi DataCo đã thực hiện. Nhóm cần bổ sung phần Solomon
nếu triển khai tối ưu tuyến; không mô tả phần đó là đã hoàn thành.

## Nguồn và đặc điểm dữ liệu

Nhóm sử dụng file DataCoSupplyChainDataset.csv tải từ bộ DataCo Supply Chain dataset
do saicharankomati đăng trên Kaggle, ghim phiên bản 1. Nguồn xuất bản và tài liệu
mô tả được đối chiếu với DataCo SMART SUPPLY CHAIN FOR BIG DATA ANALYSIS của
Constante, Silva và Pereira trên Mendeley Data, DOI 10.17632/8gx2fvg2k6.5.
Nguồn Mendeley công bố giấy phép CC BY 4.0. Repo lưu thời điểm tải và checksum
để xác định chính xác bản CSV được sử dụng, chưa khẳng định các bản trên hai nền
tảng là giống hệt từng byte.

Dữ liệu gồm 180.519 dòng và 53 biến. Mỗi dòng là một dòng hàng, xác định duy nhất
bởi Order Item Id. Có 65.752 Order Id khác nhau, vì một đơn có thể chứa nhiều dòng
hàng. Thời điểm đặt hàng từ ngày 01/01/2015 đến 31/01/2018; timestamp shipment
đến ngày 06/02/2018. Dữ liệu có phương thức vận chuyển, số ngày kế hoạch/thực tế,
trạng thái và nhãn trễ, địa bàn đích, thông tin sản phẩm, khách hàng và giá trị bán.

## Từ điển dữ liệu

Nhóm lập Data Dictionary cho đủ 53 trường gốc, ghi tên gốc và tên chuẩn hóa, mô tả,
kiểu lưu trữ sau xử lý, thang đo, đơn vị, vai trò và cách xử lý. Các mã đơn, dòng
hàng, sản phẩm, khách và ZIP là dữ liệu định danh dù chỉ chứa chữ số. Tháng/thứ là
nhãn có chu kỳ. Timestamp có thang khoảng; số lượng và duration không âm có thang
tỷ lệ. Thang đo thứ bậc chưa được xác lập cho trường nào. Phương thức vận chuyển
không được tùy ý mã hóa thành cấp bậc số.

## Chất lượng và chuẩn bị dữ liệu

Quy trình thực hiện theo bốn bước: đảm bảo chất lượng, xác thực, làm sạch và khám
phá sơ bộ. File được đọc bằng Windows-1252, chuẩn hóa khoảng trắng đầu/cuối, chuyển
số và parse ngày theo MM/DD/YYYY HH:MM. Kiểu và quy tắc chuyển đổi được ghi trong
schema; file nguồn giữ nguyên.

Không có dòng trùng hoàn toàn, không thiếu khóa dòng và không có xung đột giữa các
trường header đã kiểm tra trong cùng một đơn. Các trường logistics đáp ứng các
quy tắc miền/nhãn/ngày đã triển khai. Kết quả đó chỉ xác nhận nhất quán nội bộ;
chưa chứng minh tính đầy đủ so với hệ thống doanh nghiệp gốc.

Product Description thiếu toàn bộ nên bị loại. Order Zipcode thiếu 155.679 dòng
(86,24%) được giữ NA và không dùng làm biến dự báo mặc định; Customer Zipcode có
3 ô thiếu cũng được giữ nguyên. Các trường tên, email, password và địa chỉ đường
khách không cần cho câu hỏi logistics nên bị loại, thay vì gán nội dung thiếu.
Ngoài ra, nhóm loại cột ảnh, cột Product Status hằng số và sáu cột bản sao sau khi
đối chiếu toàn bộ giá trị. Không xóa dòng hàng và không gán giá trị thay thế.

Đầu ra gồm bảng dòng hàng sạch 180.519 dòng, 54 cột bao gồm biến dẫn xuất, và bảng
đơn 65.752 dòng, 36 cột. Khi tổng hợp đơn, nhóm kiểm tra tính nhất quán header
trước và chỉ cộng các đại lượng cấp dòng đã quy định. Giảm số dòng khi tổng hợp
không được gọi là xóa bản ghi trùng.

## Biến chuyển đổi

Nhóm tạo chênh lệch ngày delay_days bằng số ngày shipping thực tế trừ số ngày kế
hoạch; late_days là phần dương của chênh lệch; is_late_from_days nhận 1 khi chênh
lệch lớn hơn 0. Các biến năm, tháng, thứ và cuối tuần được lấy từ ngày đặt hàng.
Bảng đơn có thêm số dòng hàng, tổng số lượng và tổng giá trị dòng trước/sau giảm
giá. Công thức và thang đo của từng biến nằm trong phụ lục Data Dictionary.

Nhãn Late_delivery_risk được giữ nguyên, không bị ghi đè bằng biến tính lại. Có
4.423 dòng hủy với chênh lệch ngày dương nhưng nhãn nguồn bằng 0. Khoảng giữa hai
timestamp cũng khác số ngày shipping thực tế ở 9.737 dòng thuộc Same Day. Nhóm
giữ hai đại lượng, gắn cờ và ghi nhận sự không chắc chắn, không tự sửa nguồn.

## Mẫu phân tích và giả định

KPI chính tính cấp đơn trên mẫu không có trạng thái Shipping canceled và đạt kiểm
tra logistics, gồm 62.897 đơn; tỷ lệ nhãn trễ là 36.048/62.897 = 57,31%. Tỷ lệ
trên toàn bộ 65.752 đơn là 54,82%, còn khi chỉ giữ trạng thái COMPLETE/CLOSED là
57,42%. Nhóm báo cáo đồng thời ba định nghĩa để làm rõ ảnh hưởng của chọn mẫu,
không gọi mọi đơn không hủy là đơn đã giao được xác thực.

Sổ giả định ghi rõ đơn vị phân tích, chính sách đơn hủy, cách dùng nhãn và duration,
mốc dự báo dự kiến tại lúc đặt hàng, sự sẵn có của candidate, timezone, đơn vị tiền,
encoding và quy tắc tổng hợp. Giả định chưa có bằng chứng được đánh dấu chưa xác
minh. Khi triển khai dự báo, các trường kết quả, timestamp shipment và trạng thái
snapshot chưa rõ thời điểm không được dùng như thông tin đã biết tại lúc đặt.

## Hạn chế

Timestamp shipment không được nguồn xác nhận là thời điểm khách nhận hàng. Tọa độ
Latitude/Longitude là vị trí cửa hàng, không phải điểm nhận. Bộ dữ liệu không có
xe, sức chở, khung giờ, tuyến thực hay nhiên liệu nên chưa đủ giải tối ưu tuyến.
Loại tiền chưa xác minh, chưa có chi phí vận tải hay thiệt hại do trễ. Một số địa
danh có dấu hỏi ngay trong nguồn. Dữ liệu lịch sử quốc tế không tự động đại diện
cho logistics Việt Nam hiện tại.

Trong mẫu chính, First Class có tỷ lệ trễ 100%; đây là bất thường cần kiểm tra
nguồn và tính ổn định theo thời gian, không được suy rộng thành quy luật thực tế.
Quan hệ quan sát giữa phương thức, vùng và trễ chưa chứng minh quan hệ nhân quả.

Phụ lục kèm theo: Data Dictionary, sổ giả định, nhật ký chuẩn bị dữ liệu, bảng
profile, thống kê sơ bộ và KPI có mẫu số. Mã nguồn chạy lại từ CSV gốc nằm trong repo.
