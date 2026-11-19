# Bằng chứng và kiểm tra cho bản bàn giao kể chuyện

Tài liệu để đọc và viết tiếp: [storytelling_handoff.md](../../deliverables/report/storytelling_handoff.md).

- `evidence.json`: số liệu từ các bảng TV2–TV5, mẫu số, checksum nguồn và 31 phép đối chiếu tổng hợp.
- `figure_manifest.json`: phiên bản Matplotlib, checksum bằng chứng và tám file hình (bốn PNG, bốn SVG).
- Hình tại `deliverables/report/figures/`, chỉ giữ thông tin đọc biểu đồ; nguồn và giới hạn nằm trong tài liệu bàn giao.

## Kiểm tra ngày 19/11/2026

```powershell
.venv/Scripts/python scripts/build_storytelling_evidence.py --check
.venv/Scripts/python -m unittest discover -s tests -v
git diff --check
```

31 phép đối chiếu tổng hợp đạt; evidence lưu khớp bảng nguồn. Đã kiểm tra checksum
tám file hình, liên kết nội bộ của tài liệu và nhìn trực tiếp cả bốn PNG sau lần
bỏ dòng nguồn. Không còn nhãn cắt khỏi ảnh hoặc chú giải chồng lên nội dung.

Unittest gốc ghi nhận 9 bài chạy đạt; lớp kiểm tra Dashboard bị skip do chưa có
các CSV `data/dashboard` cục bộ. Kết quả này không xác nhận lại giao diện Dashboard,
huấn luyện hoặc bộ giải. Đợt bàn giao không sửa các phần đó; các bảng kết quả và
snapshot bàn giao được giữ nguyên.

Khi bảng nguồn thay đổi, chạy lại script evidence, xem lại nội dung số trong bản
viết, dựng lại hình và kiểm tra layout. Cập nhật số liệu trong đoạn văn là bước
biên tập có chủ đích; script không tự đổi lập luận hoặc khuyến nghị.
