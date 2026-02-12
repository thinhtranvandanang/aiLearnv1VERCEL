
import { apiClient } from './api.config.ts';
import { LoginRequest, UserCreate, Token } from '../types/auth.types.ts';
import { APIResponse } from '../types/api.types.ts';

/**
 * Thực hiện đăng nhập vào hệ thống
 * @param {LoginRequest} credentials - Tên đăng nhập và mật khẩu
 */
export async function login(credentials: LoginRequest): Promise<APIResponse<Token>> {
  const response = await apiClient.post<APIResponse<Token>>('/auth/student/login', credentials);
  return response.data;
}

/**
 * Thực hiện đăng ký tài khoản mới
 * @param {UserCreate} data - Thông tin đăng ký
 */
export async function register(data: UserCreate): Promise<APIResponse<Token>> {
  const response = await apiClient.post<APIResponse<Token>>('/auth/student/register', data);
  return response.data;
}
