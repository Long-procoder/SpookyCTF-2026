# Trypophobia

**Category:** BinRev (Reverse Engineering)

**Difficulty:** Easy

**Points:** 75

## Phân tích đề bài

Đề bài cung cấp một file có tên `binary` và gợi ý: "Classic reverse engineering, right?".

Đây là bài toán Reverse Engineering, yêu cầu phân tích chương trình để tìm ra chuỗi đầu vào hợp lệ.

## 1. Kiểm tra file

Sử dụng lệnh `file` để xác định định dạng:

```bash
file binary
```

Kết quả:

```text
binary: compiled Java class data, version 52.0 (Java 1.8)
```

Nhận thấy đây là file Java đã biên dịch, vì vậy có thể sử dụng công cụ `javap` để phân tích bytecode.

## 2. Phân tích bytecode

Đổi tên file thành `binary.class` và sử dụng lệnh:

```bash
javap -c -p binary
```

Trong hàm `check(String)`, chương trình kiểm tra độ dài chuỗi đầu vào phải bằng 34 ký tự.

Sau đó, chương trình lần lượt lấy từng ký tự bằng `charAt(i)` và thực hiện các phép toán như cộng, trừ, XOR trước khi so sánh với những giá trị cố định.

Ví dụ:

```java
(31 ^ str.charAt(0)) + 7 == 115

(('I' - str.charAt(1)) ^ 11) == -46

((str.charAt(2) + 5) ^ 22) == 98
```

Các điều kiện này được sử dụng để kiểm tra từng ký tự của flag.

## 3. Khôi phục chuỗi đầu vào

Thay vì brute force, tiến hành đảo ngược các phép toán trong từng điều kiện để tìm ký tự tương ứng.

Một số quy tắc được sử dụng:

- Phép XOR: `a ^ b = c` thì `a = c ^ b`.
- Phép cộng: chuyển vế bằng phép trừ.
- Phép trừ: biến đổi phương trình để tìm giá trị chưa biết.

Thực hiện tương tự với toàn bộ 34 ký tự, ta khôi phục được chuỗi đầu vào hợp lệ.

## 4. Kiểm tra kết quả

Chạy chương trình Java với chuỗi vừa tìm được:

```bash
java binary 'spooky{ever_reversed_java?A67b_91}'
```

Kết quả:

```text
Correct!
```

## 5. Flag

```text
spooky{ever_reversed_java?A67b_91}
```
