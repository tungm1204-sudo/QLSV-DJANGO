# QUY TẮC THIẾT KẾ GIAO DIỆN FRONTEND (ENTERPRISE UI/UX)

Tài liệu này định nghĩa các quy tắc thiết kế (Design Guidelines) bắt buộc phải tuân thủ khi lập trình Frontend cho hệ thống QLSV, nhằm đảm bảo giao diện đạt chuẩn **Enterprise-grade**, chuyên nghiệp, đồng nhất và hiệu năng cao.

## 1. Phong cách thiết kế chung (Aesthetic)
- **Chuẩn Vercel / Apple:** Thiết kế tối giản, loại bỏ các chi tiết rườm rà. Tập trung tối đa vào không gian hiển thị Dữ liệu (Data-driven).
- **Màu sắc (Color Palette):**
  - **Màu chủ đạo (Primary):** Xanh tím (Indigo) hoặc Xám xanh (Slate).
  - **Màu nền (Background):** Trắng (White) hoặc Xám cực nhạt (Gray-50) cho vùng nội dung chính.
  - **Dark Mode:** Áp dụng cho Sidebar để tạo độ sâu và phân tách vùng không gian làm việc.
- **Font chữ (Typography):** Bắt buộc sử dụng `Inter` hoặc `Geist` để tối ưu khả năng đọc số liệu trên bảng biểu.

## 2. Thư viện UI & Component
- **Thư viện gốc:** Bắt buộc sử dụng **`shadcn/ui`** kết hợp với **`Tailwind CSS`**. Không sử dụng các thư viện cồng kềnh như MUI, Ant Design hay Bootstrap.
- **Icons:** Sử dụng thư viện `lucide-react` cho đồng bộ với phong cách nét mảnh của `shadcn/ui`.
- **Form:** Mọi biểu mẫu nhập liệu đều phải được dựng bằng `react-hook-form` và kiểm tra tính hợp lệ bằng `zod`. Các input field phải có focus state rõ ràng (viền nhạt màu Primary).

## 3. Quy tắc Trải nghiệm người dùng (UX) & Tương tác
- **Micro-interactions:** Các nút bấm (Button), các dòng trong bảng (Table Row) phải có hiệu ứng hover mượt mà (chuyển màu nền nhẹ, cursor pointer).
- **Skeleton Loading:** Nghiêm cấm dùng Spinner (vòng xoay vô tận) khi tải dữ liệu bảng. Bắt buộc dùng hiệu ứng **Skeleton** nhấp nháy mô phỏng cấu trúc bảng/nội dung.
- **Phản hồi hệ thống (Feedback):** 
  - Thành công/Lỗi nhỏ: Sử dụng **Toast Notifications** (pop-up nhỏ góc phải), tự động biến mất sau 3 giây.
  - Lỗi nghiêm trọng/Xác nhận xoá: Dùng **Modal Dialog** bắt buộc người dùng xác nhận rõ ràng (ví dụ: gõ lại tên cần xóa).
- **Tránh tải lại trang (SPA Feel):** Việc lọc, tìm kiếm, phân trang trên Data Table không được làm tải lại toàn bộ trang (sử dụng State hoặc thay đổi URL query param kết hợp React Query).

## 4. Quy tắc về Bố cục (Layouting)
- Sử dụng Flexbox hoặc CSS Grid để đảm bảo tính Responsive.
- Màn hình Table: Cần có thanh tìm kiếm ở góc trên trái, nút chức năng chính (Thêm mới, Export) ở góc trên phải. Bảng phải có thanh cuộn ngang khi trên màn hình nhỏ.
- Giữ khoảng cách (Padding/Margin) rộng rãi giữa các phần tử để tạo không gian thở (White space), tránh dồn nén thông tin gây ngợp cho người dùng (Giáo vụ/Kế toán).
