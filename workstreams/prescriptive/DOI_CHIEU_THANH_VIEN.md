# Đối chiếu phần TV5 với phân công và đầu ra của nhóm

Ngày rà soát: 06/11/2026. Phạm vi bộ nộp: Phân tích đề xuất của Hoài Phú, hạn 10/11/2026.

## Đối chiếu sáu thành viên

| Thành viên | Bằng chứng đã có để đọc | Cách TV5 kế thừa hoặc phối hợp |
| --- | --- | --- |
| TV1 Phương Quỳnh | Workbook phân công, sheet công ty đề xuất và xác nhận DHL của nhóm; chưa có thư mục/bản báo cáo riêng TV1 trong bộ bài tập hiện tại | Giữ vai trò Giám đốc Logistics, Chủ đề 18 và bối cảnh DHL. Không viết thay toàn bộ phần S hoặc khẳng định đã rà báo cáo TV1 chưa có. |
| TV2 Lê Quang | Tài liệu bàn giao, sổ giả định, bảng KPI, phân phối duration, schema và bản dữ liệu sạch được giữ trong snapshot TV4 | Dùng cấp đơn, 62.897 đơn không hủy; giữ nhãn, kỳ chia tập và khoảng đệm. Phân vị cam kết chỉ tính trên train. Tọa độ DataCo không dùng làm điểm giao. |
| TV3 Hoàng Quân | Báo cáo mô tả/chẩn đoán và bảng theo phương thức/kiểm định | Đối chiếu lại số đơn và số trễ của cả bốn phương thức. Phân biệt tỷ lệ toàn mẫu với test. Sửa cách diễn giải trong phần TV5: p-value lớn chưa chứng minh độc lập hoặc không ảnh hưởng; không gọi COMPLETE/CLOSED là bằng chứng đã hoàn tất dòng tiền. Không sửa tệp TV3. |
| TV4 Ngọc Quang | Cả bản Word bên ngoài và bộ bàn giao; README, lựa chọn mô hình, kết quả test và thông tin chia tập | Giữ mô hình baseline do TV4 chọn. Xác minh từng nhãn, phương thức, mã đơn và P_Late train-only trên 13.071 đơn test. Không chọn lại mô hình theo AP test, không xem cảnh báo đúng là hiệu quả can thiệp. |
| TV5 Hoài Phú | Mã, dữ liệu và kết quả cam kết/tuyến/nhiên liệu đã chạy | Tính lại toàn bộ 33 hàng tóm tắt kịch bản từ đầu vào; kiểm tra từng cam kết cấp đơn đã xuất; kiểm tra tuyến, tải, cửa sổ và cận dưới đội xe. Bổ sung bảng đánh đổi theo phương thức, kiểm tra độ nhạy duration, khuyến nghị và điều kiện quyết định. |
| TV6 Anh Quốc | Yêu cầu bàn giao trong phân công; chưa có thư mục/dashboard riêng trong bộ bài tập hiện tại | Bàn giao CSV, schema, sơ đồ tuyến và cách ghép order_id dạng Text. Không thao tác hoặc tạo thay dashboard chính. |

## Các vấn đề đã xử lý trong phần TV5

1. Nội dung nhân sự/IBM HR còn trong phân công là mẫu cũ. Khuyến nghị TV5 bám bài toán Logistics đã được người dùng xác nhận; không có giữ chân nhân viên hay chi phí thay thế nhân viên.
2. DHL là bối cảnh doanh nghiệp. DataCo và Solomon không được xác nhận là dữ liệu nội bộ DHL. Thành tích TNO không phải kết quả TV5.
3. Link Kaggle shashwatwork là nguồn tham chiếu nhóm cung cấp; manifest đầu vào TV4 ghi saicharankomati/version 1. Chưa kiểm chứng đồng nhất byte giữa hai trang; giữ nguồn tính toán đã bàn giao và ghi rõ khác biệt.
4. Trễ toàn mẫu 57,31% và test 57,56% dùng mẫu số khác nhau. Tăng cam kết không làm thay đổi duration nguồn và chưa chứng minh giao nhanh hơn.
5. Phương án +1 ngày còn vượt hẹn 60,52% ở Second Class, nên không được giới thiệu là đã đáp ứng một mục tiêu dịch vụ cao chưa được chốt.
6. Same Day có vấn đề nhất quán duration/timestamp đã được TV2 ghi nhận. Kiểm tra loại nhóm này chỉ là độ nhạy, không thay đánh giá bốn phương thức.
7. P_Late có bốn mức theo phương thức, có điều kiện không hủy và dự báo nhãn theo cam kết cũ. Không tái dùng như xác suất vượt cam kết mới.
8. C101/Q=200 có cận dưới 10 xe và lời giải khả thi 10 xe, nên chứng minh được số xe tối thiểu trong mô hình. Không tuyên bố quãng đường tối ưu hay nhu cầu xe của DHL.
9. Đối chứng nearest feasible không tìm được tuyến đủ khách cho R101/RC101 trong K=25. Không tính % tiết kiệm từ đối chứng thất bại.
10. Nhiên liệu là mô phỏng có tham số minh họa. Chưa có chi phí cố định đội xe, chi phí can thiệp hoặc tác động thực tế; không công bố ROI, lợi nhuận ròng hay tiền tiết kiệm doanh nghiệp đã xảy ra.

## Bằng chứng kiểm tra

- `results/handoff_audit.json`: tính lại từ đầu vào, đối chiếu TV2–TV4, tất cả kịch bản cam kết, từng cam kết và lịch dừng đã xuất.
- `results/verification.json`: kiểm tra lại khóa, tỷ lệ, tuyến đủ khách, sức chở, khung giờ, quãng đường, nhiên liệu và chứng nhận đội xe.
- `evidence/`: các bản bàn giao/bảng tham chiếu cần thiết. Đây là bản sao nguồn dùng đối chiếu, không phải phần TV5 tự thực hiện.
- `package_manifest.json`: hash tệp để kiểm tra bộ nộp không bị thay đổi khi sao chép.

Kiểm tra được thực hiện bằng mã tính lại trên dữ liệu đóng gói. Không khẳng định đã có đánh giá độc lập của người thứ ba hay kiểm chứng triển khai thực tế.
