# Hướng dẫn cộng tác

Đọc README và docs/project/context.md trước khi thay đổi.
Mỗi phần có người phụ trách trong README; trao đổi khi thay schema, mẫu dữ liệu hoặc KPI dùng chung.
Anh Quốc quản lý Dashboard chính; các thành viên khác cung cấp insight/kết quả.

Không sửa dữ liệu sạch bằng tay. Sửa logic ở src, chạy lại kiểm chứng và cập nhật tài liệu bị ảnh hưởng.
Không sửa source_snapshot để thay mã hiện hành; đó là bản upstream cố định của TV4.
Không ghi đè kết quả bàn giao khi thử nghiệm: dùng replay/ và đối chiếu trước.
Giữ CSV UTF-8 BOM, ID dạng Text, tỷ lệ 0–1, ngày theo định nghĩa nguồn.
Không gọi mối liên hệ là nguyên nhân; không gọi giả định chi phí là chi phí thực tế.

Dùng nhánh theo công việc, ví dụ `docs/project-structure`, `feat/delivery-dashboard`.
Commit mô tả việc thay đổi; ghi các kiểm tra đã chạy và giới hạn còn lại khi mở PR.
Kiểm tra .gitignore để tránh đưa dữ liệu lớn, cache hoặc thông tin cấu hình cá nhân lên repo.
Không commit/push tự động trong quá trình nhập và sắp xếp tài nguyên.

Các bộ bàn giao trong workstreams và prompt nguồn được Git giữ nguyên byte/ khoảng trắng
để bảo toàn checksum. Không chạy formatter hàng loạt trên các tài nguyên này.
