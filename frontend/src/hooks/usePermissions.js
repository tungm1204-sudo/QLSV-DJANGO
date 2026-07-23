import useAuthStore from '../features/auth/store/useAuthStore';

/**
 * usePermissions - Custom hook tập trung logic đọc quyền hạn của user hiện tại.
 * Lý do: Tránh lặp code (DRY) giữa các trang. Mỗi trang chỉ cần import hook này
 * thay vì tự viết lại `user?.role?.permissions || []` ở khắp nơi.
 * 
 * @returns {object} - Các hàm và trạng thái liên quan đến quyền hạn
 *   - `permissions`: Danh sách quyền dạng string[] của user hiện tại
 *   - `hasPermission(perm)`: Kiểm tra user có quyền cụ thể không
 *   - `hasAnyPermission(perms[])`: Kiểm tra user có ít nhất 1 trong các quyền không
 *   - `hasAllPermissions(perms[])`: Kiểm tra user có đủ tất cả các quyền không
 */
export function usePermissions() {
  const { user } = useAuthStore();
  const permissions = user?.role?.permissions || [];

  const hasPermission = (perm) => permissions.includes('*') || permissions.includes(perm);

  const hasAnyPermission = (perms) => permissions.includes('*') || perms.some((p) => permissions.includes(p));

  const hasAllPermissions = (perms) => permissions.includes('*') || perms.every((p) => permissions.includes(p));

  return {
    permissions,
    hasPermission,
    hasAnyPermission,
    hasAllPermissions,
  };
}
