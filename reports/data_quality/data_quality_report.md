# Báo cáo kiểm tra và làm sạch dữ liệu

Tự sinh từ đúng file Kaggle đã ghi SHA-256; không sử dụng số liệu chép từ notebook bên ngoài.

- Nguồn: **180,519 dòng × 53 cột**, **65,752 đơn**.
- Khóa dòng hàng duy nhất: 180,519; dòng trùng hoàn toàn: 0.
- Thời điểm đặt: 2015-01-01 00:00:00 đến 2018-01-31 23:38:00; thời điểm shipment đến 2018-02-06 22:14:00.
- Bảng dòng hàng giữ 180,519 dòng, 54 cột gồm cột dẫn xuất; bảng đơn có 65,752 dòng, 36 cột.
- Loại 14 cột nguồn theo chính sách; không xóa dòng hàng; không gán giá trị thiếu.
- Dòng logistics không hợp lệ: 0; đơn mâu thuẫn header: 0.

## Giá trị thiếu trong nguồn

| source_column | raw_missing | raw_missing_rate | treatment |
| --- | --- | --- | --- |
| Customer Lname | 8 | 4.431666472781258e-05 | drop_personal |
| Customer Zipcode | 3 | 1.661874927292972e-05 | keep_missing |
| Order Zipcode | 155679 | 0.8623967560201419 | keep_missing |
| Product Description | 180519 | 1.0 | drop_empty |

## KPI ban đầu và kiểm tra độ nhạy

| grain | cohort | records_in_cohort | late_count | labeled_count | late_rate | mean_actual_days |
| --- | --- | --- | --- | --- | --- | --- |
| order_item | all_source_labels | 180519 | 98977 | 180519 | 0.548291 | 3.497654 |
| order_item | non_canceled_valid | 172765 | 98977 | 172765 | 0.5729 | 3.498596 |
| order_item | complete_closed_sensitivity | 79107 | 45308 | 79107 | 0.572743 | 3.483674 |
| order | all_source_labels | 65752 | 36048 | 65752 | 0.548242 | 3.500897 |
| order | non_canceled_valid | 62897 | 36048 | 62897 | 0.573127 | 3.501518 |
| order | complete_closed_sensitivity | 28965 | 16633 | 28965 | 0.574245 | 3.494701 |

`all_source_labels` giữ mọi nhãn gốc, gồm hủy=0. `non_canceled_valid` loại trạng thái Shipping canceled và lỗi logistics; đây là mẫu KPI phân tích mặc định. `complete_closed_sensitivity` chỉ giữ COMPLETE/CLOSED để kiểm tra ảnh hưởng của trạng thái snapshot. Không gọi mẫu non_canceled là các đơn đã giao được xác thực.

## Phân phối sơ bộ ở cấp đơn

Số ngày shipping thực tế (mỗi khối xấp xỉ tỷ trọng so với nhóm lớn nhất):

```text
0 ngày | #### 1,844
1 ngày | ### 1,727
2 ngày | ######################################## 20,554
3 ngày | #################### 10,408
4 ngày | #################### 10,423
5 ngày | #################### 10,336
6 ngày | #################### 10,460
```

| shipping_mode | delivery_kpi_eligible | order_count | late_count | late_rate | mean_actual_days |
| --- | --- | --- | --- | --- | --- |
| First Class | 1 | 9602 | 9602 | 1.0 | 2.0 |
| Same Day | 1 | 3407 | 1648 | 0.48371 | 0.48371 |
| Second Class | 1 | 12256 | 9803 | 0.799853 | 4.002937 |
| Standard Class | 1 | 37632 | 14995 | 0.398464 | 3.994553 |

## Các vấn đề cần giải thích khi báo cáo

1. Đơn hủy: 7,754 dòng / 2,855 đơn. Có 4,423 dòng hủy với delay_days>0 nhưng nhãn gốc 0; giữ hai đại lượng riêng.
2. Khoảng hai timestamp khác số ngày shipping ở 9,737 dòng. Không sửa duration từ timestamp; xem phân phối Same Day và giả định A04.
3. CP1252 giải mã nghiêm ngặt được toàn bộ file và không sinh C1 control; Latin-1 sinh 20 ký tự C1 trong địa danh. Một số địa danh đã có dấu hỏi ngay trong nguồn, chưa phục hồi được.
4. Latitude/Longitude mô tả vị trí cửa hàng; không có kho xuất phát được xác thực, điểm nhận, xe, sức chở hay khung giờ. Dữ liệu này chưa đủ tối ưu tuyến.
5. Cột lợi nhuận trùng nhau và ngữ nghĩa cấp dòng chưa rõ. Giữ một cột để truy nguyên; không công bố tổng lợi nhuận đơn hoặc chi phí giao trễ từ chúng.
6. Số ngày kế hoạch gắn chặt Shipping Mode trong bản này; quan hệ giữa phương thức và trễ không chứng minh phương thức gây trễ.
7. Không có tổng kiểm soát độc lập từ doanh nghiệp. Kiểm tra checksum, số dòng và đối chiếu nội bộ không chứng minh dữ liệu đầy đủ so với hệ thống gốc.

## Bằng chứng và nhật ký

`column_profile.csv`: 53 cột và thiếu/miền; `preparation_log.csv`: nhật ký 4 bước và số dòng ảnh hưởng; `order_header_consistency.csv`: nhất quán cấp đơn; `numeric_summary.csv`: thống kê; `initial_distributions.csv`: phân phối sơ bộ; `label_consistency.csv`: nhãn; `baseline_kpis.csv`: KPI.

## Làm sạch bổ sung và bàn giao phân tích

Các bảng trên giữ toàn bộ nguồn để đối chiếu. Bảng dùng cho mô tả/chẩn đoán là `data/processed/orders_analysis.csv`; dữ liệu dự báo được tách feature/label/split. Xem [analysis_readiness_report.md](analysis_readiness_report.md) cho xử lý địa danh hỏng, quy tắc loại mẫu, điều tra theo tháng và kiểm tra bàn giao.
