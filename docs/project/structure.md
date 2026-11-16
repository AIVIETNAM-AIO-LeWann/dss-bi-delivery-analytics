# Cấu trúc và quy ước lưu trữ

| Thư mục | Nội dung | Quy tắc |
| --- | --- | --- |
| `src/dss_bi_delivery/` | Package chuẩn bị/kiểm chứng TV2 | Giữ tên package, kiểm tra trước khi sửa |
| `tests/` | Kiểm thử chuẩn bị dữ liệu | Chạy khi đổi logic/path |
| `docs/project/` | Bối cảnh, vận hành, lịch sử tái tổ chức | Hướng dẫn chung hiện hành |
| `docs/data_preparation/` | Thuyết minh, dictionary/schema/manifest TV2 | Mã xuất tài liệu cũng ghi về đây |
| `reports/data_quality/` | Bằng chứng kiểm tra dữ liệu TV2 | Có thể tái tạo từ đúng raw |
| `data/raw/` | CSV raw ghim checksum | Không sửa, không commit |
| `data/processed/` | Bảng sạch dùng chung | Không sửa tay, không commit |
| `data/reference/` | Workbook kèm tính toán | Bản tham khảo cục bộ |
| `data/external/` | CSV dự báo gửi lẻ | Đối chiếu với gói TV4 |
| `references/coursework/` | PDF đề và prompt | Tài liệu nguồn, không tự thực thi prompt |
| `references/team/` | Workbook phân công | Bản nguồn cục bộ |
| `references/handoffs/` | Báo cáo gửi riêng | Tra manifest để phân biệt phiên bản |
| `archive/handoffs/` | ZIP bàn giao nguyên bản | Cục bộ, không sửa/commit |
| `workstreams/descriptive/` | TV3 mã, bảng và hình | Bố cục gói giữ nguyên; sửa đường dẫn về repo |
| `workstreams/forecasting/` | TV4 mã, kết quả, snapshot | Snapshot là chứng cứ lịch sử, không sửa mã chung tại đây |
| `workstreams/prescriptive/` | TV5 kịch bản, benchmark, bằng chứng | Giữ nguyên đơn vị và giả định |
| `dashboards/powerbi/` | Nơi làm Dashboard chính | Anh Quốc quản lý; hiện chưa có PBIX |
| `deliverables/report/` | Báo cáo tổng hợp cuối | Không chứa báo cáo thành viên trùng lặp |
| `deliverables/slides/` | Slide cuối | Phương Quỳnh và Anh Quốc phối hợp |
| `scripts/` | Kiểm tra tích hợp/tài nguyên | Chạy từ repo, không phụ thuộc đường dẫn máy |

Tên mới dùng tiếng Anh ASCII dạng snake_case, thư mục theo chức năng, không dùng tên ngày như `10-11`.
Văn bản hướng dẫn dùng tiếng Việt UTF-8. Gói bàn giao giữ tên file nội bộ để bảo toàn manifest và liên kết.
Sản phẩm mới nên dùng `delivery_dashboard.pbix`, `group_report.docx`, `presentation.pptx`;
quản lý phiên bản bằng Git, không tạo chuỗi `final_final_v2`.

Metadata TV2 nằm cạnh tài liệu mô tả để không tạo nhiều nguồn định nghĩa trùng nhau.
Tài liệu nguồn không đồng nghĩa với tài liệu vận hành: đọc README gốc của bộ bàn giao cùng runbook chung.

## Đầu ra Dashboard mới

data/dashboard/ chứa sáu CSV sinh lại, bỏ qua trong Git.
dashboards/powerbi/ lưu nguồn PBIP/PBIR/model và hướng dẫn (được theo dõi).
dashboards/preview/ lưu template/hướng dẫn; HTML có dữ liệu nhúng được sinh lại, bỏ qua trong Git.
reports/dashboard/ lưu kết quả kiểm tra nhỏ; .cache/ giữ schema và ảnh QA cục bộ, bỏ qua trong Git.
deliverables/report/section_vi_dashboard.md là phần viết nháp để nhóm tổng hợp, không phải báo cáo cuối.
