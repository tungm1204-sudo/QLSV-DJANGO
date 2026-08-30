### Nguyên tắc triển khai

Dựa trên **cấu trúc và source code hiện tại của cả Backend (BE) và Frontend (FE)**, hãy triển khai đúng theo kế hoạch đã thống nhất và các nhận xét kỹ thuật trước đó để **hoàn thành Phase đang được yêu cầu**.

Trong quá trình triển khai, **tuyệt đối không tự giả định, tự tạo hoặc viết lại cấu trúc code khi chưa kiểm tra code hiện tại của dự án**. Mọi thay đổi phải được xây dựng dựa trên các model, API, service, component, hook, route, convention, dependency và architecture đang thực sự tồn tại trong codebase.

Trước khi sửa hoặc tạo bất kỳ file nào, hãy:

1. **Kiểm tra cấu trúc dự án hiện tại** và xác định chính xác các file/module liên quan.
2. **Đọc và hiểu code hiện có** trước khi quyết định cách triển khai.
3. Xác định các dependency và mối quan hệ giữa BE ↔ FE để tránh tạo API, field, route hoặc component không tồn tại.
4. Với mỗi thay đổi, luôn tự kiểm tra:

   * Thay đổi này có **phá vỡ code hiện tại** không?
   * Có gây **xung đột hoặc không tương thích** với các module đang tồn tại không?
   * Có làm thay đổi behavior của chức năng cũ không?
   * API/request/response mới có **khớp hoàn toàn giữa BE và FE** không?
   * Có thể phát sinh lỗi migration, database, routing, state management, crash hoặc authentication/authorization không?
   * Có vi phạm architecture/convention hiện tại của dự án không?

### Nguyên tắc quan trọng

> **Không viết code theo suy đoán. Không tự bịa API, model, field, endpoint, component, hook hoặc cấu trúc thư mục.**

Nếu chức năng cần triển khai **chưa được Backend hỗ trợ**, trước tiên phải kiểm tra cách Backend hiện tại đang tổ chức nghiệp vụ và mở rộng dựa trên architecture có sẵn, thay vì tạo một cơ chế mới độc lập.

Nếu một phần code hiện tại có thể tái sử dụng, **ưu tiên tái sử dụng và mở rộng code cũ** thay vì tạo code trùng lặp.

Nếu phát hiện kế hoạch của Phase hiện tại có điểm **không tương thích với codebase hiện tại**, không được tự ý triển khai theo kế hoạch một cách máy móc. Hãy:

1. Chỉ ra chính xác điểm không tương thích.
2. Giải thích nguyên nhân.
3. Đề xuất phương án điều chỉnh ít ảnh hưởng nhất.
4. Chỉ triển khai sau khi phương án đã phù hợp với architecture hiện tại.

### Quy trình bắt buộc

```text
Đọc cấu trúc dự án
        ↓
Đọc code liên quan
        ↓
Hiểu architecture hiện tại
        ↓
Mapping kế hoạch Phase hiện tại
        ↓
Phân tích dependency & compatibility
        ↓
Xác định điểm cần sửa/thêm
        ↓
Triển khai dựa trên code hiện tại
        ↓
Kiểm tra lỗi / regression
        ↓
Hoàn thành Phase hiện tại
```

Trong suốt quá trình code, hãy luôn đặt câu hỏi:

> **"Thay đổi này có thực sự tương thích với code hiện tại của dự án không?"**

và:

> **"Tôi đang mở rộng architecture hiện tại hay đang vô tình tạo ra một architecture mới?"**

Mục tiêu không chỉ là làm cho chức năng của Phase hiện tại chạy được, mà là **tích hợp nó một cách tự nhiên vào codebase hiện tại, hạn chế tối đa breaking change, code duplication và technical debt**.

Cuối cùng, sau khi hoàn thành, hãy kiểm tra lại toàn bộ các thay đổi và xác nhận rằng **BE và FE vẫn đồng bộ, các chức năng cũ không bị phá vỡ, routing/API/state/data flow hoạt động đúng**, rồi mới kết luận Phase hiện tại hoàn thành.
