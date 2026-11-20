# Hướng phát triển của Hoài Phú hạn 24/11/2026

Bộ này thuộc phần việc TV5 trong `deliverables/report/section_vii/future_work/` của repo chung.

- [Báo cáo Markdown](section_vii_future_work.md) dùng để đọc và rà nội dung trên GitHub.
- [Báo cáo Word](section_vii_future_work.docx) dùng để ghép báo cáo nhóm. Chữ Times New Roman 13, màu đen.
- `figures/` có hai biểu đồ PNG được tạo bằng mã.
- `tables/` có ba CSV dùng tạo bảng số liệu.
- [code/build_report.py](code/build_report.py) tạo lại báo cáo, bảng và hình từ kết quả bàn giao.

## Tạo lại trong repo chung

Cần Python 3.12, font Times New Roman, matplotlib 3.10.8 và python-docx 1.2.0. Từ gốc repo chạy

```sh
python -m pip install matplotlib==3.10.8 python-docx==1.2.0
python deliverables/report/section_vii/future_work/code/build_report.py
```

Mã đọc `workstreams/prescriptive/results/pilot_by_mode_test.csv`, `promise_summary.csv`, `fleet_sizing_bounds.csv` và `workstreams/forecasting/results/model_comparison.csv`. Các đầu vào này được Git theo dõi. Đầu ra mặc định nằm trong thư mục chứa README này.

Có thể dùng `--source-root <repo_chung>` để chỉ định đầu vào và `--output-root <thu_muc_xem_thu>` để tạo bản xem thử riêng. Kiểm tra bố cục Word sau khi tái tạo.

## Phạm vi bản bàn giao

Báo cáo gồm ba hướng phát triển, ba bảng số liệu, hai biểu đồ và bảng nguồn cuối bài. Các mục 7.3 và 7.4 đã được bỏ theo yêu cầu của Hoài Phú. Nguồn của mỗi bảng và hình được liên kết ngay trong bảng cuối bài.
