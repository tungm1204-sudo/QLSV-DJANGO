import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * Tiện ích gộp class Tailwind CSS, tránh xung đột class.
 * Dùng thay cho việc nối chuỗi className thủ công.
 */
export function cn(...inputs) {
  return twMerge(clsx(inputs));
}
