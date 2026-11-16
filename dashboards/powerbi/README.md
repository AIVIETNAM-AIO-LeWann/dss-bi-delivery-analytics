# Mở và bảo trì Power BI

Delivery Insights có bốn trang chính và một trang lịch trình chi tiết. Màu sắc, bố cục và
cách dùng chỉ số được giải thích trong [design_notes.md](design_notes.md).

## Mở trên máy của thành viên

1. Tạo dữ liệu ở gốc repo bằng `.venv/Scripts/python -m dss_bi_delivery.dashboard_data`.
   Gói bàn giao đã kèm sáu CSV thì có thể bỏ qua bước này.
2. Mở `delivery_dashboard.pbip` bằng Power BI Desktop hỗ trợ PBIP/PBIR.
3. Transform data → Edit parameters: đặt `RepoRoot` thành thư mục có `data/` và `dashboards/`.
   Mặc định hiện là `D:/Projects/dss-bi-delivery-analytics`.
4. Apply changes và Refresh. Chờ nạp đủ dữ liệu trước khi đánh giá các biểu đồ.
5. Trong chế độ chỉnh sửa của Desktop, giữ Ctrl khi bấm nút điều hướng trên báo cáo.
   Khi xem báo cáo được xuất bản, chỉ cần bấm bình thường.

Không có dữ liệu cache nhị phân trong Git. Định nghĩa báo cáo, công thức và model được lưu
bằng văn bản. Không cần custom visual, tài khoản bản đồ hoặc dịch vụ hình ảnh bên ngoài.

## Giá trị mặc định

Ngưỡng cảnh báo 0,50. Cam kết “Thêm một ngày”, giữ nguyên Same Day. Tuyến mặc định
C101, tải 200, tối đa 25 xe, OR Tools. Quy đổi 1 km/đơn vị, tiêu hao 10 lít/100 km,
giá nhiên liệu 22.000 VND/lít. Đây là giả định mô phỏng.

## Mô hình và phạm vi lọc

12 bảng, 47 measures nghiệp vụ và 40 measures trình bày. Measures trình bày được ẩn,
chỉ định dạng thẻ số theo tiếng Việt và xử lý giá trị trống; không thay công thức số gốc.

Orders có một dòng/đơn, 62.897 dòng không hủy. P_Late chỉ có trên 13.071 đơn test.
PromiseScenarios có một dòng/(đơn test, chính sách), 65.355 dòng. Orders và Policies
lọc PromiseScenarios theo quan hệ 1:n một chiều. Không đếm bảng kịch bản làm tổng đơn.

PolicySelector tách khỏi quan hệ dữ liệu: điều khiển phương án đang xem mà không làm
biến mất bốn phương án còn lại trong bảng đối chiếu. Dòng Policies trong bảng so sánh
được ưu tiên khi tính chỉ tiêu từng dòng.

RouteCases lọc RouteStops theo 1:n. RouteMethods là bảng phương pháp độc lập để so sánh
hai lời giải cùng instance, scenario, sức chở và giới hạn xe. Chỉ tính tỷ lệ giảm khi có
đối chứng khả thi. Không có quan hệ Solomon với Orders. ModelMetrics là kết quả trên
toàn tập kiểm tra, không thay đổi theo bộ lọc Orders.

RiskThreshold, KmPerUnit, FuelConsumption và FuelPrice là bảng tham số rời. Ngưỡng
dùng CURRENCY để so sánh chính xác 0,40 và 0,50. Không có cảnh báo thì precision trống;
không có lời giải thì quãng đường/chi phí trống. Thẻ trình bày ghi “Chưa có”.

Bản đồ tuyến là SVG data URI từ RouteStops, được hiển thị bằng image visual native và
measure ImageUrl. Đường nối giữ thứ tự phục vụ và màu từng xe. Đây là tọa độ Solomon,
không phải km đường bộ hoặc vị trí đơn DataCo.

## Đối chiếu số liệu

Tổng quan: 62.897 đơn, 36.048 trễ, tỷ lệ 57,31%. Tập test: 13.071 đơn, 7.524 trễ.
Ngưỡng 0,50: 4.560 cảnh báo, 4.057 đúng, 503 sai, 3.467 bỏ sót; precision 88,97%,
recall 53,92%. Cam kết hiện tại vượt hẹn 57,56%; phương án thêm một ngày 26,82%,
tăng cam kết trung bình 0,94 ngày. C101/base/ortools: 10 xe, 828,9369 đơn vị,
nhiên liệu mô phỏng 1.823.661 VND với giả định mặc định.

## Kiểm tra khi thay đổi

```powershell
.venv/Scripts/python scripts/validate_powerbi.py
.venv/Scripts/python -m unittest discover -s tests -v
scripts/check_powerbi_native.ps1 -Port <cong_engine_cuc_bo> -ClientDirectory <thu_muc_client_net8>
```

Lệnh native chỉ đọc engine đang mở của dự án này. Dùng Microsoft.AnalysisServices.AdomdClient
từ NuGet trong cache cục bộ. Không commit client DLL hoặc cache Power BI.

Schema và CLI không chứng minh công thức hay hình thức chạy đúng. Sau khi build, phải
mở lại Desktop, refresh, kiểm tra từng trang và các tình huống thiếu dữ liệu. Kết quả được
tách trong `reports/dashboard/`: đầu vào, cấu trúc, DAX native và render native.

Nguồn thiết kế ở `src/dss_bi_delivery/powerbi_report.py`, nguồn model ở `powerbi_model.py`.
Đóng Desktop trước khi chạy `scripts/build_powerbi.py`; lệnh này thay toàn bộ file đã sinh.


## Rà bố cục native khi chỉnh thiết kế

Nguồn có kiểm tra giao nhau giữa các khung, nhưng chưa đủ để phát hiện font tràn bên trong.
Mở/refresh báo cáo trong Desktop với WebView debugging cục bộ rồi chạy
`node scripts/check_powerbi_layout.cjs`. Đặt PLAYWRIGHT_MODULE nếu Playwright chưa nằm
trong `.cache/browser/node_modules/playwright`, POWERBI_CDP_URL nếu đổi cổng mặc định 9223.
Chỉ dùng phiên Desktop của dự án này. Script đọc trang đang render, chuyển năm trang ở hai
kích thước, chụp vào `.cache/dashboard-native/` và ghi native_layout_validation.json.
Lịch trình nhiều điểm vẫn dùng cuộn dọc; đây là tương tác có chủ đích, không phải chữ chồng.
