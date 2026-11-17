# Delivery Insights, bản web

Bảng điều khiển chạy trong trình duyệt, cùng nội dung bốn trang với báo cáo Power BI:
Tổng quan, Rủi ro, Cam kết, Tuyến giao. Bộ lọc, ngưỡng cảnh báo, phương án cam kết và giả định
nhiên liệu đều chạy thật; mọi con số được tính lại theo lựa chọn, không có số cố định.

## Mở và chia sẻ

Mở `index.html` bằng Edge, Chrome hoặc Firefox mới. Đây là một file duy nhất (khoảng 130 KB), không
cần cài gì, không gọi dịch vụ ngoài và hoạt động khi không có mạng. Có thể gửi file qua chat hoặc email.

Đưa lên mạng để có đường link (miễn phí, trang tĩnh):

- **GitHub Pages:** copy `index.html` vào thư mục `docs/` của repo, vào Settings, Pages, chọn nhánh
  và thư mục `/docs`.
- **Netlify hoặc Cloudflare Pages:** kéo thả thư mục chứa `index.html` vào trang Deploy.
- **Chạy tại máy khi trình chiếu:** `python -m http.server` trong thư mục này rồi mở `localhost:8000`.

Địa chỉ có đuôi `#p1` đến `#p4` mở thẳng một trang.

## Cập nhật dữ liệu

```powershell
.venv/Scripts/python scripts/build_dashboard_web.py
```

Lệnh đọc `data/dashboard/*.csv`, gom thành bốn khối nhỏ (toàn bộ đơn theo phương thức, thị trường,
vùng, tháng; tập kiểm tra theo xác suất dự báo; các kịch bản cam kết; các phương án tuyến) và ghi lại
`index.html`. Nguồn nằm cạnh file này:

| File | Vai trò |
| --- | --- |
| `template.html` | Khung bốn trang, thanh bên, ngăn lịch trình |
| `style.css` | Chất liệu nổi và lõm, bảng màu, chuyển động |
| `app.js` | Trạng thái bộ lọc, tính tổng hợp, vẽ biểu đồ, tương tác |

Sửa ba file này rồi build lại; không sửa `index.html` bằng tay.

## Kiểm tra

```powershell
.venv/Scripts/python scripts/check_dashboard_web.py
```

Lệnh build lại, chạy trang trong trình duyệt không giao diện và so các tổng hợp (đơn, đơn trễ, ngày
cam kết và thực tế, cảnh báo ở ba ngưỡng, năm kịch bản cam kết) với pandas trên CSV gốc cho 17 tổ hợp
bộ lọc, đồng thời vẽ cả bốn trang dưới bộ lọc, kể cả cấu hình không có lời giải. Kết quả hiện tại:
153 phép so sánh, không lệch.

## Cách bộ lọc hoạt động

Bộ lọc dùng chung cho mọi trang như nhóm đồng bộ trong Power BI. Chọn phương thức (hoặc bấm vào thẻ,
cột, hàng của phương thức đó) thì các chỉ số tổng đổi theo, còn các biểu đồ so sánh giữa phương thức vẫn
hiện đủ nhóm và làm mờ nhóm không được chọn. Chọn thị trường thì vùng giao chỉ còn các vùng thuộc thị
trường đó. Bấm một dòng ở bảng phương án cam kết hoặc bảng cấu hình tuyến để chọn nó.

## Điều không đổi so với Power BI

Cùng định nghĩa chỉ số, cùng mẫu số (62.897 đơn; 13.071 đơn kiểm tra), cùng lưu ý về phương pháp:
AP không đổi theo vùng; thay đổi cam kết không phải giao nhanh hơn; sơ đồ Solomon không phải đường bộ;
nhiên liệu là giả định mô phỏng; không có đối chứng khả thi thì để trống tỷ lệ giảm, không quy về 0.
Giá trị mặc định: ngưỡng 0,50, phương án "Thêm một ngày", tuyến C101 tải 200 tối đa 25 xe OR Tools,
1 km mỗi đơn vị, 10 lít mỗi 100 km, 22.000 VND mỗi lít.

## Giới hạn

- Cần trình duyệt có `color-mix` và `zoom` (Edge, Chrome, Safari, Firefox từ bản 2024 trở lên).
  Hiệu ứng mở vòng tròn khi đổi sáng và tối chỉ có ở Chrome và Edge, trình duyệt khác đổi tức thì.
- Bố cục thiết kế cho màn hình rộng; trang tự co theo bề ngang cửa sổ, không có bố cục riêng cho điện thoại.
- Dữ liệu là bản chụp tại thời điểm build; không tự làm mới.
