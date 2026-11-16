# THƯ MỤC PHÂN TÍCH MÔ TẢ & CHẨN ĐOÁN (HOÀNG QUÂN - TV3)
**Chủ đề 18: Giao hàng đúng hẹn và tối ưu tuyến đường (Delivery Performance & Route Optimization)**  
**Thành viên:** Hoàng Quân (TV3 - Phân tích mô tả & chẩn đoán | Hạn hoàn thành: 05/11/2026)  
**Tập dữ liệu nguồn chuẩn hóa:** `data/processed/orders_analysis.csv` ($N = 62.897$ đơn hàng) & `order_items_clean.csv` ($N = 180.519$ dòng hàng) từ Lê Quang (TV2).  
**Tiêu chuẩn dữ liệu:** 100% số liệu được tính toán trực tiếp từ dữ liệu sạch, có bảng đối chiếu trong thư mục `tables/`, tuyệt đối không suy luận hay đưa ra kịch bản giả định.

---

## 1. MỤC TIÊU VÀ PHẠM VI CÔNG VIỆC

Theo phân công công việc của nhóm (Phần V - A: Phân tích mô tả & chẩn đoán):
- **Phân tích giao trễ (`late_delivery_risk`) tổng thể và theo các nhóm đơn hàng.**
- **Xác định các yếu tố/nhóm có liên hệ với rủi ro giao trễ.**
- **Thực hiện các phân tích thống kê phù hợp.**
- **Rút ra các nhóm rủi ro đáng chú ý.**
- *(Ghi chú: Tập trung trả lời "đang xảy ra gì?" và "có yếu tố/nhóm nào đáng chú ý?", không chạy quá nhiều biểu đồ/kiểm định nếu không phục vụ câu hỏi, không lấn sân sang các phần việc dự báo hay đề xuất).*

---

## 2. CẤU TRÚC THƯ MỤC TRÊN GITHUB

```
thong_ke_mo_ta/
├── README.md                          <- Giới thiệu thư mục và cấu trúc dữ liệu
├── BAO_CAO_MO_TA_VA_CHAN_DOAN.docx    <- Báo cáo Word (.docx) định dạng chuyên nghiệp, dễ đọc
├── BAO_CAO_MO_TA_VA_CHAN_DOAN.md      <- Báo cáo Markdown (.md) chuẩn hiển thị trên GitHub
├── run_pipeline.py                    <- Script tự động tái lập các bảng CSV và biểu đồ
│
├── tables/                            <- 12 bảng số liệu thống kê thực tế (.csv)
│   ├── 00_overview_baseline_kpis.csv            (Chỉ số trễ 57,31% & kiểm tra độ nhạy trên các tập mẫu)
│   ├── 01_shipping_mode_detailed.csv            (Thống kê chi tiết theo 4 phương thức vận chuyển)
│   ├── 02_mode_actual_days_distribution.csv     (Ma trận phân phối số ngày giao thực tế 0-6 ngày trong dữ liệu)
│   ├── 03_market_performance.csv                (Hiệu suất theo 5 thị trường toàn cầu)
│   ├── 04_region_performance.csv                (Hiệu suất chi tiết toàn bộ 23 vùng địa lý)
│   ├── 05_temporal_weekday_weekend.csv          (Phân tích theo thứ trong tuần & ngày thường vs cuối tuần)
│   ├── 06_temporal_year_month.csv              (Chuỗi thời gian lịch sử qua 37 tháng)
│   ├── 07_order_complexity_size.csv             (Phân tích theo quy mô đơn: số dòng hàng & nhóm số lượng)
│   ├── 08_customer_segment_payment.csv          (Phân khúc khách hàng & hình thức thanh toán)
│   ├── 09_departments_categories.csv           (Số lượng & tỷ lệ trễ theo ngành hàng & danh mục)
│   ├── 10_shipping_mode_by_market_matrix.csv    (Ma trận hai chiều: Phương thức x Thị trường)
│   └── 11_chi2_independence_tests.csv          (Bảng kiểm định Chi-bình phương & hệ số liên kết Cramer's V)
│
└── figures/                           <- 6 biểu đồ trực quan hóa độ phân giải cao (300 DPI PNG)
    ├── fig01_late_rate_by_shipping_mode.png     (Tỷ lệ trễ theo Phương thức vận chuyển vs Baseline)
    ├── fig02_actual_days_distribution.png       (Phân phối số ngày giao thực tế từ 0 đến 6 ngày)
    ├── fig03_market_performance.png             (Tỷ lệ trễ và tỷ trọng đơn theo Thị trường)
    ├── fig04_monthly_trend.png                  (Diễn biến sản lượng và tỷ lệ trễ qua 37 tháng)
    ├── fig05_weekday_performance.png            (Tỷ lệ trễ từ Thứ Hai đến Chủ Nhật)
    └── fig06_risk_heatmap.png                   (Bản đồ nhiệt ma trận rủi ro giao trễ)
```

---

## 3. CÁC PHÁT HIỆN THỰC NGHIỆM THEN CHỐT TỪ DỮ LIỆU

1. **Tỷ lệ trễ toàn hệ thống:** **57,31%** ($36.048 / 62.897$ đơn). Thời gian giao hàng thực tế trung bình là **3,50 ngày** so với cam kết **2,94 ngày** (chậm hơn trung bình **+0,57 ngày**).
2. **Hiệu suất theo Phương thức Vận chuyển:**
   - **First Class:** Trễ **100,00%** ($9.602 / 9.602$ đơn). Cam kết 1 ngày, thực tế luôn mất 2 ngày (độ lệch chuẩn = 0), ổn định suốt 37/37 tháng.
   - **Second Class:** Trễ **79,99%** ($9.803 / 12.256$ đơn). Cam kết 2 ngày, thực tế trung bình 4,00 ngày.
   - **Same Day:** Trễ **48,37%** ($1.648 / 3.407$ đơn). Cam kết 0 ngày, thực tế 48,37% đơn mất 1 ngày mới giao xong.
   - **Standard Class:** Trễ **39,85%** ($14.995 / 37.632$ đơn). Cam kết 4 ngày, thực tế trung bình 3,99 ngày.
3. **Phân phối số ngày giao hàng thực tế trong dữ liệu (Bảng 02):**
   - Với **Second Class** và **Standard Class**, số ngày giao thực tế từ 2 đến 6 ngày phân bổ đều xấp xỉ **20% cho mỗi ngày** (mỗi ngày chiếm từ 19,8% đến 20,2% số đơn). Đây là tần số xuất hiện thực tế đo đếm được từ dữ liệu gốc, không phải số liệu suy luận.
4. **Kiểm định Thống kê & Mối liên hệ:**
   - Phương thức vận chuyển là biến **duy nhất** có mối liên hệ có ý nghĩa thống kê với giao trễ ($\chi^2 = 14.530,75; p < 0,0001; \text{Cramer's } V = 0,4807$).
   - Các biến địa lý (thị trường, vùng), thời gian (thứ, cuối tuần, năm), quy mô đơn (số dòng, số lượng) và khách hàng đều có $p > 0,05$ và $V < 0,025$ (hoàn toàn độc lập với rủi ro trễ).
   - Mô hình hồi quy Logistic kiểm soát: Gửi bằng Second Class có cơ hội trễ gấp **6,03 lần** so với Standard Class ($OR = 6,034; p < 0,0001$). Same Day có cơ hội trễ gấp **1,41 lần** ($OR = 1,414; p < 0,0001$).

---

## 4. HƯỚNG DẪN CHẠY LẠI CODE (REPRODUCIBILITY)

Để tái lập toàn bộ 13 bảng CSV và 6 biểu đồ đồ họa:

```bash
cd dss-bi-delivery-analytics-main/thong_ke_mo_ta
python run_pipeline.py
```
Script sẽ tự động đọc dữ liệu sạch từ `../data/processed/` và cập nhật lại toàn bộ bảng và hình ảnh.
