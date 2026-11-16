# Mở dự án Power BI

Trạng thái: **đã mở, refresh và kiểm tra DAX native trên Power BI Desktop Store 2.159.1231.0**.
21 kiểm tra DAX đạt; đã chụp/rà các trang native và sửa các lỗi metadata, độ chính xác ngưỡng và cắt chữ phát hiện trong lần kiểm tra.

## Thiết lập

1. Tại gốc repo, cài môi trường theo runbook và tạo đầu vào:
   `.venv/Scripts/python -m dss_bi_delivery.dashboard_data`.
2. Mở `delivery_dashboard.pbip` bằng Power BI Desktop có hỗ trợ PBIP/PBIR.
3. Vào Transform data → Edit parameters, đặt `RepoRoot` thành thư mục repo trên máy bạn.
   Giá trị hiện được sinh cho `D:/Projects/dss-bi-delivery-analytics`; chỉ thay tham số này khi đổi máy.
4. Apply changes / Refresh để nạp sáu CSV trong `data/dashboard/`.
5. Chọn trang Rủi ro và ngưỡng 0,50; chọn Cam kết với chính sách +1 ngày; chọn tuyến
   `c101|base|ortools`. Các giá trị tham số chưa chọn dùng mặc định trong measures.

Không có cache dữ liệu nhị phân trong Git. Repo lưu định nghĩa báo cáo và model bằng văn bản;
CSV đầu vào được sinh cục bộ từ các nguồn bàn giao.

## Mô hình

- Orders: một dòng/đơn, 62.897 dòng. P_Late chỉ điền cho test, để trống ngoài test.
- PromiseScenarios: một dòng/(đơn test, chính sách), 65.355 dòng; không đếm bảng này như tổng đơn.
- Policies → PromiseScenarios: 1:n. Orders → PromiseScenarios: 1:n qua order_id.
- RouteCases → RouteStops: 1:n. Không có quan hệ giữa Solomon và Orders.
- ModelMetrics độc lập; bảng so sánh ghi cả validation và test, không bị lọc bởi vùng/đơn.
- RiskThreshold, KmPerUnit, FuelConsumption, FuelPrice là bảng tham số rời.

Các quan hệ lọc một chiều từ bảng 1 sang bảng n; mã là Text, tỷ lệ 0–1.
Chi phí nhiên liệu = quãng đường benchmark × km/đơn vị × lít/100km ÷100 × VND/lít.
Không có lời giải thì distance và cost để trống; không đưa về 0.

## Các mốc đã đối chiếu native và cần giữ khi chỉnh tiếp

- Mở không lỗi; Apply/Refresh thành công; không có lỗi M hoặc DAX.
- Trang Tổng quan không lọc: 62.897 đơn, 36.048 trễ, 57,31%.
- Trang Rủi ro ngưỡng 0,50: 13.071 test, 4.560 cảnh báo, 4.057 TP, 503 FP,
  3.467 FN; precision 88,97%, recall 53,92%. ModelMetrics không đổi theo bộ lọc Orders.
- Lọc Standard Class ở trang Rủi ro: không có cảnh báo tại 0,50; precision trống.
- Chính sách current: 57,56% vượt hẹn test; +1 ngày: 26,82%, cam kết tăng 0,94 ngày trung bình.
- C101/base/ortools: 10 xe, 828,9369 đơn vị; nhân giá nhiên liệu phải thay đổi chi phí tuyến đã chọn.
- Case không có lời giải: distance/cost không hiển thị 0 hoặc tuyến cũ.
- Kiểm tra tên vai trò visual, dropdown, trục, nhãn, không cắt chữ và tương tác lọc.
- Kiểm tra scatter điểm dừng đủ kho/khách; nếu cần bản đồ có đường nối tuyến, hoàn thiện trong Desktop
  hoặc dùng hình/tuyến preview làm trực quan hóa hỗ trợ với nhãn benchmark rõ ràng.
- Lưu lại PBIP, rà Git diff. Chỉ xuất PBIX để nộp khi đã kiểm tra; PBIX không theo dõi trong Git mặc định.

## Kiểm tra cấu trúc bằng schema

```powershell
.venv/Scripts/python -m pip install -e ".[dashboard]"
.venv/Scripts/python scripts/validate_powerbi.py
```

Lần đầu cần mạng để lấy schema chính thức, sau đó dùng cache `.cache/powerbi-schemas/`.
Kiểm tra này không biên dịch DAX/M, không chứng minh visual native chạy và không thay thế nghiệm thu trên.

Tài liệu định dạng: [PBIP](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview),
[PBIR](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report),
[Semantic model](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-dataset).

## Kiểm tra lại DAX native (tùy chọn)

Mở báo cáo và refresh trước. Dùng PowerShell 7 cùng client Microsoft.AnalysisServices.AdomdClient
từ NuGet (được đặt trong cache cục bộ, không commit DLL). Chạy:

```powershell
scripts/check_powerbi_native.ps1 -Port <cong_engine_cuc_bo> -ClientDirectory <thu_muc_client_net8>
```

Chỉ trỏ vào engine của dự án này. Script chỉ đọc DAX và ghi báo cáo kiểm tra, không sửa model.
Bảng ngưỡng dùng CURRENCY để giá trị 0,40/0,50 so sánh chính xác, tránh lỗi double.

Công cụ authoring Microsoft được cài cục bộ trong .cache/powerbi-tools khi QA;
không cần nó để mở báo cáo. Có thể kiểm tra lại bằng CLI sau khi cài vào cache theo tài liệu Microsoft.
