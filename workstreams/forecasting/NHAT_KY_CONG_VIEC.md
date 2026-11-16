# Những việc đã thực hiện cho Ngọc Quang

Ngày thực hiện: 05/11/2026. Chủ đề 18 — Giao hàng đúng hẹn và tối ưu tuyến đường.
Phạm vi được giao: phân tích dự báo và hạn chế/dữ liệu cần bổ sung. Đã hoàn thành thực nghiệm dự báo và bản viết tương ứng; hiệu quả triển khai thực tế chưa được kiểm chứng.

## 1. Đọc và chốt yêu cầu
- Đọc đề bài, tab PROMPT và bảng PHÂN CÔNG; áp dụng xác nhận của nhóm rằng Chủ đề 18 là chủ đề chính thức.
- Chuyển phạm vi từ nội dung nhân sự đang còn trong bảng phân công sang dự báo giao trễ DataCo. Không sửa bảng Google Sheet.

## 2. Tái tạo dữ liệu chung
- Tải snapshot mã chuẩn bị của Lê Quang tại commit 6fd157327b8fc05d6011e71659db86048dead818.
- Tải đúng CSV Kaggle phiên bản 1, đối chiếu SHA-256 994b3c8d24049cc46bf20e8161fedece9a9b95376cc0dc929921d76cf6b9bc0d.
- Chạy lại prepare_data và verify_data; 51/51 kiểm tra nguồn đạt, 24/24 kiểm tra bảng analysis đạt.
- Xác nhận 180.519 dòng hàng, 65.752 đơn nguồn, 62.897 đơn không hủy trong mẫu chính; không sửa nhãn gốc.
- Khắc phục tương thích môi trường bằng pandas 2.3.3 sau khi tái hiện lỗi pandas 3 trên trường hợp map datetime rỗng; không sửa mã chuẩn bị chung.

## 3. Xây pipeline dự báo
- Ghép feature/label/split bằng order_id và kiểm tra khóa 1:1, không ghép theo vị trí dòng.
- Dùng 13 biến allowlist; loại ID/timestamp thô và các biến kết quả khỏi predictor.
- Giữ train 39.568, validation 9.497, test 13.071; 761 đơn khoảng đệm không fit/chọn/chấm điểm.
- Fit toàn bộ preprocessing chỉ trên train; xử lý danh mục mới ở bước dự báo.
- Chạy baseline theo phương thức, logistic regression và histogram gradient boosting với cấu hình cố định.
- Chọn mô hình theo log loss validation trước khi xem test, giữ nguyên train sau chọn.

## 4. Kết quả thực nghiệm
- Mô hình được chọn: baseline theo phương thức vận chuyển.
- Test AUC 0,746; AP 0,788; log loss 0,536; Brier 0,188.
- Ngưỡng 0,5: precision 89,0%, recall 53,9%, accuracy 69,6%, F1 0,671.
- 4.057 cảnh báo đúng, 503 cảnh báo sai, 3.467 đơn trễ bỏ sót, 5.044 đơn không trễ dự báo đúng.
- Logistic có AP cao hơn baseline; không tuyên bố baseline tốt nhất theo mọi tiêu chí và không đổi lựa chọn sau khi xem test.

## 5. Kiểm tra bổ sung
- Độ nhạy bỏ First Class khỏi test, chỉ timestamp nhất quán và logistic bỏ đồng thời phương thức/ngày cam kết.
- Bảng kết quả theo tháng/vùng/phương thức; calibration và threshold sweep trên validation.
- 8/8 contract tests mới đạt; 7/7 tests chuẩn bị dữ liệu của nhóm đạt trong môi trường ghim phiên bản.
- Review độc lập phát hiện lỗi lưu custom estimator dưới __main__; đã tái hiện bằng test tiến trình mới, chuyển estimator sang baseline.py và kiểm tra lại thành công.
- 12/12 kiểm tra độc lập file đầu ra đạt, gồm nạp model ở tiến trình mới, tính lại metrics từ CSV, không mất/trùng ID và không xuất dự báo khoảng đệm.

## 6. Sản phẩm bàn giao
- Bao_cao_Ngoc_Quang_Chu_de_18.docx: nội dung Phần V và Phần VII.
- results/predictions_test.csv: 13.071 đơn ngoài mẫu với P_Late, nhãn thật và ngữ cảnh đánh giá.
- results/predictions_by_partition.csv: 62.136 đơn được gắn rõ train/validation/test; không dùng toàn bộ file để báo cáo hiệu quả.
- code/: mã huấn luyện, tạo hình, dự báo từ model lưu, kiểm chứng và tests.
- models/selected_model.joblib: mô hình đã chọn, được fit trên train.
- inputs/: feature, label, split và schema; source_snapshot/: mã/tài liệu chuẩn bị của nhóm và bốn bảng cần để chạy lại.
- results/: toàn bộ metrics, lựa chọn mô hình, ngưỡng, độ nhạy, kết quả theo nhóm/tháng, kiểm chứng và manifest.
- figures/: hai hình phục vụ báo cáo. README.md: cách chạy lại và bàn giao.

## 7. Các giới hạn được ghi rõ
- Xác suất có điều kiện không hủy; chưa phải xác suất cho mọi đơn mới.
- Baseline có bốn mức xác suất; không xếp hạng được các đơn cùng phương thức.
- First Class có nhãn trễ 100% trong nguồn; không suy rộng thành quy luật thực tế.
- Chưa có kiểm định ý nghĩa thống kê chênh lệch giữa mô hình, khoảng tin cậy hoặc đánh giá triển khai năm 2026.
- Chưa tối ưu ngưỡng theo chi phí, chưa lượng hóa lợi ích can thiệp, chưa giải tuyến VRPTW.
- Phần của Quân, Phú và Quốc vẫn có thể tiếp tục dùng chung dữ liệu và nhận file bàn giao này.

## 8. Nhật ký sử dụng AI
AI hỗ trợ đọc đề, thiết kế pipeline, viết mã, kiểm tra, diễn giải và soạn báo cáo. Số liệu trong báo cáo được tính bằng mã từ đúng dữ liệu có checksum; không tự tạo kết quả mô hình. Có bước review độc lập mã và kiểm tra lại đầu ra. Ngọc Quang cần đọc, hiểu và tự trình bày phương pháp/kết quả khi nộp bài.

## 9. Rà soát lần cuối trước khi bàn giao
- Chạy lại 8 tests dự báo và 7 tests chuẩn bị dữ liệu; tất cả đạt.
- Kiểm chứng lại nguồn 51/51 và đầu ra 12/12; nạp model bằng tiến trình mới và đối chiếu toàn bộ 13.071 xác suất test.
- Review độc lập đối chiếu nội dung Word/README với CSV, feature hashes, partition và prediction_context; không còn lỗi mô hình, phương pháp hoặc số liệu cần sửa.
- Sửa câu hướng dẫn README: các lệnh tái tạo từ raw chạy ở thư mục gốc bộ bàn giao; script tự xác định source_snapshot. Không đổi kết quả mô hình.
- Chuyển báo cáo Word đã kiểm tra sang Google Docs và đọc lại: đủ nội dung, 5 bảng, 2 hình và các tiêu đề.
- Bản báo cáo trực tuyến: https://docs.google.com/document/d/1o1Mv3GSJPJjzRc5iXewK0ULeaZiGevxNOIkLlZGZk3k/edit?usp=drivesdk
- Dự báo hạn 7/11 là phần đã hoàn thành. Phần VII hạn 24/11 có bản viết ban đầu và còn cần cập nhật theo kết quả chung của nhóm.
