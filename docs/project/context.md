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
