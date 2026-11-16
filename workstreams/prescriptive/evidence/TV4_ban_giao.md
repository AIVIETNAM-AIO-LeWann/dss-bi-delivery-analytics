# Bộ bàn giao phần Ngọc Quang

**Chủ đề 18 — Giao hàng đúng hẹn và tối ưu tuyến đường.** Thực hiện ngày 05/11/2026.

Đọc `Bao_cao_Ngoc_Quang_Chu_de_18.docx` để lấy phần viết cho Phần V và Phần VII. Đọc `NHAT_KY_CONG_VIEC.md` để xem chính xác những gì đã làm và các giới hạn.

## Kết quả

Baseline theo phương thức được chọn bằng log loss validation thấp nhất, trước khi xem test. Các mô hình logistic và histogram gradient boosting cũng đã được chạy và so sánh, không bị bỏ qua.

Trên **13.071 đơn test**, baseline đạt ROC-AUC **0,746**, AP **0,788**, log loss **0,536**, Brier **0,188**. Ngưỡng 0,5: precision **88,97%**, recall **53,92%**, accuracy **69,63%**. Logistic có AP test 0,840; không khẳng định baseline tốt nhất theo mọi mục tiêu.

Xác suất có điều kiện **không hủy trong snapshot lịch sử**. Baseline chỉ tạo bốn mức P_Late, một mức cho mỗi phương thức, không phân biệt được các đơn trong cùng phương thức. Nhãn trễ 100% của First Class trong nguồn không phải bảo đảm ngoài thực tế. Chưa tối ưu ngưỡng theo chi phí, chưa chứng minh can thiệp làm giảm trễ và chưa giải VRPTW.

## Gửi file nào cho ai

| Người nhận | File và cách dùng |
| --- | --- |
| Người tổng hợp báo cáo | Bản Word; lấy phần dự báo và hạn chế phù hợp dung lượng báo cáo nhóm |
| Hoài Phú | `results/predictions_test.csv`, `results/thresholds_validation.csv`, `results/sensitivity.csv`; dùng xác suất để xây kịch bản, không coi đây là hiệu quả can thiệp đã xảy ra |
| Anh Quốc | `results/predictions_test.csv`; ghép `order_id` dạng Text, định dạng `P_Late` thành phần trăm; chỉ dùng test để báo cáo kết quả ngoài mẫu |
| Hoàng Quân | `results/model_comparison.csv`, `results/subgroups_test.csv`, `results/monthly_test.csv`; đối chiếu insight với cùng mẫu không hủy |

Không gộp `predictions_by_partition.csv` để công bố hiệu quả toàn mẫu: file này gồm train (in-sample), validation (đã dùng chọn mô hình) và test. File có 62.136 đơn; 761 đơn khoảng đệm không có dự báo và không tham gia fit/chọn/chấm điểm.

## Các thư mục

- `results/`: metrics, dự báo, ngưỡng validation, độ nhạy, phân nhóm/tháng, kiểm chứng, manifest.
- `models/`: mô hình đã fit trên train, metadata và allowlist. Chỉ nạp joblib từ nguồn tin cậy; file này được tạo trong bộ bàn giao.
- `inputs/`: ba bảng dự báo và schema nhỏ gọn, không có tên, email, mật khẩu hoặc địa chỉ đường của khách.
- `source_snapshot/`: bản mã/tài liệu chuẩn bị của nhóm ở commit cố định và bốn bảng sạch cần chạy lại. Không chứa file nguồn 95 MB; có mã tải và checksum để tái tạo từ raw.
- `code/`: mã phân tích mới và tests. `figures/`: hình dùng trong Word.
- `provenance/`: nguồn, checksum, quy tắc chuẩn bị và kiểm tra của nhóm.

## Chạy lại từ dữ liệu đã bàn giao

Yêu cầu Python 3.12. Mở PowerShell tại thư mục bộ bàn giao. Nên giải nén vào đường dẫn ASCII, ví dụ `C:\DataCo\NgocQuang`, để tránh lỗi thư viện Windows với đường dẫn Unicode.

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m unittest discover -s code -v
$env:LOKY_MAX_CPU_COUNT = '2'
$env:MPLCONFIGDIR = Join-Path (Get-Location) '.mplconfig'
.venv\Scripts\python code\forecast.py --source-root source_snapshot --output replay
.venv\Scripts\python code\verify_outputs.py replay
```

`replay` là kết quả chạy lại, tách khỏi bản kết quả đã bàn giao. Có thể có sai khác số thực rất nhỏ giữa hệ điều hành/BLAS; seed 42 và cấu hình mô hình được lưu trong `run_manifest.json`. Bản Word là phần viết đã kiểm tra cho kết quả trong `results/`; nếu thay nguồn/cấu hình, phải cập nhật lại số liệu trong bản viết.

## Tái tạo từ nguồn gốc

Tiếp tục mở PowerShell tại thư mục gốc của bộ bàn giao, không chuyển vào `source_snapshot`. Các lệnh dưới đây tải đúng CSV Kaggle phiên bản 1 và kiểm tra SHA-256 trước khi làm sạch; script tự xác định thư mục dữ liệu bên trong `source_snapshot`. Mã nguồn chuẩn bị của nhóm được giữ nguyên. Dữ liệu thô và trung gian chỉ được tạo trong bản snapshot cục bộ, không ghi lên GitHub hoặc Google Drive.

```powershell
$env:PYTHONPATH = (Resolve-Path source_snapshot\src).Path
.venv\Scripts\python -m dss_bi_delivery.download_data
.venv\Scripts\python -m dss_bi_delivery.prepare_data
.venv\Scripts\python -m dss_bi_delivery.verify_data
.venv\Scripts\python -m unittest discover -s source_snapshot\tests -v
.venv\Scripts\python code\forecast.py --source-root source_snapshot --output replay_from_raw
.venv\Scripts\python code\verify_outputs.py replay_from_raw
```

Nếu Kaggle yêu cầu đăng nhập ở môi trường khác, tải thủ công đúng file được mô tả tại `source_snapshot/docs/01_nguon_du_lieu.md`; giữ nguyên kiểm tra checksum. Không bỏ qua lỗi nguồn hoặc đổi nhãn để chạy được.

## Nạp model và dự báo một file đầu vào

Đầu vào phải có `order_id`, `order_datetime` và đủ 13 cột trong `inputs/analysis_schema.json`; giữ mã là Text. Các candidate cần thực sự có sẵn ở thời điểm dự báo. Đây là mô hình lịch sử có phạm vi có điều kiện không hủy; chưa được xác thực cho vận hành mọi đơn mới.

```powershell
.venv\Scripts\python code\score_orders.py --model models\selected_model.joblib --input inputs\orders_model_features.csv --output scored_input.csv
```

Ví dụ này chấm lại file cung cấp, không tạo đánh giá ngoài mẫu. Không dùng `scored_input.csv` để tuyên bố hiệu quả dự báo. Muốn xem kết quả test chuẩn, dùng `results/predictions_test.csv`.

## Phương pháp và kiểm chứng

Train 39.568 đơn; validation 9.497; test 13.071; khoảng đệm 761. Encoding, scaling và estimator chỉ fit trên train. Chọn mô hình bằng log loss validation thấp nhất, không chọn bằng test và không refit sau chọn. Ngưỡng 0,5 cố định, chưa có ma trận chi phí để tối ưu kinh doanh.

8/8 tests dự báo mới và 7/7 tests chuẩn bị của nhóm đạt. Kiểm tra nguồn độc lập đạt 51/51; bảng analysis đạt 24/24; readback đầu ra đạt 12/12, gồm tính lại metrics từ CSV và nạp model ở tiến trình mới. Phiên bản pandas 2.3.3 được ghim vì pandas 3.0.1 tái hiện lỗi khi map datetime rỗng trong một edge-case test của upstream.

Nguồn mã chung: [repo của nhóm](https://github.com/AIVIETNAM-AIO-LeWann/dss-bi-delivery-analytics), commit `6fd157327b8fc05d6011e71659db86048dead818`. Nguồn dữ liệu và giấy phép theo `source_snapshot/docs/01_nguon_du_lieu.md`; bộ bàn giao không tự cấp giấy phép mới cho dữ liệu bên thứ ba.
