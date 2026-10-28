# DataCo — Dữ liệu ban đầu cho chủ đề 18

Bài tập lớn môn **Hệ Hỗ trợ Quyết định & Trí tuệ Kinh doanh**.
Chủ đề: **Giao hàng đúng hẹn và tối ưu tuyến đường**.

Phạm vi hiện tại là bước **O — Obtain the data**: nguồn dữ liệu, Data Dictionary,
kiểm tra/làm sạch, biến chuyển đổi và sổ giả định. Chưa huấn luyện mô hình,
chưa làm dashboard, chưa giải bài toán tuyến.

## Đọc từ đâu

| Yêu cầu | Tài liệu/bằng chứng |
| --- | --- |
| Nguồn và mô tả dữ liệu | [01_nguon_du_lieu.md](docs/01_nguon_du_lieu.md), [manifest](docs/source_manifest.json) |
| Data Dictionary | [02_data_dictionary.md](docs/02_data_dictionary.md), [CSV 53 cột](docs/data_dictionary.csv) |
| Kiểm tra và làm sạch | [03_chat_luong_va_lam_sach.md](docs/03_chat_luong_va_lam_sach.md), [kết quả thực chạy](reports/data_quality_report.md), [nhật ký](reports/preparation_log.csv) |
| Biến chuyển đổi | [04_bien_chuyen_doi.md](docs/04_bien_chuyen_doi.md), [công thức CSV](docs/derived_variables.csv) |
| Ghi nhận giả định | [05_so_gia_dinh.md](docs/05_so_gia_dinh.md), [sổ CSV](docs/assumption_log.csv) |
| Nội dung có thể đưa vào báo cáo | [06_phan_du_lieu_bao_cao.md](docs/06_phan_du_lieu_bao_cao.md) |

## Kết quả từ bản nguồn đã kiểm tra

- **180.519 dòng × 53 cột; 65.752 đơn hàng.** Mỗi dòng là một dòng hàng.
- Khóa dòng: `Order Item Id`; khóa đơn: `Order Id`. Không xóa các dòng chỉ vì cùng mã đơn.
- Thời điểm đặt từ **01/01/2015 đến 31/01/2018**; shipment đến **06/02/2018**.
- Không có dòng trùng hoàn toàn; không gán giá trị thiếu; không xóa dòng hàng.
- Tỷ lệ nhãn trễ trên mọi đơn: **54,82%**. Mẫu không hủy và đạt kiểm tra logistics: **57,31%**.
- `Latitude`/`Longitude` là vị trí cửa hàng theo từ điển nguồn, **không phải điểm giao**.

Các tỷ lệ trên khác nhau vì khác mẫu số. Không ghi một tỷ lệ mà bỏ qua cấp dữ liệu
và điều kiện chọn mẫu. Chi tiết và số đếm ở `reports/baseline_kpis.csv`.

## Chạy lại

Yêu cầu Python 3.10 trở lên. Cài package ở chế độ editable để chạy module trong
`src`. Chạy trong thư mục repo; đầu ra vẫn nằm ở `data/`, `docs/` và `reports/`:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -e .
.venv\Scripts\python -m dss_bi_delivery.download_data
.venv\Scripts\python -m dss_bi_delivery.prepare_data
.venv\Scripts\python -m dss_bi_delivery.verify_data
```

Nếu dùng Python đã có pandas/numpy đúng phiên bản, cài package một lần trước khi chạy:

```powershell
python -m pip install -e .
python -m dss_bi_delivery.prepare_data
python -m dss_bi_delivery.verify_data
```

Lệnh tải dùng endpoint công khai của Kaggle, ghim phiên bản 1. Nếu Kaggle yêu cầu
đăng nhập hoặc chặn endpoint ở môi trường khác, tải thủ công từ liên kết trong tài
liệu nguồn, đặt CSV vào `data/raw/`, rồi đối chiếu SHA-256 với manifest. Không ghi
token Kaggle vào repo. Lệnh xử lý mặc định từ chối file khác checksum hoặc khác schema.

`--allow-source-change` chỉ dùng sau khi chủ động xem lại nguồn, encoding, schema
và các giả định; không dùng như cách bỏ qua lỗi tải file. Các kiểm tra bỏ cột trùng,
cột rỗng và cột hằng vẫn phải đạt.

Đầu ra:

```text
data/raw/DataCoSupplyChainDataset.csv     # nguồn nguyên vẹn, không theo dõi bằng Git
data/processed/order_items_clean.csv     # 180.519 dòng; 54 cột gồm biến dẫn xuất
data/processed/orders_clean.csv          # 65.752 đơn; 36 cột
docs/                                   # tài liệu tiếng Việt, dictionary và giả định
reports/                                # số liệu kiểm tra, KPI và nhật ký 4 bước
src/dss_bi_delivery/                     # package tải, schema, xử lý và kiểm chứng
```

CSV đầu ra dùng UTF-8 BOM, phù hợp mở bằng Excel/Power BI. Khi import phải đặt các
cột mã là **Text**; CSV không lưu schema nên mở trực tiếp có thể khiến Excel suy diễn
mã thành số. Ngày xuất theo `YYYY-MM-DD HH:MM:SS`, chưa gán múi giờ.

File raw, ZIP và processed đã được `.gitignore`; không thêm chúng bằng `git add -f`.
Tài liệu, mã nguồn và báo cáo tổng hợp được theo dõi. Repo GitHub:
<https://github.com/AIVIETNAM-AIO-LeWann/dss-bi-delivery-analytics>.

`verify_data.py` đối chiếu độc lập bảng xuất với nguồn: khóa/dòng truy nguyên,
tổng theo đơn, nhãn gốc, đơn hủy, Same Day có kế hoạch 0 ngày và lợi nhuận âm.
Kết quả lưu tại `reports/validation_results.json`. Script kiểm chứng này ghim số đếm
của phiên bản đã kiểm tra; khi đổi nguồn phải xem lại các mốc, không nới kiểm tra tùy tiện.

## Quyết định phương pháp đang dùng

1. KPI logistics mặc định ở **cấp đơn**; bảng dòng hàng phục vụ phân tích danh mục/sản phẩm.
2. `late_delivery_risk` là nhãn kết quả gốc; `is_late_from_days` là biến tính lại, giữ riêng.
3. Mẫu KPI chính loại `Shipping canceled`; vẫn báo cáo tỷ lệ trên toàn nguồn và độ nhạy
   khi chỉ dùng trạng thái `COMPLETE`/`CLOSED`.
4. Mốc dự báo dự kiến là lúc đặt hàng. Các trường kết quả và cờ chọn mẫu không phải predictor.
5. DataCo phục vụ phân tích hiệu suất. Nếu nhóm triển khai tối ưu tuyến, cần thêm Solomon
   hoặc dữ liệu đủ xe/điểm nhận/khung giờ; chưa ghép hay tạo dữ liệu tuyến giả trong repo này.

Nguồn dataset giữ giấy phép riêng; repo chưa tự cấp giấy phép cho dữ liệu bên thứ ba.
Ghi công nguồn và các thay đổi theo hướng dẫn tại `docs/01_nguon_du_lieu.md`.
