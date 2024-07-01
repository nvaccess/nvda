# Các tính năng Mới của NVDA


## 2024.2

Một tính năng mới, tên gọi tách âm thanh.
Tính năng này cho phép đặt âm thanh NVDA vào một kênh (ví dụ như bên trái) trong khi âm thanh từ tất cả ứng dụng khác sẽ được đặt ở một kênh khác (ví dụ như bên phải).

Có thêm lệnh mới để tùy chỉnh vòng thiết lập cho giọng đọc, cho phép người dùng đi đến cài đặt đầu tiên hay cuối cùng, và để tăng hoặc giảm giá trị của cài đặt hiện tại bằng các bước nhảy dài hơn.
Cũng có thêm những phím lệnh di chuyển nhanh, cho phép người dùng gán thao tác để di chuyển nhanh giữa: đoạn, đoạn đã căn lề, kiểu văn bản giống nhau, kiểu văn bản khác nhau, mục trình đơn, các nút bật / tắt, thanh tiến độ, hình ảnh, và công thức toán.

Nhiều tính năng mới và sửa lỗi cho chữ nổi.
Đã thêm một chế độ chữ nổi mới gọi là "hiện đầu ra giọng đọc".
Khi kích hoạt, màn hình chữ nổi sẽ hiển thị chính xác những gì NVDA đọc.
Cũng đã thêm hỗ trợ cho các màn hình BrailleEdgeS2 và BrailleEdgeS3.
Đã cập nhật LibLouis, thêm chi tiết mới (xác định chữ hoa) cho các bản chữ nổi tiếng Belarus và Ukraina, bảng chữ nổi tiếng Lào và Tây Ban Nha để đọc văn bản tiếng Hy Lạp.

Đã cập nhật eSpeak, thêm ngôn ngữ mới Tigrinya.

Nhiều bản sửa lỗi nhỏ cho các ứng dụng như Thunderbird, Adobe Reader, trình duyệt web, Nudi và Geekbench.

### Tính năng mới

* Các phím lệnh mới:
  * Lệnh di chuyển nhanh mới `p` để di chuyển đến đoạn văn bản kế/đoạn văn bản trước trong chế độ duyệt. (#15998, @mltony)
  * Lệnh di chuyển nhanh mới, chưa gán thao tác, có thể dùng để di chuyển đến các thành phần kế tiếp hoặc trước đó:
    * nhóm hình ảnh (#10826)
    * căn lề dọc đoạn văn bản (#15999, @mltony)
    * mục trên trình đơn (#16001, @mltony)
    * nút bật / tắt (#16001, @mltony)
    * thanh tiến độ (#16001, @mltony)
    * công thức toán (#16001, @mltony)
    * kiểu văn bản giống nhau (#16000, @mltony)
    * kiểu văn bản khác nhau (#16000, @mltony)
  * Đã thêm lệnh để đi đến các mục đầu tiên, cuối cùng, đi tới và lùi trong vòng thiết lập bộ đọc. (#13768, #16095, @rmcpantoja)
    * Thiết lập cho cài đặt đầu tiên / cuối cùng trong vòng thiết lập bộ đọc chưa được gán hao tác. (#13768)
    * giảm và tăng giá trị hiện tại của vòng thiết lập bộ đọc bằng bước nhảy lớn hơn (#13768):
      * Máy bàn: `NVDA+control+pageUp` và `NVDA+control+pageDown`.
      * Máy xách tay: `NVDA+control+shift+pageUp` và `NVDA+control+shift+pageDown`.
  * Thêm thao tác chưa gán lệnh để bật / tắt thông báo nhóm hình ảnh và phụ đề. (#10826, #14349)
* Chữ nổi:
  * Thêm hỗ trợ cho các màn hình BrailleEdgeS2 và BrailleEdgeS3. (#16033, #16279, @EdKweon)
  * Thêm chế độ chữ nổi mới gọi là "hiển thị đầu ra giọng đọc". (#15898, @Emil-18)
    * Khi kích hoạt, các màn hình chữ nổi sẽ hiển thị chính xác những gì NVDA đọc.
    * Có thể bật / tắt bằng cách bấm `NVDA+alt+t`, hoặc bật / tắt trong hộp thoại cài đặt chữ nổi.
* Tách âm thanh: (#12985, @mltony)
  * Cho phép tách âm thanh NVDA ra một kênh (kênh trái chẳng hạn) trong khi âm thanh của các ứng dụng khác sẽ được đưa vào kênh còn lại (kênh phải).
  * Bật / tắt bằng lệnh `NVDA+alt+s`.
* Đã hỗ trợ thông báo tiêu đề cột và dòng  trong các phần tử HTML có thể chỉnh sửa nội dung. (#14113)
* Đã thêm tùy chọn để vô hiệu hóa thông báo nhóm hình ảnh và phụ đề trong cài đặt định dạng tài liệu. (#10826, #14349)
* Trong Windows 11, NVDA sẽ thông báo các cảnh báo khi nhập bằng giọng nói và các hành động được đề xuất bao gồm gợi ý hàng đầu khi sao chép dữ liệu như số điện thoại vào bộ nhớ tạm (Windows 11 2022 Update trở lên). (#16009, @josephsl)
* NVDA sẽ giữ cho thiết bị âm thanh luôn hoạt động sau khi dừng đọc, để tránh việc bắt đầu đọc phần tiếp theo bị cắt bớt với một số thiết bị âm thanh như tai nghe Bluetooth. (#14386, @jcsteh, @mltony)
* Giờ đây, HP Secure Browser đã được hỗ trợ. (#16377)

### Các thay đổi

* Cửa Hàng Add-on:
  * Phiên bản NVDA thấp nhất và bản thử nghiệm cuối cùng cho một add-on giờ đây đã hiển thị ở phần "các chi tiết khác". (#15776, @Nael-Sayegh)
  * Hoạt động cho phần đánh giá của cộng đồng sẽ hiển thị ở tất cả các thẻ của cửa hàng. (#16179, @nvdaes)
* Cập nhật các thành phần:
  * Cập nhật thư viện phiên dịch chữ nổi LibLouis lên [3.29.0](https://github.com/liblouis/liblouis/releases/tag/v3.29.0). (#16259, @codeofdusk)
    * Chi tiết mới (xác định chữ hoa) cho các bảng chữ nổi Tiếng Belarus và tiếng Ukraina.
    * Bảng tiếng Tây Ban Nha mới để đọc văn bản tiếng Hy Lạp.
    * Bảng chữ nổi mới cho tiếng Lào cấp 1. (#16470)
  * Đã cập nhật eSpeak NG lên 1.52-dev commit `cb62d93fd7`. (#15913)
    * Thêm ngôn ngữ mới Tigrinya.
* Thay đổi vài thao tác cho các thiết bị của BrailleSense nhằm tránh xung đột với kí tự chữ nổi tiếng Pháp. (#15306)
  * `alt+mũi tên trái` giờ đây được gán cho `chấm 2+chấm 7+khoảng trắng`
  * `alt+mũi tên phải` giờ đây được gán cho `chấm 5+chấm 7+khoảng trắng`
  * `alt+mũi tên lên` giờ đây được gán cho `chấm 2+chấm 3+chấm 7+khoảng trắng`
  * `alt+mũi tên xuống` giờ đây được gán cho `chấm 5+chấm 6+chấm 7+khoảng trắng`
* Các dấu chấm đệm thường dùng trong mục lục không còn được thông báo ở cấp dấu câu thấp. (#15845, @CyrilleB79)

### Sửa lỗi

* Sửa lỗi cho Windows 11:
  * NVDA lại một lần nữa thông báo phần cứng cho gợi ý đầu vào bàn phím. (#16283, @josephsl)
  * Trong phiên bản 24H2 (2024 Update và Windows Server 2025), có thể dùng tương tác chuột và tương tác cảm ứng trong các thiết lập nhanh (quick settings). (#16348, @josephsl)
* Cửa Hàng Add-on :
  * Khi bấm `ctrl+tab`, focus di chuyển đến đúng tiêu đề của thẻ mới. (#14986, @ABuffEr)
  * nếu các tập tin cache không chính xác, NVDA sẽ không còn khởi động lại nữa. (#16362, @nvdaes)
* Sửa lỗi cho các trình duyệt dựa trên Chrome khi sử dụng với UIA:
  * Sửa lỗi làm cho NVDA bị treo. (#16393, #16394)
  * Phím xóa lùi giờ đây hoạt động chính xác ở trường đăng nhập của Gmail. (#16395)
* Phím xóa lùi giờ đây đã hoạt động chính xác khi dùng Nudi 6.1 với tính năng "Quản lý phím từ các ứng dụng khác" của NVDA được bật. (#15822, @jcsteh)
* Đã sửa lỗi tọa độ âm thanh sẽ được phát trong khi ứng dụng ở chế độ ngủ và bật tùy chọn "Phát tọa độ âm thanh khi chuột di chuyển" được bật. (#8059, @hwf1324)
* Trong Adobe Reader, NVDA không còn bỏ qua văn bản thay thế đặt trên các công thức trong các tập tin PDF. (#12715)
* Sửa lỗi làm cho NVDA không đọc được ribbon và các tùy chọn trong Geekbench. (#16251, @mzanm)
* Sửa lỗi cho trường hợp hiếm gặp khi lưu cấu hình có thể không lưu được tất cả hồ sơ. (#16343, @CyrilleB79)
* Trong các trình duyệt dựa trên Firefox và Chrome, NVDA sẽ vào chế độ focus một cách chính xác khi bấm enter khi đang đứng tại một danh sách (ul / ol) bên trong nội dung có thể chỉnh sửa. (#16325)
* Trạng thái thay đổi cột giờ đây được thông báo chính xác khi chọn cột để hiển thị trong danh sách thư của Thunderbird. (#16323)
* Dòng lệnh chuyển `-h`/`--help` lại hoạt động chính xác. (#16522, @XLTechie)
* Hỗ trợ của NVDA cho phần mềm phiên dịch Poedit phiên bản 3.4 trở lên hoạt động chuẩn xác khi dịch các ngôn ngữ 1 hoặc nhiều hơn 2 dạng số nhiều (e.g. Chinese, Polish). (#16318)

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.md để biết thêm thông tin.

## 2024.1

+
Đã thêm chế độ đọc theo yêu cầu.
Khi ở trong chế độ này, NVDA không tự động đọc lên (ví dụ như khi di chuyển con trỏ) nhưng vẫn đọc khi gọi một lệnh được gán để thông báo thông tin gì đó (ví dụ như đọc tiêu đề cửa sổ).
Trong phân loại giọng đọc ở phần cài đặt NVDA, đã có thể bỏ đi những chế độ đọc không mong muốn từ lệnh chuyển giữa các chế độ đọc (`NVDA+s`).

Mới: chế độ chọn thực tế (bật / tắt bằng `NVDA+shift+f10`) đã có trong chế độ duyệt của NVDA cho Mozilla Firefox.
Khi được bật lên, việc chọn văn bản trong chế độ duyệt cũng sẽ làm cho Firefox thực hiện vùng chọn của chính nó.
Việc sao chép văn bản với `control+c` sẽ gửi thẳng lệnh này đến Firefox nên nội dung được sao chép sẽ là văn bản đa dạng thức, thay vì chỉ là văn bản trơn của NVDA.

Cửa hàng Add-on giờ đây đã hỗ trợ thao tác hàng loạt (cài đặt, bật / tắt các add-on) bằng cách chọn nhiều add-on
Có thêm hành động để mở trang đánh giá cho add-on đã chọn.

Thiết bị đầu ra âm thanh và các tùy chọn giảm âm  đã bị gỡ khỏi hộp thoại "Chọn bộ đọc".
Có thể tìm thấy chúng trong bản cài đặt âm thanh, mở bằng `NVDA+control+u`.

Đã cập nhật eSpeak-NG, thư viện phiên dịch chữ nổi LibLouis và Unicode CLDR.
Có thêm các bản chữ nổi tiếng Thái Lan, Philippines và Rumani.

Sửa nhiều lỗi, đặc biệt là với Cửa Hàng Add-on, chữ nổi, Libre Office, Microsoft Office và âm thanh.

### Lưu ý quan trọng

* Bản phát hành này không tương thích với các add-on hiện có.
* Không còn hỗ trợ Windows 7 và Windows 8 nữa.
Windows 8.1 là phiên bản thấp nhất được hỗ trợ.

### Tính năng mới

* Cửa hàng Add-on:
  * Cửa hàng Add-on giờ đây hỗ trợ các thao tác hàng loạt (cài đặt, bật / tắt add-on) bằng cách chọn nhiều add-on. (#15350, #15623, @CyrilleB79)
  * Một hành động mới đã được thêm vào để mở một trang web chuyên dụng nhằm xem hoặc cung cấp phản hồi về add-on đã chọn. (#15576, @nvdaes)
* Thêm hỗ trợ cho các màn hình chữ nổi HID dùng công nghệ Bluetooth Low Energy. (#15470)
* Chế độ chọn thực tế (bật / tắt bằng `NVDA+shift+f10`) đã có trong chế độ duyệt của NVDA cho Mozilla Firefox.
Khi được bật lên, việc chọn văn bản trong chế độ duyệt cũng sẽ làm cho Firefox thực hiện vùng chọn của chính nó.

Việc sao chép văn bản với `control+c` sẽ gửi thẳng lệnh này đến Firefox nên nội dung được sao chép sẽ là văn bản đa dạng thức, thay vì chỉ là văn bản trơn của NVDA.
Lưu ý là vì Firefox quản lí thao tác sao chép nên NVDA sẽ không thông báo "chép vào bộ nhớ tạm" trong chế độ này. (#15830)
* Khi sao chép văn bản trong Microsoft Word mà bật chế độ duyệt của NVDA, định dạng văn bản giờ đây đã được bao gồm.
Một tác dụng phụ của việc này là NVDA sẽ không còn báo thông điệp "chép vào bộ nhớ tạm" khi bấm `control+c` ở chế độ duyệt trong Microsoft Word / Outlook, vì việc sao  chép được quản lý bởi những ứng dụng đó chứ không phải bởi NVDA. (#16129)
* Đã thêm lệnh mới cho chế độ đọc: "theo yêu cầu".
Khi ở chế độ đọc theo yêu cầu, NVDA không tự đọc (ví dụ như khi di chuyển con trỏ) nhưng vẫn đọc khi gọi những lệnh có chức năng thông báo điều gì đó (thông báo tiêu đề cửa sổ). (#481, @CyrilleB79)
* Ở phần Tiếng nói trong cài đặt của NVDA, giờ đây đã có thể bỏ qua các chế độ đọc không mong muốn từ lệnh chuyển giữa các chế độ đọc (`NVDA+s`). (#15806, @lukaszgo1)
  * Nếu đang dùng add-on NoBeepsSpeechMode, hãy cân nhắc gỡ bỏ nó đi, rồi tắt các tùy chọn "beeps" và "theo yêu cầu" trong ản cài đặt.

### Các thay đổi

* NVDA không còn hỗ trợ Windows 7 và Windows 8.
Windows 8.1 là phiên bản thấp nhất được hỗ trợ. (#15544)
* Cập nhật các thành phần:
  * Đã cập nhật thư viện phiên dịch chữ nổi LibLouis lên [3.28.0](https://github.com/liblouis/liblouis/releases/tag/v3.28.0). (#15435, #15876, @codeofdusk)
    * Có thêm các bản chữ nổi tiếng Thái Lan, Philippines và Rumani.
  * eSpeak NG đã được cập nhật lên 1.52-dev commit `530bf0abf`. (#15036)
  * Kí hiệu và chú thích biểu tượng cảm xúc CLDR đã được cập nhật lên phiên bản 44.0. (#15712, @OzancanKaratas)
  * Đã cập nhật Java Access Bridge lên 17.0.9+8Zulu (17.46.19). (#15744)
* Phím lệnh:
  * Các phím lệnh sau, giờ đây đã hỗ trợ bấm hai và ba lần để đánh vần thông tin được thông báo và đánh vần với kí tự mô tả: thông báo vùng chọn, thông báo nội dung trong bộ nhớ tạm và thông báo đối tượng có focus. (#15449, @CyrilleB79)
  * Đã có phím tắt mặc định để bật / tắt che màn hình của NVDA: `NVDA+control+escape`. (#10560, @CyrilleB79)
  * Khi bấm bốn lần, lệnh thông báo vùng chọn giờ đây sẽ hiển thị vùng chọn trên một cửa sổ có thể duyệt. (#15858, @Emil-18)
* Microsoft Office:
  * Khi yêu cầu thông tin định dạng trên ô của Excel, đường viền, nền sẽ chỉ được thông báo nếu có định dạng đó. (#15560, @CyrilleB79)
  * NVDA sẽ lại không còn thông báo các nhóm không có nhãn như trình đơn  trong các phiên bản gần đây của Microsoft Office 365. (#15638)
Thiết bị đầu ra âm thanh và các tùy chọn giảm âm  đã bị gỡ khỏi hộp thoại "Chọn bộ đọc".
Có thể tìm thấy chúng trong bản cài đặt âm thanh, mở bằng `NVDA+control+u`. (#15512, @codeofdusk)
* Tùy chọn "Thông báo vai trò khi chuột đi vào đối tượng" trong phân loại thiết lập chuột của NVDA đã được đổi tên thành "Thông báo đối tượng khi chuột đi vào nó".
Tùy chọn này giờ đây thông báo thêm thông tin liên quan về một đối tượng khi chuột đi vào nó, chẳng hạn như trạng thái (đã chọn/đã bấm) hoặc tọa độ ô trong bảng. (#15420, @LeonarddeR)
* Đã thêm tùy chọn vào trình đơn: trang trợ giúp và cửa hàng của NV Access. (#14631)
* Hỗ trợ của NVDA cho [Poedit](https://poedit.net) được cải thiện cho Poedit version phiên bản 3 trở lên.
Người dùng Poedit 1 được khuyến khích cập nhật lên Poedit 3 nếu họ muốn dựa vào khả năng tiếp cận nâng cao trong Poedit, chẳng hạn như các phím tắt để đọc ghi chú và lưu ý cho người phiên dịch. (#15313, #7303, @LeonarddeR)
* Trình hiển thị chữ nổi và trình hiển thị nội dung đọc giờ đây bị vô hiệu trong chế độ bảo vệ. (#15680)
* Trong khi điều hướng đối tượng, các đối tượng bị vô hiệu (không sẵn sàng) sẽ không bị bỏ qua nữa. (#15477, @CyrilleB79)
* Thêm mục lục cho tài liệu danh sách các phím tắt. (#16106)

### Sửa lỗi

* Cửa hàng ad-on:
  * Khi trạng thái của một add-on bị thay đổi trong lúc đang có focus, thay đổi từ "đang tải" thành "đã tải" chẳng hạn, thành phần đã cập nhật giờ đây sẽ được thông báo chính xác. (#15859, @LeonarddeR)
  * Khi cài các add-on, thông báo xác nhận cài đặt không còn bị chồng chéo với hộp thoại khởi động lại. (#15613, @lukaszgo1)
  * Khi cài lại một add-on không tương thích, nó không còn bị buộc vô hiệu nữa. (#15584, @lukaszgo1)
  * Giờ đây, cũng đã có thể cập nhật các add-on đã vô hiệu và không tương thích. (#15568, #15029)
  * NVDA giờ đây sẽ khôi phục và hiển thị lỗi trong trường hợp một add-on không được tải xuống đúng cách. (#15796)
  * NVDA không còn bị lỗi khởi động lại liên tục sau khi mở và đóng Cửa Hàng Add-on. (#16019, @lukaszgo1)

* Âm thanh:
  * NVDA không còn bị treo trong thời gian ngắn khi nhiều âm thanh được phát liên tiếp. (#15311, #15757, @jcsteh)
  * Nếu thiết bị đầu ra âm thanh được đặt thành thiết bị khác với mặc định và thiết bị đó sẽ khả dụng trở lại sau khi không khả dụng, NVDA sẽ chuyển về thiết bị đã định cấu hình thay vì tiếp tục sử dụng thiết bị mặc định. (#15759, @jcsteh)
  * NVDA giờ đây sẽ tiếp tục âm thanh nếu cấu hình của thiết bị đầu ra thay đổi hoặc ứng dụng khác giải phóng quyền kiểm soát độc quyền của thiết bị. (#15758, #15775, @jcsteh)
* Chữ nổi:
  * Các màn hình chữ nổi nhiều dòng sẽ không còn bị lỗi trình điều khiển BRLTTY và được coi là một màn hình liên tục. (#15386)
  * Nhiều đối tượng chứa các văn bản hữu ích đã được nhận dạng, và nội dung văn bản đã hiển thị trong chữ nổi. (#15605)
  * Đầu vào chữ tắt lại hoạt động bình thường trợ lại. (#15773, @aaclause)
  * Chữ nổi giờ đây đã cập nhật khi di chuyển đối tượng điều hướng giữa các ô trong bảng trong nhiều tình huống. (#15755, @Emil-18)
  * Kết quả của các lệnh thông báo focus hiện tại, đối tượng điều hướng hiện tại, và vùng chọn hiện tại giờ đây đã hiển thị trong chữ nổi. (#15844, @Emil-18)
  * Trình điều khiển Albatross không còn quản lí Esp32 microcontroller như một màn hình Albatross. (#15671)

* LibreOffice:
  * Các từ bị xóa bằng phím tắt`control+backspace` giờ đây cũng được thông báo chính xác khi mà theo sau từ đó là khoảng trắng (là dấu cách và tab chẳng hạn). (#15436, @michaelweghorn)
  * Việc thông báo thanh trạng thái bằng phím tắt `NVDA+end`  giờ đây cũng sẽ hoạt động với các hộp thoại trong LibreOffice phiên bản 24.2 và mới hơn. (#15591, @michaelweghorn)
  * Tất cả các thuộc tính văn bản mong đợi hiện được hỗ trợ trong phiên bản LibreOffice 24.2 trở lên.
  Điều này làm cho việc thông báo lỗi chính tả có tác dụng khi thông báo một dòng trong Writer. (#15648, @michaelweghorn)
  * Việc thông báo cấp độ tiêu đề giờ đây cũng đã hoạt động với LibreOffice phiên bản 24.2 trở lên. (#15881, @michaelweghorn)
* Microsoft Office:
  * Trong Excel với UIA bị tắt, chữ nổi đã được cập nhật, và ô đang hoạt động đã được đọc lên khi bấm `control+y`, `control+z` hay `alt+backspace`. (#15547)
  * Trong Word với UIA bị tắt, chữ nổi đã được cập nhật khi bấm `control+v`, `control+x`, `control+y`, `control+z`, `alt+backspace`, `backspace` hay `control+backspace`.
  Nó cũng được cập nhật với UIA được bật, khi đánh văn bản và con trỏ nổi đi theo con trỏ duyệt và con trỏ này đi theo dấu nháy. (#3276)
  * Trong Word, ô đích bây giờ sẽ được báo cáo chính xác khi sử dụng các lệnh gốc của Word để điều hướng trong bảng `alt+home`, `alt+end`, `alt+pageUp` và ``alt+pageDown` `. (#15805, @CyrilleB79)
* Đã cải thiện khả năng thông báo phím tắt của đối tượng. (#10807, #15816, @CyrilleB79)
* Bộ đọc chuẩn SAPI4 giờ đây đã thật sự hỗ trợ các thay đổi âm lượng, tốc độ và cao độ trong cài đặt tiếng nói. (#15271, @LeonarddeR)
* Trạng thái nhiều dòng giờ đây được thông báo chính xác trong các ứng dụng dùng Java Access Bridge. (#14609)
* NVDA sẽ thông báo các nội dung cho nhiều hộp thoại của Windows 10 và 11. (#15729, @josephsl)
* NVDA sẽ không còn bị lỗi khi đọc trang mới tải trong Microsoft Edge khi dùng UI Automation. (#15736)
* Khi dùng lệnh đọc tất cả hay các lệnh để đánh vần văn bản, khoảng ngưng giữa các câu hay kí tự không còn bị giảm dần theo thời gian. (#15739, @jcsteh)
* NVDA không còn tình trạng thỉnh thoảng bị treo khi đọc một lượng văn bản lớn. (#15752, @jcsteh)
* Khi truy cập Microsoft Edge bằng UI Automation, NVDA có khả năng kích hoạt nhiều điều khiển trong chế độ duyệt. (#14612)
* NVDA không còn bị lỗi không khởi động được nữa khi tập tin cấu hình bị hư hỏng,nó sẽ khôi phục cấu hình về mặc định như  đã làm  trước đây. (#15690, @CyrilleB79)
* Sửa lỗi hộ trợ cho hệ thống các điều khiển dạng xem danh sách (`SysListView32`) trong các ứng dụng Windows Forms. (#15283, @LeonarddeR)
* Không thể ghi đè lịch sử Python console của NVDA. (#15792, @CyrilleB79)
* NVDA phải duy trì khả năng phản hồi khi có quá nhiều sự kiện của UI Automation, ví dụ: khi một lượng lớn văn bản được in ra cửa sổ terminal hoặc khi nghe tin nhắn thoại trong trình nhắn tin WhatsApp. (#14888, #15169)
  * Có thể tắt kiểu hoạt động mới này bằng tùy chọn mới "Sử lí sự kiện nâng cao" trong cài đặt nâng cao của NVDA.
* NVDA một lần nữa có thể theo dõi tiêu điểm trong các ứng dụng chạy trong Windows Defender Application Guard (WDAG). (#15164)
* Văn bản không còn được cập nhật khi chuột di chuyển trong Trình Hiển Thị Nội Dung Đọc. (#15952, @hwf1324)
* NVDA sẽ lại chuyển về chế độ duyệt khi đóng các hộp xổ với `escape` hoặc `alt+mũi tên lên` trong Firefox hay Chrome. (#15653)
* Bấm mũi tên lên / xuống ở các hộp xổ trong iTunes sẽ không còn chuyển qua chế độ duyệt ngoài ý muốn. (#15653)

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2023.3.4

Đây là bản  vá nhằm sửa lỗi bảo mật và lỗi bộ cài đặt.
Vui lòng báo các vẫn để theo [chính sách bảo mật của NVDA](https://github.com/nvaccess/nvda/blob/master/security.md).

### Sửa lỗi bảo mật

* Ngăn tải các cấu hình tùy biến` trong khi đang bị buộc chạy ở chế độ bảo vệ.
([GHSA-727q-h8j2-6p45](https://github.com/nvaccess/nvda/security/advisories/GHSA-727q-h8j2-6p45))

### Sửa lỗi

* Sửa lỗi làm cho NVDA không thoát được hoàn toàn. (#16123)
* Sửa lỗi khi  NVDA trước đó đã không tắt được hoàn toàn, và quá trình cài đặt NVDA bị thất bại theo kiểu không thể khôi phục. (#16122)

## 2023.3.3

Đây là bản  vá nhằm sửa các lỗi bảo mật.
Vui lòng báo các vẫn để theo [chính sách bảo mật của NVDA](https://github.com/nvaccess/nvda/blob/master/security.md).

### Sửa lỗi bảo mật

* - Ngăn chặn cuộc tấn công XSS được phản ánh có thể xảy ra từ nội dung được tạo để thực thi mã tùy ý.
([GHSA-xg6w-23rw-39r8](https://github.com/nvaccess/nvda/security/advisories/GHSA-xg6w-23rw-39r8))

## 2023.3.2

Đây là bản  vá nhằm sửa các lỗi bảo mật.
Bản vá lỗi trong 2023.3.1 chưa giải quyết một cách triệt đễ.
Vui lòng báo các vẫn để theo [chính sách bảo mật của NVDA](https://github.com/nvaccess/nvda/blob/master/security.md).

### Sửa lỗi bảo mật

* Bản vá lỗi trong 2023.3.1 chưa giải quyết một cách triệt đễ.
Ngăn chặn khả năng truy cập hệ thống và thực thi mã tùy ý với các đặc quyền hệ thống đối với người dùng chưa được xác thực.
([GHSA-h7pp-6jqw-g3pj](https://github.com/nvaccess/nvda/security/advisories/GHSA-h7pp-6jqw-g3pj))

## 2023.3.1

Đây là bản  vá nhằm sửa các lỗi bảo mật.
Vui lòng báo các vẫn để theo [chính sách bảo mật của NVDA](https://github.com/nvaccess/nvda/blob/master/security.md).

### Sửa lỗi

* Ngăn chặn khả năng truy cập hệ thống và thực thi mã tùy ý với các đặc quyền hệ thống đối với người dùng chưa được xác thực..
([GHSA-h7pp-6jqw-g3pj](https://github.com/nvaccess/nvda/security/advisories/GHSA-h7pp-6jqw-g3pj))

## 2023.3

Bản phát hành này bao gồm những cải tiến về sự vận hành, khả năng phản hồi và tính ổn định của đầu ra âm thanh.
Đã thêm các tùy chọn để điều khiển âm lượng âm thanh và tiếng beep của NVDA, hoặc cho phép chúng đi theo âm lượng của giọng đọc mà bạn đang dùng.

Giờ đây, NVDA có thể định kì làm mới kết quả nhận dạng văn bản (OCR), sẽ đọc nội dung văn bản mới ngay khi nó xuất hiện.
Điều này, có thể thiết lập ở phân loại Windows OCR trong hộp thoại cài đặt NVDA.

Cũng đã sửa vài lỗi liên quan đến chữ nổi, cải thiện khả năng nhận thiết bị và việc di chuyển dấu nháy.
Giờ đây, đã có thể từ chối những trình điều khiển không mong muốn từ việc tự dò tìm thiết bị để cải thiện sự vận hành của công việc này.
Cũng đã có thêm những lệnh mới cho BRLTTY.

Nhiều lỗi cho Cửa Hàng Add-On (Add-on Store), Microsoft Office, trình đơn ngữ cảnh của Microsoft Edge, và Windows Calculator cũng đã được khắc phục.

### Các tính năng mới

* Các cải tiến về quản lí âm thanh:
  * Một bảng thiết lập âm thanh mới:
    * Có thể mở bảng thiết lập này bằng `NVDA+control+u`. (#15497)
  * Tùy chọn trong cài đặt âm thanh để âm lượng âm thanh và tiếng beep của NVDA  đi theo thiết lập âm thanh của giọng đọc mà bạn đang dùng. (#1409)
  * Tùy chọn trong cài đặt âm thanh cho phép cấu hình riêng biệt âm lượng của NVDA. (#1409, #15038)
    * Các thiết lập cho việc thay đổi đầu ra âm thanh và bật / tắt chức năng giảm âm lượng đã được chuyển đến bảng thiết lập âm thanh mới trong hộp thoại chọn bộ đọc.
    Các tùy chọn này sẽ bị gỡ khỏi hộp thoại "chọn bộ đọc" trong phiên bản 2024.1. (#15486, #8711)
  * NVDA giờ đây có thể cho ra âm thanh thông qua Windows Audio Session API (WASAPI), vốn có thể cải tiến việc phản hồi, khả năng vận hành cũng như tính ổn định cho bộ đọc và âm thanh của NVDA. (#14697, #11169, #11615, #5096, #10185, #11061)
  Nếu bật WASAPI thì có thể cấu hình một số thiết lập sau đây.
  * Lưu ý: WASAPI không tương thích với vài add-on.
  Sẽ có cập nhật tính tương thích cho các add-on này. Vui lòng cập nhật chúng trước khi cập nhật NVDA.
  Các phiên bản không tương thích của những add-on này sẽ bị tắt khi cập nhật NVDA:
    * Tony's Enhancements phiên bản 1.15 trở về trước. (#15402)
    * NVDA global commands extension 12.0.8 trở về trước. (#15443)
* NVDA giờ đây có khả năng liên tục cập nhật kết quả khi thực hiện nhận dạng văn bản (OCR), văn bản mới sẽ được đọc khi chúng xuất hiện. (#2797)
  * Để dùng chức năng này, hãy bật tùy chọn "Định kì cập nhật nội dung được nhận dạng" ở phân loại Windows OCR trong hộp thoại cài đặt của NVDA.
  * Khi được bật, bạn có thể bật / tắt việc đọc văn bản mới bằng cách bật / tắt tùy chọn thông báo thay đổi nội dung động (bấm `NVDA+5`).
* Khi dùng chức năng tự dò tìm màn hình chữ nổi, giờ đây đã có thể vô hiệu hóa các trình điều khiển trong hộp thoại chọn màn hình chữ nổi. (#15196)
* Một tùy chọn mới trong cài đặt định dạng tài liệu, "Bỏ các dòng trống khi thông báo thụt lề". (#13394)
* Đã thêm một thao tác chưa gán lệnh để điều hướng qua các điều khiển dạng tab groupings (tạm dịch là điều khiển qua các thẻ) trong chế độ duyệt. (#15046)

### Các thay đổi

* Chữ nổi:
  * Khi thay đổi văn bản trong cửa sổ terminal mà không cập nhật dấu nháy, văn bản trên màn hình chữ nổi giờ đây sẽ cập nhật đúng khi được định vị trên một dòng đã được thay đổi.
  Điều này bao gồm cho các tình huống con trỏ nổi đi theo con trỏ duyệt. (#15115)
  * Nhiều tổ hợp phím của BRLTTY giờ đây đã được gán vào lệnh của NVDA. (#6483):
    * `learn`: Bật / tắt chế độ trợ giúp nhập của NVDA
    * `prefmenu`: Mở trình đơn NVDA
    * `prefload`/`prefsave`: Tải / lưu cấu hình NVDA
    * `time`: Hiện ngày giờ
    * `say_line`: Đọc dòng hiện tại, nơi con trỏ duyệt đang đứng
    * `say_below`: Đọc tất cả, sử dụng con trỏ duyệt
  * Trình điều khiển BRLTTY  chỉ hoạt động khi một phiên bản BRLTTY được bật BrlAPI đang chạy. (#15335)
  * Thiết lập nâng cao để  bật hỗ trợ cho HID braille đã bị gỡ bỏ để thay thế bằng một tùy chọn mới.
  Giờ đây, bạn có thể tắt một trình điều khiển cụ thể cho màn hình chữ nổi thuộc nhóm tự dò tìm trong hộp thoại chọn màn hình chữ nổi. (#15196)
* Cửa hàng add-on: các add-on đã cài đặt giờ đây sẽ được liệt kê ở thẻ Các add-on hiện có, nếu chúng có tồn tại trên cửa hàng. (#15374)
* Đã cập nhật vài phím tắt trên trình đơn NVDA. (#15364)

### Sửa lỗi

* Microsoft Office:
  * Sửa lỗi bị treo trong Microsoft Word khi tùy chọn trong cài đặt định dạng tài liệu "báo tiêu đề" và "báo chú thích" không được bật. (#15019)
  * Trong Word và Excel, căn lề văn bản sẽ được thông báo chính xác trong nhiều tình huống hơn. (#15206, #15220)
  * Sửa lỗi thông báo của vài phím tắt định dạng ô trong Excel. (#15527)
* Microsoft Edge:
  * NVDA sẽ không còn nhảy ngược về vị trí cuối cùng ở chế độ duyệt khi mở trình đơn ngữ cảnh trong Microsoft Edge. (#15309)
  * NVDA lại một lần nữa đọc được trình đơn ngữ cảnh của trang tải về trong Microsoft Edge. (#14916)
* Chữ nổi:
  * Con trỏ nổi và chỉ báo lựa chọn giờ đây sẽ luôn được cập nhật một cách chính xác sau khi hiện hoặc ẩn các chỉ báo tương ứng bằng thao tác. (#15115)
  * Sửa lỗi làm cho màn hình nổi Albatross  nỗ lực khởi tạo dù đã có một thiết bị khác được kết nối. (#15226)
* Cửa Hàng Add-on:
  * Sửa lỗi khi bỏ chọn mục "Bao gồm các add-on không tương thích" sẽ cho ra kết quả là các add-on không tương thích vẫn được liệt kê trong cửa hàng. (#15411)
   * Các Add-on bị khóa vì lí do tương thích giờ đây sẽ được lọc một cách chính xác khi bật / tắt bộ lọc để bật / tắt trạng thái. (#15416)
  * Sửa lỗi ngăn chặn cập nhật  các add-on không tương thích theo kiểu cài đè hoặc thay thế bằng các công cụ cài đặt bên ngoài. (#15417)
  * Sửa lỗi  NVDA không đọc cho đến khi khởi động lại sau khi cài đặt add-on. (#14525)
  * Sửa lỗi không thể cài đặt add-on nếu một bản tải về trước đó bị thất bại hoặc bị hủy bỏ. (#15469)
  * Sửa các lỗi về quản lí các add-on không tương thích khi cập nhật NVDA. (#15414, #15412, #15437)
* NVDA lại một lần nữa thông báo kết quả tính toán trong Windows 32bit calculator trên các phiên bản Server, LTSC và LTSB của Windows. (#15230)
* NVDA không còn bỏ qua các thay đổi focus khi một của sổ cháu  (grand child window) cós focus. (#15432)
* Sửa lỗi gây treo máy khi khởi động NVDA. (#15517)

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2023.2

Bản phát hành này giới thiệu cửa hàng Add-on để thay thế cho trình quản lí add-on.
Trong cửa hàng add-on, bạn có thể duyệt, tìm kiếm, cài đặt và cập nhật add-on của cộng đồng.
Giờ đây, bạn có thể tự bỏ qua vấn đề không tương thích với các add-on lỗi thời và tự chịu trách nhiệm nếu có rủi ro.

Tính năng mới cho chữ nổi, thêm lệnh và thêm màn hình được hỗ trợ.
Thêm thao tác mới cho việc nhận dạng văn bản (OCR) và điều hướng đối tượng phẳng.
Cải thiện cho việc điều hướng và đọc định dạng trong Microsoft Office

Sửa nhiều lỗi, đặc biệt là lỗi liên quan đến chữ nổi, Microsoft Office, trình duyệt web và Windows 11.

Đã cập nhật eSpeak-NG, thư viện phiên dịch chữ nổi LibLouis, và Unicode CLDR.

### Tính năng mới

* Add-on Store (Cửa Hàng Add-On) đã được tích hợp vào NVDA. (#13985)
  * Duyệt, tìm kiếm, cài đặt và cập nhật add-on từ cộng đồng.
  * Xử lý thủ công các vấn đề về tương thích với những add-on lỗi thời.
  * Công cụ Quản Lý Các Add-On đã bị gỡ bỏ và được thay thế bởi Add-on Store.
  * Xem tài liệu hướng dẫn sử dụng để biết thêm thông tin.
* Các thao tác mới:
  * Thao tác chưa gán lệnh để chuyển qua những ngôn ngữ có sẵn cho Windows OCR. (#13036)
  * Thao tác chưa gán lệnh để chuyển qua các chế độ hiển thị thông điệp của chữ nổi. (#14864)
  * Thao tác chưa gán lệnh để bật / tắt việc hiển thị chỉ báo lựa 	chọn cho chữ nổi. (#14948)
  * Đã thêm thao tác bàn phím mặc định để chuyển đến đối tượng kế hay đối tượng trước trong một chế độ xem phẳng của hệ thống phân cấp đối tượng. (#15053)
    * Máy tính bàn: `NVDA+numpad9` và `NVDA+numpad3` để chuyển đến đối tượng trước và đối tượng kế.
    * Máy xách tay: `shift+NVDA+[` và `shift+NVDA+]` để chuyển đến đối tượng trước và đối tượng kế.
* Các tính năng mới cho chữ nổi:
  * Đã thêm hỗ trợ cho màn hình nổi Help Tech Activator. (#14917)
  * Tùy chọn mới để bật / tắt hiển thị chỉ báo lựa chọn (chấm 7 và 8). (#14948)
  * Tùy chọn mới để tùy ý di chuyển dấu nháy hệ thống hay focus khi thay đổi vị trí con trỏ duyệt với các phím định tuyến chữ nổi. (#14885, #3166)
  * Khi bấm `numpad2` ba lần để xem giá trị bằng số của một kí tự tại vị trí con trỏ duyệt, thông tin đó cũng sẽ thể hiện trên chữ nổi. (#14826)
  * Thêm hỗ trợ cho `aria-brailleroledescription` thuộc tính ARIA 1.3, cho phép tác giả của trang web ghi đè loại của một thành phần được hiển thị trên màn hình chữ nổi. (#14748)
  * Trình điều khiển màn hình nổi Baum Braille: thêm vài thao tác kết hợp bằng chữ nổi để thực hiện các phím lệnh phổ biến như `windows+d` và `alt+tab`.
  Vui lòng xem hướng dẫn sử dụng NVDA để biết toàn bộ danh sách phím lệnh. (#14714)
* Thêm phát âm của các kí hiệu Unicode:
  * Các kí hiệu chữ nổi như `⠐⠣⠃⠗⠇⠐⠜`. (#13778)
  * Phím Option trên Mac `⌥`. (#14682)
* Thêm các thao tác cho màn hình nổi Tivomatic Caiku Albatross. (#14844, #15002)
  * Hiện hộp thoại cài đặt chữ nổi
  * Truy cập thanh trạng thái
  * Chuyển đến các chế độ nháy con trỏ nổi
  * Chuyển đến các chế độ hiển thị thông điệp chữ nổi
  * Bật / tắt con trỏ nổi
  * Bật / tắt chỉ báo hiển thị vùng chọn
  * Xoay vòng  các kiểu "di chuyển dấu nháy hệ thống chữ nổi khi định tuyến con trỏ duyệt". (#15122)
* Các tính năng cho Microsoft Office:
  * Khi bật làm nổi văn bản trong Định dạng tài liệu, màu được làm nổi cũng sẽ được thông báo trong Microsoft Word. (#7396, #12101, #5866)
  * Khi bật thông báo màu trong Định dạng tài liệu, màu nền giờ đây cũng được thông báo trong Microsoft Word. (#5866)
  * Khi dùng phím lệnh của Excel để bật / tắt các định dạng như in đậm, in nghiêng, gạch chân và gạch ngang chữ của một ô trong Excel, kết quả giờ đây đã được thông báo. (#14923)
* Thử nghiệm Cải tiến cho việc quản lí âm thanh:
  * NVDA giờ đây có thể cho ra âm thanh thông qua Windows Audio Session API (WASAPI), vốn có thể cải tiến việc phản hồi, khả năng vận hành cũng như tính ổn định cho bộ đọc và âm thanh của NVDA.
  * Có thể bật WASAPI trong cài đặt nâng cao để dùng. (#14697)
  Thêm nữa, nếu bật WASAPI, sẽ có một số thiết lập nâng cao sau đây.
    * Tùy chọn để chỉnh cho âm lượng âm thanh và tiếng beep của NVDA đi theo thiết lập âm lượng của giọng đọc bạn đang dùng. (#1409)
    * Tùy chọn để điều khiển riêng biệt âm lượng của âm thanh NVDA.
  * Có một vấn đề đã được tìm thấy gây treo máy khi bật WASAPI. (#15150)
* Trong Mozilla Firefox và Google Chrome, NVDA giờ đây sẽ thông báo khi một điều khiển mở ra một hộp thoại (dialog), lưới (grid), danh sách (list) hoặc cây thư mục (tree) nếu tác giả có  dùng `aria-haspopup` để quy định. (#14709)
* Giờ đây, đã có thể dùng các biến của hệ thống (chẳng hạn: `%temp%` hoặc `%homepath%`) trong phần thiết lập đường dẫn để tạo bản chạy trực tiếp cho NVDA. (#14680)
* Trong Windows 10 May 2019 Update trở lên, NVDA có thể thông báo các tên của virtual desktop khi mở, thay đổi và đóng chúng. (#5641)
* Một tham số hệ thống mở rộng đã được thêm vào, cho phép người dùng và quản trị hệ thống buộc NVDA khởi chạy trong chế độ bảo vệ. (#10018)

### Các thay đổi

* Các thành phần được cập nhật:
  * Đã cập nhật eSpeak NG lên 1.52-dev commit `ed9a7bcf`. (#15036)
  * Đã cập nhật thư viện phiên dịch chữ nổi LibLouis  lên [3.26.0](https://github.com/liblouis/liblouis/releases/tag/v3.26.0). (#14970)
  * Đã cập nhật CLDR lên phiên bản 43.0. (#14918)
* Các thay đổi cho LibreOffice:
  * Khi thông báo vị trí con trỏ duyệt, vị trí của con trỏ / dấu nháy hiện tại so với trang hiện hành giờ đây đã được thông báo trong LibreOffice Writer cho LibreOffice các phiên bản 7.6 trở lên, tương tự như với Microsoft Word. (#11696)
Việc thông báo thanh trạng thái (kích hoạt bằng lệnh `NVDA+end`) đã hoạt động với LibreOffice. (#11698)
  * Khi chuyển đến một ô khác trong LibreOffice Calc, NVDA không còn thông báo sai tọa độ của ô có focus trước đó khi tính năng đọc tọa độ ô bị tắt trong cài đặt của NVDA. (#15098)
* Các thay đổi cho chữ nổi:
  * Khi dùng một màn hình chữ nổi thông qua trình điều khiển chữ nổi HID tiêu chuẩn, có thể dùng dpad để mô phỏng các phím mũi tên và enter.
  Lệnh khoảng trắng+chấm 1 và khoảng trắng+chấm 4 giờ đây cũng được gán cho mũi tên lên và xuống. (#14713)
  * Các cập nhật cho nội dung động trên web (ARIA live regions) giờ đây đã hiển thị trong chữ nổi..
  Có thể tắt trong cài đặt nâng cao. (#7756)
* Các kí hiệu dấu gạch ngang dash và em-dash sẽ luôn được gửi ra bộ đọc. (#13830)
* Việc thông báo khoảng cách trong Microsoft Word giờ đây sẽ dùng đơn vị được quy định trong phần advanced options của Word, kể cả khi dùng UIA để truy cập tài liệu Word. (#14542)
* NVDA phản hồi nhanh hơn khi di chuyển con trỏ trong các điều khiển nhập liệu. (#14708)
* Kịch bản thông báo đường dẫn của liên kết giờ đây sẽ thông báo từ vị trí dấu nháy hoặc focus thay vì từ đối tượng điều hướng. (#14659)
* Việc tạo bản chạy trực tiếp không còn bắt buộc phải nhập kí tự ổ đĩa như là một phần của đường dẫn cụ thể. (#14681)
* Nếu Windows được cấu hình để hiển thị số giây ở đồng hồ trên khay hệ thống, việc dùng `NVDA+f12` để xem giờ sẽ đọc theo thiết lập đó. (#14742)
* NVDA giờ đây sẽ đọc các nhóm không có nhãn mà có thông tin vị trí hữu ích, như là trình đơn trong các phiên bản gần đây của Microsoft Office 365. (#14878) 

### Sửa lỗi

* Chữ nổi
  * Sửa vài lỗi về tính ổn định cho đầu vào / đầu ra của các màn hình chữ nổi, kết quả là NVDA ít xảy ra lỗi và ít bị treo. (#14627)
  * NVDA sẽ không còn tình trạng nhiều lần chuyển qua chế độ không có chữ nổi ngoài ý muốn trong khi tự dò tìm, đưa đến một bản ghi sạch hơn. (#14524)
  * NVDA giờ đây sẽ chuyển về USB nếu thiết bị HID Bluetooth  (như là HumanWare Brailliant hay APH Mantis) được tìm thấy tự động và sẵn sàng cho một kết nối USB.
  Cái này chỉ hoạt động với cổng Bluetooth Serial trước đây. (#14524)
  * Khi không có màn hình chữ nổi nào được kết nối và trình xem chữ nổi được đóng bằng cách bấm `alt+f4` hoặc bấm vào nút đóng, kích thước hiển thị của hệ thống chữ nổi phụ sẽ lại được trả về không ô. (#15214)
* Trình duyệt web:
  * NVDA không còn tình trạng thường xuyên làm cho Mozilla Firefox bị treo hay không phản hồi. (#14647)
  * Trong Mozilla Firefox và Google Chrome, các kí tự được nhập sẽ không còn bị đọc lên trong vài hộp nhập văn bản, kể cả khi tắt chế độ đọc kí tự khi nhập. (#8442)
  * Giờ bạn có thể dùng chế độ duyệt trong các điều khiển nhún Chromium  ở những nơi mà trước đây không dùng được. (#13493, #8553)
  * trong Mozilla Firefox, di chuyển chuột qua văn bản sau một liên kết giờ đây sẽ thông báo nội dung văn bản đó. (#9235)
  * Đường dẫn của các liên kết hình ảnh giờ đây đã được thông báo chính xác ở nhiều trường hợp trong Chrome và Edge. (#14783)
  * Khi nỗ lực thông báo đường dẫn cho một liên kết không có thuộc tính href, NVDA sẽ không còn rơi vào trạng thái im lặng.
  Thay vào đó, NVDA sẽ thông báo liên kết không có đường dẫn. (#14723)
  * Trong chế độ duyệt, NVDA không còn bỏ qua một cách không chính xác focus di chuyển đến một điều khiển cha hay điều khiển con. Ví dụ: di chuyển từ một điều khiển đến thành phần cha của nó thành phần trong danh sách hoặc ô lưới. (#14611)
    * Lưu ý là sửa lỗi này chỉ áp dụng khi  tắt tùy chọn Tự đưa con trỏ hệ thống đến các thành phần có thể có focus trong cài đặt chế độ duyệt (là tùy chọn mặc định).
    -  -
  -
* Sửa các lỗi trên Windows 11:
  * NVDA lại có thể đọc nội dung thanh trạng thái của Notepad. (#14573)
  * Việc chuyển giữa các thẻ sẽ thông báo tên và vị trí thẻ mới cho Notepad và File Explorer. (#14587, #14388)
  * NVDA sẽ lại thông báo tên các thành phần khi nhập văn bản trong các ngôn ngữ như tiếng Trung và tiếng Nhật chẳng hạn. (#14509)
  * Giờ đây, lại có thể mở các mục Cộng đồng hỗ trợ và giấy phép trên trình đơn trợ giúp của NVDA. (#14725)
* Sửa lỗi cho Microsoft Office:
  * Khi di chuyển nhanh qua các ô trong Excel, NVDA giờ đây ít khi thông báo sai ô hay vùng chọn. (#14983, #12200, #12108)
  * Khi đứng ở một ô ngoài trang bảng tính trong Excel, chữ nổi và bộ làm nổi focus không còn bị cập nhật một cách không cần thiết vào đối tượng đã có focus trước đó. (#15136)
  * NVDA không còn bị lỗi không thông báo các trường nhập mật khẩu đang có focus trong Microsoft Excel và Outlook. (#14839)
* Với các kí hiệu không có phần mô tả ở ngôn ngữ hiện hành, mô tả mặc định bằng tiếng Anh sẽ được dùng. (#14558, #14417)
* Giờ đây, đã có thể dùng dấu chéo ngược trong trường thay thế của một từ điển, khi loại không được quy định là biểu thức phổ thông. (#14556)
* Trong Windows 10 và 11 Calculator, Bản chạy trực tiếp của NVDA sẽ không còn tình trạng không làm gì hoặc phát âm báo lỗi khi nhập phép tính trong chế độ standard calculator trong compact overlay. (#14679)
* Phục hồi được NVDA từ nhiều tình huống hơn, như là ứng dụng không phản hồi, vốn trước đây  làm cho nó bị đóng băng hoàn toàn. (#14759) 
* Khi buộc dùng hỗ trợ UIA với một số cửa sổ terminal và consoles nhất định, đã sửa một lỗi gây đóng băng và tập tin  bản ghi dò lỗi bị xem là tập tin rác. (#14689)
* NVDA Sẽ không còn từ chối lưu cấu hình sau khi nó được khôi phục. (#13187)
* Khi chạy một phiên bản tạm thời từ trình cài đặt, NVDA sẽ không khiến người dùng hiểu lầm rằng họ có thể lưu cấu hình. (#14914)
* NVDA giờ đây nhìn chung là phản hồi nhanh hơn với lệnh và các thay đổi focus. (#14928)
* Việc hiển thị cài đặt OCR không còn bị lỗi trên vài hệ thống nữa. (#15017)
* Sửa các lỗi liên quan đến việc lưu và tải cấu hình NVDA, bao gồm việc chuyển bộ đọc. (#14760)
* Sửa lỗi  làm cho thao tác "nhả tay" để xem lại văn bản di chuyển qua từng trang, thay vì di chuyển đến dòng trước. (#15127)

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2023.1

Đã thêm một tùy chọn mới, "Kiểu đoạn" trong "Điều hướng tài liệu".
Tính năng này có thể dùng trong các trình soạn thảo văn bản không hỗ trợ điều hướng theo đoạn một cách tự nhiên, như Notepad và Notepad++.

Thêm một lệnh toàn cục mới để thông báo đường dẫn của liên kết, phím lệnh là `NVDA+k`.

Đã cải thiện hỗ trợ cho các loại ghi chú trong nội dung web (như chú thích và chú thích chân trang).
Bấm `NVDA+d` để chuyển qua lại giữa các thông điệp  tổng hợp khi được thông báo có chú thích("có chú thích, có chú thích chân trang").

Đã hỗ trợ các màn hình chữ nổi Tivomatic Caiku Albatross 46/80.

Đã cải thiện hỗ trợ cho các phiên bản ARM64 và AMD64 của Windows.
Đã sửa được nhiều lỗi, đáng chú ý là các lỗi trên Windows 11.

Đã cập nhật eSpeak, LibLouis, Sonic rate boost và Unicode CLDR.
Có các bảng chữ nổi mới: Georgian, Swahili (Kenya) và Chichewa (Malawi).

Lưu ý:

* Bản phát hành này không tương thích với các add-on hiện tại.

### Tính năng mới

* Microsoft Excel thông qua UI Automation: tự động đọc tiêu đề cột và dòng trong bảng biểu. (#14228)
  * Lưu ý: chức năng này đang đề cập đến định dạng bảng biểu thông qua nút "Table" trên thẻ Insert của Ribbon.
  "First Column" và "Header Row" trong "Table Style Options" tương ứng với tiêu đề cột và dòng.
  * Chức năng này không liên quan đến hỗ trợ xác định tiêu đề của trình đọc màn hình bằng vùng được đặt tên (named ranges), vốn không được hỗ trợ thông qua UI Automation.
* Một kịch bản chưa gán thao tác đã được thêm vào để bật tắt tính năng chờ đọc mô tả kí tự. (#14267)
* Đã thêm một tùy chọn thử nghiệm để tận dụng hỗ trợ thông báo UIA trong Windows Terminal để thông báo các văn bản mới hoặc văn bản đã thay đổi trong terminal, kết quả là cải thiện tính ổn định và khả năng phản hồi. (#13781)
  * Tham khảo hướng dẫn sử dụng để biết giới hạn của tùy chọn thử nghiệm này.
* Trên Windows 11 ARM64, chế độ duyệt đã có trong các ứng dụng AMD64 như Firefox, Google Chrome và 1Password. (#14397)
* Đã thêm một tùy chọn mới, "Kiểu đoạn" trong "Điều hướng tài liệu".
Tùy chọn này hỗ trợ cho việc điều hướng qua đoạn bằng một dấu xuống dòng  (kiểu bình thường) và nhiều dấu xuống dòng (điều hướng theo khối).
Tính năng này có thể dùng trong các trình soạn thảo văn bản không hỗ trợ điều hướng theo đoạn một cách tự nhiên, như Notepad và Notepad++. (#13797)
* Việc trình bày nhiều loại ghi chú giờ đây đã được thông báo.
`nvda+d` giờ đây sẽ chuyển qua lại giữa các loại thông báo ghi chú được tổng hợp  với nhiều loại thông báo khác nhau.
Ví dụ, khi văn bản có bao gồm chú thích hoặc chú thích chân trang. (#14507, #14480)
* Đã thêm hỗ trợ cho các màn hình chữ nổi Tivomatic Caiku Albatross 46/80. (#13045)
* Lệnh toàn cục mới: Thông báo đường dẫn liên kết (`NVDA+k`).
Bấm một lần sẽ đọc hoặc hiển thị đường dẫn của liên kết tại đối tượng điều hướng trên màn hình chữ nổi.
Bấm hai lần sẽ hiển thị trên một cửa sổ để dễ xem chi tiết hơn. (#14583)
* Thêm lệnh mới chưa gán thao tác (phân loại Công Cụ): thông báo đường dẫn liên kết trên một cửa sổ.
Giống như bấm `NVDA+k` hai lần, nhưng có thể tiện hơn cho người dùng chữ nổi. (#14583)

### Các thay đổi

* Đã cập nhật thư viện phiên dịch chữ nổi LibLouis lên [3.24.0](https://github.com/liblouis/liblouis/releases/tag/v3.24.0). (#14436)
  * Có các cập nhật chính cho tiếng Hungarian, UEB,  và chữ nổi bopomofo của Trung Hoa.
  * Hỗ trợ chữ nổi tiêu chuẩn Đan Mạch 2022.
  * Các bảng chữ nổi mới cho tiếng Georgian chữ nổi văn học, Swahili (Kenya) và Chichewa (Malawi).
* Đã cập nhật thư viện tăng tốc độ Sonic lên commit `1d70513`. (#14180)
* CLDR đã được cập nhật lên phiên bản 42.0. (#14273)
* eSpeak NG đã được cập nhật lên 1.52-dev commit `f520fecb`. (#14281, #14675)
  * Sửa lỗi đọc nhiều số. (#14241)
* Các ứng dụng Java với các điều khiển sử dụng trạng thái chọn (selectable state) giờ đây sẽ được thông báo khi một thành phần không được chọn, thay vì chỉ thông báo khi nó được chọn. (#14336)

### Sửa lỗi

* Các sửa lỗi cho Windows 11:
  * NVDA sẽ thông báo  tìm kiếm được làm nổi khi mở Start menu. (#13841)
  * Trên ARM, các ứng dụng x64 không còn bị cho là ứng dụng ARM64 nữa. (#14403)
  * Đã có thể tiếp cận các thành phần trong trình đơn của clipboard history (lịch sử bộ nhớ tạm) như là "pin item". (#14508)
  * Trong Windows 11 22H2 và mới hơn, lại có thể dùng chuột hoặc tương tác cảm ứng để tiếp cận các khu vực như khay hệ thống và hộp thoại "Open With". (#14538, #14539)
* Gợi ý đã được đọc lên khi gõ kiểu @nhắc đến trong các chú thích của Microsoft Excel. (#13764)
* Trong thanh vị trí của Google Chrome (Google Chrome location bar), các điều khiển dạng gợi ý (switch to tab - chuyển sang thẻ mới, remove suggestion - xóa gợi ý v...v...) giờ đây đã được đọc lên khi được chọn. (#13522)
* Khi yêu cầu thông tin định dạng, màu sắc giờ đây đã được thông báo rõ ràng trong Wordpad hay trình xem log, thay vì chỉ báo là "Màu mặc định". (#13959)
* Trong Firefox, Kích hoạt nút "Show options" trên  các trang GitHub issue - tạm dịch: trang bỏ phiếu của Github giờ đây đã làm việc một cách đáng tin hơn. (#14269)
* Điều khiển date picker (chọn ngày) trong hộp thoại Advanced search của Outlook 2016 / 365 giờ đây đã đọc được nhãn và giá trị của nó. (#12726)
* Các điều khiển dạng chuyển trạng thái (switch) ARIA giờ đây đã được thông báo là chuyển trong Firefox, Chrome và Edge, thay vì chỉ báo là hộp kiểm. (#11310)
* NVDA sẽ tự thông báo trạng thái sắp xếp trên tiêu đề cột trong bảng biểu  HTML  khi thay đổi bằng cách bấm nút bên trong. (#10890)
* Tên của một cột mốc hay vùng giờ đây sẽ luôn tự đọc lên khi đi vào trong từ bên ngoài bằng điều hướng nhanh hoặc focus trong chế độ duyệt. (#13307)
* Khi bật chế độ beep hoặc nói chữ hoa cùng với tính năng chờ để mô tả kí tự, NVDA không còn phát tiếng beep hoặc thông báo chữ 'hoa' hai lần. (#14239)
* Các điều khiển trong bảng biểu trong các ứng dụng Java giờ đây sẽ được thông báo chính xác hơn bởi NVDA. (#14347)
* Sẽ không còn tình trạng vài thiết lập  hoạt động khác nhau khi dùng nhiều hồ sơ cấu hình. (#14170)
  * Đã khắc phục lỗi này cho các thiết lập sau:
    * Thụt đầu dòng trong Cài đặt định dạng tài liệu.
    * Đường viền ô trong Cài đặt định dạng tài liệu
    * Hiện thông điệp trong cài đặt chữ nổi
    * Đưa theo braille trong cài đặt chữ nổi
  * Ở vài trường hợp ít gặp, việc sử dụng các thiết lập này  trong hồ sơ cấu hình có thể bị thay đổi ngoài ý muốn khi cài phiên bản NVDA này.
  * Vui lòng kiểm tra các tùy chọn này trong hồ sơ của bạn sau khi cập nhật NVDA lên phiên bản này.
* Biểu tượng cảm xúc giờ đây sẽ được đọc ở nhiều ngôn ngữ hơn. (#14433)
* Việc trình bày của một chú thích sẽ không bị thiếu trong chữ nổi với vài thành phần. (#13815)
* Sửa một lỗi làm cho các thay đổi cấu hình không được lưu một cách chính xác khi thay đổi giữa một tùy chọn "Mặc định" và giá trị của tùy chọn "Mặc định". (#14133)
* Khi cấu hình NVDA, sẽ luôn  có tối thiểu một phím được chỉ định là phím NVDA. (#14527)
* Khi truy cập trình đơn NVDA  từ vùng thông báo, NVDA sẽ không gợi ý cập nhật đang chờ khi không có bản cập nhật nào. (#14523)
* Thời gian còn lại, thời gian trôi qua và tổng thời gian giờ đây đã được đọc chính xác cho các tập tin âm thanh dài hơn một ngày trong foobar2000. (#14127)
* Trong các trình duyệt web như Chrome và Firefox, ngoài việc đọc lên, các thông báo như  tải  tập tin đã hiển thị trong chữ nổi. (#14562)
* đã sửa lỗi khi điều hướng đến cột đầu và cột cuối của bảng biểu trong Firefox (#14554)
 * Khi NVDA được gọi chạy với tham số `--lang=Windows`, lại có thể mở hộp thoại Cài Đặt Chung của NVDA. (#14407)
* NVDA không còn bị lỗi không tiếp tục đọc trong Kindle for PC sau khi lật trang. (#14390)
 -

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2022.4

Bản phát hành này tích hợp vài phím lệnh mới, bao gồm các lệnh đọc tất cả trong bảng biểu.
Đã thêm phần "Hướng Dẫn Nhanh" vào tài liệu hướng dẫn sử dụng.
Một số lỗi cũng đã được sửa.

Đã cập nhật eSpeak và LibLouis.
Đã có các bảng chữ nổi mới của tiếng Trung Quốc, Thụy Điển, Luganda và Kinyarwanda.

### Tính năng mới

* Đã thêm phần "Hướng Dẫn Nhanh" vào tài liệu hướng dẫn sử dụng. (#13934)
* Giới thiệu một lệnh mới để kiểm tra phím tắt tại vị trí con trỏ. (#13960)
  * Máy bàn: `shift+2 bàn phím số`.
  * Máy xách tay: `NVDA+ctrl+shift+.`.
* Giới thiệu lệnh mới để di chuyển con trỏ duyệt qua từng trang nếu ứng dụng có hỗ trợ. (#14021)
  * Chuyển về trang trước:
    * Máy bàn: `NVDA+pageUp`.
    * Máy xách tay: `NVDA+shift+pageUp`.
  * Chuyển đến trang kế:
    * Máy bàn: `NVDA+pageDown`.
    * Máy xách tay: `NVDA+shift+pageDown`.
* Đã thêm các lệnh sau cho bảng biểu. (#14070)
  * Đọc tất cả trong cột: `NVDA+control+alt+mũi tên xuống`
  * Đọc tất cả trong dòng: `NVDA+control+alt+mũi tên phải`
  * Đọc toàn bộ cột: `NVDA+control+alt+mũi tên lên`
  * Đọc toàn bộ dòng: `NVDA+control+alt+mũi tên trái`
* Microsoft Excel thông qua UI Automation: NVDA giờ đây sẽ thông báo khi di chuyển ra khỏi một bảng   biểu trong một bảng tính. (#14165)
* Việc đọc tiêu đề bảng giờ đây có thể cấu hình độc lập cho cột và dòng. (#14075)

### Các thay đổi

* Đã cập nhật eSpeak NG lên 1.52-dev commit `735ecdb8`. (#14060, #14079, #14118, #14203)
  * Sửa lỗi đọc các kí tự tiếng Latin khi dùng với tiếng Quan Thoại. (#12952, #13572, #14197)
* Đã cập nhật thư viện phiên dịch chữ nổi LibLouis lên [3.23.0](https://github.com/liblouis/liblouis/releases/tag/v3.23.0). (#14112)
  * Thêm các bảng chữ nổi:
    * Trung Quốc chữ nổi phổ thông (chữ Trung giản thể)
    * Kinyarwanda chữ nổi văn học
    * Luganda chữ nổi văn học
    * Thụy Điển chữ nổi đầy đủ
    * Thụy Điển chữ nổi tắt một phần
    * Thụy Điển Chữ nổi tắt
    * Trung Quốc (Trung Quốc, Quan Thoại) hệ thống chữ nổi hiện tại (không có mực)
* NVDA giờ đây đã bao gồm kiểu hệ điều hành trong việc thống kê thông tin người dùng. (#14019)

### Sửa lỗi

* Khi cập nhật NVDA bằng công cụ Windows Package Manager CLI (aka winget), phiên bản chính thức của NVDA sẽ không còn bị coi là bản mới hơn khi bạn đang cài một phiên bản alpha. (#12469)
* NVDA giờ đây sẽ thông báo chính xác các điều khiển dạng Group boxe trong các ứng dụng Java. (#13962)
* Con trỏ nháy đã đi theo một cách chính xác những văn bản được đọc trong khi "đọc tất cả" trong các ứng dụng như Bookworm, WordPad, hoặc trình xem log của NVDA. (#13420, #9179)
* Trong các chương trình có dùng UI Automation, các hộp kiểm chỉ chọn một phần sẽ được thông báo chính xác. (#13975)
* Cải thiện khả năng vận hành và tính ổn định trong Microsoft Visual Studio, Windows Terminal và các ứng dụng trên nền UI Automation khác. (#11077, #11209)
  * Việc sửa lỗi này áp dụng cho Windows 11 Sun Valley 2 (version 22H2) trở lên.
  * Đăng kí chọn lọc cho các thay đổi thuộc tính và sự kiện của UI Automation giờ đây mặc định được bật.
* Việc đọc văn bản, đầu ra chữ nổi và việc ngăn đọc mật khẩu giờ đây đã hoạt động như mong muốn trong  các điều khiển Windows Terminal được nhún trong Visual Studio 2022. (#14194)
* NVDA giờ đây được xem là  DPI khi dùng nhiều màn hình.
Có một vài lỗi được sửa để dùng thiết lập DPI cao hơn 100% hoặc nhiều màn hình.
Lỗi có thể vẫn tồn tại với các phiên bản Windows cũ hơn Windows 10 1809.
Để việc sửa lỗi phát huy tác dụng, những ứng dụng mà NVDA tương tác cũng phải là ứng dụng được xem là ứng dụng DPI.
Lưu ý là vẫn còn những lỗi được tìm thấy với Chrome và Edge. (#13254)
  * Các khung làm nổi trực quan giờ đây đã được đặt chính xác ở hầu hết các ứng dụng. (#13370, #3875, #12070)
  * Việc tương tác trên màn hình cảm ứng giờ đây đã hoạt động chính xác với hầu hết các ứng dụng. (#7083)
  * Việc theo dõi bằng chuột đã hoạt động chính xác với hầu hết các ứng dụng. (#6722)
* Trạng thái hướng màn hình (đứng / ngang) giờ đây đã bị bỏ qua khi không có thay đổi (ví dụ: thay đổi màn hình). (#14035)
 NVDA sẽ thông báo các thành phần đang được kéo trên màn hình ở những nơi như sắp xếp lại trong kiểu Windows 10 Start menu và desktop ảo trong Windows 11. (#12271, #14081)
* Trong cài đặt nâng cao, tùy chọn "Phát âm thanh cho lỗi log" giờ đây đã trả lại giá trị mặc định của nó khi bấm vào nút "Trả về mặc định". (#14149)
* NVDA giờ đây có thể chọn văn bản bằng phím lệnh `NVDA+f10`trên các ứng dụng Java. (#14163)
* NVDA sẽ không còn bị vướng lại trong một trình đơn khi bấm mũi tên lên / xuống ở chủ đề đàm thoại trong Microsoft Teams. (#14355)

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2022.3.3

Đây là bản phát hành phụ nhằm sửa lỗi với 2022.3.2, 2022.3.1 và 2022.3.
bản này cũng tìm ra một lỗi bảo mật.

### Sửa lỗi bảo mật

* Ngăn chặn truy cập hệ thống (ví dụ: NVDA Python console) với những người dùng không được xác thực.
([GHSA-fpwc-2gxx-j9v7](https://github.com/nvaccess/nvda/security/advisories/GHSA-fpwc-2gxx-j9v7))

### Sửa lỗi

* Sửa lỗi NVDA bị đóng băng khi khóa máy, NVDA sẽ cho phép truy cập Desktop người dùng khi ở trong màn hình khóa của Windows. (#14416)
* Sửa lỗi NVDA bị đóng băng khi khóa máy, NVDA sẽ không vận hành như vậy khi thiết bị còn đang bị khóa. (#14416)
* Sửa lỗi tiếp cận với Windows "forgot my PIN" process và Windows update/install experience. (#14368)
* Sửa lỗi khi cố gắng cài NVDA trong vài môi trường Windows, Windows Server chẳng hạn. (#14379)

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2022.3.2

Đây là bản phát hành phụ nhằm sửa lỗi hồi quy với 2022.3.1 và giải quyết một lỗi bảo mật.

### các sửa lỗi bảo mật

* Ngăn chặn truy cập vào các cấp độ hệ thống với các tài khoản không xác thực.
([GHSA-3jj9-295f-h69w](https://github.com/nvaccess/nvda/security/advisories/GHSA-3jj9-295f-h69w))

### Sửa lỗi

* Sửa lỗi hồi quy từ bản 2022.3.1 làm cho vài chức năng bị vô hiệu ở các màn hình bảo vệ. (#14286)
* Sửa lỗi hồi quy từ bản 2022.3.1 làm cho vài chức năng bị vô hiệu sau khi đăng nhập, nếu NVDA được gọi chạy từ màn hình khóa. (#14301)

## 2022.3.1

Đây là một bản phát hành phụ để sửa vài lỗi bảo mật..
Vui lòng báo cáo các vấn đề về bảo mật đến <info@nvaccess.org>.

### Sửa lỗi bảo mật

* Sửa lỗi làm cho có thể giả lập từ quyền người dùng đến quyền hệ thống.
([GHSA-q7c2-pgqm-vvw5](https://github.com/nvaccess/nvda/security/advisories/GHSA-q7c2-pgqm-vvw5))
* Sửa lỗi bảo mật nhằm cho phép truy cập python console ở màn hình khóa thông qua điều kiện chủng tộc (race condition) cho việc khởi chạy NVDA.
([GHSA-72mj-mqhj-qh4w](https://github.com/nvaccess/nvda/security/advisories/GHSA-72mj-mqhj-qh4w))
* Sửa lỗi làm cho văn bản của trình xem nội dung đọc được nhớ khi khóa Windows.
([GHSA-grvr-j2h8-3qm4](https://github.com/nvaccess/nvda/security/advisories/GHSA-grvr-j2h8-3qm4))

### Sửa lỗi

* Chặn  một người dùng không xác định cập nhật các thiết lập cho trình xem nội dung đọc và   trình xem nội dung chữ nổi ở màn hình khóa. ([GHSA-grvr-j2h8-3qm4](https://github.com/nvaccess/nvda/security/advisories/GHSA-grvr-j2h8-3qm4))

## 2022.3

Cộng đồng phát triển NVDA đã có một số đóng góp đáng kể cho bản phát hành này.
Bao gồm việc chờ để đọc mô tả kí tự và hỗ trợ cho Windows Console.

Bản phát hành này cũng sửa một số lỗi.
Đáng chú ý, bản cập nhật mới nhất của Adobe Acrobat/Reader sẽ không còn bị treo khi đọc một tài liệu PDF.

Đã cập nhật bộ đọc eSpeak với ba ngôn ngữ mới: Belarus, Luxembourgish và Totontepec Mixe.

### Tính năng mới

* Trong Windows Console Host được dùng bởi Command Prompt, PowerShell và Windows Subsystem for Linux trên Windows 11 phiên bản 22H2 (Sun Valley 2) trở lên:
  * Hiệu suất vận hành và tính ổn định được cải thiện rõ rệt. (#10964)
  * Khi bấm `control+f` để tìm văn bản, vị trí con trỏ duyệt đã được cập nhật để đi theo cụm từ được tìm thấy. (#11172)
  * Việc đọc các văn bản được nhập nhưng không hiện lên màn hình (mật khẩu chẳng hạn) mặc định bị vô hiệu.
Có thể bật lại nó trong bảng cài đặt mở rộng của NVDA. (#11554)
  * Có thể đọc lại văn bản đã bị cuộn khỏi màn hình mà không cần phải cuộn cửa sổ console. (#12669)
  * Xem thêm thông tin chi tiết về định dạng văn bản. ([microsoft/terminal PR 10336](https://github.com/microsoft/terminal/pull/10336))

* Đã thêm một tùy chọn cho bộ đọc để đọc mô tả kí tự sau một khoảng thời gian ngắn. (#13509)
* Đã thêm một tùy chọn cho chữ nổi để phát hiện và ngừng đọc khi cuộn màn hình tới hay lùi. (#2124)

### Các thay đổi

* Đã cập nhật eSpeak NG lên 1.52-dev commit `9de65fcb`. (#13295)
  * Các ngôn ngữ được thêm vào:
    * Belarus
    * Luxembourgish
    * Totontepec Mixe
* Khi dùng UI Automation để truy cập các điều khiển của bảng tính Microsoft Excel, NVDA giờ đây có khả năng thông báo khi một ô được trộn. (#12843)
* Thay vì thông báo "có chi tiết", thông tin chi tiết sẽ được thông báo rõ ràng. Ví dụ "có chú thích". (#13649)
* Kích thước bộ cài đặt của NVDA giờ đây được hiển thị trong Windows Programs and Feature. (#13909)

### Sửa lỗi

* Adobe Acrobat / Reader 64 bit sẽ không còn bị treo khi đọc một tài liệu PDF. (#12920)
  * Lưu ý là cần dùng bản cập nhật mới nhất của Adobe Acrobat / Reader để tránh gặp lỗi này.
* Đơn vị đo cỡ chữ đã được phiên dịch trong NVDA. (#13573)
* Bỏ qua các sự kiện của Java Access Bridge khi không thể tìm thấy window handle cho các ứng dụng Java.
Điều này sẽ cải thiện hiệu suất vận hành cho vài ứng dụng Java bao gồm IntelliJ IDEA. (#13039)
* Việc thông báo các ô được chọn cho LibreOffice Calc đã có hiệu quả hơn và không còn làm cho Calc bị đóng băng khi nhiều ô được chọn. (#13232)
* Khi chạy với một tài khoản người dùng khác, Microsoft Edge không còn bị tình trạng không tiếp cận được. (#13032)
* Khi tắt chế độ tăng tốc độ đọc, tốc độ đọc của eSpeakd không còn bị giảm giữa tốc độ 99% và 100%. (#13876)
* Sữa lỗi làm cho hai hộp thoại Quản Lý Các Thao Tác mở cùng lúc. (#13854)

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2022.2.4

Đây là bản phát hành nhằm sửa một lỗi bảo mật.

### Sữa lỗi

* Sửa một lỗi làm cho python console của NVDA có thể mở thông qua trình xem log ở màn hình khóa.
([GHSA-585m-rpvv-93qg](https://github.com/nvaccess/nvda/security/advisories/GHSA-585m-rpvv-93qg))

## 2022.2.3

Đây là bản phát hành vá lỗi, nhằm khắc phục tình trạng một API bị hỏng, được nhắc đến ở phiên bản 2022.2.1.

### Sửa lỗi

* Sửa lỗi làm cho NVDA không thông báo "Màn hình bảo vệ" khi vào một màn hình như thế.
Điều này làm cho NVDA remote không nhận ra các màn hình bảo vệ. (#14094)

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2022.2.2

Đây là bản phát hành vá lỗi, nhằm khắc phục một vấn đề  được nhắc đến ở phiên bản 2022.2.1 với việc nhập thao tác và cử chỉ.

### Sửa lỗi

* Sửa một lỗi làm cho việc nhập thao tác và cử chỉ không luôn hoạt động. (#14065)

## 2022.2.1

Đây là một bản phát hành phụ để sửa lỗi bảo mật.
Vui lòng báo cáo các vấn đề về bảo mật đến <info@nvaccess.org>.

### Sửa các lỗi bảo mật

* Sửa lỗi khai thác  để có thể gọi chạy python console từ màn hình khóa. (GHSA-rmq3-vvhq-gp32)
* Sửa lỗi để có thể thoát khỏi màn hình khóa bằng cách dùng đối tượng điều hướng. (GHSA-rmq3-vvhq-gp32)

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2022.2

Bản phát hành này bao gồm nhiều lỗi được sửa.
Đáng chú ý, có những cải tiến đáng kể cho các ứng dụng trên nền Java, màn hình nổi và các tính năng của Windows.

Đã trình làng những lệnh điều hướng mới trong bảng.
Đã cập nhật Unicode CLDR.
Đã cập nhật LibLouis, bao gồm thêm bảng chữ nổi tiếng Đức.

### Tính năng mới

* Hỗ trợ tương tác với Microsoft Loop Components trong Microsoft Office products. (#13617)
* Đã thêm các lệnh mới để điều hướng trong bảng. (#957)
 * `control+alt+home/end` chuyển tới cột đầu / cuối.
 * `control+alt+pageUp/pageDown` chuyển đến dòng đầu / cuối.
* Đã thêm một kịch bản chưa gán lệnh để chuyển qua lại giữa các chế độ ngôn ngữ và giọng theo vùng miền. (#10253)

### Các thay đổi

* Đã cập nhật NSIS lên phiên bản 3.08. (#9134)
* Đã cập nhật CLDR lên phiên bản 41.0. (#13582)
* Đã cập nhật thư viện phiên dịch chữ nổi liblouis lên [3.22.0](https://github.com/liblouis/liblouis/releases/tag/v3.22.0). (#13775)
  * Bảng chữ nổi mới: tiếng Đức cấp 2 (chi tiết)
* Thêm vai trò mới cho điều khiển "busy indicator". (#10644)
* NVDA giờ đây sẽ thông báo khi không thể thực hiện một hành động của NVDA. (#13500)
  * Điều này bao gồm khi:
    * Sử dụng bản NVDA trên Windows Store.
    * Trong một ngữ cảnh bảo vệ.
    * Chờ phản hồi đến một hộp thoại.

### Sửa lỗi

* Sửa lỗi cho các ứng dụng trên nền Java:
  * NVDA giờ đây sẽ thông báo trạng thái chỉ đọc (read-only). (#13692)
  * NVDA sẽ thông báo trạng thái tắt (disabled)/bật (enabled) một cách chính xác. (#10993)
  * NVDA giờ đây sẽ thông báo phím tắt cho các tính năng. (#13643)
  * NVDA giờ đây đã có thể phát tiếng beep hoặc đọc thông tin trên thanh trạng thái. (#13594)
  * NVDA sẽ không còn gỡ bỏ văn bản từ widgets một cách không chính xác khi  trình bày đến người dùng. (#13102)
  * NVDA giờ đây sẽ thông báo trạng thái của các nút bật / tắt. (#9728)
  * NVDA giờ đây sẽ nhận dạng cửa sổ trong một ứng dụng Java  với nhiều cửa sổ. (#9184)
  * NVDA giờ đây sẽ thông báo thông tin vị trí cho các điều khiển tab. (#13744)
* Sửa lỗi cho chữ nổi:
  * Sửa lỗi đầu ra chữ nổi khi điều hướng qua một số văn bản nhất định trong các điều khiển rich edit của Mozilla, như là soạn thư nháp trong Thunderbird chẳng hạn. (#12542)
  * Khi chữ nổi tự đi theo và  chuột cũng di chuyển với chế độ theo dõi chuột được bật, các lệnh duyệt văn bản giờ đây cập nhật trên màn hình chữ nổi với nội dung được đọc. (#11519)
  * Giờ đây đã có thể kéo màn hình chữ nổi qua nội dung sau khi dùng các lệnh duyệt văn bản. (#8682)
* Bộ cài NVDA giờ đây đã có thể gọi chạy từ một thư mục với các kí tự đặc biệt. (#13270)
* Trong Firefox, NVDA không còn bị lỗi không thông báo được thành phần trong các trang web khi các thuộc tính aria-rowindex, aria-colindex, aria-rowcount hoặc aria-colcount không hợp lệ. (#13405)
* Con trỏ không còn chuyển dòng hay cột khi dùng các lệnh di  chuyển trong bảng để điều hướng tới các ô được trộn. (#7278)
* Khi đọc các tập tin PDF không tương tác được trong Adobe Reader, loại và trạng thái trong biểu mẫu (hộp kiểm và nút radio chẳng hạn) giờ đây được thông báo. (#13285)
* "Khôi phục về cấu hình mặc định" giờ đây đã tiếp cận được trong trình đơn NVDA trong chế độ bảo vệ. (#13547)
* Mọi phím khóa chuột sẽ được mở khi thoát NVDA. Trước đây thì các nút bấm chuột vẫn bị khóa. (#13410)
* Visual Studio giờ đây đã thông báo số dòng. (#13604)
  * Lưu ý là để tính năng này hoạt động, tùy chọn hiển thị dòng phải được bật trong Visual Studio và NVDA.
* Visual Studio giờ đây đã đọc chính xác thụt lề dòng. (#13574)
* NVDA sẽ lại một lần nữa thông báo các chi tiết kết quả tìm kiếm của Start menu trong các bản phát hành gần đây của Windows 10 và 11. (#13544)
* Trong Calculator ở Windows 10 và 11 phiên bản 10.1908 trở lên, NVDA sẽ thông báo kết quả nhiều lệnh được bấm, lệnh từ chế độ chế độ khoa học (scientific) chẳng hạn. (#13383)
* Trong Windows 11, lại có thể điều hướng và tương tác với các thành phần trên giao diện người dùng như  Taskbar và Task View, sử dụng chuột và tương tác cảm ứng. (#13506)
* NVDA sẽ thông báo nội dung thanh trạng thái trong Notepad của Windows 11. (#13688)
* Làm nổi đối tượng điều hướng giờ đây đã hiển thị ngay khi kích hoạt tính năng. (#13641)
* Sửa lỗi đọc các thành phần trong danh sách trong các cột đơn. (#13659, #13735)
* Sửa lỗi tự chuyển ngôn ngữ  của eSpeak cho tiếng Anh và Pháp quay trở lại tiếng Anh của người Anh và tiếng Pháp của người Pháp. (#13727)
* Sửa lỗi tự chuyển ngôn ngữ của  OneCore khi nỗ lực chuyển qua một ngôn ngữ được cài trước đây. (#13732)

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2022.1

Bản phát hành này bao gồm các cải tiến quan trọng cho hỗ trợ UIA với MS Office.
Với Microsoft Office 16.0.15000 và cao hơn trên Windows 11, NVDA mặc định sẽ dùng UI Automation để truy cập các tài liệu Microsoft Word.
Điều này cung cấp một cải thiện hiệu suất vận hành đáng kể so với kiểu truy cập mẫu đối tượng cũ.

Cải tiến cho các trình điều khiển màn hình chữ nổi, bao gồm Seika Notetaker, Papenmeier và HID Braille. 
Nhiều lỗi trên Windows 11 cũng được khắc phục cho các ứng dụng như Calculator, Console, Terminal, Mail và bản biểu tượng cảm xúc (Emoji Panel).

eSpeak-NG và LibLouis đã được cập nhật, thêm các bản chữ nổi mới cho tiếng Nhật, Đức và Catalan.

Lưu ý:

 * Bản phát hành này không tương thích với các add-on hiện tại.

### Tính năng mới

* Hỗ trợ đọc chú thích trong MS Excel với UI Automation được bật trên Windows 11. (#12861)
* Trong các bản dựng gần đây của Microsoft Word thông qua UI Automation trên Windows 11, việc tồn tại các dấu trang, chú thích chính thức và không chính thức giờ đây đã được thông báo bằng tiếng nói và chữ nổi. (#12861)
* Tham số dòng lệnh mới --lang  cho phép bỏ qua ngôn ngữ đã được cấu hình của NVDA. (#10044)
* NVDA giờ đây sẽ cảnh báo về các tham số dòng lệnh không xác định và không được dùng bởi bất cứ add-on nào. (#12795)
* Trong Microsoft Word truy cập qua UI Automation, NVDA giờ đây sẽ dùng mathPlayer để đọc và điều hướng qua các công thức toán của Office. (#12946)
  * Để tính năng này hoạt động, bạn phải dùng Microsoft Word 365/2016 build 14326 trở lên. 
  * Công thức của MathType cũng phải được chuyển thủ công thành công thức toán của Office Math bằng cách chọn mỗi công thức và chọn Equation options -> Convert to Office Math trong trình đơn ngữ cảnh.
* Việc thông báo "có chi tiết" và phím lệnh được tích hợp để tóm lược các chi tiết liên quan đã được cập nhật để hoạt động trong chế độ focus. (#13106)
* Seika Notetaker giờ đây đã có thể tự nhận khi được kết nối qua USB và Bluetooth. (#13191, #13142)
  * Điều này có tác động đến các thiết bị: MiniSeika (16, 24 ô), V6 và V6Pro (40 ô)
  * Cũng đã hỗ trợ chọn thủ công cổng bluetooth COM.
* Thêm lệnh để bật / tắt trình xem chữ nổi; chưa gán thao tác mặc định. (#13258)
* Thêm lệnh để bật / tắt đồng thời nhiều phím bổ trợ với một màn hình chữ nổi. (#13152)
* Hộp thoại từ điển phát âm giờ đây có thêm nút "Xóa tất cả" giúp xóa toàn bộ từ điển. (#11802)
* Thêm hỗ trợ cho Windows 11 Calculator. (#13212)
* Trong Microsoft Word với UI Automation được bật trên Windows 11,  số dòng và số phần giờ đây có thể được đọc lên. (#13283)
* Với Microsoft Office 16.0.15000 và cao hơn trên Windows 11, NVDA mặc định sẽ dùng UI Automation để truy cập tài liệu Microsoft Word, cung cấp một cải thiện hiệu suất vận hành đáng kể so với kiểu truy cập mẫu đối tượng cũ. (#13437)
 * Điều này bao gồm các tài liệu trong chính Microsoft Word, cũng như áp dụng cho việc đọc và soạn thư trong Microsoft Outlook. 

### Các thay đổi

* Espeak-ng đã được cập nhật lên 1.51-dev commit `7e5457f91e10`. (#12950)
* Cập nhật thư viện phiên dịch chữ nổi liblouis lên [3.21.0](https://github.com/liblouis/liblouis/releases/tag/v3.21.0). (#13141, #13438)
  * Thêm bản chữ nổi mới: tiếng Nhật (Kantenji) chữ nổi văn học.
  * Thêm bản chữ nổi máy tính tiếng Đức 6 chấm mới.
  * Thêm bản chữ nổi tiếng Catalan cấp 1. (#13408)
* NVDA sẽ thông báo các ô được chọn và trộn trong LibreOffice Calc 7.3 và cao hơn. (#9310, #6897)
* Cập nhật Unicode Common Locale Data Repository (CLDR) lên 40.0. (#12999)
* `NVDA+Delete bàn phím số` mặc định sẽ thông báo vị trí của con trỏ nháy hoặc đối tượng có focus. (#13060)
* `NVDA+Shift+Delete bàn phím số` thông báo vị trí con trỏ duyệt. (#13060)
* Đã thêm các lệnh mặc định để bật / tắt các phím bổ trợ cho các màn hình của Freedom Scientific (#13152)
* 'Hàng ngang' không còn được thông báo qua lệnh thông báo định dạng văn bản (NVDA+F). (#11815)
* Sẽ không còn thao tác mặc định cho lệnh kích hoạt mô tả dài. (#13380)
* Lệnh thông báo tóm lược chi tiết giờ đã có thao tác mặc định, `NVDA+d`. (#13380)
* NVDA cần được khởi động lại sau khi cài MathPlayer. (#13486)

### Sửa lỗi

* Cửa sổ quản lý bộ nhớ tạm (Clipboard manager pane) sẽ không còn chiếm focus ngoài ý muốn khi mở một vài ứng dụng trong bộ Office. (#12736)
* Trên hệ thống đã được  người dùng hoán đổi hai nút chuột trái phải, NVDA sẽ không còn mở trình đơn ngữ cảnh thay vì kích hoạt một thành phần trong các ứng dụng như trình duyệt web. (#12642)
* Khi di chuyển con trỏ duyệt qua phần cuối của một điều khiển dạng văn bản, như trong Microsoft Word với UI Automation, "bottom"(ở cuối) được thông báo một cách chính xác trong nhiều trường hợp. (#12808)
* NVDA có thể thông báo tên và phiên bản của ứng dụng dạng nhị phân được thiết lập cho system32 khi chạy trên các phiên bản 64-bit của Windows. (#12943)
* Cải thiện tính nhất quán của việc đọc thông tin đầu ra trong các chương trình terminal. (#12974)
  * Lưu ý rằng trong vài trường hợp, khi chèn hay xóa kí tự ở giữa một dòng, kí tự phía sau dấu nháy có thể  bị đọc lại.
* MS word với UIA: việc di chuyển nhanh theo tiêu đề trong chế độ duyệt không còn bị kẹt ở tiêu đề cuối cùng của tài liệu, và cũng không còn tình trạng một tiêu đề được hiển thị hai lần trong cửa sổ danh sách các thành phần. (#9540)
* Trong Windows 8 trở lên, có thể lấy thông tin thanh trạng thái của File Explorer  bằng thao tác chuẩn NVDA+end (desktop) / NVDA+shift+end (laptop). (#12845)
* Các tin nhắn mới trong cửa sổ trò chuyện  của Skype for Business lại được đọc lên. (#9295)
* NVDA lại có thể giảm âm thanh khi dùng các bộ đọc SAPI5 trên Windows 11. (#12913)
* Trong Calculator của Windows 10, NVDA sẽ đọc nhãn cho thành phần trong lịch sử (history) và bộ nhớ (memory). (#11858)
* Các thao tác như cuộn (scrolling) và đưa theo (routing) lại hoạt động với các thiết bị của HID Braille. (#13228)
* Windows 11 Mail: sau khi chuyển focus giữa các ứng dụng, khi đọc một thư điện tử dài, NVDA bị kẹt lại ở một dòng trong thư. (#13050)
* HID braille: các thao tác kết hợp (ví dụ: khoảng trắng+chấm4) có thể thực hiện được trên màn hình chữ nổi. (#13326)
* Sửa lỗi nhiều hộp thoại cài đặt có thể được mở cùng lúc. (#12818)
* Sửa lỗi của vài màn hình chữ nổi Focus Blue Braille bị ngưng hoạt động sau khi bật lại máy tính từ chế độ ngủ. (#9830)
* 'Hàng ngang' không còn bị đọc lên khi tùy chọn 'đọc chỉ số trên và chỉ số dưới' được bật. (#11078)
* Trong Windows 11, NVDA sẽ không bị lỗi chặn không cho di chuyển trong bản biểu tượng cảm xúc (emoji panel) khi chọn chúng. (#13104)
* Khắc phục một lỗi làm cho NVDA đọc hai lần khi dùng Windows Console và Terminal. (#13261)
* Sửa lỗi  trong vài trường hợp, không đọc được thành phần danh sách trong các ứng dụng 64 bit như REAPER. (#8175)
* Trong trình quản lí tải về của Microsoft Edge, NVDA giờ đây sẽ tự chuyển sang chế độ focus khi thành phần trong danh sách với tập tin tải về gần nhất có focus. (#13221)
* NVDA không còn làm cho các phiên bản 64-bit  của Notepad++ 8.3 trở lên bị lỗi. (#13311)
* Adobe Reader không còn bị lỗi khi khởi động nếu đã bật chế độ bảo vệ của Adobe Reader. (#11568)
* Sửa lỗi khi chọn trình điều khiển của  Papenmeier Braille Display làm cho NVDA bị lỗi. (#13348)
* Trong Microsoft word với UIA: số trang và các thông tin định dạng khác không còn bị đọc lên ngoài ý muốn khi di chuyển từ một bảng trống đến một ô có nội dung, hoặc từ cuối tài liệu vào nội dung có sẵn. (#13458, #13459)
* NVDA sẽ không còn bị lỗi không đọc được tên trang và tự đọc khi một trang web được mở trong Google chrome 100. (#13571)
* NVDA không còn bị treo khi khôi phục cấu hình NVDA về mặc định của nhà sản xuất mà chế độ đọc phím lệnh đang bật. (#13634)

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2021.3.5

Đây là bản phát hành phụ để sửa vài lỗi bảo mật.
Vui lòng báo cáo các vấn đề về bảo mật cho <info@nvaccess.org>.

### Sửa các lỗi bảo mật

* Khặc phục lỗi bảo mật được tham mưu `GHSA-xc5m-v23f-pgr7`.
  * Hộp thoại phát âm ký hiệu dấu câu giờ đây bị vô hiệu trong chế độ bảo mật.

## 2021.3.4

Đây là bản phát hành phụ để sửa vài lỗi bảo mật.
Vui lòng báo cáo các vấn đề về bảo mật cho <info@nvaccess.org>.

### Sửa các lỗi bảo mật

* Khặc phục lỗi bảo mật được tham mưu `GHSA-354r-wr4v-cx28`. (#13488)
  * Gỡ bỏ tính năng khởi động NVDA với bản ghi dò lỗi được bật khi NVDA chạy ở chế độ bảo mật.
  * Gỡ bỏ tính năng cập nhật NVDA khi nó chạy ở chế độ bảo mật.
* Khặc phục lỗi bảo mật được tham mưu `GHSA-wg65-7r23-h6p9`. (#13489)
  * Gỡ bỏ tính năng mở hộp thoại quản lí các thao tác trong chế độ bảo mật.
  * Gỡ bỏ tính năng mở  các hộp thoại từ điển mặc định, từ điển giọng đọc và từ điển tạm  trong chế độ bảo mật.
* Khặc phục lỗi bảo mật được tham mưu `GHSA-mvc8-5rv9-w3hx`. (#13487)
  * Công cụ wx GUI inspection giờ được vô hiệu trong chế độ bảo mật.

## 2021.3.3

Bản phát hành này tương đương với 2021.3.2.
Một lỗi tồn tại trong NVDA 2021.3.2 khi đã được xác định sai ở 2021.3.1.
Bản phát hành này xác định chính xác bản thân nó như 2021.3.3.

## 2021.3.2

Đây là bản phát hành phụ để sửa vài lỗi bảo mật.
Vui lòng báo cáo các vấn đề về bảo mật cho <info@nvaccess.org>.

### Sửa lỗi

* Sửa lỗi bảo mật: chặn phương thức điều hướng đối tượng bên ngoài màn hình khóa trên Windows 10 và Windows 11. (#13328)
* Sửa lỗi bảo mật: hộp thoại quản lí các add-on giờ đây bị vô hiệu trong màn hình bảo vệ. (#13059)
* Sửa lỗi bảo mật: trợ giúp theo ngữ cảnh của NVDA không còn hoạt động trên màn hình bảo vệ. (#13353)

## 2021.3.1

Đây là bản phát hành phụ, nhằm sửa vài lỗi trong phiên bản 2021.3.

### Các thay đổi

* Giao thức chữ nổi (HID) mới không còn được ưu tiên khi có thể sử dụng một trình điều khiển màn hình nổi khác. (#13153)
* Có thể vô hiệu giao thức chữ nổi (HID) mới thông qua một cài đặt trong bảng cài đặt nâng cao. (#13180)

### Sửa lỗi

* Lại một lần nữa, các cột mốc đã được viết tắt trong chữ nổi. #13158
* Sửa lỗi hoạt động không ổn định trong việc  tự dò tìm các màn hình nổi của Humanware Brailliant và APH Mantis Q40 khi dùng Bluetooth. (#13153)
 -

## 2021.3

Bản phát hành này bắt đầu hỗ trợ cho chuẩn kết nối (HID)  mới của màn hình nổi.
Chuẩn kết nối này hướng đến tiêu chuẩn hóa việc hỗ trợ các màn hình nổi mà không cần trình điều khiển riêng biệt.
Cập nhật cho eSpeak-NG và LibLouis, bao gồm các bảng chữ nổi mới cho tiếng Nga và tiếng Tshivenda.
Có thể bật các âm thanh báo lỗi trong các bản dựng chính thức của NVDA thông qua một tùy chọn nâng cao mới.
Tính năng đọc tất cả trong  Word giờ đây sẽ cuộn màn hình để hiển thị vị trí hiện tại.
Nhiều cải tiến khi dùng các ứng dụng văn phòng với UIA.
Một lỗi trong UIA đã được sửa là Outlook giờ đây bỏ qua nhiều kiểu bố cục bảng trong thư.

### Các lưu ý quan trọng:

Vì một cập nhật trong chứng nhận bảo mật của chúng tôi, một số ít người dùng đã gặp lỗi khi NVDA 2021.2 kiểm tra cập nhật.
NVDA đã yêu cầu Windows cập nhật chứng nhận bảo mật để sửa lỗi này trong tương lai.
Người dùng gặp lỗi như trên sẽ phải tải bản cập nhật bằng cách thủ công.

### Tính năng mới

* Thêm một thao tác để chuyển đổi giữa các cài đặt cho việc thông báo kiểu đường viền ô. (#10408)
* Hỗ trợ chuẩn kết nối mới của chữ nổi, hướng đến tiêu chuẩn hóa việc hỗ trợ các màn hình nổi. (#12523)
  * Các thiết bị có hỗ trợ chuẩn kết nối này sẽ được NVDA tự nhận diện.
  * Để biết các chi tiết kĩ thuật về việc bổ sung công nghệ này của NVDA, xem tại https://github.com/nvaccess/nvda/blob/master/devDocs/hidBrailleTechnicalNotes.md
* Thêm hỗ trợ cho thiết bị VisioBraille Vario 4. (#12607)
* Có thể bật các thông báo lỗi (cài đặt nâng cao) khi dùng bất cứ phiên bản NVDA nào. (#12672)
* Trong Windows 10 trở lên, NVDA sẽ thông báo số đếm các gợi ý khi nhập nội dung tìm kiếm trong các ứng dụng như Settings và Microsoft Store. (#7330, #12758, #12790)
* Việc điều hướng trong bảng giờ đây đã hỗ trợ trong các điều khiển dạng lưới được tạo bằng cách dùng  Out-GridView cmdlet trong PowerShell. (#12928)

### Các thay đổi

* Espeak-ng đã được cập nhật lên 1.51-dev commit `74068b91bcd578bd7030a7a6cde2085114b79b44`. (#12665)
* NVDA sẽ mặc định dùng bộ đọc eSpeak nếu không cài đặt các giọng đọc OneCore cho ngôn ngữ mà  NVDA đang dùng. (#10451)
* Nếu các giọng đọc OneCore gặp lỗi và không đọc được, sẽ quay về dùng bộ đọc eSpeak. (#11544)
* Khi đọc thanh trạng thái với `NVDA+end`, con trỏ duyệt sẽ không còn di chuyển đến vị trí này nữa.
Nếu cần dùng tính năng này, vui lòng gán thao tác cho kịch bản tương ứng trong phân loại đối tượng điều hướng trong hộp thoại quản lý các thao tác. (#8600)
* Khi mở một hộp thoại cài đặt vốn đã được mở trước đó, NVDA sẽ đưa con trỏ đến hộp thoại thay vì báo lỗi. (#5383)
* Cập nhật thư viện phiên dịch chữ nổi liblouis lên [3.19.0](https://github.com/liblouis/liblouis/releases/tag/v3.19.0). (#12810)
  * Các bảng chữ nổi mới: tiếng Nga cấp 1, Tshivenda cấp 1, Tshivenda cấp 2
* Thay vì thông báo "marked content" hay "mrkd",giờ đây NVDA sẽ thông báo là "highlight" hoặc "hlght" bằng tiếng nói và chữ nổi. (#12892)
* NVDA sẽ không còn cố gắng tắt chương trình khi có các hộp thoại đang chờ một hành động (Xác nhận / Hủy bỏ chẳng hạn). (#12984)

### Sửa lỗi

* Việc theo dõi các phím bổ trợ (Control, Insert chẳng hạn) đã hoạt động hiệu quả hơn. (#12609)
* Đã có thể kiểm tra cập nhật NVDA trên một số hệ thống nhất định; bản Windows mới cài đặt chẳng hạn. (#12729)
* NVDA đã thông báo chính xác các ô rỗng trong Microsoft Word khi dùng UI automation. (#11043)
* Trong dữ liệu ARIA dạng lưới trên web, phím Escape sẽ bị bỏ qua khi ở trong lưới và không còn tắt chế độ focus nếu không có điều kiện. (#12413)
* Khi đọc một ô tiêu đề của một bảng trong Chrome, sửa lỗi đọc lại hai lần tiêu đề cột. (#10840)
* NVDA không còn đọc một giá trị số cho các thanh trượt UIA đã được quy định giá trị bằng văn bản đại diện. (UIA ValuePattern được dùng thay cho RangeValuePattern). (#12724)
* NVDA không còn xem giá trị của các thanh trượt trong UIA là luôn dựa trên phần trăm.
* Việc thông báo vị trí của một ô trong Microsoft Excel khi truy cập thông qua UI Automation lại hoạt động chính xác trên Windows 11. (#12782)
* NVDA không còn đặt ngôn nữ bản địa hóa không hợp lệ của Python. (#12753)
* Nếu gỡ bỏ một add-on đã vô hiệu hóa (đã tắt) và rồi cài lại, nó sẽ được bật. (#12792)
* Sửa các lỗi xung quanh việc cập nhật và gỡ bỏ add-on khi thư mục add-on đã đổi tên hoặc có tập tin đang mở. (#12792, #12629)
* Khi dùng UI Automation để truy cập các điều khiển trong bảng tính của Microsoft Excel, NVDA không còn thông báo khi chỉ một ô được chọn. (#12530)
* Nhiều nội dung trên hộp thoại đã tự được đọc trong LibreOffice Writer,  trong các hộp thoại xác nhận chẳng hạn. (#11687)
* Việc đọc / di chuyển với chế độ duyệt trong Microsoft Word thông qua UI automation giờ đây đảm bảo tài liệu luôn được cuộn để luôn hiển thị vị trí hiện tại trong chế độ duyệt, và vị trí con trỏ nháy trong chế độ focus phản ánh chính xác vị trí trong chế độ duyệt. (#9611)
* Khi thực hiện lệnh đọc tất cả trong Microsoft Word thông qua UI automation, tài liệu giờ đây sẽ được cuộn tự động, và vị trí con trỏ nháy đã được cập nhật một cách chính xác. (#9611)
* Khi đọc thư điện tử trong Outlook và NVDA truy cập nội dung thư với UI Automation, một số bảng nhất định giờ đây được đánh dấu là bảng bố cục, nghĩa là chúng sẽ mặc định không còn bị đọc lên. (#11430)
* Đã sửa một lỗi hiếm gặp khi thay đổi thiết bị âm thanh. (#12620)
* Việc nhập liệu với các bảng chữ nổi văn học  sẽ hoạt động hiệu quả hơn khi ở trong các trường nhập liệu. (#12667)
* Khi di chuyển trong ứng dụng lịch của Windows từ khay hệ thống, NVDA giờ đây đọc ngày của tuần một cách đầy đủ. (#12757)
* Khi dùng một kiểu nhập tiếng Trung Quốc như Taiwan - Microsoft Quick trong Microsoft Word, việc cuộn màn hình chữ nổi tới lui không còn nhảy ngược một cách không chính xác về vị trí con trỏ nháy nguyên thủy. (#12855)
* Khi truy cập tài liệu Microsoft Word thông qua UIA, việc di chuyển theo từng câu (alt+mũi tên xuống / alt+mũi tên lên) đã hoạt động trở lại. (#9254)
* Khi truy cập MS Word với UIA, các dấu thụt lề đoạn đã được thông báo. (#12899)
* Khi truy cập MS Word với UIA, việc thay đổi các lệnh theo dõi và các lệnh được bản địa hóa khác giờ đây đã được đọc trong Word . (#12904)
* Sửa lỗi lặp lại hai lần trong tiếng nói và chữ nổi khi 'description' giống với 'content' hay 'name'. (#12888)
* Trong MS Word với UIA được bật, âm báo lỗi chính tả trong khi nhập liệu được phát một cách chính xác hơn. (#12161)
* Trong Windows 11, NVDA sẽ không còn đọc "pane" khi bấm Alt+Tab để chuyển giữa các chương trình. (#12648)
* Bảng theo dõi chú thích kiểu mới giờ đã được hỗ trợ trong MS Word khi không truy cập tài liệu thông qua UIA. Bấm alt+f12 để di chuyển giữa bảng theo dõi và tài liệu. (#12982)

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2021.2

Bản phát hành này bước đầu hỗ trợ cho Windows 11.
Trong khi  Windows 11 chưa chính thức ra mắt, bản phát hành này được thử nghiệm trên các phiên bản xem trước của nó.
Bản phát hành bao gồm việc sửa một lỗi quan trọng cho tính năng Che Màn Hình (xem thêm phần các lưu ý quan trọng).
Công cụ sửa lỗi COM giờ đây có thể giải quyết nhiều vấn đề trong khi chạy NVDA.
Đã tích hợp các bản cập nhật cho bộ đọc eSpeak và thư viện phiên dịch chữ nổi LibLouis.
Ngoài ra, cũng đã sửa được nhiều lỗi và có nhiều cải thiện, đặc biệt là cải thiện cho chữ nổi và Windows terminals, máy tính, bản biểu tượng cảm xúc và lịch sử bộ nhớ tạm.

### Các lưu ý quan trọng

Do một thay đổi trong Windows Magnification API, tính năng Che Màn Hình phải được cập nhật để hỗ trợ phiên bản mới nhất của Windows.
Hãy dùng NVDA 2021.2 để bật tính năng Che Màn Hình với Windows 10 21H2 (10.0.19044) trở lên.
Điều này áp dụng cho cả Windows 10 Insiders và Windows 11.
Vì mục tiêu bảo mật, khi sử dụng một phiên bản mới của Windows, hãy tìm sự xác nhận trực quan rằng tính năng Che Màn Hình có làm cho màn hình đen toàn bộ.

### Tính năng mới

* Hỗ trợ thử nghiệm cho các ghi chú ARIA:
  * Thêm một lệnh để đọc tổng quan các chi tiết của một đối tượng với aria-details. (#12364)
  * Thêm một tùy chọn trong cài đặt mở rộng để thông báo nếu một đối tượng có các thông tin chi tiết trong chế độ duyệt. (#12439) 
* Trong Windows 10 phiên bản 1909 và cao hơn (bao gồm Windows 11), NVDA sẽ đọc số gợi ý đếm được khi thực hiện tìm kiếm trong File Explorer. (#10341, #12628)
* Trong Microsoft Word, NVDA giờ đây sẽ đọc kết quả của việc thụt lề và thụt lề đoạn khi thực hiện bằng phím tắt. (#6269)

### Các thay đổi

* Đã cập nhật Espeak-ng lên 1.51-dev commit `ab11439b18238b7a08b965d1d5a6ef31cbb05cbb`. (#12449, #12202, #12280, #12568)
* Nếu tùy chọn bài viết được bật trong thiết lập người dùng cho định dạng tài liệu, NVDA sẽ đọc "bài viết" sau khi đọc nội dung. (#11103)
* Đã cập nhật thư viện phiên dịch chữ nổi liblouis lên [3.18.0](https://github.com/liblouis/liblouis/releases/tag/v3.18.0). (#12526)
  * Các bản chữ nổi mới: Bun-ga-ri cấp 1, Burmese (Myanmar) cấp 1, Burmese cấp 2, Kazakhstan cấp 1, Khmer cấp 1, Bắc Kurdish cấp 0, Sepedi cấp 1, Sepedi cấp 2, Sesotho cấp 1, Sesotho cấp 2, Setswana cấp 1, Setswana cấp 2, Tatar cấp 1, Việt Nam cấp 0, Việt Nam cấp 2, Miền Nam Việt Nam cấp 1, Xhosa cấp 1, Xhosa cấp 2, Yakut cấp 1, Zulu cấp 1, Zulu cấp 2
* Windows 10 OCR đã đổi tên thành Windows OCR. (#12690)

### Sửa lỗi

* Trong ứng dụng Calculator của Windows 10, NVDA sẽ thể hiện biểu thức tính toán trên màn hình chữ nổi. (#12268)
* Trong các chương trình terminal trên Windows 10 phiên bản 1607 trở lên, khi thêm hay xóa các kí tự ở giữa một dòng, kí tự bên phải dấu nháy không còn bị đọc lên. (#3200)
  * Diff Match Patch giờ đây mặc định được bật. (#12485)

* Đầu vào chữ nổi đã hoạt động tốt với các bản chữ nổi viết tắt sau: Ả rập cấp 2, Tây Ban Nha cấp 2, Urdu cấp 2, Trung Quốc (Đài Loan, Quan Thoại) cấp 2. (#12541)
* Công cụ sửa lỗi đăng kí COM  giờ đây sửa được nhiều lỗi hơn, đặc biệt là trên Windows 64 bit. (#12560)
* cải thiện việc quản lý các nút cho máy đọc chữ nổi Seika Notetaker của Nippon Telesoft. (#12598)
* Cải thiện việc đọc trong bản biểu tượng cảm xúc và lịch sử bộ nhớ tạm. (#11485)
* Đã cập nhật mô tả ký tự bảng chữ cái tiếng Bengal. (#12502)
* NVDA sẽ được tắt một cách an toàn khi một bản NVDA mới được gọi chạy. (#12605)
* Việc chọn lại trình điều khiển cho màn hình nổi Handy Tech  từ hộp thoại Chọn Màn Hình Nổi không còn xảy ra lỗi. (#12618)
* Windows phiên bản 10.0.22000 trở lên được nhận dạng là Windows 11, không phải Windows 10. (#12626)
* Tính năng che màn hình đã được sửa lỗi và thử nghiệm cho các phiên bản Windows đến 10.0.22000. (#12684)
* Nếu không có kết quả nào hiển thị khi lọc các thao tác, hộp thoại Quản lý các thao tác vẫn tiếp tục hoạt động như mong muốn. (#12673)
* Sửa một lỗi làm cho mục đầu tiên trong trình đơn của một trình đơn con không đọc lên trong vài ngữ cảnh. (#12624)

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2021.1

Bản phát hành này bao gồm tùy chọn hỗ trợ thử nghiệm cho UIA trong Excel và các trình duyệt trên nền Chromium.
Sửa các lỗi cho vài ngôn ngữ và lỗi  truy cập các liên kết trong chữ nổi.
Các cập nhật cho Unicode CLDR, kí hiệu toán học và LibLouis.
Sửa nhiều lỗi và có nhiều cải thiện, bao gồm cải thiện trong  Office, Visual Studio và vài ngôn ngữ.

Lưu ý:

 * Bản phát hành này không tương thích với các add-on đang có.
 * Bản phát hành này cũng ngưng hỗ trợ cho Adobe Flash.
  -

### Tính năng mới

* Sớm hỗ trợ cho UIA với các trình duyệt trên nền Chromium (Edge chẳng hạn). (#12025)
* Tùy chọn hỗ trợ thử nghiệm cho Microsoft Excel thông qua UI Automation. Chỉ khuyên dùng cho Microsoft Excel bản dựng 16.0.13522.10000 trở lên. (#12210)
* Điều hướng dễ hơn cho đầu ra trong NVDA Python Console. (#9784)
  * alt+mũi tên lên xuống đi đến kết quả đầu ra trước và đầu ra kế tiếp (thêm phím shift để chọn).
  * control+l xóa thông tin đầu ra.
* NVDA giờ đây sẽ đọc phân loại được gán cho một cuộc hẹn (appointment) trong Microsoft Outlook nếu có. (#11598)
* Hỗ trợ cho màn hình nổi Seika Notetaker của Nippon Telesoft. (#11514)

### Các thay đổi

* Trong chế độ duyệt, các điều khiển giờ đây có thể được kích hoạt với việc đưa con trỏ nổi trên mô tả của chúng (ví dụ "lnk" cho một liên kết). Điều này đặc biệt hữu dụng để kích hoạt các đối tượng như hộp kiểm không có nhãn. (#7447)
* NVDA giờ đây sẽ ngăn không cho  người dùng thực hiện chức năng Windows 10 OCR nếu đang bật che màn hình. (#11911)
* Đã cập nhật Unicode Common Locale Data Repository (CLDR) lên 39.0. (#11943, #12314)
* Đã thêm nhiều kí hiệu toán học vào từ điển kí hiệu. (#11467)
* Các tập tin hướng dẫn sử dụng, tính năng mới và danh sách các phím lệnh giờ đã có một diện mạo mới. (#12027)
* Giờ đây, sẽ có thông báo "Không được hỗ trợ" khi cố gắng bật / tắt chế độ trình bày theo màn hình trong các ứng dụng không được hỗ trợ, như Microsoft Word. (#7297)
* Tùy chọn 'Cố gắng không đọc các sự kiện lỗi thời của focus trong bản thiết lập nâng cao giờ đây mặc định được bật. (#10885)
  * Có thể tắt nó bằng cách chọn "Không" trong tùy chọn này.
  * Các ứng dụng web  (Gmail chẳng hạn) không còn đọc các thông tin lỗi thời khi di chuyển focus một cách nhanh chóng.
* Đã cập nhật thư viện phiên dịch chữ nổi liblouis lên [3.17.0](https://github.com/liblouis/liblouis/releases/tag/v3.17.0). (#12137)
  * Các bản chữ nổi mới: Belarus chữ nổi văn học, Belarus chữ nổi máy tính, Urdu cấp 1, Urdu cấp 2.
* Hỗ trợ cho nội dung của Adobe Flash đã bị gỡ khỏi NVDA vì việc dùng Flash đang được Adobe ngưng hỗ trợ. (#11131)
* NVDA sẽ bị thoát ngay cả khi các cửa sổ đang mở. Việc thoát chương trình giờ đây sẽ đóng tất cả cửa sổ và hộp thoại của NVDA. (#1740)
* Giờ đây, có thể đóng trình hiển thị nội dung đọc bằng `alt+F4` và có nút đóng để người dùng các thiết bị trỏ dễ tương tác hơn. (#12330)
* Trình xem chữ nổi giờ đây có nút đóng để người dùng các thiết bị trỏ dễ tương tác hơn. (#12328)
* Trong hộp thoại danh sách các thành phần, phím tắt cho nút "Kích hoạt" đã dược gỡ khỏi vài ngôn ngữ để tránh xung đột với loại thành phần nút radio. Khi khả dụng, đây vẫn là nút mặc định của hộp thoại và vẫn có thể kích hoạt bằng cách đơn giản là bấm enter từ danh sách các thành phần. (#6167)

### Sửa lỗi

* Danh sách thư trong Outlook 2010 lại có thể đọc được. (#12241)
* Trong các chương trình terminal trên Windows 10 phiên bản 1607 trở lên, khi chèn hay xóa kí tự ở giữa một dòng, kí tự bên phải kí tự đó không còn bị đọc lên. (#3200)
  * Sửa lỗi thử nghiệm này phải được bật thủ công trong bảng cài đặt nâng cao của NVDA bằng cách đổi thuật toán diff algorithm thành Diff Match Patch.
* Trong MS Outlook, sẽ không còn lỗi thông báo khoảng cách một cách không hợp lý khi shift+tab từ nội dung thư đến trường tiêu đề. (#10254)
* Trong Python Console, việc chèn một tab để thụt lề ở đầu của một dòng nhập liệu không rỗng và thao tác tự hoàn thành bằng tab ở giữa một dòng giờ đã được hỗ trợ. (#11532)
* Thông tin định dạng và các thông điệp có thể duyệt khác không còn đọc là dòng trắng một cách không mong muốn khi tắt trình bày theo màn hình. (#12004)
* Giờ đây, có thể đọc bình luận trong MS Word khi bật UIA. (#9285)
* Khả năng vận hành khi tương tác với Visual Studio đã được cải thiện. (#12171)
* Sửa các lỗi đồ họa như thiếu thành phần khi dùng NVDA với bố cục từ phải sang trái. (#8859)
* Tôn trọng bố cục giao diện người dùng dựa trên ngôn ngữ NVDA, không phải bản địa hóa của hệ thống. (#638)
  * vấn đề đã biết cho các ngôn ngữ từ phải sang trái: bảng bên phải của các nhóm clip với các nhãn / điều khiển. (#12181)
* Phần bản địa của python đã được thiết lập là khớp với ngôn ngữ đã chọn trong tùy chọn, và sẽ xuất hiện khi dùng ngôn ngữ mặc định. (#12214)
* TextInfo.getTextInChunks không còn bị treo khi được gọi trong các điều khiển Rich Edit như trình xem log của NVDA. (#11613)
* Lại có thể dùng NVDA trong các ngôn ngữ có chứa dấu gạch dưới trong tên bản địa của nó như de_CH trên Windows 10 1803 và 1809. (#12250)
* Trong WordPad, cấu hình việc đọc chỉ số trên / chỉ số dưới đã hoạt động như mong muốn. (#12262)
* NVDA không còn bị lỗi khi đọc nội dung mới có focus trên một trang web nếu focus cũ biến mất và được thay thế bằng focus mới ở cùng vị trí. (#12147)
* Định dạng gạch ngang, chỉ số trên và chỉ số dưới cho toàn bộ ô trong Excel giờ đã được đọc nếu bật các tùy chọn tương ứng. (#12264)
* Sửa lỗi sao chép cấu hình trong khi cài đặt từ một bản chạy trực tiếp khi thư mục mặc định để chép cấu hình là thư mục rỗng. (#12071, #12205)
* Sửa lỗi đọc không chính xác cho vài kí tự có âm nhấn hoặc âm tiêu khi bật tùy chọn 'Đọc chữ hoa'. (#11948)
* Sửa lỗi thay đổi cao độ trong các bộ đọc SAPI4. (#12311)
* Bộ cài NVDA giờ đây tôn trọng tham số của dòng lệnh `--minimal` và không phát âm thanh khởi động, hoạt động giống nhau với tập tin thực thi của bản cài hay bản chạy trực tiếp của NVDA. (#12289)
* Trong MS Word hay Outlook, các phím di chuyển nhanh trong bảng giờ đây có thể đi đến bố cục bảng nếu bật tùy chọn "Đọc các bảng bố cục" trong cài đặt chế độ duyệt. (#11899)
* NVDA sẽ không còn đọc "↑↑↑" (các dấu mũi tên lên) cho các biểu tượng cảm xúc trong một số ngôn ngữ. (#11963)
* Espeak giờ đây lại hỗ trợ tiếng Quảng Đông và tiếng Quan Thoại. (#10418)
 * Trong phiên bản  Microsoft Edge mới trên nền tảng Chromium, các trường nhập liệu như thanh địa chỉ giờ đã được đọc khi không có nội dung. (#12474)
* Sửa lỗi trình điều khiển của Seika Braille. (#10787)

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2020.4

Những cải tiến của phiên bản này bao gồm các phương thức nhập mới cho tiếng Trung Quốc, cập nhật thư viện phiên dịch chữ nổi Liblouis và danh sách các thành phần (NVDA+f7) giờ đây đã hoạt động trong chế độ Focus.
Đã có thông tin trợ giúp theo ngữ cảnh khi bấm F1 trong các hộp thoại của NVDA.
Cải tiến các luật quy định trong phát âm kí hiệu, từ điển phát âm, thông điệp bằng chữ nổi và đọc tất cả.
Sửa lỗi và cải tiến cho Mail, Outlook, Teams, Visual Studio, Azure Data Studio, Foobar2000.
Trên web, cải tiến cho Google Docs, hỗ trợ tốt hơn cho ARIA.
Sửa nhiều lỗi và nhiều cải tiến quan trọng khác.

### Tính năng mới

* Bấm F1 trong các  hộp thoại của NVDA giờ đây sẽ mở các phần có liên quan nhất trong tập tin trợ giúp. (#7757)
* Hỗ trợ cho tính năng tự gợi ý (IntelliSense) trong Microsoft SQL Server Management Studio và Visual Studio 2017 trở lên. (#7504)
* Phát âm kí hiệu: hỗ trợ nhóm trong một kí hiệu phức tạp được định nghĩa và hỗ trợ các tham khảo nhóm trong định nghĩa thay thế để chúng trở nên đơn giản và hoạt động hiệu quả hơn. (#11107)
* Giờ đây, người dùng được thông báo khi nỗ lực tạo các từ điển phát âm với các biểu thức phổ thông thay thế không đúng. (#11407)
  * Nhóm các lỗi cụ thể giờ đã được phát hiện.
* Đã thêm hỗ trợ cho các kiểu nhập tiếng Trung Quốc truyền thống Quick và Pinyin trong Windows 10. (#11562)
* Các tiêu đề Tab  giờ đây đã được xem là biểu mẫu với phím di chuyển  nhanh là f. (#10432)
* Thêm lệnh để bật / tắt việc đọc các văn bản đã đánh dấu (được làm nổi); không có thao tác mặc định cho lệnh này. (#11807)
* Đã thêm tham số dòng lệnh --copy-portable-config cho phép tự động sao chép cấu hình được cung cấp vào tài khoản người dùng khi cài đặt NVDA ở chế độ im lặng. (#9676)
* Việc đưa đến ô trong chữ nổi giờ đây đã hỗ trợ cho trình xem chữ nổi với người dùng chuột, di chuyển chuột để đưa đến một ô chữ nổi. (#11804)
* NVDA giờ đây sẽ tự nhận  các thiết bị Humanware Brailliant BI 40X và 20X qua cả USB và Bluetooth. (#11819)

### Các thay đổi

* Đã cập nhật thư viện phiên dịch chữ nổi liblouis lên phiên bản 3.16.1:
 * Tìm và khắc phục được nhiều lỗi
 * Thêm bảng chữ nổi tiếng Bashkir cấp 1
 * Thêm bảng chữ nổi máy tính tiếng Coptic 8 chấm
 * Thêm các bảng chữ nổi văn học tiếng Nga và chữ nổi văn học tiếng Nga (chi tiết).
 * Đã thêm chữ nổi tiếng Nam Phi cấp 2
 * Gỡ bỏ bảng chữ nổi tiếng Nga cấp 1
* Khi đọc với tính năng đọc tất cả trong chế độ duyệt, các lệnh tìm tiếp và tìm trước không dừng đọc nếu tùy chọn Cho phép thay đổi vị trí đọc khi đọc tất cả được bật; việc đọc tất cả sẽ tiếp tục từ sau cụm từ được tìm thấy. (#11563)
* Với màn hình chữ nổi của HIMS, F3 đã được đổi thành khoảng trắng + chấm 148. (#11710)
* Cải tiến cho tùy chọn "thời gian kết thúc thông điệp chữ nổi" và "Hiển thị vô thời hạn". (#11602)
* Trong các trình duyệt web và các ứng dụng khác có hỗ trợ chế độ duyệt, hộp thoại danh sách các thành phần (NVDA+F7) giờ đây có thể gọi chạy khi ở trong chế độ focus. (#10453)
* Các cập nhật đến ARIA live regions giờ đây bị ngăn lại khi  tùy chọn thông báo các thay đổi nội dung động bị tắt. (#9077)
* NVDA giờ đây sẽ đọc "Đã chép lên bộ nhớ tạm" trước văn bản được sao chép. (#6757)
* Đã cải thiện cách thể hiện bảng xem dạng ảnh trong disk management. (#10048)
* Nhãn cho các điều khiển giờ đây sẽ bị vô hiệu (mờ đi) khi điều khiển đó không hoạt động. (#11809)
* Cập nhật CLDR emoji annotation lên phiên bản 38. (#11817)
* Tính năng "Làm nổi Focus" đã đổi tên thành "Làm Nổi Trực Quan". (#11700)

### Sửa lỗi

* NVDA lại một lần nữa hoạt động chính xác với các trường nhập liệu khi dùng ứng dụng Fast Log Entry. (#8996)
* Thông báo thời gian đã trôi qua trong Foobar2000 nếu không có tổng thời gian (ví dụ, khi nghe một chương trình phát trực tiếp). (#11337)
* NVDA giờ đây tôn trọng thuộc tính aria-roledescription trên các danh sách trong nội dung có thể chỉnh sửa trong các trang web. (#11607)
* 'danh sách' không còn bị đọc trên mọi dòng của danh sách trong Google Docs hay các nội dung có thể chỉnh sửa khác trong Google Chrome. (#7562)
* Khi di chuyển mũi tên theo từ hay kí tự từ một thành phần trong danh sách sang thành phần khác trong nội dung có thể chỉnh sửa trên web, việc vào một thành phần mới của danh sách giờ đây đã được thông báo. (#11569)
* NVDA giờ đây đọc chính xác các dòng khi  dấu nháy được đặt ở cuối một liên kết ở cuối một thành phần danh sách  trong Google Docs hoặc các nội dung có thể chỉnh sửa khác trên  web. (#11606)
* Trên Windows 7, việc mở và đóng trình đơn Start từ desktop giờ đây đã đặt focus chính xác. (#10567)
* Khi "Cố gắng không đọc các sự kiện lỗi thời của focus:" được bật, tên của tab lại được đọc khi chuyển giữa các  tab trong Firefox. (#11397)
* NVDA không còn bị lỗi không đọc được thành phần trong danh sách sau khi nhập một kí tự trong một danh sách khi đọc với các giọng SAPI5 Ivona. (#11651)
* Lại có thể dùng được chế độ duyệt khi đọc thư điện tử trong Windows 10 Mail 16005.13110 trở lên. (#11439)
* Khi dùng các giọng SAPI5 Ivona từ harposoftware.com, NvDA giờ đây đã lưu được cấu hình, chuyển đổi bộ đọc, và không còn bị ở trạng thái im lặng sau khi khởi động lại. (#11650)
* Giờ đây, đã có thể nhập số 6 trong  chữ nổi máy tính từ bàn phím chữ nổi trên các màn hình của HIMS. (#11710)
* Các cải tiến phụ cho hiệu suất vận hành trong Azure Data Studio. (#11533, #11715)
* Với "Cố gắng không đọc các sự kiện lỗi thời của focus:" được bật, tên của hộp thoại tìm kiếm của NVDA lại được đọc. (#11632)
* NVDA sẽ không còn bị đóng băng khi mở lại máy tính và focus lại ở một tài liệu mở bằng Microsoft Edge. (#11576)
* Không cần phải bấm tab hoặc chuyển focus sau khi đóng một trình đơn ngữ cảnh trong MS Edge để chế độ duyệt hoạt động trở lại. (#11202)
* NVDA không còn bị lỗi khi đọc thành phần trong danh sách với một ứng dụng 64-bit như  Tortoise SVN. (#8175)
* ARIA treegrids giờ đây được thể hiện như một bản biểu bình thường ở chế độ duyệt trong cả Firefox và Chrome. (#9715)
* việc tìm lại nội dung trước, giờ đây có thể thực hiện với lệnh 'tìm trước' thông qua NVDA+shift+F3 (#11770)
* Một kịch bản NVDA không còn bị xem là đang lặp lại nếu một phím không liên quan được bấm giữa hai lần gọi kịch bản. (#11388) 
* Các thẻ nhấn mạnh (strong và emphasis) trong Internet Explorer giờ đây lại có thể được tắt không cho đọc bằng cách tắt tùy chọn báo nhận mạnh trong cài đặt định dạng tài liệu của NVDA. (#11808)
* Việc bị treo vài giây được báo về bởi một số ít người dùng khi di chuyển bằng mũi tên giữa các ô trong Excel không còn xảy ra nữa. (#11818)
* Trong Microsoft Teams với các số bản dựng như 1.3.00.28xxx, NVDA không còn bị lỗi không đọc được các tin nhắn trong phần trò chuyện hay Teams channels vì  trình đơn focused không chính xác. (#11821)
* Văn bản được đánh dấu là có cả lỗi chính tả và ngữ pháp trong Google Chrome sẽ được NVDA thông báo chính xác là có cả lỗi chính tả và ngữ pháp. (#11787)
* Khi sử dụng Outlook (bản tiếng Pháp), phím tắt trả lời tất cả (control+shift+R) đã hoạt động lại bình thường. (#11196)
* Trong Visual Studio, các thông báo trợ giúp cho công cụ ụIntelliSense, cung cấp các chi tiết ban đầu về thành phần hiện được chọn trong IntelliSense giờ đây chỉ đọc một lần. (#11611)
* Trong ứng dụng Calculator của Windows 10, NVDA sẽ không đọc tiến độ của việc tính toán nếu chế độ đọc kí tự trong khi nhập bị vô hiệu hóa. (#9428)
* NVDA không còn bị lỗi khi dùng tiếng Anh cấp 2 và mở rộng ra chữ nổi máy tính tại vị trí con trỏ khi hiển thị một số nội dung nhất định như URL trong chữ nổi. (#11754)
* Lại có thể xem được thông tin định dạng cho ô có focus trong Excel bằng NVDA+F. (#11914)
* Kiểu nhập QWERTY trên các màn hình chữ nổi Papenmeier được hỗ trợ đã hoạt động trở lại và không còn làm cho NVDA bị đóng băng. (#11944)

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2020.3

Bản phát hành này bao gồm vài cải tiến lớn cho tính ổn định và hiệu suất vận hành, cụ thể là trong các ứng dụng Microsoft Office. Các thiết lập mới để bật / tắt hỗ trợ tương tác cảm ứng và thông báo hình ảnh.
Có thể đọc được nội dung có tồn tại các điểm đánh dấu (được làm nổi) trong các trình duyệt, và thêm các bản chữ nổi tiếng Đức mới.

### Tính năng mới

* Giờ bạn có thể bật / tắt việc đọc hình ảnh từ cài đặt định dạng tài liệu của NVDA. Lưu ý là việc tắt tùy chọn này vẫn sẽ đọc văn bản thay thế của ảnh. (#4837)
* Giờ bạn có thể bật / tắt hỗ trợ màn hình cảm ứng của NVDA. Một tùy chọn đã được thêm vào bảng tương tác cảm ứng trong cài đặt NVDA. Phím tắt mặc định là NVDA+control	alt+t. (#9682)
* Đã thêm các bảng chữ nổi tiếng Đức mới. (#11268)
* NVDA giờ đã nhận được văn bản có thuộc tính chỉ đọc với các điều khiển UIA. (#10494)
* Nội dung có tồn tại các điểm đánh dấu (được làm nổi) đã được thể hiện ở cả tiếng nói và chữ nổi trên tất cả các trình duyệt. (#11436)
 * Có thể bật / tắt tính năng này bởi một tùy chọn định dạng mới về làm nổi của NVDA.
* Có thể thêm các phím mô phỏng bàn phím hệ thống từ hộp thoại Quản lý các thao tác của NVDA. (#6060)
  * Để làm điều này, hãy bấm nút thêm sau khi chọn phân loại phím mô phỏng bàn phím hệ thống.
* Đã hỗ trợ cho màn hình nổi Handy Tech Active Braille với cần điều khiển. (#11655)
* Thiết lập "Tự chuyển sang chế độ focus khi di chuyển con trỏ nháy" giờ đã tương thích với việc vô hiệu hóa "Tắt tự đưa con trỏ hệ thống đến các thành phần có thể có focus". (#11663)

### Các thay đổi

* Kịch bản đọc định dạng (NVDA+f) giờ đã thay đổi để đọc định dạng tại dấu nháy hệ thống thay vì đọc tại vị trí của con trỏ duyệt. Để đọc định dạng tại vị trí con trỏ duyệt, bấm NVDA+shift+f. (#9505)
* NVDA không còn mặc định tự đặt focus hệ thống vào các thành phần có thể có focus trong chế độ duyệt, nhằm cải thiện hiệu năng và tính ổn định. (#11190)
* Đã cập nhật CLDR từ phiên bản 36.1 lên phiên bản 37. (#11303)
* Đã cập nhật eSpeak-NG lên 1.51-dev, commit 1fb68ffffea4
* Giờ bạn có thể dùng lệnh điều hướng của bảng trong các hộp danh sách với các thành phần có thể đánh dấu chọn khi một danh sách cụ thể có nhiều cột. (#8857)
* Trong trình quản lý các Add-on, khi được yêu cầu xác nhận gỡ bỏ một add-on, "No" (không) sẽ là lựa chọn mặc định. (#10015)
* Trong Microsoft Excel, hộp thoại danh sách các thành phần giờ đây trình bày các công thức như nó đã được bản địa hóa. (#9144)
* NVDA giờ đây đã đọc chính xác thuật ngữ cho các chú thích trong  MS Excel. (#11311)
* Khi dùng lệnh  "di chuyển con trỏ duyệt đến focus" trong chế độ duyệt, con trỏ duyệt giờ đây được đặt tại vị trí của dấu nháy ảo. (#9622)
* Các thông tin được đọc trong chế độ duyệt như thông tin định dạng với NVDA+F, giờ đây được hiển thị trong một cửa sổ lớn hơn ở giữa màn hình. (#9910)

### Sửa lỗi

* Giờ đây, NVDA luôn đọc khi di chuyển qua từng từ và đứng tại mọi kí hiệu đơn có dấu khoảng trắng phía sau, ở bất cứ cài đặt cấp độ đọc dấu câu nào. (#5133)
* Trong các ứng dụng dùng QT 5.11 trở lên, các mô tả đối tượng lại được đọc. (#8604)
* Khi xóa một từ với control+delete, NVDA không còn im lặng. (#3298, #11029)
  * Giờ đây, từ bên phải của từ bị xóa đã được đọc.
* Trong bảng cài đặt chung, danh sách ngôn ngữ giờ đã được sắp xếp một cách chính xác. (#10348)
* Trong hộp thoại Quản lý các thao tác, cải thiện đáng kể hiệu suất vận hành khi lọc thao tác / phím tắt. (#10307)(
* Giờ bạn có thể gửi các kí tự Unicode  ra U+FFFF từ một màn hình chữ nổi. (#10796)
* NVDA sẽ đọc nội dung của hộp thoại Open With  trong Windows 10 May 2020 Update. (#11335)
* Một tùy chọn thử nghiệm mới trong  cài đặt nâng cao (Bật các chọn lọc đăng kí cho các thay đổi sự kiện và thuộc tính của UI Automation) có thể cung cấp các cải thiện hiệu suất vận hành lớn trong Microsoft Visual Studio và các ứng dụng khác trên nền tảng UIAutomation nếu được bật. (#11077, #11209)
* Với danh sách các thành phần có thể đánh dấu chọn, thành phần đã chọn không còn bị đọc một cách dư thừa, và nếu có thể, thành phần không được chọn sẽ được đọc thay. (#8554)
* Trên Windows 10 May 2020 Update, NVDA giờ đã hiển thị Microsoft Sound Mapper khi xem các thiết bị đầu ra từ hộp thoại chọn bộ đọc. (#11349)
* Trong Internet Explorer, các số giờ đây đã được đọc một cách chính xác với danh sách có thứ tự nếu nó không bắt đầu với 1. (#8438)
* Trong Google chrome, NVDA giờ đây sẽ đọc chưa chọn cho tất cả các điều khiển có thể chọn (không chỉ với các hộp kiểm) hiện chưa được chọn. (#11377)
* Lại một lần nữa có thể điều hướng trong nhiều điều khiển khi ngôn ngữ của NVDA được thiết lập là Aragonese. (#11384)
* NVDA không còn thỉnh thoảng bị treo trong Microsoft Word khi bấm nhanh  mũi tên lên xuống hay gõ các kí tự khi đã bật chữ nổi. (#11431, #11425, #11414)
* NVDA không còn thêm dấu cách không tồn tại khi sao chép đối tượng điều hướng hiện tại vào bộ nhớ tạm. (#11438)
* NVDA không còn kích hoạt hồ sơ đọc tất cả khi không có gì để đọc. (#10899, #9947)
* NVDA không còn tình trạng không đọc được phần features list trong  Internet Information Services (IIS) Manager. (#11468)
* NVDA giờ đây giữ thiết bị audio  ở trạng thái mở, nhằm cải thiện hiệu năng trên vài thiết bị âm thanh (#5172, #10721)
* NVDA sẽ không còn bị treo hay bị tắt khi nhấn giữ control+shift+mũi tên xuống trong Microsoft Word. (#9463)
* Trạng thái đã mở rộng đã thu gọn của thư mục trong cây thư mục trên drive.google.com giờ đây luôn được đọc bởi NVDA. (#11520)
* NVDA sẽ tự nhận màn hình nổi NLS eReader Humanware qua Bluetooth như tên Bluethooth của nó giờ đây là "NLS eReader Humanware". (#11561)
* Cải thiện hiệu suất vận hành trong Visual Studio Code. (#11533)

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2020.2

Các cải tiến của bản phát hành này bao gồm hỗ trợ một màn hình chữ nổi mới từ Nattiq, hỗ trợ tốt hơn cho ESET antivirus giao diện đồ họa và Windows Terminal, cải thiện hiệu năng vận hành với 1Password và bộ đọc Windows OneCore. Nhiều lỗi quan trọng khác cũng được sửa.

### Tính năng mới

* Hỗ trợ các màn hình chữ nổi mới:
  * Nattiq nBraille (#10778)
* Đã thêm kịch bản để mở thư mục cấu hình của NVDA (không có thao tác / phím tắt mặc định). (#2214)
* Hỗ trợ tốt hơn cho giao diện đồ họa của ESET antivirus. (#10894)
* Đã thêm hỗ trợ cho Windows Terminal. (#10305)
* Đã thêm lệnh để thông báo hồ sơ cấu hình đang hoạt động (không có thao tác mặc định). (#9325)
* Đã thêm lệnh để bật / tắt đọc  chỉ số dưới và chỉ số trên (không có thao tác mặc định). (#10985)
* Các ứng dụng web (Gmail chẳng hạn) không còn đọc các thông tin lỗi thời khi chuyển focus một cách nhanh chóng. (#10885)
  * Thử nghiệm sửa lỗi này phải được bật thủ công thông qua tùy chọn 'Cố gắng không đọc các sự kiện lỗi thời của focus' trong bảng cài đặt mở rộng.
* Nhiều kí hiệu đã được thêm vào từ điển kí hiệu mặc định. (#11105)

### Các thay đổi

* Cập nhật thư viện phiên dịch chữ nổi liblouis từ 3.12 lên [3.14.0](https://github.com/liblouis/liblouis/releases/tag/v3.14.0). (#10832, #11221)
* Việc đọc các chỉ số trên và chỉ số dưới  giờ đây được điều khiển riêng biệt với việc đọc thuộc tính phông. (#10919)
* Do các thay đổi trong VS Code, NVDA không còn mặc định tắt chế độ duyệt trong Code. (#10888)
* NVDA không còn đọc thông điệp "trên cùng" và "cuối" khi di chuyển con trỏ duyệt đến dòng đầu hay cuối của đối tượng điều hướng hiện tại với kịch bản Chuyển đến dòng trên và dưới cùng của con trỏ duyệt. (#9551)
 * NVDA không còn đọc thông điệp "trái" và "phải" khi di chuyển con trỏ duyệt đến kí tự đầu hay cuối một dòng của đối tượng điều hướng hiện tại với kịch bản Chuyển về đầu  và cuối dòng của con trỏ duyệt. (#9551)

### Sửa lỗi

* NVDA giờ đây khởi động bình thường khi không thể tạo được tập tin log. (#6330)
* Trong các bản phát hành gần đây của Microsoft Word 365, NVDA không còn đọc "delete back word" khi bấm Control+Xóa lùi trong lúc soạn thảo một tài liệu. (#10851)
* Trong Winamp, NVDA lại một lần nữa sẽ đọc trạng thái chuyển của chế độ ngẫu nhiên (shuffle) và lặp lại (repeat). (#10945)
* NVDA không còn vận hành chậm chạp khi di chuyển trong danh sách thành phần trong 1Password. (#10508)
* Bộ đọc Windows OneCore không còn bị chậm chạp giữa các câu nói. (#10721)
* NVDA không còn treo khi bạn mở trình đơn ngữ cảnh của 1Password trong vùng thông báo hệ thống. (#11017)
* Trong Office 2013 về trước:
  * Ribbons đã được đọc khi focus chuyển đến chúng lần đầu tiên. (#4207)
  * Các thành phần trên trình đơn ngữ cảnh lại được đọc chính xác. (#9252)
  * Các phần của ribbon đã được đọc nhất quán khi điều hướng với Control+mũi tên. (#7067)
* Ở chế độ duyệt trong Mozilla Firefox và Google Chrome, văn bản không còn hiển thị không chính xác trên một dòng riêng biệt khi nội dung web dùng CSS display: inline-flex. (#11075)
* Ở chế độ duyệt với tùy chọn Tắt tự đưa con trỏ hệ thống đến các thành phần có thể có focus bị tắt, giờ đây có thể kích hoạt các thành phần không thể có focus.
* Ở chế độ duyệt với tùy chọn Tắt tự đưa con trỏ hệ thống đến các thành phần có thể có focus bị tắt, giờ đây có thể kích hoạt các thành phần tiếp cận được bằng cách bấm phím tab. (#8528)
* Ở chế độ duyệt với tùy chọn Tắt tự đưa con trỏ hệ thống đến các thành phần có thể có focus bị tắt, việc kích hoạt vài thành phần nhất định không còn kích hoạt sai vị trí. (#9886)
* Không còn nghe âm báo lỗi của NVDA khi truy cập các điều khiển DevExpress text. (#10918)
* Thông báo trên các biểu tượng trong khay hệ thống không còn được đọc khi điều hướng bằng bàn phím nếu nội dung đó giống với tên của biểu tượng, nhằm tránh đọc lại hai lần. (#6656)
* Ở chế độ duyệt với tùy chọn Tắt tự đưa con trỏ hệ thống đến các thành phần có thể có focus bị tắt, việc chuyện sang chế độ focus với NVDA+khoảng trắng giờ đây sẽ đặt thành phần  ở vị trí con trỏ nháy. (#11206)
* Lại có thể  kiểm tra cập nhật NVDA trên một số hệ thống nhất định; bản cài Windows mới hoàn toàn chẳng hạn. (#11253)
* Focus không di chuyển trong các ứng dụng Java khi sự lựa chọn bị thay đổi trong một thành phần không có focus dạng cây thư mục, bảng hay danh sách. (#5989)

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2020.1

Các cải tiến của bản phát hành này bao gồm hỗ trợ cho vài màn hình chữ nổi mới từ HumanWare và APH, thêm nữa là sửa nhiều lỗi quan trọng như khả năng đọc công thức toán trong Microsoft Word sử dụng MathPlayer / MathType.

### Tính năng mới

* Thành phần đang được chọn trong các hộp danh sách lại được thể hiện ở chế độ duyệt trong Chrome, tương tự như NVDA 2019.1. (#10713)
* Giờ bạn có thể thực hiện lệnh bấm chuột phải trên các thiết bị cảm ứng bằng thao tác nhấn giữ một ngón tay. (#3886)
* Hỗ trợ các màn hình nổi mới: APH Chameleon 20, APH Mantis Q40, HumanWare BrailleOne, BrailleNote Touch v2và NLS eReader. (#10830)

### Các thay đổi

* NVDA sẽ chặn không cho hệ thống bị khóa hay bật chế độ ngủ khi đang đọc tất cả. (#10643)
* Hỗ trợ cho out-of-process iframes trong Mozilla Firefox. (#10707)
* Cập nhật thư viện phiên dịch chữ nổi liblouis lên phiên bản 3.12. (#10161)

### Sửa lỗi

* Sửa lỗi NVDA không đọc kí hiệu dấu âm bảng mã Unicode (U+2212). (#10633)
* Khi cài add-on từ trình quản lý add-on, tên thư mục và tập tin trong cửa sổ duyệt tập tin không còn bị đọc hai lần. (#10620, #2395)
* Trong Firefox, khi gọi Mastodon với chế độ giao diện web mở rộng được bật, tất cả dòng thời gian giờ đây đã trả về một cách chính xác trong chế độ duyệt. (#10776)
* Trong chế độ duyệt, NVDA giờ đây đã đọc "chưa chọn" cho các hộp kiểm chưa chọn mà trước đây thỉnh thoảng nó không đọc. (#10781)
* Các điều khiển chuyển ARIA  không còn đọc các thông tin gây bối rối như  "chưa kích hoạt đã chọn" hay "đã kích hoạt đã chọn". (#9187)
* Các giọng SAPI4 không còn từ chối đọc một số nội dung nhất định. (#10792)
* NVDA lại có thể đọc và tương tác với các công thức toán trong Microsoft Word. (#10803)
* NVDA sẽ lại đọc các văn bản hiện chưa được chọn trong chế độ duyệt nếu bấm một phím mũi tên trong khi văn bản đã được chọn. (#10731).
* NVDA không còn bị thoát khi có lỗi trong quá trình khởi động eSpeak. (#10607)
* Các lỗi gây ra bởi unicode trong việc phiên dịch cho biểu tượng không còn làm cho trình cài đặt bị dừng, nó sẽ trở lại nội dung bằng tiếng Anh. (#5166, #6326)
* Việc bấm mũi tên để thoát khỏi danh sách và bảng biểu trong khi đọc tất cả với chế độ thay đổi vị trí trong khi đọc được bật không còn liên tục thông báo đang thoát khỏi danh sách hay bảng biểu. (#10706)
* Sửa lỗi theo dõi chuột cho vài thành phần MSHTML trong Internet Explorer. (#10736)

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2019.3

NVDA 2019.3 là bản phát hành rất quan trọng, có nhiều thay đổi bên trong, bao gồm việc  nâng cấp từ Python 2 lên Python 3, và viết lại một chút cho phần tiếng nói hệ thống phụ của NVDA.
Dù rằng những thay đổi này làm mất tính tương thích với add-on của các bản NVDA cũ hơn, việc nâng cấp lên Python 3 là cần thiết cho tính bảo mật, và các thay đổi với tiếng nói  cho phép   vài cải tiến thú vị trong tương lai gần.
 Những điểm nổi bật khác trong bản phát hành này bao gồm hỗ trợ cho Java VMs 64 bit, chức năng che màn hình và làm nổi Focus, hỗ trợ nhiều màn hình nổi cũng như trình xem chữ nổi mới và sửa nhiều lỗi khác.

### Tính năng mới

* Độ chính xác của lệnh di chuyển chuột đến đối tượng điều hướng đã được cải thiện ở các trường văn bản trong các ứng dụng Java. (#10157)
* Thêm hỗ trợ cho các  màn hình nổi Handy Tech sau (#8955):
 * Basic Braille Plus 40
 * Basic Braille Plus 32
 * Connect Braille
* Có thể xóa tất cả các thao tác / phím tắt do người dùng gán (user-defined gestures) thông qua nút "Khôi phục về cấu hình mặc định" trong hộp thoại Quản lý các thao tác. (#10293)
* Việc thông báo font trong Microsoft Word giờ đây đã bao gồm thông báo nội dung được đánh dấu là ẩn. (#8713)
* Thêm lệnh di chuyển con trỏ duyệt đến vị trí mà trước đó được chọn là điểm bắt đầu cho vùng chọn hoặc sao chép: NVDA+shift+F9. (#1969)
* Trong Internet Explorer, Microsoft Edge, các phiên bản gần đây của Firefox và Chrome, các cột mốc giờ đây đã được đọc trong chế độ focus và chế độ duyệt đối tượng. (#10101)
* Trong Internet Explorer, Google Chrome và Mozilla Firefox, bạn có thể điều hướng theo bài viết  (article) và grouping bằng các kịch bản di chuyển nhanh. Những kịch bản này mặc định không có thao tác / phím tắt và có thể gán trong hộp thoại Quản lý các thao tác khi nó được mở từ một tài liệu ở chế độ duyệt. (#9485, #9227)
 * Hình giáng (figure) cũng đã được thông báo. Chúng được coi là đối tượng nên sẽ duyệt bằng phím di chuyển nhanh là o.
* Trong Internet Explorer, Google Chrome và Mozilla Firefox, các thành phần dạng article giờ đây đã được đọc với việc điều hướng đối tượng, và tùy chọn trong chế độ duyệt nếu bật trong cài đặt Định dạng tài liệu. (#10424)
* Thêm tính năng che màn hình. Khi bật, sẽ làm đen màn hình từ Windows 8 trở lên. (#7857)
 * Thêm một kịch bản để bật che màn hình (cho đến khi khởi động lại nếu bấm một lần, luôn bật khi chạy NVDA nếu bấm hai lần), chưa được gán thao tác / phím tắt.
  * Có thể bật và cấu hình thông qua phân loại 'nhìn' trong hộp thoại cấu hình NVDA.
  * Thêm chức năng làm nổi bật màn hình cho NVDA. (#971, #9064)
   * Việc làm nổi bật vị trí focus, đối tượng điều hướng và dấu nháy chế độ duyệt có thể được kích hoạt và cấu hình  thông qua phân loại 'nhìn' trong hộp thoại cấu hình NVDA.
 * Lưu ý: tính năng này không tương thích với add-on focus highlight. Tuy nhiên,  add-on này vẫn có thể sử dụng khi tắt tính năng làm nổi có sẵn.
* Thêm trình xem chữ nổi, cho phép  xem đầu ra chữ nổi qua một cửa sổ trên màn hình. (#7788)

### Các thay đổi

* Hướng dẫn sử dụng giờ đây có mô tả cách sử dụng NVDA trong Windows Console. (#9957)
* Giờ đây, gọi chạy nvda.exe mặc định sẽ thay thế một phiên bản NVDA đang chạy. Tham số dòng lệnh -r|--replace vẫn còn được nhận, nhưng chương trình sẽ bỏ qua. (#8320)
* Trên Windows 8 và cao hơn, NVDA giờ đây sẽ đọc thông tin tên và phiên bản của  nhóm các ứng dụng như ứng dụng tải về từ Microsoft Store bằng các thông tin được cung cấp bởi ứng dụng đó. (#4259, #10108)
* Khi bật / tắt tính năng track changes (theo dõi thay đổi) bằng bàn phím trong Microsoft Word, NVDA sẽ đọc trạng thái của thiết lập. (#942) 
* Phiên bản NVDA sẽ được ghi ở thông điệp đầu tiên trong log. Điều này xảy ra ngay cả khi chế độ log bị tắt. (#9803)
* Hộp thoại cài đặt giờ đây không còn cho phép thay đổi mức độ log đã cấu hình nếu nó đã được ghi đè từ dòng lệnh. (#10209)
* Trong Microsoft Word, NVDA giờ đây đọc được trạng thái hiển thị của các kí tự không in được khi bấm phím bật / tắt Ctrl+Shift+8 . (#10241)
* Đã cập nhật thư viện phiên dịch chữ nổi liblouis lên commit 58d67e63. (#10094)
* Khi bật đọc các kí tự CLDR (bao gồm emojis - biểu tượng cảm xúc), chúng sẽ được đọc ở cấp độ dấu câu tất cả. (#8826)
* Các gói python của bên thứ ba đã bao gồm trong NVDA như comtypes, giờ đây sẽ ghi các cảnh báo và lỗi của chúng vào NVDA log. (#10393)
* Đã cập nhật Unicode Common Locale Data Repository emoji annotations lên phiên bản 36.0. (#10426)
* Khi đứng tại một grouping trong chế độ duyệt, mô tả giờ đây đã được đọc. (#10095)
* Java Access Bridge giờ đây đã được tích hợp vào NVDA để bật khả năng tương tác các ứng dụng Java, bao gồm cả 64 bit Java VMs. (#7724)
* Nếu Java Access Bridge không được bật cho người dùng, NVDA sẽ tự bật nó khi khởi động NVDA. (#7952)
* Cập nhật eSpeak-NG lên 1.51-dev, commit ca65812ac6019926f2fbd7f12c92d7edd3701e0c. (#10581)

### Sửa lỗi

* Emoji và các kí tự 32 bit unicode khác giờ đây chiếm ít không gian trên màn hình chữ nổi khi chúng hiển thị ở giá trị hexadecimal. (#6695)
* Trong Windows 10, NVDA sẽ đọc các thông tin giúp đỡ (tooltips) từ các ứng dụng phổ cập nếu NVDA được cấu hình để đọc thông tin giúp đỡ trong hộp thoại trình bày các đối tượng. (#8118)
* Trên Windows 10 Anniversary Update trở lên, văn bản được nhập giờ đây đã được đọc trong Mintty. (#1348)
* Trên Windows 10 Anniversary Update trở lên, các thông tin đầu ra trong Windows Console xuất hiện gần dấu nháy  không còn bị đánh vần nữa. (#513)
* Các điều khiển trong hộp thoại compressor của Audacity giờ đã được đọc khi điều hướng trong hộp thoại. (#10103)
* NVDA không còn xem các khoảng trắng là từ ở chế độ duyệt đối tượng trong các trình soạn thảo trên nền Scintilla như Notepad++. (#8295)
* NVDA sẽ ngăn chặn hệ thống vào chế độ ngủ khi cuộn qua văn bản với các thao tác của màn hình chữ nổi. (#9175)
* Trên Windows 10, chữ nổi giờ đây sẽ đi theo khi chỉnh sửa nội dung ô trong Microsoft Excel và các điều khiển văn bản UIA khác đã bị tràn nội dung sang bên cạnh. (#9749)
* NVDA một lần nữa sẽ đọc gợi ý trên thanh địa chỉ của Microsoft Edge. (#7554)
* NVDA không còn bị im lặng khi con trỏ ở tại một điều khiển thẻ tiêu đề HTML trong Internet Explorer. (#8898)
* Trong Microsoft Edge trên nền EdgeHTML, NVDA sẽ không còn phát âm thanh gợi ý tìm kiếm khi phóng lớn cửa sổ. (#9110, #10002)
* Các hộp xổ ARIA 1.1  giờ đây đã được hỗ trợ trong Mozilla Firefox và Google Chrome. (#9616)
* NVDA sẽ không còn đọc các nội dung của các cột ẩn trực quan cho  thành phần của danh sách trong các điều khiển SysListView32. (#8268)
* Hộp thoại cài đặt không còn hiển thị "thông tin" cho mức độ log hiện tại khi ở chế độ bảo mật. (#10209)
+- Trong trình đơn Start (Start menu) cho Windows 10 Anniversary Update trở lên, NVDA sẽ thông báo các chi tiết của kết quả tìm kiếm. (#10232)
* Trong chế độ duyệt, nếu di chuyển con trỏ hay dùng lệnh di chuyển nhanh làm thay đổi tài liệu, NVDA không còn đọc sai nội dung trong vài trường hợp. (#8831, #10343)
* Tên của vài  dấu đầu dòng (bullet) trong Microsoft Word đã được sửa lại. (#10399)
* Trong Windows 10 May 2019 Update trở lên, NVDA sẽ một lần nữa đọc biểu tượng cảm xúc được chọn đầu tiên hay thành phần trong bộ nhớ tạm khi mở bản biểu tượng cảm xúc hay lịch sử bộ nhớ tạm tương ứng. (#9204)
* Trong Poedit,  một lần nữa, lại có thể xem các bản dịch những ngôn ngữ dạng từ phải sang trái. (#9931)
* ứng dụng Settings (cài đặt) trong Windows 10 April 2018 Update trở lên, NVDA sẽ không còn đọc thông tin thanh tiến độ cho các thanh tùy chỉnh âm lượng được tìm thấy trong trang System/Sound. (#10284)
* Các biểu thức phổ thông không hợp lệ trong từ điển phát âm không còn phá hỏng hoàn toàn cho bộ đọc trong NVDA. (#10334)
* Khi đọc các dấu đầu dòng trong Microsoft Word với UIA được bật, các dấu đầu dòng của thành phần danh sách kế  không còn đọc một cách bất hợp lý. (#9613)
* Sửa vài lỗi hiếm gặp khi phiên dịch chữ nổi với liblouis. (#9982)
* Các ứng dụng Java được gọi chạy trước NVDA giờ đã tiếp cận được mà không cần khởi động lại ứng dụng Java. (#10296)
* Trong Mozilla Firefox, khi thành phần có focus được đánh dấu là current (aria-current), thay đổi này không còn bị đọc lại nhiều lần. (#8960)
* Giờ đây, NVDA sẽ xem một  vài kí tự unicode phức hợp nhất định như e-acute (é) là một kí tự đơn khi duy chuyển qua văn bản. (#10550)
* Đã hỗ trợ cho Spring Tool Suite phiên bản 4. (#10001)
* Không nói tên hai lần khi các đích đến liên quan của aria-labelledby là một thành phần bên trong. (#10552)
* Trên Windows 10 phiên bản 1607 trở lên, các kí tự được nhập từ bàn phím chữ nổi đã được đọc trong nhiều tình huống. (#10569)
* Khi thay đổi đầu ra thiết bị âm thanh, các âm thanh được phát bởi NVDA giờ đây sẽ phát qua thiết bị mới được chọn. (#2167)
* Trong Mozilla Firefox, việc di chuyển focus ở chế độ duyệt đã nhanh hơn. Điều này làm cho việc di chuyển con trỏ ở chế độ duyệt phản hồi nhanh hơn trong nhiều trường hợp. (#10584)

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2019.2.1

Đây là bản phát hành phụ nhằm sửa vài sự cố tồn tại trong 2019.2. Các lỗi được sửa bao gồm:

* Phát hiện vài sự cố với Gmail được tìm thấy trong cả Firefox và Chrome khi tương tác với các trình đơn popup cụ thể như khi tạo các bộ lọc hay thay đổi một số tiết lập nhất định của Gmail. (#10175, #9402, #8924)
* Trong Windows 7, NVDA không còn làm cho Windows Explorer bị sự cố khi chuộc được sử dụng trong start menu. (#9435) 
* Windows Explorer trên Windows 7 không còn gặp sự cố khi truy cập các trường chỉnh sửa siêu dữ liệu. (#5337) 
* NVDA không còn bị đóng băng khi tương tác với hình ảnh với base64 URI trong Mozilla Firefox hoặc Google Chrome. (#10227)

## 2019.2

Các cải tiến của bản phát hành này bao gồm tự nhận các màn hình chữ nổi của Freedom Scientific, một thiết lập thử nghiệm trong bảng cài đặt nâng cao để dừng việc tự di chuyển focus trong chế độ duyệt (có thể cải thiện tốc độ vận hành), tùy chọn tăng tốc độ đọc cho bộ đọc Windows OneCore nhằm đọc bằng tốc độ rất nhanh, và sửa nhiều lỗi khác.

### Các tính năng mới

* Hỗ trợ của NVDA cho Miranda NG hoạt động được với các phiên bản mới hơn của chương trình. (#9053) 
* Giờ bạn có thể mặc định tắt chế độ duyệt bằng cách vô hiệu hóa tùy chọn  mới có tên "Bật chế độ duyệt khi tải trang" trong cài đặt chế độ duyệt của NVDA. (#8716) 
 * Lưu ý rằng khi tùy chọn này bị vô hiệu, bạn vẫn có thể bật chế độ duyệt thủ công bằng cách bấm NVDA+khoảng trắng.
* Giờ bạn có thể lọc các kí hiệu trong hộp thoại phát âm kí hiệu/dấu câu, tương tự như cách mà bộ lọc hoạt động trong các hộp thoại danh sách các thành phần và quản lý thao tác. (#5761)
* Đã thêm một lệnh để thay đổi đơn vị văn bản của chuột (đơn vị văn bản sẽ được đọc khi di chuyển chuột), nó chưa được  gán thao tác mặc định. (#9056)
* Bộ đọc windows OneCore giờ đây có tùy chọn  tăng tốc độ đọc, cho phép tăng tốc độ nhanh một cách đáng kể. (#7498)
* Tùy chọn tăng tốc độ đọc giờ đây có thể cấu hình từ thiết lập nhanh cho các bộ đọc được hỗ trợ. (hiện tại là các bộ đọc eSpeak-NG và Windows OneCore). (#8934)
* Giờ đây, đã có thể kích hoạt thủ công các hồ sơ cấu hình bằng thao tác. (#4209)
 * Thao tác phải được cấu hình trong hộp thoại "Quản lý thao tác".
* Trong Eclipse, đã thêm hỗ trợ cho tính năng tự hoàn tất trong trình biên tập mã nguồn (code editor). (#5667)
 * Thêm nữa, có thể đọc các thông tin của Javadoc từ trình biên tập  khi nó xuất hiện bằng cách bấm NVDA+d.
* Thêm tùy chọn thử nghiệm trong bảng thiết lập nâng cao cho phép bạn tắt con trỏ  hệ thống tự đi theo con trỏ duyệt (Tự đưa con trỏ hệ thống đến các thành phần có thể có focus). (#2039) dù việc tắt nó trên tất cả các trang web có thể không khả thi, điều này cũng có thể khắc phục: 
 * Hiệu ứng Rubber band: NVDA thỉnh thoảng hoàn tác phím tắt sau cùng của chế độ duyệt bằng cách đi đến vị trí trước.
 * Các ô nhập liệu chiếm quyền con trỏ hệ thống khi bấm mũi tên xuống qua chúng trên các trang web.
 * Các phím tắt trong chế độ duyệt phản hồi chậm.
* Với các trình điều khiển màn hình nổi được hỗ trợ, các thiết lập trình điều khiển giờ đây có thể thay đổi từ phân loại chữ nổi trong hộp thoại cấu hình NVDA. (#7452) 
* Các màn hình chữ nổi của Freedom Scientific giờ đã được hỗ trợ bởi tính năng tự nhận màn hình nổi. (#7727)
* Thêm vào một lệnh để hiển thị nội dung thay thế cho kí hiệu dưới con trỏ duyệt. (#9286)
* Thêm một tùy chọn thử nghiệm vào bản cài đặt nâng cao, cho phép bạn dùng thử tính năng mới, đang được thực hiện để hỗ trợ cho Windows Console với NVDA, sử dụng Microsoft UI Automation API. (#9614)
* Trong Python Console, phần nhập liệu giờ đã hỗ trợ dán nhiều dòng từ bộ nhớ tạm. (#9776)

### Các thay đổi

* Âm lượng bộ đọc giờ đây tăng và giảm 5 thay vì 10 khi dùng thiết lập tham số nhanh. (#6754)
* Nội dung trong trình quản lý add-on đã được làm rõ hơn khi  NVDA được gọi chạy với tùy chọn --disable-addons. (#9473)
* Đã cập nhật dữ liệu chú thích biểu tượng cảm xúc Unicode Common Locale Data Repository  lên phiên bản 35.0. (#9445)
* Giao diện tiếng Anh: phím nóng cho bộ lọc danh sách các thành phần trong chế độ duyệt đã đổi thành alt+y. (#8728)
* Khi một màn hình chữ nổi dạng tự dò tìm được kết nối qua Bluetooth, NVDA sẽ tiếp tục tìm kiếm các màn hình USB được hỗ trợ bởi cùng trình điều khiển và chuyển sang kết nối USB nếu có. (#8853)
* Đã cập nhật eSpeak-NG lên commit 67324cc.
* Đã cập nhật thư viện phiên dịch chữ nổi liblouis lên phiên bản 3.10.0. (#9439, #9678)
* NVDA giờ đây sẽ đọc từ 'đã chọn' sau khi đọc hết nội dung mà người dùng đã chọn.(#9028, #9909)
* Trong Microsoft Visual Studio Code, NVDA mặc định bật  chế độ focus. (#9828)

### Sửa lỗi

* NVDA không còn bị sự cố khi có một thư mục add-on rỗng. (#7686)
* Các dấu LTR và RTL không còn bị đọc lên trong chữ nổi hay đọc kí tự khi truy cập cửa sổ thuộc tính. (#8361)
* Khi đi đến các trường biểu mẫu với điều hướng nhanh của chế độ duyệt, toàn bộ trường biểu mẫu sẽ được đọc lên, thay vì chỉ đọc dòng đầu tiên. (#9388)
* NVDA sẽ không còn trở nên im lặng sau khi thoát khỏi ứng dụng Windows 10 Mail. (#9341)
* NVDA không còn bị lỗi không khởi động được khi cài đặt vùng ngôn ngữ của người dùng được thiết lập là một ngôn ngữ mà NVDA không xác định, tiếng Anh Hà Lan chẳng hạn. (#8726)
* Khi chế độ duyệt được bật trong Microsoft Excel và  bạn chuyển đến một trình duyệt trong chế độ focus hay ngược lại, trạng thái của chế độ duyệt giờ đây được thông báo một cách hợp lý. (#8846)
* NVDA giờ đây đã đọc đúng dòng tại vị trí con trỏ chuột trong Notepad++ và các trình soạn thảo trên nền tảng Scintilla khác. (#5450)
* Trong Google Docs (và các trình soạn thảo trên nền tảng web khác), không còn tình trạng chữ nổi thỉnh thoảng hiển thị "lst end" trước con trỏ giữa một mục trong danh sách. (#9477)
* Trong Windows 10 May 2019 Update, NVDA không còn đọc quá nhiều thông báo âm lượng nếu thay đổi âm lượng bằng các nút bấm vật lý trong khi  File Explorer có focus. (#9466)
* Việc gọi hộp thoại phát âm kí hiệu / dấu câu giờ đây đã nhanh nhẹn hơn khi từ điển phát âm chứa trên 1000 mục. (#8790)
* Trong các điều khiển Scintilla  như Notepad++, NVDA có thể đọc chính xác một dòng khi tính năng wordwrap được bật. (#9424)
* Trong Microsoft Excel, vị trí của một ô được thông báo sau khi nó thay đổi do thao tác shift+enter hoặc shift+Enter bàn phím số. (#9499)
* Trong Visual Studio 2017 trở lên, trong cửa sổ Objects Explorer, thành phần được chọn trong objects tree hay members tree  với các phân loại giờ đây đã được đọc chính xác. (#9311)
* Các add-on có tên chỉ khác nhau ở chữ hoa / thường không còn bị xem là các add-on riêng biệt. (#9334)
* Với các giọng Windows OneCore, thiết lập tốc độ đọc trong NVDA không còn chịu ảnh hưởng từ thiết lập tốc độ đọc trong Speech Settings của Windows 10 . (#7498)
* Giờ đây, có thể mở log bằng NVDA+F1 khi không có thông tin cho nhà phát triển ở đối tượng điều hướng hiện tại. (#8613)
* Lại có thể dùng được các lệnh điều hướng trong bảng của NVDA trong Google Docs, trong Firefox và Chrome. (#9494)
* Các phím bumper giờ đây đã hoạt động chính xác trên các màn hình chữ nổi của Freedom Scientific. (#8849)
* Khi đọc kí tự đầu tiên của một tài liệu trong Notepad++ 7.7 X64, NVDA không còn bị đóng băng trong tối đa 10 giây. (#9609)
* HTCom giờ đây có thể sử dụng với một màn hình nổi Handy Tech kết hợp với NVDA. (#9691)
* Trong Mozilla Firefox, các cập nhật đến live region không còn được đọc khi nó ở trong thẻ chạy ngầm. (#1318)
* Hộp thoại tìm kiếm trong chế độ duyệt của NVDA không còn tình trạng không hoạt động khi hộp thoại giới thiệu NVDA đang được mở. (#8566)

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2019.1.1

Bản phát hành này sửa các lỗi sau:

* NVDA không còn làm cho Excel 2007 bị  sự cố hoặc không đọc khi một ô có chứa công thức. (#9431)
* Google Chrome không còn bị sự cố khi tương tác với một số hộp danh sách nhất định. (#9364)
* Đã sửa một lỗi làm quá trình sao chép cấu hình người dùng sang hồ sơ cấu hình hệ thống bị chặn. (#9448)
* Trong Microsoft Excel, NVDA lại dùng thông điệp đã bản địa hóa khi thông báo vị trí các ô đã được trộn. (#9471)

## 2019.1

Các cải tiến của bản phát hành này bao gồm cải thiện khả năng vận hành với Microsoft Word và Excel, cải thiện về độ ổn định và bảo mật như hỗ trợ thông tin về phiên bản NVDA tương thích với các add-on, và sửa nhiều lỗi khác.

Xin lưu ý rằng từ bản phát hành NVDA này, Module ứng dụng, Plugins toàn cục, các trình điều khiển của màn hình nổi và bộ đọc sẽ không còn được gọi tự động từ thư mục cấu hình người dùng NVDA của bạn. 
Thay vào đó, chúng phải được cài đặt như một gói add-on NVDA. Những ai đang phát triển add-on, có thể lưu mã nguồn để chạy thử vào thư mục mới tên gọi scratchpad trong thư mục cấu hình người dùng NVDA,  nếu bật tùy chọn gọi mã nguồn từ thư mục scratchpad trong phân loại cài đặt mới tên gọi nâng cao của NVDA.
Những thay đổi này là cần thiết nhằm đảm bảo sự tương thích của mã nguồn, để NVDA không bị lỗi khi mã nguồn không tương thích với các bản phát hành mới hơn.
Xin xem các thay đổi  dưới đây để biết thêm chi tiết về điều này và các add-on bây giờ tốt hơn ra sao.

### Tính năng mới

* Các bản chữ nổi mới: Nam Phi, chữ nổi máy tính 8 chấm Ả Rập, Ả rập cấp 2, Tây ban nha cấp 2. (#4435), #9186)
* Thêm một tùy chọn vào cài đặt chuột của NVDA để quản lý các tình huống mà chuột được điều khiển bởi một ứng dụng khác. (#8452) 
 * Điều này sẽ cho phép NVDA theo dõi chuột khi hệ thống được điều khiển từ xa bằng TeamViewer hay các phần mềm điều khiển từ xa khác.
* Đã thêm tham số `--enable-start-on-logon` vào tham số dòng lệnh nhằm cho phép cài NVDA ở chế độ silent  cho NVDA chạy ở màn hình đăng nhập hay không. Chỉ dịnh true để cho phép chạy ở màn hình đăng nhập hoặc false để không cho phép. Nếu đối số --enable-start-on-logon không được chỉ định thì NVDA mặc định sẽ chạy ở màn hình đăng nhập, ngoại trừ nó đã được cấu hình bởi một phiên bản trước đó là không chạy. (#8574)
* Có thể tắt tính năng log của NVDA bằng cách thiết lập mức độ log là "tắt" trong bản cài đặt chung. (#8516)
* Các công thức của các bảng tính trình bày trong LibreOffice và Apache OpenOffice giờ đây đã được đọc. (#860)
* Trong Mozilla Firefox và Google Chrome, chế độ duyệt  giờ đây đã đọc thành phần được chọn trong các hộp danh sách và cây thư mục.
 * Tính năng này hoạt động trong Firefox 66 trở lên.
 * không hoạt động trong một số hộp danh sách nhất định (HTML select controls) trong Chrome.
* Sớm hỗ trợ cho các ứng dụng như Mozilla Firefox trên các máy vi tính với các bộ vi xử lý ARM64 (ví dụ: Qualcomm Snapdragon). (#9216)
* Một phân loại cài đặt nâng cao đã được thêm vào hộp thoại cấu hình của NVDA, bao gồm một tùy chọn để dùng thử tính năng mới của NVDA hỗ trợ cho Microsoft Word thông qua Microsoft UI Automation API. (#9200)
* Đã hỗ trợ dạng xem đồ họa trong Disk Management của Windows. (#1486)
* Đã thêm hỗ trợ cho Handy Tech Connect Braille và Basic Braille 84. (#9249)

### Các thay đổi

* Cập nhật thư viện phiên dịch chữ nổi liblouis lên phiên bản 3.8.0. (#9013)
* Tác giả của add-on giờ đây có thể yêu cầu một phiên bản NVDA tối thiểu cho các add-on của mình. NVDA sẽ từ chối cài đặt và gọi một add-on yêu cầu phiên bản tối thiểu cao hơn phiên bản NVDA hiện tại. (#6275)
* Các tác giả của add-on giờ đây có thể chỉ định phiên bản NVDA cuối cùng mà add-on đã được thử nghiệm. Nếu một add-on chỉ được thử nghiệm trên một phiên bản thấp hơn phiên bản NVDA hiện tại, NVDA sẽ từ chối cài hay gọi add-on. (#6275)
* Phiên bản NVDA này sẽ cho phép cài và gọi các add-on chưa có thông tin về phiên bản tối thiểu và bản thử nghiệm cuối cùng của NVDA, nhưng khi nâng cấp lên các phiên bản NVDA trong tương lai (ví dụ: 2019.2) có thể khiến các add-on cũ bị vô hiệu hóa.
* Lệnh di chuyển chuột đến đối tượng điều hướng giờ đây đã có trong Microsoft Word cũng như các điều khiển UIA, cụ thể là Microsoft Edge. (#7916, #8371)
* Việc thông báo văn bản tại vị trí chuột đã được cải thiện trong Microsoft Edge và các ứng dụng UIA khác. (#8370)
* Khi NVDA được khởi động với tham số dòng lệnh `--portable-path`, đường dẫn đã được cung cấp sẽ được điền tự động khi tạo bản NVDA chạy trực tiếp bằng thực đơn của NVDA. (#8623)
* Đã cập nhật đường dẫn đến bản chữ nổi  tiếng Na Uy  để phản ánh đúng tiêu chuẩn từ năm 2015. (#9170)
* Khi duyệt theo đoạn (control+các phím mũi tên) hay theo ô trong bảng (control+alt+các phím mũi tên), các lỗi chính tả đang tồn tại sẽ không còn được đọc lên nữa, ngay cả khi NVDA được cấu hình để tự đọc chúng. Điều này là do số lượng các đoạn và ô trong bảng có thể rất lớn, việc phát hiện các lỗi chính tả trong vài ứng dụng có thể mất rất nhiều thời gian. (#9217)
* NVDA không còn tự gọi các Module ứng dụng, Plugins toàn cục, các trình điều khiển màn hình chữ nổi và bộ đọc đã tùy  chỉnh từ thư mục cấu hình người dùng NVDA.  Thay vào đó, những mã nguồn này nên được đóng gói như một add-on với thông tin phiên bản chính xác, đảm bảo rằng các đoạn mã không tương thích sẽ không chạy trên phiên bản NVDA hiện tại. (#9238)
 * Với những nhà phát triển muốn thử nghiệm các đoạn mã đang được phát triển,  hãy bật  tùy chọn developer scratchpad directory của NVDA trong phân loại nâng cao trong phần cài đặt NVDA, và lưu mã nguồn của bạn trong thư mục 'scratchpad'  được tìm thấy trong thư mục cấu hình người dùng của NVDA khi tùy chọn này được bật.

### Sửa lỗi

* Khi dùng bộ đọc OneCore trên Windows 10 April 2018 Update trở lên, không còn tình trạng nhiều khoảng lặng bị chèn vào giữa các câu nói. (#8985)
* Khi di chuyển bằng kí tự trong   các điều khiển văn bản ` (như là Notepad) hay trong chế độ duyệt, các kí tự biểu tượng cảm xúc 32 bit  gồm hai điểm mã UTF-16  (như ðŸ¤¦) giờ đây sẽ được đọc đúng cách. (#8782)
* Cải thiện hộp thoại xác nhận khởi động lại sau khi thay đổi ngôn ngữ giao diện người dùng của NVDA. Nội dung và nhãn của các nút giờ đây sẽ rõ ràng và dễ hiểu hơn. (#6416)
* Nếu không gọi được một bộ đọc nào đó của bên thứ ba, NVDA sẽ gọi trở lại bộ đọc Windows OneCore trên Windows 10, thay vì là espeak. (#9025)
* Gỡ bỏ mục "Hộp thoại chào mừng" trong thực đơn của NVDA khi ở  trong các màn hình bảo vệ. (#8520)
* Khi chạm hay dùng di chuyển nhanh trong chế độ duyệt, các ghi chú trên tab panels giờ đây đã được đọc nhất quán hơn. (#709)
* NVDA giờ đây sẽ thông báo sự thay đổi lựa chọn cho một số bộ chọn giờ nhất định như trong ứng dụng Alarms and Clock trên Windows 10. (#5231)
* Trong Action Center của Windows 10, NVDA sẽ thông báo các thông điệp trạng thái  khi bật / tắt các hành động nhanh  như là độ sáng và hỗ trợ tập trung. (#8954)
* Trong action Center của Windows 10 October 2018 Update trở về trước, NVDA sẽ nhận dạng điều khiển chỉnh độ sáng là một nút bấm thay vì là một nút chuyện. (#8845)
* NVDA sẽ lại theo dõi  con trỏ và thông báo các kí tự đã xóa trong hộp thoại Go To và ô find edit của Microsoft Excel. (#9042)
* Sửa một lỗi hiếm gặp làm cho bị treo ở chế độ duyệt trong Firefox. (#9152)
* NVDA không còn bị lỗi khi thông báo focus cho vài điều khiển trong Microsoft Office 2016 ribbon khi bị thu gọn.
* NVDA không còn bị lỗi không đọc các gợi ý liên lạc khi nhập các địa chỉ cho các thư mới trong Outlook 2016. (#8502)
* Vài phím đưa con trỏ cuối  trên các màn hình nổi 80 ô eurobraille  không còn đưa con trỏ đến ngay hoặc sau vị trí là nơi bắt đầu của một dòng chữ nổi. (#9160)
* Sửa lỗi khi duyệt trong bảng ở chế độ xem threaded trong Mozilla Thunderbird. (#8396)
* Trong Mozilla Firefox và Google Chrome, chuyển sang chế độ focus giờ đây đã hoạt động chính xác với một số hộp danh sách và  cây thư mục nhất định (khi mà hộp danh sách và cây thư mục không tự nó có focus nhưng các thành phần của chúng thì có). (#3573, #9157)
* Chế độ duyệt giờ đã mặc định được bật một cách chính xác khi đọc thư trong  Outlook 2016/365 nếu dùng hỗ trợ thử nghiệm UI Automation của NVDA cho các tài liệu Word. (#9188)
* NVDA giờ đây ít rơi vào tình trạng giống bị đóng băng theo cách  mà đó chỉ là cách duy nhất để thoát khỏi việc đăng xuất khỏi Windows. (#6291)
* Trong Windows 10 October 2018 Update trở lên, khi mở lịch sử bộ nhớ tạm đám mây mà bộ nhớ không có gì, NVDA sẽ thông báo trạng thái bộ nhớ tạm. (#9112)
* Trong Windows 10 October 2018 Update trở lên, khi tìm các biểu tượng cảm xúc trong bảng biểu tượng cảm xúc, NVDA sẽ thông báo các kết quả tìm kiếm hàng đầu. (#9112)
* NVDA không còn bị đóng băng trong cửa sổ chính của Oracle VirtualBox 5.2 trở lên. (#9202)
* Phản hồi trong Microsoft Word khi duyệt theo dòng, đoạn hay theo ô trong bảng có thể được cải thiện đáng kể trong một số tài liệu. Một lời nhắc rằng để làm việc một cách tốt nhất, hãy thiết lập Microsoft Word ở dạng xem Draft với alt+w,e sau khi mở một tài liệu. (#9217) 
* Trong Mozilla Firefox và Google Chrome, các thông báo rỗng không còn được đọc nữa. (#5657)
* Cải thiện hiệu năng vận hành đáng kể khi duyệt qua các ô trong Microsoft Excel, cụ thể là khi một bảng tính có chứa các chú thích hay các hộp xổ xác nhận. (#7348)
* Không cần phải tắt in-cell editing trong Options của Microsoft Excel để tiếp cận điều khiển nhập liệu của ô với NVDA trong Excel 2016/365. (#8146).
* Sửa lỗi thỉnh thoảng Firefox bị đóng băng khi di chuyển nhanh qua các cột mốc, mà lại đang dùng Enhanced Aria add-on. (#8980)

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2018.4.1

 Bản phát hành này sửa lỗi làm cho NVDA bị treo lúc khởi động, nếu cài đặt ngôn ngữ giao diện người dùng là tiếng Aragon. (#9089)

## 2018.4

Các cải tiến của bản phát hành này bao gồm cải thiện khả năng vận hành trong các phiên bản gần đây của Mozilla Firefox, đọc biểu tượng cảm xúc với tất cả các bộ đọc, thông báo trạng thái đã trả lời hay chuyển tiếp trong Outlook, thông báo khoảng cách của con trỏ đến lề của một trang trong Microsoft Word và sửa nhiều lỗi.

### Tính năng mới

* Các bản chữ nổi mới: Tiếng Trung Quốc (Đài Loan, Quan Thoại) cấp 1 và cấp 2. (#5553)
* Trạng thái trả lời (Replied) / chuyển tiếp (Forwarded) đã được thông báo trên các thư trong danh sách thư của Microsoft Outlook. (#6911)
* NVDA giờ đây đã đọc được mô tả cho các biểu tượng cảm xúc và cả những kí tự là một bộ phận của kho dữ liệu Unicode Common Locale Data Repository. (#6523)
* Trong Microsoft Word, có thể đọc thông báo khoảng cách con trỏ từ lề trên và lề trái của trang bằng cách bấm NVDA+Delete bàn phím số. (#1939)
* Trong Google Sheets với chế độ chữ nổi được bật, NVDA không còn thông báo 'đã chọn' ở mọi ô khi di chuyển con trỏ giữa các ô. (#8879)
* Đã hỗ trợ cho Foxit Reader và Foxit Phantom PDF (#8944)
* Đã hỗ trợ cho công cụ cơ sở dữ liệu tổng hợp DBeaver. (#8905)

### Các thay đổi

* Đổi tên tùy chọn "Đọc các thông báo trợ giúp" trong hộp thoại trình bày đối tượng thành "Đọc các thông báo" để bao gồm việc đọc các thông báo toast trong Windows 8 và cao hơn. (#5789)
* Trong cài đặt bàn phím của NVDA, các hộp kiểm để bật / tắt các phím bổ trợ NVDA giờ đây hiển thị thành một danh sách thay vì là các hộp kiểm riêng lẻ.
* NVDA sẽ không còn đọc các thông tin thừa  khi xem đồng hồ từ khay hệ thống trên vài phiên bản Windows. (#4364)
* Cập nhật thư viện phiên dịch chữ nổi liblouis lên phiên bản 3.7.0. (#8697)
* Cập nhật eSpeak-NG lên bản commit 919f3240cbb.

### Sửa lỗi

* Trong Outlook 2016/365, trạng thái phân loại và gắn cờ của các thư đã được đọc. (#8603)
* Khi ngôn ngữ được chọn cho NVDA là Kirgyz, Mongolian hay Macedonian chẳng hạn, không còn tình trạng hiển thị hộp thoại lúc khởi động cảnh báo ngôn ngữ không được hệ thống hỗ trợ. (#8064)
* Việc di chuyển chuột đến đối tượng điều hướng giờ đây sẽ di chuyển chuột chính xác hơn đến vị trí chế độ duyệt trong Mozilla Firefox, Google Chrome và Acrobat Reader DC. (#6460)
* Việc tương tác với các hộp xổ trên web trong Firefox, Chrome và Internet Explorer đã được cải thiện. (#8664)
+- Nếu đang chạy trên một phiên bản Windows XP hay Vista tiếng Nhật , NVDA giờ đây đã hiển thị thông điệp yêu cầu phiên bản hệ điều hành như mong muốn. (#8771)
* Cải thiện khả năng vận hành khi điều hướng trên các trang lớn với nhiều nội dung động trong Mozilla Firefox. (#8678)
* Không còn tình trạng hiện thuộc tính phông trong chữ nổi nếu đã được tắt trong cài đặt định dạng tài liệu. (#7615)
* NVDA không còn bị lỗi khi theo dõi con trỏ trong File Explorer và các ứng dụng khác đang dùng UI Automation khi một ứng dụng khác đang hoạt động (xử lý tập tin âm thanh hàng loạt chẳng hạn). (#7345)
* Trong các trình đơn ARIA trên web, phím Escape giờ đây sẽ được chuyển đến trình đơn và không còn tình trạng tắt chế độ focus vô điều kiện. (#3215)
* Trong giao diện web mới của Gmail, khi dùng các phím di chuyển nhanh trong các thư khi đọc chúng, toàn bộ phần nội dung thư không còn bị đọc lên sau thành phần mà bạn mới điều hướng đến. (#8887)
* Sau khi cập nhật NVDA, các trình duyệt như Firefox và google Chrome sẽ không còn bị sự cố, và chế độ duyệt sẽ tiếp tục phản ánh một cách chính xác bất kì tài liệu nào đang được tải. (#7641) 
* NVDA không còn đọc cụm từ có thể kích nhiều lần trên một dòng khi điều hướng  qua các nội dung có thể kích trong chế độ duyệt. (#7430)
* Các thao tác trên các màn hình nổi baum Vario 40 không còn bị lỗi không thực hiện được. (#8894)
* Trong Google Slides với Mozilla Firefox, NVDA không còn thông báo văn bản đã chọn trên mỗi điều khiển với focus. (#8964)

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2018.3.2

Đây là bản phát hành phụ nhằm giải quyết sự cố trong  Google Chrome khi điều hướng qua các tweett trên trang [www.twitter.com](http://www.twitter.com). (#8777)

## 2018.3.1

Đây là bản phát hành phụ nhằm sửa một lỗi nghiêm trọng của NVDA làm cho các phiên bản 32 bit của Mozilla Firefox bị sự cố. (#8759)

## 2018.3

Các cải tiến của bản phát hành này bao gồm khả năng tự nhận biết nhiều màn hình nổi, hỗ trợ các tính năng mới của Windows 10, bao gồm bảng nhập biểu tượng cảm xúc  (Emoji input panel) và sửa nhiều lỗi.

### Các tính năng mới

* NVDA sẽ thông báo các lỗi ngữ pháp khi tiếp xúc một cách thích hợp trên các trang web trong Mozilla Firefox và Google Chrome. (#8280)
* Nội dung đã đánh dấu là đang được thêm vào hay xóa đi trong các trang web đã được thông báo trong Google Chrome. (#8558)
* Đã hỗ trợ nút cuộn của máy BrailleNote QT và Apex BT's khi sử dụng như một màn hình chữ nổi với NVDA. (#5992, #5993)
* Đã thêm kịch bản thông báo thời gian còn lại và tổng thời gian của bài hát hiện tại trong Foobar2000. (#6596)
* Kí hiệu command trên Mac (⌘) giờ đây đã được thông báo khi đọc văn bản với bất kì bộ đọc nào. (#8366)
* vai trò tùy chỉnh thông qua thuộc tính aria-roledescription hiện đã hỗ trợ trong tất cả các trình duyệt. (#8448)
* Các bảng chữ nổi mới: Czech 8 chấm, Central Kurdish, Esperanto, Hungarian, Thụy Điẻn máy tính 8 chấm. (#8226, #8437)
* Đã hỗ trợ tự động ngầm nhận biết các màn hình chữ nổi. (#1271)
 * Các màn hình ALVA, Baum/HumanWare/APH/Orbit, Eurobraille, Handy Tech, Hims, SuperBraille, HumanWare BrailleNote và Brailliant BI/B hiện đã được hỗ trợ.
 * Bạn có thể bật tính năng này bằng cách chọn tùy chọn tự động từ danh sách màn hình nổi trong hộp thoại chọn màn hình nổi của NVDA.
 * Vui lòng xem tài liệu để biết thêm chi tiết.
* Đã hỗ trợ cho nhiều tính năng nhập liệu mới được giới thiệu trong các bản phát hành gần đây của Windows 10. Các hỗ trợ bao gồm emoji panel - bản biểu tượng cảm xúc (Fall Creators Update), dictation (Fall Creators Update), hardware keyboard input suggestions (April 2018 Update), và cloud clipboard paste (October 2018 Update). (#7273)
* Nội dung được đánh dấu là đoạn trích dẫn bằng ARIA (role blockquote) giờ đây đã được hỗ trợ trong Mozilla Firefox 63. (#8577)

### Các thay đổi

* Danh sách các ngôn ngữ hiện hành trong hộp thoại thiết lập chung giờ đây được sắp xếp theo tên thay vì theo mã ISO 639. (#7284)
* Thêm thao tác mặc định cho alt shift tab và windows tab với tất cả màn hình chữ nổi được hỗ trợ của Freedom Scientific. (#7387)
* Với các màn hình ALVA BC680 và cổng chuyển đổi giao thức, giờ đây đã gán được các chức năng khác nhau cho smart pad trái và phải, các phím thumb và etouch. (#8230)
* Với các màn hình ALVA BC6, tổ hợp phím sp2+sp3 giờ đây sẽ thông báo ngày giờ hiện tại, trong khi sp1+sp2 là phím Windows. (#8230)
* Giờ đây, người dùng được hỏi một lần khi khởi động NVDA về việc gửi thông tin thống kê sử dụng cho NV Access khi kiểm tra cập nhật NVDA. (#8217)
* Khi kiểm tra cập nhật, nếu người dùng đồng ý gửi thông tin thống kê sử dụng cho NV Access, NVDA sẽ gửi tên driver của bộ đọc và màn hình chữ nổi hiện tại , nhằm hỗ trợ tốt hơn trong việc ưu tiên cho các cập nhật sắp tới của những driver này. (#8217)
* Đã cập nhật thư viện phiên dịch chữ nổi  liblouis lên phiên bản 3.6.0. (#8365)
* Đã cập nhật đường dẫn chính xác cho bảng chữ nổi tiếng Nga tám chấm. (#8446)
* Đã cập nhật eSpeak-ng lên phiên bản 1.49.3dev commit 910f4c2 (#8561)

### Sửa lỗi

* Nhãn tiếp cận cho các điều khiển trong Google Chrome giờ đây đã sẵn sàng hơn khi thông báo trong chế độ duyệt khi chúng không được xuất hiện như nội dung  của chính nó. (#4773)
* Đã hỗ trợ đọc các thông báo trong Zoom. Ví dụ: đọc trạng thái bật / tắt âm thanh và khi có tin nhắn tới. (#7754)
* Chuyển ngữ cảnh trình bày của chữ nổi khi ở trong chế độ duyệt không còn làm đầu ra chữ nổi bị dừng, không đi theo con trỏ trong chế độ duyệt. (#7741)
* Các màn hình nổi ALVA BC680 không còn tình trạng liên tục không khởi động được. (#8106)
* Mặc định, các màn hình ALVA BC6 sẽ không còn gọi các phím mô phỏng hệ thống khi bấm các tổ hợp phím liên quan đến sp2+sp3 để gọi các chức năng nội bộ. (#8230)
* Bấm sp2 trên một màn hình ALVA BC6 để mô phỏng phím alt giờ đã hoạt động như quảng cáo. (#8360)
* NVDA không còn thông báo thông tin dư thừa cho các  thay đổi kiểu bàn phím. (#7383, #8419)
* Tính năng thông báo chuột giờ đã hoạt động chính xác hơn trong Notepad và các điều khiển nhập văn bản khác khi ở trong một tài liệu có nhiều hơn 65535 kí tự. (#8397)
* NVDA sẽ nhận dạng thêm các hộp thoại trong Windows 10 và các ứng dụng hiện đại khác. (#8405)
* Trên Windows 10 October 2018 Update và Server 2019 trở lên, NVDA không còn tình trạng lỗi không đi theo dấu nháy hệ thống khi một ứng dụng bị đóng băng hoặc bao phủ hệ thống bằng các sự kiện. (#7345, #8535)
* Giờ đây, người dùng  đã được thông báo khi có ý định đọc hay sao chép nội dung rỗng từ thanh trạng thái. (#7789)
* Sửa lỗi trạng thái "chưa chọn" trên các điều khiển không được thông báo bằng bộ đọc nếu nó đã được chọn trước đó. (#6946)
* Trong danh sách ngôn ngữ ở hộp thoại thiết lập chung, tên ngôn ngữ của tiếng Burmese đã hiển thị chính xác trên Windows 7. (#8544)
* Trong Microsoft Edge, NVDA sẽ đọc các thông báo  như trình bày kiểu đọc và tiến trình tải trang. (#8423)
* Khi điều hướng vào một danh sách trên web, NVDA sẽ thông báo nhãn của nó nếu được người thiết kế web cung cấp. (#7652)
* khi gán thủ công một thao tác cho chức năng của một màn hình nổi cụ thể, những thao tác này giờ đây sẽ luôn hiển thị rằng đang được gán cho màn hình đó. Trong khi trước đây, nó hiển thị rằng đã được gán cho màn hình đang được kết nối. (#8108)
* Đã hỗ trợ phiên bản 64-bit của Media Player Classic. (#6066)
* Vài cải tiến cho việc hỗ trợ chữ nổi trong Microsoft Word với UI Automation được bật:
 * Tương tự như các trường nhập liệu nhiều dòng khác, khi đứng ở đầu một tài liệu trong chữ nổi, màn hình giờ đây sẽ cuộn để kí tự đầu tiên của tài liệu sẽ ở trên cùng của màn hình. (#8406)
 * Giảm bớt các chi tiết trình bày trong cả bộ đọc và chữ nổi khi đứng ở một tài liệu Word. (#8407)
 * Cursor routing trong chữ nổi giờ đây đã làm việc chính xác khi ở trong danh sách trong tài liệu Word. (#7971)
 * Các danh sách có / không thứ tự mới được chèn vào trong tài liệu Word đã được thông báo chính xác trong chữ nổi và bộ đọc. (#7970)
* Trong Windows 10 1803 và cao hơn, giờ đây đã có thể cài đặt add-on nếu bật tính năng "Use Unicode UTF-8 for worldwide language support". (#8599)
* NVDA sẽ không còn làm cho iTunes 12.9 hay mới hơn rơi vào tình trạng hoàn toàn không tương tác được. (#8744)

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2018.2.1

Bản phát hành này bao gồm các cập nhật phiên dịch vì xảy ra lỗi từ việc gỡ bỏ một tính năng.

## 2018.2

Một số tính năng nổi bật trong bản phát hành này bao gồm hỗ trợ đọc bảng cho Kindle for PC, hỗ trợ màn hình nổi HumanWare BrailleNote Touch và BI14, cải thiện khả năng làm việc với các bộ đọc OneCore và Sapi5, các cải thiện cho Microsoft Outlook và hơn thế nữa.

### Các tính năng mới

* Các cột và dòng được trộn trong bảng giờ đây đã được thông báo trên cả bộ đọc và màn hình nổi. (#2642)
* Các lệnh điều hướng trong bảng của NVDA giờ đã được hỗ trợ cho Google Docs (khi bật chế độ màn hình nổi. (#7946)
* Có khả năng đọc và điều hướng trong các bảng  trên máy Kindle for PC. (#7977)
* Hỗ trợ màn hình nổi HumanWare BrailleNote touch và Brailliant BI 14 thông qua USB và bluetooth. (#6524)
* Với Windows 10 Fall Creators Update trở lên, NVDA đã có thể đọc thông báo từ các ứng dụng như Calculator và Windows Store. (#7984)
* Các bảng dịch chữ nổi mới: Lithuanian 8 chấm, Ukrainian, Mông cổ cấp 2\. (#7839)
* Đã thêm kịch bản thông báo các thông tin định dạng của văn bản tại vị trí con trỏ trên màn hình nổi. (#7106)
* Khi cập nhật  NVDA, đã có thể tạm hoãn việc cài đặt bản cập nhật để thực hiện ở một thời điểm khác. (#4263) 
* Có thêm các ngôn ngữ mới: Mông cổ, Đức Thụy Sỹ.
* Giờ bạn có thể bật các phím control, shift, alt, windows và NVDA từ bàn phím chữ nổi và kết hợp các phím bổ trợ này với kiểu nhập liệu chữ nổi (ví dụ: control+s). (#7306) 
 * Bạn có thể gán phím để bật / tắt hai phím bổ trợ bằng  các lệnh được tìm thấy trong phần Các phím mô phỏng bàn phím hệ thống  trong hộp thoại Quản lý thao tác.
* Hỗ trợ lại cho màn hình nổi Handy Tech Braillino và Modular (với firmware cũ). (#8016)
* Ngày và giờ cho các thiết bị được hỗ trợ  của Handy Tech (như Active Braille and Active Star) sẽ được đồng bộ bởi  NVDA khi bị ra khỏi đồng bộ quá 5 giây. (#8016)
* Có thể gán thao tác để tạm thời vô hiệu hóa tất cả các tác nhân hồ sơ cấu hình. (#4935)

### Các thay đổi

* Cột trạng thái trong hộp thoại quản lý Add-on đã được thay đổi để xác định Add-on đang bật hay tắt thay vì thông báo đang chạy hay đã tắt. (#7929)
* Đã cập nhật thư viện phiên dịch chữ nổi liblouis lên 3.5.0\. (#7839)
* Bảng chữ nổi Lithuanian đã được đổi tên thành Lithuanian 6 dot (6 chấm) để tránh rắc rối với bảng chữ nổi 8 chấm của ngôn ngữ này. (#7839)
* Bảng chữ nổi tiếng Pháp, Canada cấp 1 và 2 đã được gỡ bỏ. Thay vào đó là bản chữ nổi máy tính tiếng Pháp (unified) 6 chấm và chữ nổi tiếng Pháp cấp 2 sẽ được dùng. (#7839)
* Các nút secondary routing trên màn hình nổi Alva BC6, EuroBraille và Papenmeier giờ đây đã thông báo thông tin định dạng cho văn bản tại ô chữ nổi của nút đó. (#7106)
* Các bảng chữ nổi tắt sẽ tự trả về chữ đủ trong  những trường hợp không ở trong vùng soạn thảo (trường hợp không có con trỏ hay trong chế độ duyệt). (#7306)
* NVDA giờ đây đã ít phát ra tiếng beep trong phần lịch của Outlook. (#7949)
* Tất cả các thiết lập của NVDA giờ đây có thể tìm thấy ở một hộp thoại duy nhất trong trình đơn của NVDA -> Tùy Chọn -> Cấu hình, thay vì phải thiết lập thông qua nhiều hộp thoại. (#577)
* Bộ đọc mặc định khi chạy chương trình trên Windows 10 giờ đây là oneCore thay vì eSpeak. (#8176)

### Sửa lỗi

* NVDA không còn bị lỗi không đọc được tên các điều khiển tại vị trí con trỏ trong màn hình đăng nhập tài khoản Microsoft trong Settings sau khi nhập địa chỉ e-mail. (#7997)
* NVDA không còn bị lỗi không đọc được trang khi trở về trang trước trong Microsoft Edge. (#7997)
* NVDA không còn bị lỗi đọc kí tự cuối cùng ngoài ý muốn khi nhập mã pin ở màn hình đăng nhập của Windows 10 để mở khóa máy tính. (#7908)
* Các nhãn của hộp kiểm và nút radio trong Chrome và Firefox không còn bị đọc hai lần khi duyệt web bằng phím Tab hay các phím điều hướng nhanh ở chế độ duyệt. (#7960)
* aria-current với giá trị false sẽ được thông báo là "false" thay vì là "true". (#7892).
* Không còn lỗi không tải được các giọng đọc của Windows OneCore nếu đã gỡ bỏ các giọng đọc được cấu hình. (#7553)
* Việc thay đổi các giọng đọc trong bộ Windows OneCore giờ đây đã hoạt động nhanh hơn. (#7999)
* Đã sửa lỗi định dạng sai cho đầu ra của vài bảng chữ nổi, bao gồm dấu báo  hoa  trong bảng chữ nổi tắt 8 chấm tiếng Đan Mạch. (#7526, #7693)
* NVDA giờ đây đã có thể thông báo nhiều kiểu đánh dấu danh sách không thứ tự trong Microsoft Word. (#6778)
* Lệnh thông báo định dạng sẽ không di chuyển con trỏ ngoài ý muốn nữa. Vậy nên bấm lệnh này nhiều lần cũng không bị cho ra các kết quả khác nhau. (#7869)
* Đầu vào chữ nổi không còn cho phép bạn dùng chữ nổi tắt trong trường hợp không được hỗ trợ (Ví dụ: các từ đầy đủ sẽ không được gửi ra hệ thống khi ở ngoài nội dung văn bản hay trong chế độ duyệt. (#7306)
* Sửa lỗi kết nối không ổn định cho màn hình nổi Handy Tech Easy Braille và Braille Wave. (#8016)
* Từ Windows 8 trở lên, NVDA sẽ không còn đọc "không xác định" khi mở trình đơn các liên kết nhanh (Windows+X) và chọn các thành phần từ trình đơn này. (#8137)
* Vài thao tác cho các nút trên màn hình nổi của Hims đã hoạt động như được  quảng cáo trong hướng dẫn sử dụng. (#8096)
* NVDA sẽ cố gắng sửa lỗi hệ thống COM registration khiến cho các chương trình như Firefox và Internet Explorer trở nên không tiếp cận  và NVDA thông báo "không xác định". (#2807)
* Làm việc về lỗi trong Task Manager khiến NVDA không cho phép người dùng truy cập nội dung của vài chi tiết về quá trình vận hành. (#8147)
* Các giọng đọc mới chuẩn Sapi5 không còn bị chậm khi kết thúc quá trình đọc, điều đó giúp  cho việc điều hướng với các giọng đọc này trở nên hiệu quả hơn. (#8174)
* NVDA không còn thông báo (dấu LTR và RTL) qua màn hình nổi hay khi đọc kí tự khi truy cập biểu tượng đồng hồ trong các phiên bản Windows gần đây. (#5729)
* Tìm ra các phím cuộn trên màn hình Hims Smart Beetle lại một lần nữa  trở nên tin cậy. (#6086)
* Trong vài điều khiển văn bản, đặc biệt là trong các ứng dụng viết bằng Delphi, các thông tin được cung cấp liên quan đến chỉnh sửa và điều hướng giờ đây đã trở nên đáng tin cậy hơn.. (#636, #8102)
* Trong Windows 10 RS5, NVDA không còn thông báo thêm thông tin dư thừa khi chuyển cửa  sổ bằng alt+tab. (#8258)

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2018.1.1

Đây là bản phát hành đặc biệt  của NVDA, sửa một lỗi trong driver của bộ đọc OneCore, khiến cho nó bị đọc nhanh và cao hơn trong Windows 10 Redstone 4 (1803). (#8082) 

## 2018.1

Một số tính năng nổi bật trong bản phát hành này là hỗ trợ sơ đồ cho Microsoft word và PowerPoint, hỗ trợ màn hình nổi mới là Eurobraille và bộ chuyển giao thức Optelec, hỗ trợ thêm cho màn hình nổi của Hims và Optelec, cải thiện hoạt động với Mozilla Firefox 58 và bản cao hơn, và nhiều tính năng mới khác.

### Tính Năng Mới

* Đã có thể tương tác với các biểu đồ trong Microsoft Word và Microsoft PowerPoint, giống như hỗ trợ hiện tại cho Microsoft Excel. (#7046)
 * Ở chế độ duyệt trong Microsoft Word, chuyển con trỏ đến biểu đồ nhúng và nhấn enter để tương tác. 
 * Khi sửa slide trong Microsoft PowerPoint: tab đến đối tượng biểu đồ, nhấn enter hoặc khoảng trắng để tương tác.
 * Nhấn esc để thoát.
* Ngôn ngữ mới: Kyrgyz.
* Hỗ trợ cho VitalSource Bookshelf. (#7155)
* Hỗ trợ cho bộ chuyển giao thức Optelec, một thiết bị cho phép sử dụng Braille Voyager và Satellite bằng giao thức giao tiếp ALVA BC6. (#6731)
* Có thể nhập liệu chữ nổi với màn hình ALVA 640 Comfort. (#7733) 
 * Chức năng nhập chữ liệu của NVDA đã có thể sử dụng với các màn hình BC6 chạy firmware 3.0.0 và cao hơn.
* Hỗ trợ cơ bản cho Google Sheets ở chế độ chữ nổi. (#7935)
* Hỗ trợ màn hình nổi Eurobraille Esys, Esytime và Iris. (#7488)

### Thay Đổi

* Đã thay thế các driver cho HIMS Braille Sense/Braille EDGE/Smart Beetle và Hims Sync thành một driver. Driver mới sẽ tự động kích hoạt cho người dùng driver syncBraille cũ. (#7459) 
 * Một vài phím như phím cuộn đã được gán lại theo quy tắc của màn hình nổi Hims. Xem tài liệu hướng dẫn để biết thêm chi tiết.
* Khi nhập liệu với bàn phím on-screen qua tương tác cảm ứng, bạn cần phải chạm đôi để kích hoạt phím như với các điều khiển. (#7309)
 * Để sử dụng chế độ nhập liệu cảm ứng như hiện tại với một chạm, hãy bật tùy chọn này trong hộp thoại thiết lập tương tác cảm ứng trong thực đơn tùy chọn.
* Không còn cần thiết chọn chế độ đưa con trỏ nổi theo focus hay con trỏ duyệt, vì mặc định nó sẽ tự động thay động.(#2385) 
 * Lưu ý, tự động chuyển qua chế độ đi theo con trỏ duyệt chỉ khi con trỏ duyệt kích hoạt hoặc dùng lệnh điều hướng đối tượng được thực hiện. Khi cuộn sẽ không tự động chuyển.

### Sửa Lỗi

* Các thông báo có thể duyệt khi nhấn NVDA+f hai lần đã không còn bị lỗi khi cài NVDA dưới đường dẫn có chứa ký tự ngoài mã ascii. (#7474)
* Focus trở về Spotify từ ứng dụng khác. (#7689)
* Ở Windows 10 Fall Creaters Update, NVDA hết bị lỗi cập nhật khi Controlled Folder Access được bật trong Windows Defender Security Center. (#7696)
* Nhận dạng phím cuộn trên màn hình Hims Smart Beetle isplays đã ổn định. (#6086)
* Cải thiện một phần nhỏ khả năng hoạt động với Firefox 58 trở lên khi tải tài liệu có nội dung lớn. (#7719)
* Trong Microsoft Outlook, không còn gặp lỗi khi đọc email có các bảng. (#6827)
* Các phím tắt màn hình nổi đã có thể mô phỏng với các phím bổ trợ của hệ thống. (#7783)
* Trong n Mozilla Firefox, chế độ duyệt đã hoạt động chính xác hơn khi có cửa sổ pop-up bở các tiện ích mở rộng, ví dụ như LastPass và bitwarden. (#7809)
* NVDA không còn treo mỗi khi thay đổi focus trong trường hợp Firefox hoặc Chrome không phản hồi/bị treo. (#7818)
* Ở các trình twitter như Chicken Nugget, NVDA không còn bỏ qua 20 ký tự cuối trong dãy 255 ký tự. (#7828)
* NVDA đã đọc các ký hiệu đúng với ngôn ngữ khi văn bản được chọn. (#7687)
* Ở những phiên bản gần đây của Office 365, có thể duyệt các biểu đồ với phím mũi tên. (#7046)
* In Ở phần xuất chữ nổi và giọng đọc, control states sẽ thông báo cùng thứ tự. (#7076)
* Trong những ứng dụng như Windows 10 Mail, NVDA đã đọc đúng ký tự được xóa khi nhấn xóa lùi. (#7456)
* Tất cả các phím trên màn hình the Hims Braille Sense Polaris đã hoạt động như mong muốn. (#7865)

### Các thay Đổi cho Nhà Phát Triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2017.4

Những tính năng mới và thay đổi nổi bật trong bản phát hành này bao gồm việc hỗ trợ web như chế duyệt cho các hộp thoại web ở mặc định, cải thiện khả năng thông báo nhãn của các nhóm trường ở chế độ duyệt, hỗ trợ những công nghệ mới trên Windows 10 như Windows Defender Application Guard và Windows 10 trên ARM64, và tự động thông báo hướng màn hình cũng như tình trạng pin.
Lưu ý, từ phiên bản NVDA này trở đi, sẽ không còn hỗ trợ cho Windows XP và Vista. Yêu cầu tối thiểu là từ Windows 7 SP1 trở lên.

### Tính Năng Mới

* Ở chế độ duyệt, đã có thể đi đến/bỏ qua đầu/cuối của các landmark với lệnh chuyển đến cuối hoặc đầu đối tượng chứa (phẩy hoặc shift+phẩy). (#5482)
* Lệnh di chuyển nhanh đến ô soạn thảo và các trường biểu mẫu trong Firefox, Chrome và Internet Explorer đã gồm luôn trường soạn thảo có thuộc tính, ví dụ như contentEdible. (#5534)
* Danh sách các thành phần trong các trình duyệt web đã có thể liệt kê các trường biểu mẫu và nút. (#588)
* Hỗ trợ bước đầu cho Windows 10 trên ARM64. (#7508)
* Bước đầu hỗ trợ đọc và tương tác với nội dung Toán của sách Kindle có định dạng tiếp cận. (#7536)
* Thêm hỗ trợ cho phần mềm đọc sách Azardi. (#5848)
* Đã thông báo thông tin phiên bản của add-on khi được cặp nhật. (#5324)
* Thêm tham số dòng lệnh để tạo bản NVDA chạy trực tiếp. (#6329)
* Hỗ trợ Microsoft Edge chạy với Windows Defender Application Guard trên Windows 10 Fall Creators Update. (#7600)
* Khi chạy trên laptop hay tablet, NVDA sẽ thông báo khi cắm hoặc gỡ dây sạc và khi thiết bị thay đổi hướng màn hình. (#4574, #4612)
* Thêm ngôn ngữ mới: Macedonian.
* Thêm bảng chữ nổi mới: Croatian cấp 1, tiếng Việt cấp 1. (#7518, #7565)
* Hỗ trợ màn hình nổi Actilino của hãng Handy Tech. (#7590)
* Hỗ trợ nhập liệu chữ nổi cho các màn hình nổi của Handy Tech. (#7590)

### Thay Đổi

* Hệ điều hành Windows yêu cầu tối thiểu hiện nay cho NVDA là Windows 7 Service Pack 1, hoặc Windows Server 2008 R2 Service Pack 1. (#7546)
* Nếu không đứng ở ứng dụng web, các hộp thoại web trong Firefox và Chrome sẽ mặc định ở chế độ duyệt. (#4493)
* Ở chế độ duyệt, NVDA không còn thông báo ra khỏi đối tượng chứa như danh sách và bảng biểu. Điều này giúp việc di chuyển ổn định hơn. (#2591)
* NVDA đã thông báo tên các nhóm biểu mẫu khi di chuyển nhanh đến đó trong chế độ duyệt với Firefox và Chrome. (#3321)
* Ở chế độ duyệt, phím tắt di chuyển nhanh đến đối tượng nhúng (o và shift+o) cũng sẽ bao gồm các đối tượng audio, video cũng như những thành phần là hộp thoại và ứng dụng có các vai trò aria. (#7239)
* Đã cập nhật lên bản Espeak-ng 1.49.2, sửa một số vấn đề của bản build trước đó. (#7385, #7583)
* Nếu thực hiện lệnh đọc thanh trạng thái 3 lần sẽ chép nội dung trên thanh lên bộ nhớ tạm. (#1785)
* Khi gán cử chỉ cho màn hình Baum, bạn có thể giới hạn mô đen màn hình nổi được sử dụng, ví dụ như VarioUltra hoặc Pronto). (#7517)
* Đã thay đổi phím tắt chuyển đến ô lọc của danh sách thành phần ở chế độ duyệt. (#7569)
* Lệnh gỡ gán (unbound) đã được thêm cho chế độ duyệt, giúp bật tắt phần tùy chỉnh tạm thời cho bảng biểu trình bày. Có thể tìm thấy trong phân loại chế độ duyệt của cửa sổ quản lý cử chỉ. (#7634)
* Cập nhật thư viện phiên dịch chữ nổi liblouis lên 3.3.0. (#7565)
* Đã đổi phím tắt cho nút radio chọn biểu thức thông thường trong hộp thoại từ điển. (#6782)
* Tập tin từ điển giọng đọc đã được đặt phiên bản và chuyển qua thư mục 'speechDicts/voiceDicts.v1'. (#7592)
* Khi chạy NVDA từ trình khởi động, NVDA sẽ không lưu các thay đổi của tập tin được đánh phiên bản như cấu hình người dùng và từ điển giọng đọc. (#7688)
* Không còn hỗ trợ Braillino, Bookworm và Modular của Handy Tech dùng firmware cũ. Hãy cài driver Universial của Handy Tech và add-on của NVDA để tiếp tục sử dụng. (#7590)

### Sửa Lỗi

* Đã báo chữ nổi cho liên kết trong các ứng dụng như Microsoft Word. (#6780)
* NVDA không còn chậm khi mở nhiều tab với Firefox và Chrome. (#3138)
* Chức năng đưa con trỏ cho màn hình nổi MDV Lilli không còn lỗi đi trước một ô so với ô cần có focus. (#7469)
* Trong tài liệu MSHTML hoặc Internet Explorer, đã hỗ trợ thuộc tính bắt buộc (require) của HTML5 để báo trạng thái của các trường biểu mẫu.  (#7321)
* Màn hình nổi đã cặp nhật khi gõ ký tự Arobic với Wordpad theo lề trái. (#511)
* Những nhãn điều khiển tiếp cận trong Firefox đã đọc ở chế độ duyệt, cho dù nội dung của nó có bị ẩn đi. (#4773)
* Trên windows 10 Creaters Update, NVDA có thể truy xuất Firefox sau khi khởi động lại NVDA. (#7269)
* Khi khởi động lại NVDA mà Firefox đang có focus, nó vẫn sẽ nằm ở chế độ duyệt, cho dù bạn có thể phải nhấn alt+tab đi và trở lại cửa sổ Firefox. (#5758)
* Đã có thể truy cập nội dung toán trên Google Chrome cho dù không cần cài Firefox.  (#7308)
* Hệ điều hành hay những ứng dụng khác chạy ổn định hơn ngay sau khi cài đặt NVDA nhưng trước lúc khởi động lại. Điều này được so với những bản cài trước đây. (#7563)
* Khi sử dụng chức năng nhận dạng nội dung, NVDA sẽ thông báo lỗi nếu đối tượng điều hướng bị mất. (#7567)
* Chức năng cuộn trở lại của màn hình nổi Freedom Scientific đã hoạt động. (#7713)

### Các thay Đổi cho Nhà Phát Triển

* "scons tests" sẽ kiểm tra những chuỗi dịch có chú thích của người dịch không. Bạn có thể chạy độc lập với "scons checkPot". (#7492)
* Có mô đun extensionPoints mới cung cấp framework để bật khả năng mở rộng mã tại điểm cụ thể của mã. Điều này giúp các chương trình khác muốn đăng ký để được thông báo khi có action xuất hiện (extensionPoints.Action), để chỉnh sửa các loại dữ liệu (extensionPoints.Filter) hoặc tham gia quá trình quyết định một việc sẽ được hoàn tất (extensionPoints.Decider). (#3393)
* Đã có thể đăng ký thông báo khi thay đổi hồ sơ cấu hình với config.configProfileSwitched Action. (#3393)
* Các cư chỉ/phím tắt của màn hình nổi đã có thể mô phỏng các phím bổ trợ của hệ thống (như control và alt) mà không cần phải định nghĩa riêng. (#6213) 
 * Ví dụ: nếu trên màn hình nổi bạn có gán một phím với alt và một phím với mũi tên xuống, thì có thể nhấn alt+mũi tên xuống.
* Lớp braille.BrailleDisplayGesture đã có thêm thuộc tính model. Nếu khai báo, khi nhấn sẽ tạo ra thêm phím. Điều này giúp người dùng gán phím tắt cho cụ thể dòng màn hình nổi nào đó. 
 * Xem thêm driver baum để biết thêm tính năng này.
* NVDA hiện nay được biên dịch với Visual Studio 2017 và Windows 10 SDK. (#7568)

## 2017.3

Những chức năng nổi bật trong phiên bản này là cho phép nhập liệu chữ nổi viết tắt, hỗ trợ các giọng OneCore trên Windows 10, chức năng nhận dạng với Windows 10 OCR và rất nhiều những cải thiện quan trọng khác cho màn hình nổi và web.

### Tính Năng Mới

* Thêm một thiết lập chữ nổi mới là "Hiển thị thông điệp không xác định". (#6669)
* Thông báo thư được đánh cờ khi đứng trong danh sách thư của Microsoft Outlook. (#6374)
* Đã thông báo kiểu hình dạng khi chỉnh sửa slide trong Microsoft PowerPoint (ví dụ: hình tam giác, hình tròn, video, mũi tên) thay vì chỉ thông báo là "hình dạng". (#7111)
* Hỗ trợ đọc nội dung toán theo chuẩn MathML trong Google Chrome. (#7184)
* NVDA có thể đọc với các giọng OneCore của Windows 10 (còn được biết là giọng đọc di động). Bạn có thể chọn giọng OneCore Windows trong hộp thoại bộ đọc của NVDA. (#6159)
* Các tập tin cấu hình người dùng đã có thể lưu trong thư mục dữ liệu ứng dụng cục bộ. Chức năng này được bật trong phần thiết lập của registry. Xem phần "Các tham số hệ thống" trong tài liệu hướng dẫn sử dụng để biết thêm thông tin. (#6812)
* Đã thông báo giá trị các placeholder trong các trình duyệt web, cụ thể là hỗ trợ cho ARIA-placeholder.(#7004)
* Ở chế độ duyệt trong Microsoft Word, có thể dùng phím di chuyển nhanh (w và shift+w) chuyển qua lại các lỗi chính tả. (#6942)
* Hỗ trợ tương tác với điều khiển chọn ngày trong hộp thoại lịch hẹn của Microsoft Outlook. (#7217)
* NVDA đã đọc gợi ý đang chọn ở trường To/CC của Windows 10 Mail và ô tìm kiếm của cửa sổ Settings trên Windows 10. (#6241)
* Sẽ phát âm thanh khi có gợi ý ở các ô tìm kiếm trên Windows 10, ví dụ như ô tìm kiếm ở màn hình khởi động, cửa sổ settings, To/CC của Windows Mail. (#6241)
* Tự động đọc các thông báo của bản Skype Business cho desktop khi có người bắt đầu cuộc trò chuyện với bạn. (#7281)
* Tự động thông báo tin nhắn mới khi đứng tại cửa sổ trò chuyện của bản Skype for Business. (#7286)
* Tự động đọc thông báo trong Microsoft Edge, ví dụ khi có một download được bắt đầu. (#7281)
* Có thể nhập liệu cả chữ nổi đầy đủ và viết tắt với bàn phím chữ nổi trên màn hình nổi. Xem phần nhập liệu chữ nổi trong tài liệu hướng dẫn sử dụng để biết thêm thông tin. (#2439)
* Bạn có thể nhập ký tự chữ nổi Unicode với bàn phím chữ nổi trên màn hình nổi bằng cách chọn Chữ nổi Unicode ở mục bảng đầu vào trong hộp thoại thiết lập màn hình nổi. (#6449)
* Hỗ trợ màn hình nổi SuperBraille được sử dụng nhiều ở Đài Loan. (#7352)
* Các bảng chuyển đổi chữ nổi mới: Danish 8 dot computer braille, Lithuanian, Persian 8 dot computer braille, Persian grade 1, Slovenian 8 dot computer braille. (#6188, #6550, #6773, #7367)
* Cập nhật bảng chuyển đổi chữ nổi cho tiếng Anh Mỹ, bao gồm những dấu bullet, ký hiệu euro và những ký tự có dấu. (#6836)
* Hiện NVDA có thể sử dụng chức năng OCR của Windows 10 để nhận dạng văn bản từ hình ảnh và những ứng dụng không tiếp cận. (#7361)
 * Có thể chọn ngôn ngữ từ hộp thoại Windows 10 OCR trong thực đơn tùy chọn của NVDA. 
 * Nhấn NVDA+r để nhận dạng đối tượng điều hướng hiện tại.
  * Xem thêm phần Nhận Dạng Nội Dung trong tài liệu hướng dẫn sử dụng để biết thêm thông tin.
  * Bạn có thể chọn thông tin ngữ cảnh nào được hiển thị trên màn hình nổi khi đối tượng có focus trong mục "Trình bày ngữ cảnh tại focus" trong hộp thoại thiết lập màn hình nổi. (#217)
 * Ví dụ: hai tùy chọn "Điền trên màn hình khi thay đổi ngữ cảnh" và "Chỉ khi cuộn lại" sẽ hoạt động tốt với loại danh sách và thực đơn, vì vị trí các mục sẽ không thay đổi liên tục trên màn hình.
  * Xem phần "Trình bày ngữ cảnh tại focus" trong tài liệu hướng dẫn sử dụng để biết thêm thông tin.
* Trong Firefox và Chrome, NVDA đã hỗ trợ những đối tượng lưới động phức tạp, ví dụ như các bảng tính mà nó chỉ tải hoặc hiển thị một vài nội dung.  Cụ thể, là hỗ trợ những thuộc tính aria giới thiệu trong phiên bản 1.1 như aria-rowcount, aria-colcount, aria-rowindex và aria-colindex. (#7410)

### Thay Đổi

* Thêm thao tác chưa được gán phím (script_restart) để giúp khởi động lại NVDA nhanh hơn. Xem trong phần các lệnh tổng hợp trong hộp thoại quản lý thao tác của NVDA. (#6396)
* Có thể cài đặt kiểu bàn phím ở cửa sổ chào mừng của NVDA. (#6863)
  * Thêm nhiều định nghĩa viết tắt cho các cột mốc và trạng thái của điều khiển. Xem phần viết tắt cho các cột mốc và trạng thái điều khiển trong tài liệu hướng dẫn sử dụng để biết đầy đủ danh sách các định nghĩa viết tắt này. (#7188)
* Đã cập nhật Espeak-ng lên phiên bản 1.49.1 (#7280).
* Đã sắp xếp các mục trong danh sách bảng đầu vào và đầu ra của hộp thoại thiết lập màn hình nổi theo an-pha-bê. (#6113)
* Cập nhật thư viện phiên dịch chữ nổi liblouis lên bản  3.2.0. (#6935)
* Bảng mã chữ nổi cấp 1 UEBC tiếng Anh được chọn là bảng mã mặc định. (#6952)
* Mặc định, NVDA chỉ hiển thị những phần thông tin ngữ cảnh mà nó thay đổi trên màn hình nổi mỗi khi một đối tượng có focus. (#217)
 * Trước đây, nó sẽ hiển thị tất cả thông tin ngữ cảnh cho dù bạn đã thấy thông tin ngữ cảnh đó rồi.
 * Bạn có thể chọn hiển thị theo cách cũ bằng cách chọn "Luôn luôn điền trên màn hình" ở tùy chọn "Trình bày ngữ cảnh tại focus" trong hộp thoại thiết lập màn hình nổi.
* Có thể chọn hình dạng con trỏ nổi khi chọn chế độ đi theo focus hoặc con trỏ duyệt. (#7112)
 * Cập nhật logo của NVDA. Logo được cập nhật theo kiểu pha trộn giữa các ký tự NVDA với chữ màu trắng trên nền màu tía. Điều này sẽ giúp có thể nhìn thấy logo NVDA trên những màu nền khác. Sử dụng cùng màu tía với logo của NV Access. (#7446)

### Sửa Lỗi

* Đối với các thành phần div có thể soạn thảo trong Chrome, khi ở chế độ duyệt, nhãn không còn thông báo giống với giá trị của nó. (#7153)
* Ở chế độ duyệt trong Microsoft Word, nhấn phím End trong một văn bản trống sẽ không còn bị lỗi runtime. (#7009)
* Đã hỗ trợ chế độ duyệt trong Microsoft Edge khi tài liệu được cung cấp vai trò ARIA cụ thể cho nó. (#6998)
* Ở chế độ duyệt, nhấn shift+end đã có thể chọn hoặc bỏ chọn về cuối dòng, ngay cả khi dấu nháy nằm tại ký tự cuối của dòng đó. (#7157)
* Nếu hộp thoại có thanh tiến trình, văn bản hộp thoại sẽ được cập nhật khi thanh tiến trình thay đổi. Ví dụ, thời gian còn lại trong hộp thoại tải NVDA đã có thể đọc bằng văn bản với NVDA. (#6862)
* NVDA sẽ thông báo các thay đổi vùng chọn trong một số hộp xổ của Windows 10, ví dụ như hộp xổ Autoplay trong phần Settings. (#6337).
* Không còn thông báo thông tin không tồn tại ở hộp thoại tạo lịch hẹn hay cuộc họp của Microsoft Outlook. (#7216)
* Bíp ở các hộp thoại có thanh tiến trình không xác định như hộp thoại kiểm tra bản cập nhật, khi thiết lập cho thanh tiến trình bao gồm lựa chọn bíp. (#6759)
* Đã đọc lại các ô khi di chuyển bằng mũi tên trong bảng tính với Microsoft Excel 2003 và 2007. (#8243)
* Chế độ duyệt đã được tự động bật khi đọc email trong Windows 10 Mail với bản Windows 10 creator update và những bản sau này. (#7289)
* Ở hầu hết màn hình nổi có bàn phím chữ nổi, chấm 7 sẽ dùng để xóa ký tự hoặc ô được nhập trước đó và chấm 8 là phím enter. (#6054)
* Khi đứng ở văn bản có thể chỉnh sửa và di chuyển dấu nháy, ví dụ với phím mũi tên hoặc xóa lùi, NVDA đã đọc chính xác hơn, đặc biệt là trong Google Chrome và những ứng dụng đầu cuối. (#6424)
* Đã đọc nội dung trong cửa sổ viết chữ ký của Microsoft Outlook 2016. (#7253)
* NVDA không còn treo khi di chuyển bảng biểu ở các ứng dụng Java Swing. (#6992)
* NVDA không còn đọc thông báo toast nhiều lần trên Windows 10 Creators Update. (#7128)
* Trên Windows 10, NVDA không còn đọc nội dung tìm kiếm sau khi nhấn Enter để đóng start menu. (#7370)
* Di chuyển nhanh giữa các tiêu đề trong Microsoft Edge đã cải thiện nhanh hơn rất nhiều. (#7343)
* NVDA không còn bỏ qua nhiều phần lớn nội dung trang web trên một số website như giao diện Wordpress 2015 khi ở chế độ duyệt của Microsoft Edge. (#7143)
* Trong Microsoft Edge, các cột mốc (landmarks) đã được bản địa hóa, thay vì dùng tiếng Anh như thường lệ. (#7328)
* Con trỏ Braille đã đi theo vùng chọn khi vùng chọn lớn hơn màn hình nổi.  Ví dụ, khi nhấn shift+mũi tên xuống để chọn nhiều dòng, màn hình nổi sẽ hiển thị dòng chọn cuối cùng. (#5770)
* Ở Firefox, NVDA không còn đọc "Section" nhiều lần khi mở mục chi tiết của bài viết trên trang Twitter. (#5741)
* Các lệnh di chuyển trong bảng không có hiệu lực với loại bảng bố cục nếu không bật tùy chọn thông báo bảng bố cục. (#7382)
* Trong Firefox và Chrome, khi thực hiện lệnh di chuyển trong bảng ở chế độ duyệt sẽ bỏ qua những ô có thuộc tính ẩn. (#6652, #5655)

### Các thay Đổi cho Nhà Phát Triển

* Đã thêm mili giây vào phần đánh dấu thời gian trong  bản ghi. (#7163)
* NVDA phải được build với Visual Studio Community 2015. Đã ngưng hỗ trợ cho bộ Visual Studio Express. (#7110)
 * Cũng yêu cầu cài đặt thêm bộ Windows 10 Tools và SDK; có thể chọn khi cài đặt Visual Studio.
 * Vui lòng xem phần hướng dẫn cài đặt các gói phụ thuộc để biết thêm thông tin.
 * Hỗ trợ những trình nhận dạng nội dung như công cụ mô tả ảnh và OCR, đã có thể dễ dàng thực hiện với gói ContentRecog mới. (#7361)
* Gói Python json đã được biên dịch chung với bản chạy NVDA. (#3050)

## 2017.2

Một số điểm nổi bật trong bản phát hành này bao gồm: hỗ trợ đầy đủ các chế độ giảm âm lượng ứng dụng khác trên Windows 10 Creators Update; Sửa một số  vấn đề khi chọn ở chế độ duyệt ví dụ như chọn tất cả; cải thiện khả năng làm việc với  Microsoft Edge; và cải thiện nhiều hỗ trợ cho web ví dụ như nhận biết các thành phần sử dụng ARIA-current.

### Tính Năng Mới

* Có thể thông báo thông tin đường viền ô trong Microsoft Excel với phím tắt NVDA+f. (#3044)
* NVDA đã có thể nhận biết các thành phần được đánh dấu với current trên các trình duyệt web (cụ thể là khi dùng thuộc tính ARIA-current). (#6358)
* Hỗ trợ tự động chuyển ngôn ngữ cho Microsoft Edge. (#6852)
* Hỗ trợ chương trình máy tính trên Windows 10 Enterprise LTSB (Long-Term Servicing Branch) và bản máy chủ. (#6914)
* Thực hiện lệnh đọc dòng hiện tại nhanh ba lần sẽ đánh vần dòng đó với phần mô tả ký tự. (#6893)
* Thêm ngôn ngữ Burmese
* Đã đọc ký hiệu phân số và dấu mũi tên lên xuống mã unicode. (#3805)

### Các Thay Đổi

* Khi di chuyển với chế độ duyệt đơn giản trong những ứng dụng sử dụng UI Automation, nhiều đối tượng chứa không liên quan  sẽ được bỏ qua. Điều này sẽ giúp việc di chuyển dễ dàng hơn. (#6948, #6950) 

### Sửa Lỗi

* Đã có thể kích hoạt các mục trong thực đơn trên web khi ở chế độ duyệt. (#6735)
* Nhấn escape khi focus đang ở cửa sổ xác nhận xóa hồ sơ cấu hình sẽ thoát khỏi hộp thoại. (#6851)
* Sửa lỗi treo khi bật chức năng multi-process (đa xử lý) trong Mozilla Firefox và các ứng dụng Gecko khác. (#6885)
* Ở chế độ xem màn hình (screen reivew), việc thông báo màu nền đã chính xác hơn khi nội dung được trình bày trên nền trong suốt. (#6467) 
* Cải thiện tính năng hỗ trợ các mô tả điều khiển trên trang web cho Internet Explorer 11, (bao gồm hỗ trợ aria-describedby trong iframes và khi có nhiều ID được khai báo). (#5784)
* Tất cả chức năng giảm âm lượng ứng dụng khác như giảm khi đọc và phát âm thanh, không giảm và luôn luôn giảm đã hoạt động lại với bản cập nhật Windows 10 Creator, giống như ở các bản phát hành trước của Windows. (#6933)
* NVDA đã có thể di chuyển đến và đọc các điều khiển UIA không có khai báo phím tắt. (#6779)
* Không còn thêm vào hai khoảng trắng trong phần thông tin phím tắt cho các điều khiển UIA. (#6790)
* Một số tổ hợp phím trên màn hình nổi HIMS như (space+chấm 4), không còn tình trạng thỉnh thoảng ngưng hoạt động. (#3157)
* Sửa lỗi mở cổng serial trên các máy dùng ngôn ngữ không phải là tiếng Anh. Điều này, đã gây ra một số trường hợp không thể kết nối màn hình nổi. (#6845)
* Giảm nguy cơ hỏng tập tin cấu hình khi tắt máy. Hiện nay, tập tin cấu hình sẽ được lưu trong tập tin tạm trước khi được lưu vào tập tin cấu hình chính. (#3165)
* Sử dụng đúng ngôn ngữ khi thực hiện nhanh hai lần lệnh đọc dòng hiện tại để đánh vần. (#6726)
* Di chuyển dòng trong Microsoft Edge trên Windows 10 Creaters Update đã nhanh hơn 3 lần (#6994)
* NVDA không còn thông báo "Web Runtime Grouping" khi focus đứng ở tài liệu Microsoft Edge trên Windows 10 Creaters Update. (#6948)
* Đã hỗ trợ tất cả phiên bản hiện có của SecureCRT. (#6302)
* Adobe Acrobat Reader không còn bị treo trong một số tài liệu PDF (cụ thể là những tài liệu có thuộc tính ActualText trống). (#7021, #7034)
* Khi ở chế độ duyệt trong Microsoft Edge, nhấn t và shift+t để duyệt bảng sẽ không còn bỏ qua các loại bảng tương tác (ARIA rid). (#6977)
* Ở chế độ duyệt, Sau khi chọn, nhấn shift+home sẽ bỏ chọn và về đầu dòng. (#5746)
* Khi ở chế độ duyệt, nhấn (control+a) đã có thể chọn tất cả, mà không cần dấu nháy phải đứng ở đầu văn bản. (#6909)
* Sửa một số lỗi hiếm gặp khi chọn ở chế độ duyệt. (#7131)

### Các Thay Đổi Cho Nhà Phát Triển

* Các tham số dòng lệnh đã được xử lý bởi mô-đun argparser của Python, thay vì là optparser. Điều này sẽ cho phép xử lý riêng các tùy chọn như -r và -q. (#6865)
* core.callLater sẽ ở hàng chờ hàm gọi đến hàng chờ chính của NVDA sau một khoảng độ trễ được chỉ định, thay vì can thiệp phần lõi và thực thi trực tiếp.  Điều này sẽ giúp ngưng sự cố đóng băng hoặc treo sau khi phần lõi xử lý hàm gọi, ví dụ như khi gọi hàm giữa chừng để hiển thị hộp thông báo. (#6797) 
* Thuộc tính InputGesture.identifiers đã được thay đổi, vì vậy nó sẽ không còn được normalize. (#6945)
 * Các lớp con (subclasses) không còn cần phải normalize các indentifier trước khi trả về lại từ thuộc tính này. .
  * Nếu muốn normalize các identifier, bây giờ bạn có thể dùng thuộc tính InputGesture.normalizedIdentifiers. Nó sẽ normalize các identifiers được trả về bởi thuộc tính identifiers.
* Thuộc tính InputGesture.logIdentifier hiện nay sẽ không được khuyến khích tiếp tục sử dụng. Thay vào đó, có thể dùng InputGesture.identifiers[0]. (#6945)
* Bỏ các mã không còn được khuyến khích sử dụng:
 * Các hằng số `speech.REASON_*`, thay vào đó, sẽ sử dụng `controlTypes.REASON_*`. (#6846)
 * `i18nName` để thiết lập bộ đọc. Sẽ thay thế bằng `displayName` và `displayNameWithAccelerator`. (#6846, #5185)
 * `config.validateConfig`. (#6846, #667)
 * `config.save`: thay vào đó, hãy sử dụng `config.conf.save`. (#6846, #667)
 * Danh sách thành phần hoàn tất trong thực đơn ngữ cảnh autocomplete (tự động hoàn tất) của PythonConsole sẽ không còn hiển thị phần đường dẫn đối tượng đứng phía trước ký hiệu cuối được hoàn tất. (#7023)
 * Hiện đã có framework kiểm thử theo đơn vị cho NVDA. (#7026)
 * Cấu trúc cơ sở hạ tầng và phần kiểm thử theo đơn vị nằm tại thư mục tests/unit. Xem docstring trong  tập tin tests\unit\init.py để biết thêm thông tin.
 * Bạn có thể chạy phần kiểm thử với "scons tests". Hãy xem phần "Running Tests" trong tập tin  readme.md để biết thêm thông tin.
 * Nếu muốn gửi pull request cho NVDA, bạn cần phải chạy thành công phần kiểm thử.

## 2017.1

Một số tính năng mới nổi bật trong phiên bản này bao gồm thông báo các vùng và cột nội dung trong Microsoft Word; hỗ trợ di chuyển, ghi chú lại và đọc sách với máy Kindle bản PC; và những cải thiện cho Microsoft Edge.

### Tính Năng Mới

* Đã có thể thông báo các kiểu số phân vùng và ngắt vùng trong Microsoft Word . Chức năng này được bật ở tùy chọn "Báo số trang" trong hộp thoại định dạng tài liệu. (#5946)
* Đã có thể thông báo các cột nội dung trong Microsoft Word . Chức năng này được bật ở tùy chọn "Báo số trang" trong hộp thoại định dạng tài liệu. (#5946)
* Đã hỗ trợ tự chuyển đổi ngôn ngữ trong Wordpad. (#6555)
* Lệnh tìm kiếm của NVDA (NVDA+control+f) đã được hỗ trợ trong chế độ duyệt (Browse mode) cho Microsoft Edge. (#6580)
* Lệnh di chuyển nhanh ở chế độ duyệt đến các nút (b và shift+b) đã được hỗ trợ trong  Microsoft Edge. (#6577)
* Thiết lập cho tiêu đề cột và dòng vẫn được nhớ khi copy bảng tính từ Microsoft Excel. (#6628)
* Hỗ trợ đọc và duyệt sách trên máy Kindle phiên bản PC 1.19, sử dụng được các mục như liên kết, phần chú thích chân, hình ảnh, nội dung in đậm và ghi chú của người dùng. Vui lòng xem thêm phần Kindle cho PC trong tài liệu hướng dẫn sử dụng của NVDA. (#6247, #6638)
* Di chuyển bảng ở chế độ duyệt đã được hỗ trợ trong Microsoft Edge. (#6594)
* Trong Microsoft Excel, phím lệnh thông báo vị trí con trỏ duyệt (Máy bàn: NVDA+delete bàn phím số, Sách tay: NVDA+Delete) đã đọc tên của bảng tính và vị trí ô. (#6613)
* Thêm tùy chọn khởi động lại với chế độ bản ghi dò lỗi trong hộp thoại thoát NVDA. (#6689)

### Thay Đổi

* Tốc độ nháy tối thiểu của con trỏ màn hình nổi là 200ms. Những cấu hình trước đây có giá trị thấp hơn sẽ tự động được thiết lập về 200ms. (#6470)
* Thêm một tùy chỉnh hộp kiểm trong hộp thoại thiết lập màn hình nổi cho phép tắt/bật nhấp nháy con trỏ màn hình nổi.  Trước đây, nhập giá trị 0 để tắt. (#6470)
* Cập nhật eSpeak NG (Bản phát triển e095f008, 10 tháng 1, 2017). (#6717)
* Do những thay đổi trong bản cập nhật của windows 10 Creators, chế độ "Luôn luôn giảm âm" đã được gỡ bỏ khỏi phần cấu hình giảm âm lượng các ứng dụng khác. Chế độ này vẫn được giữ cho bản Windows 10 cũ. (#6684)
* Do những thay đổi trong bản cập nhật của windows 10 Creators, chế độ giảm âm khi NVDA đọc và phát âm thanh sẽ không còn đảm bảo giảm âm thanh ứng dụng khác ngay khi NVDA đọc. Những thay đổi này không ảnh hưởng  đến bản Windows 10 cũ. (#6684)

### Sửa Lỗi

* Sửa lỗi treo khi di chuyển giữa các đoạn trong một văn bản lớn ở chế độ duyệt trong Microsoft Word (#6368)
* Các bảng được copy từ Microsoft Excel qua Microsoft Word không còn được xem như bảng bố cục  vì vậy sẽ không bị bỏ qua (#5927)
* Khi nhập liệu trong Microsoft Excel ở chế độ bảo vệ, NVDA sẽ phát âm thanh thay vì đọc các ký tự được gõ (#6570)
* Khi nhấn Escape trong Microsoft Excel sẽ không chuyển sang chế độ duyệt, trừ phi người dùng chuyển sang chế độ duyệt trước đó với NVDA+space và sau đó ở trong chế độ focus bằng cách nhấn Enter trong ô biểu mẫu. (#6569) 
* NVDA không còn treo trong các bảng tính  của Microsoft Excel khi toàn bộ  một dòng hoặc  cột được kết hợp (merged) (#6216)
* Thông báo chính xác hơn các văn bản bị cắt hoặc bị tràn trong các ô của Microsoft Excel. (#6472)
* NVDA sẽ thông báo các hộp kiểm có thuộc tính Chỉ đọc (Read-only). (#6563)
* Trình chạy NVDA sẽ không hiển thị hộp thoại cảnh báo khi nó không thể phát âm thanh logo do thiếu thiết bị âm thanh. (#6289)
* Các điều khiển không hoạt động trong ribbon của Microsoft Excel sẽ được thông báo. (#6430)
* NVDA không còn thông báo "vùng (pane)" khi thu nhỏ cửa sổ. (#6671)
* Đã đọc ký tự khi gõ trong các ứng dụng của nền Windows Universal (UWP), (bao gồm Microsoft Edge) trong bản cập nhật  Windows 10 Creators. (#6017)
* Chức năng di chuyển theo chuột đã hoạt động trong mọi cửa sổ của máy tính có nhiều màn hình. (#6598)
* NVDA không còn bị lỗi sau khi đóng chương trình Windows Media Player trong khi focus nằm tại điều khiển thanh trượt. (#5467)

### Các thay đổi cho nhà phát triển

* Các tập tin cấu hình cũng như hồ sơ cá nhân đều tự động được nâng cấp để đáp ứng những yêu cầu chỉnh sửa schema. Nếu có lỗi khi nâng cấp, hộp thoại thông báo sẽ xuất hiện, cấu hình sẽ được khởi tạo lại và tập tin cấu hình cũ được lưu trong bản ghi log của NVDA tại cấp 'Info'. (#6470)

## 2016.4

Các điểm chính trong phiên bản này bao gồm, cải thiện Microsoft Edge; chế độ duyệt trong   ứng dụng Windows 10 Mail; và những cập nhật quan trọng cho các hộp thoại của NVDA.

### Các Tính Năng Mới

* NVDA sẽ xác định thụt đầu dòng bằng âm thanh. Có thể cấu hình trong hộp combo "Báo thụt đầu dòng" trong hộp thoại tùy chọn định dạng tài liệu của NVDA. (#5906)
* Hỗ trợ màn hình nổi Orbit Reader 20. (#6007)
* Thêm tùy chọn mở cửa sổ speech viewer khi khởi động. Có thể bật trong cửa sổ speech viewer. (#5050)
* Khi mở lại cửa sổ speech viewer, các vị trí và kích cỡ sẽ được phục hồi. (#5050)
* Các trường tham khảo trong Microsoft Word sẽ được xem như các liên kết. Nó sẽ được thông báo là liên kết và có thể kích hoạt. (#5050)
* Hỗ trợ  màn hình nổi Baum SuperVario2, Baum Vario 340 và HumanWare Brailliant2. (#6116)
* Hỗ trợ cơ bản cho việc cập nhật Anniversary update của Microsoft Edge. (#6271)
* Chế độ duyệt sẽ được sử dụng khi đọc email với Windows 10 mail. (#6271)
* Thêm ngôn ngữ mới: Lithuanian.

### Các thay đổi

* Cập nhật thư viện phiên dịch chữ nổi liblouis lên 3.0.0. Bản này gồm nhiều cập nhật quan trọng cho Unified English Braille. (#6109, #4194, #6220, #6140)
* Trong trình quản lý Add-ons, nút tắt và bật đã có phím tắt lần lượt là (alt+d và alt+e). (#6388)
* Nhiều vấn đề canh chỉnh và dấu chân trong các hộp thoại của NVDA đã được chỉnh sửa. (#6317, #5548, #6342, #6343, #6349)
* Hộp thoại định dạng tài liệu đã được điều chỉnh để có thể cuộn nội dung. (#6348)
* Điều chỉnh lại bố cục hộp thoại phát âm ký hiệu để danh sách ký hiệu sẽ sử dụng toàn bộ độ rộng của hộp thoại. (#6101)
* Ở chế độ duyệt trong các trình duyệt web, các phím lệnh di chuyển nhanh đến các trường soạn thảo (e and shift+e) và biểu mẫu (f and shift+f) có thể dùng để di chuyển đến các trường soạn thảo có thuộc tính Chỉ đọc (Read-only). (#4164)
* Ở các thiết lập định dạng tài liệu NVDA, "Thông báo thay đổi định dạng sau con trỏ" được đổi tên thành "Báo thay đổi định dạng sau con trỏ", vì nó ảnh hưởng đến phần chữ nổi và đọc. (#6336)
* Điều chỉnh lại màn hình "hộp thoại chào mừng" của NVDA. (#6350)
* Nút "Đồng ý" và "Hủy" của các hộp thoại NVDA đều được canh phải trên các hộp thoại. (#6333)
* Các điều khiển spin được dùng cho các trường nhập số như "Phần trăm thay đổi độ cao chữ hoa" trong hộp thoại thiết lập giọng đọc. Bạn có thể nhập giá trị hoặc dùng mũi tên lên/xuống để điều chỉnh. (#6099)
* Cách thông báo các IFrames (nội dung nhúng trong một tài liệu) đã thống nhất và ổn định trên các trình duyệt web khác nhau. IFrames được thông báo là "frame" trong Firefox. (#6047)

### Đã sửa các lỗi

* Sửa lỗi hiếm gặp khi tắt NVDA trong khi speech viewer mở. (#5050)
* Các Image maps chạy đúng trong Mozilla Firefox. (#6051)
* Khi đứng trong hộp thoại Từ điển, nhấn Enter sẽ lưu lại các thay đổi và đóng hộp thoại. Trước đây, khi nhấn Enter sẽ không có tác dụng. (#6206)
* Các thông điệp sẽ hiển thị dạng chữ nổi khi thay đổi chế độ nhập cho một phương thức nhập (native input/alphanumeric, full shaped/half shaped, etc.). (#5892, #5893)
* Khi tắt và bật một add-on ngay sau đó hoặc ngược lại, trạng thái của add-on sẽ được hiển thị đúng. (#6299)
* Khi sử dụng Microsoft Word, có thể đọc được ô số trang trong các tiêu đề. (#6004)
* Chuột có thể di chuyển focus giữa danh sách ký hiệu và ô soạn thảo trong hộp thoại phát âm ký hiệu. (#6312)
* Ở chế độ duyệt trong Microsoft Word, đã sửa lỗi không hiển thị danh sách các thành phần khi trong tài liệu có liên kết không hợp lệ. (#5886)
* Sau khi tắt từ thanh tác vụ hoặc bằng phím tắt Alt+F4, hộp kiểm speech viewer trong thực đơn NVDA sẽ hiển thị rõ ràng cửa sổ của nó. (#6340)
* Lệnh tải lại plugin không còn gặp lỗi đối với hồ sơ cấu hình, cho các tài liệu mới trong trình duyệt web và screen review. (#2892, #5380)
* Trong danh sách ngôn ngữ của hộp thoại thiết lập chung, các ngôn ngữ như Aragonese đã được hiển thị đúng. (#6259)
* Các phím của bàn phím hệ thống mô phỏng như một nút trên màn hình nổi mô phỏng chức năng phím Tab, đã có trong phần cấu hình ngôn ngữ NVDA trong hộp thoại thao tác nhập và giúp đỡ nhập. Trước đây, nó chỉ có trong tiếng Anh. (#6212)
* Thay đổi ngôn ngữ NVDA (từ hộp thoại thiết lập chung) sẽ không có tác dụng đến khi NVDA được khởi động lại. (#4561)
* Không thể để ô pattern trống khi tạo một mục mới trong từ điển phát âm. (#6412)
* Sửa lỗi hiếm gặp khi quét tìm cổng serial trên một số hệ thống đã không thể sử dụng một số drivers của màn hình nổi. (#6462)
* Trong Microsoft Word, đã đọc các dấu bullet số khi di chuyển theo ô trong bảng biểu. (#6446)
* Đã có thể gán các thao tác lệnh cho driver màn hình nổi Handy Tech trong hộp thoại thao tác nhập của NVDA. (#6461)
* Trong Microsoft Excel, nhấn Enter khi duyệt các bảng tính, NVDA sẽ thông báo chính xác dòng kế. (#6500)
* iTunes sẽ không còn thỉnh thoảng treo khi dùng chế độ duyệt trong iTunes Store, Apple Music vvv. (#6502)
* Sửa lỗi sung đột và treo trong các ứng dụng 64-bit trên nền Chrome và Mozilla. (#6497)
* Khi bật multi-process trong Firefox, các ô soạn thảo và chế độ duyệt đã hoạt động tốt. (#6380)

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2016.3

Các cải tiến của bản phát hành này bao gồm khả năng vô hiệu hóa một Add-on riêng biệt, hỗ trợ dùng biểu mẫu trong Microsoft Excel; cải thiện khả năng đọc màu; các chỉnh sửa / cải tiến cho vài loại màn hình chữ nổi và cải tiến trong việc hỗ trợ cho Microsoft Word.

### Các tính năng mới

* Chế độ duyệt giờ đây đã có thể đọc các tài liệu PDF trong Microsoft Edge trên Windows 10 Anniversary Update. (#5740)
* Strikethrough và double-strikethrough hiện đã được thông báo một cách hợp lý trong Microsoft Word. (5800)
* Trong Microsoft Word, tên của bảng đã được đọc nếu được khai báo trước đó. Nếu có phần mô tả, người dùng có thể xem bằng lệnh dọc mô tả (NVDA+D) trong chế độ duyệt. (#5943)
* Trong Microsoft Word, NVDA đã thông báo các thông tin vị trí con trỏ khi di chuyển từng đoạn bằng lệnh Alt+ Shift+ mũi tên xuống và Alt+ Shift+ mũi tên lên. (#5945)
* Trong Microsoft Word, khoảng cách dòng đã được đọc thông qua các lệnh thông báo định dạng của NVDA, khi thông số này được thay đổi bằng các phím nóng của Word và khi di chuyển qua các dòng với các định dạng khác nhau về khoảng cách, mà tính năng thông báo khoảng cách dòng  trong cài đặt định dạng tài liệu được bật. (#2961)
* Trong Internet Explorer, cấu trúc thành phần HTML5 đã được nhận biết. (#5591)
* Có thể vô hiệu tính năng thông báo chú thích (trong Microsoft Word chẳng hạn) bằng cách bỏ chọn mục thông báo chú thích trong hộp thoại cài đặt định dạng tài liệu. (#5108)
* Giờ đây, đã có thể vô hiệu hóa một Add-on nào đó thông qua trình quản lý Add-on. (#3090)
* Thêm các phím lệnh cho màn hình chữ nổi dòng ALVA BC640/680. (#5206)
* Đã có lệnh di chuyển con trỏ của màn hình chữ nổi đến vị trí đang có focus. Hiện nay, chỉ dòng ALVA BC640/680 được gán phím nóng cho lệnh này. Tuy nhiên, người dùng có thể gán phím nóng cho các màn hình chữ nổi khác thông qua hộp thoại Quản lý thao tác. (#5250)
* Trong Microsoft Excel, bạn đã có thể tương tác được với biểu mẫu. Bạn di chuyển đến các biểu mẫu thông qua danh sách các thành phần hoặc dùng các phím di chuyển nhanh trong chế độ duyệt. (#4953)
* Giờ đây, bạn có thể gán thao tác để bật/ tắt chế độ simple review thông qua hộp thoại Quản lý thao tác. (#6173)

### Các thay đổi

* Giờ đây, NVDA thông báo màu sắc bằng nhóm màu căn bản, phổ biến, gồm 9 kiểu màu thông thường, 3 kiểu màu bóng, với bóng sáng và bóng mờ. như vậy sẽ tốt hơn là thông báo màu với nhiều chủ đề và với những tên gọi khó hiểu. (#6029)
* Phím lệnh NVDA+F9 và NVDA+F10 đã được thay đổi. Giờ đây, người dùng bấm F10 lần thứ nhất để kết thúc vùng chọn, bấm thêm lần nữa để sao chép vùng chọn vào bộ nhớ tạm. (#4636)
* Đã cập nhật bộ đọc eSpeak NG lên phiên bản Master 11b1a7b (ra mắt ngày 22/6/2016). (#6037)

### Sửa lỗi

* Ở chế độ duyệt trong Microsoft Word, định dạng của văn bản được giữ nguyên khi sao chép. (#5956)
* Trong Microsoft Word, NVDA đã đọc chính xác khi di chuyển trong bảng biểu bằng phím nóng của Word (Alt+Home, Alt+End, Alt+PageUp và Alt+PageDown), và các phím lệnh cho việc chọn văn bản trong bảng biểu đã được thêm vào nhóm các phím lệnh điều hướng. (#5961)
* Trong các hộp thoại của Microsoft Word, chế độ duyệt đối tượng đã được cải thiện và hoạt động một cách tuyệt vời. (#6036)
* Trong một vài ứng dụng như Visual Studio 2015, các phím lệnh như Ctrl+C để sao chép nay đã được NVDA đọc như mong đợi. (#6021)
* Sửa một lỗi hiếm gặp khi quét cổng Serial trên vài hệ thống. Lỗi này làm cho các driver màn hình chữ nổi trở nên vô dụng. (#6015)
* Việc đọc màu trong Microsoft Word giờ đây đã chính xác hơn khi mà các thay đổi trong giao diện nền của Office đã được đưa vào tài khoản. (#5997)
* Chế độ duyệt cho Microsoft Edge và hỗ trợ tính năng gợi ý tìm kiếm trên Start Menu nay đã hoạt động với các phiên bản Windows 10 phát hành sau tháng 4/2016. (#5955)
* Trong Microsoft Word, tính năng tự đọc tiêu đề của bảng biểu đã hoạt động tốt hơn khi làm việc với bảng có các ô được trộn lại. (#5926)
* Trong ứng dụng Mail của Windows 10, NVDA không còn bị lỗi không đọc được nội dung của
thư. (#5635)
* Khi bật chế độ đọc phím lệnh, không còn xảy ra tình trạng đọc hai lần các phím như phím khóa hoa. (#5490)
* NVDA đã đọc chính xác trong hộp thoại User account Control của Windows 10 Anniversary update. (#5942)
* Trong các Plugin dành cho trò chuyện trên Web như trang out-of-sight.net chẳng hạn, không còn xảy ra tình trạng NvDA phát ra tiếng Beep và đọc các cập nhật liên quan tới Microphone. (#5888)
* Khả năng vận hành của lệnh tìm tiếp và tìm lùi trong chế độ duyệt giờ đây sẽ thực hiện chính xác việc phân biệt chữ hoa/ chữ thường khi tìm kiếm, nếu trước đó người dùng đã tìm kiếm ở chế độ này. (#5522)
* Khi chỉnh sửa một từ trong từ điển, đã có phản hồi khi gán sai cú pháp. NVDA không còn bị hỏng khi gõ sai cú pháp. (#4834)
* Nếu NVDA không thể giao tiếp với một màn hình chữ nổi vì nó đã bị ngắt kết nối, việc sử dụng màn hình đó sẽ bị vô hiệu hóa. (#1555)
* Cải thiện khả năng vận hành của bộ lọc trong chế độ duyệt danh sách các thành phần trong vài trường hợp. (#6126)
* Trong Microsoft Excel, các tên của mẫu nền được thông báo bởi NVDA giờ đã thống nhất với tên dùng bởi Excel. (#6092)
* Cải thiện khả năng hỗ trợ cho màn hình đăng nhập của Windows 10, bao gồm việc đọc các thông báo và tiếp cận với ô nhập mật khẩu thông qua màn hình cảm ứng. (#6010)
* Giờ đây, NVDA đã nhận chính xác các nút secondary routing trên các màn hình chữ nổi ALVA dòng BC640/680. (#5206)
* NVDA lại tiếp tục đọc được các thông báo Toast của Windows trong các bản phát hành gần đây của Windows 10. (#6096)
* NVDA không còn tình trạng thỉnh thoảng không nhận biết các phím được bấm trên các màn hình nổi tương thích của Baum và HumanWare Brailliant B. (#6035)
* Nếu bật tính năng thông báo số dòng trong cài đặt định dạng tài liệu của NVDA, nó cũng sẽ hiển thị tên màn hình chữ nổi. (#5941)
* Khi tắt chế độ đọc, việc lấy thông tin qua các lệnh ở nhóm thông báo đôi tượng (Ví dụ: NVDA+Tab để thông báo vị trí con trỏ) sẽ hiển thị trong Speech Viewer như mong đợi. (#6049)
* Trong danh sách thư của Outlook 2016, không còn tình trạng thông báo các thông tin nháp. (#6219)
* Trong Google Chrome hay các trình duyệt dựa trên nền tảng này, và không sử dụng tiếng Anh, chế độ dhuyệt không bị lỗi khi đọc tài liệu. (#6249)

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2016.2.1

Bản phát hành này sửa lỗi làm treo Microsoft Word:

* NVDA không còn làm cho Microsoft Word bị lỗi ngay sau khi khởi động trong Windows XP. (#6033)
* Gỡ bỏ tính năng báo lỗi ngữ pháp vì nó gâyy ra lỗi bị treo trong Microsoft Word. (#5954, #5877)

## 2016.2

Các cải tiến của bản phát hành này bao gồm khả năng thông báo lỗi chính tả trong khi soạn thảo hỗ trợ thông báo lỗi ngữ pháp với Microsoft Word; sửa lỗi và cải thiện khả năng hỗ trợ cho Microsoft Office.

### Các tính năng mới

* Ở chế độ duyệt trong Internet Explorer và các điều khiển MSHTML khác, phím lệnh di chuyển qua các Annotation (A và Shift+A) sẽ di chuyển đến các đoạn văn bản được chèn và được xóa. (#5691)
* Trong Microsoft Excel, NVDA giờ đã thông báo cấp độ của một nhóm nhiều ô, cũng như chúng đang được mở rộng hay thu nhỏ. (#5690)
* Bấm lệnh thông báo định dạng văn bản (NVDA+F) nhanh hai lần sẽ hiển thị thông tin ở chế độ duyệt, dễ dàng xem các thông tin này hơn. (#4908)
* Từ Microsoft Excel 2010 trở lên, NVDA sẽ thông báo các ô có thuộc tính Shading và Gradient. Việc tự động thông báo được điều khiển bởi tùy chọn thông báo màu trong thiết lập định dạng tài liệu. (#3683)
* Bản phiên dịch chữ nổi mới: Koine Greek. (#5393)
* Trong Log Viewer, người dùng có thể lưu lại thông tin bằng phím Ctrl+S. (#4532)
* Nếu tính năng thông báo lỗi chính tả được bật và ứng dụng đang soạn thảo có hỗ trợ kiểm tra chính tả, NVDA sẽ phát âm thanh khi gặp từ sai chính tả. Người dùng có thể tắt tính năng này thông qua tùy chọn “Phát âm thanh báo lỗi chính tả khi nhập liệu" trong cài đặt bàn phím. (#2024)
* Lỗi ngữ pháp giờ đây đã được thông báo trong Microsoft Word. Có thể tắt tính năng này thông qua tùy chọn "Thông báo lỗi chính tả" trong cài đặt định dạng tài liệu của NVDA. (#5877)

### Các thay đổi

* Trong chế độ duyệt, ở các trường nhập liệu, phím Enter bên bàn phím số đã hoạt động giống như phím Enter bên bàn phím chữ. (#5385)
* NVDA đã chuyển sang bộ đọc eSpeak NG. (#5651)
* Trong Microsoft Excel, NVDA không bỏ qua các tiêu đề cột hay tiêu đề dòng trong trường hợp có một dòng trắng giữa phần dữ liệu và tiêu đề. (#5396)
* Trong Microsoft Excel, NVDA sẽ đọc tọa độ trước khi đọc tiêu đề cột / dòng để tránh sự nhầm lẫn giữa tiêu đề và nội dung. (#5396)

### Sửa lỗi

* Trong chế độ duyệt, khi dùng các phím di chuyển  để đi đến các thành phần không được hỗ trợ cho một tài liệu, NVDA sẽ thông báo nó không được hỗ trợ, thay vì thông báo không có thành phần đó. (#5691)
* Khi liệt kê các bảng tính trong danh sách các thành phần của Microsoft Excel, các bản tính chỉ có đồ thị nay đã được bao gồm trong NVDA. (#5698)
* Giờ đây, NVDA không thông báo những thông tin không cần thiết khi chuyển cửa sổ trong một ứng dụng Java với nhiều cửa sổ như IntelliJ hay Android Studio. (#5732)
* Trong vài phần mềm soạn thảo trên nền tảng Scintilla như Notepad ++, chữ nổi đã được cập nhật một cách chính xác khi di chuyển con trỏ bằng màn hình chữ nổi. (#5678)
* NVDA không còn lỗi thỉnh thoảng bị tắt khi bật đầu ra của chữ nổi. (#4457)
* Trong Microsoft Word, NVDA luôn thông báo các dấu thụt vào đầu dòng mà không bị phụ thuộc vào đơn vị đo (centimeters hay inches). (#5804)
* Khi sử dụng màn hình chữ nổi, hiển thị được nhiều thông điệp mà trước đây chỉ được NVDA thông báo bằng giọng nói. (#5557)
* Với các ứng dụng Java tiếp cận được với NVDA, thông tin về cấp độ của cây thư mục đã được thông báo (#5766)
* Sửa lỗi bị tắt ngang trong Mozilla Firefox và Adobe Flash Player trong vài trường hợp. (#5367)
* Trong Google Chrome và các trình duyệt dựa trên nền tảng này, nội dung trong các hộp thoại hay một ứng dụng có thể đọc được trong chế độ duyệt. (#5818)
* Trong Google Chrome và các trình duyệt dựa trên nền tảng này, người dùng có thể buộc NVDA chuyển sang Browse Mode trong một hộp thoại hay ứng dụng.
Trong Google Chrome và các trình duyệt dựa trên nền tảng này, giờ bạn có thể buộc NVDA chuyển sang chế độ duyệt trrong các hộp thoạii hay ứng dụng web. (#5818)
* Trong Internet Explorer hay các điều khiển MSHTML khác, di chuyển đến các điều khiển (cụ thể, khi dùng aria-activedescendant), NVDA không bị chuyển sang chế độ duyệt. Lỗi này thường xuất hiện khi di chuyển đến các gợi ý ở trường địa chỉ khi soạn thư trong Gmail. (#5676)
* Trong Microsoft Word, NVDA không bị đóng băng trong một bảng lớn khi bật tính năng thông báo tiêu đề cột / dòng. (#5878)
* Trong Microsoft Word, NVDA không thông báo sai các đoạn văn bản là Outline Level (nhưng không phải tiêu đề dựng sẵn) là Heading. #5186)
* Trong chế độ duyệt của Microsoft Word, lệnh Move Past End và Move Past To Of Container (comma và shift+comma) nay đã hoạt động với bảng. (#5883)

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2016.1

Các cải tiến của bản phát hành này bao gồm khả năng giảm âm lượng của các âm thanh khác; các cải thiện liên quan đến màn hình chữ nổi, sửa vài lỗi liên quan đến bộ ứng dụng Microsoft Office và chế độ duyệt trong iTunes.

### Các tính năng mới

* Các bản chữ nổi mới: Ba Lan máy tính 8 chấm,  Mông Cổ. (#5537, #5574)
* Bạn có thể tắt con trỏ chữ Braille và thay đổi hình dạng của nó thông qua tùy chọn hiện con trỏ và kiểu con trỏ trong hộp thoại cài đặt chữ nổi. (#5198)
* Giờ đây, NVDA có thể kết nối với màn hình chữ nổi HIMS Smart Beetle thông qua Bluetooth. (#5607)
* NVDA có thể giảm các âm thanh khác khi được cài đặt trên Windows 8 trở lên. Có thể cấu hình qua tùy chọn giảm âm thanh trong hộp thoại chọn bộ đọc của NVDA hoặc bấm NVDA+shift+d. (#3830, #5575)
* Hỗ trợ sử dụng APH Refreshabraille trong chế độ HID, Baum VarioUltra và Pronto! Khi kết nối qua USB. (#5609)
* Hỗ trợ các màn hình nổi HumanWare Brailliant BI/B khi giao thức được thiết lập là OpenBraille. (#5612)

### Các thay đổi

* Mặc định, tính năng thông báo nhấn mạnh đã được tắt. (#4920)
* Trong hộp thoại danh sách các thành phần của Microsoft Office Excel, phím nóng để hiển thị công thức nay được đổi thành Alt+R nên sẽ khác với phím tắt ở trường bộ lọc. (5527)
* Cập nhật thư viện phiên dịch chữ nổi liblouis lên 2.6.5. (#5574)
* Từ “văn bản” sẽ không còn được đọc khi di chuyển con trỏ máy hoặc con trỏ duyệt đến các đối tượng là văn bản. (#5452)

### Sửa lỗi

* Trong iTunes 12, chế độ duyệt nay đã cập nhật một cách chính xác khi một trang mới được tải xuống trong iTunes Store. (#5191)
* Trong Internet Explorer và các trình điều khiển khác có hỗ trợ HTML, phím tắt di chuyển đến các tiêu đề đã vận hành đúng như cách mà người dùng mong đợi khi một Heading bị bỏ đi nhằm phục vụ cho tính tiếp cận với trình đọc màn hình (chính xác là khi cấp độ của tiêu đề được  đánh dấu bằng Aria thay cho thẻ H). (#5434)
* Trong Spotify, con trỏ không thường xuyên bị rơi vào tình trạng “không xác định đối tượng”. (#5439)
* Con trỏ được trả về đúng vị trí trước đó của nó khi chuyển từ cửa sổ khác về Spotify . (#5439)
* Khi chuyển qua lại giữa 2 chế độ duyệt và chế độ Focus, NVDA sẽ thông báo chế độ được chọn bằng giọng nói, đồng thời hiển thị thông tin đó trên màn hình nổi. (#5239)
* NVDA sẽ không đọc nút Start là danh sách hay đã chọn khi di chuyển con trỏ đến nút này trên một số phiên bản hệ điều hành. (#5178)
* NVDA sẽ không đọc các thông điệp như “Inserted” khi soạn thư trong Microsoft Outlook. (#5486)
* Khi dùng màn hình chữ nổi mà có một đoạn văn bản được chọn ở dòng hiện tại (khi tìm những từ xuất hiện trên cùng một dòng chẳng hạn), nội dung trên màn hình chữ nổi sẽ được cuộn khi cần thiết. (#5410)
* NVDA sẽ không bị tắt một cách âm thầm khi bấm Alt+F4 để thoát Command Prompt trong Windows 10. (#5343)
* Trong hộp thoại danh sách các thành phần ở chế độ duyệt, khi người dùng thay đổi kiểu liệt kê thành phần, nội dung trong trường bộ lọc sẽ được xoá sạch. (#5511)
* Ở vùng soạn thảo trong các ứng dụng của Mozilla, khi di chuyển bằng chuột, NVDA sẽ đọc từ, kí tự, dòng… thay vì đọc toàn bộ nội dung. (#5535)
* Khi di chuyển chuột trong vùng soạn thảo trong các ứng dụng của Mozilla, việc đọc các điều khiển dạng Element như liên kết sẽ không bị dừng khi chúng chứa trong các dòng đang được đọc. (#2160, #5535)
* Trong Internet Explorer, NVDA nay đã đọc được nội dung trang shoprite.com trong chế độ duyệt thay vì đọc Blank. (#5569)
* Trong Microsoft Word, NVDA sẽ không đọc các Track Changes như “Inserted” khi Track Changes Markup không được hiển thị. (#5566)
* Khi bấm một nút bật / tắt tại vị trí con trỏ, NVDA sẽ thông báo khi chúng chuyển từ đã chọn sang không chọn. (#5441)
* Các thay đổi hình dạng chuột đã đượđã hoạt động như mong muốn. (#5595)
* Khi đọc các dòng có thụt vào đầu dòng, các khoảng trắng bị đặt sai quy tắc sẽ được thông báo ngắn gọn hơn (trước đây, NVDA đọc Space Space Space thay vì 3 Space). (#5610)
* Khi đóng một danh sách phương thức nhập hiện đại của Microsoft, focus được trả về đúng thành phần đầu vào của tài liệu cơ bản. (
* Từ Microsoft Office 2013 trở lên, khi Ribbond được thiết lập ở chế độ Show Only Tabs (chỉ hiện thị các Tab), các thành phần trên Ribbond sẽ được thông báo chính xác khi một Tab được kích hoạt. (#5504)
* Sửa lỗi và cải thiẹn cho việc tìm và nhận biết thao tác trên màn hình cảm ứng. (#5652)
* Không còn thông báo màn hình cảm ứng trong trợ giúp nhập. (#5652)
* NVDA không bị lỗi khi liệt kê các chú thích trong Microsoft Office Excel khi chúng nằm trong các ô bị trộn. (#5704)
* Trường hợp rất hiếm gặp, NVDA không bị lỗi khi đọc nội dung của Sheet khi bật chế độ đọc tiêu đề cột và dòng. (#5705)
* Trong Google Chrome, di chuyển trong vùng nhập liệu, kí tự trong các bảng chữ cái của người châu Á được thông báo chính xác. (#4080)
* Khi tìm kiếm nhạc của Apple bằng iTunes, kết quả tìm kiếm được cập nhật chính xác. (#5659)
* Trong Microsoft Office Excel, khi bấm Shift+F11 để tạo bảng tính mới, NVDA sẽ thông báo vị trí mới của con trỏ thay vì không đọc gì. (5689)
* Sửa lỗi hiển thị trên màn hình chữ nổi với tiếng Hàn Quốc. (#5640)

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2015.4

Các cải tiến của bản phát hành này bao gồm các cải thiện cho việc vận hành trên Windows 10; tích hợp vào Ease of Access Center (Windows 8 trở lên); các cải tiến cho Microsoft Excel, bao gồm liệt kê và đổi tên bảng tính và truy cập các ô bị khóa trong các bảng tính được bảo vệ, hỗ trợ soạn thảo văn bản với Mozilla Firefox, Google Chrome và Mozilla Thunderbird. 

### Tính năng mới

* NVDA được tích hợp trong Ease of access Center. (#308)
* Khi di chuyển giữa các ô trong Excel, các thay đổi về định dạng sẽ được thông báo nếu bật các tùy chọn liên quan trong hộp thoại định dạng tài liệu. (#4878)
* Tích hợp tính năng thông báo nhấn mạnh trong hộp thoại định dạng tài liệu và mặc định được bật. tùy chọn này cho phép NVDA tự thông báo sự tồn tại của các văn bản được nhấn mạnh trong một tài liệu. Đến nay, chỉ 	mới hỗ trợ các thẻ em và strong trong chế độ duyệt cho Internet Explorer và các điều khiển MSHTML khác. (#4920)
* NVDA sẽ thông báo các văn bản được chèn và xoá khi soạn thảo ở chế độ duyệt trên các trình biên tập web, nếu bật tính năng Report Editor Revision trong hộp thoại cài đặt tài liệu. (#4920)
* Khi xem Track Changes thông qua danh sách các thành phần của NVDA trong Microsoft Word, các thông tin liên quan đến thay đổi định dạng nay đã được hiển thị. (#4920)
* Trong Microsoft Excel, bấm NVDA+F7 để liệt kê các bảng tính cũng như đổi tên chúng. (#4630, #4414)
* Trong một bộ đọc, người dùng có thể quy định các dấu câu nào được đọc thông qua hộp thoại Sympal Pronounciation. (#5234)
* Trong Microsoft Excel, NVDA giờ đây đã thông báo các thông điệp đầu vào được tạo bởi người tạo bảng tính trên các ô. (#5051)
* Hỗ trợ màn hình chữ nổi  Baum Pronto! V4 và VarioUltra thông qua kết nối Bluetooth. (#3717)
* Hỗ trợ soạn thảo văn bản với các ứng dụng của Mozilla, như hỗ trợ Google Docs với chế độ chữ nổi được bật trong Mozilla Firefox và HTML composition trong Mozilla Thunderbird. . (#1668)
* Hỗ trợ soạn thảo văn bản trong Google Chrome và các ứng dụng trên nền tảng Chrome như Google Docs với hỗ trợ chữ nổi được bật. (#2634)
 * Yêu cầu Chrome 47 trở lên
* Ở  chế độ duyệt trong Microsoft Excel, người dùng có thể di chuyển qua các ô bị khoá trong các bảng tính được bảo vệ. (#4952)

### Các thay đổi

* Tùy chọn Report Editor Revisions trong hộp thoại định dạng tài liệu của NVDA giờ đây mặc định được bật. (#4920)
* khi di chuyển qua từng kí tự trong Microsoft Word với tùy chọn Report Editor Revisions được bật, thông tin cho track changes sẽ được thông báo ít hơn, giúp việc điều hướng trở nên hiệu quả hơn. Để có thêm thông tin, hãy dùng danh sách các thành phần. (#4920)
* Cập nhật thư viện phiên dịch chữ nổi liblouis lên 2.6.4. (#5341)
* Vài kí hiệu (các kí hiệu toán học cơ bản) đã được chuyển sang cấp độ một vài nên mặc định chúng sẽ được đọc. (# 3799)
* nếu bộ đọc có hỗ trợ, việc đọc sẽ được ngừng nghĩ khi gặp dấu ngoặc và dấu gạch ngang  (–). (#3799)
* Khi quét khối các đoạn văn bản, NVDA sẽ đọc nội dung của đoạn văn bản đó trước khi đọc đang chọn. (#1707)

### Sửa lỗi

* Cải tiến nhỏ cho khả năng vận hành khi duyệt danh sách thư trong Outlook 2010/2013. (#5268)
* Trong một biểu đồ trong Microsoft Excel, điều hướng bằng một số phím (như là chuyển sang bảng tính khác với control+pageUp và control+pageDown) giờ đâyy đã hoạt động chính xác. (#5336)
* Sửa diện mạo của các nút trong hộp thoại cảnh báo được hiển thị khi bạn chuẩn bị cài NVDA bản cũ hơn. (#5325)
* Từ Windows 8 trở lên, nếu thiết lập để khởi động cùng với Windows, NVDA sẽ khởi động nhanh hơn. (308)
 * Nếu cập nhật NVDA từ các phiên bản cũ hơn, người dùng cần thực hiện các bước sau đây để tắt rồi bật lại để tính năng này phát huy tác dụng:
  1. Vào hộp thoại Thiết lập chung
  1. Bỏ chọn Tự khởi động NVDA sau khi đăng nhập vào Windows
  1. Bấm nút Đồng ý
  1. Vào lại hộp thoại Thiết lập chung
  1. Đánh dấu chọn vào Tự khởi động NVDA sau khi đăng nhập vào Windows
  1. Bấm nút OK
+
* Cải thiện vận hành cho UI Automation bao gồm File Explorer và Task Viewer. (#5293)
* NVDA sẽ tự chuyển sang chế độ Focus nếu di chuyển bằng Tab đến các điều khiển có thuộc tính chỉ đọc ở chế độ duyệt trong Mozilla Firefox và các điều khiển trên nền Gecko. (#5118)
* NVDA đã đọc chính xác là “No Previous” thay vì “No Next” khi vuốt sang trái trên màn hình cảm ứng mà không còn đối tượng để di chuyển con trỏ đến.
* Sửa lỗi khi gõ nhiều từ trong ô lọc trong hộp thoại quản lý thao tác. (#5426)
* NVDA không còn bị treo trong vài trường hợp khi kết nối lại với một màn hình nổi HumanWare dòng Brailliant BI/B thông qua USB. (#5406)
* Trong các ngôn ngữ với các kí tự kết hợp, mô tả kí tự giờ đã hoạt động như mong muốn cho chữ hoa tiếng Anh. (#5375)
* NVDA không còn thỉnh thoảng bị đứng khi mở Start Menu trên Windows 10. (#5417)
* Trong Skype cho Desktop, các thông báo bị ẩn đã được NVDA đọc lên. (#4841)
* Các thông báo đã được NVDA đọc một cách chính xác trong Skype cho Desktop 7.12 trở lên. (#5405)
NVDA đã đọc chính xác vị trí con trỏ khi tắt trình đơn ngữ cảnh trong một số ứng dụng như Jart. (#5302)
* Windows 7 trở lên, tính năng báo màu đã trở lại trên một số ứng dụng như Wordpad. (#5352)
* Khi soạn thảo trong Microsoft Office Power Point mà bấm Enter, NVDA sẽ thông báo các văn bản đã được nhập vào. Ví dụ như dấu chấm đầu dòng (Bullet). (#5360)

## 2015.3

Các cải tiến của bản phát hành này bao gồm việc  bắt đầu hỗ trợ cho Windows 10; khả năng vô hiệu hóa kí tự di chuyển nhanh trong chế độ duyệt (hữu dụng cho vài ứng dụng web); cải thiện cho Internet Explorer; và sửa lỗi văn bản bị cắt khi nhập liệu trong một số ứng dụng với chữ nổi.

### Các tính năng mới

* lỗi chính tả đã được thông báo trong các trường nhập liệu với Internet Explorer và các điều khiển MSHTML khác. (#4174)
* Nhiều kí hiệu toán học mã Unicode giờ đây đã được đọc khi chúng xuất hiện trong văn bản. (#3805)
* Đã tự đọc gợi ý tìm kiếm trong start screen của Windows 10. (#5049)
* Hỗ trợ các màn hình nổi EcoBraille 20, EcoBraille 40, EcoBraille 80 và EcoBraille Plus. (#4078)
* Trong chế độ duyệt, có thể bật / tắt kí tự di chuyển nhanh bằng lệnh NVDA+shift+khoảng trắng. khi tắt, các phím chữ sẽ được chuyển tới ứng dụng, có ích cho một số ứng dụng web như Gmail, Twitter và Facebook. (#3203)
* Các bản chữ nổi mới: Phần Lan 6 chấm, Ailen cấp 1, Ailen cấp 2, Hàn quốc cấp 1 (2006), Hàn Quốc cấp 2 (2006). (#5137, #5074, #5097)
* Bàn phím QWERTY trên màn hình nổi Papenmeier BRAILLEX Live Plus đã được hỗ trợ. (#5181)
* Thử nghiệm hỗ trợ cho trình duyệt web Microsoft Edge và browsing engine trong Windows 10. (#5212)
* Ngôn ngữ mới: Kannada.

### Các thay đổi

* Cập nhật thư viện biên dịch chữ nổi liblouis lên 2.6.3. (#5137)
* Khi chuẩn bị cài một bản NVDA cũ hơn bản hiện tại, bạn sẽ được cảnh báo rằng điều này không được khuyến khích và phải gỡ hoàn toàn NVDA trước khi thực hiện. (#5037)

### Sửa lỗi

* Ở chế độ duyệt trong Internet Explorer và các điều khiển MSHTML khác, di chuyển nhanh qua các biểu mẫu không còn bao gồm các danh sách ngoài ý muốn. (#4204)
* Trong Firefox, NVDA không còn thông báo nội dung của một ARIA tab panel một cách không hợp lý khi focus chuyển vào bên trong nó. (#4638)
* Trong Internet Explorer và các điều khiển MSHTML khác, tab đến một phần, các bài viết hay các hộp thoại sẽ không còn tình trạng thông báo toàn bộ nội dung bên trong một cách không hợp lý. (#5021, #5025)
* Khi dùng các màn hình nổi Baum/HumanWare/APH  với bàn phím chữ nổi, đầu vào chữ nổi không còn bị ngưng hoạt động sau khi bấm các kiểu phím khác trên màn hình. (#3541)
* Trong Windows 10, các thông tin không liên quan không còn được thông báo khi bấm alt+tab hay alt+shift+tab để chuyển giữa các cửa sổ. (#5116)
* Văn bản được nhập không còn bị cắt khi dùng một số ứng dụng như Microsoft Outlook với màn hình chữ nổi. (#2953)
* Ở chế độ duyệt trong Internet Explorer và các điều khiển MSHTML khác, nội dung chính xác đã được thông báo khi một thành phần xuất hiện hay thay đổi và focus được đưa đến đó ngay lập tức. (#5040)
* Ở chế độ duyệt trong Microsoft Word, kí tự di chuyển nhanh giờ đây đã cập nhật màn hình chữ nổi và con trỏ duyệt như mong muốn. (#4968)
* Trong chữ nổi, các khoảng trắng không liên quan không còn hiển thị giữa hay sau các chỉ báo cho các điều khiển và định dạng. (#5043)
* khi một ứng dụng phản ứng chậm chạp và bạn chuyển cửa sổ đi khỏi nó, NVDA đã phản ứng nhanh hơn ở các ứng dụng kia trong đa số trường hợp. (#3831)
* Thông báo Toast của Windows 10 đã được đọc như mong đợi. (#5136)
* Giá trị đã được đọc đúng như thay đổi của nó trong một số hộp xổ (UI Automation) vốn trước đây không đọc được.
* Ở chế độ duyệt trong các trình duyệt, lệnh tab đã hoạt động như mong đợi sau khi tab đến một khung tài liệu. (#5227)
* Đã có thể bỏ qua Màn hình khóa của Windows 10 thông qua màn hình cảm ứng . (#5220)
* Trong Windows 7 và cao hơn, văn bản không còn bị cắt khi nhập trong một số ứng dụng như Wordpad và Skype với màn hình chữ nổi. (#4291)
* Ở màn hình khóa của Windows 10, không còn đọc được nội dung bộ nhớ tạm, truy cập các ứng dụng đang chạy bằng con trỏ duyệt, thay đổi cấu hình cho NVDA, v...v... (#5269)

## 2015.2

Các cải tiến của bản phát hành này bao gồm khả năng đọc biểu đồ trong Microsoft Excel, hỗ trợ đọc và tương tác với các nội dung toán học.

### Các tính năng mới

* Di chuyển tới hay lùi từng câu trong Microsoft Word và Outlook giờ đây đã có thể thực hiện với Alt + mũi tên lên / xuống. (#3288)
* Bản chữ nổi mới cho vài ngôn nữ tiếng Ấn độ. (#4778)
* Trong Microsoft Excel, NVDA giờ đây sẽ thông báo khi một ô có nội dung bị tràn hay bị khuất. (#3040)
* Trong Microsoft Excel, bạn có thể dùng danh sách các thành phần (NVDA+f7) để liệt kê danh sách theo biểu đồ, chú thích và công thức. (#1987)
* Hỗ trợ đọc biểu đồ trong Microsoft Excel. Để dùng tính năng này, chọn biểu đồ thông qua danh sách các thành phần (NVDA+f7) rồi dùng các phím mũi tên để di chuyển giữa các điểm dữ liệu. (#1987)
* Sử dụng MathPlayer 4 từ Design Science, NVDA giờ đây đã có thể đọc và duyệt các nội dung toán học trong các trình duyệt web, trong Microsoft Word và PowerPoint. Xem phần "Đọc nội dung toán học" trong tài liệu hướng dẫn để biết thêm chi tiết. (#4673)
* Giờ đây đã có thể gán các thao tác (phím lệnh, thao tác cảm ứng, v...v...) cho tất cả các hộp thoại như thiết lập và định dạng tài liệu của NVDA thông qua hộp thoại quản lý các thao tác. (#4898)

### Các thay đổi

* Trong hộp thoại định dạng tài liệu của NVDA, đã đổi phím tắt cho các tùy chọn thông báo danh sách, thông báo liên kết, thông báo số dòng và  thông báo tên phông. (#4650)
* Trong hộp thoại thiết lập chuột của NVDA, đã gán phím tắt cho tùy chọn phát âm thanh theo tọa độ khi chuột di chuyển và âm lượng độ sáng tọa độ âm thanh. (#4916)
* Các cải tiến đáng kể cho tính năng thông báo màu. (#4984)
* Cập nhật thư viện phiên dịch chữ nổi liblouis lên 2.6.2. (#4777)

### Sửa lỗi

* Mô tả kí tự giờ đã đọc đúng cho kí tự conjunct trong một số ngôn ngữ tiếng Ấn độ nhất định. (#4582)
* Nếu bật tùy chọn "Sử dụng giọng đọc của ngôn ngữ để xử lý ký hiệu và ký tự", hộp thoại từ điển phát âm kí tự và kí hiệu sẽ dùng giọng đọc của ngôn ngữ đó một cách chính xác. Ngôn ngữ cho phát âm đang được chỉnh sửa cũng hiển thị trên tên của hộp thoại. (#4930)
* Trong Internet Explorer và các điều khiển MSHTML khác, các kí tự được nhập không còn bị đọc một cách tùy tiện trong các hộp xổ nhập liệu như là trường tìm kiếm của Google trong Google Chrome. (#4976)
* Khi chọn màu trong các ứng dụng của Microsoft Office, tên màu đã được thông báo. (#3045)
* Đầu ra chữ nổi tiếng Đan Mạch đã hoạt động trở lại. (#4986)
* PageUp/pageDown đã có thể dùng trở lại để thay đổi slides trong bài thuyết trình PowerPoint. (#4850)
* Trong Skype for Desktop 7.2 trở lên, đã thông báo khi đang nhập nội dung và trục trặc xảy ra ngay sau khi di chuyển focus khỏi một cuộc đàm thoại đã được sửa. (#4972)
* Sửa lỗi khi nhập một số kí hiệu / kí tự như ngoặc vuông vào ô lọc trong hộp thoại quản lý các thao tác. (#5060)
* Trong Internet Explorer và các điều khiển MSHTML khác, bấm g hay shift+g để duyệt hình ảnh giờ đây đã bao gồm các thành phần được đánh dấu là ảnh cho mục tiêu tăng tính tiếp cận (ví dụ: ARIA role img). (#5062)

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2015.1

Các cải tiến của bản phát hành này bao gồm chế độ duyệt cho tài liệu trong Microsoft Word và Outlook; các cải tiến nhỏ trong việc hỗ trợ cho Skype for Desktop; và sửa các lỗi đáng kể cho Microsoft Internet Explorer.

### Các tính năng mới

* Giờ bạn có thể thêm kí hiệu mới thông qua hộp thoại từ điển phát âm kí tự và kí hiệu. (#4354)
* Trong hộp thoại quản lý các thao tác, bạn có thể dùng trường "Lọc theo" để chỉ hiện các thao tác có chứa một số từ cụ thể. (#4458)
* NVDA giờ đây đã tự đọc các văn bản mới trong mintty. (#4588)
* Trong hộp thoại tìm kiếm ở chế độ duyệt, đã có tùy chọn để thực hiện tìm kiếm phân biệt chữ hoa / thường. (#4584)
* Di chuyển nhanh (bấm h di chuyển qua các tiêu đề, v...v...) và danh sách các thành phần (NVDA+f7) giờ đã hỗ trợ cho tài liệu Microsoft Word bằng cách bật chế độ duyệt với phím nóng NVDA+khoảng trắng. (#2975)
* Đọc các thư định dạng HTML trong Microsoft Outlook 2007 trở lên đã có các cải tiến nhỏ như chế độ duyệt đã tự động bật cho các thư này. Nếu nó không được bật trong vài tình huống ít gặp, bạn có thể bật nó bằng lệnh NVDA+khoảng trắng. (#2975)
* Tiêu đề cột của bảng trong Microsoft word giờ đã được thông báo tự động cho các bảng mà dòng tiêu đề đã được tác giả chỉ định thông qua thuộc tính bảng của Microsoft word. (#4510)
 * Tuy nhiên, với các bảng mà các dòng đã bị trộn, tính năng này sẽ không tự hoạt động. Tình huống này, bạn có thể thiết lập tiêu đề cột thủ công với NVDA+shift+c.
* Đã đọc các thông báo trong Skype for Desktop. (#4741)
* Trong Skype for Desktop, giờ bạn có thể nghe đọc và xem lại các tin nhắn gần đây bằng lệnh NVDA+control+1 đến NVDA+control+0; ví dụ: bấm NVDA+control+1 để đọc tin nhắn mới nhất và NVDA+control+0 để đọc tin nhắn thứ mười. (#3210)
* Ở một cuộc đàm thoại trong Skype for Desktop, NVDA giờ đây sẽ thông báo khi người dùng đang gõ nội dung trò chuyện. (#3506)
* Giờ đây, có thể cài đặt NVDA ở chế độ im lặng thông qua dòng lệnh và không chạy chương trình sau khi cài đặt hoàn tất. Để làm điều đó, Dùng tùy chọn --install-silent. (#4206)
* Hỗ trợ các màn hình nổi Papenmeier BRAILLEX Live 20, BRAILLEX Live và BRAILLEX Live Plus. (#4614)

### Các thay đổi

* Trong hộp thoại cài đặt định dạng tài liệu của NVDA, đã có phím tắt cho tùy chọn thông báo lỗi chính tả (alt+c). (#793)
* Giờ đây, NVDA sẽ sử dụng ngôn ngữ của bộ đọc / giọng đọc để xử lý các kí tự và kí hiệu (bao gồm tên của các dấu câu / kí hiệu), bất kể tùy chọn chuyển đổi ngôn ngữ tự động có được bật hay không. Nếu muốn tắt tính năng này để NVDA dùng lại ngôn ngữ giao diện của nó, tắt tùy chọn mới trong cài đặt giọng đọc tên gọi Sử dụng giọng đọc của ngôn ngữ để xử lý ký hiệu và ký tự. (#4210)
* Ngưng hỗ trợ bộ đọc Newfon. Giờ đây, Newfon là một add-on của NVDA. (#3184)
* Phiên bản NVDA này yêu cầu Skype for Desktop 7 trở lên; các phiên bản cũ không được hỗ trợ. (#4218)
* Việc tải các bản cập nhật của NVDA giờ đã an toàn hơn. (Cụ thể, thông tin cập nhật được thu thập qua giao thức https và các phần của tập tin được kiểm tra sau khi nó được tải về.) (#4716)
* Cập nhật eSpeak lên phiên bản 1.48.04 (#4325)

### Sửa lỗi

* Trong Microsoft Excel, các dòng và cột tiêu đề bị trộn giờ đây đã được quản lý một cách chính xác. Ví dụ, nếu A1 và B1 bị trộn thì B2 sẽ được thông báo có A1 và B1 là tiêu đề cột thay vì không thông báo gì. (#4617)
* Khi sửa nội dung ở các hộp nhập văn bản trong Microsoft PowerPoint 2003, NVDA sẽ đọc chính xác nội dung ở mỗi dòng. Trước đây, ở mỗi đoạn, các dòng cứ càng lúc càng bị mất đi một kí tự. (#4619)
* Tất cả các hộp thoại của NVDA giờ đây đều được đặt ở giữa màn hình, cải thiện trình bày trực quan và khả năng sử dụng. (#3148)
* Trong Skype for desktop, khi nhập thông điệp giới thiệu để thêm người vào danh bạ, việc nhập và di chuyển trong nội dung đã hoạt động chính xác. (#3661)
* Khi focus chuyển đến một thành phần mới ở cây thư mục trong Eclipse IDE, nếu thành phần có focus trước đó là một hộp kiểm, sẽ không còn tình trạng thông báo sai. (#4586)
* Trong hộp thoại spell check của Microsoft Word, lỗi sai tiếp theo sẽ được tự thông báo khi lỗi trước đó được sửa hay bỏ qua bằng phím tắt tương ứng. (#1938)
* Văn bản lại được đọc chính xác ở những nơi như là cửa sổ Tera Term Pro và các tài liệu trong Balabolka. (#4229)
* Giờ đây, focus đã trở về tài liệu đang soạn thảo một cách chính xác khi kết thúc nhập nội dung tiếng Hàn Quốc và các phần nhỏ ngôn ngữ châu Á khác khi soạn thảo trong một khung trên Internet Explorer và các tài liệu MSHTML khác. (#4045)
* Trong hộp thoại quản lý các thao tác, khi chọn kiểu bàn phím cho thao tác đã gán, việc bấm escape giờ đây sẽ thoát khỏi trình đơn thay vì đóng hộp thoại. (#3617)
* Khi gỡ bỏ một add-on, thư mục của add-on đó chắc chắn được xóa sau khi khởi động lại NVDA. Trước đây, bạn phải khởi động lại hai lần. (#3461)
* Sửa các lỗi nhỏ khi dùng Skype for Desktop 7. (#4218)
* Khi gửi một tin nhắn trong Skype for Desktop, không còn tình trạng đọc hai lần. (#3616)
* Trong Skype for Desktop, NVDA không còn tình trạng thỉnh thoảng đọc một lượng lớn tin nhắn (chẳng hạn như toàn bộ cuộc trò chuyện). (#4644)
* Sửa lỗi làm cho lệnh thông báo ngày / giờ của NVDA không tuân theo cài đặt ngày giờ của người dùng trong vài trường hợp(#2987)
* Trong chế độ duyệt, văn bản vô nghĩa (đôi khi bao trùm một vài dòng) không còn diễn ra với một số hình ảnh như đã tìm thấy trong Google Groups. (Cụ thể, điều này xảy ra với các ảnh mã hóa theo chuẩn base64.) (#4793)
* NVDA không còn bị đóng băng sau vài giây khi chuyển khỏi một ứng dụng của Windows Store khi mà nó bị tạm ngưng. (#4572)
* thuộc tính aria-atomic trên các vùng sống trong Mozilla Firefox giờ đây đã được tiếp thu ngay cả khi thành phần atomic tự có những thay đổi. Trước đây, nó chỉ có ảnh hưởng cho các thành phần hậu tố. (#4794)
* Chế độ duyệt sẽ phản ánh các cập nhật, và các vùng động sẽ được thông báo, với các tài liệu ở chế độ duyệt trong các ứng dụng ARIA đã nhún vào tài liệu trong Internet Explorer hay các điều khiển MSHTML khác. (#4798)
* Khi thay đổi hay thêm nội dung vào các vùng động trong Internet Explorer và các điều khiển MSHTML khác, ở những nơi mà tác giả đã quy định nội dung liên quan, chỉ các nội dung đã thay đổi hay thêm vào mới được đọc lên, thay vì đọc toàn bộ nội dung trong thành phần. (#4800)
* Nội dung được xác định bởi thuộc tính aria-labelledby trên các thành phần trong Internet Explorer và các điều khiển MSHTML khác đã thay thế chính xác các nội dung  phù hợp. (#4575)
* Khi kiểm tra chính tả trong Microsoft Outlook 2013, các từ bị lỗi giờ đây đã được thông báo. (#4848)
* Trong Internet Explorer và các điều khiển MSHTML khác, nội dung bên trong các thành phần bị ẩn với visibility:hidden không còn hiển thị ngoài ý muốn trong chế độ duyệt. (#4839, #3776)
* Trong Internet Explorer và các điều khiển MSHTML khác, thuộc tính tiêu đề trên các điều khiển biểu mẫu không còn sở hữu các liên kết nhãn khác. (#4491)
* Trong Internet Explorer và các điều khiển MSHTML khác, NVDA không còn bỏ qua các thành phần tại vị trí con trỏ do thuộc tính aria-activedescendant. (#4667)

## 2014.4

### Các tính năng mới

* Các ngôn ngữ mới: Colombian Spanish, Punjabi.
* Giờ đây, đã có thể khởi động lại NVDA hay khởi động lại NVDA và vô hiệu hóa các add-on từ hộp thoại thoát NVDA. (#4057)
 * Cũng có thể chạy NVDA ở chế độ vô hiệu hóa add-on bằng cách dùng --disable-addons trong tùy chọn dòng lệnh.
* Trong từ điển phát âm, giờ đã có thể quy định một mẫu chỉ khớp khi nó là một từ trọn vẹn; chẳng hạn, không so sánh khi nó là một bộ phận của một từ. (#1704)

### Các thay đổi

* Nếu di chuyển bằng cách duyệt đối tượng đến một đối tượng bên trong một tài liệu ở chế độ duyệt, nhưng đối tượng trước đó thì không, con trỏ duyệt sẽ tự động bật cho tài liệu. Trước đây, điều đó chỉ xảy ra nếu con trỏ duyệt đối tượng bị chuyển đi vì focus có thay đổi. (#4369)
* Danh sách các màn hình chữ nổi và bộ đọc trong các hộp thoại cài đặt giờ đây đã được sắp xếp theo bảng chữ cái, ngoại trừ không có màn hình nổi / không đọc, giờ đây được đặt ở cuối. (#2724)
* Cập nhật thư viện phiên dịch chữ nổi liblouis lên 2.6.0. (#4434, #3835)
* Trong chế độ duyệt, bấm e và shift+e để di chuyển đến các trường nhập liệu giờ đây đã bao gồm các hộp xổ nhập liệu. Điều này bao gồm ô tìm kiếm trong phiên bản mới nhất của trang tìm kiếm Google. (#4436)
* Bấm chuột trái vào biểu tượng NVDA ở vùng thông báo giờ đây sẽ mở trình đơn NVDA thay vì không làm gì. (#4459)

### Sửa lỗi

* Khi chuyển focus trở về một tài liệu trong chế độ duyệt, (ví dụ: bấm alt+tab chuyển đến một trang web đang mở), con trỏ duyệt được đặt đúng vị trí của con trỏ ảo, thay vì là vị  trí của con trỏ hệ thống. (ví dụ: một liên kết gần đó). (#4369)
* Trong trình chiếu PowerPoint, con trỏ duyệt đã đi theo con trỏ ảo một cách chính xác. (#4370)
* Trong Mozilla Firefox và các trình duyệt trên nền Gecko-based khác, nội dung trong live region sẽ được thông báo nếu nó có một loại ARIA live có thể dùng được  khác với live region cha; ví dụ: khi nội dung được đánh dấu là chắc chắn được thêm vào live region được đánh dấu là polite. (#4169)
* Trong Internet Explorer và các điều khiển MSHTML khác, trong vài trường hợp mà tài liệu nằm trong một tài liệu khác không còn ngăn chặn người dùng truy xuất một vài nội dung trong đó (cụ thể, framesets bên trong framesets). (#4418)
* NVDA không còn xảy ra lỗi khi chuẩn bị dùng một màn hình nổi Handy Tech trong vài trường hợp. (#3709)
* Trong Windows Vista, hộp thoại giả mạo tên gọi "Entry Point Not Found" không còn hiển thị trong vài trường hợp như là khi khởi động NVDA từ biểu tượng trên Desktop hoặc bằng phím nóng. (#4235)
* Các lỗi nghiêm trọng với điều khiển nhập văn bản trong các hộp thoại của các phiên bản Eclipse gần đây đã được sửa. (#3872)
* Trong Outlook 2010, việc di chuyển con trỏ giờ đây đã hoạt động như mong muốn trong trường location của appointments và meeting requests. (#4126)
* Bên trong một live region, nội dung được đánh dấu không phải là live (aria-live="off" chẳng hạn) giờ đây đã bị bỏ qua một cách chính xác. (#4405)
* Khi đọc nội dung của một thanh trạng thái có tên, tên của thanh trạng thái giờ đây đã tách rời với từ đầu tiên của nội dung thanh trạng thái đó. (#4430)
* Ở các trường nhập mật khẩu với chế độ nhập từ khi đọc được bật, không còn tình trạng đọc nhiều dấu sao khi bắt đầu đánh một từ mới. (#4402)
* Trong danh sách thư của Microsoft Outlook, các thành phần không còn bị đọc một cách vô nghĩa là thành phần dữ liệu. (#4439)
* Khi chọn văn bản trong điều khiển chỉnh sửa mã của Eclipse IDE, không còn tình trạng toàn bộ nội dung đã chọn bị đọc lên mỗi khi thay đổi lựa chọn. (#2314)
* Nhiều phiên bản của Eclipse, như là Spring Tool Suite và phiên bản được bao gồm trong Android Developer Tools bundle giờ đây đã được nhận dạng đúng là Eclipse và được quản lý một cách phù hợp. (#4360, #4454)
* Theo dõi chuột và khám phá bằng cảm ứng trong Internet Explorer và các điều khiển MSHTML khác (bao gồm nhiều ứng dụng của Windows 8) giờ đây đã hoạt động chính xác hơn trên các màn hình có điểm ảnh cao hay kích thước thu phóng của tài liệu bị thay đổi . (#3494) 
* Theo dõi chuột và khám phá bằng cảm ứng trong Internet Explorer và các điều khiển MSHTML khác giờ đây sẽ đọc nhãn của nhiều nút hơn. (#4173)
* Khi dùng một màn hình nổi của Papenmeier BRAILLEX với BrxCom, các phím trên màn hình đã hoạt động như mong muốn. (#4614)

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2014.3

### Các tính năng mới

* Có thể tắt âm thanh khởi động  và thoát NVDA thông qua một tùy chọn mới trong hộp thoại thiết lập chung. (#834)
* Có thể mở trợ giúp cho add-on từ trình quản lý Add-on nếu được cung cấp bởi tác giả. (#2694)
* Hỗ trợ cho Calendar (lịch) trong Microsoft Outlook 2007 trở lên (#2943) bao gồm:
 * Thông báo thời gian hiện tại khi di chuyển bằng các phím mũi tên.
 * thông báo nếu thời gian được chọn đang ở trong một cuộc hẹn.
 * Thông báo cuộc hẹn đã chọn khi bấm tab.
 * Lọc ngày thông minh để chỉ thông báo ngày nếu thời gian hay cuộc hẹn đã chọn ở vào một ngày khác với ngày cuối cùng.
* Cải thiện hỗ trợ cho hộp thư đến và các danh sách thư khác trong Microsoft Outlook 2010 trở lên (#3834) bao gồm:
 * Khả năng tắt đọc tiêu đề cột (người gửi, tiêu đề, v...v...) bằng cách tắt tùy chọn thông báo tiêu đề cột và dòng trong cài đặt định dạng tài liệu.
 * Khả năng dùng các lệnh điều hướng trong bảng  (control + alt + mũi tên) để chuyển đến một cột cụ thể. 
* Microsoft word: nếu một ảnh được chèn vào không có văn bản mô tả, NVDA sẽ đọc tên của ảnh nếu được tác giả cung cấp. (#4193)
* Microsoft Word: giờ đây NVDA có thể thông báo thụt lề đoạn với lệnh thông báo định dạng (NVDA+f). Nó cũng có thể tự thông báo khi thông báo thụt lề đoạn được bật trong cài đặt định dạng tài liệu. (#4165)
* Tự đọc các văn bản được tự chèn vào như bullet (tạm dịch: gạch đầu dòng), number (số thứ tự) hoặc thụt lề bằng tab khi bấm Enter trong các tài liệu hay trường nhập văn bản. (#4185)
* Microsoft word: Bấm NVDA+alt+c sẽ đọc nội dung của một chú thích nếu con trỏ đứng tại đó. (#3528)
* Cải thiện hỗ trợ cho việc tự đọc tiêu đề cột và dòng trong Microsoft Excel (#3568) bao gồm:
 * Hỗ trợ tính năng đặt tên cho vùng của Excel để xác định các ô tiêu đề (tương thích với trình đọc màn hình Jaws) .
 * Lệnh thiết lập tiêu đề cột (NVDA+shift+c) và thiết lập tiêu đề dòng (NVDA+shift+r) giờ đây lưu thiết lập vào bảng tính nên sẽ sử dụng được khi mở lại bảng tính đó và sẽ dùng được với các trình đọc màn hình có hỗ trợ đặt tên theo vùng.
 * Các lệnh này giờ đây cũng có thể dùng nhiều lần trên một bảng tính để thiết lập tiêu đề cho các vùng khác nhau.
* Hỗ trợ tự đọc tiêu đề cột và dòng trong Microsoft Word (#3110) bao gồm:
 * Hỗ trợ dấu trang của Microsoft Word để thống nhất các ô tiêu đề (tương thích với trình đọc màn hình Jaws).
 -  Dùng các lệnh thiết lập tiêu đề cột (NVDA+shift+c) và thiết lập tiêu đề dòng (NVDA+shift+r) khi đứng ở ô tiêu đề đầu tiên trong một bảng sẽ cho phép bạn thiết lập để NVDA tự đọc những tiêu đề này. Các thiết lập được lưu luôn trong tài liệu nên có thể dùng tiếp khi mở lại tài liệu này, và cũng dùng được với các trình đọc màn hình khác có hỗ trợ dấu trang.
* Microsoft Word: thông báo khoảng cách từ lề trái của trang khi bấm phím tab. (#1353)
* Microsoft Word: cung cấp phản hồi với cả bộ đọc và chữ nổi cho hầu hết các phím tắt định dạng (in đậm, in nghiêng, gạch chân, căn lề, cấp độ bố cục, chỉ số trên, chỉ số dưới và kích thước phông). (#1353)
* Microsoft Excel: nếu có chú thích trong các ô được chọn, có thể đọc chúng bằng cách bấm NVDA+alt+c. (#2920)
* Microsoft Excel: Cung cấp một hộp thoại của NVDA để chỉnh sửa chú thích ở ô hiện tại khi bấm lệnh shift+f2 của Excel để vào chế độ chỉnh sửa chú thích. (#2920)
* Microsoft Excel: phản hồi bằng giọng đọc và chữ nổi với nhiều phím tắt hơn để chọn và di chuyển (#4211) including:
 * Chuyển trang dọc (pageUp và pageDown);
 * Chuyển trang ngang (alt+pageUp và alt+pageDown);
 * Mở rộng vùng chọn (các phím tên và thêm phím Shift); và
 * Chọn vùng hiện tại (control+shift+8).
* Microsoft Excel: có thể đọc thông tin căn chỉnh ô theo chiều ngang và dọc bằng lệnh thông báo định dạng (NVDA+f). Nó cũng có thể tự đọc nếu bật tùy chọn thông báo căn lề trong cài đặt định dạng tài liệu. (#4212)
* Microsoft Excel: có thể xem kiểu dáng của một ô với lệnh thông báo định dạng (NVDA+f). Nó cũng có thể tự đọc nếu bật tùy chọn thông báo kiểu dáng trong cài đặt dịnh dạng tài liệu. (#4213)
* Microsoft PowerPoint: khi di chuyển ảnh quanh một slide bằng các phím mũi tên, vị trí hiện tại của ảnh giờ đây đã được thông báo (#4214) bao gồm:
 * Thông báo khoảng cách giữa ảnh và mỗi lề của slide.
 * Nếu một ảnh đang che hay bị che bởi một ảnh khác, khoảng cách sẽ bị tràn và ảnh nào bị tràn sẽ được thông báo.
 * Để xem thông tin này bất cứ lúc nào mà không phải di chuyển ảnh, bấm lệnh thông báo vị trí con trỏ duyệt (NVDA+delete).
 * Khi chọn một ảnh, nếu nó bị che bởi một ảnh khác, NVDA sẽ thông báo rằng nó bị khuất.
* Lệnh thông báo vị trí con trỏ (NVDA+delete) sẽ hoạt động chính xác trong nhiều ngữ cảnh của nhiều tình huống hơn. (#4219)
 * trong các trường nhập liệu chuẩn và chế độ duyệt, vị trí con trỏ theo tỉ lệ phần trăm của nội dung và tọa độ của nó đã được thông báo.
 * Trên các ảnh trong bài trình chiếu PowerPoint, vị trí của ảnh liên quan đến slide và các ảnh khác đã được thông báo.
 * Bấm lệnh này hai lần sẽ trình bày kiểu thông báo thông tin vị trí trước đây cho toàn bộ điều khiển.
* Ngôn ngữ mới: Catalan.

### Các thay đổi

* Cập nhật thư viện phiên dịch chữ nổi liblouis lên phiên bản 2.5.4. (#4103)

### Sửa lỗi

* Trong Google Chrome và các trình duyệt trên nền tảng Chrome, một số đoạn văn bản nhất định (như văn bản được nhấn mạnh) không còn bị lặp lại khi đọc nội dung của một thông báo hay hộp thoại. (#4066)
* Ở chế độ duyệt trong các ứng dụng của Mozilla, bấm enter tại một nút, v...v... không còn tình trạng không kích hoạt được (hay kích hoạt sai) trong vài trường hợp nhất định như nút bấm ở đầu trang Facebook. (#4106)
* Không còn đọc các thông tin vô ích khi bấm tab trong iTunes. (#4128)
* Ở một số danh sách nhất định trong iTunes như danh sách nhạc, việc chuyển tới mục kế bằng phương pháp duyệt đối tượng giờ đây đã làm việc chính xác. (#4129)
* Các thành phần HTML đã xem xét các tiêu đề vì WAI ARIA markup đã được tích hợp trong danh sách các thành phần và phím di chuyển nhanh ở chế độ duyệt cho tài liệu trong Internet Explorer. (#4140)
* Các liên kết cùng trang  trong những phiên bản gần đây của Internet Explorer giờ đây đã di chuyển chính xác và thông báo vị trí đích trong tài liệu ở chế độ duyệt. (#4134)
* Microsoft Outlook 2010 trở lên: nhìn chung, việc truy cập các hộp thoại bảo mật như các hộp thoại New profiles và mail setup đã được cải thiện. (#4090, #4091, #4095)
* Microsoft Outlook: giảm bớt sự rườm rà trong các lệnh của thanh công cụ khi điều hướng qua một số hộp thoại nhất định. (#4096, #3407)
* Microsoft word: bấm tab đến một ô rỗng trong một bảng không còn bị thông báo sai là thoát khỏi bảng. (#4151)
* Microsoft Word: kí tự đầu tiên sau dòng cuối bảng (bao gồm dòng trống) không còn bị hiểu sai là đang ở trong bảng. (#4152)
* Hộp thoại spell Check của Microsoft Word 2010: đã thông báo từ sai chính tả hiện tại thay vì chỉ thông báo từ đầu tiên. (#3431)
* Ở chế độ duyệt trong Internet Explorer và các điều khiển MSHTML khác, bấm tab hay dùng các kí tự di chuyển nhanh để đến các biểu mẫu đã thông báo lại nhãn trong nhiều trường hợp mà trước đây không thông báo (cụ thể, thành phần nhãn HTML được sử dụng). (#4170)
* Microsoft Word: thông báo chính xác hơn các chú thích đã tồn tại và bị thay thế. (#3528)
* Điều hướng qua một số hộp thoại nhất định trong bộ MS Office như Word, Excel và Outlook đã được cải thiện bằng cách không thông báo một vài điều khiển cụ thể không có lợi cho người dùng. (#4198) 
* các bản tác vụ như quản lý bộ nhớ tạm hay phục hồi tập tin không còn bị chuyển focus đến ngoài ý muốn khi mở một ứng dụng như Microsoft Word hoặc Excel, trước đây điều đó thỉnh thoảng khiến người dùng phải chuyển qua cửa sổ khác rồi trở về cửa sổ ứng dụng.  (#4199)
* NVDA không còn xảy ra lỗi khi chạy trên các phiên bản Windows gần đây nếu ngôn ngữ người dùng được thiết lập là Serbian (Latin). (#4203)
* Bấm phím numlock khi bật trợ giúp nhập giờ đây đã bật / tắt numlock thay vì làm cho hệ thông và bàn phím trở nên không đồng bộ  ở trạng thái của phím này. (#4226)
* Trong Google Chrome, tiêu đề của tài liệu lại được đọc khi chuyển qua các thẻ. Trong NVDA 2014.2, chức năng này không hoạt động trong vài trường hợp. (#4222)
* Trong Google Chrome và các trình duyệt trên nền tảng Chrome, URL của tài liệu không còn bị đọc khi đọc tài liệu. (#4223)
* Khi dùng chức năng đọc tất cả mà không chọn bộ đọc nào (có tác dụng trong việc kiểm tra tự động), chế độ này sẽ hoạt động bình thường thay vì ngừng ở vài dòng đầu tiên. (#4225)
* Hộp thoại Signature của Microsoft Outlook: trường chỉnh sửa chữ kí (signature editting) giờ đây đã tiếp cận được, cho phép theo dõi con trỏ và định dạng. (#3833)
* Microsoft Word: khi đọc dòng cuối cùng của một bảng, toàn bộ bảng không còn bị đọc lên nữa. (#3421)
* Microsoft Word: khi đọc dòng đầu hay cuối của mục lục, toàn bộ trang mục lục không còn bị đọc lên nữa. (#3421)
* Khi đọc các từ đã nhập và trong vài trường hợp khác, các từ không còn bị lỗi ở một số dấu như kí tự nguyên âm và virama trong các ngôn ngữ tiếng Ấn độ. (#4254)
* Các trường nhập số trong GoldWave giờ đã được quản lý một cách chính xác. (#670)
* Microsoft Word: khi di chuyển qua đoạn với control+mũi tên xuống / control+mũi tên lên, không cần phải bấm hai lần nếu di chuyển qua các danh sách không và có thứ tự. (#3290)

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2014.2

### Các tính năng mới

* Việc thông báo chọn văn bản đã có thể thực hiện trong vài trường nhập liệu tùy chỉnh sử dụng thông tin hiện thị. (#770)
* Trong các ứng dụng tiếp cận được của Java, thông tin vị trí đã được thông báo cho nút radio và các điều khiển khác hiển thị theo nhóm. (#3754)
* Trong các ứng dụng tiếp cận được của Java, các phím tắt đã được thông báo  cho các điều khiển có phím tắt. (#3881)
* Trong chế độ duyệt, nhãn trên các cột mốc đã được dọc. Chúng cũng được tích hợp trong hộp thoại danh sách các thành phần. (#1195)
* Trong chế độ duyệt, các vùng đã gán nhãn giờ đây được xem như các cột mốc. (#3741)
* Trong các tài liệu và ứng dụng Internet Explorer, Live Regions (một bộ phận của chuẩn W3c ARIA) đã được hỗ trợ, vậy nên người làm web được phép đánh dấu các nội dung cụ thể sẽ tự đọc khi có sự thay đổi. (#1846)

### Các thay đổi

* Khi thoát khỏi một hộp thoại hay ứng dụng trong một tài liệu ở chế độ duyệt, không còn đọc tên và kiểu tài liệu ở chế độ duyệt. (#4069)

### Sửa lỗi

* Trình đơn hệ thống chuẩn không còn bị im lặng ngoài ý muốn trong các ứng dụng Java. (#3882)
* Khi chép văn bản ở chế độ duyệt màn hình, không còn tình trạng bỏ qua các dấu xuống dòng. (#3900)
* Các đối tượng rỗng vô nghĩa không còn dược thông báo trong vài ứng dụng khi thay đổi focus hay khi dùn phương pháp duyệt đối tượng với chế độ xem đơn giản được bật. (#3839)
* Các hộp thông điệp và hộp thoại khác của NVDA lại tiếp tục hủy bỏ các thông điệp đang đọc trước đó rồi mới đọc nội dung của hộp thoại.
* Trong chế độ duyệt, nhãn của các điều khiển như liên kết và nút đã được thông báo một cách chính xác khi mà chúng bị viết đè bởi tác giả cho mục tiêu tiếp cận (Cụ thể, dùng nhãn aria-label hay aria-labelledby). (#1354)
* Ở chế độ duyệt trong  Internet Explorer, nội dung chứa trong thành phần được đánh dấu là presentational (ARIA role="presentation") không còn bị bỏ qua một cách không hợp lý. (#4031)
* Lại tiếp tục gõ được văn bản tiếng Việt với phần mềm UniKey. Để làm điều đó, bỏ chọn mục Quản lý phím từ ứng dụng khác trong hộp thoại cài đặt bàn phím của NVDA. (#4043)
* Trong chế độ duyệt, các thành phần trình đơn dạng radio và check đã được thông báo là một điều khiển thay vì chỉ thông báo là văn bản có thể kích hoạt. (#4092)
* NVDA không còn chuyển từ chế độ focus sang chế độ duyệt một cách không chính xác khi đứng tại một thành phần dạng radio hay trình đơn dạng check. (#4092)
* Trong Microsoft PowerPoint với chế độ đọc từ khi nhập được bật, kí tự bị xóa bởi phím xóa lùi không còn bị đọc như một bộ phận của từ đã nhập. (#3231)
* Trong hộp thoại Options của Microsoft Office 2010, nhãn của các hộp xổ đã được đọc chính xác. (#4056)
* Ở chế độ duyệt trong các ứng dụng của Mozilla, dùng các lệnh di chuyển nhanh để chuyển tới nút, biểu mẫu kế hay nút, biểu mẫu trước đã bao gồm việc bật / tắt các nút như mong đợi. (#4098)
* Nội dung các bản thông báo trong ứng dụng của  Mozilla không còn bị đọc  hai lần. (#3481)
* Trong chế độ duyệt, container và các cột mốc  không còn bị lặp lại ngoài ý muốn khi  di chuyển bên trong chúng mà cùng lúc nội dung trang có sự thay đổi (ví dụ: di chuyển trong các trang Facebook và Twitter). (#2199)
* NVDA được phục hồi trong nhiều trường hợp khi chuyển cửa sổ đi khỏi các ứng dụng bị treo. (#3825)
* Con trỏ (điểm chèn) lại dược cập nhật một cách chính xác khi dùng lệnh đọc tất cả ở một ô nhập văn bản trực tiếp vào màn hình. (#4125)

## 2014.1

### Các tính năng mới

* Hỗ trợ cho Microsoft PowerPoint 2013. Lưu ý là chưa hỗ trợ cho dạng xem bảo vệ. (#3578)
* Trong Microsoft word và Excel, NVDA có thể đọc các ki hiệu được chọn khi dùng hộp thoại Insert Symbols. (#3538)
* Giờ đã có thể thiết lập để NVDA xác định một đối tượng trong nội dung là có thể kích hoạt thông qua hộp thoại cài đặt định dạng tài liệu. Tùy chọn này mặc định được bật để chương trình hoạt động như các phiên bản trước. (#3556)
* Hỗ trợ các màn hình nổi được kết nối thông qua Bluetooth trên một máy tính đang chạy phần mềm Widcomm Bluetooth Software. (#2418)
* Khi chỉnh sửa văn bản trong PowerPoint, siêu liên kết đã được thông báo. (#3416)
* Khi ở trong các ứng dụng hay hộp thoại ARIA trên web, giờ đã có thể buộc NVDA chuyển sang chế độ duyệt với lệnh NVDA+khoảng trắng cho phép duyệt qua các kiểu tài liệu hay hộp thoại. (#2023)
* Trong Outlook Express / Windows Mail / Windows Live Mail, NVDA giờ đây đã thông báo khi thư có tệp đính kèm hay bị gắn cờ. (#1594)
* Khi duyệt qua bảng biểu trong các ứng dụng Java tiếp cận dược, tọa độ cột và dòng đã được thông báo, bao gồm tiêu đề cột và dòng nếu có. (#3756)

### Các thay đổi

* Với các màn hình nổi của Papenmeier, các lệnh chuyển đến flat review/focus đã bị gỡ bỏ. Người dùng có thể gán phím tắt của riêngn mình thông qua hộp thoại quản lý các thao tác. (#3652)
* NVDA giờ đây dựa trên Microsoft VC runtime phiên bản 11, nghĩa là nó có thể không còn chạy được trên các hệ điều hành cũ hơn Windows XP Service Pack 2 hay Windows Server 2003 Service Pack 1.
* cấp độ đọc dấu câu một vài sẽ đọc dấu sao (*) và dấu cộng (+). (#3614)
* Cập nhật eSpeak lên phiên bản 1.48.04, bao gồm sửa lỗi cho nhiều ngôn ngữ. (#3842, #3739, #3860)

### Sửa lỗi

* Khi di chuyển hay chọn ô trong Microsoft Excel, NVDA không còn đọc các ô cũ thay vì là ô mới khi Microsoft Excel di chuyển đến ô đã chọn một cách chậm chạp. (#3558)
* NVDA đã quản lý một cách chính xác danh sách thả xuống của một ô trong Microsoft Excel thông qua trình đơn ngữ cảnh. (#3586)
* Các trang mới trong cửa hàng iTunes 11 đã hiển thị chính xác trong chế độ duyệt khi theo một liên kết trong cửa hàng hoặc khi mở cửa hàng lúc đầu. (#3625)
* Các nút để nghe thử bài hát trong  cửa hàng iTunes 11 giờ đây đã hiển thị nhãn của chúng trong chế độ duyệt. (#3638)
* Ở chế độ duyệt của Google Chrome, nhãn của các hộp kiểm  và nút radio giờ đã được đưua ra một cách chính xác. (#1562)
* Trong Instantbird, NVDA không còn đọc các thông tin vô ích mỗi khi di chuyển đến một liên lạc trong danh bạ. (#2667)
* Ở chế độ duyệt trong Adobe Reader, đã nhận ra đúng nội dung văn bản cho các nút, v...v... trong khi nhãn của chúng đã bị ghi đè bởi  một thông báo chẳng hạn. (#3640)
* Ở chế độ duyệt trong Adobe Reader, các hình ảnh không liên quan có chứa cụm văn bản "mc-ref" sẽ không bị xuất ra nữa. (#3645)
* NVDA không còn thông báo tất cả ô trong Microsoft Excel là đã gạch dưới trong thông tin định dạng của nó. (#3669)
* Không còn hiện những kí tự vô nghĩa trong các tài liệu ở chế độ duyệt như đã tìm thấy trong phạm vi sử dụng riêng của Unicode. Trong vài trường hợp, chúng đã làm cho nhiều nhãn hữu ích không hiển thị được. (#2963)
* Phương thức nhập cho các kí tự east-asian không còn bị lỗi trong PuTTY. (#3432)
* Di chuyển trong một tài liệu sau khi hủy lệnh đọc tất cả không còn làm cho NVDA thỉnh thoảng thông báo rằng bạn vừa rời khỏi một trường (như một bảng biểu) phần còn lại của tài liệu mà chức năng đọc tất cả chưa đọc đến. (#3688)
* Dùng các lệnh di chuyển nhanh trong chế độ duyệt  khi ở chế độ tất cả với chế độ cho phép thay đổi vị trí trong khi đọc được bật, NVDA thông báo chính xác hơn các trường mới; ví dụ: nó sẽ đọc một tiêu đề là tiêu đề, thay vì chỉ đọc nội dung của tiêu đề đó. (#3689)
* Các lệnh di chuyển nhanh để đi đến đầu hay cuối thành phần giờ đây đã tuân theo thiết lập thay đổi vị trí trong khi đọc; ví dụ: nó sẽ không bị hủy trong khi đọc tất cả. (#3675)
* Tên của các thao tác cảm ứng được liệt kê trong hộp thoại quản lý các thao tác của NVDA đã được đặt một cách thân thiện và đã có thể bản địa hóa. (#3624)
* NVDA không còn làm cho vài chương trình nhất định bị treo khi di chuyển chuột qua các điều khiển soạn thảo (TRichEdit) của chúng. Các chương trình bao gồm Jarte 5.1 và BRfácil. (#3693, #3603, #3581)
* Trong Internet Explorer và các điều khiển MSHTML khác, các thành phần như bảng được đánh dấu là trình chiếu bởi ARIA không còn bị thông báo đến người dùng. (#3713)
* Trong Microsoft Word, NVDA không còn lặp lại thông tin cột và dòng của một ô nhiều lần trên màn hình nổi. (#3702)
* Trong các ngôn ngữ dùng khoảng trắng để ngăn cách các chữ số như tiếng Pháp và Đức, các nội dung số từ các phần được chia nhỏ không còn bị đọc là một số đơn lẻ. Điều này đặc biệt đã xảy ra cho các ô có chứa số trong bảng biểu. (#3698)
* Chữ nổi không còn bị lỗi cập nhật khi dấu nháy hệ thống bị di chuyển trong Microsoft Word 2013. (#3784)
* Khi con trỏ ở tại kí tự đầu tiên của  một tiêu đề trong Microsoft Word, không còn tình trạng không hiển thị nội dung thông báo đây là tiêu đề (bao gồm cấp độ của tiêu đề) trên màn hình chữ nổi. (#3701)
* Khi hồ sơ cấu hình là tác nhân cho một ứng dụng và ứng dụng đó đã tắt, NVDA không còn thỉnh thoảng bị lỗi không bỏ kích hoạt được hồ sơ. (#3732)
* Khi nhập các kí tự châu Á vào một điều khiển của chính NVDA (ví dụ: hộp thoại tìm kiếm trong chế độ duyệt), "NVDA" không còn thông báo một cách không chính xác vị trí của candidate. (#3726)
* Các thẻ trong hộp thoại options của Outlook 2013 giờ đây đã được đọc. (#3826)
* Cải thiện hỗ trợ cho ARIA live regions trong Firefox và các ứng dụng Mozilla Gecko khác:
 * Hỗ trợ các cập nhật aria-atomic và cập nhật bộ lọc của aria-busy. (#2640)
 * Văn bản thay thế (như alt attribute hay aria-label) đã được bao gồm nếu chúng không có các văn bản hữu ích khác. (#3329)
 * Các cập nhật live region không còn bị im lặng nếu xuất hiện cùng lúc với focus bị di chuyển. (#3777)
* Một số thành phần trình chiếu nhất định trong Firefox và các ứng dụng Mozilla Gecko khác không còn hiển thị ngoài ý muốn ở chế độ duyệt (cụ thể, khi thành phần được đánh dấu là aria-presentation nhưng nó cũng đang có focus). (#3781)
* Cải thiện vận hành khi điều hướng trong một tài liệu trong Microsoft Word với chế độ kiểm tra chính tả được bật. (#3785)
* Vài sửa lỗi trong việc hỗ trợ cho các ứng dụng tiếp cận của Java:
 * Điều khiển có focused ban đầu trong một khung hoặc hộp thoại không còn bị lỗi không được thông báo khi khung hay hộp thoại hiển thị dạng forground. (#3753)
 * Các thông tin vị trí vô ích không còn được thông báo cho các nút radio (ví dụ: 1 của 1). (#3754)
 * Đọc tốt hơn với điều khiển JComboBox (không còn đọc cho html, đọc tốt hơn với trạng thái đã mở rộng (expanded) và thu nhỏ (collapsed)). (#3755)
 * Khi đọc văn bản trên các hộp thoại, đã bao gồm vài nội dung bị bỏ sót trước đây. (#3757)
 * Các thay đổi đến tên, giá trị hay mô tả của focused control giờ đây đã được thông báo chính xác hơn. (#3770)
* Sửa lỗi của NVDA tìm thấy trong Windows 8 khi đứng tại một số điều khiển nhập liệu nhất định có chứa nhiều nội dung văn bản (ví dụ: xem log của NVDA, windbg). (#3867)
* Trên các hệ thống với một màn hình có cài đặt điểm ảnh cao (thường thấy ở nhiều màn hình hiện đại), NVDA không còn đưa chuột đi sai vị trí trong vài ứng dụng. (#3758, #3703)
* Sửa một lỗi ít gặp khi lướt web làm cho NVDA bị dừng cho đến khi khởi động lại, ngay cả khi nó không bị treo hay đóng băng. (#3804)
* Giờ đã có thể dùng màn hình nổi dòng Papenmeier ngay cả khi màn hình này chưa bao giờ được kết nối qua USB. (#3712)
* NVDA không còn bị đóng băng khi chọn một mẫu cũ của màn hình nổi Papenmeier BRAILLEX mà không kết nối màn hình đó vào.

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2013.3

### các tính năng mới

* Các biểu mẫu giờ đây đã được đọc trong các tài liệu  của Microsoft word. (#2295)
* NVDA giờ đây đã có thể thông báo các thông tin bản sửa biên tập trong Microsoft Word khi bật Track Changes. Lưu ý là phải bật thông báo Các bản sửa biên tập trong hộp thoại cài đặt định dạng tài liệu của NVDA (mặc định không được bật). (#1670)
* Danh sách thả xuống trong Microsoft Excel 2003 đến 2010 đã được thông báo khi mở và di chuyển trong tập tin. (#3382)
* Tùy chọn mới: 'cho phép thay đổi vị trí trong khi đọc tất cả' trong hộp thoại cài đặt bàn phím cho phép di chuyển qua một tài liệu với các phím di chuyển nhanh trong chế độ duyệt, và các lệnh di chuyển theo dòng hay đoạn khi vẫn đang trong chế độ đọc tất cả. Mặc định, tính năng này không được bật. (#2766) 
* Giờ đây, đã có hộp thoại quản lý các cử chỉ cho phép tùy chỉnh  các thao tác một cách dễ dàng hơn (như các phím trên bàn phím) cho những lệnh của NVDA. (#1532)
* Giờ bạn có thể thực hiện các cài đặt khác nhau cho các tình huống khác nhau thông qua hồ sơ cấu hình. Các hồ sơ có thể được kích hoạt thủ công hoặc tự động (ví dụ: kích hoạt cho một ứng dụng cụ thể). (#87, #667, #1913)
* Trong Microsoft Excel, các ô là liên kết đã được thông báo là liên kết. (#3042)
* Trong Microsoft Excel, bình luận có sẵn trên một ô giờ đây đã được thông báo đến người dùng. (#2921)

### sửa lỗi

* Zend Studio giờ đã hoạt động như Eclipse. (#3420)
* trạng thái các thay đổi của một số hộp kiểm nhất định trong hộp thoại message rules của Microsoft Outlook 2010 đã được tự đọc. (#3063)
* NVDA giờ đây sẽ đọc trạng thái pinned cho các điều khiển pinned như các tab trong Mozilla Firefox. (#3372)
* giờ đã có thể gán kịch bản cho các thao tác bàn phím có các phím Alt và Windows như phím bổ trợ. Trước đây, nếu làm điều đó thì khi thực hiện kịch bản sẽ làm cho Start Menu hay thanh trình đơn bị kích hoạt. (#3472)
* Chọn văn bản trong tài liệu ở chế độ duyệt (ví dụ: dùng control+shift+end) không còn làm cho kiểu bàn phím bị chuyển đổi trên các hệ thống đã cài đặt nhiều kiểu bàn phím. (#3472)
* Internet Explorer không còn bị lỗi hay trở nên vô dụng khi đóng NVDA. (#3397)
* Việc dịch chuyển và các sự kiện khác trên vài máy tính mới không còn bị coi là đã bấm các phím ngoài ý muốn. Trước đây, nó sẽ làm ngưng bộ đọc và đôi khi thực hiện các lệnh của NVDA. (#3468)
* NVDA giờ đã hoạt động như ý muốn trong Poedit 1.5.7. Người dùng các phiên bản cũ hơn sẽ phải cập nhật. (#3485)
* NVDA giờ đây có thể đọc các tài liệu ở dạng xem bảo vệ trong Microsoft Word 2010,  không còn làm cho Microsoft Word bị lỗi. (#1686)
* Nếu dùng một dòng lệnh không xác định khi chạy gói NVDA distribution, không còn sinh ra một vòng lặp vô tận các hộp thoại thông điệp báo lỗi. (#3463)
* NVDA không còn bị lỗi khi đọc văn bản thay thế cho các ảnh và đối tượng trong Microsoft Word nếu chúng có các dấu nháy kép hay các kí tự không phải tiêu chuẩn. (#3579)
* Số thành phần của một số danh sách nằm ngang trong chế độ duyệt giờ đã hoạt động chính xác. Trước đó nó có thể nhận đôi các thành phần. (#2151)
* Khi bấm control+a trong một bảng tính của Microsoft Excel, các vùng chọn đã cập nhật sẽ được thông báo. (#3043)
* NVDA giờ đây đã có thể đọc chính xác các tài liệu XHTML trong Microsoft Internet Explorer và các điều khiển MSHTML khác. (#3542)
* Hộp thoại cài đặt bàn phím: nếu không có phím nào được chọn làm phím bổ trợ NVDA, sẽ thông báo lỗi đến người dùng khi đóng hộp thoại. Phải chọn tối thiểu một phím làm phím bổ trợ. (#2871)
* Trong Microsoft Excel, NVDA giờ sẽ thông báo các ô đã trộn khác với thông báo nhiều ô đã được chọn. (#3567)
* Con trỏ trong chế độ duyệt không còn bị đặt sai vị trí khi rời khỏi một hộp thoại hay ứng dụng bên trong tài liệu. (#3145)
* Sửa lỗi làm cho driver các màn hình nổi của HumanWare Brailliant dòng BI/B không được hiển thị như một tùy chọn trong hộp thoại cài đặt chữ nổi trên vài hệ thống, ngay khi chúng được kết nối qua cổng USB.
* NVDA không còn bị lỗi không chuyển được sang chế độ duyệt màn hình khi con trỏ duyệt đối tượng không đứng chính xác ở vị trí màn hình. Trường hợp này, con trỏ duyệt sẽ được đặt ở trên cùng của màn hình. (#3454)
* Sửa lỗi driver màn hình nổi của Freedom Scientific khi chọn cổng kết nối là USB trong vài trường hợp. (#3509, #3662)
* Sửa lỗi không nhận được phím trên các màn hình chữ nổi của Freedom Scientific  trong vài trường hợp. (#3401, #3662)

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2013.2

### Các tính năng mới

* Hỗ trợ Chromium Embedded Framework, là một điều khiển trình duyệt web được dùng trong vài ứng dụng. (#3108)
* Biến thể mới cho giọng đọc eSpeak: Iven3.
* Trong Skype, các nội dung chat mới được đọc tự động khi đứng tại cuộc trò chuyện. (#2298)
* Hỗ trợ cho Tween, bao gồm đọc tên các tab và giảm độ chi tiết khi đọc tweet.
* Giờ bạn có thể vô hiệu hóa việc hiển thị thông điệp của NVDA trên màn hình chữ nổi bằng cách thiết lập thời gian cho thông điệp thành 0 trong hộp thoại cài đặt chữ nổi. (#2482)
* Trong Trình Quản Lý Add-on, giờ đã có nút xem và tải các add-on để mở trang web Add-on của NVDA, nơi bạn có thể tìm và tải các add-on. (#3209)
* Trong hộp thoại chào mừng của NVDA luôn hiển thị ở lần khởi động NVDA đầu tiên, bạn có thể thiết lập để NVDA tự khởi động sau khi đăng nhập vào Windows. (#2234)
* Chế độ ngủ được bật tự động khi dùng Dolphin Cicero. (#2055)
* Phiên bản Windows x64 của Miranda IM/Miranda NG giờ đã được hỗ trợ. (#3296)
* Các gợi ý tìm kiếm trong  Start Screen của Windows 8.1 đã được đọc tự động. (#3322)
* Hỗ trợ duyệt và chỉnh sửa các bảng tính trong Microsoft Excel 2013. (#3360)
* Các màn hình nổi Focus 14 Blue và Focus 80 Blue của Freedom Scientific, luôn cả Focus 40 Blue trong vài cấu hình nhất định mà trước đây không được hỗ trợ, giờ đã được hỗ trợ khi kết nối qua Bluetooth. (#3307)
* Các gợi ý tự động hoàn tất giờ đã được đọc trong Outlook 2010. (#2816)
* Các bản dịch chữ nổi mới: tiếng Anh (Anh) chữ nổi máy tính, Hàn quốc cấp 2, chữ nổi máy tính tiếng Nga.
* Ngôn ngữ mới: Farsi. (#1427)

### Các thay đổi

* trên một màn hình cảm ứng, thực hiện thao tác vuốt một ngón qua trái hay phải khi trong chế độ đối tượng giờ đây sẽ di chuyển lùi hay tới tất cả các đối tượng chứ không chỉ di chuyển trong đối tượng chứa. Vuốt hai ngón tay qua trái hay phải để thực hiện hành động nguyên thủy của việc di chuyển đến đối tượng trước hay kế trong đối tượng chứa hiện tại.
* Hộp kiểm Thông báo kiểu bảng trong hộp thoại cài đặt chế độ duyệt giờ đã được đổi tên thành Bao gồm kiểu bảng để thể hiện rằng việc di chuyển nhanh cũng không định vị chúng nếu không đánh dấu chọn hộp kiểm này. (#3140)
* Flat review đã được thay thế với chế độ duyệt đối tượng, duyệt tài liệu và duyệt màn hình. (#2996)
 * Duyệt đối tượng chỉ xem nội dung ở đối tượng điều hướng, duyệt tài liệu xem tất cả nội dung trong tài liệu ở chế độ duyệt (nếu có) và duyệt màn hình xem nội dung màn hình của ứng dụng hiện tại.
 * Những lệnh di chuyển trước đây của flat review giờ đây sẽ chuyển giữa các chế độ duyệt mới này.
 * Đối tượng điều hướng sẽ tự đi theo con trỏ duyệt như vẫn còn đối tượng sâu nhất tại vị trí của con trỏ duyệt khi ở trong chế độ duyệt tài liệu hoặc duyệt màn hình.
 * Sau khi chuyển sang chế độ duyệt màn hình, NVDA sẽ ở chế độ này cho đến khi bạn chủ động chuyển về chế độ duyệt tài liệu hay duyệt đối tượng.
 * Khi trong chế độ duyệt tài liệu hay duyệt đối tượng, NVDA có thể tự chuyển giữa hai chế độ này, tùy thuộc vào việc bạn có đang di chuyển trong tài liệu ở chế độ duyệt hay không.
* Cập nhật thư viện phiên dịch chữ nổi liblouis lên phiên bản 2.5.3. (#3371)

### Sửa lỗi

* Việc kích hoạt một đối tượng sẽ thông báo hoạt động trước khi thực hiện hoạt động đó, thay vì thông báo sau (ví dụ: mở rộng khi đang mở rộng thay vì thu hẹp). (#2982)
* Đọc và thông báo con trỏ chính xác hơn trong nhiều trường nhập liệu của những phiên bản Skype gần đây như trường tìm kiếm và trò chuyện. (#1601, #3036)
* Trong danh sách trò chuyện gần đây của Skype, số sự kiện mới đã được đọc cho mỗi cuộc trò chuyện nếu có. (#1446)
* Cải thiện khả năng theo dõi và thứ tự đọc con trỏ cho việc đọc văn bản từ phải sang trái trên màn hình; ví dụ: chỉnh sửa văn bản tiếng Ả rập với Microsoft Excel. (#1601) 
* Di chuyển nhanh tới các nút và biểu mẫu sẽ xác định các liên kết được đánh dấu là nút cho mục tiêu tiếp cận trong Internet Explorer. (#2750)
* Ở chế độ duyệt, nội dung trong cây thư mục không còn bị trích xuất như đại diện phẳng không hữu dụng. Bạn có thể bấm enter tại một cây thư mục để tương tác với nó ở chế độ focus. (#3023)
* Bấm alt+mũi tên xuống hay alt+mũi tên lên để mở rộng một hộp xổ khi ở chế độ focus không còn tình trạng chuyển sang chế độ duyệt. (#2340)
* Trong Internet Explorer 10, các ô trong bảng không còn kích hoạt chế độ focus, trừ khi chúng được nhà phát triển web làm cho có focus. (#3248)
* NVDA không còn bị lỗi không khởi động được  khi thời gian hệ thống là sớm hơn thời gian của lần cập nhật cuối cùng. (#3260)
* Nếu có thanh tiến trình hiển thị trên màn hình chữ nổi, màn hình chữ nổi sẽ được cập nhật khi thanh tiến trình có thay đổi. (#3258)
* Ở chế độ duyệt trong các ứng dụng của Mozilla, các chú thích cho bảng không còn bị trích xuất hai lần. Thêm nữa, tóm tắt cũng được hiển thị khi có chú thích. (#3196)
* Khi thay đổi ngôn ngữ đầu vào trong Windows 8, NVDA giờ đây đã đọc ngôn ngữ chính xác thay vì là ngôn ngữ trước đó.
* NVDA giờ đây đã thông báo các chế độ thay đổi của IME conversion trong Windows 8.
* NVDA không còn các thông báo rác trên Desktop khi dùng phương thức nhập là Google tiếng Nhật hay Atok IME. (#3234)
* Trong Windows 7 và cao hơn, NVDA không còn thông báo một cách bất hợp lý rằng nhận dạng giọng nói hay nhập liệu cảm ứng là một thay đổi ngôn ngữ bàn phím.
* NVDA không còn đọc kí tự đặc biệt (0x7f) khi bấm control+xóa lùi trong vài trình soạn thảo với chế độ đọc kí tự khi gõ được bật. (#3315)
* eSpeak không còn thay đổi cao độ, âm lượng, v...v.... ngoài ý muốn khi NVDA đọc các nội dung có chứa một số kí tự điều khiển nhất định hay XML. (#3334) (hồi quy của #437)
* Trong các ứng dụng Java, các thay đổi của nhãn hay giá trị của điều khiển có focus giờ đã được tự đọc, và được phản ánh khi truy vấn điều khiển sau đó. (#3119)
* Trong các điều khiển của Scintilla, dòng giờ đây đã được đọc chính xác khi bật word wrap. (#885)
* Trong các ứng dụng của Mozilla, tên các thành phần trong danh sách có thuộc tính chỉ đọc giờ đây đã được thông báo chính xác; ví dụ: khi duyệt các tweet ở chế độ focus trên twitter.com. (#3327)
* Nội dung các hộp thoại xác nhận trong Microsoft Office 2013 giờ đây đã được tự đọc khi chúng xuất hiện. 
* Cải thiện khả năng vận hành khi duyệt qua một số bảng nhất định trong Microsoft Word. (#3326)
* Các lệnh duyệt bảng của NVDA (control+alt+mũi tên) hoạt động tốt hơn trong một số bảng nhất định của Microsoft Word mà một ô bao gồm nhiều dòng.
* Nếu đang mở hộp thoại Quản lý các Add-on, việc mở lại nó (từ trình đơn công cụ hoặc mở một tập tin add-on), không còn bị lỗi hoặc không thể đóng hộp thoại Quản lý các Add-on. (#3351)
* NVDA không còn bị treo trong một số hộp thoại nhất định khi dùng Office 2010 IME tiếng Nhật hay tiếng Trung Quốc. (#3064)
* Nhiều khoảng trắng không còn bị gom lại thành một trên các màn hình chữ nổi. (#1366)
* Các công cụ Zend Eclipse PHP giờ đây đã hoạt động giống như Eclipse. (#3353)
* Trong Internet Explorer, lại không cần phải bấm tab để tương tác với một đối tượng nhún. (như nội dung Flash) sau khi bấm enter tại đó. (#3364)
* Khi soạn thảo nội dung trong Microsoft PowerPoint, dòng cuối cùng không còn bị đọc như dòng phía trên nếu nó là dòng trắng. (#3403)
* Trong Microsoft PowerPoint, các đối tượng không còn thỉnh thoảng bị đọc hai lần khi bạn chọn hay chỉnh sửa chúng. (#3394)
* NVDA không còn làm cho Adobe Reader bị lỗi hay treo với một vài mẫu tài liệu PDF bị định dạng sai quy cách, có các dòng nằm ngoài bảng biểu. (#3399)
* NVDA giờ đã nhận dạng chính xác slide kế tiếp với focus khi xóa một slide trong Microsoft PowerPoint ở chế độ xem thumbnails. (#3415)

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2013.1.1

Bản phát hành này sửa lỗi NVDA bị treo khi khởi động nếu đã được cấu hình để dùng với tiếng Irish, cũng bao gồm cả việc cập nhật và sửa vài lỗi khác.

### Sửa lỗi

* Sửa lỗi các kí tự được tạo ra khi gõ trong giao diện người dùng của NVDA với phương thức nhập mặc định là tiếng Nhật hay tiếng Hàn quốc. (#2909)
* Trong Internet Explorer và các điều khiển MSHTML khác, các trường được đánh dấu có một entry không hợp lệ giờ đây đã được quản lý một cách chính xác. (#3256)
* NVDA không còn bị lỗi khi khởi động nếu nó được cấu hình để dùng với tiếng Irish.

## 2013.1

Các cải tiến của bản phát hành này bao gồm kiểu bàn phím laptop trực quan và nhất quán hơn; hỗ trợ cơ bản cho Microsoft PowerPoint; hỗ trợ mô tả trên các trình duyệt web; và hỗ trợ kiểu nhập chữ nổi máy tính cho  các màn hình nổi có bàn phím.

### Quan trọng

#### Kiểu bàn phím Laptop mới

Kiểu bàn phím laptop đã được thiết kế lại hoàn toàn để nó trở nên trực quan và nhất quán hơn.
Kiểu bàn phím mới dùng các phím mũi tên phối hợp với phím NVDA và các phím bổ trợ khác cho các lệnh kiểm duyệt.

Xin lưu ý các thay đổi sau cho các lệnh được dùng phổ biến:

| Tên |Phím|
|---|---|
|Đọc tất cả |NVDA+a|
|Đọc dòng hiện tại |NVDA+l|
|Đọc vùng văn bản đang chọn |NVDA+shift+s|
|Thông báo thanh trạng thái |NVDA+shift+end|

Ngoài ra, trong các thay đổi khác, tất cả lệnh của việc duyệt đối tượng, duyệt văn bản, nhấp chuột và các thiết lập nhanh cho bộ đọc cũng bị thay đổi.
Vui lòng xem [Bản tham khảo các phím lệnh](keyCommands.html) để biết các phím lệnh mới.

### Các tính năng mới

* Hỗ trợ cơ bản cho việc đọc và soạn thảo các bài trình chiếu Microsoft PowerPoint. (#501)
* Hỗ trợ cơ bản cho việc đọc và soạn tin nhắn trong Lotus Notes 8.5. (#543)
* Hỗ trợ tự chuyển ngôn ngữ khi đọc tài liệu trong Microsoft Word. (#2047) 
* Ở chế độ duyệt cho MSHTML (ví dụ: Internet Explorer) và Gecko (ví dụ: Firefox), các mô tả đã được thông báo. Cũng có thể mở thông báo mô tả trên một cửa sổ mới bằng cách bấm NVDA+d. (#809)
* Thông báo trong Internet Explorer 9 trở lên giờ đây đã được đọc (nội dung bị chặn hay có tập tin tải về chẳng hạn). (#2343)
* Việc tự đọc tiêu đề cột và dòng giờ đây đã hỗ trợ cho tài liệu ở chế độ duyệt trong Internet Explorer và  các điều khiển MSHTML khác. (#778)
* Các ngôn ngữ mới: Aragon, Ailen
* Các bản phiên dịch chữ nổi mới: Đan Mạch cấp 2, Hàn Quốc cấp 1. (#2737)
* Hỗ trợ các màn hình chữ nổi kết nối qua bluetooth trên máy tính đang chạy Bluetooth Stack cho Windows của Toshiba. (#2419)
* Hỗ trợ chọn cổng khi dùng các màn hình của Freedom Scientific (Tự động, USB hoặc Bluetooth).
* Hỗ trợ cho BrailleNote thành viên của notetakers từ HumanWare khi hoạt động như braille terminal cho trình đọc màn hình. (#2012)
* Hỗ trợ các mẫu cũ của màn hình nổi Papenmeier BRAILLEX. (#2679)
* Hỗ trợ nhập chữ nổi máy tính cho các màn hình có bàn phím chữ nổi. (#808)
* Cài đặt mới của bàn phím cho phép lựa chọn để NVDA ngừng đọc khi gõ kí tự hay phím Enter. (#698)
* Hỗ trợ vài trình duyệt web trên nền tảng Google Chrome: Rockmelt, BlackHawk, Comodo Dragon và SRWare Iron. (#2236, #2813, #2814, #2815)

### Các thay đổi

* Cập nhật thư viện phiên dịch chữ nổi liblouis lên phiên bản 2.5.2. (#2737)
* Kiểu bàn phím laptop đã được thiết kế lại hoàn toàn để nó trực quan và nhất quán hơn. (#804)
* Cập nhật bộ đọc eSpeak lên 1.47.11. (#2680, #3124, #3132, #3141, #3143, #3172)

### Sửa lỗi

* các phím di chuyển nhanh đến phân cách trước hay phân cách kế ở chế độ duyệt giờ đã hoạt động trong  Internet Explorer và các điều khiển MSHTML khác. (#2781)
* Nếu NVDA trở lại bộ đọc eSpeak hoặc không đọc do bộ đọc đã thiết lập bị lỗi khi khởi động, cấu hình lựa chọn không còn bị chuyển sang bộ đọc này nữa. Điều đó có nghĩa là bộ đọc trước đó sẽ được thử lại vào lần khởi động NVDA tiếp theo. (#2589)
* Nếu NVDA chuyển sang Không có Braille vì cấu hình cho màn hình chữ nổi bị lỗi khi khởi động, cấu hình sẽ không còn tự thiết lập là Không có Braille. Điều này có nghĩa là màn hình trước đó sẽ được thử lại vào lần khởi động  NVDA tiếp theo. (#2264)
* Ở chế độ duyệt trong các ứng dụng Mozilla, các cập nhật cho bảng biểu đã được thể hiện chính xác. Ví dụ, trong các ô đã cập nhật, tọa độ dòng và cột đã được đọc và điều hướng trong bảng đã hoạt động như bình thường. (#2784)
* Ở chế độ duyệt trong các trình duyệt web, một số biểu tượng có thể kích không gắn nhãn mà trước đây không được thể hiện, giờ đã thể hiện chính xác. (#2838)
* Đã hỗ trợ các phiên bản cũ và mới hơn của SecureCRT. (#2800)
* Với các phương thức nhập như Easy Dots IME trên XP, các chuỗi để đọc giờ đã được thông báo chính xác.
* Danh sách thử nghiệm của kiểu nhập tiếng Trung giản thể Microsoft Pinyin trên Windows 7 giờ đã được đọc chính xác khi chuyển trang bằng mũi tên trái / phải, và ở lần mở đầu với Home.
* Khi các thông tin tùy biến cho phát âm kí hiệu được lưu, trường mở rộng "Giữ lại" không còn bị gỡ bỏ. (#2852)
* Khi tắt tự động cập nhật, NVDA không còn yêu cầu phải khởi động lại để  thay đổi có hiệu lực.
* NVDA không còn tình trạng không khởi động được khi có một add-on không thể gỡ bỏ do  thư mục của nó đang được dùng bởi một ứng dụng khác. (#2860)
* Nhãn của các thẻ trong hộp thoại  preferences của Dropbox đã có thể xem được với Flat Review.
* Nếu ngôn ngữ đầu vào được thay đổi khác với mặc định, NVDA giờ đây đã nhận ra các phím chính xác cho phím lệnh và chế độ trợ giúp nhập.
* Với các ngôn ngữ như tiếng Đức, kí hiệu + (dấu cộng) là một phím riêng lẽ trên bàn phím, giờ đây đã có thể liên kết các lệnh đến nó bằng cách dùng từ "plus". (#2898)
* Trong Internet Explorer và các điều khiển MSHTML khác, các đoạn trích dẫn giờ đã được thông báo hợp lý. (#2888)
* Driver của dòng màn hình nổi HumanWare Brailliant BI/B giờ đây đã có thể được lựa chọn khi màn hình được kết nối qua Bluetooth nhưng chưa bao giờ kết nối qua USB.
* Việc lọc các thành phần ở chế độ duyệt danh sách các thành phần với chế độ lọc văn bản chữ hoa giờ đây trả về kết quả không phân biệt chữ hoa / thường giống như chữ thường thay vì không trả về cái gì. (#2951)
* Trong các trình duyệt Mozilla, chế độ duyệt lại có thể dùng khi nội dung Flash có focus. (#2546)
* Khi dùng một bảng chữ nổi viết tắt và bật tùy chọn mở rộng sang chữ nổi máy tính cho từ tại vị trí con trỏ, con trỏ nổi giờ đây đã đứng chính xác khi ở sau một từ mà một kí tự được thể hiện bởi nhiều ô chữ nổi (ví dụ: kí tự hoa, chữ cái, số, v...v...). (#2947)
* Việc chọn văn bản giờ đây đã hiển thị chính xác trên một màn hình chữ nổi trong các ứng dụng như Microsoft word 2003 và các điều khiển soạn thảo của Internet Explorer.
* Lại có thể chọn văn bản theo hướng ngược trong Microsoft Word khi bật Braille.
* Khi kiểm duyệt, xóa  các kí tự trong điều khiển soạn thảo của Scintilla, NVDA thông báo chính xác các kí tự đa nhân. (#2855)
* NVDA không còn tình trạng không cài đặt được khi đường dẫn đến hồ sơ người dùng chứa một số kí tự đa nhân nhất định. (#2729)
* Việc thông báo các nhóm cho các điều khiển danh sách (SysListview32) trong các ứng dụng 64-bit không còn gây ra lỗi.
* Ở chế độ duyệt trong các ứng dụng Mozilla, nội dung văn bản không còn bị nhận dạng sai là có thể nhập trong vài trường hợp hiếm gặp. (#2959)
* Trong IBM Lotus Symphony và OpenOffice, việc di chuyển con trỏ sẽ di chuyển luôn con trỏ duyệt nếu phù hợp.
* Nội dung của Adobe Flash giờ đây đã tiếp cận được trong Internet Explorer trên Windows 8. (#2454)
* Sửa lỗi hỗ trợ Bluetooth cho Papenmeier Braillex Trio. (#2995)
* Sửa lỗi không dùng được một số giọng đọc Microsoft Speech API phiên bản 5 như các giọng đọc Koba Speech 2. (#2629)
* Trong các ứng dụng dùng Java Access Bridge, các màn hình nổi giờ đây đã được cập nhật chính xác khi dấu nháy di chuyển trong các trường nhập liệu. (#3107)
* Hỗ trợ các trường cột mốc trong các tài liệu chế độ duyệt có hỗ trợ các cột mốc. (#2997) 
* Trình điều khiển của bộ đọc eSpeak giờ đây quản lý việc đọc theo kí tự một cách phù hợp hơn (ví dụ: đọc tên của một kí tự tiếng nước ngoài hay giá trị thay vì chỉ âm thanh hay tên chung của nó ). (#3106)
* NVDA không còn bị lỗi khi  sao chép các thiết lập của người dùng để sử dụng ở màn hình khởi động hay các màn hình bảo vệ khác khi  đường dẫn đến thư mục hồ sơ người dùng có chứa các kí tự không thuộc mã ASCII. (#3092)
* NVDA Không còn bị đóng băng khi dùng đầu vào là các kí tự Châu Á trong vài ứng dụng .NET. (#3005)
* Giờ đây đã có thể dùng chế độ duyệt cho các trang trong Internet Explorer 10 ở chế độ chuẩn; ví dụ: trang đăng nhập [www.gmail.com](http://www.gmail.com). (#3151)

### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2012.3
Các cải tiến của bản phát hành này bao gồm hỗ trợ nhập các kí tự Châu Á; thử nghiệm hỗ trợ màn hình cảm ứng trên Windows 8; đọc số trang và cải thiện hỗ trợ cho bảng trong Adobe Reader; các phím điều hướng ở dòng trong bảng tại dòng đang có focus và các điều khiển dạng danh sách trình bày của Windows; hỗ trợ thêm vài màn hình nổi; và thông báo tiêu đề cột và dòng trong Microsoft Excel.

### Các tính năng mới
- NVDA giờ đây có thể hỗ trợ nhập các kí tự Châu Á bằng dịch vụ phương thức nhập IME và văn bản trong tất cả các ứng dụng, bao gồm:
    - Thông báo và duyệt qua danh sách hiện có;
    - Thông báo và duyệt qua các chuỗi thành phần; và
    - Thông báo các chuỗi đọc.
- Thể hiện của dấu gạch dưới và dấu strikethrough giờ đây đã được đọcAdobe trong các tài liệu Adobe Reader. (#2410)
- Khi bật chức năng Windows Sticky Keys, phím bổ trợ NVDA giờ đây sẽ hoạt động như các phím bổ trợ khác. Điều này cho phép bạn dùng phím bổ trợ NVDA mà không cần phải giữ nó trong khi bấm các phím khác. (#230)
- Đã hỗ trợ tự đọc tiêu đề cột và dòng trong Microsoft Excel. Bấm `NVDA+shift+c` để chỉ định dòng có tiêu đề cột và `NVDA+shift+r` để chỉ định cột có tiêu đề dòng. Bấm các lệnh trên nhanh hai lần để xóa thiết lập. (#1519)
- Hỗ trợ cho các màn hình nổi HIMS Braille Sense, Braille EDGE và SyncBraille. (#1266, #1267)
- Khi xuất hiện thông báo Toast của Windows 8, NVDA sẽ đọc chúng nếu bật thông báo trợ giúp. (#2143)
- Thử nghiệm hỗ trợ cho màn hình cảm ứng trên Windows 8, bao gồm:
    - Đọc trực tiếp văn bản dưới ngón tay của bạn khi di chuyển trên màn hình
    - Nhiều thao tác để thực hiện duyệt đối tượng, duyệt văn bản và các lệnh khác của NVDA.
- Hỗ trợ cho VIP Mud. (#1728)
- Trong Adobe Reader, nếu một bảng có phần tóm tắt, nó sẽ được trình bày. (#2465)
- Trong Adobe Reader, tiêu đề cột và dòng giờ đây đã có thể được đọc. (#2193, #2527, #2528)
- Các ngôn ngữ mới: Amharic, Hàn quốc, Nepal, Slovenia.
- NVDA giờ đây có thể đọc các gợi ý tự hoàn tất khi nhập các địa chỉ email trong Microsoft Outlook 2007. (#689)
- Các biến thể mới của bộ đọc eSpeak: Gene, Gene2. (#2512)
- Trong Adobe Reader, số trang giờ đây cũng có thể đọc được. (#2534)
    - Trong Reader XI, các nhãn trang được đọc ở nơi trình bày, phản ánh các thay đổi đến số trang trong các phần khác nhau, v...v... Trong các phiên bản trước, điều này là không thể và chỉ các số trang tuần tự được đọc.
- Giờ đã có thể khôi phục cấu hình của NVDA về thiết lập mặc định của nhà sản xuất bằng cách bấm `NVDA+control+r` nhanh ba lần hoặc chọn Khôi phục về cấu hình mặc định từ trình đơn NVDA. (#2086)
- Hỗ trợ cho các màn hình nổi Seika phiên bản 3, 4 và 5 và Seika80 từ Nippon Telesoft. (#2452)
- Các nút định tuyến đầu tiên và cuối cùng ở phía trên của Freedom Scientific PAC Mate và các màn hình nổi Focus Braille giờ đây có thể dùng để cuộn lùi và cuộn tới. (#2556)
- Nhiều tính năng được hỗ trợ thêm trên các màn hình nổi Focus của Freedom Scientific như thanh mở rộng, thanh rocker và vài kết hợp chấm nổi cho các hoạt động phổ biến. (#2516)
- Trong các ứng dụng đang dùng IAccessible2 như các ứng dụng của Mozilla, các tiêu đề cột và dòng giờ đây có thể được đọc khi không ở trong chế độ duyệt. (#926)
- Hỗ trợ sơ bộ cho điều khiển tài liệu trong Microsoft Word 2013. (#2543)
- Giờ đây, canh lề văn bản có thể được thông báo trong các ứng dụng dùng IAccessible2 như các ứng dụng của Mozilla. (#2612)
- Khi focus tại một dòng trong bảng hay một điều khiển là danh sách chuẩn của Windows có nhiều cột, bạn có thể dùng các lệnh điều hướng trong bảng để tương tác với một ô cụ thể. (#828)
- Các bản phiên dịch chữ nổi mới: Estonia cấp 0, Bồ Đào Nha máy tính 8 chấm, Italia máy tính 6 chấm. (#2319, #2662)
- Nếu đã cài đặt NVDA vào hệ thống, khi mở trực tiếp một gói add-on của NVDA (ví dụ: mở từ  Windows Explorer hay mở sau khi  tải trong một   trình duyệt web), nó sẽ được cài vào NVDA. (#2306)
- Hỗ trợ cho các mẫu mới hơn của màn hình chữ nổi Papenmeier BRAILLEX. (#1265)
- Thông tin vị trí (ví dụ 1 của 4) giờ đây đã được đọc trong danh sách thành phần của Windows Explorer  trên Windows 7 trở lên. Điều này cũng bao gồm bất kì điều khiển nào UIAutomation có hỗ trợ các thuộc tính tùy biến itemIndex và itemCount. (#2643)


### Các thay đổi
- Trong hộp thoại thiết lập con trỏ duyệt của NVDA, đã đổi tên mục Follow keyboard focus  (đi theo focus bàn phím) thành Follow system focus (đi theo focus hệ thống) cho thống nhất với thuật ngữ đã  dùng ở những nơi khác của NVDA.
- Khi chữ nổi đi theo con trỏ duyệt và con trỏ đứng tại một đối tượng không phải là văn bản (ví dụ: một ô nhập văn bản), các phím cursor routing giờ đây sẽ kích hoạt đối tượng. (#2386)
- Tùy chọn lưu thiết lập khi thoát NVDA giờ đây mặc định được bật cho cấu hình mới.
- Khi cập nhật từ một bản  NVDA đã cài trước đó, phím tắt của biểu tượng trên desktop sẽ không còn quay trở lại control+alt+n nếu nó đã được thay đổi bởi người dùng. (#2572)
- Danh sách add-on trong trình quản lý Add-on giờ đây hiển thị tên gói add-on trước trạng thái của nó. (#2548)
- Nếu cài cùng hoặc khác phiên bản với một  add-on đang được cài đặt, NVDA sẽ hỏi bạn có muốn cập nhật add-on, thay vì chỉ hiện thông báo lỗi và hủy cài đặt. (#2501)
- Các lệnh duyệt đối tượng (trừ lệnh thông báo đối tượng hiện tại) giờ đây sẽ thông báo gọn gàng hơn. Bạn vẫn có thể  lấy các thông tin thêm bằng cách dùng lệnh thông báo đối tượng hiện tại. (#2560)
- Cập nhật thư viện phiên dịch chữ nổi liblouis lên 2.5.1. (#2319, #2480, #2662, #2672)
- Lệnh NVDA Key Commands Quick Reference document đã được đổi tên thành Commands Quick Reference, vì nó giờ đây đã bao gồm các thao tác cảm ứng cũng như lệnh bàn phím.- Danh sách các thành phần trong chế độ duyệt giờ đây sẽ nhớ loại thành phần đã hiển thị sau cùng (ví dụ: liên kết, tiêu đề hay cột mốc) mỗi lần hộp thoại hiển thị trong cùng phiên làm việc của 	NVDA. (#365)
- Hầu hết các ứng dụng Metro trong Windows 8 (Mail, Calendar) không còn kích hoạt chế độ duyệt cho toàn bộ ứng dụng.
- Đã cập nhật Handy Tech BrailleDriver COM-Server lên 1.4.2.0.


### Sửa lỗi
- Trong Windows Vista hay cao hơn, NVDA không còn xem như phím Windows đang được giữ khi mở khóa Windows sau khi khóa nó bằng lệnh Windows+l. (#1856)
- Trong Adobe Reader, tiêu đề dòng giờ đây được nhận dạng chính xác là ô trong bảng; chẳng hạn: tọa độ được đọc và có thể truy cập chúng bằng các lệnh điều hướng trong bảng. (#2444)
- Trong Adobe Reader, các ô trong bảng nằm ở nhiều hơn một cột hay dòng giờ đã được quản lý một cách chính xác. (#2437, #2438, #2450)
- Gói phân phối NVDA giờ đây sẽ kiểm tra tính toàn vẹn của nó trước khi thực thi. (#2475)
- Các tập tin tạm giờ đây được gỡ bỏ nếu việc tải một bản cập nhật của NVDA bị thất bại. (#2477)
- NVDA không còn bị treo khi chạy với quyền quản trị trong lúc sao chép cấu hình người dùng vào cấu hình hệ thống (để dùng khi   đăng nhập Windows và các màn hình bảo vệ khác). (#2485)
- Trình bày dạng tiles trên Start Screen của Windows 8 giờ đây thể hiện tốt hơn trong tiếng nói và chữ nổi. Các tên không còn bị đọc lặp lại, thông báo chưa chọn cũng không còn được đọc trên tất cả thành phần, và các thông tin trạng thái trực tiếp đã được thể hiện như mô tả của thành phần (chẳng hạn, nhiệt độ hiện tại của ứng dụng thời tiết).
- Mật khẩu không còn bị thông báo khi xem các ô nhập mật khẩu trong Microsoft Outlook và các điều khiển nhập liệu chuẩn có đành dấu được bảo vệ. (#2021)
- Trong Adobe Reader, các thay đổi của biểu mẫu giờ đây được trả về chính xác trong chế độ duyệt. (#2529)
- Cải thiện để hỗ trợ tính năng kiểm tra chính tả của Microsoft Word, bao gồm việc đọc lỗi chính tả hiện tại một cách chính xác hơn, và khả năng hỗ trợ kiểm tra chính tả khi đang chạy một  bản NVDA đã cài đặt trên Windows Vista trở lên.
- Các Add-on bao gồm tập tin có chứa các kí tự không phải tiếng Anh giờ đây đã có thể cài đặt trong đa số trường hợp. (#2505)
- Trong Adobe Reader, ngôn ngữ của văn bản không còn bị mất khi nó được cập nhật hay cuộn đến. (#2544)
- Khi cài đặt một add-on, hộp thoại xác nhận giờ đây sẽ hiển thị chính xác tên bản địa của add-on nếu có. (#2422)
- Trong các ứng dụng dùng UI Automation (.net và các ứng dụng Silverlight chẳng hạn), việc tính toán các giá trị số cho các điều khiển như thanh trượt đã được sửa lại. (#2417)
- Cấu hình cho việc đọc các thanh tiến độ giờ đây đã quản lý được các thanh tiến độ không xác định được hiển thị bởi NVDA khi cài đặt, tạo bản chạy trực tiếp, v...v.... (#2574)
- Các lệnh của NVDA có thể không kích hoạt được từ màn hình nổi khi một màn hình bảo vệ (màn hình khóa chẳng hạn) đang hoạt động. (#2449)
- Trong chế độ duyệt, chữ nổi giờ đây đã được cập nhật khi nội dung đang hiển thị có sự thay đổi. (#2074)
- Khi ở một màn hình bảo vệ của Windows như màn hình khóa, các thông điệp phát âm từ ứng dụng hay hiển thị bằng chữ nổi thông qua NVDA giờ đây bị bỏ qua.
- Ở chế độ Duyệt, không còn có thể rơi ra khỏi cuối tài liệu bằng phím mũi tên phải khi ở ký tự cuối cùng hoặc bằng cách nhảy đến cuối vùng chứa khi vùng chứa đó là mục cuối cùng trong tài liệu. (#2463)
- Nội dung không liên quan không còn được đưa vào không chính xác khi báo cáo văn bản của hộp thoại trong ứng dụng web (cụ thể là hộp thoại ARIA không có thuộc tính aria-descriptionby). (#2390)
- NVDA không còn đọc hoặc định vị không chính xác các trường chỉnh sửa nhất định trong tài liệu MSHTML (ví dụ: Internet Explorer), đặc biệt khi tác giả trang web sử dụng vai trò ARIA rõ ràng. (#2435)
- Phím xóa lùi hiện được xử lý chính xác khi đọc các từ đã nhập trong bảng điều khiển lệnh của Windows. (#2586)
- Tọa độ ô trong Microsoft Excel hiện đã hiển thị lại trong chữ nổi.
- Trong Microsoft Word, NVDA không còn khiến bạn bị mắc kẹt trong một đoạn văn có định dạng danh sách khi cố gắng di chuyển qua một dấu đầu dòng hoặc số bằng mũi tên trái hoặc control + mũi tên trái. (#2402)
- Ở chế độ duyệt trong ứng dụng Mozilla, các mục trong một số hộp danh sách nhất định (cụ thể là hộp danh sách ARIA) không còn bị hiển thị sai nữa.
- Ở chế độ duyệt trong ứng dụng Mozilla, một số điều khiển nhất định được hiển thị với nhãn không chính xác hoặc chỉ có khoảng trắng hiện đã hiển thị với nhãn chính xác.
- Ở chế độ duyệt trong ứng dụng Mozilla, một số khoảng trắng không liên quan đã bị loại bỏ.
- Ở chế độ duyệt trong trình duyệt web, một số đồ họa nhất định được đánh dấu rõ ràng là mang tính trình bày (cụ thể là với thuộc tính alt="") hiện đã bị bỏ qua một cách chính xác.
- Trong trình duyệt web, NVDA hiện ẩn nội dung được đánh dấu là ẩn khỏi trình đọc màn hình (cụ thể là sử dụng thuộc tính aria-hidden). (#2117)
- Số tiền âm (ví dụ: -$123) hiện được đọc chính xác là số âm, bất kể cấp độ đọc ký hiệu. (#2625)
- Trong chế độ đọc tất cả, NVDA sẽ không còn hoàn nguyên sai về ngôn ngữ mặc định khi một dòng không kết thúc một câu. (#2630)
- Thông tin phông chữ hiện được nhận dạng chính xác trong Adobe Reader 10.1 trở lên. (#2175)
- Trong Adobe Reader, nếu văn bản thay thế được cung cấp thì chỉ văn bản đó mới được hiển thị. Trước đây, văn bản không liên quan đôi khi được đưa vào. (#2174)
- Trong trường hợp tài liệu chứa ứng dụng, nội dung của ứng dụng đó không còn được đưa vào chế độ duyệt. Điều này ngăn việc di chuyển bất ngờ bên trong ứng dụng khi điều hướng. Bạn có thể tương tác với ứng dụng theo cách tương tự như đối với các đối tượng được nhúng. (#990)
- Trong các ứng dụng Mozilla, giá trị của các nút xoay hiện được báo cáo chính xác khi nó thay đổi. (#2653)
- Cập nhật hỗ trợ cho Adobe Digital Editions để nó hoạt động ở phiên bản 2.0. (#2688)
- Bấm NVDA+mũi tên lên khi đang ở hộp xổ trong Internet Explorer và các tài liệu MSHTML khác sẽ không còn đọc sai tất cả các mục. Thay vào đó, chỉ mục đang hoạt động sẽ được đọc. (#2337)
- Từ điển giọng nói giờ đây sẽ lưu đúng cách khi sử dụng dấu số (#) trong trường mẫu hoặc trường thay thế. (#961)
- Chế độ duyệt các tài liệu MSHTML (ví dụ: Internet Explorer) giờ đây hiển thị chính xác nội dung hiển thị có trong nội dung ẩn (cụ thể là các phần tử có kiểu hiển thị:hiển thị bên trong một phần tử có kiểu hiển thị:ẩn). (#2097)
- Các liên kết trong Security Center của Windows XP không còn báo cáo rác ngẫu nhiên sau tên của chúng nữa. (#1331)
- Các điều khiển văn bản của - UI Automation (ví dụ: trường tìm kiếm trong Start Menu của Windows 7) hiện được thông báo chính xác khi di chuyển chuột qua chúng thay vì giữ im lặng.
- Những thay đổi về bố cục bàn phím không còn được nói lên trong khi ở chế độ tất cả, điều này đặc biệt gây ra vấn đề đối với các tài liệu đa ngôn ngữ bao gồm cả văn bản tiếng Ả Rập. (#1676)
- Toàn bộ nội dung của một số điều khiển văn bản có thể chỉnh sửa UI Automation (ví dụ: Hộp Tìm kiếm trong Menu Bắt đầu của Windows 7/8) không còn được thông báo mỗi khi thay đổi.
- Khi di chuyển giữa các nhóm trên start screen của Windows 8, các nhóm không được gắn nhãn sẽ không còn thông báo ô đầu tiên của họ là tên của nhóm nữa. (#2658)
- Khi mở start screen của Windows 8, tiêu điểm được đặt chính xác trên ô đầu tiên, thay vì nhảy đến thư mục gốc của màn hình bắt đầu, điều này có thể gây nhầm lẫn khi điều hướng. (#2720)
- NVDA sẽ không còn bị lỗi khởi động khi đường dẫn hồ sơ người dùng chứa các ký tự nhiều byte nhất định. (#2729)
- Ở chế độ duyệt trong Google Chrome, văn bản của các tab hiện được hiển thị chính xác.
- Ở chế độ duyệt, các nút trình đơn hiện được đọc chính xác.
- Trong OpenOffice.org/LibreOffice Calc, việc đọc các ô trong bảng tính hiện hoạt động chính xác. (#2765)
- NVDA có thể hoạt động trở lại trong danh sách thư của Yahoo! khi được sử dụng từ Internet Explorer. (#2780)


### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

## 2012.2.1
Bản phát hành này giải quyết một số vấn đề bảo mật tiềm ẩn (bằng cách nâng cấp Python lên 2.7.3).


## 2012.2
Điểm nổi bật của bản phát hành này bao gồm trình cài đặt dựng sẵn và tính năng tạo bản chạy trực tiếp, cập nhật tự động, quản lý dễ dàng các add-on mới của NVDA, thông báo hình ảnh trong Microsoft Word, hỗ trợ các ứng dụng kiểu Windows 8 Metro và một số sửa lỗi quan trọng.

### Tính năng mới
- NVDA giờ đây có thể tự động kiểm tra, tải xuống và cài đặt các bản cập nhật. (#73)
- Việc mở rộng chức năng của NVDA đã trở nên dễ dàng hơn với việc bổ sung Trình quản lý Add-on (có trong Công cụ trong trình đơn NVDA) cho phép bạn cài đặt và gỡ cài đặt các gói tiện ích NVDA mới (tập tin .nvda-addon) có chứa các plugin và trình điều khiển. Lưu ý rằng trình quản lý Tiện ích bổ sung không hiển thị các plugin và trình điều khiển tùy chỉnh cũ hơn được sao chép thủ công vào thư mục cấu hình của bạn. (#213)
- Nhiều tính năng phổ biến  của NVDA hiện đã hoạt động trong các ứng dụng kiểu Metro của Windows 8 khi sử dụng bản phát hành NVDA đã cài đặt, bao gồm đọc các ký tự đã nhập và chế độ duyệt tài liệu web (bao gồm hỗ trợ cho phiên bản metro của Internet Explorer 10). Bản chạy trực tiếp của NVDA không thể truy cập các ứng dụng kiểu metro. (#1801)
- Trong các tài liệu ở chế độ duyệt (Internet Explorer, Firefox, v.v.), giờ đây bạn có thể chuyển đến phần đầu và phần cuối của một số phần tử chứa nhất định (chẳng hạn như danh sách và bảng) bằng shift+ và , tương ứng. (#123)
- Ngôn ngữ mới: Greek.
- Hình ảnh và văn bản thay thế giờ đây đã được đọc trong tài liệu Microsoft Word. (#2282, #1541)


### Các thay đổi
- Thông báo tọa độ ô trong Microsoft Excel hiện được đọc sau nội dung, thay vì đọc trước và hiện chỉ được bao gồm nếu  bật các cài đặt thông báo bảng biểu và tọa độ ô trong hộp thoại Cài đặt định dạng tài liệu. (#320)
- NVDA hiện được phân phối thành một gói. Thay vì tách riêng phiên bản chạy trực tiếp và trình cài đặt, giờ đây chỉ có một tập tin mà khi chạy sẽ khởi động một bản sao tạm thời của NVDA và cho phép bạn cài đặt hoặc tạo bản phân phối di động. (#1715)
- NVDA giờ đây luôn được cài đặt vào thu mục Program Files trên tất cả các hệ thống. Cập nhật các bản cài đặt  cũng sẽ tự động di chuyển nó nếu trước đó nó chưa được cài đặt ở đây.


### Sửa lỗi
- Khi bật tính năng chuyển đổi ngôn ngữ tự động, Nội dung như văn bản thay thế cho hình ảnh và nhãn cho các điều khiển nhất định khác trong Mozilla Gecko (ví dụ: Firefox) hiện được báo cáo bằng ngôn ngữ chính xác nếu được đánh dấu thích hợp.
- Tính năng đọc tất cả trong BibleSeeker (và các điều khiển TRxRichEdit khác) không còn dừng ở giữa đoạn văn nữa.
- Danh sách được tìm thấy trong File Properties của Windows 8 Explorer (thẻ permitions ) và trong Windows 8 Windows Update giờ đã được đọc chính xác.
- Đã khắc phục lỗi có thể xảy ra trong MS Word, dẫn đến việc mất hơn 2 giây để tìm nạp văn bản từ tài liệu (dòng hoặc mục lục cực dài). (#2191)
- Tính năng phát hiện ngắt từ hiện hoạt động chính xác khi khoảng trắng được theo sau bởi dấu câu nhất định. (#1656)
- Trong chế độ duyệt trong Adobe Reader, giờ đây bạn có thể điều hướng đến các tiêu đề không cần cấp độ bằng cách sử dụng điều hướng nhanh và Danh sách Thành phần. (#2181)
- Trong Winamp, chữ nổi hiện được cập nhật chính xác khi bạn di chuyển đến một mục khác trong Trình chỉnh sửa danh sách phát. (#1912)
- Cây trong Danh sách Thành phần (có sẵn cho các tài liệu ở chế độ duyệt) hiện có kích thước phù hợp để hiển thị văn bản của từng thành phần. (#2276)
- Trong các ứng dụng sử dụng Java Access Bridge, các trường văn bản có thể chỉnh sửa giờ đây được trình bày chính xác bằng chữ nổi. (#2284)
- Trong các ứng dụng sử dụng java Access Bridge, các trường văn bản có thể chỉnh sửa không còn báo cáo các ký tự lạ trong một số trường hợp nhất định. (#1892)
- Trong các ứng dụng sử dụng Java Access Bridge, khi ở cuối trường văn bản có thể chỉnh sửa, dòng hiện tại sẽ được đọc chính xác. (#1892)
- Ở chế độ duyệt trong các ứng dụng sử dụng Mozilla Gecko 14 trở lên (ví dụ: Firefox 14), điều hướng nhanh hiện hoạt động đối với các trích dẫn khối và các đối tượng được nhúng. (#2287)
- Trong Internet Explorer 9, NVDA không còn đọc nội dung không mong muốn khi tiêu điểm di chuyển bên trong các mốc hoặc phần tử có thể lấy tiêu điểm nhất định (cụ thể là phần tử div có thể lấy tiêu điểm hoặc có vai trò đánh dấu ARIA).
- Biểu tượng của NVDA trên Desktop và Start Menu giờ đã hiển thị chính xác trên các phiên bản 64 bit của Windows. (#354)


### Các thay đổi cho nhà phát triển

Phần này không được dịch. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.
### Các phiên bản cũ

Các thay đổi và tính năng mới của các phiên bản cũ hiện không được dịch sang tiếng Việt. Vui lòng xem bản tiếng Anh changes.t2t để biết thêm thông tin.

