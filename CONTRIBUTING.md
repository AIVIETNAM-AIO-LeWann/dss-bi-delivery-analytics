# Hướng dẫn đóng góp

Cảm ơn bạn đã góp sức cho **Delivery Insights**. Dự án này có một tiêu chuẩn cao hơn bình thường ở một điểm: **kết quả phải truy nguyên được và không được nói quá những gì dữ liệu cho phép**. Tài liệu này giúp bạn làm đúng điều đó mà không mất thời gian đoán.

<table>
<tr>
<td width="33%"><b>1 · Trung thực với dữ liệu</b><br><sub>Liên hệ không phải nhân quả; giả định không phải số đo; thiếu lời giải không phải bằng 0.</sub></td>
<td width="33%"><b>2 · Tái lập được</b><br><sub>Mọi con số sinh ra từ mã và dữ liệu có checksum, không từ chỉnh tay.</sub></td>
<td width="33%"><b>3 · Không phá bằng chứng</b><br><sub>Kết quả bàn giao và bản chụp mã là chứng cứ lịch sử; thử nghiệm đi vào thư mục riêng.</sub></td>
</tr>
</table>

**Mục lục:** [Bắt đầu](#bắt-đầu) · [Ai phụ trách gì](#ai-phụ-trách-gì) · [Quy trình làm việc](#quy-trình-làm-việc) · [Quy tắc dữ liệu và phân tích](#quy-tắc-dữ-liệu-và-phân-tích) · [Làm việc với dashboard](#làm-việc-với-dashboard) · [Viết tài liệu](#viết-tài-liệu) · [Những thứ không đưa lên Git](#những-thứ-không-đưa-lên-git) · [Danh sách kiểm tra trước khi gửi](#danh-sách-kiểm-tra-trước-khi-gửi)

---

## Bắt đầu

Đọc theo thứ tự này, mất khoảng 15 phút:

1. [README](README.md): bài toán, kết quả và giới hạn.
2. [Bối cảnh và trạng thái](docs/project/context.md): phạm vi, luồng dữ liệu, điều cần giữ khi trình bày.
3. [Bản đồ thư mục](docs/project/structure.md): đặt và tìm file ở đâu.
4. [Hướng dẫn vận hành](docs/project/runbook.md): chạy lại từng phần.

### Cài môi trường

```powershell
git clone https://github.com/AIVIETNAM-AIO-LeWann/dss-bi-delivery-analytics.git
cd dss-bi-delivery-analytics
python -m venv .venv
.venv/Scripts/python -m pip install -e .
.venv/Scripts/python -m unittest discover -s tests -v
```

Gói gốc yêu cầu Python 3.10 trở lên với `pandas==2.3.3` và `numpy==2.2.6`. **Mỗi bộ bàn giao trong `workstreams/` có môi trường riêng** (ví dụ dự báo dùng Python 3.12). Các phiên bản được ghim khác nhau có chủ ý: đừng gộp các `requirements.txt` lại với nhau.

### Các lệnh kiểm tra thường dùng

| Mục đích | Lệnh |
| --- | --- |
| Kiểm thử đơn vị | `.venv/Scripts/python -m unittest discover -s tests -v` |
| Checksum tài nguyên, ghép khóa giữa các bộ kết quả | `.venv/Scripts/python scripts/check_project.py` |
| Dựng lại bảng cho dashboard | `.venv/Scripts/python -m dss_bi_delivery.dashboard_data` |
| Dựng lại bản web | `.venv/Scripts/python scripts/build_dashboard_web.py` |
| So số liệu bản web với pandas | `.venv/Scripts/python scripts/check_dashboard_web.py` |
| Kiểm tra lược đồ và bố cục Power BI | `.venv/Scripts/python scripts/validate_powerbi.py` |

Một số lệnh cần dữ liệu cục bộ chưa nằm trong Git; cách khôi phục có ở [hướng dẫn vận hành](docs/project/runbook.md#khôi-phục-tài-nguyên-sau-khi-clone).

## Ai phụ trách gì

Mỗi phần có một người chịu trách nhiệm. Bạn vẫn có thể sửa phần của người khác, nhưng hãy **nhắn họ trước** khi đổi thứ mà nhiều phần cùng dùng: schema bảng, mẫu dữ liệu, định nghĩa KPI.

| Phần | Phụ trách | Thư mục chính |
| --- | --- | --- |
| Chuẩn bị dữ liệu | Lê Quang | `src/dss_bi_delivery/`, `docs/data_preparation/` |
| Mô tả và chẩn đoán | Hoàng Quân | `workstreams/descriptive/` |
| Dự báo và hạn chế | Ngọc Quang | `workstreams/forecasting/` |
| Đề xuất và benchmark tuyến | Hoài Phú | `workstreams/prescriptive/` |
| Dashboard | Anh Quốc | `dashboards/` |
| Báo cáo tổng hợp, slide | Phương Quỳnh, Anh Quốc | `deliverables/` |

## Quy trình làm việc

### 1. Nhánh

Mỗi công việc một nhánh, đặt tên theo loại và nội dung:

| Tiền tố | Dùng cho | Ví dụ |
| --- | --- | --- |
| `feat/` | Tính năng hoặc phân tích mới | `feat/delivery-dashboard` |
| `fix/` | Sửa lỗi | `fix/late-rate-denominator` |
| `docs/` | Chỉ thay đổi tài liệu | `docs/project-structure` |
| `chore/` | Dọn dẹp, công cụ, cấu hình | `chore/ignore-local-cache` |

Không đẩy thẳng vào `main`.

### 2. Commit

Mỗi commit làm **một việc** và mô tả việc đó, theo dạng `loại: nội dung` bằng tiếng Việt hoặc tiếng Anh nhất quán trong cùng PR:

```text
feat: thêm bộ lọc ngưỡng cảnh báo cho trang Rủi ro
fix: dùng mẫu số đơn kiểm tra cho độ bao phủ khi lọc theo vùng
docs: bổ sung giới hạn của mô hình baseline vào README
```

Thân commit (nếu cần) nói **vì sao**, không lặp lại diff.

### 3. Pull request

PR nên nhỏ và đọc được trong một lần. Mô tả cần có:

- **Thay đổi gì và vì sao**, một đến hai câu.
- **Đã kiểm tra gì**: dán các lệnh đã chạy và kết quả chính (số test, số phép so sánh).
- **Giới hạn còn lại**: điều bạn chưa kiểm tra hoặc chưa làm. Nói thẳng điều này được đánh giá cao hơn là bỏ qua.
- **Ảnh chụp** nếu thay đổi giao diện, trước và sau.

Người rà soát kiểm tra: số liệu có truy nguyên được không, diễn đạt có nói quá không, tài liệu bị ảnh hưởng đã được cập nhật chưa.

## Quy tắc dữ liệu và phân tích

### Dữ liệu

| Quy tắc | Lý do |
| --- | --- |
| **Không sửa dữ liệu sạch bằng tay.** Sửa logic trong `src/`, chạy lại kiểm chứng, rồi cập nhật tài liệu bị ảnh hưởng. | Chỉ như vậy mới tái lập được |
| CSV dùng **UTF-8 có BOM**; cột `order_id` là **Text**; tỷ lệ và xác suất lưu **0 đến 1**; ngày theo định nghĩa nguồn. | Excel và Power BI hiểu sai nếu lệch; `order_id` dạng số mất số 0 và sai khi ghép |
| Chỉ ghép DataCo với DataCo theo `order_id`. **Không ghép sang node Solomon.** | Hai nguồn độc lập nhau |
| Nêu rõ **mẫu số**: toàn nguồn (180.519 dòng), đơn không hủy (62.897), tập test (13.071) là ba mẫu khác nhau. | Nhầm mẫu số là lỗi phổ biến nhất |
| Không dùng `git add -f` để đưa dữ liệu thô, bảng sạch hoặc mô hình vào kho. | Dung lượng, giấy phép, checksum |

### Kết quả bàn giao

- **`source_snapshot/` là bản chụp cố định** của mã chuẩn bị dữ liệu tại một commit. Không sửa nó để thay mã hiện hành.
- **Không ghi đè thư mục `results/` khi thử nghiệm.** Chạy vào `replay/` (đã được bỏ qua trong Git), đối chiếu với bản bàn giao, và chỉ thay bản bàn giao sau khi đã cập nhật báo cáo tương ứng.
- Bộ bàn giao và prompt nguồn được Git giữ nguyên từng byte để bảo toàn checksum. **Không chạy formatter hàng loạt** lên chúng.

### Cách diễn đạt kết quả

| Đừng viết | Hãy viết |
| --- | --- |
| "X **gây ra** việc trễ" | "X **có liên hệ** với trễ" |
| "Không có liên hệ (p > 0,05)" | "Chưa tìm thấy bằng chứng về liên hệ trong phép kiểm định này" |
| "Tiết kiệm được N đồng nhiên liệu" | "Nhiên liệu mô phỏng N đồng theo giả định đã nêu" |
| "Giao nhanh hơn" (khi chỉ đổi lời hứa) | "Giảm tỷ lệ vượt hẹn tính lại; thời gian giao thực tế không đổi" |
| "Quãng đường tối ưu" | "Tuyến khả thi; chưa chứng minh tối ưu quãng đường" |
| "Quãng đường 828,9 km" | "828,9 đơn vị tọa độ Solomon" |
| Số xe hoặc quãng đường bằng `0` khi không có lời giải | Để trống và ghi "chưa có lời giải" |

`P_Late` là xác suất vượt **cam kết cũ**, có điều kiện không hủy; không dùng nó như xác suất vượt cam kết mới hay hiệu quả của một can thiệp.

## Làm việc với dashboard

Có hai bản dashboard cùng nội dung. **Không có số cố định nào trong giao diện**: mọi con số và câu kết luận phải được tính từ dữ liệu theo bộ lọc.

### Bản web (`dashboards/web/`)

| File | Vai trò |
| --- | --- |
| `template.html` | Khung bốn trang |
| `style.css` | Chất liệu, bảng màu, chuyển động |
| `app.js` | Trạng thái bộ lọc, tổng hợp, biểu đồ, tương tác |
| `index.html` | **Sinh ra**, đừng sửa tay |

Quy trình: sửa ba file nguồn, chạy `scripts/build_dashboard_web.py`, chạy `scripts/check_dashboard_web.py`, rồi mở `index.html` xem bằng mắt ở cả chế độ sáng và tối. Nếu thêm tổng hợp mới, **thêm phép so sánh tương ứng với pandas** vào script kiểm tra. Chi tiết: [dashboards/web/README.md](dashboards/web/README.md).

### Bản Power BI (`dashboards/powerbi/`)

Báo cáo được **sinh từ mã** (`src/dss_bi_delivery/powerbi_report.py`, `powerbi_model.py`, `powerbi_svg.py`). Vì vậy:

- Sửa ở mã nguồn sinh, rồi chạy `scripts/build_powerbi.py`. Lệnh này **ghi đè toàn bộ** file đã sinh.
- **Đừng lưu từ Power BI Desktop rồi build lại.** Desktop chuẩn hóa lại file (phiên bản lược đồ, siêu dữ liệu) và mọi chỉnh sửa tay trong Desktop sẽ mất khi build. Nếu bạn đã chỉnh trong Desktop, hãy chuyển thay đổi đó vào mã nguồn sinh trước.
- Chạy `scripts/validate_powerbi.py`; bộ kiểm tra này **không** chứng minh DAX chạy đúng hay giao diện hiển thị đúng, nên hãy mở Desktop, refresh và xem từng trang.

### Nguyên tắc thiết kế chung

- Màu không là kênh duy nhất: luôn có nhãn, số hoặc chú giải đi kèm.
- Đỏ chỉ dùng cho điều xấu (trễ, bỏ sót), xanh dầu cho điều ổn, vàng đồng cho thận trọng.
- Mọi chuyển động phải tắt được khi hệ điều hành bật "giảm chuyển động".
- Giữ nguyên giải thích phương pháp ở nơi người xem dễ hiểu nhầm: nhiên liệu là giả định, sơ đồ là tọa độ, đổi cam kết không là giao nhanh hơn.

## Viết tài liệu

- Văn bản hướng dẫn dùng **tiếng Việt UTF-8**; tên file mới dùng tiếng Anh ASCII dạng `snake_case`.
- Luôn ghi **đơn vị và mẫu số** bên cạnh con số.
- Hình dùng trong README đặt ở `docs/assets/`, ưu tiên JPEG cho ảnh chụp giao diện và PNG cho biểu đồ nét; mỗi ảnh nên dưới 600 KB.
- Quản lý phiên bản bằng Git, không tạo chuỗi `final`, `final_final`, `v2`.
- Khi đổi hành vi, cập nhật tài liệu liên quan **trong cùng PR**.

## Những thứ không đưa lên Git

Các mục này đã nằm trong `.gitignore`; đừng ép đưa vào bằng `git add -f`.

| Loại | Ví dụ |
| --- | --- |
| Dữ liệu thô và bảng sạch | `data/raw/`, `data/processed/`, `data/dashboard/` |
| Tài liệu nguồn nặng hoặc có bản quyền | `archive/handoffs/`, workbook trong `data/reference/`, `references/team/*.xlsx` |
| Mô hình nhị phân, dự báo cấp đơn | `*.joblib`, `predictions*.csv` |
| Môi trường và cache | `.venv/`, `.cache/`, `__pycache__/`, `**/replay*/`, `.pbi/cache.abf` |
| Thông tin cá nhân | `.env`, khóa, đường dẫn máy của bạn |

Trước khi gửi, chạy `git status --short` và `git diff --stat` để chắc chắn không có gì ngoài ý muốn.

## Danh sách kiểm tra trước khi gửi

- [ ] Nhánh đặt tên đúng, mỗi commit một việc.
- [ ] `python -m unittest discover -s tests -v` đạt.
- [ ] Nếu đổi dữ liệu, ghép khóa hoặc KPI: `scripts/check_project.py` đạt.
- [ ] Nếu đổi dashboard: dựng lại, chạy script kiểm tra tương ứng, xem bằng mắt các trang bị ảnh hưởng.
- [ ] `git diff --check` không báo lỗi khoảng trắng.
- [ ] Không có dữ liệu thô, bảng sạch, mô hình, khóa hoặc đường dẫn cá nhân trong diff.
- [ ] Số liệu mới ghi rõ **mẫu số và đơn vị**; diễn đạt không nói quá (xem [bảng trên](#cách-diễn-đạt-kết-quả)).
- [ ] Tài liệu bị ảnh hưởng đã được cập nhật.
- [ ] Mô tả PR nêu **đã kiểm tra gì** và **còn giới hạn gì**.

## Báo lỗi và đề xuất

Mở một issue và nêu: bạn thấy gì, bạn mong đợi gì, cách tái hiện (lệnh, bộ lọc, trang), và ảnh chụp nếu là lỗi giao diện. Với lỗi số liệu, ghi rõ **mẫu số** và con số bạn cho là đúng cùng cách bạn tính ra nó.
