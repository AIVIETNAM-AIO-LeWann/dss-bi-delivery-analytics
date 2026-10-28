# 1. Nguồn và mô tả dữ liệu

## Nguồn sử dụng thực tế

- Tên hiển thị: **DataCo Supply Chain dataset**.
- Nhà đăng trên Kaggle: `saicharankomati`.
- Trang người dùng cung cấp: <https://www.kaggle.com/datasets/saicharankomati/dataco-supply-chain-dataset/data>.
- File: `DataCoSupplyChainDataset.csv`, **95.729.629 byte**.
- Bản tải được ghim: `datasetVersionNumber=1`, ngày tải theo giờ Việt Nam **26/10/2026**.
- Archive chỉ chứa CSV chính; không có Data Dictionary hay access logs.
- SHA-256 và thời điểm tải UTC được lưu tại [source_manifest.json](source_manifest.json).

Không coi bản Kaggle và mọi phiên bản trên Mendeley là cùng một file nếu chưa so
checksum. Các kết quả trong repo chỉ áp dụng cho file đã ghi nhận trong manifest.

## Nguồn xuất bản và tài liệu đối chiếu

Nguồn tham chiếu là **DataCo SMART SUPPLY CHAIN FOR BIG DATA ANALYSIS**, tác giả
Fabian Constante, Fernando Silva và António Pereira, Mendeley Data, V5, công bố
12/03/2019; DOI **10.17632/8gx2fvg2k6.5**.

- Trang gốc: <https://data.mendeley.com/datasets/8gx2fvg2k6/5>.
- Giấy phép ghi tại nguồn gốc: **CC BY 4.0**. Đây là thông tin nguồn Mendeley;
  chưa xác minh metadata giấy phép riêng của nhà đăng Kaggle qua API.
- Từ điển gốc được đối chiếu trên trang file phiên bản 1:
  <https://data.mendeley.com/datasets/8gx2fvg2k6/1/files/29dc7b05-dda6-4834-8354-5b5cc44430df>.
- Nguồn gốc còn mô tả file clickstream và file mô tả biến; hai file đó không nằm
  trong archive Kaggle đã tải, không được giả vờ là đầu vào đã xử lý.

Ghi công đề xuất: “Constante, F., Silva, F., & Pereira, A. (2019). DataCo SMART
SUPPLY CHAIN FOR BIG DATA ANALYSIS, Mendeley Data, V5,
doi:10.17632/8gx2fvg2k6.5. Bản CSV tải qua Kaggle của saicharankomati;
nhóm chuẩn hóa kiểu dữ liệu, lọc cột và tạo các biến dẫn xuất.”

## Đặc tính đã kiểm tra từ CSV

| Thuộc tính | Kết quả |
| --- | --- |
| Kích thước | 180.519 dòng, 53 cột |
| Đơn vị quan sát | Một dòng hàng trong một đơn; được xác nhận qua hai khóa |
| Khóa dòng | `Order Item Id`: 180.519 giá trị duy nhất, không thiếu |
| Khóa đơn | `Order Id`: 65.752 giá trị duy nhất; lặp hợp lệ ở bảng dòng hàng |
| Khoảng thời điểm đặt | 01/01/2015 00:00 – 31/01/2018 23:38 |
| Khoảng timestamp shipment | 03/01/2015 00:00 – 06/02/2018 22:14 |
| Phương thức vận chuyển | Standard Class, First Class, Second Class, Same Day |
| Vùng/thị trường | 23 Order Region; 5 Market; 164 Order Country |
| Sản phẩm | 118 mã sản phẩm, 51 mã danh mục, 50 tên danh mục |
| Nhóm trường | Đơn/dòng hàng; shipping; địa lý; sản phẩm; khách hàng; giá trị tiền |
| Encoding xử lý | Windows-1252, giải mã nghiêm ngặt; đầu ra UTF-8 BOM |

Không diễn giải 180.519 dòng thành 180.519 đơn. Không mặc định tên danh mục là khóa
duy nhất vì số mã và số tên khác nhau. Số liệu xuất bản “khoảng 180 nghìn” chỉ là
tham chiếu, không phải tổng kiểm soát độc lập của doanh nghiệp.

## Phù hợp với chủ đề 18 và giới hạn

DataCo cho phép mô tả và so sánh nhãn trễ theo phương thức, vùng và thời gian, đồng
thời chuẩn bị bài toán dự báo tại lúc đặt hàng. Nó không chứa lịch sử sự kiện đủ
để chứng minh mọi trường candidate thực sự đã được biết tại mốc dự báo.

Từ điển gốc gọi `shipping date (DateOrders)` là timestamp shipment, không xác nhận
là thời điểm khách nhận hàng. Báo cáo dùng các chỉ báo shipping của nguồn; chưa
đánh đồng chúng với thời gian giao tận tay được đo độc lập.

`Latitude` và `Longitude` là vị trí cửa hàng theo từ điển gốc. `Order City`,
`Order Country`, `Order Region` mới mô tả địa bàn đích. Không có tuyến thực,
thứ tự điểm dừng, vị trí kho xuất phát xác thực, sức chở xe, khung giờ nhận hàng,
nhiên liệu hoặc chi phí vận tải. Không dựng kết luận tiết kiệm tuyến từ CSV này.

Đề môn học, trang 40–41 của `BTN_ChuDe.pdf`, gợi ý **Solomon VRPTW** để làm phần
tối ưu tuyến. Phần hiện tại chỉ xử lý DataCo; dữ liệu Solomon chưa tải và chưa có
Data Dictionary trong repo. Kết quả benchmark Solomon sau này phải được trình bày
đúng là benchmark, không phải cải thiện tuyến đã quan sát của DataCo.

Dữ liệu thuộc giai đoạn 2015–2018, bối cảnh quốc tế. Chưa có căn cứ chuyển thẳng
kết luận sang doanh nghiệp Việt Nam hiện tại. Không gán múi giờ, loại tiền, ngày
lễ, khoảng cách hay chi phí nhiên liệu khi nguồn chưa đủ thông tin.
