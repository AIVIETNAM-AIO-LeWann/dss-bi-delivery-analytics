# Kiểm tra sau tổ chức lại

Ngày: 16/11/2026. Không coi kết quả kiểm tra lịch sử của bộ bàn giao là lượt chạy mới.

## Đã kiểm tra trực tiếp

- 9 file sao chép khớp SHA-256 với file gốc Downloads.
- 3 gói ZIP được giải nén có kiểm soát đường dẫn; byte từng file khớp nội dung ZIP lúc nhập.
- 4 bảng sạch phục hồi khớp checksum snapshot; tổng cộng 13 checksum qua scripts/check_project.py.
- Mẫu chính có 62.897 mã đơn duy nhất và 36.048 nhãn trễ.
- CSV dự báo gửi lẻ, TV4, đầu vào TV5 và bảng Dashboard TV5 cùng có đúng 13.071 ID test;
  nhãn và P_Late khớp từng đơn. Chưa gọi đây là kiểm chứng mọi cột kịch bản hoặc tuyến.
- scripts/restore_resources.py chạy lại được khi tài nguyên đã tồn tại và giữ nguyên mã đã chỉnh.
- Liên kết Markdown trong README và docs không còn đích cục bộ bị thiếu.
- git diff --check đạt; các file dữ liệu nặng/ZIP/workbook nguồn không xuất hiện trong danh sách file mới được Git theo dõi.

## Kiểm thử và giới hạn

Bộ 7 unittest của TV2 chạy bằng runtime sẵn có (pandas 3.0.1): 6 đạt, 1 lỗi
`Cannot cast DatetimeArray to dtype float64` ở trường hợp trùng mã đơn.
Chạy cùng bộ tests trên snapshot nguyên bản cũng tái hiện đúng lỗi này.
README TV4 đã lưu ý phải dùng pandas 2.3.3; không sửa logic phân tích để né lỗi phiên bản.

Đã tạo .venv và thử cài editable package với pandas 2.3.3/numpy 2.2.6 theo requirements.
Lượt tải thư viện không tiến triển trong thời gian kiểm tra nên đã dừng tiến trình cài;
.venv chưa sẵn sàng. Chạy lại bước cài trong runbook rồi chạy tests để xác nhận trên đúng môi trường.

Chưa chạy toàn bộ ETL từ raw (clone chưa có CSV nguồn đã ghim), chưa huấn luyện TV4,
chưa tái giải tuyến TV5, chưa render lại báo cáo Word/PDF nguồn vì không chỉnh chúng,
chưa tạo hay kiểm thử Power BI. Đây là bước nhập tài nguyên và tổ chức dự án.
Không commit, stage hoặc push thay đổi.

## Cập nhật sau triển khai Dashboard

Lỗi phiên bản thư viện đã được xử lý bằng môi trường riêng pandas 2.3.3/numpy 2.2.6.
7/7 unittest TV2 và 4/4 kiểm tra hợp đồng dữ liệu mới đều đạt (11 tổng).
81 kiểm tra đầu vào Dashboard, 66 file qua schema chính thức và 56 visual qua kiểm tra
tham chiếu/bố cục. Preview có 18 kiểm tra tương tác đạt trong Edge; đã xem ảnh bốn trang và màn hình nhỏ.
Bằng chứng từng phần nằm tại reports/dashboard/.

Power BI Desktop vẫn chưa có trên máy: chưa mở dự án native, refresh, thực thi DAX/M hoặc render native.
Các kiểm tra schema và preview không thay thế các bước này. Chưa chạy lại raw ETL/huấn luyện/tối ưu tuyến.
Không stage, commit hoặc push.

## Kết quả kiểm tra native cuối cùng

Đã phát hiện Power BI Desktop bản Microsoft Store 2.159.1231.0, mở dự án và refresh đủ sáu bảng.
21 kiểm tra DAX native đã đạt, gồm ngưỡng 0,40, precision trống khi không có cảnh báo,
mẫu số chính sách, giá nhiên liệu và tuyến chưa có lời giải.

Đã sửa lỗi phiên bản nội dung PBIR, tham chiếu activePageName, metadata tooltip,
ngưỡng double (chuyển CURRENCY), chữ bị cắt và cách viết tắt số trên card.
CLI authoring Microsoft: 0 lỗi, 0 cảnh báo. Đã chụp và xem bốn trang native;
Power BI dùng scatter điểm dừng/bảng thứ tự, preview có các đoạn nối tuyến.
Các ghi nhận “chưa có Desktop/chưa chạy native” phía trên là lịch sử trước khi tìm được bản Store.

Không chạy lại raw ETL/huấn luyện/tối ưu tuyến, không stage/commit/push.
