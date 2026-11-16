# Prompt bước S (Specify the question) – 20 chủ đề bài tập nhóm

Cách dùng: tính các ô [__] từ dữ liệu, thay vào, rồi sao chép toàn bộ khối prompt của chủ đề vào công cụ AI. Kiểm tra lại tên cột và từng phép tính AI đề xuất; lưu prompt và phản hồi vào nhật ký dùng AI.

## Template chung (dùng khi nhóm tự đề xuất chủ đề)

```text
VAI TRÒ CỦA AI
Bạn là chuyên gia phân tích kinh doanh, hỗ trợ tôi thực hiện bước S (Specify the question) của mô hình SOAR. Ở bước này chỉ giúp tôi đặt đúng câu hỏi: KHÔNG phân tích dữ liệu, KHÔNG đưa ra số liệu hay kết luận.

BỐI CẢNH
Tôi là [VAI TRÒ/CHỨC VỤ] tại [TÊN DOANH NGHIỆP/PHÒNG BAN – nếu là bối cảnh giả định, ghi rõ “giả định”].

LỚP 1) VẤN ĐỀ KINH DOANH – fact đã biết (rộng, có số liệu và mốc so sánh)
“[Mô tả hiện tượng/số liệu bất thường, có so sánh thời gian hoặc mốc chuẩn. VD: Doanh số giảm 15% so với tháng trước]”
Nguồn của fact: [tính từ dữ liệu (ghi phép tính) / báo cáo nội bộ / giả định].

QUYẾT ĐỊNH cần đưa ra sau phân tích
“[Ai quyết định điều gì, trước thời điểm nào]”
KPI đánh giá quyết định: [...].
Ràng buộc: [ngân sách, năng lực, thời gian, quy định...].

PHẠM VI phân tích
- Chỉ tập trung vào: [...].
- KHÔNG xét đến: [...].

DỮ LIỆU TÔI ĐANG CÓ
- Tên bộ dữ liệu/nguồn: [...].
- Đơn vị quan sát (mỗi dòng là gì): [...].
- Quy mô và khung thời gian: [...].
- Các cột dữ liệu (ghi đúng tên cột): [...].
- Hạn chế đã biết: [...].

════════════════════════════════════════
PHẦN A — MÔ HÌNH 4 LỚP CÂU HỎI (phễu thu hẹp: Vấn đề kinh doanh → Câu hỏi kinh doanh → Câu hỏi phân tích → Câu hỏi thống kê)
════════════════════════════════════════
Lớp 1 (Vấn đề kinh doanh) là fact đã nêu ở trên: rộng, mơ hồ, chưa phân tích trực tiếp được. Hãy thu hẹp dần qua các lớp 2–4 dưới đây.

LỚP 2) CÂU HỎI KINH DOANH (thu hẹp phạm vi) – đặt 5–7 câu, sắp xếp theo ưu tiên
- Là câu hỏi mở, ngôn ngữ quản lý, KHÔNG gắn số liệu cụ thể; chỉ nằm trong PHẠM VI.
- Mục đích: định hướng điều tra nguyên nhân của VẤN ĐỀ KINH DOANH và phục vụ QUYẾT ĐỊNH ở trên.
- Ưu tiên = mức ảnh hưởng tới QUYẾT ĐỊNH × khả năng trả lời bằng dữ liệu đang có.
- Ví dụ dạng: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”

LỚP 3) CÂU HỎI PHÂN TÍCH (gắn với dữ liệu) – tương ứng với mỗi câu hỏi kinh doanh
- Chuyển câu hỏi kinh doanh thành yêu cầu đo lường được.
- Phải gắn cụ thể: tên đơn vị/phạm vi, khoảng thời gian so sánh, chỉ số liên quan (kèm định nghĩa công thức).
- Ví dụ dạng: “[Chỉ số X] tại [đơn vị Y] đã thay đổi bao nhiêu % trong [kỳ A] so với [kỳ B]?”

LỚP 4) CÂU HỎI THỐNG KÊ (đo lường cụ thể) – tương ứng với mỗi câu hỏi phân tích
- Là câu hỏi trả lời trực tiếp được bằng một phép tính cụ thể trên dữ liệu, cho ra một con số với đơn vị đo rõ ràng.
- Ghi rõ: (i) các cột sử dụng, đúng tên; (ii) phép tính/kỹ thuật (tổng, trung bình, tỷ lệ, kiểm định, hồi quy, mô hình dự báo, tối ưu hóa, mô phỏng…); (iii) đơn vị đo của kết quả.
- Ví dụ dạng: “[Chỉ số cụ thể] trung bình/tổng tại [đơn vị Y]: [kỳ A] vs [kỳ B] là bao nhiêu [đơn vị đo]?”

MINH HỌA MỘT CHUỖI 4 LỚP
- Lớp 1 – Vấn đề kinh doanh: “Lợi nhuận quý này giảm 12% so với quý trước.”
- Lớp 2 – Câu hỏi kinh doanh: “Chi phí nào tăng nhanh nhất và ở khu vực nào?”
- Lớp 3 – Câu hỏi phân tích: “Chi phí nguyên liệu tại chi nhánh Đà Nẵng đã tăng bao nhiêu % trong Q3 so với Q2?”
- Lớp 4 – Câu hỏi thống kê: “Giá vốn hàng bán (COGS) trung bình/đơn hàng tại Đà Nẵng: Q2 vs Q3 là bao nhiêu VNĐ?”

PHÂN LOẠI LOẠI HÌNH CÂU HỎI (thuộc tính của mỗi chuỗi câu hỏi, không phải một lớp)
- Gắn mỗi câu hỏi kinh doanh (và chuỗi câu hỏi đi kèm) với một loại hình: Mô tả (điều gì đã xảy ra?) / Chẩn đoán (vì sao?) / Dự đoán (điều gì có thể xảy ra?) / Đề xuất (nên làm gì?).
- Khuyến khích bộ câu hỏi phủ đủ 4 loại hình nhưng không bắt buộc: nếu với QUYẾT ĐỊNH này một loại hình không cần thiết, bỏ qua và nêu lý do. Ít nhất một câu phải trả lời trực tiếp QUYẾT ĐỊNH.
- Ví dụ dạng câu hỏi kinh doanh theo loại hình:
    • Mô tả: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”
    • Chẩn đoán: “Vì sao [kết quả] ở [phạm vi nào] lại [tăng/giảm]?”
    • Dự đoán: “[Kết quả] sẽ diễn biến thế nào trong [kỳ tới] nếu [điều kiện] giữ nguyên?”
    • Đề xuất: “Nên [hành động nào] với [đối tượng nào] để đạt [mục tiêu] trong [ràng buộc]?”
- Ví dụ dạng câu hỏi thống kê theo loại hình (ngoài dạng Mô tả ở Lớp 4):
    • Chẩn đoán: “Chênh lệch trung bình [cột X] giữa [nhóm 1] và [nhóm 2] là bao nhiêu [đơn vị đo], p-value của kiểm định [t / chi-bình phương] là bao nhiêu?”
    • Dự đoán: “Mô hình [tên] dùng [các cột] dự báo [cột mục tiêu] cho [kỳ tới] có sai số [MAPE/RMSE/AUC] bao nhiêu trên tập kiểm tra [kỳ C]?”
    • Đề xuất: “Với [ràng buộc], giá trị tối ưu của [biến quyết định] là bao nhiêu và [KPI] tăng thêm bao nhiêu [đơn vị đo] so với hiện trạng?”

════════════════════════════════════════
PHẦN B — HAI YÊU CẦU BỔ SUNG
════════════════════════════════════════

BỔ SUNG 1) DỮ LIỆU CẦN THU THẬP THÊM – kiểm tra từng câu hỏi thống kê
- Nếu dữ liệu đang có đã đủ: ghi “Đủ dữ liệu hiện có”.
- Nếu chưa đủ, chỉ rõ: a. tên trường còn thiếu; b. nguồn có thể thu thập; c. mức ưu tiên (Cao/Trung bình/Thấp); d. nếu không thu thập được (dữ liệu công khai), đề xuất biến thay thế hoặc giả định có căn cứ và cách kiểm tra độ nhạy.
- Ví dụ: “Thiếu giá vốn theo sản phẩm – nguồn: phần mềm kế toán hoặc BCTC doanh nghiệp cùng ngành – ưu tiên Cao – nếu không có: giả định biên gộp theo danh mục, kiểm tra độ nhạy ±5 điểm %.”

BỔ SUNG 2) HÀNH ĐỘNG DỰ KIẾN – cho mỗi câu hỏi kinh doanh
- Viết dạng: “Nếu [chỉ số] [>/<] [ngưỡng] thì [hành động A]; ngược lại [hành động B]”. Nếu chưa biết ngưỡng, ghi ngưỡng là tham số cần xác định và cách xác định.
- Ví dụ: “Nếu tỷ lệ giao trễ ở vùng Y > 15% → mở kho vệ tinh tại Y; ngược lại → giữ mạng lưới hiện tại và điều chỉnh cam kết thời gian giao.”

════════════════════════════════════════
QUY TẮC CHO AI
════════════════════════════════════════
- Không bịa trường dữ liệu: chỉ dùng các cột đã liệt kê; mọi trường khác phải đưa vào cột “Dữ liệu cần thu thập thêm”.
- Không trả lời các câu hỏi, không đưa số liệu giả định như thể là kết quả.
- Nếu bối cảnh hoặc dữ liệu chưa đủ để đặt câu hỏi tốt, nêu điểm thiếu ở đầu câu trả lời, rồi vẫn lập bảng với giả định tạm thời được ghi rõ.

════════════════════════════════════════
YÊU CẦU TRÌNH BÀY
════════════════════════════════════════
- 1. Nhắc lại LỚP 1 (Vấn đề kinh doanh) ở đầu câu trả lời, sau đó lập bảng, mỗi dòng 6 cột: [Câu hỏi kinh doanh (đã sắp ưu tiên) | Câu hỏi phân tích | Câu hỏi thống kê | Loại hình câu hỏi | Dữ liệu cần thu thập thêm (nếu có) | Hành động dự kiến].
- 2. Dưới bảng: (a) CÂU HỎI QUYẾT ĐỊNH CHỐT, viết trong một câu; (b) tự kiểm tra: số câu theo từng loại hình, số câu thống kê “Đủ dữ liệu hiện có”, các câu phải dựa vào giả định; (c) đánh giá mức khả thi của đề tài với dữ liệu hiện có (Cao/Trung bình/Thấp) và lý do.
```

## Chủ đề 1: Thiết kế combo sản phẩm tăng giá trị đơn hàng

```text
VAI TRÒ CỦA AI
Bạn là chuyên gia phân tích kinh doanh, hỗ trợ tôi thực hiện bước S (Specify the question) của mô hình SOAR. Ở bước này chỉ giúp tôi đặt đúng câu hỏi: KHÔNG phân tích dữ liệu, KHÔNG đưa ra số liệu hay kết luận.

BỐI CẢNH
Tôi là Giám đốc ngành hàng tại một nhà bán lẻ quà tặng trực tuyến tại Anh (bối cảnh theo dữ liệu Online Retail II).

LỚP 1) VẤN ĐỀ KINH DOANH – fact đã biết (rộng, có số liệu và mốc so sánh)
“Giá trị đơn hàng trung bình (AOV) giai đoạn 12/2010–11/2011 là [__] GBP, gần như không đổi so với cùng kỳ năm trước ([__] GBP), trong khi [__]% đơn hàng chỉ có 1–3 mã hàng.”
Nguồn của fact: tính từ Quantity × Price, gộp theo Invoice, đã loại hóa đơn hủy.

QUYẾT ĐỊNH cần đưa ra sau phân tích
“Chọn 5 combo sản phẩm và mức giảm giá combo để triển khai trong quý tới.”
KPI đánh giá quyết định: AOV; lợi nhuận gộp/đơn; tỷ lệ đơn có combo.
Ràng buộc: tối đa 5 combo; mức giảm giá combo không quá 15%.

PHẠM VI phân tích
- Chỉ tập trung vào: đơn hàng hợp lệ của khách lẻ tại Vương quốc Anh.
- KHÔNG xét đến: khách bán sỉ, mã phí vận chuyển/bưu phí, thị trường ngoài Anh.

DỮ LIỆU TÔI ĐANG CÓ
- Tên bộ dữ liệu/nguồn: Online Retail II (UCI).
- Đơn vị quan sát (mỗi dòng là gì): một mã hàng trong một hóa đơn.
- Quy mô và khung thời gian: khoảng 1 triệu dòng, 12/2009–12/2011.
- Các cột dữ liệu (ghi đúng tên cột): Invoice, StockCode, Description, Quantity, InvoiceDate, Price, Customer ID, Country.
- Hạn chế đã biết: không có danh mục sản phẩm và giá vốn; hóa đơn hủy có mã bắt đầu bằng “C”.

════════════════════════════════════════
PHẦN A — MÔ HÌNH 4 LỚP CÂU HỎI (phễu thu hẹp: Vấn đề kinh doanh → Câu hỏi kinh doanh → Câu hỏi phân tích → Câu hỏi thống kê)
════════════════════════════════════════
Lớp 1 (Vấn đề kinh doanh) là fact đã nêu ở trên: rộng, mơ hồ, chưa phân tích trực tiếp được. Hãy thu hẹp dần qua các lớp 2–4 dưới đây.

LỚP 2) CÂU HỎI KINH DOANH (thu hẹp phạm vi) – đặt 5–7 câu, sắp xếp theo ưu tiên
- Là câu hỏi mở, ngôn ngữ quản lý, KHÔNG gắn số liệu cụ thể; chỉ nằm trong PHẠM VI.
- Mục đích: định hướng điều tra nguyên nhân của VẤN ĐỀ KINH DOANH và phục vụ QUYẾT ĐỊNH ở trên.
- Ưu tiên = mức ảnh hưởng tới QUYẾT ĐỊNH × khả năng trả lời bằng dữ liệu đang có.
- Ví dụ dạng: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”

LỚP 3) CÂU HỎI PHÂN TÍCH (gắn với dữ liệu) – tương ứng với mỗi câu hỏi kinh doanh
- Chuyển câu hỏi kinh doanh thành yêu cầu đo lường được.
- Phải gắn cụ thể: tên đơn vị/phạm vi, khoảng thời gian so sánh, chỉ số liên quan (kèm định nghĩa công thức).
- Ví dụ dạng: “[Chỉ số X] tại [đơn vị Y] đã thay đổi bao nhiêu % trong [kỳ A] so với [kỳ B]?”

LỚP 4) CÂU HỎI THỐNG KÊ (đo lường cụ thể) – tương ứng với mỗi câu hỏi phân tích
- Là câu hỏi trả lời trực tiếp được bằng một phép tính cụ thể trên dữ liệu, cho ra một con số với đơn vị đo rõ ràng.
- Ghi rõ: (i) các cột sử dụng, đúng tên; (ii) phép tính/kỹ thuật (tổng, trung bình, tỷ lệ, kiểm định, hồi quy, mô hình dự báo, tối ưu hóa, mô phỏng…); (iii) đơn vị đo của kết quả.
- Ví dụ dạng: “[Chỉ số cụ thể] trung bình/tổng tại [đơn vị Y]: [kỳ A] vs [kỳ B] là bao nhiêu [đơn vị đo]?”

MINH HỌA MỘT CHUỖI 4 LỚP
- Lớp 1 – Vấn đề kinh doanh: “Lợi nhuận quý này giảm 12% so với quý trước.”
- Lớp 2 – Câu hỏi kinh doanh: “Chi phí nào tăng nhanh nhất và ở khu vực nào?”
- Lớp 3 – Câu hỏi phân tích: “Chi phí nguyên liệu tại chi nhánh Đà Nẵng đã tăng bao nhiêu % trong Q3 so với Q2?”
- Lớp 4 – Câu hỏi thống kê: “Giá vốn hàng bán (COGS) trung bình/đơn hàng tại Đà Nẵng: Q2 vs Q3 là bao nhiêu VNĐ?”

PHÂN LOẠI LOẠI HÌNH CÂU HỎI (thuộc tính của mỗi chuỗi câu hỏi, không phải một lớp)
- Gắn mỗi câu hỏi kinh doanh (và chuỗi câu hỏi đi kèm) với một loại hình: Mô tả (điều gì đã xảy ra?) / Chẩn đoán (vì sao?) / Dự đoán (điều gì có thể xảy ra?) / Đề xuất (nên làm gì?).
- Khuyến khích bộ câu hỏi phủ đủ 4 loại hình nhưng không bắt buộc: nếu với QUYẾT ĐỊNH này một loại hình không cần thiết, bỏ qua và nêu lý do. Ít nhất một câu phải trả lời trực tiếp QUYẾT ĐỊNH.
- Ví dụ dạng câu hỏi kinh doanh theo loại hình:
    • Mô tả: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”
    • Chẩn đoán: “Vì sao [kết quả] ở [phạm vi nào] lại [tăng/giảm]?”
    • Dự đoán: “[Kết quả] sẽ diễn biến thế nào trong [kỳ tới] nếu [điều kiện] giữ nguyên?”
    • Đề xuất: “Nên [hành động nào] với [đối tượng nào] để đạt [mục tiêu] trong [ràng buộc]?”
- Ví dụ dạng câu hỏi thống kê theo loại hình (ngoài dạng Mô tả ở Lớp 4):
    • Chẩn đoán: “Chênh lệch trung bình [cột X] giữa [nhóm 1] và [nhóm 2] là bao nhiêu [đơn vị đo], p-value của kiểm định [t / chi-bình phương] là bao nhiêu?”
    • Dự đoán: “Mô hình [tên] dùng [các cột] dự báo [cột mục tiêu] cho [kỳ tới] có sai số [MAPE/RMSE/AUC] bao nhiêu trên tập kiểm tra [kỳ C]?”
    • Đề xuất: “Với [ràng buộc], giá trị tối ưu của [biến quyết định] là bao nhiêu và [KPI] tăng thêm bao nhiêu [đơn vị đo] so với hiện trạng?”

════════════════════════════════════════
PHẦN B — HAI YÊU CẦU BỔ SUNG
════════════════════════════════════════

BỔ SUNG 1) DỮ LIỆU CẦN THU THẬP THÊM – kiểm tra từng câu hỏi thống kê
- Nếu dữ liệu đang có đã đủ: ghi “Đủ dữ liệu hiện có”.
- Nếu chưa đủ, chỉ rõ: a. tên trường còn thiếu; b. nguồn có thể thu thập; c. mức ưu tiên (Cao/Trung bình/Thấp); d. nếu không thu thập được (dữ liệu công khai), đề xuất biến thay thế hoặc giả định có căn cứ và cách kiểm tra độ nhạy.
- Ví dụ: “Thiếu giá vốn theo sản phẩm – nguồn: phần mềm kế toán hoặc BCTC doanh nghiệp cùng ngành – ưu tiên Cao – nếu không có: giả định biên gộp theo danh mục, kiểm tra độ nhạy ±5 điểm %.”

BỔ SUNG 2) HÀNH ĐỘNG DỰ KIẾN – cho mỗi câu hỏi kinh doanh
- Viết dạng: “Nếu [chỉ số] [>/<] [ngưỡng] thì [hành động A]; ngược lại [hành động B]”. Nếu chưa biết ngưỡng, ghi ngưỡng là tham số cần xác định và cách xác định.
- Ví dụ: “Nếu tỷ lệ giao trễ ở vùng Y > 15% → mở kho vệ tinh tại Y; ngược lại → giữ mạng lưới hiện tại và điều chỉnh cam kết thời gian giao.”

════════════════════════════════════════
QUY TẮC CHO AI
════════════════════════════════════════
- Không bịa trường dữ liệu: chỉ dùng các cột đã liệt kê; mọi trường khác phải đưa vào cột “Dữ liệu cần thu thập thêm”.
- Không trả lời các câu hỏi, không đưa số liệu giả định như thể là kết quả.
- Nếu bối cảnh hoặc dữ liệu chưa đủ để đặt câu hỏi tốt, nêu điểm thiếu ở đầu câu trả lời, rồi vẫn lập bảng với giả định tạm thời được ghi rõ.

════════════════════════════════════════
YÊU CẦU TRÌNH BÀY
════════════════════════════════════════
- 1. Nhắc lại LỚP 1 (Vấn đề kinh doanh) ở đầu câu trả lời, sau đó lập bảng, mỗi dòng 6 cột: [Câu hỏi kinh doanh (đã sắp ưu tiên) | Câu hỏi phân tích | Câu hỏi thống kê | Loại hình câu hỏi | Dữ liệu cần thu thập thêm (nếu có) | Hành động dự kiến].
- 2. Dưới bảng: (a) CÂU HỎI QUYẾT ĐỊNH CHỐT, viết trong một câu; (b) tự kiểm tra: số câu theo từng loại hình, số câu thống kê “Đủ dữ liệu hiện có”, các câu phải dựa vào giả định; (c) đánh giá mức khả thi của đề tài với dữ liệu hiện có (Cao/Trung bình/Thấp) và lý do.
```

## Chủ đề 2: Định giá tối ưu dựa trên độ co giãn của cầu

```text
VAI TRÒ CỦA AI
Bạn là chuyên gia phân tích kinh doanh, hỗ trợ tôi thực hiện bước S (Specify the question) của mô hình SOAR. Ở bước này chỉ giúp tôi đặt đúng câu hỏi: KHÔNG phân tích dữ liệu, KHÔNG đưa ra số liệu hay kết luận.

BỐI CẢNH
Tôi là Trưởng bộ phận định giá tại một chuỗi siêu thị (bối cảnh theo dữ liệu dunnhumby “Breakfast at the Frat”).

LỚP 1) VẤN ĐỀ KINH DOANH – fact đã biết (rộng, có số liệu và mốc so sánh)
“Trong 52 tuần gần nhất, [__]% sản lượng nhóm ngũ cốc được bán trong tuần có giảm giá tạm thời, nhưng doanh thu nhóm chỉ tăng [__]% so với 52 tuần trước đó.”
Nguồn của fact: tính từ UNITS, SPEND, TPR_ONLY theo WEEK_END_DATE.

QUYẾT ĐỊNH cần đưa ra sau phân tích
“Điều chỉnh giá cơ sở và tần suất giảm giá cho 4 nhóm hàng trong chu kỳ giá tới.”
KPI đánh giá quyết định: lợi nhuận gộp; sản lượng; độ co giãn giá.
Ràng buộc: mỗi lần đổi giá không quá ±10%.

PHẠM VI phân tích
- Chỉ tập trung vào: 4 nhóm hàng và các cửa hàng có trong dữ liệu.
- KHÔNG xét đến: nhóm hàng khác, ngân sách quảng cáo.

DỮ LIỆU TÔI ĐANG CÓ
- Tên bộ dữ liệu/nguồn: dunnhumby – Breakfast at the Frat.
- Đơn vị quan sát (mỗi dòng là gì): cửa hàng – sản phẩm (UPC) – tuần.
- Quy mô và khung thời gian: 156 tuần.
- Các cột dữ liệu (ghi đúng tên cột): bảng giao dịch: WEEK_END_DATE, STORE_NUM, UPC, UNITS, VISITS, HHS, SPEND, PRICE, BASE_PRICE, FEATURE, DISPLAY, TPR_ONLY; bảng sản phẩm: UPC, CATEGORY, SUB_CATEGORY, MANUFACTURER, PRODUCT_SIZE; bảng cửa hàng.
- Hạn chế đã biết: không có giá vốn, không có giá đối thủ.

════════════════════════════════════════
PHẦN A — MÔ HÌNH 4 LỚP CÂU HỎI (phễu thu hẹp: Vấn đề kinh doanh → Câu hỏi kinh doanh → Câu hỏi phân tích → Câu hỏi thống kê)
════════════════════════════════════════
Lớp 1 (Vấn đề kinh doanh) là fact đã nêu ở trên: rộng, mơ hồ, chưa phân tích trực tiếp được. Hãy thu hẹp dần qua các lớp 2–4 dưới đây.

LỚP 2) CÂU HỎI KINH DOANH (thu hẹp phạm vi) – đặt 5–7 câu, sắp xếp theo ưu tiên
- Là câu hỏi mở, ngôn ngữ quản lý, KHÔNG gắn số liệu cụ thể; chỉ nằm trong PHẠM VI.
- Mục đích: định hướng điều tra nguyên nhân của VẤN ĐỀ KINH DOANH và phục vụ QUYẾT ĐỊNH ở trên.
- Ưu tiên = mức ảnh hưởng tới QUYẾT ĐỊNH × khả năng trả lời bằng dữ liệu đang có.
- Ví dụ dạng: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”

LỚP 3) CÂU HỎI PHÂN TÍCH (gắn với dữ liệu) – tương ứng với mỗi câu hỏi kinh doanh
- Chuyển câu hỏi kinh doanh thành yêu cầu đo lường được.
- Phải gắn cụ thể: tên đơn vị/phạm vi, khoảng thời gian so sánh, chỉ số liên quan (kèm định nghĩa công thức).
- Ví dụ dạng: “[Chỉ số X] tại [đơn vị Y] đã thay đổi bao nhiêu % trong [kỳ A] so với [kỳ B]?”

LỚP 4) CÂU HỎI THỐNG KÊ (đo lường cụ thể) – tương ứng với mỗi câu hỏi phân tích
- Là câu hỏi trả lời trực tiếp được bằng một phép tính cụ thể trên dữ liệu, cho ra một con số với đơn vị đo rõ ràng.
- Ghi rõ: (i) các cột sử dụng, đúng tên; (ii) phép tính/kỹ thuật (tổng, trung bình, tỷ lệ, kiểm định, hồi quy, mô hình dự báo, tối ưu hóa, mô phỏng…); (iii) đơn vị đo của kết quả.
- Ví dụ dạng: “[Chỉ số cụ thể] trung bình/tổng tại [đơn vị Y]: [kỳ A] vs [kỳ B] là bao nhiêu [đơn vị đo]?”

MINH HỌA MỘT CHUỖI 4 LỚP
- Lớp 1 – Vấn đề kinh doanh: “Lợi nhuận quý này giảm 12% so với quý trước.”
- Lớp 2 – Câu hỏi kinh doanh: “Chi phí nào tăng nhanh nhất và ở khu vực nào?”
- Lớp 3 – Câu hỏi phân tích: “Chi phí nguyên liệu tại chi nhánh Đà Nẵng đã tăng bao nhiêu % trong Q3 so với Q2?”
- Lớp 4 – Câu hỏi thống kê: “Giá vốn hàng bán (COGS) trung bình/đơn hàng tại Đà Nẵng: Q2 vs Q3 là bao nhiêu VNĐ?”

PHÂN LOẠI LOẠI HÌNH CÂU HỎI (thuộc tính của mỗi chuỗi câu hỏi, không phải một lớp)
- Gắn mỗi câu hỏi kinh doanh (và chuỗi câu hỏi đi kèm) với một loại hình: Mô tả (điều gì đã xảy ra?) / Chẩn đoán (vì sao?) / Dự đoán (điều gì có thể xảy ra?) / Đề xuất (nên làm gì?).
- Khuyến khích bộ câu hỏi phủ đủ 4 loại hình nhưng không bắt buộc: nếu với QUYẾT ĐỊNH này một loại hình không cần thiết, bỏ qua và nêu lý do. Ít nhất một câu phải trả lời trực tiếp QUYẾT ĐỊNH.
- Ví dụ dạng câu hỏi kinh doanh theo loại hình:
    • Mô tả: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”
    • Chẩn đoán: “Vì sao [kết quả] ở [phạm vi nào] lại [tăng/giảm]?”
    • Dự đoán: “[Kết quả] sẽ diễn biến thế nào trong [kỳ tới] nếu [điều kiện] giữ nguyên?”
    • Đề xuất: “Nên [hành động nào] với [đối tượng nào] để đạt [mục tiêu] trong [ràng buộc]?”
- Ví dụ dạng câu hỏi thống kê theo loại hình (ngoài dạng Mô tả ở Lớp 4):
    • Chẩn đoán: “Chênh lệch trung bình [cột X] giữa [nhóm 1] và [nhóm 2] là bao nhiêu [đơn vị đo], p-value của kiểm định [t / chi-bình phương] là bao nhiêu?”
    • Dự đoán: “Mô hình [tên] dùng [các cột] dự báo [cột mục tiêu] cho [kỳ tới] có sai số [MAPE/RMSE/AUC] bao nhiêu trên tập kiểm tra [kỳ C]?”
    • Đề xuất: “Với [ràng buộc], giá trị tối ưu của [biến quyết định] là bao nhiêu và [KPI] tăng thêm bao nhiêu [đơn vị đo] so với hiện trạng?”

════════════════════════════════════════
PHẦN B — HAI YÊU CẦU BỔ SUNG
════════════════════════════════════════

BỔ SUNG 1) DỮ LIỆU CẦN THU THẬP THÊM – kiểm tra từng câu hỏi thống kê
- Nếu dữ liệu đang có đã đủ: ghi “Đủ dữ liệu hiện có”.
- Nếu chưa đủ, chỉ rõ: a. tên trường còn thiếu; b. nguồn có thể thu thập; c. mức ưu tiên (Cao/Trung bình/Thấp); d. nếu không thu thập được (dữ liệu công khai), đề xuất biến thay thế hoặc giả định có căn cứ và cách kiểm tra độ nhạy.
- Ví dụ: “Thiếu giá vốn theo sản phẩm – nguồn: phần mềm kế toán hoặc BCTC doanh nghiệp cùng ngành – ưu tiên Cao – nếu không có: giả định biên gộp theo danh mục, kiểm tra độ nhạy ±5 điểm %.”

BỔ SUNG 2) HÀNH ĐỘNG DỰ KIẾN – cho mỗi câu hỏi kinh doanh
- Viết dạng: “Nếu [chỉ số] [>/<] [ngưỡng] thì [hành động A]; ngược lại [hành động B]”. Nếu chưa biết ngưỡng, ghi ngưỡng là tham số cần xác định và cách xác định.
- Ví dụ: “Nếu tỷ lệ giao trễ ở vùng Y > 15% → mở kho vệ tinh tại Y; ngược lại → giữ mạng lưới hiện tại và điều chỉnh cam kết thời gian giao.”

════════════════════════════════════════
QUY TẮC CHO AI
════════════════════════════════════════
- Không bịa trường dữ liệu: chỉ dùng các cột đã liệt kê; mọi trường khác phải đưa vào cột “Dữ liệu cần thu thập thêm”.
- Không trả lời các câu hỏi, không đưa số liệu giả định như thể là kết quả.
- Nếu bối cảnh hoặc dữ liệu chưa đủ để đặt câu hỏi tốt, nêu điểm thiếu ở đầu câu trả lời, rồi vẫn lập bảng với giả định tạm thời được ghi rõ.

════════════════════════════════════════
YÊU CẦU TRÌNH BÀY
════════════════════════════════════════
- 1. Nhắc lại LỚP 1 (Vấn đề kinh doanh) ở đầu câu trả lời, sau đó lập bảng, mỗi dòng 6 cột: [Câu hỏi kinh doanh (đã sắp ưu tiên) | Câu hỏi phân tích | Câu hỏi thống kê | Loại hình câu hỏi | Dữ liệu cần thu thập thêm (nếu có) | Hành động dự kiến].
- 2. Dưới bảng: (a) CÂU HỎI QUYẾT ĐỊNH CHỐT, viết trong một câu; (b) tự kiểm tra: số câu theo từng loại hình, số câu thống kê “Đủ dữ liệu hiện có”, các câu phải dựa vào giả định; (c) đánh giá mức khả thi của đề tài với dữ liệu hiện có (Cao/Trung bình/Thấp) và lý do.
```

## Chủ đề 3: Chiến lược phân phối theo vùng và trải nghiệm giao hàng

```text
VAI TRÒ CỦA AI
Bạn là chuyên gia phân tích kinh doanh, hỗ trợ tôi thực hiện bước S (Specify the question) của mô hình SOAR. Ở bước này chỉ giúp tôi đặt đúng câu hỏi: KHÔNG phân tích dữ liệu, KHÔNG đưa ra số liệu hay kết luận.

BỐI CẢNH
Tôi là Giám đốc vận hành thương mại điện tử tại một sàn thương mại điện tử (bối cảnh theo dữ liệu Olist, Brazil).

LỚP 1) VẤN ĐỀ KINH DOANH – fact đã biết (rộng, có số liệu và mốc so sánh)
“Tỷ lệ đơn giao trễ so với ngày hẹn là [__]% ở các bang miền Bắc/Đông Bắc, so với [__]% ở São Paulo; điểm đánh giá trung bình của đơn trễ là [__] so với [__] của đơn đúng hẹn.”
Nguồn của fact: so sánh order_delivered_customer_date với order_estimated_delivery_date; review_score theo customer_state.

QUYẾT ĐỊNH cần đưa ra sau phân tích
“Chọn 1–2 bang đặt kho vệ tinh trong năm tới.”
KPI đánh giá quyết định: tỷ lệ giao trễ; thời gian giao; điểm đánh giá.
Ràng buộc: ngân sách cho tối đa 2 kho.

PHẠM VI phân tích
- Chỉ tập trung vào: đơn đã giao (order_status = delivered).
- KHÔNG xét đến: đơn hủy, thanh toán, hoạt động marketing.

DỮ LIỆU TÔI ĐANG CÓ
- Tên bộ dữ liệu/nguồn: Brazilian E-Commerce Public Dataset by Olist.
- Đơn vị quan sát (mỗi dòng là gì): nhiều bảng: đơn hàng, dòng hàng, đánh giá, khách, người bán, geolocation.
- Quy mô và khung thời gian: khoảng 100 nghìn đơn, 2016–2018.
- Các cột dữ liệu (ghi đúng tên cột): order_id, order_status, order_purchase_timestamp, order_delivered_customer_date, order_estimated_delivery_date, review_score, customer_state, customer_zip_code_prefix, seller_state, seller_zip_code_prefix, price, freight_value, geolocation_lat, geolocation_lng.
- Hạn chế đã biết: không có tồn kho và hãng vận chuyển; dữ liệu của Brazil.

════════════════════════════════════════
PHẦN A — MÔ HÌNH 4 LỚP CÂU HỎI (phễu thu hẹp: Vấn đề kinh doanh → Câu hỏi kinh doanh → Câu hỏi phân tích → Câu hỏi thống kê)
════════════════════════════════════════
Lớp 1 (Vấn đề kinh doanh) là fact đã nêu ở trên: rộng, mơ hồ, chưa phân tích trực tiếp được. Hãy thu hẹp dần qua các lớp 2–4 dưới đây.

LỚP 2) CÂU HỎI KINH DOANH (thu hẹp phạm vi) – đặt 5–7 câu, sắp xếp theo ưu tiên
- Là câu hỏi mở, ngôn ngữ quản lý, KHÔNG gắn số liệu cụ thể; chỉ nằm trong PHẠM VI.
- Mục đích: định hướng điều tra nguyên nhân của VẤN ĐỀ KINH DOANH và phục vụ QUYẾT ĐỊNH ở trên.
- Ưu tiên = mức ảnh hưởng tới QUYẾT ĐỊNH × khả năng trả lời bằng dữ liệu đang có.
- Ví dụ dạng: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”

LỚP 3) CÂU HỎI PHÂN TÍCH (gắn với dữ liệu) – tương ứng với mỗi câu hỏi kinh doanh
- Chuyển câu hỏi kinh doanh thành yêu cầu đo lường được.
- Phải gắn cụ thể: tên đơn vị/phạm vi, khoảng thời gian so sánh, chỉ số liên quan (kèm định nghĩa công thức).
- Ví dụ dạng: “[Chỉ số X] tại [đơn vị Y] đã thay đổi bao nhiêu % trong [kỳ A] so với [kỳ B]?”

LỚP 4) CÂU HỎI THỐNG KÊ (đo lường cụ thể) – tương ứng với mỗi câu hỏi phân tích
- Là câu hỏi trả lời trực tiếp được bằng một phép tính cụ thể trên dữ liệu, cho ra một con số với đơn vị đo rõ ràng.
- Ghi rõ: (i) các cột sử dụng, đúng tên; (ii) phép tính/kỹ thuật (tổng, trung bình, tỷ lệ, kiểm định, hồi quy, mô hình dự báo, tối ưu hóa, mô phỏng…); (iii) đơn vị đo của kết quả.
- Ví dụ dạng: “[Chỉ số cụ thể] trung bình/tổng tại [đơn vị Y]: [kỳ A] vs [kỳ B] là bao nhiêu [đơn vị đo]?”

MINH HỌA MỘT CHUỖI 4 LỚP
- Lớp 1 – Vấn đề kinh doanh: “Lợi nhuận quý này giảm 12% so với quý trước.”
- Lớp 2 – Câu hỏi kinh doanh: “Chi phí nào tăng nhanh nhất và ở khu vực nào?”
- Lớp 3 – Câu hỏi phân tích: “Chi phí nguyên liệu tại chi nhánh Đà Nẵng đã tăng bao nhiêu % trong Q3 so với Q2?”
- Lớp 4 – Câu hỏi thống kê: “Giá vốn hàng bán (COGS) trung bình/đơn hàng tại Đà Nẵng: Q2 vs Q3 là bao nhiêu VNĐ?”

PHÂN LOẠI LOẠI HÌNH CÂU HỎI (thuộc tính của mỗi chuỗi câu hỏi, không phải một lớp)
- Gắn mỗi câu hỏi kinh doanh (và chuỗi câu hỏi đi kèm) với một loại hình: Mô tả (điều gì đã xảy ra?) / Chẩn đoán (vì sao?) / Dự đoán (điều gì có thể xảy ra?) / Đề xuất (nên làm gì?).
- Khuyến khích bộ câu hỏi phủ đủ 4 loại hình nhưng không bắt buộc: nếu với QUYẾT ĐỊNH này một loại hình không cần thiết, bỏ qua và nêu lý do. Ít nhất một câu phải trả lời trực tiếp QUYẾT ĐỊNH.
- Ví dụ dạng câu hỏi kinh doanh theo loại hình:
    • Mô tả: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”
    • Chẩn đoán: “Vì sao [kết quả] ở [phạm vi nào] lại [tăng/giảm]?”
    • Dự đoán: “[Kết quả] sẽ diễn biến thế nào trong [kỳ tới] nếu [điều kiện] giữ nguyên?”
    • Đề xuất: “Nên [hành động nào] với [đối tượng nào] để đạt [mục tiêu] trong [ràng buộc]?”
- Ví dụ dạng câu hỏi thống kê theo loại hình (ngoài dạng Mô tả ở Lớp 4):
    • Chẩn đoán: “Chênh lệch trung bình [cột X] giữa [nhóm 1] và [nhóm 2] là bao nhiêu [đơn vị đo], p-value của kiểm định [t / chi-bình phương] là bao nhiêu?”
    • Dự đoán: “Mô hình [tên] dùng [các cột] dự báo [cột mục tiêu] cho [kỳ tới] có sai số [MAPE/RMSE/AUC] bao nhiêu trên tập kiểm tra [kỳ C]?”
    • Đề xuất: “Với [ràng buộc], giá trị tối ưu của [biến quyết định] là bao nhiêu và [KPI] tăng thêm bao nhiêu [đơn vị đo] so với hiện trạng?”

════════════════════════════════════════
PHẦN B — HAI YÊU CẦU BỔ SUNG
════════════════════════════════════════

BỔ SUNG 1) DỮ LIỆU CẦN THU THẬP THÊM – kiểm tra từng câu hỏi thống kê
- Nếu dữ liệu đang có đã đủ: ghi “Đủ dữ liệu hiện có”.
- Nếu chưa đủ, chỉ rõ: a. tên trường còn thiếu; b. nguồn có thể thu thập; c. mức ưu tiên (Cao/Trung bình/Thấp); d. nếu không thu thập được (dữ liệu công khai), đề xuất biến thay thế hoặc giả định có căn cứ và cách kiểm tra độ nhạy.
- Ví dụ: “Thiếu giá vốn theo sản phẩm – nguồn: phần mềm kế toán hoặc BCTC doanh nghiệp cùng ngành – ưu tiên Cao – nếu không có: giả định biên gộp theo danh mục, kiểm tra độ nhạy ±5 điểm %.”

BỔ SUNG 2) HÀNH ĐỘNG DỰ KIẾN – cho mỗi câu hỏi kinh doanh
- Viết dạng: “Nếu [chỉ số] [>/<] [ngưỡng] thì [hành động A]; ngược lại [hành động B]”. Nếu chưa biết ngưỡng, ghi ngưỡng là tham số cần xác định và cách xác định.
- Ví dụ: “Nếu tỷ lệ giao trễ ở vùng Y > 15% → mở kho vệ tinh tại Y; ngược lại → giữ mạng lưới hiện tại và điều chỉnh cam kết thời gian giao.”

════════════════════════════════════════
QUY TẮC CHO AI
════════════════════════════════════════
- Không bịa trường dữ liệu: chỉ dùng các cột đã liệt kê; mọi trường khác phải đưa vào cột “Dữ liệu cần thu thập thêm”.
- Không trả lời các câu hỏi, không đưa số liệu giả định như thể là kết quả.
- Nếu bối cảnh hoặc dữ liệu chưa đủ để đặt câu hỏi tốt, nêu điểm thiếu ở đầu câu trả lời, rồi vẫn lập bảng với giả định tạm thời được ghi rõ.

════════════════════════════════════════
YÊU CẦU TRÌNH BÀY
════════════════════════════════════════
- 1. Nhắc lại LỚP 1 (Vấn đề kinh doanh) ở đầu câu trả lời, sau đó lập bảng, mỗi dòng 6 cột: [Câu hỏi kinh doanh (đã sắp ưu tiên) | Câu hỏi phân tích | Câu hỏi thống kê | Loại hình câu hỏi | Dữ liệu cần thu thập thêm (nếu có) | Hành động dự kiến].
- 2. Dưới bảng: (a) CÂU HỎI QUYẾT ĐỊNH CHỐT, viết trong một câu; (b) tự kiểm tra: số câu theo từng loại hình, số câu thống kê “Đủ dữ liệu hiện có”, các câu phải dựa vào giả định; (c) đánh giá mức khả thi của đề tài với dữ liệu hiện có (Cao/Trung bình/Thấp) và lý do.
```

## Chủ đề 4: Dự báo khách hàng rời bỏ và phân bổ ngân sách giữ chân

```text
VAI TRÒ CỦA AI
Bạn là chuyên gia phân tích kinh doanh, hỗ trợ tôi thực hiện bước S (Specify the question) của mô hình SOAR. Ở bước này chỉ giúp tôi đặt đúng câu hỏi: KHÔNG phân tích dữ liệu, KHÔNG đưa ra số liệu hay kết luận.

BỐI CẢNH
Tôi là Giám đốc Chăm sóc khách hàng (CRM) tại một nhà mạng viễn thông (bối cảnh theo dữ liệu Telco Customer Churn).

LỚP 1) VẤN ĐỀ KINH DOANH – fact đã biết (rộng, có số liệu và mốc so sánh)
“Tỷ lệ khách rời bỏ là [__]%; riêng nhóm hợp đồng theo tháng là [__]%, cao gấp [__] lần nhóm hợp đồng 2 năm.”
Nguồn của fact: tỷ lệ Churn = “Yes” theo Contract.

QUYẾT ĐỊNH cần đưa ra sau phân tích
“Phân bổ ngân sách giữ chân B đồng/tháng cho chiến dịch quý tới.”
KPI đánh giá quyết định: tỷ lệ rời bỏ; doanh thu được giữ lại; ROI chiến dịch.
Ràng buộc: ngân sách B; mỗi khách tối đa một ưu đãi.

PHẠM VI phân tích
- Chỉ tập trung vào: khách hàng cá nhân hiện có.
- KHÔNG xét đến: phát triển khách mới, thiết kế lại gói cước.

DỮ LIỆU TÔI ĐANG CÓ
- Tên bộ dữ liệu/nguồn: Telco Customer Churn (IBM).
- Đơn vị quan sát (mỗi dòng là gì): một khách hàng tại một thời điểm.
- Quy mô và khung thời gian: 7.043 khách hàng.
- Các cột dữ liệu (ghi đúng tên cột): customerID, gender, SeniorCitizen, Partner, Dependents, tenure, PhoneService, MultipleLines, InternetService, OnlineSecurity, TechSupport, StreamingTV, Contract, PaperlessBilling, PaymentMethod, MonthlyCharges, TotalCharges, Churn.
- Hạn chế đã biết: ảnh chụp một thời điểm, không có ngày rời bỏ; không có chi phí và biên lợi nhuận.

════════════════════════════════════════
PHẦN A — MÔ HÌNH 4 LỚP CÂU HỎI (phễu thu hẹp: Vấn đề kinh doanh → Câu hỏi kinh doanh → Câu hỏi phân tích → Câu hỏi thống kê)
════════════════════════════════════════
Lớp 1 (Vấn đề kinh doanh) là fact đã nêu ở trên: rộng, mơ hồ, chưa phân tích trực tiếp được. Hãy thu hẹp dần qua các lớp 2–4 dưới đây.

LỚP 2) CÂU HỎI KINH DOANH (thu hẹp phạm vi) – đặt 5–7 câu, sắp xếp theo ưu tiên
- Là câu hỏi mở, ngôn ngữ quản lý, KHÔNG gắn số liệu cụ thể; chỉ nằm trong PHẠM VI.
- Mục đích: định hướng điều tra nguyên nhân của VẤN ĐỀ KINH DOANH và phục vụ QUYẾT ĐỊNH ở trên.
- Ưu tiên = mức ảnh hưởng tới QUYẾT ĐỊNH × khả năng trả lời bằng dữ liệu đang có.
- Ví dụ dạng: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”

LỚP 3) CÂU HỎI PHÂN TÍCH (gắn với dữ liệu) – tương ứng với mỗi câu hỏi kinh doanh
- Chuyển câu hỏi kinh doanh thành yêu cầu đo lường được.
- Phải gắn cụ thể: tên đơn vị/phạm vi, khoảng thời gian so sánh, chỉ số liên quan (kèm định nghĩa công thức).
- Ví dụ dạng: “[Chỉ số X] tại [đơn vị Y] đã thay đổi bao nhiêu % trong [kỳ A] so với [kỳ B]?”

LỚP 4) CÂU HỎI THỐNG KÊ (đo lường cụ thể) – tương ứng với mỗi câu hỏi phân tích
- Là câu hỏi trả lời trực tiếp được bằng một phép tính cụ thể trên dữ liệu, cho ra một con số với đơn vị đo rõ ràng.
- Ghi rõ: (i) các cột sử dụng, đúng tên; (ii) phép tính/kỹ thuật (tổng, trung bình, tỷ lệ, kiểm định, hồi quy, mô hình dự báo, tối ưu hóa, mô phỏng…); (iii) đơn vị đo của kết quả.
- Ví dụ dạng: “[Chỉ số cụ thể] trung bình/tổng tại [đơn vị Y]: [kỳ A] vs [kỳ B] là bao nhiêu [đơn vị đo]?”

MINH HỌA MỘT CHUỖI 4 LỚP
- Lớp 1 – Vấn đề kinh doanh: “Lợi nhuận quý này giảm 12% so với quý trước.”
- Lớp 2 – Câu hỏi kinh doanh: “Chi phí nào tăng nhanh nhất và ở khu vực nào?”
- Lớp 3 – Câu hỏi phân tích: “Chi phí nguyên liệu tại chi nhánh Đà Nẵng đã tăng bao nhiêu % trong Q3 so với Q2?”
- Lớp 4 – Câu hỏi thống kê: “Giá vốn hàng bán (COGS) trung bình/đơn hàng tại Đà Nẵng: Q2 vs Q3 là bao nhiêu VNĐ?”

PHÂN LOẠI LOẠI HÌNH CÂU HỎI (thuộc tính của mỗi chuỗi câu hỏi, không phải một lớp)
- Gắn mỗi câu hỏi kinh doanh (và chuỗi câu hỏi đi kèm) với một loại hình: Mô tả (điều gì đã xảy ra?) / Chẩn đoán (vì sao?) / Dự đoán (điều gì có thể xảy ra?) / Đề xuất (nên làm gì?).
- Khuyến khích bộ câu hỏi phủ đủ 4 loại hình nhưng không bắt buộc: nếu với QUYẾT ĐỊNH này một loại hình không cần thiết, bỏ qua và nêu lý do. Ít nhất một câu phải trả lời trực tiếp QUYẾT ĐỊNH.
- Ví dụ dạng câu hỏi kinh doanh theo loại hình:
    • Mô tả: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”
    • Chẩn đoán: “Vì sao [kết quả] ở [phạm vi nào] lại [tăng/giảm]?”
    • Dự đoán: “[Kết quả] sẽ diễn biến thế nào trong [kỳ tới] nếu [điều kiện] giữ nguyên?”
    • Đề xuất: “Nên [hành động nào] với [đối tượng nào] để đạt [mục tiêu] trong [ràng buộc]?”
- Ví dụ dạng câu hỏi thống kê theo loại hình (ngoài dạng Mô tả ở Lớp 4):
    • Chẩn đoán: “Chênh lệch trung bình [cột X] giữa [nhóm 1] và [nhóm 2] là bao nhiêu [đơn vị đo], p-value của kiểm định [t / chi-bình phương] là bao nhiêu?”
    • Dự đoán: “Mô hình [tên] dùng [các cột] dự báo [cột mục tiêu] cho [kỳ tới] có sai số [MAPE/RMSE/AUC] bao nhiêu trên tập kiểm tra [kỳ C]?”
    • Đề xuất: “Với [ràng buộc], giá trị tối ưu của [biến quyết định] là bao nhiêu và [KPI] tăng thêm bao nhiêu [đơn vị đo] so với hiện trạng?”

════════════════════════════════════════
PHẦN B — HAI YÊU CẦU BỔ SUNG
════════════════════════════════════════

BỔ SUNG 1) DỮ LIỆU CẦN THU THẬP THÊM – kiểm tra từng câu hỏi thống kê
- Nếu dữ liệu đang có đã đủ: ghi “Đủ dữ liệu hiện có”.
- Nếu chưa đủ, chỉ rõ: a. tên trường còn thiếu; b. nguồn có thể thu thập; c. mức ưu tiên (Cao/Trung bình/Thấp); d. nếu không thu thập được (dữ liệu công khai), đề xuất biến thay thế hoặc giả định có căn cứ và cách kiểm tra độ nhạy.
- Ví dụ: “Thiếu giá vốn theo sản phẩm – nguồn: phần mềm kế toán hoặc BCTC doanh nghiệp cùng ngành – ưu tiên Cao – nếu không có: giả định biên gộp theo danh mục, kiểm tra độ nhạy ±5 điểm %.”

BỔ SUNG 2) HÀNH ĐỘNG DỰ KIẾN – cho mỗi câu hỏi kinh doanh
- Viết dạng: “Nếu [chỉ số] [>/<] [ngưỡng] thì [hành động A]; ngược lại [hành động B]”. Nếu chưa biết ngưỡng, ghi ngưỡng là tham số cần xác định và cách xác định.
- Ví dụ: “Nếu tỷ lệ giao trễ ở vùng Y > 15% → mở kho vệ tinh tại Y; ngược lại → giữ mạng lưới hiện tại và điều chỉnh cam kết thời gian giao.”

════════════════════════════════════════
QUY TẮC CHO AI
════════════════════════════════════════
- Không bịa trường dữ liệu: chỉ dùng các cột đã liệt kê; mọi trường khác phải đưa vào cột “Dữ liệu cần thu thập thêm”.
- Không trả lời các câu hỏi, không đưa số liệu giả định như thể là kết quả.
- Nếu bối cảnh hoặc dữ liệu chưa đủ để đặt câu hỏi tốt, nêu điểm thiếu ở đầu câu trả lời, rồi vẫn lập bảng với giả định tạm thời được ghi rõ.

════════════════════════════════════════
YÊU CẦU TRÌNH BÀY
════════════════════════════════════════
- 1. Nhắc lại LỚP 1 (Vấn đề kinh doanh) ở đầu câu trả lời, sau đó lập bảng, mỗi dòng 6 cột: [Câu hỏi kinh doanh (đã sắp ưu tiên) | Câu hỏi phân tích | Câu hỏi thống kê | Loại hình câu hỏi | Dữ liệu cần thu thập thêm (nếu có) | Hành động dự kiến].
- 2. Dưới bảng: (a) CÂU HỎI QUYẾT ĐỊNH CHỐT, viết trong một câu; (b) tự kiểm tra: số câu theo từng loại hình, số câu thống kê “Đủ dữ liệu hiện có”, các câu phải dựa vào giả định; (c) đánh giá mức khả thi của đề tài với dữ liệu hiện có (Cao/Trung bình/Thấp) và lý do.
```

## Chủ đề 5: Quản trị doanh thu khách sạn: kênh bán, hủy phòng và overbooking

```text
VAI TRÒ CỦA AI
Bạn là chuyên gia phân tích kinh doanh, hỗ trợ tôi thực hiện bước S (Specify the question) của mô hình SOAR. Ở bước này chỉ giúp tôi đặt đúng câu hỏi: KHÔNG phân tích dữ liệu, KHÔNG đưa ra số liệu hay kết luận.

BỐI CẢNH
Tôi là Giám đốc Doanh thu (Revenue Manager) tại một khách sạn thành phố (bối cảnh theo dữ liệu Hotel Booking Demand, City Hotel).

LỚP 1) VẤN ĐỀ KINH DOANH – fact đã biết (rộng, có số liệu và mốc so sánh)
“Tỷ lệ hủy của đặt phòng qua kênh TA/TO là [__]%, so với [__]% của kênh Direct; kênh TA/TO chiếm [__]% số đêm phòng.”
Nguồn của fact: is_canceled và số đêm theo distribution_channel.

QUYẾT ĐỊNH cần đưa ra sau phân tích
“Quyết định số phòng giữ cho kênh trực tiếp, mức overbooking và chính sách đặt cọc cho mùa cao điểm tới.”
KPI đánh giá quyết định: RevPAR; lợi nhuận ròng/phòng-đêm; tỷ lệ hủy.
Ràng buộc: công suất cố định; chi phí chuyển khách khi overbooking.

PHẠM VI phân tích
- Chỉ tập trung vào: City Hotel.
- KHÔNG xét đến: Resort Hotel, dịch vụ ăn uống.

DỮ LIỆU TÔI ĐANG CÓ
- Tên bộ dữ liệu/nguồn: Hotel Booking Demand (Antonio, Almeida & Nunes, 2019).
- Đơn vị quan sát (mỗi dòng là gì): một lượt đặt phòng.
- Quy mô và khung thời gian: 119.390 lượt, 7/2015–8/2017.
- Các cột dữ liệu (ghi đúng tên cột): hotel, is_canceled, lead_time, arrival_date_year, arrival_date_month, arrival_date_day_of_month, stays_in_weekend_nights, stays_in_week_nights, adults, market_segment, distribution_channel, is_repeated_guest, previous_cancellations, deposit_type, customer_type, adr.
- Hạn chế đã biết: không có công suất và hoa hồng; reservation_status là kết quả, không dùng để dự báo hủy.

════════════════════════════════════════
PHẦN A — MÔ HÌNH 4 LỚP CÂU HỎI (phễu thu hẹp: Vấn đề kinh doanh → Câu hỏi kinh doanh → Câu hỏi phân tích → Câu hỏi thống kê)
════════════════════════════════════════
Lớp 1 (Vấn đề kinh doanh) là fact đã nêu ở trên: rộng, mơ hồ, chưa phân tích trực tiếp được. Hãy thu hẹp dần qua các lớp 2–4 dưới đây.

LỚP 2) CÂU HỎI KINH DOANH (thu hẹp phạm vi) – đặt 5–7 câu, sắp xếp theo ưu tiên
- Là câu hỏi mở, ngôn ngữ quản lý, KHÔNG gắn số liệu cụ thể; chỉ nằm trong PHẠM VI.
- Mục đích: định hướng điều tra nguyên nhân của VẤN ĐỀ KINH DOANH và phục vụ QUYẾT ĐỊNH ở trên.
- Ưu tiên = mức ảnh hưởng tới QUYẾT ĐỊNH × khả năng trả lời bằng dữ liệu đang có.
- Ví dụ dạng: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”

LỚP 3) CÂU HỎI PHÂN TÍCH (gắn với dữ liệu) – tương ứng với mỗi câu hỏi kinh doanh
- Chuyển câu hỏi kinh doanh thành yêu cầu đo lường được.
- Phải gắn cụ thể: tên đơn vị/phạm vi, khoảng thời gian so sánh, chỉ số liên quan (kèm định nghĩa công thức).
- Ví dụ dạng: “[Chỉ số X] tại [đơn vị Y] đã thay đổi bao nhiêu % trong [kỳ A] so với [kỳ B]?”

LỚP 4) CÂU HỎI THỐNG KÊ (đo lường cụ thể) – tương ứng với mỗi câu hỏi phân tích
- Là câu hỏi trả lời trực tiếp được bằng một phép tính cụ thể trên dữ liệu, cho ra một con số với đơn vị đo rõ ràng.
- Ghi rõ: (i) các cột sử dụng, đúng tên; (ii) phép tính/kỹ thuật (tổng, trung bình, tỷ lệ, kiểm định, hồi quy, mô hình dự báo, tối ưu hóa, mô phỏng…); (iii) đơn vị đo của kết quả.
- Ví dụ dạng: “[Chỉ số cụ thể] trung bình/tổng tại [đơn vị Y]: [kỳ A] vs [kỳ B] là bao nhiêu [đơn vị đo]?”

MINH HỌA MỘT CHUỖI 4 LỚP
- Lớp 1 – Vấn đề kinh doanh: “Lợi nhuận quý này giảm 12% so với quý trước.”
- Lớp 2 – Câu hỏi kinh doanh: “Chi phí nào tăng nhanh nhất và ở khu vực nào?”
- Lớp 3 – Câu hỏi phân tích: “Chi phí nguyên liệu tại chi nhánh Đà Nẵng đã tăng bao nhiêu % trong Q3 so với Q2?”
- Lớp 4 – Câu hỏi thống kê: “Giá vốn hàng bán (COGS) trung bình/đơn hàng tại Đà Nẵng: Q2 vs Q3 là bao nhiêu VNĐ?”

PHÂN LOẠI LOẠI HÌNH CÂU HỎI (thuộc tính của mỗi chuỗi câu hỏi, không phải một lớp)
- Gắn mỗi câu hỏi kinh doanh (và chuỗi câu hỏi đi kèm) với một loại hình: Mô tả (điều gì đã xảy ra?) / Chẩn đoán (vì sao?) / Dự đoán (điều gì có thể xảy ra?) / Đề xuất (nên làm gì?).
- Khuyến khích bộ câu hỏi phủ đủ 4 loại hình nhưng không bắt buộc: nếu với QUYẾT ĐỊNH này một loại hình không cần thiết, bỏ qua và nêu lý do. Ít nhất một câu phải trả lời trực tiếp QUYẾT ĐỊNH.
- Ví dụ dạng câu hỏi kinh doanh theo loại hình:
    • Mô tả: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”
    • Chẩn đoán: “Vì sao [kết quả] ở [phạm vi nào] lại [tăng/giảm]?”
    • Dự đoán: “[Kết quả] sẽ diễn biến thế nào trong [kỳ tới] nếu [điều kiện] giữ nguyên?”
    • Đề xuất: “Nên [hành động nào] với [đối tượng nào] để đạt [mục tiêu] trong [ràng buộc]?”
- Ví dụ dạng câu hỏi thống kê theo loại hình (ngoài dạng Mô tả ở Lớp 4):
    • Chẩn đoán: “Chênh lệch trung bình [cột X] giữa [nhóm 1] và [nhóm 2] là bao nhiêu [đơn vị đo], p-value của kiểm định [t / chi-bình phương] là bao nhiêu?”
    • Dự đoán: “Mô hình [tên] dùng [các cột] dự báo [cột mục tiêu] cho [kỳ tới] có sai số [MAPE/RMSE/AUC] bao nhiêu trên tập kiểm tra [kỳ C]?”
    • Đề xuất: “Với [ràng buộc], giá trị tối ưu của [biến quyết định] là bao nhiêu và [KPI] tăng thêm bao nhiêu [đơn vị đo] so với hiện trạng?”

════════════════════════════════════════
PHẦN B — HAI YÊU CẦU BỔ SUNG
════════════════════════════════════════

BỔ SUNG 1) DỮ LIỆU CẦN THU THẬP THÊM – kiểm tra từng câu hỏi thống kê
- Nếu dữ liệu đang có đã đủ: ghi “Đủ dữ liệu hiện có”.
- Nếu chưa đủ, chỉ rõ: a. tên trường còn thiếu; b. nguồn có thể thu thập; c. mức ưu tiên (Cao/Trung bình/Thấp); d. nếu không thu thập được (dữ liệu công khai), đề xuất biến thay thế hoặc giả định có căn cứ và cách kiểm tra độ nhạy.
- Ví dụ: “Thiếu giá vốn theo sản phẩm – nguồn: phần mềm kế toán hoặc BCTC doanh nghiệp cùng ngành – ưu tiên Cao – nếu không có: giả định biên gộp theo danh mục, kiểm tra độ nhạy ±5 điểm %.”

BỔ SUNG 2) HÀNH ĐỘNG DỰ KIẾN – cho mỗi câu hỏi kinh doanh
- Viết dạng: “Nếu [chỉ số] [>/<] [ngưỡng] thì [hành động A]; ngược lại [hành động B]”. Nếu chưa biết ngưỡng, ghi ngưỡng là tham số cần xác định và cách xác định.
- Ví dụ: “Nếu tỷ lệ giao trễ ở vùng Y > 15% → mở kho vệ tinh tại Y; ngược lại → giữ mạng lưới hiện tại và điều chỉnh cam kết thời gian giao.”

════════════════════════════════════════
QUY TẮC CHO AI
════════════════════════════════════════
- Không bịa trường dữ liệu: chỉ dùng các cột đã liệt kê; mọi trường khác phải đưa vào cột “Dữ liệu cần thu thập thêm”.
- Không trả lời các câu hỏi, không đưa số liệu giả định như thể là kết quả.
- Nếu bối cảnh hoặc dữ liệu chưa đủ để đặt câu hỏi tốt, nêu điểm thiếu ở đầu câu trả lời, rồi vẫn lập bảng với giả định tạm thời được ghi rõ.

════════════════════════════════════════
YÊU CẦU TRÌNH BÀY
════════════════════════════════════════
- 1. Nhắc lại LỚP 1 (Vấn đề kinh doanh) ở đầu câu trả lời, sau đó lập bảng, mỗi dòng 6 cột: [Câu hỏi kinh doanh (đã sắp ưu tiên) | Câu hỏi phân tích | Câu hỏi thống kê | Loại hình câu hỏi | Dữ liệu cần thu thập thêm (nếu có) | Hành động dự kiến].
- 2. Dưới bảng: (a) CÂU HỎI QUYẾT ĐỊNH CHỐT, viết trong một câu; (b) tự kiểm tra: số câu theo từng loại hình, số câu thống kê “Đủ dữ liệu hiện có”, các câu phải dựa vào giả định; (c) đánh giá mức khả thi của đề tài với dữ liệu hiện có (Cao/Trung bình/Thấp) và lý do.
```

## Chủ đề 6: Sức khỏe tài chính và cảnh báo sớm kiệt quệ tài chính

```text
VAI TRÒ CỦA AI
Bạn là chuyên gia phân tích kinh doanh, hỗ trợ tôi thực hiện bước S (Specify the question) của mô hình SOAR. Ở bước này chỉ giúp tôi đặt đúng câu hỏi: KHÔNG phân tích dữ liệu, KHÔNG đưa ra số liệu hay kết luận.

BỐI CẢNH
Tôi là Chuyên viên thẩm định tín dụng doanh nghiệp tại một ngân hàng thương mại (bối cảnh giả định).

LỚP 1) VẤN ĐỀ KINH DOANH – fact đã biết (rộng, có số liệu và mốc so sánh)
“Trong mẫu doanh nghiệp niêm yết ngành [__] giai đoạn [__]–[__], có [__] doanh nghiệp lỗ 3 năm liên tiếp hoặc âm vốn chủ; doanh nghiệp X có ROE giảm từ [__]% xuống [__]% dù doanh thu tăng [__]%.”
Nguồn của fact: báo cáo tài chính năm tải bằng vnstock/CafeF.

QUYẾT ĐỊNH cần đưa ra sau phân tích
“Có cấp hạn mức tín dụng cho doanh nghiệp X không và với điều kiện gì.”
KPI đánh giá quyết định: xác suất kiệt quệ tài chính 2 năm; tổn thất kỳ vọng.
Ràng buộc: khẩu vị rủi ro của ngân hàng.

PHẠM VI phân tích
- Chỉ tập trung vào: doanh nghiệp niêm yết ngành [__] trên HOSE/HNX.
- KHÔNG xét đến: ngân hàng, bảo hiểm, chứng khoán (cấu trúc BCTC khác).

DỮ LIỆU TÔI ĐANG CÓ
- Tên bộ dữ liệu/nguồn: Báo cáo tài chính doanh nghiệp niêm yết Việt Nam.
- Đơn vị quan sát (mỗi dòng là gì): doanh nghiệp – năm.
- Quy mô và khung thời gian: [__] doanh nghiệp, [__] năm.
- Các cột dữ liệu (ghi đúng tên cột): doanh thu thuần, giá vốn, lợi nhuận gộp, chi phí bán hàng, chi phí QLDN, chi phí lãi vay, LN trước thuế, LN sau thuế, tổng tài sản, tài sản ngắn hạn, nợ ngắn hạn, tổng nợ, vốn chủ sở hữu, LN sau thuế chưa phân phối, khấu hao, lưu chuyển tiền từ HĐKD, tiền chi mua sắm TSCĐ, vốn hóa thị trường.
- Hạn chế đã biết: phá sản chính thức rất hiếm, phải dùng định nghĩa kiệt quệ thay thế; chuẩn mực kế toán có thay đổi giữa các năm.

════════════════════════════════════════
PHẦN A — MÔ HÌNH 4 LỚP CÂU HỎI (phễu thu hẹp: Vấn đề kinh doanh → Câu hỏi kinh doanh → Câu hỏi phân tích → Câu hỏi thống kê)
════════════════════════════════════════
Lớp 1 (Vấn đề kinh doanh) là fact đã nêu ở trên: rộng, mơ hồ, chưa phân tích trực tiếp được. Hãy thu hẹp dần qua các lớp 2–4 dưới đây.

LỚP 2) CÂU HỎI KINH DOANH (thu hẹp phạm vi) – đặt 5–7 câu, sắp xếp theo ưu tiên
- Là câu hỏi mở, ngôn ngữ quản lý, KHÔNG gắn số liệu cụ thể; chỉ nằm trong PHẠM VI.
- Mục đích: định hướng điều tra nguyên nhân của VẤN ĐỀ KINH DOANH và phục vụ QUYẾT ĐỊNH ở trên.
- Ưu tiên = mức ảnh hưởng tới QUYẾT ĐỊNH × khả năng trả lời bằng dữ liệu đang có.
- Ví dụ dạng: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”

LỚP 3) CÂU HỎI PHÂN TÍCH (gắn với dữ liệu) – tương ứng với mỗi câu hỏi kinh doanh
- Chuyển câu hỏi kinh doanh thành yêu cầu đo lường được.
- Phải gắn cụ thể: tên đơn vị/phạm vi, khoảng thời gian so sánh, chỉ số liên quan (kèm định nghĩa công thức).
- Ví dụ dạng: “[Chỉ số X] tại [đơn vị Y] đã thay đổi bao nhiêu % trong [kỳ A] so với [kỳ B]?”

LỚP 4) CÂU HỎI THỐNG KÊ (đo lường cụ thể) – tương ứng với mỗi câu hỏi phân tích
- Là câu hỏi trả lời trực tiếp được bằng một phép tính cụ thể trên dữ liệu, cho ra một con số với đơn vị đo rõ ràng.
- Ghi rõ: (i) các cột sử dụng, đúng tên; (ii) phép tính/kỹ thuật (tổng, trung bình, tỷ lệ, kiểm định, hồi quy, mô hình dự báo, tối ưu hóa, mô phỏng…); (iii) đơn vị đo của kết quả.
- Ví dụ dạng: “[Chỉ số cụ thể] trung bình/tổng tại [đơn vị Y]: [kỳ A] vs [kỳ B] là bao nhiêu [đơn vị đo]?”

MINH HỌA MỘT CHUỖI 4 LỚP
- Lớp 1 – Vấn đề kinh doanh: “Lợi nhuận quý này giảm 12% so với quý trước.”
- Lớp 2 – Câu hỏi kinh doanh: “Chi phí nào tăng nhanh nhất và ở khu vực nào?”
- Lớp 3 – Câu hỏi phân tích: “Chi phí nguyên liệu tại chi nhánh Đà Nẵng đã tăng bao nhiêu % trong Q3 so với Q2?”
- Lớp 4 – Câu hỏi thống kê: “Giá vốn hàng bán (COGS) trung bình/đơn hàng tại Đà Nẵng: Q2 vs Q3 là bao nhiêu VNĐ?”

PHÂN LOẠI LOẠI HÌNH CÂU HỎI (thuộc tính của mỗi chuỗi câu hỏi, không phải một lớp)
- Gắn mỗi câu hỏi kinh doanh (và chuỗi câu hỏi đi kèm) với một loại hình: Mô tả (điều gì đã xảy ra?) / Chẩn đoán (vì sao?) / Dự đoán (điều gì có thể xảy ra?) / Đề xuất (nên làm gì?).
- Khuyến khích bộ câu hỏi phủ đủ 4 loại hình nhưng không bắt buộc: nếu với QUYẾT ĐỊNH này một loại hình không cần thiết, bỏ qua và nêu lý do. Ít nhất một câu phải trả lời trực tiếp QUYẾT ĐỊNH.
- Ví dụ dạng câu hỏi kinh doanh theo loại hình:
    • Mô tả: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”
    • Chẩn đoán: “Vì sao [kết quả] ở [phạm vi nào] lại [tăng/giảm]?”
    • Dự đoán: “[Kết quả] sẽ diễn biến thế nào trong [kỳ tới] nếu [điều kiện] giữ nguyên?”
    • Đề xuất: “Nên [hành động nào] với [đối tượng nào] để đạt [mục tiêu] trong [ràng buộc]?”
- Ví dụ dạng câu hỏi thống kê theo loại hình (ngoài dạng Mô tả ở Lớp 4):
    • Chẩn đoán: “Chênh lệch trung bình [cột X] giữa [nhóm 1] và [nhóm 2] là bao nhiêu [đơn vị đo], p-value của kiểm định [t / chi-bình phương] là bao nhiêu?”
    • Dự đoán: “Mô hình [tên] dùng [các cột] dự báo [cột mục tiêu] cho [kỳ tới] có sai số [MAPE/RMSE/AUC] bao nhiêu trên tập kiểm tra [kỳ C]?”
    • Đề xuất: “Với [ràng buộc], giá trị tối ưu của [biến quyết định] là bao nhiêu và [KPI] tăng thêm bao nhiêu [đơn vị đo] so với hiện trạng?”

════════════════════════════════════════
PHẦN B — HAI YÊU CẦU BỔ SUNG
════════════════════════════════════════

BỔ SUNG 1) DỮ LIỆU CẦN THU THẬP THÊM – kiểm tra từng câu hỏi thống kê
- Nếu dữ liệu đang có đã đủ: ghi “Đủ dữ liệu hiện có”.
- Nếu chưa đủ, chỉ rõ: a. tên trường còn thiếu; b. nguồn có thể thu thập; c. mức ưu tiên (Cao/Trung bình/Thấp); d. nếu không thu thập được (dữ liệu công khai), đề xuất biến thay thế hoặc giả định có căn cứ và cách kiểm tra độ nhạy.
- Ví dụ: “Thiếu giá vốn theo sản phẩm – nguồn: phần mềm kế toán hoặc BCTC doanh nghiệp cùng ngành – ưu tiên Cao – nếu không có: giả định biên gộp theo danh mục, kiểm tra độ nhạy ±5 điểm %.”

BỔ SUNG 2) HÀNH ĐỘNG DỰ KIẾN – cho mỗi câu hỏi kinh doanh
- Viết dạng: “Nếu [chỉ số] [>/<] [ngưỡng] thì [hành động A]; ngược lại [hành động B]”. Nếu chưa biết ngưỡng, ghi ngưỡng là tham số cần xác định và cách xác định.
- Ví dụ: “Nếu tỷ lệ giao trễ ở vùng Y > 15% → mở kho vệ tinh tại Y; ngược lại → giữ mạng lưới hiện tại và điều chỉnh cam kết thời gian giao.”

════════════════════════════════════════
QUY TẮC CHO AI
════════════════════════════════════════
- Không bịa trường dữ liệu: chỉ dùng các cột đã liệt kê; mọi trường khác phải đưa vào cột “Dữ liệu cần thu thập thêm”.
- Không trả lời các câu hỏi, không đưa số liệu giả định như thể là kết quả.
- Nếu bối cảnh hoặc dữ liệu chưa đủ để đặt câu hỏi tốt, nêu điểm thiếu ở đầu câu trả lời, rồi vẫn lập bảng với giả định tạm thời được ghi rõ.

════════════════════════════════════════
YÊU CẦU TRÌNH BÀY
════════════════════════════════════════
- 1. Nhắc lại LỚP 1 (Vấn đề kinh doanh) ở đầu câu trả lời, sau đó lập bảng, mỗi dòng 6 cột: [Câu hỏi kinh doanh (đã sắp ưu tiên) | Câu hỏi phân tích | Câu hỏi thống kê | Loại hình câu hỏi | Dữ liệu cần thu thập thêm (nếu có) | Hành động dự kiến].
- 2. Dưới bảng: (a) CÂU HỎI QUYẾT ĐỊNH CHỐT, viết trong một câu; (b) tự kiểm tra: số câu theo từng loại hình, số câu thống kê “Đủ dữ liệu hiện có”, các câu phải dựa vào giả định; (c) đánh giá mức khả thi của đề tài với dữ liệu hiện có (Cao/Trung bình/Thấp) và lý do.
```

## Chủ đề 7: Lợi nhuận thực theo khách hàng: chi phí phục vụ và ABC

```text
VAI TRÒ CỦA AI
Bạn là chuyên gia phân tích kinh doanh, hỗ trợ tôi thực hiện bước S (Specify the question) của mô hình SOAR. Ở bước này chỉ giúp tôi đặt đúng câu hỏi: KHÔNG phân tích dữ liệu, KHÔNG đưa ra số liệu hay kết luận.

BỐI CẢNH
Tôi là Kế toán trưởng quản trị tại một nhà bán lẻ trực tuyến (bối cảnh theo dữ liệu Online Retail II).

LỚP 1) VẤN ĐỀ KINH DOANH – fact đã biết (rộng, có số liệu và mốc so sánh)
“[__]% khách hàng có giá trị đơn trung bình dưới [__] GBP và tỷ lệ hóa đơn trả hàng là [__]%, trong khi chính sách hiện tại không thu phí xử lý hay phí trả hàng.”
Nguồn của fact: gộp theo Customer ID; hóa đơn trả hàng có mã “C”.

QUYẾT ĐỊNH cần đưa ra sau phân tích
“Ban hành chính sách đơn tối thiểu, phí giao hàng và phí trả hàng cho năm tài chính tới.”
KPI đánh giá quyết định: lợi nhuận ròng theo khách; chi phí phục vụ.
Ràng buộc: doanh thu không giảm quá [__]%.

PHẠM VI phân tích
- Chỉ tập trung vào: khách có Customer ID, năm 2010–2011.
- KHÔNG xét đến: khách không có mã, thay đổi giá bán.

DỮ LIỆU TÔI ĐANG CÓ
- Tên bộ dữ liệu/nguồn: Online Retail II (UCI).
- Đơn vị quan sát (mỗi dòng là gì): một mã hàng trong một hóa đơn.
- Quy mô và khung thời gian: khoảng 1 triệu dòng, 12/2009–12/2011.
- Các cột dữ liệu (ghi đúng tên cột): Invoice, StockCode, Description, Quantity, InvoiceDate, Price, Customer ID, Country.
- Hạn chế đã biết: không có dữ liệu chi phí; đơn giá hoạt động phải giả định có căn cứ.

════════════════════════════════════════
PHẦN A — MÔ HÌNH 4 LỚP CÂU HỎI (phễu thu hẹp: Vấn đề kinh doanh → Câu hỏi kinh doanh → Câu hỏi phân tích → Câu hỏi thống kê)
════════════════════════════════════════
Lớp 1 (Vấn đề kinh doanh) là fact đã nêu ở trên: rộng, mơ hồ, chưa phân tích trực tiếp được. Hãy thu hẹp dần qua các lớp 2–4 dưới đây.

LỚP 2) CÂU HỎI KINH DOANH (thu hẹp phạm vi) – đặt 5–7 câu, sắp xếp theo ưu tiên
- Là câu hỏi mở, ngôn ngữ quản lý, KHÔNG gắn số liệu cụ thể; chỉ nằm trong PHẠM VI.
- Mục đích: định hướng điều tra nguyên nhân của VẤN ĐỀ KINH DOANH và phục vụ QUYẾT ĐỊNH ở trên.
- Ưu tiên = mức ảnh hưởng tới QUYẾT ĐỊNH × khả năng trả lời bằng dữ liệu đang có.
- Ví dụ dạng: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”

LỚP 3) CÂU HỎI PHÂN TÍCH (gắn với dữ liệu) – tương ứng với mỗi câu hỏi kinh doanh
- Chuyển câu hỏi kinh doanh thành yêu cầu đo lường được.
- Phải gắn cụ thể: tên đơn vị/phạm vi, khoảng thời gian so sánh, chỉ số liên quan (kèm định nghĩa công thức).
- Ví dụ dạng: “[Chỉ số X] tại [đơn vị Y] đã thay đổi bao nhiêu % trong [kỳ A] so với [kỳ B]?”

LỚP 4) CÂU HỎI THỐNG KÊ (đo lường cụ thể) – tương ứng với mỗi câu hỏi phân tích
- Là câu hỏi trả lời trực tiếp được bằng một phép tính cụ thể trên dữ liệu, cho ra một con số với đơn vị đo rõ ràng.
- Ghi rõ: (i) các cột sử dụng, đúng tên; (ii) phép tính/kỹ thuật (tổng, trung bình, tỷ lệ, kiểm định, hồi quy, mô hình dự báo, tối ưu hóa, mô phỏng…); (iii) đơn vị đo của kết quả.
- Ví dụ dạng: “[Chỉ số cụ thể] trung bình/tổng tại [đơn vị Y]: [kỳ A] vs [kỳ B] là bao nhiêu [đơn vị đo]?”

MINH HỌA MỘT CHUỖI 4 LỚP
- Lớp 1 – Vấn đề kinh doanh: “Lợi nhuận quý này giảm 12% so với quý trước.”
- Lớp 2 – Câu hỏi kinh doanh: “Chi phí nào tăng nhanh nhất và ở khu vực nào?”
- Lớp 3 – Câu hỏi phân tích: “Chi phí nguyên liệu tại chi nhánh Đà Nẵng đã tăng bao nhiêu % trong Q3 so với Q2?”
- Lớp 4 – Câu hỏi thống kê: “Giá vốn hàng bán (COGS) trung bình/đơn hàng tại Đà Nẵng: Q2 vs Q3 là bao nhiêu VNĐ?”

PHÂN LOẠI LOẠI HÌNH CÂU HỎI (thuộc tính của mỗi chuỗi câu hỏi, không phải một lớp)
- Gắn mỗi câu hỏi kinh doanh (và chuỗi câu hỏi đi kèm) với một loại hình: Mô tả (điều gì đã xảy ra?) / Chẩn đoán (vì sao?) / Dự đoán (điều gì có thể xảy ra?) / Đề xuất (nên làm gì?).
- Khuyến khích bộ câu hỏi phủ đủ 4 loại hình nhưng không bắt buộc: nếu với QUYẾT ĐỊNH này một loại hình không cần thiết, bỏ qua và nêu lý do. Ít nhất một câu phải trả lời trực tiếp QUYẾT ĐỊNH.
- Ví dụ dạng câu hỏi kinh doanh theo loại hình:
    • Mô tả: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”
    • Chẩn đoán: “Vì sao [kết quả] ở [phạm vi nào] lại [tăng/giảm]?”
    • Dự đoán: “[Kết quả] sẽ diễn biến thế nào trong [kỳ tới] nếu [điều kiện] giữ nguyên?”
    • Đề xuất: “Nên [hành động nào] với [đối tượng nào] để đạt [mục tiêu] trong [ràng buộc]?”
- Ví dụ dạng câu hỏi thống kê theo loại hình (ngoài dạng Mô tả ở Lớp 4):
    • Chẩn đoán: “Chênh lệch trung bình [cột X] giữa [nhóm 1] và [nhóm 2] là bao nhiêu [đơn vị đo], p-value của kiểm định [t / chi-bình phương] là bao nhiêu?”
    • Dự đoán: “Mô hình [tên] dùng [các cột] dự báo [cột mục tiêu] cho [kỳ tới] có sai số [MAPE/RMSE/AUC] bao nhiêu trên tập kiểm tra [kỳ C]?”
    • Đề xuất: “Với [ràng buộc], giá trị tối ưu của [biến quyết định] là bao nhiêu và [KPI] tăng thêm bao nhiêu [đơn vị đo] so với hiện trạng?”

════════════════════════════════════════
PHẦN B — HAI YÊU CẦU BỔ SUNG
════════════════════════════════════════

BỔ SUNG 1) DỮ LIỆU CẦN THU THẬP THÊM – kiểm tra từng câu hỏi thống kê
- Nếu dữ liệu đang có đã đủ: ghi “Đủ dữ liệu hiện có”.
- Nếu chưa đủ, chỉ rõ: a. tên trường còn thiếu; b. nguồn có thể thu thập; c. mức ưu tiên (Cao/Trung bình/Thấp); d. nếu không thu thập được (dữ liệu công khai), đề xuất biến thay thế hoặc giả định có căn cứ và cách kiểm tra độ nhạy.
- Ví dụ: “Thiếu giá vốn theo sản phẩm – nguồn: phần mềm kế toán hoặc BCTC doanh nghiệp cùng ngành – ưu tiên Cao – nếu không có: giả định biên gộp theo danh mục, kiểm tra độ nhạy ±5 điểm %.”

BỔ SUNG 2) HÀNH ĐỘNG DỰ KIẾN – cho mỗi câu hỏi kinh doanh
- Viết dạng: “Nếu [chỉ số] [>/<] [ngưỡng] thì [hành động A]; ngược lại [hành động B]”. Nếu chưa biết ngưỡng, ghi ngưỡng là tham số cần xác định và cách xác định.
- Ví dụ: “Nếu tỷ lệ giao trễ ở vùng Y > 15% → mở kho vệ tinh tại Y; ngược lại → giữ mạng lưới hiện tại và điều chỉnh cam kết thời gian giao.”

════════════════════════════════════════
QUY TẮC CHO AI
════════════════════════════════════════
- Không bịa trường dữ liệu: chỉ dùng các cột đã liệt kê; mọi trường khác phải đưa vào cột “Dữ liệu cần thu thập thêm”.
- Không trả lời các câu hỏi, không đưa số liệu giả định như thể là kết quả.
- Nếu bối cảnh hoặc dữ liệu chưa đủ để đặt câu hỏi tốt, nêu điểm thiếu ở đầu câu trả lời, rồi vẫn lập bảng với giả định tạm thời được ghi rõ.

════════════════════════════════════════
YÊU CẦU TRÌNH BÀY
════════════════════════════════════════
- 1. Nhắc lại LỚP 1 (Vấn đề kinh doanh) ở đầu câu trả lời, sau đó lập bảng, mỗi dòng 6 cột: [Câu hỏi kinh doanh (đã sắp ưu tiên) | Câu hỏi phân tích | Câu hỏi thống kê | Loại hình câu hỏi | Dữ liệu cần thu thập thêm (nếu có) | Hành động dự kiến].
- 2. Dưới bảng: (a) CÂU HỎI QUYẾT ĐỊNH CHỐT, viết trong một câu; (b) tự kiểm tra: số câu theo từng loại hình, số câu thống kê “Đủ dữ liệu hiện có”, các câu phải dựa vào giả định; (c) đánh giá mức khả thi của đề tài với dữ liệu hiện có (Cao/Trung bình/Thấp) và lý do.
```

## Chủ đề 8: Kiểm toán dựa trên dữ liệu: phát hiện giao dịch bất thường

```text
VAI TRÒ CỦA AI
Bạn là chuyên gia phân tích kinh doanh, hỗ trợ tôi thực hiện bước S (Specify the question) của mô hình SOAR. Ở bước này chỉ giúp tôi đặt đúng câu hỏi: KHÔNG phân tích dữ liệu, KHÔNG đưa ra số liệu hay kết luận.

BỐI CẢNH
Tôi là Trưởng Kiểm toán nội bộ tại cơ quan quản lý ngân sách cấp bang (bối cảnh theo dữ liệu Oklahoma Purchase Card).

LỚP 1) VẤN ĐỀ KINH DOANH – fact đã biết (rộng, có số liệu và mốc so sánh)
“Có [__] giao dịch thẻ mua sắm công trong năm tài chính, tổng [__] USD; [__]% giao dịch phát sinh vào cuối tuần và có [__] cặp giao dịch trùng nhà cung cấp – số tiền – ngày.”
Nguồn của fact: thống kê trên toàn bộ tệp dữ liệu.

QUYẾT ĐỊNH cần đưa ra sau phân tích
“Chọn 50 giao dịch kiểm tra chi tiết mỗi tháng và đề xuất thủ tục kiểm soát.”
KPI đánh giá quyết định: tỷ lệ phát hiện trên mẫu; giá trị rủi ro được bao phủ.
Ràng buộc: năng lực kiểm tra 50 giao dịch/tháng.

PHẠM VI phân tích
- Chỉ tập trung vào: toàn bộ cơ quan trong năm tài chính của dữ liệu.
- KHÔNG xét đến: đánh giá hiệu quả chi tiêu.

DỮ LIỆU TÔI ĐANG CÓ
- Tên bộ dữ liệu/nguồn: Oklahoma Purchase Card (P-Card) Transactions.
- Đơn vị quan sát (mỗi dòng là gì): một giao dịch.
- Quy mô và khung thời gian: hàng trăm nghìn giao dịch.
- Các cột dữ liệu (ghi đúng tên cột): tháng ghi sổ, mã và tên cơ quan (Agency), tên chủ thẻ, mô tả, số tiền (Amount), nhà cung cấp (Vendor), ngày giao dịch, ngày ghi sổ, mã ngành hàng (MCC) – đối chiếu lại tên cột trong tệp tải về.
- Hạn chế đã biết: không có nhãn sai phạm; không có hạn mức từng thẻ.

════════════════════════════════════════
PHẦN A — MÔ HÌNH 4 LỚP CÂU HỎI (phễu thu hẹp: Vấn đề kinh doanh → Câu hỏi kinh doanh → Câu hỏi phân tích → Câu hỏi thống kê)
════════════════════════════════════════
Lớp 1 (Vấn đề kinh doanh) là fact đã nêu ở trên: rộng, mơ hồ, chưa phân tích trực tiếp được. Hãy thu hẹp dần qua các lớp 2–4 dưới đây.

LỚP 2) CÂU HỎI KINH DOANH (thu hẹp phạm vi) – đặt 5–7 câu, sắp xếp theo ưu tiên
- Là câu hỏi mở, ngôn ngữ quản lý, KHÔNG gắn số liệu cụ thể; chỉ nằm trong PHẠM VI.
- Mục đích: định hướng điều tra nguyên nhân của VẤN ĐỀ KINH DOANH và phục vụ QUYẾT ĐỊNH ở trên.
- Ưu tiên = mức ảnh hưởng tới QUYẾT ĐỊNH × khả năng trả lời bằng dữ liệu đang có.
- Ví dụ dạng: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”

LỚP 3) CÂU HỎI PHÂN TÍCH (gắn với dữ liệu) – tương ứng với mỗi câu hỏi kinh doanh
- Chuyển câu hỏi kinh doanh thành yêu cầu đo lường được.
- Phải gắn cụ thể: tên đơn vị/phạm vi, khoảng thời gian so sánh, chỉ số liên quan (kèm định nghĩa công thức).
- Ví dụ dạng: “[Chỉ số X] tại [đơn vị Y] đã thay đổi bao nhiêu % trong [kỳ A] so với [kỳ B]?”

LỚP 4) CÂU HỎI THỐNG KÊ (đo lường cụ thể) – tương ứng với mỗi câu hỏi phân tích
- Là câu hỏi trả lời trực tiếp được bằng một phép tính cụ thể trên dữ liệu, cho ra một con số với đơn vị đo rõ ràng.
- Ghi rõ: (i) các cột sử dụng, đúng tên; (ii) phép tính/kỹ thuật (tổng, trung bình, tỷ lệ, kiểm định, hồi quy, mô hình dự báo, tối ưu hóa, mô phỏng…); (iii) đơn vị đo của kết quả.
- Ví dụ dạng: “[Chỉ số cụ thể] trung bình/tổng tại [đơn vị Y]: [kỳ A] vs [kỳ B] là bao nhiêu [đơn vị đo]?”

MINH HỌA MỘT CHUỖI 4 LỚP
- Lớp 1 – Vấn đề kinh doanh: “Lợi nhuận quý này giảm 12% so với quý trước.”
- Lớp 2 – Câu hỏi kinh doanh: “Chi phí nào tăng nhanh nhất và ở khu vực nào?”
- Lớp 3 – Câu hỏi phân tích: “Chi phí nguyên liệu tại chi nhánh Đà Nẵng đã tăng bao nhiêu % trong Q3 so với Q2?”
- Lớp 4 – Câu hỏi thống kê: “Giá vốn hàng bán (COGS) trung bình/đơn hàng tại Đà Nẵng: Q2 vs Q3 là bao nhiêu VNĐ?”

PHÂN LOẠI LOẠI HÌNH CÂU HỎI (thuộc tính của mỗi chuỗi câu hỏi, không phải một lớp)
- Gắn mỗi câu hỏi kinh doanh (và chuỗi câu hỏi đi kèm) với một loại hình: Mô tả (điều gì đã xảy ra?) / Chẩn đoán (vì sao?) / Dự đoán (điều gì có thể xảy ra?) / Đề xuất (nên làm gì?).
- Khuyến khích bộ câu hỏi phủ đủ 4 loại hình nhưng không bắt buộc: nếu với QUYẾT ĐỊNH này một loại hình không cần thiết, bỏ qua và nêu lý do. Ít nhất một câu phải trả lời trực tiếp QUYẾT ĐỊNH.
- Ví dụ dạng câu hỏi kinh doanh theo loại hình:
    • Mô tả: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”
    • Chẩn đoán: “Vì sao [kết quả] ở [phạm vi nào] lại [tăng/giảm]?”
    • Dự đoán: “[Kết quả] sẽ diễn biến thế nào trong [kỳ tới] nếu [điều kiện] giữ nguyên?”
    • Đề xuất: “Nên [hành động nào] với [đối tượng nào] để đạt [mục tiêu] trong [ràng buộc]?”
- Ví dụ dạng câu hỏi thống kê theo loại hình (ngoài dạng Mô tả ở Lớp 4):
    • Chẩn đoán: “Chênh lệch trung bình [cột X] giữa [nhóm 1] và [nhóm 2] là bao nhiêu [đơn vị đo], p-value của kiểm định [t / chi-bình phương] là bao nhiêu?”
    • Dự đoán: “Mô hình [tên] dùng [các cột] dự báo [cột mục tiêu] cho [kỳ tới] có sai số [MAPE/RMSE/AUC] bao nhiêu trên tập kiểm tra [kỳ C]?”
    • Đề xuất: “Với [ràng buộc], giá trị tối ưu của [biến quyết định] là bao nhiêu và [KPI] tăng thêm bao nhiêu [đơn vị đo] so với hiện trạng?”

════════════════════════════════════════
PHẦN B — HAI YÊU CẦU BỔ SUNG
════════════════════════════════════════

BỔ SUNG 1) DỮ LIỆU CẦN THU THẬP THÊM – kiểm tra từng câu hỏi thống kê
- Nếu dữ liệu đang có đã đủ: ghi “Đủ dữ liệu hiện có”.
- Nếu chưa đủ, chỉ rõ: a. tên trường còn thiếu; b. nguồn có thể thu thập; c. mức ưu tiên (Cao/Trung bình/Thấp); d. nếu không thu thập được (dữ liệu công khai), đề xuất biến thay thế hoặc giả định có căn cứ và cách kiểm tra độ nhạy.
- Ví dụ: “Thiếu giá vốn theo sản phẩm – nguồn: phần mềm kế toán hoặc BCTC doanh nghiệp cùng ngành – ưu tiên Cao – nếu không có: giả định biên gộp theo danh mục, kiểm tra độ nhạy ±5 điểm %.”

BỔ SUNG 2) HÀNH ĐỘNG DỰ KIẾN – cho mỗi câu hỏi kinh doanh
- Viết dạng: “Nếu [chỉ số] [>/<] [ngưỡng] thì [hành động A]; ngược lại [hành động B]”. Nếu chưa biết ngưỡng, ghi ngưỡng là tham số cần xác định và cách xác định.
- Ví dụ: “Nếu tỷ lệ giao trễ ở vùng Y > 15% → mở kho vệ tinh tại Y; ngược lại → giữ mạng lưới hiện tại và điều chỉnh cam kết thời gian giao.”

════════════════════════════════════════
QUY TẮC CHO AI
════════════════════════════════════════
- Không bịa trường dữ liệu: chỉ dùng các cột đã liệt kê; mọi trường khác phải đưa vào cột “Dữ liệu cần thu thập thêm”.
- Không trả lời các câu hỏi, không đưa số liệu giả định như thể là kết quả.
- Nếu bối cảnh hoặc dữ liệu chưa đủ để đặt câu hỏi tốt, nêu điểm thiếu ở đầu câu trả lời, rồi vẫn lập bảng với giả định tạm thời được ghi rõ.

════════════════════════════════════════
YÊU CẦU TRÌNH BÀY
════════════════════════════════════════
- 1. Nhắc lại LỚP 1 (Vấn đề kinh doanh) ở đầu câu trả lời, sau đó lập bảng, mỗi dòng 6 cột: [Câu hỏi kinh doanh (đã sắp ưu tiên) | Câu hỏi phân tích | Câu hỏi thống kê | Loại hình câu hỏi | Dữ liệu cần thu thập thêm (nếu có) | Hành động dự kiến].
- 2. Dưới bảng: (a) CÂU HỎI QUYẾT ĐỊNH CHỐT, viết trong một câu; (b) tự kiểm tra: số câu theo từng loại hình, số câu thống kê “Đủ dữ liệu hiện có”, các câu phải dựa vào giả định; (c) đánh giá mức khả thi của đề tài với dữ liệu hiện có (Cao/Trung bình/Thấp) và lý do.
```

## Chủ đề 9: Thuế suất thực tế và quyết định địa điểm đầu tư

```text
VAI TRÒ CỦA AI
Bạn là chuyên gia phân tích kinh doanh, hỗ trợ tôi thực hiện bước S (Specify the question) của mô hình SOAR. Ở bước này chỉ giúp tôi đặt đúng câu hỏi: KHÔNG phân tích dữ liệu, KHÔNG đưa ra số liệu hay kết luận.

BỐI CẢNH
Tôi là Trưởng phòng Thuế tại một tập đoàn sản xuất đa quốc gia (bối cảnh giả định).

LỚP 1) VẤN ĐỀ KINH DOANH – fact đã biết (rộng, có số liệu và mốc so sánh)
“Thuế suất thực tế trung vị của doanh nghiệp niêm yết ngành [__] tại Việt Nam giai đoạn [__]–[__] là [__]%, so với thuế suất phổ thông 20%; doanh thu hợp nhất của tập đoàn là [__] triệu EUR.”
Nguồn của fact: chi phí thuế TNDN / LN trước thuế từ BCTC doanh nghiệp niêm yết.

QUYẾT ĐỊNH cần đưa ra sau phân tích
“Chọn địa điểm và cơ chế ưu đãi cho dự án nhà máy mới.”
KPI đánh giá quyết định: NPV sau thuế; thuế suất thực tế.
Ràng buộc: tuân thủ pháp luật; vốn đầu tư [__].

PHẠM VI phân tích
- Chỉ tập trung vào: 2–3 phương án địa điểm.
- KHÔNG xét đến: chuyển giá, thuế gián thu.

DỮ LIỆU TÔI ĐANG CÓ
- Tên bộ dữ liệu/nguồn: BCTC doanh nghiệp niêm yết Việt Nam; OECD Corporate Tax Statistics.
- Đơn vị quan sát (mỗi dòng là gì): doanh nghiệp – năm; quốc gia – năm.
- Quy mô và khung thời gian: [__] doanh nghiệp, [__] năm.
- Các cột dữ liệu (ghi đúng tên cột): LN trước thuế, chi phí thuế TNDN hiện hành, chi phí thuế TNDN hoãn lại, doanh thu, tổng tài sản, TSCĐ, nợ vay, ngành, loại sở hữu; OECD: thuế suất danh nghĩa, EATR, EMTR.
- Hạn chế đã biết: không có dữ liệu thuế nội bộ của tập đoàn; quy định thay đổi (Luật 67/2025/QH15, NQ 107/2023/QH15).

════════════════════════════════════════
PHẦN A — MÔ HÌNH 4 LỚP CÂU HỎI (phễu thu hẹp: Vấn đề kinh doanh → Câu hỏi kinh doanh → Câu hỏi phân tích → Câu hỏi thống kê)
════════════════════════════════════════
Lớp 1 (Vấn đề kinh doanh) là fact đã nêu ở trên: rộng, mơ hồ, chưa phân tích trực tiếp được. Hãy thu hẹp dần qua các lớp 2–4 dưới đây.

LỚP 2) CÂU HỎI KINH DOANH (thu hẹp phạm vi) – đặt 5–7 câu, sắp xếp theo ưu tiên
- Là câu hỏi mở, ngôn ngữ quản lý, KHÔNG gắn số liệu cụ thể; chỉ nằm trong PHẠM VI.
- Mục đích: định hướng điều tra nguyên nhân của VẤN ĐỀ KINH DOANH và phục vụ QUYẾT ĐỊNH ở trên.
- Ưu tiên = mức ảnh hưởng tới QUYẾT ĐỊNH × khả năng trả lời bằng dữ liệu đang có.
- Ví dụ dạng: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”

LỚP 3) CÂU HỎI PHÂN TÍCH (gắn với dữ liệu) – tương ứng với mỗi câu hỏi kinh doanh
- Chuyển câu hỏi kinh doanh thành yêu cầu đo lường được.
- Phải gắn cụ thể: tên đơn vị/phạm vi, khoảng thời gian so sánh, chỉ số liên quan (kèm định nghĩa công thức).
- Ví dụ dạng: “[Chỉ số X] tại [đơn vị Y] đã thay đổi bao nhiêu % trong [kỳ A] so với [kỳ B]?”

LỚP 4) CÂU HỎI THỐNG KÊ (đo lường cụ thể) – tương ứng với mỗi câu hỏi phân tích
- Là câu hỏi trả lời trực tiếp được bằng một phép tính cụ thể trên dữ liệu, cho ra một con số với đơn vị đo rõ ràng.
- Ghi rõ: (i) các cột sử dụng, đúng tên; (ii) phép tính/kỹ thuật (tổng, trung bình, tỷ lệ, kiểm định, hồi quy, mô hình dự báo, tối ưu hóa, mô phỏng…); (iii) đơn vị đo của kết quả.
- Ví dụ dạng: “[Chỉ số cụ thể] trung bình/tổng tại [đơn vị Y]: [kỳ A] vs [kỳ B] là bao nhiêu [đơn vị đo]?”

MINH HỌA MỘT CHUỖI 4 LỚP
- Lớp 1 – Vấn đề kinh doanh: “Lợi nhuận quý này giảm 12% so với quý trước.”
- Lớp 2 – Câu hỏi kinh doanh: “Chi phí nào tăng nhanh nhất và ở khu vực nào?”
- Lớp 3 – Câu hỏi phân tích: “Chi phí nguyên liệu tại chi nhánh Đà Nẵng đã tăng bao nhiêu % trong Q3 so với Q2?”
- Lớp 4 – Câu hỏi thống kê: “Giá vốn hàng bán (COGS) trung bình/đơn hàng tại Đà Nẵng: Q2 vs Q3 là bao nhiêu VNĐ?”

PHÂN LOẠI LOẠI HÌNH CÂU HỎI (thuộc tính của mỗi chuỗi câu hỏi, không phải một lớp)
- Gắn mỗi câu hỏi kinh doanh (và chuỗi câu hỏi đi kèm) với một loại hình: Mô tả (điều gì đã xảy ra?) / Chẩn đoán (vì sao?) / Dự đoán (điều gì có thể xảy ra?) / Đề xuất (nên làm gì?).
- Khuyến khích bộ câu hỏi phủ đủ 4 loại hình nhưng không bắt buộc: nếu với QUYẾT ĐỊNH này một loại hình không cần thiết, bỏ qua và nêu lý do. Ít nhất một câu phải trả lời trực tiếp QUYẾT ĐỊNH.
- Ví dụ dạng câu hỏi kinh doanh theo loại hình:
    • Mô tả: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”
    • Chẩn đoán: “Vì sao [kết quả] ở [phạm vi nào] lại [tăng/giảm]?”
    • Dự đoán: “[Kết quả] sẽ diễn biến thế nào trong [kỳ tới] nếu [điều kiện] giữ nguyên?”
    • Đề xuất: “Nên [hành động nào] với [đối tượng nào] để đạt [mục tiêu] trong [ràng buộc]?”
- Ví dụ dạng câu hỏi thống kê theo loại hình (ngoài dạng Mô tả ở Lớp 4):
    • Chẩn đoán: “Chênh lệch trung bình [cột X] giữa [nhóm 1] và [nhóm 2] là bao nhiêu [đơn vị đo], p-value của kiểm định [t / chi-bình phương] là bao nhiêu?”
    • Dự đoán: “Mô hình [tên] dùng [các cột] dự báo [cột mục tiêu] cho [kỳ tới] có sai số [MAPE/RMSE/AUC] bao nhiêu trên tập kiểm tra [kỳ C]?”
    • Đề xuất: “Với [ràng buộc], giá trị tối ưu của [biến quyết định] là bao nhiêu và [KPI] tăng thêm bao nhiêu [đơn vị đo] so với hiện trạng?”

════════════════════════════════════════
PHẦN B — HAI YÊU CẦU BỔ SUNG
════════════════════════════════════════

BỔ SUNG 1) DỮ LIỆU CẦN THU THẬP THÊM – kiểm tra từng câu hỏi thống kê
- Nếu dữ liệu đang có đã đủ: ghi “Đủ dữ liệu hiện có”.
- Nếu chưa đủ, chỉ rõ: a. tên trường còn thiếu; b. nguồn có thể thu thập; c. mức ưu tiên (Cao/Trung bình/Thấp); d. nếu không thu thập được (dữ liệu công khai), đề xuất biến thay thế hoặc giả định có căn cứ và cách kiểm tra độ nhạy.
- Ví dụ: “Thiếu giá vốn theo sản phẩm – nguồn: phần mềm kế toán hoặc BCTC doanh nghiệp cùng ngành – ưu tiên Cao – nếu không có: giả định biên gộp theo danh mục, kiểm tra độ nhạy ±5 điểm %.”

BỔ SUNG 2) HÀNH ĐỘNG DỰ KIẾN – cho mỗi câu hỏi kinh doanh
- Viết dạng: “Nếu [chỉ số] [>/<] [ngưỡng] thì [hành động A]; ngược lại [hành động B]”. Nếu chưa biết ngưỡng, ghi ngưỡng là tham số cần xác định và cách xác định.
- Ví dụ: “Nếu tỷ lệ giao trễ ở vùng Y > 15% → mở kho vệ tinh tại Y; ngược lại → giữ mạng lưới hiện tại và điều chỉnh cam kết thời gian giao.”

════════════════════════════════════════
QUY TẮC CHO AI
════════════════════════════════════════
- Không bịa trường dữ liệu: chỉ dùng các cột đã liệt kê; mọi trường khác phải đưa vào cột “Dữ liệu cần thu thập thêm”.
- Không trả lời các câu hỏi, không đưa số liệu giả định như thể là kết quả.
- Nếu bối cảnh hoặc dữ liệu chưa đủ để đặt câu hỏi tốt, nêu điểm thiếu ở đầu câu trả lời, rồi vẫn lập bảng với giả định tạm thời được ghi rõ.

════════════════════════════════════════
YÊU CẦU TRÌNH BÀY
════════════════════════════════════════
- 1. Nhắc lại LỚP 1 (Vấn đề kinh doanh) ở đầu câu trả lời, sau đó lập bảng, mỗi dòng 6 cột: [Câu hỏi kinh doanh (đã sắp ưu tiên) | Câu hỏi phân tích | Câu hỏi thống kê | Loại hình câu hỏi | Dữ liệu cần thu thập thêm (nếu có) | Hành động dự kiến].
- 2. Dưới bảng: (a) CÂU HỎI QUYẾT ĐỊNH CHỐT, viết trong một câu; (b) tự kiểm tra: số câu theo từng loại hình, số câu thống kê “Đủ dữ liệu hiện có”, các câu phải dựa vào giả định; (c) đánh giá mức khả thi của đề tài với dữ liệu hiện có (Cao/Trung bình/Thấp) và lý do.
```

## Chủ đề 10: Tối ưu chi phí điện năng theo biểu giá ba khung giờ

```text
VAI TRÒ CỦA AI
Bạn là chuyên gia phân tích kinh doanh, hỗ trợ tôi thực hiện bước S (Specify the question) của mô hình SOAR. Ở bước này chỉ giúp tôi đặt đúng câu hỏi: KHÔNG phân tích dữ liệu, KHÔNG đưa ra số liệu hay kết luận.

BỐI CẢNH
Tôi là Trưởng ban quản lý tòa nhà tại một tòa nhà văn phòng (bối cảnh theo dữ liệu ASHRAE, primary_use = Office).

LỚP 1) VẤN ĐỀ KINH DOANH – fact đã biết (rộng, có số liệu và mốc so sánh)
“Tải nền ban đêm (0h–6h) bằng [__]% tải trung bình giờ hành chính; chi phí điện ước tính theo biểu giá ba khung giờ là [__] triệu đồng/năm.”
Nguồn của fact: meter_reading của meter = 0 (điện) theo giờ, ghép biểu giá EVN.

QUYẾT ĐỊNH cần đưa ra sau phân tích
“Chọn biện pháp dịch tải và giảm tải nền cho năm tới.”
KPI đánh giá quyết định: chi phí điện; kWh/m²/năm.
Ràng buộc: không ảnh hưởng tiện nghi trong giờ làm việc.

PHẠM VI phân tích
- Chỉ tập trung vào: các tòa có primary_use = Office, công tơ điện.
- KHÔNG xét đến: nước lạnh, hơi, nước nóng.

DỮ LIỆU TÔI ĐANG CÓ
- Tên bộ dữ liệu/nguồn: ASHRAE – Great Energy Predictor III.
- Đơn vị quan sát (mỗi dòng là gì): tòa nhà – loại công tơ – giờ.
- Quy mô và khung thời gian: năm 2016.
- Các cột dữ liệu (ghi đúng tên cột): building_id, meter, timestamp, meter_reading, site_id, primary_use, square_feet, year_built, air_temperature, dew_temperature.
- Hạn chế đã biết: tòa nhà không ở Việt Nam; không biết phụ tải nào dịch chuyển được; biểu giá Việt Nam là dữ liệu ghép thêm.

════════════════════════════════════════
PHẦN A — MÔ HÌNH 4 LỚP CÂU HỎI (phễu thu hẹp: Vấn đề kinh doanh → Câu hỏi kinh doanh → Câu hỏi phân tích → Câu hỏi thống kê)
════════════════════════════════════════
Lớp 1 (Vấn đề kinh doanh) là fact đã nêu ở trên: rộng, mơ hồ, chưa phân tích trực tiếp được. Hãy thu hẹp dần qua các lớp 2–4 dưới đây.

LỚP 2) CÂU HỎI KINH DOANH (thu hẹp phạm vi) – đặt 5–7 câu, sắp xếp theo ưu tiên
- Là câu hỏi mở, ngôn ngữ quản lý, KHÔNG gắn số liệu cụ thể; chỉ nằm trong PHẠM VI.
- Mục đích: định hướng điều tra nguyên nhân của VẤN ĐỀ KINH DOANH và phục vụ QUYẾT ĐỊNH ở trên.
- Ưu tiên = mức ảnh hưởng tới QUYẾT ĐỊNH × khả năng trả lời bằng dữ liệu đang có.
- Ví dụ dạng: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”

LỚP 3) CÂU HỎI PHÂN TÍCH (gắn với dữ liệu) – tương ứng với mỗi câu hỏi kinh doanh
- Chuyển câu hỏi kinh doanh thành yêu cầu đo lường được.
- Phải gắn cụ thể: tên đơn vị/phạm vi, khoảng thời gian so sánh, chỉ số liên quan (kèm định nghĩa công thức).
- Ví dụ dạng: “[Chỉ số X] tại [đơn vị Y] đã thay đổi bao nhiêu % trong [kỳ A] so với [kỳ B]?”

LỚP 4) CÂU HỎI THỐNG KÊ (đo lường cụ thể) – tương ứng với mỗi câu hỏi phân tích
- Là câu hỏi trả lời trực tiếp được bằng một phép tính cụ thể trên dữ liệu, cho ra một con số với đơn vị đo rõ ràng.
- Ghi rõ: (i) các cột sử dụng, đúng tên; (ii) phép tính/kỹ thuật (tổng, trung bình, tỷ lệ, kiểm định, hồi quy, mô hình dự báo, tối ưu hóa, mô phỏng…); (iii) đơn vị đo của kết quả.
- Ví dụ dạng: “[Chỉ số cụ thể] trung bình/tổng tại [đơn vị Y]: [kỳ A] vs [kỳ B] là bao nhiêu [đơn vị đo]?”

MINH HỌA MỘT CHUỖI 4 LỚP
- Lớp 1 – Vấn đề kinh doanh: “Lợi nhuận quý này giảm 12% so với quý trước.”
- Lớp 2 – Câu hỏi kinh doanh: “Chi phí nào tăng nhanh nhất và ở khu vực nào?”
- Lớp 3 – Câu hỏi phân tích: “Chi phí nguyên liệu tại chi nhánh Đà Nẵng đã tăng bao nhiêu % trong Q3 so với Q2?”
- Lớp 4 – Câu hỏi thống kê: “Giá vốn hàng bán (COGS) trung bình/đơn hàng tại Đà Nẵng: Q2 vs Q3 là bao nhiêu VNĐ?”

PHÂN LOẠI LOẠI HÌNH CÂU HỎI (thuộc tính của mỗi chuỗi câu hỏi, không phải một lớp)
- Gắn mỗi câu hỏi kinh doanh (và chuỗi câu hỏi đi kèm) với một loại hình: Mô tả (điều gì đã xảy ra?) / Chẩn đoán (vì sao?) / Dự đoán (điều gì có thể xảy ra?) / Đề xuất (nên làm gì?).
- Khuyến khích bộ câu hỏi phủ đủ 4 loại hình nhưng không bắt buộc: nếu với QUYẾT ĐỊNH này một loại hình không cần thiết, bỏ qua và nêu lý do. Ít nhất một câu phải trả lời trực tiếp QUYẾT ĐỊNH.
- Ví dụ dạng câu hỏi kinh doanh theo loại hình:
    • Mô tả: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”
    • Chẩn đoán: “Vì sao [kết quả] ở [phạm vi nào] lại [tăng/giảm]?”
    • Dự đoán: “[Kết quả] sẽ diễn biến thế nào trong [kỳ tới] nếu [điều kiện] giữ nguyên?”
    • Đề xuất: “Nên [hành động nào] với [đối tượng nào] để đạt [mục tiêu] trong [ràng buộc]?”
- Ví dụ dạng câu hỏi thống kê theo loại hình (ngoài dạng Mô tả ở Lớp 4):
    • Chẩn đoán: “Chênh lệch trung bình [cột X] giữa [nhóm 1] và [nhóm 2] là bao nhiêu [đơn vị đo], p-value của kiểm định [t / chi-bình phương] là bao nhiêu?”
    • Dự đoán: “Mô hình [tên] dùng [các cột] dự báo [cột mục tiêu] cho [kỳ tới] có sai số [MAPE/RMSE/AUC] bao nhiêu trên tập kiểm tra [kỳ C]?”
    • Đề xuất: “Với [ràng buộc], giá trị tối ưu của [biến quyết định] là bao nhiêu và [KPI] tăng thêm bao nhiêu [đơn vị đo] so với hiện trạng?”

════════════════════════════════════════
PHẦN B — HAI YÊU CẦU BỔ SUNG
════════════════════════════════════════

BỔ SUNG 1) DỮ LIỆU CẦN THU THẬP THÊM – kiểm tra từng câu hỏi thống kê
- Nếu dữ liệu đang có đã đủ: ghi “Đủ dữ liệu hiện có”.
- Nếu chưa đủ, chỉ rõ: a. tên trường còn thiếu; b. nguồn có thể thu thập; c. mức ưu tiên (Cao/Trung bình/Thấp); d. nếu không thu thập được (dữ liệu công khai), đề xuất biến thay thế hoặc giả định có căn cứ và cách kiểm tra độ nhạy.
- Ví dụ: “Thiếu giá vốn theo sản phẩm – nguồn: phần mềm kế toán hoặc BCTC doanh nghiệp cùng ngành – ưu tiên Cao – nếu không có: giả định biên gộp theo danh mục, kiểm tra độ nhạy ±5 điểm %.”

BỔ SUNG 2) HÀNH ĐỘNG DỰ KIẾN – cho mỗi câu hỏi kinh doanh
- Viết dạng: “Nếu [chỉ số] [>/<] [ngưỡng] thì [hành động A]; ngược lại [hành động B]”. Nếu chưa biết ngưỡng, ghi ngưỡng là tham số cần xác định và cách xác định.
- Ví dụ: “Nếu tỷ lệ giao trễ ở vùng Y > 15% → mở kho vệ tinh tại Y; ngược lại → giữ mạng lưới hiện tại và điều chỉnh cam kết thời gian giao.”

════════════════════════════════════════
QUY TẮC CHO AI
════════════════════════════════════════
- Không bịa trường dữ liệu: chỉ dùng các cột đã liệt kê; mọi trường khác phải đưa vào cột “Dữ liệu cần thu thập thêm”.
- Không trả lời các câu hỏi, không đưa số liệu giả định như thể là kết quả.
- Nếu bối cảnh hoặc dữ liệu chưa đủ để đặt câu hỏi tốt, nêu điểm thiếu ở đầu câu trả lời, rồi vẫn lập bảng với giả định tạm thời được ghi rõ.

════════════════════════════════════════
YÊU CẦU TRÌNH BÀY
════════════════════════════════════════
- 1. Nhắc lại LỚP 1 (Vấn đề kinh doanh) ở đầu câu trả lời, sau đó lập bảng, mỗi dòng 6 cột: [Câu hỏi kinh doanh (đã sắp ưu tiên) | Câu hỏi phân tích | Câu hỏi thống kê | Loại hình câu hỏi | Dữ liệu cần thu thập thêm (nếu có) | Hành động dự kiến].
- 2. Dưới bảng: (a) CÂU HỎI QUYẾT ĐỊNH CHỐT, viết trong một câu; (b) tự kiểm tra: số câu theo từng loại hình, số câu thống kê “Đủ dữ liệu hiện có”, các câu phải dựa vào giả định; (c) đánh giá mức khả thi của đề tài với dữ liệu hiện có (Cao/Trung bình/Thấp) và lý do.
```

## Chủ đề 11: Hoạch định vốn đầu tư có tính rủi ro

```text
VAI TRÒ CỦA AI
Bạn là chuyên gia phân tích kinh doanh, hỗ trợ tôi thực hiện bước S (Specify the question) của mô hình SOAR. Ở bước này chỉ giúp tôi đặt đúng câu hỏi: KHÔNG phân tích dữ liệu, KHÔNG đưa ra số liệu hay kết luận.

BỐI CẢNH
Tôi là Giám đốc Tài chính tại [tên doanh nghiệp niêm yết] với dự án [__] đã công bố.

LỚP 1) VẤN ĐỀ KINH DOANH – fact đã biết (rộng, có số liệu và mốc so sánh)
“Dự án [__] có tổng vốn đầu tư công bố [__] tỷ đồng; ROIC bình quân 5 năm của doanh nghiệp là [__]% so với WACC ước tính [__]%.”
Nguồn của fact: báo cáo thường niên, nghị quyết ĐHĐCĐ, BCTC.

QUYẾT ĐỊNH cần đưa ra sau phân tích
“Khuyến nghị Hội đồng quản trị phê duyệt, không phê duyệt hoặc điều chỉnh dự án.”
KPI đánh giá quyết định: NPV; IRR; P(NPV < 0).
Ràng buộc: cơ cấu vốn mục tiêu; tiến độ.

PHẠM VI phân tích
- Chỉ tập trung vào: dự án [__].
- KHÔNG xét đến: các mảng kinh doanh khác của doanh nghiệp.

DỮ LIỆU TÔI ĐANG CÓ
- Tên bộ dữ liệu/nguồn: BCTN, nghị quyết ĐHĐCĐ, BCTC (vnstock); World Bank Pink Sheet; lợi suất TPCP.
- Đơn vị quan sát (mỗi dòng là gì): doanh nghiệp – năm; hàng hóa – tháng.
- Quy mô và khung thời gian: [__] năm.
- Các cột dữ liệu (ghi đúng tên cột): capex, EBIT, thuế, khấu hao, vốn lưu động, nợ vay, vốn hóa thị trường; giá sản phẩm và nguyên liệu; lợi suất TPCP 10 năm; beta.
- Hạn chế đã biết: không có dòng tiền cấp dự án – phải dựng mô hình từ thông tin công bố.

════════════════════════════════════════
PHẦN A — MÔ HÌNH 4 LỚP CÂU HỎI (phễu thu hẹp: Vấn đề kinh doanh → Câu hỏi kinh doanh → Câu hỏi phân tích → Câu hỏi thống kê)
════════════════════════════════════════
Lớp 1 (Vấn đề kinh doanh) là fact đã nêu ở trên: rộng, mơ hồ, chưa phân tích trực tiếp được. Hãy thu hẹp dần qua các lớp 2–4 dưới đây.

LỚP 2) CÂU HỎI KINH DOANH (thu hẹp phạm vi) – đặt 5–7 câu, sắp xếp theo ưu tiên
- Là câu hỏi mở, ngôn ngữ quản lý, KHÔNG gắn số liệu cụ thể; chỉ nằm trong PHẠM VI.
- Mục đích: định hướng điều tra nguyên nhân của VẤN ĐỀ KINH DOANH và phục vụ QUYẾT ĐỊNH ở trên.
- Ưu tiên = mức ảnh hưởng tới QUYẾT ĐỊNH × khả năng trả lời bằng dữ liệu đang có.
- Ví dụ dạng: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”

LỚP 3) CÂU HỎI PHÂN TÍCH (gắn với dữ liệu) – tương ứng với mỗi câu hỏi kinh doanh
- Chuyển câu hỏi kinh doanh thành yêu cầu đo lường được.
- Phải gắn cụ thể: tên đơn vị/phạm vi, khoảng thời gian so sánh, chỉ số liên quan (kèm định nghĩa công thức).
- Ví dụ dạng: “[Chỉ số X] tại [đơn vị Y] đã thay đổi bao nhiêu % trong [kỳ A] so với [kỳ B]?”

LỚP 4) CÂU HỎI THỐNG KÊ (đo lường cụ thể) – tương ứng với mỗi câu hỏi phân tích
- Là câu hỏi trả lời trực tiếp được bằng một phép tính cụ thể trên dữ liệu, cho ra một con số với đơn vị đo rõ ràng.
- Ghi rõ: (i) các cột sử dụng, đúng tên; (ii) phép tính/kỹ thuật (tổng, trung bình, tỷ lệ, kiểm định, hồi quy, mô hình dự báo, tối ưu hóa, mô phỏng…); (iii) đơn vị đo của kết quả.
- Ví dụ dạng: “[Chỉ số cụ thể] trung bình/tổng tại [đơn vị Y]: [kỳ A] vs [kỳ B] là bao nhiêu [đơn vị đo]?”

MINH HỌA MỘT CHUỖI 4 LỚP
- Lớp 1 – Vấn đề kinh doanh: “Lợi nhuận quý này giảm 12% so với quý trước.”
- Lớp 2 – Câu hỏi kinh doanh: “Chi phí nào tăng nhanh nhất và ở khu vực nào?”
- Lớp 3 – Câu hỏi phân tích: “Chi phí nguyên liệu tại chi nhánh Đà Nẵng đã tăng bao nhiêu % trong Q3 so với Q2?”
- Lớp 4 – Câu hỏi thống kê: “Giá vốn hàng bán (COGS) trung bình/đơn hàng tại Đà Nẵng: Q2 vs Q3 là bao nhiêu VNĐ?”

PHÂN LOẠI LOẠI HÌNH CÂU HỎI (thuộc tính của mỗi chuỗi câu hỏi, không phải một lớp)
- Gắn mỗi câu hỏi kinh doanh (và chuỗi câu hỏi đi kèm) với một loại hình: Mô tả (điều gì đã xảy ra?) / Chẩn đoán (vì sao?) / Dự đoán (điều gì có thể xảy ra?) / Đề xuất (nên làm gì?).
- Khuyến khích bộ câu hỏi phủ đủ 4 loại hình nhưng không bắt buộc: nếu với QUYẾT ĐỊNH này một loại hình không cần thiết, bỏ qua và nêu lý do. Ít nhất một câu phải trả lời trực tiếp QUYẾT ĐỊNH.
- Ví dụ dạng câu hỏi kinh doanh theo loại hình:
    • Mô tả: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”
    • Chẩn đoán: “Vì sao [kết quả] ở [phạm vi nào] lại [tăng/giảm]?”
    • Dự đoán: “[Kết quả] sẽ diễn biến thế nào trong [kỳ tới] nếu [điều kiện] giữ nguyên?”
    • Đề xuất: “Nên [hành động nào] với [đối tượng nào] để đạt [mục tiêu] trong [ràng buộc]?”
- Ví dụ dạng câu hỏi thống kê theo loại hình (ngoài dạng Mô tả ở Lớp 4):
    • Chẩn đoán: “Chênh lệch trung bình [cột X] giữa [nhóm 1] và [nhóm 2] là bao nhiêu [đơn vị đo], p-value của kiểm định [t / chi-bình phương] là bao nhiêu?”
    • Dự đoán: “Mô hình [tên] dùng [các cột] dự báo [cột mục tiêu] cho [kỳ tới] có sai số [MAPE/RMSE/AUC] bao nhiêu trên tập kiểm tra [kỳ C]?”
    • Đề xuất: “Với [ràng buộc], giá trị tối ưu của [biến quyết định] là bao nhiêu và [KPI] tăng thêm bao nhiêu [đơn vị đo] so với hiện trạng?”

════════════════════════════════════════
PHẦN B — HAI YÊU CẦU BỔ SUNG
════════════════════════════════════════

BỔ SUNG 1) DỮ LIỆU CẦN THU THẬP THÊM – kiểm tra từng câu hỏi thống kê
- Nếu dữ liệu đang có đã đủ: ghi “Đủ dữ liệu hiện có”.
- Nếu chưa đủ, chỉ rõ: a. tên trường còn thiếu; b. nguồn có thể thu thập; c. mức ưu tiên (Cao/Trung bình/Thấp); d. nếu không thu thập được (dữ liệu công khai), đề xuất biến thay thế hoặc giả định có căn cứ và cách kiểm tra độ nhạy.
- Ví dụ: “Thiếu giá vốn theo sản phẩm – nguồn: phần mềm kế toán hoặc BCTC doanh nghiệp cùng ngành – ưu tiên Cao – nếu không có: giả định biên gộp theo danh mục, kiểm tra độ nhạy ±5 điểm %.”

BỔ SUNG 2) HÀNH ĐỘNG DỰ KIẾN – cho mỗi câu hỏi kinh doanh
- Viết dạng: “Nếu [chỉ số] [>/<] [ngưỡng] thì [hành động A]; ngược lại [hành động B]”. Nếu chưa biết ngưỡng, ghi ngưỡng là tham số cần xác định và cách xác định.
- Ví dụ: “Nếu tỷ lệ giao trễ ở vùng Y > 15% → mở kho vệ tinh tại Y; ngược lại → giữ mạng lưới hiện tại và điều chỉnh cam kết thời gian giao.”

════════════════════════════════════════
QUY TẮC CHO AI
════════════════════════════════════════
- Không bịa trường dữ liệu: chỉ dùng các cột đã liệt kê; mọi trường khác phải đưa vào cột “Dữ liệu cần thu thập thêm”.
- Không trả lời các câu hỏi, không đưa số liệu giả định như thể là kết quả.
- Nếu bối cảnh hoặc dữ liệu chưa đủ để đặt câu hỏi tốt, nêu điểm thiếu ở đầu câu trả lời, rồi vẫn lập bảng với giả định tạm thời được ghi rõ.

════════════════════════════════════════
YÊU CẦU TRÌNH BÀY
════════════════════════════════════════
- 1. Nhắc lại LỚP 1 (Vấn đề kinh doanh) ở đầu câu trả lời, sau đó lập bảng, mỗi dòng 6 cột: [Câu hỏi kinh doanh (đã sắp ưu tiên) | Câu hỏi phân tích | Câu hỏi thống kê | Loại hình câu hỏi | Dữ liệu cần thu thập thêm (nếu có) | Hành động dự kiến].
- 2. Dưới bảng: (a) CÂU HỎI QUYẾT ĐỊNH CHỐT, viết trong một câu; (b) tự kiểm tra: số câu theo từng loại hình, số câu thống kê “Đủ dữ liệu hiện có”, các câu phải dựa vào giả định; (c) đánh giá mức khả thi của đề tài với dữ liệu hiện có (Cao/Trung bình/Thấp) và lý do.
```

## Chủ đề 12: Tối ưu hóa danh mục đầu tư cổ phiếu Việt Nam

```text
VAI TRÒ CỦA AI
Bạn là chuyên gia phân tích kinh doanh, hỗ trợ tôi thực hiện bước S (Specify the question) của mô hình SOAR. Ở bước này chỉ giúp tôi đặt đúng câu hỏi: KHÔNG phân tích dữ liệu, KHÔNG đưa ra số liệu hay kết luận.

BỐI CẢNH
Tôi là Giám đốc đầu tư tại một quỹ mở cổ phiếu (bối cảnh giả định).

LỚP 1) VẤN ĐỀ KINH DOANH – fact đã biết (rộng, có số liệu và mốc so sánh)
“Trong 3 năm qua, danh mục hiện tại có Sharpe [__] và sụt giảm tối đa [__]%, so với VN-Index là [__] và [__]%.”
Nguồn của fact: giá đóng cửa đã điều chỉnh tải bằng vnstock.

QUYẾT ĐỊNH cần đưa ra sau phân tích
“Xác định tỷ trọng mục tiêu cho kỳ tái cân bằng tới.”
KPI đánh giá quyết định: Sharpe; sụt giảm tối đa; vòng quay danh mục.
Ràng buộc: không bán khống; tối đa [__]% mỗi mã; thanh khoản tối thiểu.

PHẠM VI phân tích
- Chỉ tập trung vào: 15–30 cổ phiếu thanh khoản cao (ví dụ VN30).
- KHÔNG xét đến: phái sinh, trái phiếu doanh nghiệp.

DỮ LIỆU TÔI ĐANG CÓ
- Tên bộ dữ liệu/nguồn: Giá cổ phiếu Việt Nam (vnstock).
- Đơn vị quan sát (mỗi dòng là gì): mã – ngày.
- Quy mô và khung thời gian: [__] năm.
- Các cột dữ liệu (ghi đúng tên cột): time, open, high, low, close (đã điều chỉnh), volume; VN-Index; lãi suất phi rủi ro.
- Hạn chế đã biết: thiên lệch sống sót; cần kiểm tra điều chỉnh cổ tức và chia tách.

════════════════════════════════════════
PHẦN A — MÔ HÌNH 4 LỚP CÂU HỎI (phễu thu hẹp: Vấn đề kinh doanh → Câu hỏi kinh doanh → Câu hỏi phân tích → Câu hỏi thống kê)
════════════════════════════════════════
Lớp 1 (Vấn đề kinh doanh) là fact đã nêu ở trên: rộng, mơ hồ, chưa phân tích trực tiếp được. Hãy thu hẹp dần qua các lớp 2–4 dưới đây.

LỚP 2) CÂU HỎI KINH DOANH (thu hẹp phạm vi) – đặt 5–7 câu, sắp xếp theo ưu tiên
- Là câu hỏi mở, ngôn ngữ quản lý, KHÔNG gắn số liệu cụ thể; chỉ nằm trong PHẠM VI.
- Mục đích: định hướng điều tra nguyên nhân của VẤN ĐỀ KINH DOANH và phục vụ QUYẾT ĐỊNH ở trên.
- Ưu tiên = mức ảnh hưởng tới QUYẾT ĐỊNH × khả năng trả lời bằng dữ liệu đang có.
- Ví dụ dạng: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”

LỚP 3) CÂU HỎI PHÂN TÍCH (gắn với dữ liệu) – tương ứng với mỗi câu hỏi kinh doanh
- Chuyển câu hỏi kinh doanh thành yêu cầu đo lường được.
- Phải gắn cụ thể: tên đơn vị/phạm vi, khoảng thời gian so sánh, chỉ số liên quan (kèm định nghĩa công thức).
- Ví dụ dạng: “[Chỉ số X] tại [đơn vị Y] đã thay đổi bao nhiêu % trong [kỳ A] so với [kỳ B]?”

LỚP 4) CÂU HỎI THỐNG KÊ (đo lường cụ thể) – tương ứng với mỗi câu hỏi phân tích
- Là câu hỏi trả lời trực tiếp được bằng một phép tính cụ thể trên dữ liệu, cho ra một con số với đơn vị đo rõ ràng.
- Ghi rõ: (i) các cột sử dụng, đúng tên; (ii) phép tính/kỹ thuật (tổng, trung bình, tỷ lệ, kiểm định, hồi quy, mô hình dự báo, tối ưu hóa, mô phỏng…); (iii) đơn vị đo của kết quả.
- Ví dụ dạng: “[Chỉ số cụ thể] trung bình/tổng tại [đơn vị Y]: [kỳ A] vs [kỳ B] là bao nhiêu [đơn vị đo]?”

MINH HỌA MỘT CHUỖI 4 LỚP
- Lớp 1 – Vấn đề kinh doanh: “Lợi nhuận quý này giảm 12% so với quý trước.”
- Lớp 2 – Câu hỏi kinh doanh: “Chi phí nào tăng nhanh nhất và ở khu vực nào?”
- Lớp 3 – Câu hỏi phân tích: “Chi phí nguyên liệu tại chi nhánh Đà Nẵng đã tăng bao nhiêu % trong Q3 so với Q2?”
- Lớp 4 – Câu hỏi thống kê: “Giá vốn hàng bán (COGS) trung bình/đơn hàng tại Đà Nẵng: Q2 vs Q3 là bao nhiêu VNĐ?”

PHÂN LOẠI LOẠI HÌNH CÂU HỎI (thuộc tính của mỗi chuỗi câu hỏi, không phải một lớp)
- Gắn mỗi câu hỏi kinh doanh (và chuỗi câu hỏi đi kèm) với một loại hình: Mô tả (điều gì đã xảy ra?) / Chẩn đoán (vì sao?) / Dự đoán (điều gì có thể xảy ra?) / Đề xuất (nên làm gì?).
- Khuyến khích bộ câu hỏi phủ đủ 4 loại hình nhưng không bắt buộc: nếu với QUYẾT ĐỊNH này một loại hình không cần thiết, bỏ qua và nêu lý do. Ít nhất một câu phải trả lời trực tiếp QUYẾT ĐỊNH.
- Ví dụ dạng câu hỏi kinh doanh theo loại hình:
    • Mô tả: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”
    • Chẩn đoán: “Vì sao [kết quả] ở [phạm vi nào] lại [tăng/giảm]?”
    • Dự đoán: “[Kết quả] sẽ diễn biến thế nào trong [kỳ tới] nếu [điều kiện] giữ nguyên?”
    • Đề xuất: “Nên [hành động nào] với [đối tượng nào] để đạt [mục tiêu] trong [ràng buộc]?”
- Ví dụ dạng câu hỏi thống kê theo loại hình (ngoài dạng Mô tả ở Lớp 4):
    • Chẩn đoán: “Chênh lệch trung bình [cột X] giữa [nhóm 1] và [nhóm 2] là bao nhiêu [đơn vị đo], p-value của kiểm định [t / chi-bình phương] là bao nhiêu?”
    • Dự đoán: “Mô hình [tên] dùng [các cột] dự báo [cột mục tiêu] cho [kỳ tới] có sai số [MAPE/RMSE/AUC] bao nhiêu trên tập kiểm tra [kỳ C]?”
    • Đề xuất: “Với [ràng buộc], giá trị tối ưu của [biến quyết định] là bao nhiêu và [KPI] tăng thêm bao nhiêu [đơn vị đo] so với hiện trạng?”

════════════════════════════════════════
PHẦN B — HAI YÊU CẦU BỔ SUNG
════════════════════════════════════════

BỔ SUNG 1) DỮ LIỆU CẦN THU THẬP THÊM – kiểm tra từng câu hỏi thống kê
- Nếu dữ liệu đang có đã đủ: ghi “Đủ dữ liệu hiện có”.
- Nếu chưa đủ, chỉ rõ: a. tên trường còn thiếu; b. nguồn có thể thu thập; c. mức ưu tiên (Cao/Trung bình/Thấp); d. nếu không thu thập được (dữ liệu công khai), đề xuất biến thay thế hoặc giả định có căn cứ và cách kiểm tra độ nhạy.
- Ví dụ: “Thiếu giá vốn theo sản phẩm – nguồn: phần mềm kế toán hoặc BCTC doanh nghiệp cùng ngành – ưu tiên Cao – nếu không có: giả định biên gộp theo danh mục, kiểm tra độ nhạy ±5 điểm %.”

BỔ SUNG 2) HÀNH ĐỘNG DỰ KIẾN – cho mỗi câu hỏi kinh doanh
- Viết dạng: “Nếu [chỉ số] [>/<] [ngưỡng] thì [hành động A]; ngược lại [hành động B]”. Nếu chưa biết ngưỡng, ghi ngưỡng là tham số cần xác định và cách xác định.
- Ví dụ: “Nếu tỷ lệ giao trễ ở vùng Y > 15% → mở kho vệ tinh tại Y; ngược lại → giữ mạng lưới hiện tại và điều chỉnh cam kết thời gian giao.”

════════════════════════════════════════
QUY TẮC CHO AI
════════════════════════════════════════
- Không bịa trường dữ liệu: chỉ dùng các cột đã liệt kê; mọi trường khác phải đưa vào cột “Dữ liệu cần thu thập thêm”.
- Không trả lời các câu hỏi, không đưa số liệu giả định như thể là kết quả.
- Nếu bối cảnh hoặc dữ liệu chưa đủ để đặt câu hỏi tốt, nêu điểm thiếu ở đầu câu trả lời, rồi vẫn lập bảng với giả định tạm thời được ghi rõ.

════════════════════════════════════════
YÊU CẦU TRÌNH BÀY
════════════════════════════════════════
- 1. Nhắc lại LỚP 1 (Vấn đề kinh doanh) ở đầu câu trả lời, sau đó lập bảng, mỗi dòng 6 cột: [Câu hỏi kinh doanh (đã sắp ưu tiên) | Câu hỏi phân tích | Câu hỏi thống kê | Loại hình câu hỏi | Dữ liệu cần thu thập thêm (nếu có) | Hành động dự kiến].
- 2. Dưới bảng: (a) CÂU HỎI QUYẾT ĐỊNH CHỐT, viết trong một câu; (b) tự kiểm tra: số câu theo từng loại hình, số câu thống kê “Đủ dữ liệu hiện có”, các câu phải dựa vào giả định; (c) đánh giá mức khả thi của đề tài với dữ liệu hiện có (Cao/Trung bình/Thấp) và lý do.
```

## Chủ đề 13: Chấm điểm tín dụng cá nhân và chính sách duyệt vay

```text
VAI TRÒ CỦA AI
Bạn là chuyên gia phân tích kinh doanh, hỗ trợ tôi thực hiện bước S (Specify the question) của mô hình SOAR. Ở bước này chỉ giúp tôi đặt đúng câu hỏi: KHÔNG phân tích dữ liệu, KHÔNG đưa ra số liệu hay kết luận.

BỐI CẢNH
Tôi là Giám đốc Quản trị rủi ro tín dụng bán lẻ tại một công ty tài chính tiêu dùng (bối cảnh theo dữ liệu Home Credit).

LỚP 1) VẤN ĐỀ KINH DOANH – fact đã biết (rộng, có số liệu và mốc so sánh)
“Tỷ lệ vỡ nợ là [__]%; nhóm khách dưới 30 tuổi có tỷ lệ [__]%, cao gấp [__] lần nhóm trên 50 tuổi.”
Nguồn của fact: TARGET theo nhóm tuổi tính từ DAYS_BIRTH.

QUYẾT ĐỊNH cần đưa ra sau phân tích
“Đặt ngưỡng điểm duyệt vay và chính sách duyệt có điều kiện cho quý tới.”
KPI đánh giá quyết định: tỷ lệ duyệt; tổn thất kỳ vọng; lợi nhuận kỳ vọng.
Ràng buộc: tỷ lệ duyệt tối thiểu [__]%; mô hình phải giải thích được và công bằng.

PHẠM VI phân tích
- Chỉ tập trung vào: hồ sơ trong application_train.
- KHÔNG xét đến: thu hồi nợ, định giá lãi suất.

DỮ LIỆU TÔI ĐANG CÓ
- Tên bộ dữ liệu/nguồn: Home Credit Default Risk (Kaggle).
- Đơn vị quan sát (mỗi dòng là gì): một hồ sơ vay.
- Quy mô và khung thời gian: khoảng 307 nghìn hồ sơ.
- Các cột dữ liệu (ghi đúng tên cột): SK_ID_CURR, TARGET, NAME_CONTRACT_TYPE, CODE_GENDER, DAYS_BIRTH, DAYS_EMPLOYED, AMT_INCOME_TOTAL, AMT_CREDIT, AMT_ANNUITY, AMT_GOODS_PRICE, NAME_INCOME_TYPE, NAME_EDUCATION_TYPE, EXT_SOURCE_1, EXT_SOURCE_2, EXT_SOURCE_3; bảng phụ bureau, previous_application.
- Hạn chế đã biết: không có LGD và lãi suất; dữ liệu mất cân bằng.

════════════════════════════════════════
PHẦN A — MÔ HÌNH 4 LỚP CÂU HỎI (phễu thu hẹp: Vấn đề kinh doanh → Câu hỏi kinh doanh → Câu hỏi phân tích → Câu hỏi thống kê)
════════════════════════════════════════
Lớp 1 (Vấn đề kinh doanh) là fact đã nêu ở trên: rộng, mơ hồ, chưa phân tích trực tiếp được. Hãy thu hẹp dần qua các lớp 2–4 dưới đây.

LỚP 2) CÂU HỎI KINH DOANH (thu hẹp phạm vi) – đặt 5–7 câu, sắp xếp theo ưu tiên
- Là câu hỏi mở, ngôn ngữ quản lý, KHÔNG gắn số liệu cụ thể; chỉ nằm trong PHẠM VI.
- Mục đích: định hướng điều tra nguyên nhân của VẤN ĐỀ KINH DOANH và phục vụ QUYẾT ĐỊNH ở trên.
- Ưu tiên = mức ảnh hưởng tới QUYẾT ĐỊNH × khả năng trả lời bằng dữ liệu đang có.
- Ví dụ dạng: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”

LỚP 3) CÂU HỎI PHÂN TÍCH (gắn với dữ liệu) – tương ứng với mỗi câu hỏi kinh doanh
- Chuyển câu hỏi kinh doanh thành yêu cầu đo lường được.
- Phải gắn cụ thể: tên đơn vị/phạm vi, khoảng thời gian so sánh, chỉ số liên quan (kèm định nghĩa công thức).
- Ví dụ dạng: “[Chỉ số X] tại [đơn vị Y] đã thay đổi bao nhiêu % trong [kỳ A] so với [kỳ B]?”

LỚP 4) CÂU HỎI THỐNG KÊ (đo lường cụ thể) – tương ứng với mỗi câu hỏi phân tích
- Là câu hỏi trả lời trực tiếp được bằng một phép tính cụ thể trên dữ liệu, cho ra một con số với đơn vị đo rõ ràng.
- Ghi rõ: (i) các cột sử dụng, đúng tên; (ii) phép tính/kỹ thuật (tổng, trung bình, tỷ lệ, kiểm định, hồi quy, mô hình dự báo, tối ưu hóa, mô phỏng…); (iii) đơn vị đo của kết quả.
- Ví dụ dạng: “[Chỉ số cụ thể] trung bình/tổng tại [đơn vị Y]: [kỳ A] vs [kỳ B] là bao nhiêu [đơn vị đo]?”

MINH HỌA MỘT CHUỖI 4 LỚP
- Lớp 1 – Vấn đề kinh doanh: “Lợi nhuận quý này giảm 12% so với quý trước.”
- Lớp 2 – Câu hỏi kinh doanh: “Chi phí nào tăng nhanh nhất và ở khu vực nào?”
- Lớp 3 – Câu hỏi phân tích: “Chi phí nguyên liệu tại chi nhánh Đà Nẵng đã tăng bao nhiêu % trong Q3 so với Q2?”
- Lớp 4 – Câu hỏi thống kê: “Giá vốn hàng bán (COGS) trung bình/đơn hàng tại Đà Nẵng: Q2 vs Q3 là bao nhiêu VNĐ?”

PHÂN LOẠI LOẠI HÌNH CÂU HỎI (thuộc tính của mỗi chuỗi câu hỏi, không phải một lớp)
- Gắn mỗi câu hỏi kinh doanh (và chuỗi câu hỏi đi kèm) với một loại hình: Mô tả (điều gì đã xảy ra?) / Chẩn đoán (vì sao?) / Dự đoán (điều gì có thể xảy ra?) / Đề xuất (nên làm gì?).
- Khuyến khích bộ câu hỏi phủ đủ 4 loại hình nhưng không bắt buộc: nếu với QUYẾT ĐỊNH này một loại hình không cần thiết, bỏ qua và nêu lý do. Ít nhất một câu phải trả lời trực tiếp QUYẾT ĐỊNH.
- Ví dụ dạng câu hỏi kinh doanh theo loại hình:
    • Mô tả: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”
    • Chẩn đoán: “Vì sao [kết quả] ở [phạm vi nào] lại [tăng/giảm]?”
    • Dự đoán: “[Kết quả] sẽ diễn biến thế nào trong [kỳ tới] nếu [điều kiện] giữ nguyên?”
    • Đề xuất: “Nên [hành động nào] với [đối tượng nào] để đạt [mục tiêu] trong [ràng buộc]?”
- Ví dụ dạng câu hỏi thống kê theo loại hình (ngoài dạng Mô tả ở Lớp 4):
    • Chẩn đoán: “Chênh lệch trung bình [cột X] giữa [nhóm 1] và [nhóm 2] là bao nhiêu [đơn vị đo], p-value của kiểm định [t / chi-bình phương] là bao nhiêu?”
    • Dự đoán: “Mô hình [tên] dùng [các cột] dự báo [cột mục tiêu] cho [kỳ tới] có sai số [MAPE/RMSE/AUC] bao nhiêu trên tập kiểm tra [kỳ C]?”
    • Đề xuất: “Với [ràng buộc], giá trị tối ưu của [biến quyết định] là bao nhiêu và [KPI] tăng thêm bao nhiêu [đơn vị đo] so với hiện trạng?”

════════════════════════════════════════
PHẦN B — HAI YÊU CẦU BỔ SUNG
════════════════════════════════════════

BỔ SUNG 1) DỮ LIỆU CẦN THU THẬP THÊM – kiểm tra từng câu hỏi thống kê
- Nếu dữ liệu đang có đã đủ: ghi “Đủ dữ liệu hiện có”.
- Nếu chưa đủ, chỉ rõ: a. tên trường còn thiếu; b. nguồn có thể thu thập; c. mức ưu tiên (Cao/Trung bình/Thấp); d. nếu không thu thập được (dữ liệu công khai), đề xuất biến thay thế hoặc giả định có căn cứ và cách kiểm tra độ nhạy.
- Ví dụ: “Thiếu giá vốn theo sản phẩm – nguồn: phần mềm kế toán hoặc BCTC doanh nghiệp cùng ngành – ưu tiên Cao – nếu không có: giả định biên gộp theo danh mục, kiểm tra độ nhạy ±5 điểm %.”

BỔ SUNG 2) HÀNH ĐỘNG DỰ KIẾN – cho mỗi câu hỏi kinh doanh
- Viết dạng: “Nếu [chỉ số] [>/<] [ngưỡng] thì [hành động A]; ngược lại [hành động B]”. Nếu chưa biết ngưỡng, ghi ngưỡng là tham số cần xác định và cách xác định.
- Ví dụ: “Nếu tỷ lệ giao trễ ở vùng Y > 15% → mở kho vệ tinh tại Y; ngược lại → giữ mạng lưới hiện tại và điều chỉnh cam kết thời gian giao.”

════════════════════════════════════════
QUY TẮC CHO AI
════════════════════════════════════════
- Không bịa trường dữ liệu: chỉ dùng các cột đã liệt kê; mọi trường khác phải đưa vào cột “Dữ liệu cần thu thập thêm”.
- Không trả lời các câu hỏi, không đưa số liệu giả định như thể là kết quả.
- Nếu bối cảnh hoặc dữ liệu chưa đủ để đặt câu hỏi tốt, nêu điểm thiếu ở đầu câu trả lời, rồi vẫn lập bảng với giả định tạm thời được ghi rõ.

════════════════════════════════════════
YÊU CẦU TRÌNH BÀY
════════════════════════════════════════
- 1. Nhắc lại LỚP 1 (Vấn đề kinh doanh) ở đầu câu trả lời, sau đó lập bảng, mỗi dòng 6 cột: [Câu hỏi kinh doanh (đã sắp ưu tiên) | Câu hỏi phân tích | Câu hỏi thống kê | Loại hình câu hỏi | Dữ liệu cần thu thập thêm (nếu có) | Hành động dự kiến].
- 2. Dưới bảng: (a) CÂU HỎI QUYẾT ĐỊNH CHỐT, viết trong một câu; (b) tự kiểm tra: số câu theo từng loại hình, số câu thống kê “Đủ dữ liệu hiện có”, các câu phải dựa vào giả định; (c) đánh giá mức khả thi của đề tài với dữ liệu hiện có (Cao/Trung bình/Thấp) và lý do.
```

## Chủ đề 14: Mô hình định giá bất động sản tự động

```text
VAI TRÒ CỦA AI
Bạn là chuyên gia phân tích kinh doanh, hỗ trợ tôi thực hiện bước S (Specify the question) của mô hình SOAR. Ở bước này chỉ giúp tôi đặt đúng câu hỏi: KHÔNG phân tích dữ liệu, KHÔNG đưa ra số liệu hay kết luận.

BỐI CẢNH
Tôi là Giám đốc đầu tư quỹ bất động sản tại một quỹ bất động sản (bối cảnh theo dữ liệu King County).

LỚP 1) VẤN ĐỀ KINH DOANH – fact đã biết (rộng, có số liệu và mốc so sánh)
“Giá trên mỗi ft² trung vị chênh lệch [__] lần giữa các zipcode; [__]% giao dịch có giá thấp hơn trung vị cùng zipcode quá [__]%.”
Nguồn của fact: price / sqft_living theo zipcode.

QUYẾT ĐỊNH cần đưa ra sau phân tích
“Lập danh sách tối đa 20 căn đưa vào thẩm định thực địa.”
KPI đánh giá quyết định: MAPE; số ứng viên; tỷ lệ ứng viên đạt thẩm định.
Ràng buộc: ngân sách thẩm định 20 căn.

PHẠM VI phân tích
- Chỉ tập trung vào: nhà ở King County, 5/2014–5/2015.
- KHÔNG xét đến: bất động sản thương mại, yếu tố vĩ mô.

DỮ LIỆU TÔI ĐANG CÓ
- Tên bộ dữ liệu/nguồn: House Sales in King County, USA.
- Đơn vị quan sát (mỗi dòng là gì): một giao dịch.
- Quy mô và khung thời gian: 21.613 giao dịch.
- Các cột dữ liệu (ghi đúng tên cột): id, date, price, bedrooms, bathrooms, sqft_living, sqft_lot, floors, waterfront, view, condition, grade, yr_built, yr_renovated, zipcode, lat, long.
- Hạn chế đã biết: không có thông tin pháp lý và nội thất; chỉ một năm dữ liệu.

════════════════════════════════════════
PHẦN A — MÔ HÌNH 4 LỚP CÂU HỎI (phễu thu hẹp: Vấn đề kinh doanh → Câu hỏi kinh doanh → Câu hỏi phân tích → Câu hỏi thống kê)
════════════════════════════════════════
Lớp 1 (Vấn đề kinh doanh) là fact đã nêu ở trên: rộng, mơ hồ, chưa phân tích trực tiếp được. Hãy thu hẹp dần qua các lớp 2–4 dưới đây.

LỚP 2) CÂU HỎI KINH DOANH (thu hẹp phạm vi) – đặt 5–7 câu, sắp xếp theo ưu tiên
- Là câu hỏi mở, ngôn ngữ quản lý, KHÔNG gắn số liệu cụ thể; chỉ nằm trong PHẠM VI.
- Mục đích: định hướng điều tra nguyên nhân của VẤN ĐỀ KINH DOANH và phục vụ QUYẾT ĐỊNH ở trên.
- Ưu tiên = mức ảnh hưởng tới QUYẾT ĐỊNH × khả năng trả lời bằng dữ liệu đang có.
- Ví dụ dạng: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”

LỚP 3) CÂU HỎI PHÂN TÍCH (gắn với dữ liệu) – tương ứng với mỗi câu hỏi kinh doanh
- Chuyển câu hỏi kinh doanh thành yêu cầu đo lường được.
- Phải gắn cụ thể: tên đơn vị/phạm vi, khoảng thời gian so sánh, chỉ số liên quan (kèm định nghĩa công thức).
- Ví dụ dạng: “[Chỉ số X] tại [đơn vị Y] đã thay đổi bao nhiêu % trong [kỳ A] so với [kỳ B]?”

LỚP 4) CÂU HỎI THỐNG KÊ (đo lường cụ thể) – tương ứng với mỗi câu hỏi phân tích
- Là câu hỏi trả lời trực tiếp được bằng một phép tính cụ thể trên dữ liệu, cho ra một con số với đơn vị đo rõ ràng.
- Ghi rõ: (i) các cột sử dụng, đúng tên; (ii) phép tính/kỹ thuật (tổng, trung bình, tỷ lệ, kiểm định, hồi quy, mô hình dự báo, tối ưu hóa, mô phỏng…); (iii) đơn vị đo của kết quả.
- Ví dụ dạng: “[Chỉ số cụ thể] trung bình/tổng tại [đơn vị Y]: [kỳ A] vs [kỳ B] là bao nhiêu [đơn vị đo]?”

MINH HỌA MỘT CHUỖI 4 LỚP
- Lớp 1 – Vấn đề kinh doanh: “Lợi nhuận quý này giảm 12% so với quý trước.”
- Lớp 2 – Câu hỏi kinh doanh: “Chi phí nào tăng nhanh nhất và ở khu vực nào?”
- Lớp 3 – Câu hỏi phân tích: “Chi phí nguyên liệu tại chi nhánh Đà Nẵng đã tăng bao nhiêu % trong Q3 so với Q2?”
- Lớp 4 – Câu hỏi thống kê: “Giá vốn hàng bán (COGS) trung bình/đơn hàng tại Đà Nẵng: Q2 vs Q3 là bao nhiêu VNĐ?”

PHÂN LOẠI LOẠI HÌNH CÂU HỎI (thuộc tính của mỗi chuỗi câu hỏi, không phải một lớp)
- Gắn mỗi câu hỏi kinh doanh (và chuỗi câu hỏi đi kèm) với một loại hình: Mô tả (điều gì đã xảy ra?) / Chẩn đoán (vì sao?) / Dự đoán (điều gì có thể xảy ra?) / Đề xuất (nên làm gì?).
- Khuyến khích bộ câu hỏi phủ đủ 4 loại hình nhưng không bắt buộc: nếu với QUYẾT ĐỊNH này một loại hình không cần thiết, bỏ qua và nêu lý do. Ít nhất một câu phải trả lời trực tiếp QUYẾT ĐỊNH.
- Ví dụ dạng câu hỏi kinh doanh theo loại hình:
    • Mô tả: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”
    • Chẩn đoán: “Vì sao [kết quả] ở [phạm vi nào] lại [tăng/giảm]?”
    • Dự đoán: “[Kết quả] sẽ diễn biến thế nào trong [kỳ tới] nếu [điều kiện] giữ nguyên?”
    • Đề xuất: “Nên [hành động nào] với [đối tượng nào] để đạt [mục tiêu] trong [ràng buộc]?”
- Ví dụ dạng câu hỏi thống kê theo loại hình (ngoài dạng Mô tả ở Lớp 4):
    • Chẩn đoán: “Chênh lệch trung bình [cột X] giữa [nhóm 1] và [nhóm 2] là bao nhiêu [đơn vị đo], p-value của kiểm định [t / chi-bình phương] là bao nhiêu?”
    • Dự đoán: “Mô hình [tên] dùng [các cột] dự báo [cột mục tiêu] cho [kỳ tới] có sai số [MAPE/RMSE/AUC] bao nhiêu trên tập kiểm tra [kỳ C]?”
    • Đề xuất: “Với [ràng buộc], giá trị tối ưu của [biến quyết định] là bao nhiêu và [KPI] tăng thêm bao nhiêu [đơn vị đo] so với hiện trạng?”

════════════════════════════════════════
PHẦN B — HAI YÊU CẦU BỔ SUNG
════════════════════════════════════════

BỔ SUNG 1) DỮ LIỆU CẦN THU THẬP THÊM – kiểm tra từng câu hỏi thống kê
- Nếu dữ liệu đang có đã đủ: ghi “Đủ dữ liệu hiện có”.
- Nếu chưa đủ, chỉ rõ: a. tên trường còn thiếu; b. nguồn có thể thu thập; c. mức ưu tiên (Cao/Trung bình/Thấp); d. nếu không thu thập được (dữ liệu công khai), đề xuất biến thay thế hoặc giả định có căn cứ và cách kiểm tra độ nhạy.
- Ví dụ: “Thiếu giá vốn theo sản phẩm – nguồn: phần mềm kế toán hoặc BCTC doanh nghiệp cùng ngành – ưu tiên Cao – nếu không có: giả định biên gộp theo danh mục, kiểm tra độ nhạy ±5 điểm %.”

BỔ SUNG 2) HÀNH ĐỘNG DỰ KIẾN – cho mỗi câu hỏi kinh doanh
- Viết dạng: “Nếu [chỉ số] [>/<] [ngưỡng] thì [hành động A]; ngược lại [hành động B]”. Nếu chưa biết ngưỡng, ghi ngưỡng là tham số cần xác định và cách xác định.
- Ví dụ: “Nếu tỷ lệ giao trễ ở vùng Y > 15% → mở kho vệ tinh tại Y; ngược lại → giữ mạng lưới hiện tại và điều chỉnh cam kết thời gian giao.”

════════════════════════════════════════
QUY TẮC CHO AI
════════════════════════════════════════
- Không bịa trường dữ liệu: chỉ dùng các cột đã liệt kê; mọi trường khác phải đưa vào cột “Dữ liệu cần thu thập thêm”.
- Không trả lời các câu hỏi, không đưa số liệu giả định như thể là kết quả.
- Nếu bối cảnh hoặc dữ liệu chưa đủ để đặt câu hỏi tốt, nêu điểm thiếu ở đầu câu trả lời, rồi vẫn lập bảng với giả định tạm thời được ghi rõ.

════════════════════════════════════════
YÊU CẦU TRÌNH BÀY
════════════════════════════════════════
- 1. Nhắc lại LỚP 1 (Vấn đề kinh doanh) ở đầu câu trả lời, sau đó lập bảng, mỗi dòng 6 cột: [Câu hỏi kinh doanh (đã sắp ưu tiên) | Câu hỏi phân tích | Câu hỏi thống kê | Loại hình câu hỏi | Dữ liệu cần thu thập thêm (nếu có) | Hành động dự kiến].
- 2. Dưới bảng: (a) CÂU HỎI QUYẾT ĐỊNH CHỐT, viết trong một câu; (b) tự kiểm tra: số câu theo từng loại hình, số câu thống kê “Đủ dữ liệu hiện có”, các câu phải dựa vào giả định; (c) đánh giá mức khả thi của đề tài với dữ liệu hiện có (Cao/Trung bình/Thấp) và lý do.
```

## Chủ đề 15: Moneyball: định giá và tuyển chọn cầu thủ trong ngân sách

```text
VAI TRÒ CỦA AI
Bạn là chuyên gia phân tích kinh doanh, hỗ trợ tôi thực hiện bước S (Specify the question) của mô hình SOAR. Ở bước này chỉ giúp tôi đặt đúng câu hỏi: KHÔNG phân tích dữ liệu, KHÔNG đưa ra số liệu hay kết luận.

BỐI CẢNH
Tôi là Giám đốc thể thao tại một câu lạc bộ bóng đá ngân sách vừa (bối cảnh giả định).

LỚP 1) VẤN ĐỀ KINH DOANH – fact đã biết (rộng, có số liệu và mốc so sánh)
“Mùa trước đội có hiệu số xG [__] nhưng hiệu số bàn thắng [__]; quỹ lương chiếm [__]% doanh thu.”
Nguồn của fact: Understat; báo cáo tài chính câu lạc bộ (nếu có).

QUYẾT ĐỊNH cần đưa ra sau phân tích
“Lập danh sách mục tiêu chuyển nhượng cho kỳ chuyển nhượng tới.”
KPI đánh giá quyết định: đóng góp kỳ vọng trên mỗi đồng chi phí.
Ràng buộc: ngân sách phí [__]; quỹ lương [__]; số suất theo vị trí.

PHẠM VI phân tích
- Chỉ tập trung vào: cầu thủ 5 giải hàng đầu châu Âu, 1–2 mùa gần nhất.
- KHÔNG xét đến: cầu thủ trẻ học viện, thủ môn (nếu thiếu chỉ số).

DỮ LIỆU TÔI ĐANG CÓ
- Tên bộ dữ liệu/nguồn: Football Data from Transfermarkt (Kaggle); Understat.
- Đơn vị quan sát (mỗi dòng là gì): cầu thủ – mùa.
- Quy mô và khung thời gian: [__] cầu thủ.
- Các cột dữ liệu (ghi đúng tên cột): player_id, name, position, date_of_birth, market_value_in_eur, current_club, competition, minutes_played, goals, assists; xG, xA, npxG.
- Hạn chế đã biết: lương thường không công khai; giá trị Transfermarkt là ước tính.

════════════════════════════════════════
PHẦN A — MÔ HÌNH 4 LỚP CÂU HỎI (phễu thu hẹp: Vấn đề kinh doanh → Câu hỏi kinh doanh → Câu hỏi phân tích → Câu hỏi thống kê)
════════════════════════════════════════
Lớp 1 (Vấn đề kinh doanh) là fact đã nêu ở trên: rộng, mơ hồ, chưa phân tích trực tiếp được. Hãy thu hẹp dần qua các lớp 2–4 dưới đây.

LỚP 2) CÂU HỎI KINH DOANH (thu hẹp phạm vi) – đặt 5–7 câu, sắp xếp theo ưu tiên
- Là câu hỏi mở, ngôn ngữ quản lý, KHÔNG gắn số liệu cụ thể; chỉ nằm trong PHẠM VI.
- Mục đích: định hướng điều tra nguyên nhân của VẤN ĐỀ KINH DOANH và phục vụ QUYẾT ĐỊNH ở trên.
- Ưu tiên = mức ảnh hưởng tới QUYẾT ĐỊNH × khả năng trả lời bằng dữ liệu đang có.
- Ví dụ dạng: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”

LỚP 3) CÂU HỎI PHÂN TÍCH (gắn với dữ liệu) – tương ứng với mỗi câu hỏi kinh doanh
- Chuyển câu hỏi kinh doanh thành yêu cầu đo lường được.
- Phải gắn cụ thể: tên đơn vị/phạm vi, khoảng thời gian so sánh, chỉ số liên quan (kèm định nghĩa công thức).
- Ví dụ dạng: “[Chỉ số X] tại [đơn vị Y] đã thay đổi bao nhiêu % trong [kỳ A] so với [kỳ B]?”

LỚP 4) CÂU HỎI THỐNG KÊ (đo lường cụ thể) – tương ứng với mỗi câu hỏi phân tích
- Là câu hỏi trả lời trực tiếp được bằng một phép tính cụ thể trên dữ liệu, cho ra một con số với đơn vị đo rõ ràng.
- Ghi rõ: (i) các cột sử dụng, đúng tên; (ii) phép tính/kỹ thuật (tổng, trung bình, tỷ lệ, kiểm định, hồi quy, mô hình dự báo, tối ưu hóa, mô phỏng…); (iii) đơn vị đo của kết quả.
- Ví dụ dạng: “[Chỉ số cụ thể] trung bình/tổng tại [đơn vị Y]: [kỳ A] vs [kỳ B] là bao nhiêu [đơn vị đo]?”

MINH HỌA MỘT CHUỖI 4 LỚP
- Lớp 1 – Vấn đề kinh doanh: “Lợi nhuận quý này giảm 12% so với quý trước.”
- Lớp 2 – Câu hỏi kinh doanh: “Chi phí nào tăng nhanh nhất và ở khu vực nào?”
- Lớp 3 – Câu hỏi phân tích: “Chi phí nguyên liệu tại chi nhánh Đà Nẵng đã tăng bao nhiêu % trong Q3 so với Q2?”
- Lớp 4 – Câu hỏi thống kê: “Giá vốn hàng bán (COGS) trung bình/đơn hàng tại Đà Nẵng: Q2 vs Q3 là bao nhiêu VNĐ?”

PHÂN LOẠI LOẠI HÌNH CÂU HỎI (thuộc tính của mỗi chuỗi câu hỏi, không phải một lớp)
- Gắn mỗi câu hỏi kinh doanh (và chuỗi câu hỏi đi kèm) với một loại hình: Mô tả (điều gì đã xảy ra?) / Chẩn đoán (vì sao?) / Dự đoán (điều gì có thể xảy ra?) / Đề xuất (nên làm gì?).
- Khuyến khích bộ câu hỏi phủ đủ 4 loại hình nhưng không bắt buộc: nếu với QUYẾT ĐỊNH này một loại hình không cần thiết, bỏ qua và nêu lý do. Ít nhất một câu phải trả lời trực tiếp QUYẾT ĐỊNH.
- Ví dụ dạng câu hỏi kinh doanh theo loại hình:
    • Mô tả: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”
    • Chẩn đoán: “Vì sao [kết quả] ở [phạm vi nào] lại [tăng/giảm]?”
    • Dự đoán: “[Kết quả] sẽ diễn biến thế nào trong [kỳ tới] nếu [điều kiện] giữ nguyên?”
    • Đề xuất: “Nên [hành động nào] với [đối tượng nào] để đạt [mục tiêu] trong [ràng buộc]?”
- Ví dụ dạng câu hỏi thống kê theo loại hình (ngoài dạng Mô tả ở Lớp 4):
    • Chẩn đoán: “Chênh lệch trung bình [cột X] giữa [nhóm 1] và [nhóm 2] là bao nhiêu [đơn vị đo], p-value của kiểm định [t / chi-bình phương] là bao nhiêu?”
    • Dự đoán: “Mô hình [tên] dùng [các cột] dự báo [cột mục tiêu] cho [kỳ tới] có sai số [MAPE/RMSE/AUC] bao nhiêu trên tập kiểm tra [kỳ C]?”
    • Đề xuất: “Với [ràng buộc], giá trị tối ưu của [biến quyết định] là bao nhiêu và [KPI] tăng thêm bao nhiêu [đơn vị đo] so với hiện trạng?”

════════════════════════════════════════
PHẦN B — HAI YÊU CẦU BỔ SUNG
════════════════════════════════════════

BỔ SUNG 1) DỮ LIỆU CẦN THU THẬP THÊM – kiểm tra từng câu hỏi thống kê
- Nếu dữ liệu đang có đã đủ: ghi “Đủ dữ liệu hiện có”.
- Nếu chưa đủ, chỉ rõ: a. tên trường còn thiếu; b. nguồn có thể thu thập; c. mức ưu tiên (Cao/Trung bình/Thấp); d. nếu không thu thập được (dữ liệu công khai), đề xuất biến thay thế hoặc giả định có căn cứ và cách kiểm tra độ nhạy.
- Ví dụ: “Thiếu giá vốn theo sản phẩm – nguồn: phần mềm kế toán hoặc BCTC doanh nghiệp cùng ngành – ưu tiên Cao – nếu không có: giả định biên gộp theo danh mục, kiểm tra độ nhạy ±5 điểm %.”

BỔ SUNG 2) HÀNH ĐỘNG DỰ KIẾN – cho mỗi câu hỏi kinh doanh
- Viết dạng: “Nếu [chỉ số] [>/<] [ngưỡng] thì [hành động A]; ngược lại [hành động B]”. Nếu chưa biết ngưỡng, ghi ngưỡng là tham số cần xác định và cách xác định.
- Ví dụ: “Nếu tỷ lệ giao trễ ở vùng Y > 15% → mở kho vệ tinh tại Y; ngược lại → giữ mạng lưới hiện tại và điều chỉnh cam kết thời gian giao.”

════════════════════════════════════════
QUY TẮC CHO AI
════════════════════════════════════════
- Không bịa trường dữ liệu: chỉ dùng các cột đã liệt kê; mọi trường khác phải đưa vào cột “Dữ liệu cần thu thập thêm”.
- Không trả lời các câu hỏi, không đưa số liệu giả định như thể là kết quả.
- Nếu bối cảnh hoặc dữ liệu chưa đủ để đặt câu hỏi tốt, nêu điểm thiếu ở đầu câu trả lời, rồi vẫn lập bảng với giả định tạm thời được ghi rõ.

════════════════════════════════════════
YÊU CẦU TRÌNH BÀY
════════════════════════════════════════
- 1. Nhắc lại LỚP 1 (Vấn đề kinh doanh) ở đầu câu trả lời, sau đó lập bảng, mỗi dòng 6 cột: [Câu hỏi kinh doanh (đã sắp ưu tiên) | Câu hỏi phân tích | Câu hỏi thống kê | Loại hình câu hỏi | Dữ liệu cần thu thập thêm (nếu có) | Hành động dự kiến].
- 2. Dưới bảng: (a) CÂU HỎI QUYẾT ĐỊNH CHỐT, viết trong một câu; (b) tự kiểm tra: số câu theo từng loại hình, số câu thống kê “Đủ dữ liệu hiện có”, các câu phải dựa vào giả định; (c) đánh giá mức khả thi của đề tài với dữ liệu hiện có (Cao/Trung bình/Thấp) và lý do.
```

## Chủ đề 16: Giữ chân nhân tài: dự báo nghỉ việc và thiết kế can thiệp

```text
VAI TRÒ CỦA AI
Bạn là chuyên gia phân tích kinh doanh, hỗ trợ tôi thực hiện bước S (Specify the question) của mô hình SOAR. Ở bước này chỉ giúp tôi đặt đúng câu hỏi: KHÔNG phân tích dữ liệu, KHÔNG đưa ra số liệu hay kết luận.

BỐI CẢNH
Tôi là Giám đốc Nhân sự tại một công ty (bối cảnh theo dữ liệu hư cấu IBM HR Analytics).

LỚP 1) VẤN ĐỀ KINH DOANH – fact đã biết (rộng, có số liệu và mốc so sánh)
“Tỷ lệ nghỉ việc là [__]%; nhóm làm thêm giờ có tỷ lệ [__]% so với [__]% ở nhóm không làm thêm.”
Nguồn của fact: Attrition theo OverTime.

QUYẾT ĐỊNH cần đưa ra sau phân tích
“Thiết kế chương trình giữ chân và ngân sách cho năm tới.”
KPI đánh giá quyết định: tỷ lệ nghỉ việc; lợi ích ròng của can thiệp.
Ràng buộc: ngân sách tăng lương [__]%; không định danh cá nhân khi báo cáo.

PHẠM VI phân tích
- Chỉ tập trung vào: toàn bộ nhân viên hiện có.
- KHÔNG xét đến: tuyển dụng, đánh giá hiệu suất.

DỮ LIỆU TÔI ĐANG CÓ
- Tên bộ dữ liệu/nguồn: IBM HR Analytics Employee Attrition & Performance.
- Đơn vị quan sát (mỗi dòng là gì): một nhân viên.
- Quy mô và khung thời gian: 1.470 nhân viên.
- Các cột dữ liệu (ghi đúng tên cột): Age, Attrition, BusinessTravel, Department, DistanceFromHome, Education, EnvironmentSatisfaction, JobInvolvement, JobLevel, JobRole, JobSatisfaction, MonthlyIncome, NumCompaniesWorked, OverTime, PercentSalaryHike, PerformanceRating, StockOptionLevel, TotalWorkingYears, TrainingTimesLastYear, WorkLifeBalance, YearsAtCompany, YearsInCurrentRole, YearsSinceLastPromotion.
- Hạn chế đã biết: dữ liệu hư cấu, cắt ngang; không có chi phí thay thế nhân viên.

════════════════════════════════════════
PHẦN A — MÔ HÌNH 4 LỚP CÂU HỎI (phễu thu hẹp: Vấn đề kinh doanh → Câu hỏi kinh doanh → Câu hỏi phân tích → Câu hỏi thống kê)
════════════════════════════════════════
Lớp 1 (Vấn đề kinh doanh) là fact đã nêu ở trên: rộng, mơ hồ, chưa phân tích trực tiếp được. Hãy thu hẹp dần qua các lớp 2–4 dưới đây.

LỚP 2) CÂU HỎI KINH DOANH (thu hẹp phạm vi) – đặt 5–7 câu, sắp xếp theo ưu tiên
- Là câu hỏi mở, ngôn ngữ quản lý, KHÔNG gắn số liệu cụ thể; chỉ nằm trong PHẠM VI.
- Mục đích: định hướng điều tra nguyên nhân của VẤN ĐỀ KINH DOANH và phục vụ QUYẾT ĐỊNH ở trên.
- Ưu tiên = mức ảnh hưởng tới QUYẾT ĐỊNH × khả năng trả lời bằng dữ liệu đang có.
- Ví dụ dạng: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”

LỚP 3) CÂU HỎI PHÂN TÍCH (gắn với dữ liệu) – tương ứng với mỗi câu hỏi kinh doanh
- Chuyển câu hỏi kinh doanh thành yêu cầu đo lường được.
- Phải gắn cụ thể: tên đơn vị/phạm vi, khoảng thời gian so sánh, chỉ số liên quan (kèm định nghĩa công thức).
- Ví dụ dạng: “[Chỉ số X] tại [đơn vị Y] đã thay đổi bao nhiêu % trong [kỳ A] so với [kỳ B]?”

LỚP 4) CÂU HỎI THỐNG KÊ (đo lường cụ thể) – tương ứng với mỗi câu hỏi phân tích
- Là câu hỏi trả lời trực tiếp được bằng một phép tính cụ thể trên dữ liệu, cho ra một con số với đơn vị đo rõ ràng.
- Ghi rõ: (i) các cột sử dụng, đúng tên; (ii) phép tính/kỹ thuật (tổng, trung bình, tỷ lệ, kiểm định, hồi quy, mô hình dự báo, tối ưu hóa, mô phỏng…); (iii) đơn vị đo của kết quả.
- Ví dụ dạng: “[Chỉ số cụ thể] trung bình/tổng tại [đơn vị Y]: [kỳ A] vs [kỳ B] là bao nhiêu [đơn vị đo]?”

MINH HỌA MỘT CHUỖI 4 LỚP
- Lớp 1 – Vấn đề kinh doanh: “Lợi nhuận quý này giảm 12% so với quý trước.”
- Lớp 2 – Câu hỏi kinh doanh: “Chi phí nào tăng nhanh nhất và ở khu vực nào?”
- Lớp 3 – Câu hỏi phân tích: “Chi phí nguyên liệu tại chi nhánh Đà Nẵng đã tăng bao nhiêu % trong Q3 so với Q2?”
- Lớp 4 – Câu hỏi thống kê: “Giá vốn hàng bán (COGS) trung bình/đơn hàng tại Đà Nẵng: Q2 vs Q3 là bao nhiêu VNĐ?”

PHÂN LOẠI LOẠI HÌNH CÂU HỎI (thuộc tính của mỗi chuỗi câu hỏi, không phải một lớp)
- Gắn mỗi câu hỏi kinh doanh (và chuỗi câu hỏi đi kèm) với một loại hình: Mô tả (điều gì đã xảy ra?) / Chẩn đoán (vì sao?) / Dự đoán (điều gì có thể xảy ra?) / Đề xuất (nên làm gì?).
- Khuyến khích bộ câu hỏi phủ đủ 4 loại hình nhưng không bắt buộc: nếu với QUYẾT ĐỊNH này một loại hình không cần thiết, bỏ qua và nêu lý do. Ít nhất một câu phải trả lời trực tiếp QUYẾT ĐỊNH.
- Ví dụ dạng câu hỏi kinh doanh theo loại hình:
    • Mô tả: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”
    • Chẩn đoán: “Vì sao [kết quả] ở [phạm vi nào] lại [tăng/giảm]?”
    • Dự đoán: “[Kết quả] sẽ diễn biến thế nào trong [kỳ tới] nếu [điều kiện] giữ nguyên?”
    • Đề xuất: “Nên [hành động nào] với [đối tượng nào] để đạt [mục tiêu] trong [ràng buộc]?”
- Ví dụ dạng câu hỏi thống kê theo loại hình (ngoài dạng Mô tả ở Lớp 4):
    • Chẩn đoán: “Chênh lệch trung bình [cột X] giữa [nhóm 1] và [nhóm 2] là bao nhiêu [đơn vị đo], p-value của kiểm định [t / chi-bình phương] là bao nhiêu?”
    • Dự đoán: “Mô hình [tên] dùng [các cột] dự báo [cột mục tiêu] cho [kỳ tới] có sai số [MAPE/RMSE/AUC] bao nhiêu trên tập kiểm tra [kỳ C]?”
    • Đề xuất: “Với [ràng buộc], giá trị tối ưu của [biến quyết định] là bao nhiêu và [KPI] tăng thêm bao nhiêu [đơn vị đo] so với hiện trạng?”

════════════════════════════════════════
PHẦN B — HAI YÊU CẦU BỔ SUNG
════════════════════════════════════════

BỔ SUNG 1) DỮ LIỆU CẦN THU THẬP THÊM – kiểm tra từng câu hỏi thống kê
- Nếu dữ liệu đang có đã đủ: ghi “Đủ dữ liệu hiện có”.
- Nếu chưa đủ, chỉ rõ: a. tên trường còn thiếu; b. nguồn có thể thu thập; c. mức ưu tiên (Cao/Trung bình/Thấp); d. nếu không thu thập được (dữ liệu công khai), đề xuất biến thay thế hoặc giả định có căn cứ và cách kiểm tra độ nhạy.
- Ví dụ: “Thiếu giá vốn theo sản phẩm – nguồn: phần mềm kế toán hoặc BCTC doanh nghiệp cùng ngành – ưu tiên Cao – nếu không có: giả định biên gộp theo danh mục, kiểm tra độ nhạy ±5 điểm %.”

BỔ SUNG 2) HÀNH ĐỘNG DỰ KIẾN – cho mỗi câu hỏi kinh doanh
- Viết dạng: “Nếu [chỉ số] [>/<] [ngưỡng] thì [hành động A]; ngược lại [hành động B]”. Nếu chưa biết ngưỡng, ghi ngưỡng là tham số cần xác định và cách xác định.
- Ví dụ: “Nếu tỷ lệ giao trễ ở vùng Y > 15% → mở kho vệ tinh tại Y; ngược lại → giữ mạng lưới hiện tại và điều chỉnh cam kết thời gian giao.”

════════════════════════════════════════
QUY TẮC CHO AI
════════════════════════════════════════
- Không bịa trường dữ liệu: chỉ dùng các cột đã liệt kê; mọi trường khác phải đưa vào cột “Dữ liệu cần thu thập thêm”.
- Không trả lời các câu hỏi, không đưa số liệu giả định như thể là kết quả.
- Nếu bối cảnh hoặc dữ liệu chưa đủ để đặt câu hỏi tốt, nêu điểm thiếu ở đầu câu trả lời, rồi vẫn lập bảng với giả định tạm thời được ghi rõ.

════════════════════════════════════════
YÊU CẦU TRÌNH BÀY
════════════════════════════════════════
- 1. Nhắc lại LỚP 1 (Vấn đề kinh doanh) ở đầu câu trả lời, sau đó lập bảng, mỗi dòng 6 cột: [Câu hỏi kinh doanh (đã sắp ưu tiên) | Câu hỏi phân tích | Câu hỏi thống kê | Loại hình câu hỏi | Dữ liệu cần thu thập thêm (nếu có) | Hành động dự kiến].
- 2. Dưới bảng: (a) CÂU HỎI QUYẾT ĐỊNH CHỐT, viết trong một câu; (b) tự kiểm tra: số câu theo từng loại hình, số câu thống kê “Đủ dữ liệu hiện có”, các câu phải dựa vào giả định; (c) đánh giá mức khả thi của đề tài với dữ liệu hiện có (Cao/Trung bình/Thấp) và lý do.
```

## Chủ đề 17: Dự báo nhu cầu và chính sách tồn kho

```text
VAI TRÒ CỦA AI
Bạn là chuyên gia phân tích kinh doanh, hỗ trợ tôi thực hiện bước S (Specify the question) của mô hình SOAR. Ở bước này chỉ giúp tôi đặt đúng câu hỏi: KHÔNG phân tích dữ liệu, KHÔNG đưa ra số liệu hay kết luận.

BỐI CẢNH
Tôi là Giám đốc chuỗi cung ứng tại một chuỗi bán lẻ (bối cảnh theo dữ liệu M5 – Walmart).

LỚP 1) VẤN ĐỀ KINH DOANH – fact đã biết (rộng, có số liệu và mốc so sánh)
“Ở cửa hàng [__], [__]% SKU nhóm FOODS có ít nhất 7 ngày liên tiếp bán bằng 0 dù bình thường bán trên [__] đơn vị/ngày (dấu hiệu hết hàng).”
Nguồn của fact: chuỗi doanh số ngày d_1…d_1941 theo item_id.

QUYẾT ĐỊNH cần đưa ra sau phân tích
“Ban hành chính sách đặt hàng cho nhóm FOODS tại một cửa hàng cho quý tới.”
KPI đánh giá quyết định: mức phục vụ; tồn kho bình quân; chi phí tồn kho.
Ràng buộc: mức phục vụ ≥ 95%; lead time [__] ngày.

PHẠM VI phân tích
- Chỉ tập trung vào: một cửa hàng, cat_id = FOODS.
- KHÔNG xét đến: nhóm HOBBIES, HOUSEHOLD và các cửa hàng khác.

DỮ LIỆU TÔI ĐANG CÓ
- Tên bộ dữ liệu/nguồn: M5 Forecasting – Accuracy (Kaggle).
- Đơn vị quan sát (mỗi dòng là gì): sản phẩm – cửa hàng – ngày.
- Quy mô và khung thời gian: 3.049 sản phẩm, 10 cửa hàng, 2011–2016.
- Các cột dữ liệu (ghi đúng tên cột): sales: item_id, dept_id, cat_id, store_id, state_id, d_1…d_1941; calendar: date, wm_yr_wk, weekday, event_name_1, event_type_1, snap_CA, snap_TX, snap_WI; sell_prices: store_id, item_id, wm_yr_wk, sell_price.
- Hạn chế đã biết: không có tồn kho, lead time và chi phí.

════════════════════════════════════════
PHẦN A — MÔ HÌNH 4 LỚP CÂU HỎI (phễu thu hẹp: Vấn đề kinh doanh → Câu hỏi kinh doanh → Câu hỏi phân tích → Câu hỏi thống kê)
════════════════════════════════════════
Lớp 1 (Vấn đề kinh doanh) là fact đã nêu ở trên: rộng, mơ hồ, chưa phân tích trực tiếp được. Hãy thu hẹp dần qua các lớp 2–4 dưới đây.

LỚP 2) CÂU HỎI KINH DOANH (thu hẹp phạm vi) – đặt 5–7 câu, sắp xếp theo ưu tiên
- Là câu hỏi mở, ngôn ngữ quản lý, KHÔNG gắn số liệu cụ thể; chỉ nằm trong PHẠM VI.
- Mục đích: định hướng điều tra nguyên nhân của VẤN ĐỀ KINH DOANH và phục vụ QUYẾT ĐỊNH ở trên.
- Ưu tiên = mức ảnh hưởng tới QUYẾT ĐỊNH × khả năng trả lời bằng dữ liệu đang có.
- Ví dụ dạng: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”

LỚP 3) CÂU HỎI PHÂN TÍCH (gắn với dữ liệu) – tương ứng với mỗi câu hỏi kinh doanh
- Chuyển câu hỏi kinh doanh thành yêu cầu đo lường được.
- Phải gắn cụ thể: tên đơn vị/phạm vi, khoảng thời gian so sánh, chỉ số liên quan (kèm định nghĩa công thức).
- Ví dụ dạng: “[Chỉ số X] tại [đơn vị Y] đã thay đổi bao nhiêu % trong [kỳ A] so với [kỳ B]?”

LỚP 4) CÂU HỎI THỐNG KÊ (đo lường cụ thể) – tương ứng với mỗi câu hỏi phân tích
- Là câu hỏi trả lời trực tiếp được bằng một phép tính cụ thể trên dữ liệu, cho ra một con số với đơn vị đo rõ ràng.
- Ghi rõ: (i) các cột sử dụng, đúng tên; (ii) phép tính/kỹ thuật (tổng, trung bình, tỷ lệ, kiểm định, hồi quy, mô hình dự báo, tối ưu hóa, mô phỏng…); (iii) đơn vị đo của kết quả.
- Ví dụ dạng: “[Chỉ số cụ thể] trung bình/tổng tại [đơn vị Y]: [kỳ A] vs [kỳ B] là bao nhiêu [đơn vị đo]?”

MINH HỌA MỘT CHUỖI 4 LỚP
- Lớp 1 – Vấn đề kinh doanh: “Lợi nhuận quý này giảm 12% so với quý trước.”
- Lớp 2 – Câu hỏi kinh doanh: “Chi phí nào tăng nhanh nhất và ở khu vực nào?”
- Lớp 3 – Câu hỏi phân tích: “Chi phí nguyên liệu tại chi nhánh Đà Nẵng đã tăng bao nhiêu % trong Q3 so với Q2?”
- Lớp 4 – Câu hỏi thống kê: “Giá vốn hàng bán (COGS) trung bình/đơn hàng tại Đà Nẵng: Q2 vs Q3 là bao nhiêu VNĐ?”

PHÂN LOẠI LOẠI HÌNH CÂU HỎI (thuộc tính của mỗi chuỗi câu hỏi, không phải một lớp)
- Gắn mỗi câu hỏi kinh doanh (và chuỗi câu hỏi đi kèm) với một loại hình: Mô tả (điều gì đã xảy ra?) / Chẩn đoán (vì sao?) / Dự đoán (điều gì có thể xảy ra?) / Đề xuất (nên làm gì?).
- Khuyến khích bộ câu hỏi phủ đủ 4 loại hình nhưng không bắt buộc: nếu với QUYẾT ĐỊNH này một loại hình không cần thiết, bỏ qua và nêu lý do. Ít nhất một câu phải trả lời trực tiếp QUYẾT ĐỊNH.
- Ví dụ dạng câu hỏi kinh doanh theo loại hình:
    • Mô tả: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”
    • Chẩn đoán: “Vì sao [kết quả] ở [phạm vi nào] lại [tăng/giảm]?”
    • Dự đoán: “[Kết quả] sẽ diễn biến thế nào trong [kỳ tới] nếu [điều kiện] giữ nguyên?”
    • Đề xuất: “Nên [hành động nào] với [đối tượng nào] để đạt [mục tiêu] trong [ràng buộc]?”
- Ví dụ dạng câu hỏi thống kê theo loại hình (ngoài dạng Mô tả ở Lớp 4):
    • Chẩn đoán: “Chênh lệch trung bình [cột X] giữa [nhóm 1] và [nhóm 2] là bao nhiêu [đơn vị đo], p-value của kiểm định [t / chi-bình phương] là bao nhiêu?”
    • Dự đoán: “Mô hình [tên] dùng [các cột] dự báo [cột mục tiêu] cho [kỳ tới] có sai số [MAPE/RMSE/AUC] bao nhiêu trên tập kiểm tra [kỳ C]?”
    • Đề xuất: “Với [ràng buộc], giá trị tối ưu của [biến quyết định] là bao nhiêu và [KPI] tăng thêm bao nhiêu [đơn vị đo] so với hiện trạng?”

════════════════════════════════════════
PHẦN B — HAI YÊU CẦU BỔ SUNG
════════════════════════════════════════

BỔ SUNG 1) DỮ LIỆU CẦN THU THẬP THÊM – kiểm tra từng câu hỏi thống kê
- Nếu dữ liệu đang có đã đủ: ghi “Đủ dữ liệu hiện có”.
- Nếu chưa đủ, chỉ rõ: a. tên trường còn thiếu; b. nguồn có thể thu thập; c. mức ưu tiên (Cao/Trung bình/Thấp); d. nếu không thu thập được (dữ liệu công khai), đề xuất biến thay thế hoặc giả định có căn cứ và cách kiểm tra độ nhạy.
- Ví dụ: “Thiếu giá vốn theo sản phẩm – nguồn: phần mềm kế toán hoặc BCTC doanh nghiệp cùng ngành – ưu tiên Cao – nếu không có: giả định biên gộp theo danh mục, kiểm tra độ nhạy ±5 điểm %.”

BỔ SUNG 2) HÀNH ĐỘNG DỰ KIẾN – cho mỗi câu hỏi kinh doanh
- Viết dạng: “Nếu [chỉ số] [>/<] [ngưỡng] thì [hành động A]; ngược lại [hành động B]”. Nếu chưa biết ngưỡng, ghi ngưỡng là tham số cần xác định và cách xác định.
- Ví dụ: “Nếu tỷ lệ giao trễ ở vùng Y > 15% → mở kho vệ tinh tại Y; ngược lại → giữ mạng lưới hiện tại và điều chỉnh cam kết thời gian giao.”

════════════════════════════════════════
QUY TẮC CHO AI
════════════════════════════════════════
- Không bịa trường dữ liệu: chỉ dùng các cột đã liệt kê; mọi trường khác phải đưa vào cột “Dữ liệu cần thu thập thêm”.
- Không trả lời các câu hỏi, không đưa số liệu giả định như thể là kết quả.
- Nếu bối cảnh hoặc dữ liệu chưa đủ để đặt câu hỏi tốt, nêu điểm thiếu ở đầu câu trả lời, rồi vẫn lập bảng với giả định tạm thời được ghi rõ.

════════════════════════════════════════
YÊU CẦU TRÌNH BÀY
════════════════════════════════════════
- 1. Nhắc lại LỚP 1 (Vấn đề kinh doanh) ở đầu câu trả lời, sau đó lập bảng, mỗi dòng 6 cột: [Câu hỏi kinh doanh (đã sắp ưu tiên) | Câu hỏi phân tích | Câu hỏi thống kê | Loại hình câu hỏi | Dữ liệu cần thu thập thêm (nếu có) | Hành động dự kiến].
- 2. Dưới bảng: (a) CÂU HỎI QUYẾT ĐỊNH CHỐT, viết trong một câu; (b) tự kiểm tra: số câu theo từng loại hình, số câu thống kê “Đủ dữ liệu hiện có”, các câu phải dựa vào giả định; (c) đánh giá mức khả thi của đề tài với dữ liệu hiện có (Cao/Trung bình/Thấp) và lý do.
```

## Chủ đề 18: Giao hàng đúng hẹn và tối ưu tuyến đường

```text
VAI TRÒ CỦA AI
Bạn là chuyên gia phân tích kinh doanh, hỗ trợ tôi thực hiện bước S (Specify the question) của mô hình SOAR. Ở bước này chỉ giúp tôi đặt đúng câu hỏi: KHÔNG phân tích dữ liệu, KHÔNG đưa ra số liệu hay kết luận.

BỐI CẢNH
Tôi là Giám đốc Logistics tại một công ty phân phối (bối cảnh theo dữ liệu DataCo).

LỚP 1) VẤN ĐỀ KINH DOANH – fact đã biết (rộng, có số liệu và mốc so sánh)
“[__]% đơn hàng giao trễ; riêng phương thức First Class trễ [__]% và Second Class trễ [__]%.”
Nguồn của fact: Late_delivery_risk theo Shipping Mode.

QUYẾT ĐỊNH cần đưa ra sau phân tích
“Điều chỉnh cam kết thời gian giao theo phương thức và vùng, và chọn phương án xếp tuyến giao hàng nội thành.”
KPI đánh giá quyết định: tỷ lệ trễ; tổng quãng đường; chi phí nhiên liệu.
Ràng buộc: số xe [__]; sức chở mỗi xe [__].

PHẠM VI phân tích
- Chỉ tập trung vào: toàn bộ đơn trong dữ liệu; bài toán tuyến trên bộ Solomon.
- KHÔNG xét đến: chọn nhà vận chuyển, định giá phí giao hàng.

DỮ LIỆU TÔI ĐANG CÓ
- Tên bộ dữ liệu/nguồn: DataCo Smart Supply Chain; Solomon VRPTW instances.
- Đơn vị quan sát (mỗi dòng là gì): một dòng đơn hàng.
- Quy mô và khung thời gian: khoảng 180 nghìn dòng.
- Các cột dữ liệu (ghi đúng tên cột): order date (DateOrders), Days for shipment (scheduled), Days for shipping (real), Delivery Status, Late_delivery_risk, Shipping Mode, Order Region, Order Country, Order City, Category Name, Sales, Latitude, Longitude.
- Hạn chế đã biết: không có tuyến xe; Days for shipping (real) và Delivery Status là kết quả, không dùng làm biến dự báo.

════════════════════════════════════════
PHẦN A — MÔ HÌNH 4 LỚP CÂU HỎI (phễu thu hẹp: Vấn đề kinh doanh → Câu hỏi kinh doanh → Câu hỏi phân tích → Câu hỏi thống kê)
════════════════════════════════════════
Lớp 1 (Vấn đề kinh doanh) là fact đã nêu ở trên: rộng, mơ hồ, chưa phân tích trực tiếp được. Hãy thu hẹp dần qua các lớp 2–4 dưới đây.

LỚP 2) CÂU HỎI KINH DOANH (thu hẹp phạm vi) – đặt 5–7 câu, sắp xếp theo ưu tiên
- Là câu hỏi mở, ngôn ngữ quản lý, KHÔNG gắn số liệu cụ thể; chỉ nằm trong PHẠM VI.
- Mục đích: định hướng điều tra nguyên nhân của VẤN ĐỀ KINH DOANH và phục vụ QUYẾT ĐỊNH ở trên.
- Ưu tiên = mức ảnh hưởng tới QUYẾT ĐỊNH × khả năng trả lời bằng dữ liệu đang có.
- Ví dụ dạng: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”

LỚP 3) CÂU HỎI PHÂN TÍCH (gắn với dữ liệu) – tương ứng với mỗi câu hỏi kinh doanh
- Chuyển câu hỏi kinh doanh thành yêu cầu đo lường được.
- Phải gắn cụ thể: tên đơn vị/phạm vi, khoảng thời gian so sánh, chỉ số liên quan (kèm định nghĩa công thức).
- Ví dụ dạng: “[Chỉ số X] tại [đơn vị Y] đã thay đổi bao nhiêu % trong [kỳ A] so với [kỳ B]?”

LỚP 4) CÂU HỎI THỐNG KÊ (đo lường cụ thể) – tương ứng với mỗi câu hỏi phân tích
- Là câu hỏi trả lời trực tiếp được bằng một phép tính cụ thể trên dữ liệu, cho ra một con số với đơn vị đo rõ ràng.
- Ghi rõ: (i) các cột sử dụng, đúng tên; (ii) phép tính/kỹ thuật (tổng, trung bình, tỷ lệ, kiểm định, hồi quy, mô hình dự báo, tối ưu hóa, mô phỏng…); (iii) đơn vị đo của kết quả.
- Ví dụ dạng: “[Chỉ số cụ thể] trung bình/tổng tại [đơn vị Y]: [kỳ A] vs [kỳ B] là bao nhiêu [đơn vị đo]?”

MINH HỌA MỘT CHUỖI 4 LỚP
- Lớp 1 – Vấn đề kinh doanh: “Lợi nhuận quý này giảm 12% so với quý trước.”
- Lớp 2 – Câu hỏi kinh doanh: “Chi phí nào tăng nhanh nhất và ở khu vực nào?”
- Lớp 3 – Câu hỏi phân tích: “Chi phí nguyên liệu tại chi nhánh Đà Nẵng đã tăng bao nhiêu % trong Q3 so với Q2?”
- Lớp 4 – Câu hỏi thống kê: “Giá vốn hàng bán (COGS) trung bình/đơn hàng tại Đà Nẵng: Q2 vs Q3 là bao nhiêu VNĐ?”

PHÂN LOẠI LOẠI HÌNH CÂU HỎI (thuộc tính của mỗi chuỗi câu hỏi, không phải một lớp)
- Gắn mỗi câu hỏi kinh doanh (và chuỗi câu hỏi đi kèm) với một loại hình: Mô tả (điều gì đã xảy ra?) / Chẩn đoán (vì sao?) / Dự đoán (điều gì có thể xảy ra?) / Đề xuất (nên làm gì?).
- Khuyến khích bộ câu hỏi phủ đủ 4 loại hình nhưng không bắt buộc: nếu với QUYẾT ĐỊNH này một loại hình không cần thiết, bỏ qua và nêu lý do. Ít nhất một câu phải trả lời trực tiếp QUYẾT ĐỊNH.
- Ví dụ dạng câu hỏi kinh doanh theo loại hình:
    • Mô tả: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”
    • Chẩn đoán: “Vì sao [kết quả] ở [phạm vi nào] lại [tăng/giảm]?”
    • Dự đoán: “[Kết quả] sẽ diễn biến thế nào trong [kỳ tới] nếu [điều kiện] giữ nguyên?”
    • Đề xuất: “Nên [hành động nào] với [đối tượng nào] để đạt [mục tiêu] trong [ràng buộc]?”
- Ví dụ dạng câu hỏi thống kê theo loại hình (ngoài dạng Mô tả ở Lớp 4):
    • Chẩn đoán: “Chênh lệch trung bình [cột X] giữa [nhóm 1] và [nhóm 2] là bao nhiêu [đơn vị đo], p-value của kiểm định [t / chi-bình phương] là bao nhiêu?”
    • Dự đoán: “Mô hình [tên] dùng [các cột] dự báo [cột mục tiêu] cho [kỳ tới] có sai số [MAPE/RMSE/AUC] bao nhiêu trên tập kiểm tra [kỳ C]?”
    • Đề xuất: “Với [ràng buộc], giá trị tối ưu của [biến quyết định] là bao nhiêu và [KPI] tăng thêm bao nhiêu [đơn vị đo] so với hiện trạng?”

════════════════════════════════════════
PHẦN B — HAI YÊU CẦU BỔ SUNG
════════════════════════════════════════

BỔ SUNG 1) DỮ LIỆU CẦN THU THẬP THÊM – kiểm tra từng câu hỏi thống kê
- Nếu dữ liệu đang có đã đủ: ghi “Đủ dữ liệu hiện có”.
- Nếu chưa đủ, chỉ rõ: a. tên trường còn thiếu; b. nguồn có thể thu thập; c. mức ưu tiên (Cao/Trung bình/Thấp); d. nếu không thu thập được (dữ liệu công khai), đề xuất biến thay thế hoặc giả định có căn cứ và cách kiểm tra độ nhạy.
- Ví dụ: “Thiếu giá vốn theo sản phẩm – nguồn: phần mềm kế toán hoặc BCTC doanh nghiệp cùng ngành – ưu tiên Cao – nếu không có: giả định biên gộp theo danh mục, kiểm tra độ nhạy ±5 điểm %.”

BỔ SUNG 2) HÀNH ĐỘNG DỰ KIẾN – cho mỗi câu hỏi kinh doanh
- Viết dạng: “Nếu [chỉ số] [>/<] [ngưỡng] thì [hành động A]; ngược lại [hành động B]”. Nếu chưa biết ngưỡng, ghi ngưỡng là tham số cần xác định và cách xác định.
- Ví dụ: “Nếu tỷ lệ giao trễ ở vùng Y > 15% → mở kho vệ tinh tại Y; ngược lại → giữ mạng lưới hiện tại và điều chỉnh cam kết thời gian giao.”

════════════════════════════════════════
QUY TẮC CHO AI
════════════════════════════════════════
- Không bịa trường dữ liệu: chỉ dùng các cột đã liệt kê; mọi trường khác phải đưa vào cột “Dữ liệu cần thu thập thêm”.
- Không trả lời các câu hỏi, không đưa số liệu giả định như thể là kết quả.
- Nếu bối cảnh hoặc dữ liệu chưa đủ để đặt câu hỏi tốt, nêu điểm thiếu ở đầu câu trả lời, rồi vẫn lập bảng với giả định tạm thời được ghi rõ.

════════════════════════════════════════
YÊU CẦU TRÌNH BÀY
════════════════════════════════════════
- 1. Nhắc lại LỚP 1 (Vấn đề kinh doanh) ở đầu câu trả lời, sau đó lập bảng, mỗi dòng 6 cột: [Câu hỏi kinh doanh (đã sắp ưu tiên) | Câu hỏi phân tích | Câu hỏi thống kê | Loại hình câu hỏi | Dữ liệu cần thu thập thêm (nếu có) | Hành động dự kiến].
- 2. Dưới bảng: (a) CÂU HỎI QUYẾT ĐỊNH CHỐT, viết trong một câu; (b) tự kiểm tra: số câu theo từng loại hình, số câu thống kê “Đủ dữ liệu hiện có”, các câu phải dựa vào giả định; (c) đánh giá mức khả thi của đề tài với dữ liệu hiện có (Cao/Trung bình/Thấp) và lý do.
```

## Chủ đề 19: Bảo trì dự đoán dựa trên cảm biến

```text
VAI TRÒ CỦA AI
Bạn là chuyên gia phân tích kinh doanh, hỗ trợ tôi thực hiện bước S (Specify the question) của mô hình SOAR. Ở bước này chỉ giúp tôi đặt đúng câu hỏi: KHÔNG phân tích dữ liệu, KHÔNG đưa ra số liệu hay kết luận.

BỐI CẢNH
Tôi là Giám đốc sản xuất tại một nhà máy có 100 máy (bối cảnh theo dữ liệu Azure Predictive Maintenance).

LỚP 1) VẤN ĐỀ KINH DOANH – fact đã biết (rộng, có số liệu và mốc so sánh)
“Năm qua có [__] lần hỏng đột xuất, [__]% trong đó ở linh kiện comp[__]; thời gian từ lần bảo trì gần nhất đến khi hỏng trung bình [__] ngày.”
Nguồn của fact: bảng failures và maint.

QUYẾT ĐỊNH cần đưa ra sau phân tích
“Đặt ngưỡng cảnh báo và lịch bảo trì cho năm tới.”
KPI đánh giá quyết định: chi phí bảo trì/máy/năm; availability.
Ràng buộc: số đội bảo trì [__] mỗi ca.

PHẠM VI phân tích
- Chỉ tập trung vào: 100 máy, 4 linh kiện.
- KHÔNG xét đến: đầu tư máy mới.

DỮ LIỆU TÔI ĐANG CÓ
- Tên bộ dữ liệu/nguồn: Microsoft Azure Predictive Maintenance.
- Đơn vị quan sát (mỗi dòng là gì): máy – giờ (telemetry) và các bảng sự kiện.
- Quy mô và khung thời gian: năm 2015.
- Các cột dữ liệu (ghi đúng tên cột): telemetry: datetime, machineID, volt, rotate, pressure, vibration; errors: errorID; maint: comp; failures: failure; machines: model, age.
- Hạn chế đã biết: dữ liệu mô phỏng; không có chi phí.

════════════════════════════════════════
PHẦN A — MÔ HÌNH 4 LỚP CÂU HỎI (phễu thu hẹp: Vấn đề kinh doanh → Câu hỏi kinh doanh → Câu hỏi phân tích → Câu hỏi thống kê)
════════════════════════════════════════
Lớp 1 (Vấn đề kinh doanh) là fact đã nêu ở trên: rộng, mơ hồ, chưa phân tích trực tiếp được. Hãy thu hẹp dần qua các lớp 2–4 dưới đây.

LỚP 2) CÂU HỎI KINH DOANH (thu hẹp phạm vi) – đặt 5–7 câu, sắp xếp theo ưu tiên
- Là câu hỏi mở, ngôn ngữ quản lý, KHÔNG gắn số liệu cụ thể; chỉ nằm trong PHẠM VI.
- Mục đích: định hướng điều tra nguyên nhân của VẤN ĐỀ KINH DOANH và phục vụ QUYẾT ĐỊNH ở trên.
- Ưu tiên = mức ảnh hưởng tới QUYẾT ĐỊNH × khả năng trả lời bằng dữ liệu đang có.
- Ví dụ dạng: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”

LỚP 3) CÂU HỎI PHÂN TÍCH (gắn với dữ liệu) – tương ứng với mỗi câu hỏi kinh doanh
- Chuyển câu hỏi kinh doanh thành yêu cầu đo lường được.
- Phải gắn cụ thể: tên đơn vị/phạm vi, khoảng thời gian so sánh, chỉ số liên quan (kèm định nghĩa công thức).
- Ví dụ dạng: “[Chỉ số X] tại [đơn vị Y] đã thay đổi bao nhiêu % trong [kỳ A] so với [kỳ B]?”

LỚP 4) CÂU HỎI THỐNG KÊ (đo lường cụ thể) – tương ứng với mỗi câu hỏi phân tích
- Là câu hỏi trả lời trực tiếp được bằng một phép tính cụ thể trên dữ liệu, cho ra một con số với đơn vị đo rõ ràng.
- Ghi rõ: (i) các cột sử dụng, đúng tên; (ii) phép tính/kỹ thuật (tổng, trung bình, tỷ lệ, kiểm định, hồi quy, mô hình dự báo, tối ưu hóa, mô phỏng…); (iii) đơn vị đo của kết quả.
- Ví dụ dạng: “[Chỉ số cụ thể] trung bình/tổng tại [đơn vị Y]: [kỳ A] vs [kỳ B] là bao nhiêu [đơn vị đo]?”

MINH HỌA MỘT CHUỖI 4 LỚP
- Lớp 1 – Vấn đề kinh doanh: “Lợi nhuận quý này giảm 12% so với quý trước.”
- Lớp 2 – Câu hỏi kinh doanh: “Chi phí nào tăng nhanh nhất và ở khu vực nào?”
- Lớp 3 – Câu hỏi phân tích: “Chi phí nguyên liệu tại chi nhánh Đà Nẵng đã tăng bao nhiêu % trong Q3 so với Q2?”
- Lớp 4 – Câu hỏi thống kê: “Giá vốn hàng bán (COGS) trung bình/đơn hàng tại Đà Nẵng: Q2 vs Q3 là bao nhiêu VNĐ?”

PHÂN LOẠI LOẠI HÌNH CÂU HỎI (thuộc tính của mỗi chuỗi câu hỏi, không phải một lớp)
- Gắn mỗi câu hỏi kinh doanh (và chuỗi câu hỏi đi kèm) với một loại hình: Mô tả (điều gì đã xảy ra?) / Chẩn đoán (vì sao?) / Dự đoán (điều gì có thể xảy ra?) / Đề xuất (nên làm gì?).
- Khuyến khích bộ câu hỏi phủ đủ 4 loại hình nhưng không bắt buộc: nếu với QUYẾT ĐỊNH này một loại hình không cần thiết, bỏ qua và nêu lý do. Ít nhất một câu phải trả lời trực tiếp QUYẾT ĐỊNH.
- Ví dụ dạng câu hỏi kinh doanh theo loại hình:
    • Mô tả: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”
    • Chẩn đoán: “Vì sao [kết quả] ở [phạm vi nào] lại [tăng/giảm]?”
    • Dự đoán: “[Kết quả] sẽ diễn biến thế nào trong [kỳ tới] nếu [điều kiện] giữ nguyên?”
    • Đề xuất: “Nên [hành động nào] với [đối tượng nào] để đạt [mục tiêu] trong [ràng buộc]?”
- Ví dụ dạng câu hỏi thống kê theo loại hình (ngoài dạng Mô tả ở Lớp 4):
    • Chẩn đoán: “Chênh lệch trung bình [cột X] giữa [nhóm 1] và [nhóm 2] là bao nhiêu [đơn vị đo], p-value của kiểm định [t / chi-bình phương] là bao nhiêu?”
    • Dự đoán: “Mô hình [tên] dùng [các cột] dự báo [cột mục tiêu] cho [kỳ tới] có sai số [MAPE/RMSE/AUC] bao nhiêu trên tập kiểm tra [kỳ C]?”
    • Đề xuất: “Với [ràng buộc], giá trị tối ưu của [biến quyết định] là bao nhiêu và [KPI] tăng thêm bao nhiêu [đơn vị đo] so với hiện trạng?”

════════════════════════════════════════
PHẦN B — HAI YÊU CẦU BỔ SUNG
════════════════════════════════════════

BỔ SUNG 1) DỮ LIỆU CẦN THU THẬP THÊM – kiểm tra từng câu hỏi thống kê
- Nếu dữ liệu đang có đã đủ: ghi “Đủ dữ liệu hiện có”.
- Nếu chưa đủ, chỉ rõ: a. tên trường còn thiếu; b. nguồn có thể thu thập; c. mức ưu tiên (Cao/Trung bình/Thấp); d. nếu không thu thập được (dữ liệu công khai), đề xuất biến thay thế hoặc giả định có căn cứ và cách kiểm tra độ nhạy.
- Ví dụ: “Thiếu giá vốn theo sản phẩm – nguồn: phần mềm kế toán hoặc BCTC doanh nghiệp cùng ngành – ưu tiên Cao – nếu không có: giả định biên gộp theo danh mục, kiểm tra độ nhạy ±5 điểm %.”

BỔ SUNG 2) HÀNH ĐỘNG DỰ KIẾN – cho mỗi câu hỏi kinh doanh
- Viết dạng: “Nếu [chỉ số] [>/<] [ngưỡng] thì [hành động A]; ngược lại [hành động B]”. Nếu chưa biết ngưỡng, ghi ngưỡng là tham số cần xác định và cách xác định.
- Ví dụ: “Nếu tỷ lệ giao trễ ở vùng Y > 15% → mở kho vệ tinh tại Y; ngược lại → giữ mạng lưới hiện tại và điều chỉnh cam kết thời gian giao.”

════════════════════════════════════════
QUY TẮC CHO AI
════════════════════════════════════════
- Không bịa trường dữ liệu: chỉ dùng các cột đã liệt kê; mọi trường khác phải đưa vào cột “Dữ liệu cần thu thập thêm”.
- Không trả lời các câu hỏi, không đưa số liệu giả định như thể là kết quả.
- Nếu bối cảnh hoặc dữ liệu chưa đủ để đặt câu hỏi tốt, nêu điểm thiếu ở đầu câu trả lời, rồi vẫn lập bảng với giả định tạm thời được ghi rõ.

════════════════════════════════════════
YÊU CẦU TRÌNH BÀY
════════════════════════════════════════
- 1. Nhắc lại LỚP 1 (Vấn đề kinh doanh) ở đầu câu trả lời, sau đó lập bảng, mỗi dòng 6 cột: [Câu hỏi kinh doanh (đã sắp ưu tiên) | Câu hỏi phân tích | Câu hỏi thống kê | Loại hình câu hỏi | Dữ liệu cần thu thập thêm (nếu có) | Hành động dự kiến].
- 2. Dưới bảng: (a) CÂU HỎI QUYẾT ĐỊNH CHỐT, viết trong một câu; (b) tự kiểm tra: số câu theo từng loại hình, số câu thống kê “Đủ dữ liệu hiện có”, các câu phải dựa vào giả định; (c) đánh giá mức khả thi của đề tài với dữ liệu hiện có (Cao/Trung bình/Thấp) và lý do.
```

## Chủ đề 20: Quản lý chất lượng đào tạo: cảnh báo sớm học viên có nguy cơ

```text
VAI TRÒ CỦA AI
Bạn là chuyên gia phân tích kinh doanh, hỗ trợ tôi thực hiện bước S (Specify the question) của mô hình SOAR. Ở bước này chỉ giúp tôi đặt đúng câu hỏi: KHÔNG phân tích dữ liệu, KHÔNG đưa ra số liệu hay kết luận.

BỐI CẢNH
Tôi là Giám đốc đào tạo trực tuyến tại một chương trình đào tạo trực tuyến (bối cảnh theo dữ liệu OULAD).

LỚP 1) VẤN ĐỀ KINH DOANH – fact đã biết (rộng, có số liệu và mốc so sánh)
“Ở học phần [__], [__]% học viên rút lui, phần lớn trước ngày thứ [__] của khóa; học viên đạt có số lượt click 4 tuần đầu gấp [__] lần học viên rút lui.”
Nguồn của fact: final_result, date_unregistration, sum_click.

QUYẾT ĐỊNH cần đưa ra sau phân tích
“Thiết kế quy trình và ngưỡng cảnh báo sớm cho lượt mở lớp tới.”
KPI đánh giá quyết định: tỷ lệ rút lui; tỷ lệ không đạt; recall của cảnh báo.
Ràng buộc: năng lực cố vấn 50 ca/tuần.

PHẠM VI phân tích
- Chỉ tập trung vào: 1–2 học phần.
- KHÔNG xét đến: thiết kế lại nội dung học phần.

DỮ LIỆU TÔI ĐANG CÓ
- Tên bộ dữ liệu/nguồn: Open University Learning Analytics Dataset (OULAD).
- Đơn vị quan sát (mỗi dòng là gì): nhiều bảng: học viên – học phần, click theo ngày, điểm bài.
- Quy mô và khung thời gian: 32.593 lượt học viên, 2013–2014.
- Các cột dữ liệu (ghi đúng tên cột): studentInfo: code_module, code_presentation, id_student, gender, region, highest_education, imd_band, age_band, num_of_prev_attempts, studied_credits, disability, final_result; studentVle: date, sum_click, id_site; vle: activity_type; studentAssessment: date_submitted, score; assessments: date, weight; studentRegistration: date_registration, date_unregistration.
- Hạn chế đã biết: chỉ được dùng dữ liệu trước mốc dự báo.

════════════════════════════════════════
PHẦN A — MÔ HÌNH 4 LỚP CÂU HỎI (phễu thu hẹp: Vấn đề kinh doanh → Câu hỏi kinh doanh → Câu hỏi phân tích → Câu hỏi thống kê)
════════════════════════════════════════
Lớp 1 (Vấn đề kinh doanh) là fact đã nêu ở trên: rộng, mơ hồ, chưa phân tích trực tiếp được. Hãy thu hẹp dần qua các lớp 2–4 dưới đây.

LỚP 2) CÂU HỎI KINH DOANH (thu hẹp phạm vi) – đặt 5–7 câu, sắp xếp theo ưu tiên
- Là câu hỏi mở, ngôn ngữ quản lý, KHÔNG gắn số liệu cụ thể; chỉ nằm trong PHẠM VI.
- Mục đích: định hướng điều tra nguyên nhân của VẤN ĐỀ KINH DOANH và phục vụ QUYẾT ĐỊNH ở trên.
- Ưu tiên = mức ảnh hưởng tới QUYẾT ĐỊNH × khả năng trả lời bằng dữ liệu đang có.
- Ví dụ dạng: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”

LỚP 3) CÂU HỎI PHÂN TÍCH (gắn với dữ liệu) – tương ứng với mỗi câu hỏi kinh doanh
- Chuyển câu hỏi kinh doanh thành yêu cầu đo lường được.
- Phải gắn cụ thể: tên đơn vị/phạm vi, khoảng thời gian so sánh, chỉ số liên quan (kèm định nghĩa công thức).
- Ví dụ dạng: “[Chỉ số X] tại [đơn vị Y] đã thay đổi bao nhiêu % trong [kỳ A] so với [kỳ B]?”

LỚP 4) CÂU HỎI THỐNG KÊ (đo lường cụ thể) – tương ứng với mỗi câu hỏi phân tích
- Là câu hỏi trả lời trực tiếp được bằng một phép tính cụ thể trên dữ liệu, cho ra một con số với đơn vị đo rõ ràng.
- Ghi rõ: (i) các cột sử dụng, đúng tên; (ii) phép tính/kỹ thuật (tổng, trung bình, tỷ lệ, kiểm định, hồi quy, mô hình dự báo, tối ưu hóa, mô phỏng…); (iii) đơn vị đo của kết quả.
- Ví dụ dạng: “[Chỉ số cụ thể] trung bình/tổng tại [đơn vị Y]: [kỳ A] vs [kỳ B] là bao nhiêu [đơn vị đo]?”

MINH HỌA MỘT CHUỖI 4 LỚP
- Lớp 1 – Vấn đề kinh doanh: “Lợi nhuận quý này giảm 12% so với quý trước.”
- Lớp 2 – Câu hỏi kinh doanh: “Chi phí nào tăng nhanh nhất và ở khu vực nào?”
- Lớp 3 – Câu hỏi phân tích: “Chi phí nguyên liệu tại chi nhánh Đà Nẵng đã tăng bao nhiêu % trong Q3 so với Q2?”
- Lớp 4 – Câu hỏi thống kê: “Giá vốn hàng bán (COGS) trung bình/đơn hàng tại Đà Nẵng: Q2 vs Q3 là bao nhiêu VNĐ?”

PHÂN LOẠI LOẠI HÌNH CÂU HỎI (thuộc tính của mỗi chuỗi câu hỏi, không phải một lớp)
- Gắn mỗi câu hỏi kinh doanh (và chuỗi câu hỏi đi kèm) với một loại hình: Mô tả (điều gì đã xảy ra?) / Chẩn đoán (vì sao?) / Dự đoán (điều gì có thể xảy ra?) / Đề xuất (nên làm gì?).
- Khuyến khích bộ câu hỏi phủ đủ 4 loại hình nhưng không bắt buộc: nếu với QUYẾT ĐỊNH này một loại hình không cần thiết, bỏ qua và nêu lý do. Ít nhất một câu phải trả lời trực tiếp QUYẾT ĐỊNH.
- Ví dụ dạng câu hỏi kinh doanh theo loại hình:
    • Mô tả: “[Yếu tố nào] thay đổi nhanh nhất và ở [phạm vi nào]?”
    • Chẩn đoán: “Vì sao [kết quả] ở [phạm vi nào] lại [tăng/giảm]?”
    • Dự đoán: “[Kết quả] sẽ diễn biến thế nào trong [kỳ tới] nếu [điều kiện] giữ nguyên?”
    • Đề xuất: “Nên [hành động nào] với [đối tượng nào] để đạt [mục tiêu] trong [ràng buộc]?”
- Ví dụ dạng câu hỏi thống kê theo loại hình (ngoài dạng Mô tả ở Lớp 4):
    • Chẩn đoán: “Chênh lệch trung bình [cột X] giữa [nhóm 1] và [nhóm 2] là bao nhiêu [đơn vị đo], p-value của kiểm định [t / chi-bình phương] là bao nhiêu?”
    • Dự đoán: “Mô hình [tên] dùng [các cột] dự báo [cột mục tiêu] cho [kỳ tới] có sai số [MAPE/RMSE/AUC] bao nhiêu trên tập kiểm tra [kỳ C]?”
    • Đề xuất: “Với [ràng buộc], giá trị tối ưu của [biến quyết định] là bao nhiêu và [KPI] tăng thêm bao nhiêu [đơn vị đo] so với hiện trạng?”

════════════════════════════════════════
PHẦN B — HAI YÊU CẦU BỔ SUNG
════════════════════════════════════════

BỔ SUNG 1) DỮ LIỆU CẦN THU THẬP THÊM – kiểm tra từng câu hỏi thống kê
- Nếu dữ liệu đang có đã đủ: ghi “Đủ dữ liệu hiện có”.
- Nếu chưa đủ, chỉ rõ: a. tên trường còn thiếu; b. nguồn có thể thu thập; c. mức ưu tiên (Cao/Trung bình/Thấp); d. nếu không thu thập được (dữ liệu công khai), đề xuất biến thay thế hoặc giả định có căn cứ và cách kiểm tra độ nhạy.
- Ví dụ: “Thiếu giá vốn theo sản phẩm – nguồn: phần mềm kế toán hoặc BCTC doanh nghiệp cùng ngành – ưu tiên Cao – nếu không có: giả định biên gộp theo danh mục, kiểm tra độ nhạy ±5 điểm %.”

BỔ SUNG 2) HÀNH ĐỘNG DỰ KIẾN – cho mỗi câu hỏi kinh doanh
- Viết dạng: “Nếu [chỉ số] [>/<] [ngưỡng] thì [hành động A]; ngược lại [hành động B]”. Nếu chưa biết ngưỡng, ghi ngưỡng là tham số cần xác định và cách xác định.
- Ví dụ: “Nếu tỷ lệ giao trễ ở vùng Y > 15% → mở kho vệ tinh tại Y; ngược lại → giữ mạng lưới hiện tại và điều chỉnh cam kết thời gian giao.”

════════════════════════════════════════
QUY TẮC CHO AI
════════════════════════════════════════
- Không bịa trường dữ liệu: chỉ dùng các cột đã liệt kê; mọi trường khác phải đưa vào cột “Dữ liệu cần thu thập thêm”.
- Không trả lời các câu hỏi, không đưa số liệu giả định như thể là kết quả.
- Nếu bối cảnh hoặc dữ liệu chưa đủ để đặt câu hỏi tốt, nêu điểm thiếu ở đầu câu trả lời, rồi vẫn lập bảng với giả định tạm thời được ghi rõ.

════════════════════════════════════════
YÊU CẦU TRÌNH BÀY
════════════════════════════════════════
- 1. Nhắc lại LỚP 1 (Vấn đề kinh doanh) ở đầu câu trả lời, sau đó lập bảng, mỗi dòng 6 cột: [Câu hỏi kinh doanh (đã sắp ưu tiên) | Câu hỏi phân tích | Câu hỏi thống kê | Loại hình câu hỏi | Dữ liệu cần thu thập thêm (nếu có) | Hành động dự kiến].
- 2. Dưới bảng: (a) CÂU HỎI QUYẾT ĐỊNH CHỐT, viết trong một câu; (b) tự kiểm tra: số câu theo từng loại hình, số câu thống kê “Đủ dữ liệu hiện có”, các câu phải dựa vào giả định; (c) đánh giá mức khả thi của đề tài với dữ liệu hiện có (Cao/Trung bình/Thấp) và lý do.
```

