
import { apiClient } from './api.config.ts';
import { HistorySummary, ResultOut } from '../types/result.types.ts';
import { UserOut } from '../types/auth.types.ts';
import { APIResponse } from '../types/api.types.ts';

/**
 * Lấy thông tin cá nhân của người dùng hiện tại
 */
export async function getMe(): Promise<APIResponse<UserOut>> {
  const response = await apiClient.get<APIResponse<UserOut>>('/auth/student/me');
  return response.data;
}

/**
 * Lấy tổng quan lịch sử học tập và thống kê xu hướng
 */
export async function getHistory(): Promise<APIResponse<HistorySummary>> {
  const response = await apiClient.get<APIResponse<HistorySummary>>('/students/me/learning-history');
  return response.data;
}

/**
 * Xem lại chi tiết kết quả của một bài thi cũ trong lịch sử
 * @param {number} submissionId - ID bài làm cũ
 */
export async function getHistoryDetail(submissionId: number): Promise<APIResponse<ResultOut>> {
  const response = await apiClient.get<APIResponse<ResultOut>>(`/students/me/learning-history/${submissionId}`);
  return response.data;
}
