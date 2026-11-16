from pathlib import Path
import pandas as pd
from fleet_bounds import write_bounds
R=Path(__file__).resolve().parents[1];O=R/'results'
fleet_bounds=write_bounds()
s=pd.read_csv(O/'promise_summary.csv');g=pd.read_csv(O/'routing_summary.csv')
def trieu(n):
 return f'{n/1e6:.2f}'.replace('.',',')
def table(headers,rows):
 return '| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+'\n'.join('| '+' | '.join(map(str,row))+' |' for row in rows)
labels={'current':'Cam kết hiện tại','bounded_plus1_keep_same_day':'Tăng tối đa 1 ngày, giữ Same Day','q80_min100':'Phân vị 80%, nhóm train ≥100','q90_min100':'Phân vị 90%, nhóm train ≥100','q95_min100':'Phân vị 95%, nhóm train ≥100'}
rows=[]
for name,label in labels.items():
 v=s[(s.policy==name)&(s.partition=='validation')].iloc[0];t=s[(s.policy==name)&(s.partition=='test')].iloc[0]
 rows.append([label,f'{v.proposed_exceedance_rate:.2%}',f'{t.proposed_exceedance_rate:.2%}',f'{t.mean_proposed_days:.2f}',f'{t.mean_actual_days:.2f}'])
route_rows=[]
for x in g.itertuples():
 route_rows.append([x.instance.upper(),x.scenario,x.method,int(x.max_vehicles),int(x.capacity),int(x.vehicles_used) if pd.notna(x.vehicles_used) else '—',f'{x.distance_units:.2f}' if pd.notna(x.distance_units) else 'Chưa tìm được'])
c=g[(g.instance=='c101')&(g.scenario=='base')];d0=c[c.method=='nearest_feasible'].distance_units.iloc[0];d1=c[c.method=='ortools'].distance_units.iloc[0]
text=f'''# PHẦN V — PHÂN TÍCH ĐỀ XUẤT

**Chủ đề 18: Giao hàng đúng hẹn và tối ưu tuyến đường**  
**Thành viên: Hoài Phú (TV5) — Hạn nộp: 10/11/2026**  
**Bối cảnh doanh nghiệp: DHL Supply Chain North America — ứng dụng minh họa bằng DataCo và Solomon.**  
**Ngày hoàn thành: 06/11/2026. Người nhận: Giám đốc Logistics và nhóm tổng hợp báo cáo.**

## 1. Quyết định và phạm vi

Đề xuất đưa cam kết First Class 2 ngày vào bước rà soát và thí điểm, trình hai mức điều chỉnh cho Second Class và Standard Class cùng đánh đổi về thời gian chờ, giữ nguyên ý nghĩa giao trong ngày của Same Day. Dùng xác suất TV4 để ưu tiên kiểm tra theo phương thức, chưa tự động chi tiền can thiệp. Với bài toán tuyến C101 và sức chở 200 đơn vị, chọn phương án 10 xe đã kiểm tra tính khả thi; số xe này đạt cận dưới sức chở. Chi phí nhiên liệu trình dưới dạng kịch bản, chưa kết luận ROI doanh nghiệp.

Các lựa chọn trên là đề xuất quản trị dựa trên dữ liệu lịch sử và benchmark. Mức dịch vụ được phép cam kết, giới hạn kéo dài thời gian và tham số chi phí vẫn cần do doanh nghiệp quyết định trước khi triển khai.

Giám đốc Logistics cần lựa chọn cam kết thời gian giao theo phương thức/vùng và phương án xếp tuyến trong giới hạn số xe, sức chở, khung giờ khách hẹn. Chỉ tiêu đánh giá gồm tỷ lệ vượt cam kết, thời gian cam kết, thời gian giao thực tế, quãng đường, số xe sử dụng và chi phí nhiên liệu.

Phần này kế thừa dữ liệu TV2, phát hiện TV3 và xác suất dự báo TV4. Không huấn luyện lại hoặc thay mô hình TV4; không chọn nhà vận chuyển hay định giá giao hàng. Hai bài toán dùng hai nguồn riêng: DataCo cho cam kết; Solomon cho thử nghiệm tuyến. Không ghép khách hàng DataCo vào điểm giao Solomon.

### 1.1. Liên hệ với DHL Supply Chain

Nghiên cứu của Dang và cộng sự (2024) mô tả DHL Supply Chain North America xử lý hơn một tỷ kiện/năm. Bộ TNO có bốn mô-đun: Freight, Fleet, Pool Point và Round Trip. Trong 2,5 năm từ 2020, tác giả báo cáo tiết kiệm **ước tính** hơn 117 triệu USD cho DHL và khách hàng, tăng 20% win-rate và giảm ít nhất 0,1 megaton CO₂. Con số 20% không được tự đổi thành 20 điểm phần trăm. OR-Tools kết hợp heuristic được mô tả cụ thể cho mô-đun Round Trip. [Nguồn nghiên cứu](https://doi.org/10.1287/inte.2023.0087).

Nhóm dùng DHL làm bối cảnh tham chiếu cho quyết định của Giám đốc Logistics. Dữ liệu DataCo và Solomon không được xác nhận là dữ liệu nội bộ DHL; các kết quả tính trong báo cáo là thực nghiệm của nhóm. Thành tích TNO không được dùng làm tỷ lệ tiết kiệm kỳ vọng hoặc mục tiêu hiệu quả mặc định cho các kịch bản này.

Trong phần TV5, tách rõ hai quyết định: **fleet sizing** xác định số xe và cấu hình sức chở cần xem xét; **routing** phân khách, sắp thứ tự dừng và lịch phục vụ để kiểm tra tính khả thi. Một quy trình phù hợp cho bài này là lập cấu hình K/Q, giải tuyến, rồi điều chỉnh cấu hình nếu cần. Không chốt số xe chỉ bằng tổng nhu cầu chia sức chở, vì khung giờ và thời gian phục vụ còn có thể làm tăng nhu cầu xe. Mẫu Solomon hiện có đội xe đồng nhất; thay Q là kịch bản sức chở, chưa phải chọn loại xe thương mại hay tối ưu đội xe hỗn hợp.

Phạm vi báo cáo là **Phần V — Phân tích đề xuất, hạn 10/11/2026** của Hoài Phú. Bài toán và khuyến nghị được xây dựng cho Logistics theo Chủ đề 18.

## 2. Kết quả đầu vào và cách sử dụng

- TV2 xác định 180.519 dòng hàng thuộc 65.752 đơn. Mẫu chính có 62.897 đơn không hủy; tỷ lệ nhãn trễ 57,31%. Dữ liệu đặt hàng từ 2015 đến tháng 01/2018, không phải dữ liệu vận hành năm 2026.
- TV3 ghi nhận First Class trễ 100% trong mẫu, Second Class 79,99%, Same Day 48,37%, Standard Class 39,85%. First Class luôn có duration nguồn 2 ngày trong khi cam kết 1 ngày. Đây là đặc tính nguồn, không phải bảo đảm hành vi ngoài thực tế.
- TV3 chưa tìm thấy bằng chứng liên hệ rõ cho nhiều biến như vùng, thị trường, ngày đặt trong các kiểm định đã thực hiện. Không diễn giải p-value lớn thành bằng chứng các biến hoàn toàn độc lập hoặc không có tác động.
- TV4 chọn baseline theo phương thức bằng log loss validation. P_Late train tương ứng First Class 100%, Second Class 80,09%, Same Day 46,03%, Standard Class 40,05%. Mỗi phương thức chỉ có một mức xác suất; không dùng để xếp thứ tự rủi ro giữa các đơn cùng phương thức.
- Tất cả diễn giải về dự báo hiện có điều kiện không hủy trong snapshot. Duration nguồn chưa được xác thực là thời gian khách thực nhận; Latitude/Longitude là vị trí cửa hàng theo tài liệu nhóm, không dùng làm điểm giao.

Bản sao dữ liệu sạch trong bộ bàn giao TV4 được dùng để tái lập vì có đầy đủ bảng cần thiết. Các khóa được ghép 1:1 bằng `order_id` dạng Text. Đầu ra TV2–TV4 giữ nguyên.

**Nguồn DataCo:** link nhóm cung cấp là [DataCo Smart Supply Chain trên Kaggle — shashwatwork](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis). Manifest thực nghiệm TV4 ghi bản tải lại từ `saicharankomati/dataco-supply-chain-dataset`, phiên bản 1, SHA-256 CSV `994b3c8d24049cc46bf20e8161fedece9a9b95376cc0dc929921d76cf6b9bc0d`. Chưa đối chiếu byte giữa hai trang Kaggle, vì vậy link mới được ghi làm nguồn tham chiếu do nhóm cung cấp, không thay thế nguồn tính toán đã truy vết. Không tải đè hoặc làm lại dữ liệu TV2–TV4 trong lần cập nhật bối cảnh này.

## 3. Phương án cam kết giao hàng

### 3.1. Thiết kế đánh giá

Giữ nguyên phân chia TV4: train 39.568 đơn; validation 9.497; test 13.071; 761 đơn khoảng đệm không tham gia ước lượng hay đánh giá. Chỉ tính phân vị từ train. Với từng phương thức–vùng, nếu train có ít nhất 100 đơn thì dùng phân vị của nhóm; nếu không, lùi về phân vị cùng phương thức. Kiểm tra độ nhạy ngưỡng nhóm tại 50 và 200 đơn. Ngưỡng 100 là quy tắc ổn định mẫu cho thử nghiệm, chưa phải chuẩn thống kê đã được chứng minh.

Cam kết phân vị: d(m,r)=Q_target(duration nguồn trong train), lấy giá trị quan sát kế tiếp (`higher`) để giữ ngày nguyên. Các mức 80%, 90%, 95% là kịch bản mục tiêu, chưa được doanh nghiệp phê duyệt. Tỷ lệ vượt hẹn = số đơn có duration nguồn > cam kết kịch bản / tổng đơn trong cùng kỳ. Cam kết hiện tại được đối chiếu với nhãn gốc trên mẫu phân tích.

Bổ sung phương án giới hạn: d_giới_hạn = min(d_phân_vị90, d_hiện_tại + 1) cho phương thức khác Same Day; giữ Same Day ở 0 ngày. Đây là quy tắc thử nghiệm để trình bày đánh đổi giữa độ dài cam kết và tỷ lệ vượt hẹn, không phải chính sách đã duyệt.

Thiết kế được lập sau khi đã đọc kết quả mô tả toàn lịch sử của nhóm. Do đó, dù ước lượng chỉ dùng train và test không tham gia fit, kết quả vẫn là đánh giá khám phá trên holdout lịch sử đã được nhóm sử dụng; cần giai đoạn mới hoặc thử nghiệm triển khai để xác nhận độc lập. Không chọn một kịch bản “tốt nhất” bằng kết quả test.

### 3.2. Kết quả kịch bản

{table(['Kịch bản','Vượt hẹn validation','Vượt hẹn test','Cam kết TB test (ngày)','Duration thực tế TB test (ngày)'],rows)}

Nguồn tính: `results/promise_summary.csv`. Cùng 13.071 đơn test ở mỗi hàng. Tỷ lệ hiện tại trên test 57,56% khác 57,31% toàn mẫu vì mẫu số khác nhau.

Phương án giới hạn tương ứng First Class 2 ngày, Second Class 3 ngày, Standard Class 5 ngày, Same Day 0 ngày. Trên test, 12.340 đơn có cam kết thay đổi; tỷ lệ vượt hẹn còn 26,82%, giảm 30,75 điểm phần trăm, trong khi cam kết bình quân tăng khoảng 0,94 ngày. Duration thực tế giữ nguyên 3,50 ngày vì đây là phép tính hồi cứu trên cùng đơn, không có can thiệp vận hành.

Phân vị 90% và 95% cho cùng cam kết trên mẫu này: First Class 2 ngày, Second Class 6 ngày, Standard Class 6 ngày, Same Day 1 ngày. Tỷ lệ vượt hẹn test bằng 0 là kết quả của phân phối nguồn có miền giá trị hẹp; không suy ra độ tin cậy 100% ở đơn tương lai. Đặc biệt, Same Day chuyển thành 1 ngày làm thay đổi lời hứa dịch vụ; chỉ có thể trình như phương án dịch vụ ngày kế tiếp riêng, không tiếp tục gọi đó là giao trong ngày.

Ở kịch bản phân vị 90%, không xuất hiện khác biệt cam kết giữa các vùng trong cùng phương thức; 201 đơn test thuộc nhóm phải lùi về phân vị phương thức. Chưa có lý do từ kết quả này để tạo một hệ thống cam kết khác nhau cho mọi vùng. Phân vị 80% có thể khác theo nhóm; xem bảng chi tiết trước khi cân nhắc độ phức tạp chính sách.

### 3.3. Đánh đổi theo từng phương thức

{table(['Phương thức','Số đơn test','Cam kết cũ → kịch bản giới hạn','Vượt hẹn cũ','Vượt hẹn kịch bản'],[[x.shipping_mode,x.n,str(x.current_days)+' → '+str(x.proposed_days)+' ngày',f'{x.current_late_rate:.2%}',f'{x.proposed_exceedance_rate:.2%}'] for x in pd.read_csv(O/'pilot_by_mode_test.csv').itertuples()])}

Giới hạn +1 ngày chưa đủ tạo mức đúng hẹn cao cho Second Class: tỷ lệ vượt hẹn vẫn 60,52% trên test. Với Standard Class, tỷ lệ này còn 19,87%. Vì vậy không chọn phương án +1 ngày làm cam kết chính thức chỉ vì KPI toàn mẫu giảm; cần đối chiếu riêng mục tiêu dịch vụ của từng phương thức. Phương án phân vị 90% đưa Second Class và Standard Class lên 6 ngày, giảm tỷ lệ vượt hẹn lịch sử nhưng kéo dài lời hứa đáng kể. Cần cân nhắc khả năng khách chấp nhận, không tự suy ra phương án tối ưu lợi nhuận.

Độ nhạy đo lường: giữ toàn bộ test cho tỷ lệ vượt hẹn kịch bản 26,82%; chỉ giữ 12.340 đơn có timestamp nhất quán cho 25,21%, với tỷ lệ hiện tại 57,78%. Mẫu sau loại toàn bộ 731 đơn Same Day, nên chỉ là kiểm tra độ nhạy, không thay thế đánh giá bốn phương thức. Chi tiết ở `results/pilot_duration_sensitivity.csv`.

### 3.4. Khuyến nghị cam kết có điều kiện

**Khuyến nghị 1:** ưu tiên rà soát First Class và Second Class. Trình First Class 2 ngày để xác minh và thí điểm; với Second Class trình rõ lựa chọn 3 ngày còn vượt hẹn cao và lựa chọn 6 ngày có lời hứa dài hơn. Với Standard Class so sánh 5 và 6 ngày theo mục tiêu được giao. Giữ Same Day ở 0 ngày trong phương án bảo toàn tên dịch vụ; không coi việc đổi thành 1 ngày là cải thiện giao trong ngày. Mục tiêu là cam kết phù hợp hơn với năng lực được quan sát; không ghi là giao nhanh hơn hay loại bỏ được nguyên nhân trễ.

Nếu quản lý cho phép nới tối đa một ngày và chấp nhận mức vượt hẹn mục tiêu phù hợp kết quả validation thì chuyển phương án giới hạn sang pilot; ngược lại giữ cam kết và xác định nhu cầu cải thiện vận hành. Nếu yêu cầu mức đúng hẹn cao hơn, trình các phương án phân vị cùng phần tăng thời gian cam kết và đánh giá ảnh hưởng trải nghiệm khách. Cần chốt trước: tỷ lệ vượt hẹn cho phép, giới hạn ngày cam kết, định nghĩa ngày, lời hứa Same Day và giới hạn chất lượng dịch vụ.

Pilot cần theo dõi cả tỷ lệ vượt hẹn, thời gian thực nhận, khiếu nại và tỷ lệ chấp nhận lời hứa. Chưa có các dữ liệu sau trong bộ hiện tại; không tự gán lợi ích giữ khách hoặc doanh thu.

## 4. Sử dụng P_Late để thiết kế ưu tiên xử lý

Trên test có First Class 1.974 đơn, Second Class 2.586, Same Day 731 và Standard Class 7.780. Ngưỡng 0,5 của TV4 tạo 4.560 cảnh báo, với 4.057 cảnh báo đúng và 503 cảnh báo sai; đây là hiệu suất nhận diện lịch sử, không phải 4.057 đơn đã được cứu khỏi trễ.

**Khuyến nghị 2:** dùng P_Late để ưu tiên rà soát ở cấp phương thức, đồng thời thu thập chi phí và đo hiệu quả can thiệp trước khi chọn ngưỡng kinh doanh. Chưa đủ dữ liệu để tuyên bố ROI hoặc tự động xếp hạng đơn cùng phương thức.

Công thức kịch bản cho một hành động đủ điều kiện: EV_i = p_i × e_i × L_i − C_i; trong đó p_i là nguy cơ trễ theo cam kết hiện tại, e_i là tỷ lệ ngăn trễ có điều kiện khi can thiệp vào đơn sẽ trễ, L_i là tổn thất tránh được mỗi đơn, C_i là chi phí hành động cho mỗi đơn được xử lý. e, L và C đều chưa có trong dữ liệu; nguồn cần bổ sung là thử nghiệm vận hành, chăm sóc khách hàng và kế toán. Không gán chúng thành dữ kiện thực tế.

Nếu EV_i > 0 và còn năng lực xử lý thì xem xét hành động; ngược lại không phân bổ thêm nguồn lực chỉ dựa trên cảnh báo. Khi eL > 0, ngưỡng hòa vốn p* = C/(eL). Kiểm tra độ nhạy theo từng giá trị do quản lý cung cấp và tính lại nếu năng lực bị giới hạn. Trường hợp các đơn có cùng xác suất, cần quy tắc vận hành đã phê duyệt để phá hòa; chưa thể gọi là xếp hạng rủi ro cá nhân.

P_Late hiện dự báo nhãn theo cam kết cũ. Sau khi đổi cam kết, không tái sử dụng các xác suất này như xác suất vượt cam kết mới; cần đánh giá hoặc ước lượng lại mục tiêu tương ứng. Không đưa xác suất đơn DataCo vào các điểm Solomon do không có quan hệ ghép.

## 5. Thử nghiệm xếp tuyến Solomon VRPTW

### 5.1. Nguồn và mô hình

Chọn trước khi chạy ba instance C101, R101, RC101, mỗi instance gồm kho 0 và 100 khách; đây là phạm vi thử nghiệm giới hạn, không đại diện toàn bộ benchmark hay đường nội thành thực tế. Tệp có số xe tối đa 25 và sức chở 200 đơn vị tải. Giữ tọa độ, nhu cầu, cửa sổ thời gian và thời gian phục vụ của tệp.

Tham chiếu phương pháp và nguồn gốc: [SINTEF Solomon benchmark](https://www.sintef.no/projectweb/top/vrptw/solomon-benchmark/) và [danh mục 100 khách](https://www.sintef.no/projectweb/top/vrptw/100-customers/). Tải ZIP trực tiếp SINTEF bị HTTP 403; tệp thực nghiệm lấy từ bản sao công khai trong `data/solomon` của [kho lưu bản sao](https://github.com/ashishshukla77/solomon-vrptw-optimization). Chưa đối chiếu được byte với ZIP gốc; URL và SHA-256 tệp đã lưu trong manifest. Chỉ dùng các tệp dữ liệu, không lấy kết quả hay mã giải của kho bản sao làm kết quả của nhóm.

Mục tiêu của lượt giải tuyến là giảm tổng quãng đường dưới giới hạn đội xe, không gán chi phí cố định mỗi xe. Bổ sung kiểm tra cận dưới để chứng minh số xe tối thiểu ở trường hợp đủ điều kiện, trình bày ở mục 5.3; không xem số xe OR-Tools trả về mặc nhiên là tối thiểu. Ràng buộc: mỗi khách được phục vụ đúng một lần; mọi xe xuất phát và về kho; tổng nhu cầu trên tuyến không vượt Q; bắt đầu phục vụ trong cửa sổ khách; được chờ; về kho trước hạn. Cửa sổ áp dụng cho thời điểm bắt đầu phục vụ. Không cho phép bỏ khách.

Đối chứng “điểm gần nhất khả thi”: lần lượt xây từng tuyến, chọn khách chưa phục vụ gần nhất trong số khách đáp ứng sức chở, cửa sổ và khả năng về kho; nếu hết lựa chọn thì đóng tuyến và mở xe mới. Khi không thể phục vụ đủ khách trong K xe thì báo chưa tìm được, không coi là một tuyến hợp lệ.

OR-Tools dùng parallel cheapest insertion, sau đó guided local search, giới hạn 8 giây/lượt. Khi đối chứng có tuyến khả thi, dùng làm lời giải khởi tạo. Hướng xây dựng dựa trên [tài liệu VRPTW của Google](https://developers.google.com/optimization/routing/vrptw). Khoảng cách Euclid và thời gian di chuyển được làm tròn lên ở độ phân giải 0,001 để dùng số nguyên; tổng khoảng cách báo cáo được tính lại bằng số thực. Vì quy ước số học và mục tiêu khác bảng SINTEF, không so sánh trực tiếp như cùng điều kiện, không tuyên bố tối ưu toàn cục.

### 5.2. Kết quả thực chạy

{table(['Instance','Kịch bản','Phương pháp','K tối đa','Q','Xe dùng','Quãng đường (đơn vị benchmark)'],route_rows)}

Trên C101 cơ sở, đối chứng và OR-Tools đều phục vụ đủ 100 khách và qua kiểm tra. Quãng đường giảm từ {d0:.2f} xuống {d1:.2f} đơn vị, tương ứng **{(1-d1/d0)*100:.2f}%**; xe sử dụng giảm từ 21 xuống 10 trong giới hạn cùng K=25. Đây là mức cải thiện so với đúng heuristic tham lam được triển khai, có thể lớn do đối chứng còn yếu; không dùng như mức tiết kiệm doanh nghiệp hay đại diện toàn bộ benchmark.

R101 và RC101: đối chứng không tìm được tuyến hoàn chỉnh trong giới hạn 25 xe, còn OR-Tools tìm được. Không tính phần trăm tiết kiệm cho hai trường hợp này vì không có mẫu số đối chứng khả thi. Không diễn giải thất bại thuật toán là bằng chứng bài toán vô nghiệm.

Độ nhạy trên C101: giảm sức chở xuống 160 cho lời giải OR-Tools dùng 13 xe, quãng đường 1.069,11 đơn vị; tăng lên 240 cho kết quả quan sát không cải thiện so với Q=200. Với K=10, Q=200 vẫn tìm được lời giải khả thi. Các mức quãng đường chưa được chứng minh tối ưu; kết luận riêng về số xe được kiểm tra bằng cận dưới ở mục 5.3. Chưa có căn cứ nói tăng Q không bao giờ có lợi.

### 5.3. Câu trả lời cho “cần bao nhiêu xe?”

Với đội xe đồng nhất, mỗi xe chạy một tuyến kho–khách–kho trong mô hình, cận dưới từ sức chở là **LB = ceil(tổng nhu cầu / Q)**. Đây là điều kiện cần, chưa đủ bảo đảm cửa sổ thời gian. Số xe của một lời giải đã kiểm tra là cận trên khả thi. Nếu hai cận bằng nhau, số xe tối thiểu được chứng minh cho chính cấu hình đó; không đồng nghĩa quãng đường cũng tối ưu.

{table(['Instance / cấu hình','Tổng nhu cầu','Q','Cận dưới số xe','Xe trong lời giải khả thi','Kết luận về số xe'],[[x['instance'].upper()+' / '+x['scenario'],x['total_demand'],x['vehicle_capacity'],x['capacity_lower_bound'],x['feasible_vehicles_used'],'Tối thiểu đã chứng minh' if x['minimum_fleet_certified'] else 'Chưa chứng minh tối thiểu'] for x in fleet_bounds])}

**C101, Q=200:** tổng nhu cầu là 1.810 đơn vị tải, nên LB=ceil(1.810/200)=10. Đội 9 xe chỉ chở tối đa 1.800 đơn vị, không đủ. Lời giải đã lưu dùng đúng 10 xe và phục vụ đủ 100 khách, không vi phạm tải hoặc khung giờ. Do đó, **10 xe là số xe tối thiểu trong mô hình C101 với Q=200**, với quãng đường của lời giải tìm được là 828,94 đơn vị. Kết luận này được suy ra từ cận dưới và lời giải khả thi đã kiểm chứng, không phải tuyên bố OR-Tools chứng minh tối ưu toàn bộ bài toán.

R101, RC101 và C101 với Q khác 200 còn khoảng cách giữa hai cận, nên chỉ báo cáo số xe khả thi tìm được. Không chuyển kết luận 10 xe của C101 thành nhu cầu xe của DHL. Muốn tối ưu cơ cấu loại xe cần thêm sức chở, chi phí, số lượng sẵn có và giới hạn vận hành theo loại; chưa có các đầu vào đó trong thực nghiệm này.

**Khuyến nghị 3:** dùng OR-Tools làm công cụ tạo phương án tuyến ứng viên. Nếu phương án phục vụ đủ khách, không vi phạm tải/khung giờ và có quãng đường thấp hơn đối chứng khả thi thì ưu tiên đưa sang kiểm tra nghiệp vụ; ngược lại giữ đối chứng hoặc điều chỉnh K/Q và chạy lại. Nếu đối chứng không khả thi, chỉ so sánh khả năng phục vụ, chưa công bố tỷ lệ tiết kiệm. Trước áp dụng thực tế cần kho, tọa độ khách, nhu cầu, xe và ma trận thời gian đường bộ đúng ngày giao.

## 6. Quy đổi nhiên liệu và kiểm tra độ nhạy

Solomon dùng đơn vị benchmark, chưa có căn cứ coi một đơn vị là một km đường bộ. Vì vậy bảng nhiên liệu chỉ là mô phỏng: km_kịch_bản = D × a; lít = km_kịch_bản × c/100; chi phí = lít × P. Với a là km/đơn vị benchmark, c là lít/100 km và P là VNĐ/lít.

Lưới giả định minh họa: a ∈ {{0,5; 1; 2}}, c ∈ {{8; 12; 16}}, P ∈ {{18.000; 22.000; 26.000}}. Đây là các giá trị kịch bản để kiểm tra độ nhạy, không phải thông số xe hay giá nhiên liệu Việt Nam đã thu thập. Khi có nguồn doanh nghiệp, thay tham số và ghi ngày/nguồn; chưa dùng giá hiện hành trong báo cáo này.

Ví dụ minh họa a=1, c=12, P=22.000: chi phí C101 đối chứng xấp xỉ {trieu(d0*0.12*22000)} triệu VNĐ/kịch bản, OR-Tools xấp xỉ {trieu(d1*0.12*22000)} triệu VNĐ/kịch bản, chênh lệch xấp xỉ {trieu((d0-d1)*0.12*22000)} triệu VNĐ/kịch bản. Đây không phải tiền tiết kiệm thực tế. Với cùng a,c,P và tiêu hao tuyến tính, phần trăm giảm chi phí bằng phần trăm giảm quãng đường trong mọi tổ hợp. Không coi đây là bằng chứng tác động của tải, tắc đường hoặc chạy không tải; chưa có chi phí tài xế/thuê xe để tính tổng chi phí hoặc ROI.

## 7. Sổ giả định bổ sung của TV5

{table(['Mã','Quy ước/giả định','Nguồn/cách kiểm tra'],[
['P01','Mục tiêu đúng hẹn 80/90/95%','Kịch bản; quản lý chưa duyệt; so sánh độ dài cam kết và vượt hẹn'],
['P02','Nhóm train tối thiểu 100 đơn','Quy tắc thực nghiệm; kiểm tra lại ở 50 và 200'],
['P03','Duration nguồn không đổi khi đổi lời hứa','Giả định hồi cứu; cần pilot đo thời gian thực nhận'],
['P04','Phương án giới hạn +1 ngày, Same Day=0','Kịch bản; cần chốt giới hạn thương mại và mục tiêu dịch vụ'],
['P05','e,L,C của can thiệp chưa biết','Thu thập từ pilot/kế toán; chưa công bố ROI'],
['P06','K/Q cơ sở theo tệp Solomon; biến thể C101 ghi riêng','Q không có đơn vị kg đã xác thực; không đổi nhu cầu gốc'],
['P07','Khoảng cách Euclid, thời gian bằng khoảng cách benchmark','Nguồn SINTEF; kiểm tra lại tuyến số thực; chưa có đường bộ'],
['P08','a,c,P là lưới minh họa','27 tổ hợp mỗi lời giải khả thi; thay bằng dữ liệu có nguồn khi triển khai'],
['P09','Giới hạn giải 8 giây/lượt','Quãng đường chưa chứng minh tối ưu; số xe chỉ chứng nhận khi lời giải đạt cận dưới tải'],
['P10','Một xe chạy một tuyến, tải cộng dồn, đội xe đồng nhất trong mỗi cấu hình','Điều kiện áp dụng cận dưới ceil(tổng nhu cầu/Q); không mở rộng sang nhiều chuyến hoặc đội xe hỗn hợp'],
['P11','DHL là bối cảnh, DataCo/Solomon là dữ liệu thực nghiệm riêng','Không gán kết quả benchmark cho DHL; lưu riêng nguồn bối cảnh và manifest dữ liệu']])}

## 8. Quy tắc ra quyết định và bàn giao

- Nếu tỷ lệ vượt cam kết của phương thức trên validation lớn hơn ngưỡng τ được doanh nghiệp chốt, rà soát mức cam kết hoặc năng lực thực hiện; ngược lại giữ phương án và theo dõi. Không dùng một τ chung nếu các dịch vụ có yêu cầu khác nhau.
- Nếu mức cam kết ứng viên vượt giới hạn ngày cho phép, không triển khai chỉ để đạt KPI đúng hẹn; giữ lời hứa và đưa nhu cầu cải thiện vận hành vào quyết định của quản lý.
- Nếu EV của một hành động lớn hơn 0 theo tham số có căn cứ và còn năng lực xử lý, ưu tiên hành động; ngược lại chưa phân bổ thêm ngân sách dựa trên P_Late. Chưa đủ đầu vào để chốt ngưỡng tiền thực tế.
- Nếu tuyến ứng viên phục vụ đủ khách, đáp ứng ràng buộc và giảm quãng đường so với đối chứng khả thi, chọn làm phương án kiểm tra nghiệp vụ; ngược lại giữ đối chứng hoặc điều chỉnh cấu hình. Không tính mức tiết kiệm từ đối chứng thất bại.

### Bàn giao kết quả

TV6 ghép kết quả cam kết với P_Late bằng order_id dạng Text; dùng cùng test để đối chiếu và không gộp train/validation thành hiệu quả ngoài mẫu. Dashboard cần nhãn riêng cho cam kết mới, thời gian giao thực tế, tỷ lệ vượt hẹn kịch bản, quãng đường benchmark và chi phí mô phỏng. Bản đồ tuyến nằm ở hệ tọa độ Solomon; không vẽ lên địa lý DataCo.

Nhóm cần chốt ba lựa chọn: (1) mức dịch vụ và số ngày được phép nới; (2) cách giữ lời hứa Same Day; (3) giá trị quy đổi nhiên liệu có nguồn hay giữ toàn bộ dưới dạng kịch bản. Sau khi chốt, cập nhật khuyến nghị cuối nhưng không sửa kết quả lịch sử để khớp mục tiêu.

Tệp bàn giao chi tiết nằm trong README. Các kết quả đã được gom thành bộ độc lập trong thư mục 10-11, gồm báo cáo Word, dữ liệu đầu vào gọn, kết quả, hình tuyến, mã nguồn và bằng chứng đối chiếu. Kiểm chứng độc lập đọc lại CSV/JSON đã đối chiếu số đơn, khóa, tỷ lệ, khoảng cách, phục vụ đủ khách, tải, cửa sổ và phép quy đổi nhiên liệu; kết quả lưu `results/verification.json`. Kết quả lịch sử và benchmark chưa chứng minh hiệu quả nhân quả hay hiệu quả triển khai hiện tại.

## Nguồn nội bộ đã đọc

- TV2: README; docs/07_du_lieu_cho_phan_tich.md; docs/05_so_gia_dinh.md và analysis_schema.json.
- TV3: BAO_CAO_MO_TA_VA_CHAN_DOAN.md, các bảng bàn giao mô tả và kiểm định.
- TV4: README; báo cáo Word; NHAT_KY_CONG_VIEC.md; model_selection.json, mode_baseline_train.csv, thresholds_validation.csv và predictions_test.csv.
- Đề bài BTN_ChuDe.pdf trang 40–41 và bảng phân công: phần TV5 hạn 10/11.
- Workbook HỆ HỖ TRỢ QĐ & TTKD - HK261.xlsx: sheet PHÂN CÔNG hàng 13 (TV5 hạn 10/11), sheet CÁC CÔNG TY ĐỀ XUẤT ô B4 (DHL); sheet PROMPT ô C2 (link DataCo). Workbook được đọc làm tài liệu tham chiếu, không chỉnh sửa.
- Dang, Y., Allen, T. T., Singh, M., Gillespie, J., Cox, J., & Monkmeyer, J. (2024). Innovative Integer Programming Software and Methods for Large-Scale Routing at DHL Supply Chain. INFORMS Journal on Applied Analytics, 54(1), 20–36. https://doi.org/10.1287/inte.2023.0087. Chi tiết Round Trip/OR-Tools ở trang 25; bản nghiên cứu công khai: https://courses.ie.bilkent.edu.tr/ie479/wp-content/uploads/sites/16/2024/11/Innovative-Integer-Programming-Software-and-Methods-forLarge-Scale-Routing-at-DHL-Supply-Chain.pdf.
'''
(R/'evidence/noi_dung_bao_cao.md').write_text(text)
print('Report written:',len(text),'characters')
