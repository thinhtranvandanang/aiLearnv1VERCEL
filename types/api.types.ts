
/**
 * Cấu trúc phản hồi chuẩn từ EduNexia API
 * Khớp với app.core.response.APIResponse trong Backend
 */
export interface APIResponse<T = any> {
  /** Trạng thái phản hồi: "success" hoặc "error" */
  status: 'success' | 'error';
  /** Thông báo chi tiết từ hệ thống (nếu có) */
  message: string | null;
  /** Dữ liệu trả về thuộc kiểu T */
  data: T | null;
}

/**
 * Cấu trúc lỗi nghiệp vụ từ hệ thống
 */
export interface APIError {
  status: 'error';
  message: string;
}
