# Nosocomephobia

**Category:** OSINT

**Difficulty:** Easy

**Points:** 50

## Phân tích đề bài

Đề bài cung cấp hai tệp dữ liệu gồm một bức ảnh và một đoạn ghi âm. Nhiệm vụ là phân tích các dữ liệu này để xác định địa điểm và năm liên quan đến bản ghi âm.

## 1. Phân tích file âm thanh

File `cassetterecording.mp3` chứa các tín hiệu âm thanh ngắn và dài, đây là dấu hiệu cho thấy nội dung được mã hóa bằng Morse.

Sử dụng công cụ [Morse Code Adaptive Audio Decoder](https://morsecode.world/international/decoder/audio-decoder-adaptive.html) để giải mã.

Sau khi giải mã, thu được một thông điệp kể về một bệnh nhân đang ở trong một cơ sở y tế. Đáng chú ý, người gửi nhắc đến hoạt động chiếu phim giáo dục tại phòng `Male 2`.

Chi tiết này là manh mối quan trọng để xác định cơ sở y tế được nhắc đến.

## 2. Phân tích metadata hình ảnh

Sử dụng ExifTool để kiểm tra metadata của file `picture_in_bottle.jpg`.

```bash
exiftool picture_in_bottle.jpg
```

Trong kết quả, chú ý đến trường `Description`:

```text
Creator: Hulton Archive
Description: Denbigh, Wales, from the northwest,
             circa 1885.
```

Từ thông tin này, xác định bức ảnh mô tả thị trấn Denbigh, Wales. Đây là cơ sở để thu hẹp phạm vi tìm kiếm địa điểm của bệnh viện.

## 3. Tìm kiếm tài liệu lưu trữ

Dựa trên hai manh mối từ file âm thanh và hình ảnh, tiến hành tìm kiếm thông tin về các bệnh viện tại Denbigh, đặc biệt là những nơi có hoạt động dành cho bệnh nhân.

Tìm được bài viết của Denbighshire Archives:

https://denbighshirearchives.wordpress.com/2019/07/05/entertaining-patients-in-the-north-wales-hospital/

Bài viết giới thiệu các hoạt động giải trí dành cho bệnh nhân tại North Wales Hospital, đồng thời cung cấp một bản tin hoạt động hằng tuần năm 1966.

Đối chiếu với nội dung âm thanh, bản tin có nhắc đến hoạt động chiếu phim giáo dục tại phòng `Male 2`. Chi tiết này trùng khớp với thông điệp Morse đã giải mã.

Từ đó xác định được địa điểm liên quan là North Wales Hospital và năm của tài liệu tương ứng là 1966.

## 4. Flag

Sau khi tổng hợp các manh mối từ hình ảnh, âm thanh và tài liệu lưu trữ, xác định được địa điểm là North Wales Hospital và năm ghi âm là 1966.

Flag:

```text
spooky{north_wales_hospital.1966}
```
