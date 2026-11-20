# 7.1 Hạn chế và dữ liệu cần bổ sung, Ngọc Quang, hạn 24/11/2026

Bộ này thuộc phần việc của Ngọc Quang trong Phần VII. Mục 7.2 Hướng phát triển của Hoài Phú nằm ở `../future_work/` và không bị sửa.

- [Báo cáo Markdown](section_vii_limitations.md) dùng để đọc và rà trên GitHub.
- [Báo cáo Word](section_vii_limitations.docx) dùng để ghép báo cáo nhóm. Khổ Letter, Times New Roman 13, chữ đen; các bảng nhiều cột dùng cỡ 11. Bản hiện tại dài 10 trang.
- [code/verify_figures.py](code/verify_figures.py) kiểm tra lại mọi con số được trích, so với file nguồn trong repo.
- [code/build_docx.py](code/build_docx.py) tạo bản Word từ bản Markdown.
- `tables/figure_checks.csv` là kết quả của lần kiểm tra số liệu gần nhất: mỗi dòng gồm khóa, giá trị, giá trị mong đợi và file nguồn.

## Nội dung

Có 13 hạn chế (H1–H13), xếp theo bảy nhóm: nguồn và mẫu; nhãn và rò rỉ; mô tả và chẩn đoán; dự báo; cam kết; tuyến Solomon; dashboard. Mỗi hạn chế gồm bằng chứng, ảnh hưởng và dữ liệu cần bổ sung, trong đó dữ liệu được tách thành "thiếu thực sự" và "đã có, chưa dùng". Cuối bài có ba bảng: Bảng 7.1.1 (hạn chế, bằng chứng, ảnh hưởng, dữ liệu cần bổ sung, mức ưu tiên), Bảng 7.1.2 (dữ liệu theo loại, nguồn và mục đích) và Bảng 7.1.3 (nguồn bằng chứng, có liên kết tới commit `6b5acb7`).

## Những việc đã làm

1. Đọc README, CONTRIBUTING, `docs/project/context.md`; repo không có AGENTS.md hay CLAUDE.md.
2. Đọc tài liệu chuẩn bị dữ liệu (01, 03, 05, 07), báo cáo chất lượng dữ liệu, bảng và báo cáo mô tả, kết quả và nhật ký dự báo, kết quả và mã của phần đề xuất, Phần VI và mục 7.2.
3. Đọc phần "Hạn chế và dữ liệu cần bổ sung" trong `workstreams/forecasting/Bao_cao_Ngoc_Quang_Chu_de_18.docx` (05/11/2026) rồi mở rộng ra toàn bộ nghiên cứu. File Word cũ được giữ nguyên.
4. Viết mã kiểm tra 91 con số và mệnh đề với file nguồn; cả 91 đều đạt.
5. Tạo bản Word, xuất PDF bằng Microsoft Word và xem lần lượt cả 10 trang: chữ không tràn khung, bảng không vỡ dòng giữa trang, tiêu đề bảng lặp lại khi bảng sang trang mới.

Không sửa dữ liệu, không huấn luyện lại mô hình, không chạy lại bộ giải, không sửa dashboard, không ghi đè `results/` hay mục 7.2.

## Điểm chưa kiểm chứng

- Không mở dữ liệu thô hay bảng sạch, vì chúng không nằm trong Git. Mọi số liệu đều lấy từ các bảng tổng hợp đã bàn giao, nên độ đúng của chúng phụ thuộc vào các bước trước đó.
- Không chạy lại unittest của repo, `check_project.py` hay các bản replay. Con số 153 phép so sánh của dashboard được trích từ README, chưa chạy lại.
- Chưa đối chiếu bản Kaggle với Mendeley V5 và chưa đối chiếu Solomon với SINTEF. Hai việc này được ghi là dữ liệu "đã có, chưa dùng", không phải việc đã làm.
- Nhận xét về các mẫu hình đều đặn bất thường của DataCo (H1) dựa trên phân phối đã quan sát, không dựa trên tài liệu của tác giả dữ liệu; bài không khẳng định dữ liệu được mô phỏng.
- Nguồn dự kiến cho dữ liệu cần bổ sung là đề xuất. Chưa có xác nhận từ doanh nghiệp nào rằng dữ liệu này tồn tại hay có thể chia sẻ.

## Tạo lại

Cần Python 3.12 và `python-docx==1.2.0`. Từ gốc repo:

```sh
python -m pip install python-docx==1.2.0
python deliverables/report/section_vii/limitations/code/verify_figures.py
python deliverables/report/section_vii/limitations/code/build_docx.py
```

`verify_figures.py` chỉ đọc file đã được Git theo dõi và trả mã lỗi 1 nếu có con số lệch. Nếu nhóm cập nhật kết quả bàn giao, hãy chạy lại lệnh này trước, sửa bản Markdown cho khớp, rồi mới tạo lại bản Word. Sau khi tạo lại, mở bản Word để kiểm tra bố cục từng trang.
