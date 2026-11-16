# Bộ nộp TV5 Hoài Phú hạn 10/11/2026

**Chủ đề 18: Giao hàng đúng hẹn và tối ưu tuyến đường.** Bối cảnh: DHL Supply Chain North America. Bộ này chỉ gồm **Phân tích đề xuất hạn 10/11**, chưa làm phần Hướng phát triển hạn 24/11.

## Đọc và nộp từ đâu

1. **`Bao_cao_TV5_Hoai_Phu_10-11.docx`**: báo cáo Word chính, có khuyến nghị, điều kiện áp dụng, bảng kết quả, sơ đồ tuyến và nguồn tham khảo.
2. **`DOI_CHIEU_THANH_VIEN.md`**: bằng chứng đối chiếu TV5 với phân công và đầu ra hiện có của cả nhóm; ghi rõ chưa có báo cáo riêng TV1/TV6 trong thư mục được cung cấp.
3. **`results/`**: kết quả thực nghiệm và bảng bàn giao TV6. Những chi phí mô phỏng được tách riêng, không phải chi phí thực tế của DHL.

Có thể nộp toàn bộ thư mục `10-11` hoặc file nén cùng tên. Không cần nộp lại các thư mục làm việc cũ ở ngoài thư mục này. Các kết quả cũ được giữ để truy nguyên; bộ nộp trong `10-11` là phiên bản đã rà soát và đóng gói.

## Cấu trúc thư mục

```text
10-11/
├── Bao_cao_TV5_Hoai_Phu_10-11.docx
├── README.md
├── DOI_CHIEU_THANH_VIEN.md
├── requirements.txt
├── package_manifest.json
├── code/                 Mã tính toán, tạo báo cáo và kiểm chứng
├── inputs/
│   ├── dataco/           Dữ liệu sạch, cách chia tập và dự báo kế thừa
│   └── *.txt            C101, R101, RC101 nguyên tệp tải để thử nghiệm
├── results/              Cam kết, tuyến, cận dưới đội xe, nhiên liệu, kiểm tra
├── figures/              Sơ đồ tuyến benchmark; PNG dùng trong báo cáo
└── evidence/             Bản sao tài liệu và bảng bàn giao TV2–TV4 để đối chiếu
```

## Phần việc TV5 đã hoàn thành

- Chuyển phát hiện TV3 và xác suất TV4 thành các phương án điều chỉnh cam kết, nêu rõ đánh đổi về thời gian khách chờ và tỷ lệ vượt hẹn.
- Dùng train để tính phân vị theo phương thức/vùng, với fallback khi ít đơn; kiểm tra riêng validation và test, cùng độ nhạy ngưỡng nhóm.
- Bổ sung bảng theo phương thức: phương án +1 ngày còn vượt hẹn 60,52% ở Second Class trên test, nên không khuyến nghị áp dụng chung chỉ vì KPI toàn mẫu giảm.
- Xây nguyên tắc ưu tiên theo giá trị kỳ vọng; chưa gán chi phí hoặc hiệu quả can thiệp không có trong nguồn thành số liệu thực tế.
- Giải thử VRPTW, so với điểm gần nhất khả thi, kiểm tra tải và khung giờ, công khai trường hợp đối chứng không tìm được lời giải.
- Chứng minh riêng C101/Q=200 cần tối thiểu 10 xe bằng cận dưới sức chở và tuyến khả thi 10 xe. Chưa chứng minh quãng đường tối ưu.
- Quy đổi nhiên liệu theo kịch bản và lưới độ nhạy. Không công bố ROI, lợi nhuận ròng, chi phí thay thế nhân viên hoặc tiền tiết kiệm doanh nghiệp đã xảy ra.

## Các file kết quả chính

| File trong `results/` | Nội dung và cách đọc |
| --- | --- |
| `promise_summary.csv` | 33 hàng, 11 chính sách × train/validation/test. `n` là số đơn; các tỷ lệ lưu 0–1; số ngày không đổi đơn vị. |
| `promise_scenario_parameters.csv` | Mục tiêu đúng hẹn và số đơn train tối thiểu của 9 kịch bản phân vị. Đây là tham số thử nghiệm, chưa được doanh nghiệp duyệt. |
| `promise_validation_screen.csv` | Kiểm tra mục tiêu trên validation. Không dùng test để chọn kịch bản thắng. |
| `promise_by_mode_region_test.csv` | Chi tiết phương thức–vùng trên test, gồm nhóm fallback. |
| `promise_orders_*.csv` | Kết quả từng đơn test cho hiện trạng, các phân vị và phương án giới hạn +1 ngày. |
| `pilot_by_mode_test.csv` | Số đơn, cam kết và tỷ lệ vượt hẹn trước/sau tính lại theo từng phương thức. |
| `pilot_duration_sensitivity.csv` | Độ nhạy khi giữ nhóm timestamp nhất quán; nhóm này loại toàn bộ Same Day nên không đại diện đủ bốn phương thức. |
| `risk_groups_test.csv` | Bốn mức xác suất theo phương thức của mô hình TV4, không phải rủi ro cá nhân khác nhau trong cùng phương thức. |
| `dashboard_orders_test.csv` | 13.071 đơn test đã ghép P_Late của TV4 với phương án giới hạn của TV5; bàn giao cho TV6. |
| `routing_summary.csv` | Kết quả theo instance, K/Q và phương pháp; quãng đường là đơn vị benchmark, chưa phải km đường bộ. |
| `fleet_sizing_bounds.csv` | Tổng nhu cầu, cận dưới số xe, số xe khả thi và trạng thái chứng minh số xe tối thiểu. |
| `route_*.json`, `route_stops_*.csv` | Thứ tự khách theo xe và thời điểm bắt đầu phục vụ, tải tích lũy; node 0 là kho, 1–100 là khách Solomon. |
| `fuel_scenarios.csv` | 27 tổ hợp quy đổi/tiêu hao/giá cho mỗi lời giải khả thi. Mọi trường có hậu tố `_assumption` là giả định kịch bản. |
| `run_manifest.json` | Cấu hình và nguồn của lượt chạy gốc; giữ các đường dẫn nguồn gốc để truy nguyên. |
| `context_manifest.json` | Bối cảnh DHL, workbook phân công và khác biệt nguồn Kaggle. |
| `replay_validation.json` | Ghi nhận chạy lại độc lập từ gói dữ liệu và khác biệt hợp lệ do giới hạn thời gian giải; báo cáo vẫn dùng kết quả lượt chạy gốc. |
| `verification.json`, `handoff_audit.json` | Kết quả đọc lại và tính lại từ đầu vào đóng gói; không phải đánh giá triển khai doanh nghiệp. |

Trong `routing_summary.csv`, `feasible` nghĩa đã có tuyến được kiểm tra. `no_solution_found` nghĩa phương pháp chưa tìm được lời giải hoàn chỉnh trong cấu hình đã chạy, không chứng minh bài toán vô nghiệm. Ô số xe/quãng đường để trống khi không có lời giải; không thay bằng 0.

## Lưu ý cho TV6 và người tổng hợp

- Mã `order_id` phải import dạng **Text**. Chỉ join DataCo với DataCo theo khóa này; không ghép sang node Solomon.
- `P_Late` là xác suất vượt **cam kết cũ**, có điều kiện không hủy trong snapshot. Không coi đó là xác suất vượt cam kết mới hoặc hiệu quả can thiệp.
- `late_current`/`exceed_proposed` là cờ hồi cứu theo duration nguồn. `proposed_days` là đầu ra kịch bản, chưa phải cam kết đã triển khai. Giảm tỷ lệ vượt hẹn không làm thay đổi thời gian giao thực tế.
- Các file cấp đơn bàn giao đều là test 01/07/2017–31/01/2018, không phải hoạt động năm 2026. Số liệu toàn mẫu 62.897 đơn dùng mẫu số khác.
- Dashboard cần nhãn riêng cho thực nghiệm DataCo, benchmark Solomon và tiền mô phỏng. Chỉ TV6 sửa dashboard chính theo phân công.

## Nguồn dữ liệu và giới hạn

DHL là bối cảnh tham chiếu, dựa trên [Dang và cộng sự, 2024](https://doi.org/10.1287/inte.2023.0087). Thành tích TNO được dẫn để giải thích ý nghĩa quản trị, không chuyển thành hiệu quả kỳ vọng của TV5.

Link nhóm cung cấp: [DataCo trên Kaggle/shashwatwork](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis). Tuy nhiên manifest TV4 ghi nguồn tải `saicharankomati/dataco-supply-chain-dataset`, version 1, raw CSV SHA-256 `994b3c8d24049cc46bf20e8161fedece9a9b95376cc0dc929921d76cf6b9bc0d`. Chưa xác nhận hai bản giống byte. Bộ nộp giữ nguyên đầu vào đã được nhóm bàn giao, không tải đè dữ liệu để đổi nguồn trích dẫn.

Solomon tham chiếu [SINTEF](https://www.sintef.no/projectweb/top/vrptw/100-customers/). Tải trực tiếp từng gặp HTTP 403; các tệp trong `inputs/` lấy từ bản sao công khai có URL/hash trong manifest gốc. Chưa đối chiếu byte với ZIP SINTEF. Không lấy kết quả hoặc mã giải của bản sao làm kết quả của nhóm.

Không đưa raw DataCo 95 MB, thông tin liên hệ khách hàng, mô hình nhị phân hoặc file dashboard của thành viên khác vào bộ này. Dữ liệu bên thứ ba giữ giấy phép riêng, không được bộ nộp tự cấp giấy phép mới.

## Kiểm tra và tái lập

Mã phân tích đã chạy trên Python 3.14.7 với các phiên bản thư viện trong `requirements.txt`. Mã kiểm chứng và tạo Word cũng đã được kiểm tra trên runtime Python đóng gói của Codex. Không cần mạng để đọc hoặc kiểm chứng các kết quả đã lưu, sau khi có thư viện.

Từ chính thư mục `10-11`, cài trong môi trường riêng và kiểm chứng:

```sh
python3 -m pip install -r requirements.txt
python3 code/verify_results.py
python3 code/verify_handoffs.py
```

Chạy lại phân tích tùy chọn:

```sh
python3 code/run_analysis.py --output replay
python3 code/fleet_bounds.py --results replay
python3 code/verify_results.py --results replay
python3 code/verify_handoffs.py --results replay
```

Lệnh trên chỉ đọc các đầu vào đóng gói và ghi vào `replay/`, không ghi đè `results/`. OR-Tools chạy theo giới hạn thời gian, nên thứ tự tuyến/quãng đường có thể khác đôi chút theo máy. Đối chiếu và kiểm tra lời giải mới trước khi thay kết quả đã nộp; chưa tự cập nhật báo cáo Word theo một lần chạy mới.

Tái tạo báo cáo từ **kết quả đã đóng băng trong results/**:

```sh
python3 code/verify_handoffs.py
python3 code/write_report.py
python3 code/build_docx.py
```

Hai hình PNG cần cho Word đã kèm trong `figures/`. Mã `build_docx.py` dùng `python-docx`. Nếu chỉnh nội dung/layout, phải xuất và kiểm tra lại từng trang trước khi nộp. Ảnh render/PDF phục vụ kiểm tra không được đưa vào bộ nộp.

## Nhật ký dùng AI

Ngày 06/11/2026: AI hỗ trợ đọc đề và các đầu ra, kiểm tra bằng mã, thiết kế kịch bản, chạy tối ưu tuyến, rà cách diễn giải và tạo báo cáo. Kết quả tính có bảng/mã truy nguyên; mục tiêu dịch vụ và đầu vào tiền thiếu được ghi thành kịch bản. Hoài Phú cần hiểu và chịu trách nhiệm trình bày phần chuyên môn khi nộp/thuyết trình. Nhật ký này không thay thế việc tự kiểm tra số liệu hoặc xác nhận chính sách doanh nghiệp.
