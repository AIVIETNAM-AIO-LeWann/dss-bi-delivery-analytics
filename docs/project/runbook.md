# Hướng dẫn chạy và kiểm tra

Mở PowerShell tại thư mục gốc repo. Xem `docs/project/verification.md` để biết các kiểm tra thực sự đã chạy và giới hạn môi trường hiện tại. Cần Python có phiên bản phù hợp từng phần.
Các đường dẫn bên dưới là tương đối với repo, dùng được khi chuyển máy.

## Chuẩn bị dữ liệu TV2

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -e .
.venv/Scripts/python -m unittest discover -s tests -v
.venv/Scripts/python -m dss_bi_delivery.download_data
.venv/Scripts/python -m dss_bi_delivery.prepare_data
.venv/Scripts/python -m dss_bi_delivery.verify_data
```

Nguồn CSV ở `data/raw/DataCoSupplyChainDataset.csv`, SHA-256 theo
`docs/data_preparation/source_manifest.json`. Không chuyển Excel thành raw để bỏ qua checksum.
Chuẩn bị sinh lại dữ liệu, dictionary/schema và báo cáo chất lượng. Bản clone chưa có raw;
bốn bảng sạch dùng ngay hiện được phục hồi từ snapshot TV4, có manifest riêng.
Muốn tái chạy TV3 đủ mọi bảng phải chạy chuẩn bị trước để có `orders_clean.csv` và `order_items_clean.csv`.

## Kiểm tra tài nguyên và ghép khóa

```powershell
.venv/Scripts/python scripts/check_project.py
```

Kiểm tra checksum 9 tệp gốc, bốn bảng phục hồi và đối chiếu ID/P_Late giữa CSV gửi riêng,
TV4, TV5 và tập test TV2. Lệnh chỉ đọc và in kết quả; không huấn luyện hoặc ghi đè báo cáo.

## Mô tả TV3

`workstreams/descriptive/run_pipeline.py` đọc `data/processed/` từ gốc repo;
chạy sẽ ghi lại tables/figures. Chỉ chạy sau khi đủ ba bảng đầu vào và cài các thư viện
import trong script (pandas, numpy, scipy, matplotlib, seaborn, statsmodels).
Chưa có bộ requirements ghim riêng TV3 trong bàn giao; không giả định môi trường TV2 đã đủ.

## Dự báo TV4

Dùng môi trường riêng và requirements của `workstreams/forecasting/`, Python 3.12 theo bàn giao.
Từ thư mục này chạy:

```powershell
python -m unittest discover -s code -v
python code/forecast.py --source-root source_snapshot --output replay
python code/verify_outputs.py replay
```

Giữ `results/` làm mốc bàn giao; chỉ thay khi đã đối chiếu và cập nhật báo cáo.

## Đề xuất TV5

Dùng môi trường riêng với requirements của `workstreams/prescriptive/`.
Từ thư mục này chạy `python code/verify_results.py` và `python code/verify_handoffs.py`.
Hai lệnh có thể cập nhật file bằng chứng kiểm tra trong results; so diff trước khi giữ thay đổi.
Chạy phân tích mới bằng `python code/run_analysis.py --output replay` rồi kiểm chứng theo README bộ này.
Không gọi `build_docx.py` nếu chỉ muốn đọc/kiểm tra số liệu.

## Trước khi chia sẻ lên GitHub

Chạy kiểm tra tài nguyên và tests liên quan; đọc `git diff --check`, `git diff --stat`, `git status --short`.
Không thêm raw/reference workbook/ZIP/snapshot dữ liệu/mô hình nhị phân bằng `git add -f`.
Các file bỏ qua bởi Git vẫn có trong thư mục làm việc, người clone mới cần nhận gói gốc
theo resource_manifest rồi khôi phục theo hướng dẫn; repo không tự đính kèm dữ liệu nặng.

## Khôi phục tài nguyên sau khi clone

Nhận đủ chín file gốc theo references/resource_manifest.json, rồi chạy:

`powershell
python scripts/restore_resources.py --source <thu_muc_chua_file_goc>
python scripts/check_project.py
`

Công cụ kiểm tra checksum, chỉ giải nén file còn thiếu và không ghi đè mã/kết quả đã chỉnh.

## Dashboard — dữ liệu, Power BI và preview

Môi trường .venv đã được cài đúng pandas 2.3.3/numpy 2.2.6; bộ 11 unittest hiện đạt.

```powershell
.venv/Scripts/python -m dss_bi_delivery.dashboard_data
.venv/Scripts/python scripts/build_dashboard_preview.py
.venv/Scripts/python -m unittest discover -s tests -v
```

Nguồn Power BI đã sinh trong dashboards/powerbi/; không chạy lại build_powerbi.py khi chỉ refresh dữ liệu.
Đọc dashboards/powerbi/README.md để đặt RepoRoot và nghiệm thu trực tiếp bằng Desktop.
Đọc dashboards/README.md để biết khác biệt giữa native Power BI và preview.
