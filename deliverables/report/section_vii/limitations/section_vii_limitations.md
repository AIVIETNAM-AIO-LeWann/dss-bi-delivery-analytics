# 7.1 Hạn chế và dữ liệu cần bổ sung

Mục này rà toàn bộ chuỗi phân tích của nhóm, từ chuẩn bị dữ liệu, mô tả và chẩn đoán, dự báo, đề xuất cam kết, benchmark tuyến đến dashboard. Mỗi hạn chế gồm ba phần: bằng chứng lấy từ file trong repo tại commit `6b5acb7`, ảnh hưởng đến kết luận hoặc quyết định logistics, và dữ liệu cần bổ sung. Dữ liệu cần bổ sung được tách thành hai loại. **Thiếu thực sự** là dữ liệu không có trong DataCo, Solomon hay repo. **Đã có, chưa dùng** là dữ liệu đã nằm trong nguồn hoặc tài liệu công khai nhưng chưa được đưa vào phân tích.

Mục 7.2 trình bày hướng nghiên cứu và thiết kế thử nghiệm. Mục này chỉ nêu điều kết quả hiện tại chưa chứng minh được và dữ liệu cần có để chứng minh.

## 7.1.1 Nguồn dữ liệu, cấp quan sát và tính đại diện

**H1. DataCo là snapshot lịch sử công khai, chưa đối chiếu với hệ thống vận hành.**

*Bằng chứng.* Dữ liệu gồm các đơn đặt từ 01/01/2015 đến 31/01/2018 (`01_nguon_du_lieu.md`). Nguồn không kèm tổng kiểm soát từ ERP nên độ đầy đủ được ghi là chưa xác minh được (`03_chat_luong_va_lam_sach.md`, Bước 2). Bản tải dùng slug `saicharankomati`, khác slug `shashwatwork` trong đề; hai bản chưa được chứng minh trùng byte (`context_manifest.json`). Dữ liệu còn có những mẫu hình đều đặn bất thường so với vận hành thông thường. First Class luôn mất đúng 2 ngày ở cả 37 tháng. Second Class và Standard Class có số ngày thực tế trải gần đều từ 2 đến 6 ngày, mỗi mức chiếm 19,8%–20,2% số đơn (`02_mode_actual_days_distribution.csv`). Tỷ lệ trễ theo tháng chỉ dao động 55,0%–59,9%, theo thị trường 56,55%–57,68%. Nhóm không xác minh được cơ chế tạo ra các mẫu hình này, nên không khẳng định dữ liệu được mô phỏng, nhưng cũng không coi chúng là hành vi vận hành thực.

*Ảnh hưởng.* Các con số 57,31% đơn trễ, 100% First Class trễ hay AUC 0,746 mô tả đúng file đã ghim checksum, không mô tả một doanh nghiệp đang hoạt động. Khuyến nghị ở Phần VI vì vậy là giả thuyết cần kiểm chứng trên dữ liệu của doanh nghiệp áp dụng. DHL chỉ là bối cảnh tham chiếu. Nếu thời gian giao trong từng phương thức thực sự phân phối đều và không phụ thuộc biến nào khác, thì không mô hình nào dùng các biến hiện có có thể dự báo tốt hơn mức theo phương thức (xem H6).

*Dữ liệu cần bổ sung.* Thiếu thực sự: bản trích đơn hàng và giao vận từ OMS/TMS của doanh nghiệp áp dụng, giai đoạn gần đây và đủ dài để bao phủ mùa vụ, kèm tổng kiểm soát số đơn theo tháng. Mục đích là kiểm tra tính đại diện và chạy lại toàn bộ chuỗi phân tích. Đã có, chưa dùng: bản Mendeley Data V5 gốc (DOI 10.17632/8gx2fvg2k6.5) để đối chiếu checksum với bản Kaggle đã dùng.

**H2. Cấp dòng hàng, cấp đơn và mẫu không hủy.**

*Bằng chứng.* Nguồn có 180.519 dòng hàng thuộc 65.752 đơn. KPI chính tính ở cấp đơn trên 62.897 đơn không hủy, sau khi loại 2.855 đơn hủy. Đơn hủy mang nhãn trễ 0, nên tỷ lệ trễ toàn nguồn là 54,82%, thấp hơn 57,31% của mẫu chính (`baseline_kpis.csv`). Có 4.423 dòng hàng thuộc đơn hủy có số ngày thực tế vượt cam kết nhưng vẫn mang nhãn 0 (`label_consistency.csv`). Mẫu chỉ gồm trạng thái COMPLETE/CLOSED có 28.965 đơn, tỷ lệ trễ 57,42%, và chỉ dùng để kiểm tra độ nhạy. Phân tích sản phẩm và danh mục làm ở cấp dòng, nên một đơn có thể thuộc nhiều nhóm.

*Ảnh hưởng.* Mọi tỷ lệ trễ và P_Late đều có điều kiện "đơn không bị hủy". Tại lúc đặt hàng chưa biết đơn có bị hủy hay không, nên P_Late không áp dụng trực tiếp cho mọi đơn mới (giả định A16). Nếu một phần đơn bị hủy vì khách chờ lâu, việc loại đơn hủy làm tỷ lệ trễ lệch theo hướng chưa xác định được. Không được cộng số đơn giữa các danh mục để ra tổng số đơn.

*Dữ liệu cần bổ sung.* Thiếu thực sự: thời điểm hủy, lý do hủy, bên khởi tạo hủy và trạng thái đơn lúc hủy, lấy từ OMS và bộ phận chăm sóc khách hàng. Mục đích là dự báo hủy riêng hoặc xây mô hình ba trạng thái, đồng thời đo thiên lệch do loại đơn hủy. Đã có, chưa dùng: trường `order_status`, gồm cả các trạng thái chờ xử lý, mới chỉ dùng cho kiểm tra độ nhạy COMPLETE/CLOSED.

## 7.1.2 Nhãn giao trễ, thời điểm đo và rò rỉ thông tin

**H3. Nhãn trễ là chỉ báo shipping của nguồn, đo bằng số ngày nguyên.**

*Bằng chứng.* Nhãn `late_delivery_risk` được giữ nguyên từ nguồn. Từ điển gốc gọi `shipping date` là timestamp shipment, không xác nhận đó là lúc khách nhận hàng (`01_nguon_du_lieu.md`). Số ngày thực tế là số nguyên từ 0 đến 6. Toàn bộ 3.407 đơn Same Day trong mẫu chính lệch ±0,5 ngày giữa duration và khoảng timestamp. Nếu chỉ giữ đơn có timestamp nhất quán, mẫu còn 59.490 đơn và mất hết Same Day (`analysis_sensitivity.csv`, giả định A04 và A14). Same Day chỉ nhận giá trị 0 hoặc 1 ngày với cam kết 0 ngày, nên tỷ lệ trễ 48,37% của nhóm này phụ thuộc hoàn toàn vào cách làm tròn. Số ngày cam kết không đổi trong từng phương thức (độ lệch chuẩn bằng 0).

*Ảnh hưởng.* Các kết luận về Same Day có độ tin cậy thấp nhất, gồm tỷ lệ trễ, 394 đơn trễ bị bỏ sót và việc giữ cam kết 0 ngày trong phương án +1 ngày. Vì số ngày là số nguyên, cam kết chỉ thay đổi được theo từng ngày. Ví dụ, kịch bản mục tiêu 80% đúng hẹn cho tỷ lệ vượt hẹn 7,20% trên validation và 5,11% trên test, thay vì khoảng 20% như mục tiêu (`promise_summary.csv`). Nhãn đo theo ngày cũng không phân biệt trễ vài giờ với trễ gần trọn một ngày.

*Dữ liệu cần bổ sung.* Thiếu thực sự: ngày giờ cam kết giao hoặc khung giờ đã hứa, thời điểm giao thành công có bằng chứng (quét POD, chữ ký, ảnh), múi giờ điểm giao và lịch làm việc theo quốc gia. Nguồn dự kiến là TMS và dữ liệu tracking của hãng vận chuyển. Mục đích là tính lại nhãn theo giờ và xác thực mẫu hình của Same Day và First Class.

**H4. Chưa chứng minh được các biến dự báo đã biết tại lúc đặt hàng.**

*Bằng chứng.* Sổ giả định ghi A05 (mốc dự báo là lúc đặt hàng) và A06 (một số biến candidate đã có khi đặt hàng) đều chưa xác minh (`05_so_gia_dinh.md`). Khoảng đệm 7 ngày, gồm 761 đơn, dựa vào timestamp shipment làm proxy, vì nguồn không cho biết nhãn được ghi nhận lúc nào (`07_du_lieu_cho_phan_tich.md`). Gần như toàn bộ tín hiệu dự báo nằm ở `shipping_mode` (H6). Biến `shipping_days_scheduled` hoàn toàn được xác định bởi phương thức nên không thêm thông tin.

*Ảnh hưởng.* Nếu phương thức hoặc cam kết được gán hay thay đổi sau lúc đặt, chẳng hạn nâng hạng dịch vụ khi kho chậm, thì AUC 0,746 có thể lạc quan và cảnh báo không dùng được ngay lúc nhận đơn. Các kiểm tra kỹ thuật hiện có chỉ loại các biến kết quả rõ ràng, chưa loại trừ được rò rỉ do quy trình nghiệp vụ.

*Dữ liệu cần bổ sung.* Thiếu thực sự: nhật ký sự kiện có dấu thời gian cho từng đơn, gồm tạo đơn, chọn hoặc đổi phương thức, xác nhận cam kết, xuất kho, bàn giao hãng, giao, hủy và thời điểm ghi nhãn. Nguồn dự kiến là OMS, WMS và TMS. Mục đích là dựng bộ biến theo đúng trạng thái tại mốc dự báo và kiểm tra rò rỉ.

## 7.1.3 Phân tích mô tả và chẩn đoán

**H5. Liên hệ thống kê không chứng minh nhân quả; p > 0,05 không chứng minh độc lập.**

*Bằng chứng.* Trong chín kiểm định χ², `shipping_mode` có Cramér's V = 0,4807. Tám biến còn lại có p ≥ 0,05 và V ≤ 0,0221 (`11_chi2_independence_tests.csv`). Báo cáo mô tả kết luận các biến này "đều độc lập với rủi ro trễ" (`BAO_CAO_MO_TA_VA_CHAN_DOAN.md`, dòng 144), README của phần mô tả viết "hoàn toàn độc lập" (dòng 66). Mỗi kiểm định chỉ xét một biến với nhãn, không kiểm soát phương thức. Tháng đặt hàng và danh mục sản phẩm không có trong bảng kiểm định. Phương thức do khách hoặc chính sách lựa chọn, không được phân bổ ngẫu nhiên.

*Ảnh hưởng.* Cách viết đúng là "chưa tìm thấy bằng chứng về liên hệ trong phép kiểm định này". Với 62.897 đơn, V ≤ 0,0221 cho thấy nếu có liên hệ thì liên hệ đó rất nhỏ trong mẫu này. Điều đó không chứng minh thị trường hay thời điểm không quan trọng ở doanh nghiệp khác, hoặc khi đã kiểm soát phương thức. Liên hệ mạnh của phương thức cũng không có nghĩa đổi phương thức sẽ giảm trễ. Second Class và Standard Class có phân phối thời gian thực tế gần như giống nhau (H1); khác biệt về tỷ lệ trễ chủ yếu nằm ở mức cam kết 2 ngày và 4 ngày. Khi ghép báo cáo, nhóm tổng hợp nên sửa cách diễn đạt về "độc lập" và ghi rõ đã sửa, không sửa ngầm file gốc.

*Dữ liệu cần bổ sung.* Thiếu thực sự: dữ liệu theo từng chặng của quy trình, gồm thời gian xử lý tại kho, thời điểm bàn giao hãng, hãng và tuyến vận chuyển, khoảng cách từ kho đến điểm giao, khối lượng công việc theo ngày. Mục đích là tách thời gian giao thành từng chặng để chẩn đoán nguyên nhân. Đã có, chưa dùng: danh mục, bộ phận, sản phẩm, số lượng từng dòng, thành phố và bang đích, tọa độ cửa hàng đã có trong bảng sạch nhưng chưa đưa vào kiểm định có kiểm soát phương thức hay phân tích đa biến.

## 7.1.4 Mô hình dự báo

**H6. Baseline chỉ có bốn mức P_Late, không phân biệt được các đơn trong cùng phương thức và có recall thấp.**

*Bằng chứng.* Mỗi phương thức chỉ có một điểm số (`risk_groups_test.csv`), nên AUC trong từng phương thức bằng 0,5 (`subgroups_test.csv`). Tại ngưỡng 0,5, 4.560 cảnh báo trên test chính là toàn bộ đơn First Class và Second Class. 3.467 đơn trễ bị bỏ sót gồm 3.073 đơn Standard Class và 394 đơn Same Day; hai nhóm này không bao giờ được cảnh báo. Trên validation, mọi ngưỡng từ 0,2 đến 0,4 đều cảnh báo tất cả các đơn, còn các ngưỡng từ 0,5 đến 0,8 cho cùng một kết quả (`thresholds_validation.csv`). Khi bỏ First Class khỏi test, AUC giảm từ 0,746 xuống 0,656. Mô hình logistic bỏ phương thức và số ngày cam kết có AUC 0,501 trên validation và 0,499 trên test (`sensitivity.csv`), tức 11 biến còn lại gần như không mang tín hiệu dự báo. Logistic đầy đủ có AP trên test 0,840, cao hơn 0,788 của baseline, nhưng chưa có kiểm định ý nghĩa hay khoảng tin cậy. Tập test chỉ gồm 7 tháng, từ 07/2017 đến 01/2018.

*Ảnh hưởng.* Precision 88,97% chủ yếu đến từ First Class, nhóm có nhãn trễ 100% (6.050/6.050 đơn train). Cảnh báo hiện tại tương đương quy tắc "cảnh báo mọi đơn First Class và Second Class". Nó không giúp chọn đơn nào trong 7.780 đơn Standard Class của test cần xử lý trước. Thanh trượt ngưỡng trên dashboard chỉ đổi kết quả khi đi qua một trong bốn mức xác suất. Mô hình hiện chưa dùng được để phân bổ nguồn lực theo từng đơn.

*Dữ liệu cần bổ sung.* Thiếu thực sự: các tín hiệu cấp đơn có trước lúc giao, gồm tình trạng tồn kho và kho xuất hàng, giờ đặt so với giờ chốt đơn của kho, hãng và dịch vụ vận chuyển thực tế, khoảng cách và vùng giao theo địa chỉ, khối lượng và kích thước kiện, số đơn tồn đọng theo ngày, ngày lễ và thời tiết theo vùng. Nguồn dự kiến là WMS, TMS, lịch nội bộ và dữ liệu thời tiết công khai. Mục đích là xếp hạng rủi ro được trong từng phương thức. Đã có, chưa dùng: sản phẩm, danh mục, bộ phận, đơn giá, chiết khấu, thành phố và bang đích có trong `order_items_clean.csv` và `orders_clean.csv` nhưng chưa nằm trong 13 biến của allowlist; cần rà lại thời điểm biết các biến này trước khi dùng.

**H7. P_Late là xác suất vượt cam kết cũ, không phải xác suất vượt cam kết mới hay hiệu quả can thiệp.**

*Bằng chứng.* Nhãn được định nghĩa theo số ngày cam kết cũ, trên mẫu không hủy (`CONTRIBUTING.md`, `analysis_schema.json`). Trên test, First Class có P_Late 100%, nhưng khi cam kết tăng từ 1 lên 2 ngày thì vượt hẹn tính lại của nhóm này bằng 0% (`pilot_by_mode_test.csv`). Dữ liệu không có biến nào ghi nhận đơn đã được can thiệp hay kết quả sau can thiệp.

*Ảnh hưởng.* Không được ghép P_Late với cam kết mới của khuyến nghị 1. Cũng không được dùng P_Late để ước tính số đơn trễ tránh được nhờ cảnh báo trong khuyến nghị 2. Mọi phép tính giá trị kỳ vọng của can thiệp hiện thiếu cả xác suất theo cam kết mới lẫn hiệu quả can thiệp (xem 7.2.2).

*Dữ liệu cần bổ sung.* Thiếu thực sự: nhật ký xử lý từng cảnh báo (loại hành động, thời điểm, người xử lý) và kết quả giao sau đó, cùng một nhóm đơn không can thiệp để so sánh; chi phí của một đơn trễ và chi phí xử lý một cảnh báo. Nguồn dự kiến là hệ thống chăm sóc khách hàng, điều phối và kế toán. Mục đích là ước lượng hiệu quả can thiệp và chọn ngưỡng theo chi phí.

## 7.1.5 Đề xuất điều chỉnh cam kết

**H8. Đổi cam kết không làm giao hàng nhanh hơn; kết quả là mô phỏng hồi cứu.**

*Bằng chứng.* Thời gian giao thực tế trung bình trên test là 3,4968 ngày ở cả 11 phương án trong `promise_summary.csv`, vì duration nguồn được giữ cố định. Phương án +1 ngày giảm tỷ lệ vượt hẹn tính lại từ 57,56% xuống 26,82%, đổi lại cam kết trung bình tăng 0,94 ngày. Các phương án mục tiêu 90% và 95% đạt 0,00% vượt hẹn trên test với cam kết trung bình 5,12 ngày. Lý do là số ngày thực tế lớn nhất trong dữ liệu chỉ là 6 ngày, và phân vị tính trên train gần chạm mức này.

*Ảnh hưởng.* Mức giảm vượt hẹn chỉ là thay đổi cách so với lời hứa, không phải cải thiện vận hành. Kết quả 0% là hệ quả của giới hạn trên 6 ngày trong snapshot; nếu dữ liệu thực có những đơn giao lâu hơn nhiều, cam kết cần đặt và tỷ lệ vượt hẹn đều sẽ khác. Dữ liệu không cho biết khách phản ứng thế nào khi phải chờ thêm, nên chưa đánh giá được cái giá thương mại của 0,94 ngày cam kết tăng thêm.

*Dữ liệu cần bổ sung.* Thiếu thực sự: cam kết hiển thị cho khách tại lúc đặt; tỷ lệ chuyển đổi, bỏ giỏ, hủy đơn, khiếu nại và đánh giá theo từng mức cam kết; mục tiêu dịch vụ được phê duyệt cho từng phương thức. Nguồn dự kiến là website hoặc OMS, bộ phận chăm sóc khách hàng và ban lãnh đạo. Mục đích là định lượng đánh đổi giữa giữ lời hứa và thời gian chờ. Thiết kế thử nghiệm được trình bày ở 7.2.1.

## 7.1.6 Benchmark tuyến Solomon

**H9. Solomon độc lập với DataCo; đơn vị tọa độ không phải km; nhiên liệu là giả định.**

*Bằng chứng.* DataCo không có điểm dừng, xe, sức chở, khung giờ hay nhiên liệu; Latitude/Longitude là vị trí cửa hàng (giả định A11). Bài toán tuyến được giải trên C101, R101 và RC101 tải từ một bản sao trên GitHub, vì trang SINTEF trả lỗi HTTP 403; ba file chưa được đối chiếu byte với bản gốc (`run_manifest.json`). Quãng đường là khoảng cách Euclid trên tọa độ benchmark. Hệ số quy đổi (0,5; 1; 2 km mỗi đơn vị), mức tiêu hao (8; 12; 16 lít/100 km) và giá nhiên liệu (18.000; 22.000; 26.000 đồng/lít) đều là giả định (`run_analysis.py`). Với cùng một lời giải C101 dùng 10 xe, 27 tổ hợp giả định cho chi phí nhiên liệu mô phỏng từ 596.835 đến 6.896.755 đồng, chênh 11,56 lần (`fuel_scenarios.csv`).

*Ảnh hưởng.* 828,94 là đơn vị tọa độ Solomon, không phải km đường bộ. Chi phí nhiên liệu phản ánh giả định nhiều hơn phản ánh tuyến, nên không dùng để công bố tiền tiết kiệm. Kết quả tuyến không ghép được với tỷ lệ trễ của DataCo.

*Dữ liệu cần bổ sung.* Thiếu thực sự: tọa độ kho và điểm giao thực, ma trận khoảng cách và thời gian đường bộ, định mức tiêu hao theo loại xe, giá nhiên liệu kèm ngày hiệu lực. Nguồn dự kiến là TMS/GPS, dịch vụ bản đồ, bộ phận đội xe và kế toán. Đã có, chưa dùng: bộ Solomon gốc trên trang SINTEF, dùng để đối chiếu checksum ba file đã giải.

**H10. Tuyến khả thi, số xe tối thiểu đã chứng minh và quãng đường chưa chứng minh tối ưu là ba mức kết luận khác nhau.**

*Bằng chứng.* Mọi tuyến bàn giao đã được kiểm tra đủ khách, sức chở và khung giờ (hàm `verify_routes` trong `run_analysis.py`). Số xe tối thiểu chỉ được chứng minh cho C101 với Q = 200, ở cả cấu hình base và fleet10, vì cận dưới theo tải bằng đúng số xe của tuyến khả thi (10 xe). Các cấu hình khác còn khoảng cách, ví dụ R101 từ 8 đến 21 xe và RC101 từ 9 đến 17 xe (`fleet_sizing_bounds.csv`, Bảng 7.3 ở mục 7.2.3). Hàm mục tiêu chỉ gồm quãng đường, không có chi phí cố định cho mỗi xe (`run_manifest.json`), và chưa có cận dưới cho quãng đường.

*Ảnh hưởng.* Kết luận được phép là: với C101 và Q = 200 cần tối thiểu 10 xe, và đã có tuyến khả thi 10 xe dài 828,94 đơn vị. Không được nói quãng đường này tối ưu, cũng không được nói R101 cần 21 xe hay RC101 cần 17 xe. Kết luận số xe không chuyển sang kịch bản 5 xe × 500 kg trong bảng phân công hay sang một đội xe thực.

*Dữ liệu cần bổ sung.* Đã có, chưa dùng: bảng nghiệm tốt nhất đã công bố (best-known solutions) cho bộ Solomon trên trang SINTEF, dùng để đo khoảng cách chất lượng của lời giải. Cận dưới có xét khung giờ là đầu ra phương pháp, được bàn ở 7.2.3.

**H11. Đối chứng yếu, thời gian giải ngắn và chưa kiểm tra ngoài mẫu.**

*Bằng chứng.* Đối chứng `nearest_feasible` không tìm được lời giải ở R101, RC101 và C101/fleet10, nên chỉ C101 có phần trăm giảm quãng đường (55,69%). Đối chứng cho cùng kết quả 21 xe và 1.870,69 đơn vị ở Q = 200 và Q = 240, tức không phản ứng với thay đổi sức chở (`routing_summary.csv`). OR-Tools được khởi tạo từ lời giải đối chứng khi có, dùng GUIDED_LOCAL_SEARCH, giới hạn 8 giây cho mỗi cấu hình và chỉ chạy một lần (`run_analysis.py`). Khi chạy lại, RC101 cho 16 xe và 1.718,55 đơn vị, khác bản công bố là 17 xe và 1.700,09 đơn vị (`replay_validation.json`). Thử nghiệm chỉ gồm ba instance 100 khách, mỗi lớp C, R, RC một instance.

*Ảnh hưởng.* 55,69% là mức tốt hơn một quy tắc tham lam đơn giản, không phải mức tốt hơn cách điều phối thực tế hay nghiệm tốt nhất đã biết. Số xe và quãng đường của R101, RC101 thay đổi theo lần chạy, nhưng chưa có khoảng dao động. Chưa có bằng chứng bộ giải cho kết quả tương tự trên instance khác, quy mô khác hay dữ liệu thực.

*Dữ liệu cần bổ sung.* Đã có, chưa dùng: các instance Solomon còn lại và các bộ benchmark công khai lớn hơn. Thiếu thực sự: tuyến do điều phối viên lập cho cùng một ngày giao để làm đối chứng nghiệp vụ; nhật ký nhiều lần chạy với các mức thời gian giải khác nhau.

**H12. Khả năng áp dụng vào doanh nghiệp còn hạn chế.**

*Bằng chứng.* Mô hình VRPTW hiện có một kho, đội xe đồng nhất, mỗi xe chạy một tuyến, khung giờ cứng và thời gian di chuyển lấy theo khoảng cách Euclid. Mô hình chưa có giờ làm của tài xế, tắc đường, nhiều chuyến hay giới hạn thể tích (`run_analysis.py`). DHL chỉ là bối cảnh tham chiếu; repo không có dữ liệu DHL (`context_manifest.json`).

*Ảnh hưởng.* Kết quả cho thấy cách tiếp cận chạy được trên benchmark, nhưng chưa đủ căn cứ cho quyết định mua thêm xe, cắt giảm xe hay đầu tư phần mềm.

*Dữ liệu cần bổ sung.* Thiếu thực sự: danh mục xe theo loại (tải trọng, thể tích, chi phí cố định), ca và giờ làm của tài xế, thời gian phục vụ thực tế tại điểm, khung giờ nhận hàng của khách, thời gian di chuyển theo giờ trong ngày. Nguồn dự kiến là bộ phận đội xe, nhân sự và TMS/GPS.

## 7.1.7 Dashboard và tích hợp kết quả

**H13. Dashboard là ảnh chụp kết quả lịch sử, không phải hệ thống giám sát vận hành.**

*Bằng chứng.* Bản web nhúng sẵn dữ liệu đã tổng hợp và chạy không cần mạng (`README.md`). Trang Rủi ro và trang Cam kết dùng 13.071 đơn test từ 07/2017 đến 01/2018; trang Tuyến dùng Solomon. README ghi bộ kiểm tra đã so 153 phép tính trong trình duyệt với pandas trên CSV gốc. Phép so này chứng minh dashboard nhất quán với CSV, không chứng minh bản thân dữ liệu nguồn đúng.

*Ảnh hưởng.* Số liệu trên dashboard không tự cập nhật, và mọi hạn chế H1–H12 vẫn áp dụng cho từng trang tương ứng. DataCo và Solomon là hai nguồn riêng, không lọc chéo được với nhau.

*Dữ liệu cần bổ sung.* Thiếu thực sự: nguồn dữ liệu vận hành cập nhật định kỳ, dùng cùng định nghĩa KPI trong `kpi_dictionary.md`; nhật ký các quyết định đã ra dựa trên dashboard, để đánh giá giá trị sử dụng.

## 7.1.8 Bảng tổng hợp

Mức ưu tiên **Cao** nghĩa là hạn chế có thể làm thay đổi hoặc chặn một khuyến nghị ở Phần VI. **Trung bình** nghĩa là hạn chế giới hạn phạm vi diễn giải nhưng không đổi hướng khuyến nghị. **Thấp** nghĩa là hạn chế chủ yếu ảnh hưởng cách trình bày.

**Bảng 7.1.1 Hạn chế – Bằng chứng – Ảnh hưởng – Dữ liệu cần bổ sung – Mức ưu tiên**

| Hạn chế | Bằng chứng | Ảnh hưởng | Dữ liệu cần bổ sung | Ưu tiên |
| --- | --- | --- | --- | --- |
| H1. Snapshot công khai 2015–2018 | Không có tổng kiểm soát ERP; duration Second/Standard đều 2–6 ngày; First Class luôn 2 ngày | Kết quả không đại diện doanh nghiệp đang hoạt động | Dữ liệu OMS/TMS gần đây của doanh nghiệp áp dụng | Cao |
| H2. Mẫu không hủy | 2.855 đơn hủy bị loại; 54,82% so với 57,31% | P_Late không áp dụng cho mọi đơn mới | Thời điểm, lý do hủy | Trung bình |
| H3. Nhãn theo ngày nguyên | 3.407 đơn Same Day lệch ±0,5 ngày | Kết luận Same Day kém tin cậy; cam kết nhảy bậc | Mốc cam kết và giao theo giờ, POD | Cao |
| H4. Thời điểm biết biến dự báo | A05, A06 chưa xác minh; nhãn không có dấu thời gian | AUC có thể lạc quan nếu có rò rỉ | Nhật ký sự kiện từng đơn | Cao |
| H5. Liên hệ, không nhân quả | p ≥ 0,05 bị viết là "độc lập"; kiểm định từng biến | Không kết luận đổi phương thức giảm trễ | Dữ liệu từng chặng; biến đã có dùng đa biến | Trung bình |
| H6. Bốn mức P_Late | AUC trong phương thức 0,5; ablation AUC 0,499; bỏ sót 3.467 đơn | Không xếp hạng được đơn để xử lý | Tín hiệu kho, hãng, địa chỉ, tồn đọng | Cao |
| H7. P_Late theo cam kết cũ | First Class P_Late 100% nhưng 0% vượt hẹn khi cam kết 2 ngày | Không tính được hiệu quả KN1, KN2 | Nhật ký can thiệp, nhóm đối chứng, chi phí | Cao |
| H8. Đổi cam kết không giao nhanh hơn | Thời gian thực tế 3,4968 ngày ở cả 11 phương án | 0% vượt hẹn do trần 6 ngày | Phản ứng khách theo mức cam kết | Trung bình |
| H9. Solomon, đơn vị, nhiên liệu | Bản sao chưa đối chiếu; nhiên liệu chênh 11,56 lần | Không công bố km hay tiền tiết kiệm | Tọa độ thật, ma trận đường bộ, định mức | Trung bình |
| H10. Khả thi khác tối ưu | Chỉ C101/Q = 200 chứng minh 10 xe | Không nói quãng đường tối ưu | Nghiệm tốt nhất đã công bố | Trung bình |
| H11. Đối chứng và thời gian giải | 8 giây, một lần; RC101 chạy lại 16 xe | 55,69% chỉ so với quy tắc tham lam | Tuyến điều phối thực; nhiều lần chạy | Trung bình |
| H12. Áp dụng doanh nghiệp | Một kho, xe đồng nhất, Euclid | Chưa đủ căn cứ quyết định đội xe | Loại xe, ca tài xế, thời gian theo giờ | Cao |
| H13. Dashboard tĩnh | Dữ liệu nhúng sẵn; 153 phép so chỉ với CSV | Không giám sát vận hành | Nguồn cập nhật định kỳ | Thấp |

Số liệu trong bảng lấy từ các file nêu ở H1–H13; mẫu số giữ nguyên như trong từng đoạn.

**Bảng 7.1.2 Dữ liệu cần bổ sung theo loại, nguồn và mục đích**

| Dữ liệu | Loại | Nguồn dự kiến | Mục đích | Hạn chế |
| --- | --- | --- | --- | --- |
| Đơn hàng, giao vận gần đây có tổng kiểm soát | Thiếu | OMS/TMS doanh nghiệp | Kiểm tra đại diện, chạy lại phân tích | H1 |
| Mốc cam kết và giao theo giờ, bằng chứng POD | Thiếu | TMS, tracking hãng | Xác thực nhãn, Same Day | H3 |
| Nhật ký sự kiện từng đơn | Thiếu | OMS/WMS/TMS | Kiểm tra rò rỉ, mốc dự báo | H4 |
| Thời điểm, lý do hủy | Thiếu | OMS, CSKH | Mô hình cho mọi đơn mới | H2 |
| Tín hiệu kho, hãng, địa chỉ, tồn đọng, thời tiết | Thiếu | WMS/TMS, dữ liệu công khai | Xếp hạng trong phương thức | H5, H6 |
| Nhật ký can thiệp, nhóm đối chứng, chi phí | Thiếu | CSKH, điều phối, kế toán | Hiệu quả can thiệp, ngưỡng | H7 |
| Phản ứng khách theo mức cam kết | Thiếu | Website/OMS, CSKH | Đánh đổi cam kết | H8 |
| Tọa độ thật, ma trận đường bộ, xe, ca, nhiên liệu | Thiếu | TMS/GPS, bản đồ, đội xe | Bài toán tuyến thực | H9, H12 |
| Tuyến điều phối thực cùng ngày | Thiếu | Điều phối | Đối chứng nghiệp vụ | H11 |
| `order_status` | Đã có, chưa dùng | `orders_clean.csv` | Phân tích trạng thái chờ | H2 |
| Sản phẩm, danh mục, đơn giá, thành phố/bang đích | Đã có, chưa dùng | `order_items_clean.csv`, `orders_clean.csv` | Kiểm định đa biến, biến dự báo | H5, H6 |
| Bản Mendeley V5 gốc | Đã có, chưa dùng | Mendeley Data | Đối chiếu checksum | H1 |
| Bộ Solomon gốc và nghiệm tốt nhất | Đã có, chưa dùng | SINTEF | Đối chiếu file, đo chất lượng | H9–H11 |

## 7.1.9 Ghi chú cho người tổng hợp

- Mục 7.2 của Hoài Phú đã dùng tên Bảng 7.1–7.3. Mục này đánh số Bảng 7.1.1 và 7.1.2 để không trùng; người tổng hợp có thể đánh lại số bảng cho toàn Phần VII.
- Khi ghép Phần VI và báo cáo mô tả, nên đổi "độc lập" hoặc "hoàn toàn độc lập" thành "chưa tìm thấy bằng chứng về liên hệ trong phép kiểm định này", và ghi rõ đã sửa.
- Mục này thay thế phần "Hạn chế và dữ liệu cần bổ sung" trong bản Word dự báo ngày 05/11/2026 và mở rộng ra toàn bộ nghiên cứu. Bản Word cũ được giữ nguyên.

**Bảng 7.1.3 Nguồn bằng chứng**

Tất cả file được đọc tại commit [`6b5acb7`](https://github.com/AIVIETNAM-AIO-LeWann/dss-bi-delivery-analytics/tree/6b5acb7cf54f1f72682ed8bea86cc4c9eba74b9b). Mọi con số trong mục này được kiểm tra lại bằng `code/verify_figures.py` (91/91 kiểm tra đạt).

| File | Dùng cho | Hạn chế |
| --- | --- | --- |
| [docs/data_preparation/01_nguon_du_lieu.md](https://github.com/AIVIETNAM-AIO-LeWann/dss-bi-delivery-analytics/blob/6b5acb7cf54f1f72682ed8bea86cc4c9eba74b9b/docs/data_preparation/01_nguon_du_lieu.md) | Khoảng thời gian, định nghĩa timestamp, tọa độ cửa hàng | H1, H3, H9 |
| [docs/data_preparation/03_chat_luong_va_lam_sach.md](https://github.com/AIVIETNAM-AIO-LeWann/dss-bi-delivery-analytics/blob/6b5acb7cf54f1f72682ed8bea86cc4c9eba74b9b/docs/data_preparation/03_chat_luong_va_lam_sach.md) | Độ đầy đủ chưa xác minh | H1 |
| [docs/data_preparation/05_so_gia_dinh.md](https://github.com/AIVIETNAM-AIO-LeWann/dss-bi-delivery-analytics/blob/6b5acb7cf54f1f72682ed8bea86cc4c9eba74b9b/docs/data_preparation/05_so_gia_dinh.md) | Giả định A04–A06, A11, A14, A16 | H2–H4, H9 |
| [docs/data_preparation/07_du_lieu_cho_phan_tich.md](https://github.com/AIVIETNAM-AIO-LeWann/dss-bi-delivery-analytics/blob/6b5acb7cf54f1f72682ed8bea86cc4c9eba74b9b/docs/data_preparation/07_du_lieu_cho_phan_tich.md) | Chia tập, khoảng đệm, proxy nhãn | H4 |
| [reports/data_quality/baseline_kpis.csv](https://github.com/AIVIETNAM-AIO-LeWann/dss-bi-delivery-analytics/blob/6b5acb7cf54f1f72682ed8bea86cc4c9eba74b9b/reports/data_quality/baseline_kpis.csv), [analysis_exclusion_summary.csv](https://github.com/AIVIETNAM-AIO-LeWann/dss-bi-delivery-analytics/blob/6b5acb7cf54f1f72682ed8bea86cc4c9eba74b9b/reports/data_quality/analysis_exclusion_summary.csv), [label_consistency.csv](https://github.com/AIVIETNAM-AIO-LeWann/dss-bi-delivery-analytics/blob/6b5acb7cf54f1f72682ed8bea86cc4c9eba74b9b/reports/data_quality/label_consistency.csv), [analysis_sensitivity.csv](https://github.com/AIVIETNAM-AIO-LeWann/dss-bi-delivery-analytics/blob/6b5acb7cf54f1f72682ed8bea86cc4c9eba74b9b/reports/data_quality/analysis_sensitivity.csv) | Số dòng, số đơn, đơn hủy, Same Day | H2, H3 |
| [workstreams/descriptive/tables/](https://github.com/AIVIETNAM-AIO-LeWann/dss-bi-delivery-analytics/tree/6b5acb7cf54f1f72682ed8bea86cc4c9eba74b9b/workstreams/descriptive/tables) (01, 02, 03, 06, 11) | Phân phối ngày, theo tháng, thị trường, χ² | H1, H3, H5 |
| [workstreams/descriptive/BAO_CAO_MO_TA_VA_CHAN_DOAN.md](https://github.com/AIVIETNAM-AIO-LeWann/dss-bi-delivery-analytics/blob/6b5acb7cf54f1f72682ed8bea86cc4c9eba74b9b/workstreams/descriptive/BAO_CAO_MO_TA_VA_CHAN_DOAN.md) dòng 144, [README.md](https://github.com/AIVIETNAM-AIO-LeWann/dss-bi-delivery-analytics/blob/6b5acb7cf54f1f72682ed8bea86cc4c9eba74b9b/workstreams/descriptive/README.md) dòng 66 | Cách diễn đạt "độc lập" | H5 |
| [workstreams/forecasting/results/](https://github.com/AIVIETNAM-AIO-LeWann/dss-bi-delivery-analytics/tree/6b5acb7cf54f1f72682ed8bea86cc4c9eba74b9b/workstreams/forecasting/results) (model_comparison, subgroups_test, thresholds_validation, sensitivity, split_summary, mode_baseline_train) | Chỉ số mô hình, ngưỡng, độ nhạy | H4, H6 |
| [workstreams/prescriptive/results/](https://github.com/AIVIETNAM-AIO-LeWann/dss-bi-delivery-analytics/tree/6b5acb7cf54f1f72682ed8bea86cc4c9eba74b9b/workstreams/prescriptive/results) (risk_groups_test, promise_summary, pilot_by_mode_test) | Bốn mức P_Late, phương án cam kết | H6–H8 |
| [workstreams/prescriptive/results/](https://github.com/AIVIETNAM-AIO-LeWann/dss-bi-delivery-analytics/tree/6b5acb7cf54f1f72682ed8bea86cc4c9eba74b9b/workstreams/prescriptive/results) (routing_summary, fleet_sizing_bounds, fuel_scenarios, run_manifest, replay_validation, context_manifest) | Tuyến, số xe, nhiên liệu, nguồn Solomon | H1, H9–H12 |
| [workstreams/prescriptive/code/run_analysis.py](https://github.com/AIVIETNAM-AIO-LeWann/dss-bi-delivery-analytics/blob/6b5acb7cf54f1f72682ed8bea86cc4c9eba74b9b/workstreams/prescriptive/code/run_analysis.py) | Cấu hình bộ giải, giả định nhiên liệu, kiểm tra tuyến | H9–H12 |
| [README.md](https://github.com/AIVIETNAM-AIO-LeWann/dss-bi-delivery-analytics/blob/6b5acb7cf54f1f72682ed8bea86cc4c9eba74b9b/README.md), [CONTRIBUTING.md](https://github.com/AIVIETNAM-AIO-LeWann/dss-bi-delivery-analytics/blob/6b5acb7cf54f1f72682ed8bea86cc4c9eba74b9b/CONTRIBUTING.md) | Định nghĩa P_Late, dashboard, quy tắc diễn đạt | H7, H13 |
