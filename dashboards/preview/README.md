# Bản xem trước tương tác ngoại tuyến

Mở delivery_dashboard.html bằng Edge/Chrome sau khi chạy
`.venv/Scripts/python scripts/build_dashboard_preview.py` từ gốc repo.
Tệp chứa dữ liệu tối thiểu đã đối chiếu, không gọi API hoặc tải tài nguyên từ bên ngoài.
HTML được sinh không theo dõi trong Git; template và bộ dựng được theo dõi.

Bản này giúp Anh Quốc và nhóm rà thông điệp, KPI, what-if và tuyến ngay khi chưa có Power BI.
Nó không phải trình render Power BI. Preview giữ thiết kế trước lần nâng cấp Delivery Insights.
Power BI mới đã đồng bộ bộ lọc giữa các trang DataCo và có đường nối tuyến bằng SVG native,
cùng trang lịch trình riêng. Xem giao diện mới trong Power BI, không suy ra từ preview HTML.
Không dùng kết quả preview để tuyên bố model Power BI đã refresh hoặc DAX/M đã được thực thi.

Kiểm tra tương tác tùy chọn: cài Playwright vào `.cache/browser/` (không tạo package ở gốc repo),
hoặc đặt PLAYWRIGHT_MODULE trỏ đến package có sẵn, rồi chạy `node scripts/check_dashboard_preview.cjs`.
Script tự tìm Edge trên Windows, hoặc dùng Chromium của Playwright; có thể đặt BROWSER_EXECUTABLE.
Ảnh QA nằm trong `.cache/dashboard-previews/`, kết quả ở `reports/dashboard/preview_validation.json`.
