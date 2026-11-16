# Bối cảnh và trạng thái dự án

Ngày rà soát: 16/11/2026. Đây là kết quả đọc tài nguyên được cung cấp; chưa phải xác nhận nghiệm thu của nhóm.

## Phạm vi và bằng chứng

Đề bài: `references/coursework/assignment_topics.pdf`, quy tắc chung trang 1–4,
Chủ đề 18 trang 40–41. Prompt chung chứa 20 chủ đề; chỉ Chủ đề 18 liên quan dự án này.
Bảng phân công: `references/team/team_assignments_hk261.xlsx`, sheet PHÂN CÔNG.
Bảng này còn mô tả IBM HR/Attrition từ đề cũ; giữ nguyên bản nguồn và ghi nhận mâu thuẫn ở đây.
Các đầu ra kỹ thuật TV2–TV5 đều triển khai DataCo/Solomon, nên tài liệu vận hành dùng phạm vi Chủ đề 18.
Không dùng phần nhân sự làm yêu cầu Dashboard logistics.

Repo ban đầu chỉ chứa bước O. Nay đã nhập các bộ A: mô tả/chẩn đoán, dự báo, đề xuất.
Chưa có bản báo cáo riêng của Phương Quỳnh, Dashboard Power BI hoặc slide hoàn chỉnh.
DHL là bối cảnh tham chiếu trong TV5, không phải bằng chứng dữ liệu vận hành thực tế của DHL.

## Luồng dữ liệu

CSV raw ghim checksum → mã chuẩn bị TV2 → bảng analysis/features/labels/splits.
Analysis → TV3 bảng mô tả; features/labels/splits → TV4 dự báo.
Analysis + dự báo + Solomon → TV5 kịch bản cam kết và tuyến.
TV2–TV5 → Dashboard Anh Quốc → thông điệp, báo cáo và slide nhóm.

## Kết quả và giới hạn cần giữ khi trình bày

- Nguồn: 180.519 dòng hàng, 65.752 đơn. Mẫu không hủy: 62.897 đơn.
- Dự báo: train 39.568; validation 9.497; test 13.071; khoảng đệm 761.
- TV4 chọn baseline theo phương thức bằng log loss validation. Có bốn mức P_Late;
  các đơn cùng phương thức không được phân biệt rủi ro riêng. Test AUC khoảng 0,746.
- P_Late là xác suất theo cam kết cũ, có điều kiện không hủy; không phải hiệu quả can thiệp.
- TV3 có cách diễn giải p > 0,05 là “hoàn toàn độc lập”; khi viết chung cần sửa thành
  “chưa tìm thấy bằng chứng về liên hệ trong phép kiểm định này”. Không sửa báo cáo gốc ngầm.
- TV5 thay cam kết có thể giảm tỷ lệ vượt hẹn tính lại, không chứng minh thời gian giao thực giảm.
- Solomon độc lập với DataCo. Đơn vị quãng đường benchmark chưa phải km; nhiên liệu/giá là giả định.
- C101 sức chở 200 cần tối thiểu 10 xe theo cận dưới và tuyến khả thi đã bàn giao;
  không ép kết quả này thành kịch bản 5 xe × 500 kg trong workbook.
- Nguồn Kaggle trong prompt và manifest khác slug; chưa chứng minh giống byte.
- Python/thư viện TV2, TV4, TV5 ghim khác phiên bản. Dùng môi trường riêng, không gộp requirements tùy tiện.

## Việc kế tiếp của Anh Quốc

Theo workbook: Dashboard hạn 15/11, thông điệp nhóm hạn 19/11, báo cáo 26/11, slide 28/11/2026.
Dashboard đã qua hạn theo bảng; chưa tạo sản phẩm Dashboard trong đợt tổ chức thư mục này.
Ưu tiên xác minh dữ liệu ghép, định nghĩa KPI, rồi dựng visual/what-if và phối hợp người viết thông điệp.

## Cập nhật triển khai Dashboard ngày 16/11/2026

Đã có nguồn Power BI bốn trang, sáu bảng đầu vào được kiểm tra, bản xem trước offline và nháp thông điệp phần VI.
Đã khắc phục môi trường thư viện; 11/11 unittest đạt. Sau đó đã tìm thấy Power BI Store và kiểm tra trực tiếp. Báo cáo đã mở/refresh; 21 kiểm tra DAX native đạt.
Trạng thái phần VI: có Dashboard kỹ thuật và bản viết bàn giao; Anh Quốc/nhóm rà thông điệp trước khi nộp.


## Nâng cấp Delivery Insights ngày 16/11/2026

Bốn trang chính và một trang lịch trình chi tiết thay thiết kế native trước đó. Bố cục,
màu sắc, nhãn, thứ tự xem chỉ số và điều hướng được thiết kế lại. Power BI đã có đường nối
tuyến theo xe bằng image visual native, bộ lọc DataCo đồng bộ và bộ chọn cam kết độc lập
để luôn giữ đủ năm phương án trong bảng so sánh. Giả định nhiên liệu được đồng bộ sang
trang lịch trình bằng slicer ẩn. Nguồn dữ liệu bàn giao và kết quả số gốc được giữ nguyên.

84 kiểm tra đầu vào, 13 unittest, 132 file qua schema, 119 visual qua kiểm tra tham chiếu/
bố cục và 26 kiểm tra DAX native đạt. CLI Microsoft xác nhận 0 lỗi, 0 cảnh báo. Chi tiết
render và tương tác xem reports/dashboard/native_render_validation.json. Các ghi nhận
scatter/chưa đồng bộ phía trên mô tả phiên bản cũ. Không chạy lại huấn luyện hoặc bộ giải.
Chưa stage, commit hoặc push bản nâng cấp này.


## Điều chỉnh điều hướng và nội dung Dashboard

Theo góp ý của Anh Quốc, chuyển DELIVERY INSIGHTS và bốn mục điều hướng từ cột trái
lên thanh ngang cao 72. Canvas giảm từ 1440 × 960 xuống 1440 × 864, nội dung trải hết
chiều ngang với lề 28. Bỏ thông tin người phụ trách, dòng giới thiệu lặp, hướng dẫn thao tác,
khuyến nghị chung và footer dài. Giữ phạm vi, đơn vị và các giải thích cần để đọc đúng số liệu.
Thay đoạn lời khuyên ở trang Cam kết bằng bảng thời gian cam kết theo phương thức.

100 file qua schema, 87 visual qua kiểm tra tham chiếu và bố cục; không sửa measures,
quan hệ hoặc CSV. Đã rà ảnh native năm trang và thử thanh điều hướng ngang cùng nút
lịch trình. Kết quả hiện hành xem reports/dashboard/native_render_validation.json.
Chưa commit/push lượt điều chỉnh này.


## Sửa chồng lấn và khoảng trống trong Dashboard

Tách tiêu đề, chú thích và số KPI thành các vùng hiển thị độc lập; số có đủ chiều cao dòng
theo font native. Tách nhãn bộ lọc với dropdown đúng kích thước tối thiểu. Cố định độ rộng
cột để bảng phủ khoảng 97% khung; căn tiêu đề theo kiểu dữ liệu. Bỏ ba ô kết luận lớn bị
lặp, mở rộng bảng tương ứng và cân tỷ lệ khung sơ đồ tuyến/lịch trình.

175 file qua schema, 162 visual qua kiểm tra nguồn; CLI Microsoft không có lỗi/cảnh báo.
Đo trực tiếp Power BI ở 2400 × 1580 và 1366 × 900, đủ năm trang mỗi kích thước: không
phát hiện chữ vượt vùng riêng, khung tiền cảnh giao nhau hoặc nhãn biểu đồ chồng nhau
trong các trạng thái mặc định đã kiểm tra. Đã xem ảnh native; phạm vi và giới hạn được
ghi trong native_layout_validation.json. Công thức, quan hệ và CSV giữ nguyên.
Chưa commit/push lượt sửa này.

## Bàn giao Git

Bản nâng cấp Power BI và bộ kiểm tra bố cục được đưa vào commit của lượt bàn giao này. Các ghi nhận chưa commit/push phía trên mô tả thời điểm kiểm tra trước bàn giao.
