# Bằng chứng kiểm tra Dashboard

- input_validation.json: 81 kiểm tra đầu vào, checksum nguồn và bảng xuất.
- powerbi_validation.json: schema JSON, tham chiếu field và bố cục; không chạy DAX/M/native render.
- preview_validation.json: kiểm tra tương tác trong trình duyệt cho bản xem trước độc lập.

Không dùng kết quả lịch sử của TV2–TV5 thay bằng chứng lượt chạy hiện tại.

- native_dax_validation.json: 21 phép đối chiếu đã thực thi trên engine Power BI Desktop cục bộ.
- native_render_validation.json: bằng chứng mở/chụp các trang native, tách khỏi preview HTML.
