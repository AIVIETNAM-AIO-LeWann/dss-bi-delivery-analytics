# Nhật ký tổ chức lại ngày 16/11/2026

- Sao chép 9 tài nguyên từ Downloads; giữ nguyên file gốc, kiểm tra SHA-256 sau sao chép.
- Đổi tên ngoài theo chức năng; lưu ánh xạ tại references/resource_manifest.json.
- Giải nén ba ZIP vào workstreams/descriptive, forecasting, prescriptive; kiểm tra từng byte và đường dẫn.
- Chuyển docs TV2 vào docs/data_preparation; reports TV2 vào reports/data_quality.
- Cập nhật đường dẫn đọc/ghi trong package TV2; sửa REPO_ROOT của pipeline TV3 theo độ sâu mới.
- Phục hồi 4 CSV sạch từ snapshot TV4 vào data/processed, ghi nguồn và checksum.
- Bổ sung context, structure, runbook, hướng dẫn cộng tác và điểm vào Dashboard/báo cáo/slide.
- Giữ nguyên tên package, schema, cách tính và nội bộ gói bàn giao; ZIP gốc là bản đối chiếu.
- Không tải thay raw, không huấn luyện lại, không tạo Dashboard hay commit/push trong bước này.

Quyết định cấu trúc: nhóm theo chức năng ở gốc; bảo toàn gói thành viên ở workstreams để tái lập độc lập.
Không hợp nhất dependency đang xung đột; không đổi tên mọi tệp trong gói vì manifest và mã tham chiếu nội bộ.
