
import { apiClient } from './api.config.ts';
import { ResultOut, LearningSuggestionOut } from '../types/result.types.ts';
import { APIResponse } from '../types/api.types.ts';

/**
 * Lấy điểm số và feedback chi tiết từng câu cho một bài nộp
 * @param {number} submissionId - ID bài làm
 */
export async function getResult(submissionId: number): Promise<APIResponse<ResultOut>> {
  const response = await apiClient.get<APIResponse<ResultOut>>(`/submissions/${submissionId}/result`);
  return response.data;
}

/**
 * Lấy danh sách gợi ý kiến thức cần ôn tập dựa trên kết quả bài làm
 * @param {number} submissionId - ID bài làm
 */
export async function getSuggestions(submissionId: number): Promise<APIResponse<LearningSuggestionOut[]>> {
  const response = await apiClient.get<APIResponse<LearningSuggestionOut[]>>(`/submissions/${submissionId}/learning-suggestions`);
  return response.data;
}
