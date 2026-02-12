
/**
 * Thông tin JWT Token trả về sau khi login/register
 * Khớp với app.schemas.auth.Token
 */
export interface Token {
  access_token: string;
  token_type: string;
  /** Đính kèm thông tin user (tùy chỉnh trong auth_service.py) */
  user?: UserOut;
}

/**
 * Payload của Token
 * Khớp với app.schemas.auth.TokenPayload
 */
export interface TokenPayload {
  sub: number | null;
}

/**
 * Yêu cầu đăng nhập
 * Khớp với app.schemas.auth.LoginRequest
 */
export interface LoginRequest {
  username: string;
  password: string;
}

/**
 * Thông tin cơ bản của User
 * Khớp với app.schemas.auth.UserBase
 */
export interface UserBase {
  username: string;
  email: string;
  full_name: string;
  role: 'student' | 'admin' | 'teacher';
}

/**
 * Yêu cầu đăng ký tài khoản mới
 */
export interface UserCreate extends UserBase {
  password: string;
}

/**
 * Thông tin User trả về từ API
 * Khớp với app.schemas.auth.UserOut
 */
export interface UserOut extends UserBase {
  id: number;
  is_active: boolean;
}
