
import { apiClient } from './api.config.ts';
import { TestGenerateRequest, TestContent } from '../types/test.types.ts';
import { APIResponse } from '../types/api.types.ts';

/**
 * Yêu cầu hệ thống tạo một đề thi mới dựa trên tiêu chí
 * @param {TestGenerateRequest} data - Môn học, chủ đề, độ khó
 * @returns {Promise<APIResponse<{test_id: number, title: string}>>}
 */
export async function generateTest(data: TestGenerateRequest): Promise<APIResponse<{test_id: number, title: string}>> {
  const response = await apiClient.post<APIResponse<{test_id: number, title: string}>>('/practice-tests/generate', data);
  return response.data;
}

/**
 * Lấy nội dung đầy đủ của đề thi (bao gồm danh sách câu hỏi)
 * @param {number} testId - ID của đề thi
 * @returns {Promise<APIResponse<TestContent>>}
 */
export async function getTestContent(testId: number): Promise<APIResponse<TestContent>> {
  const response = await apiClient.get<APIResponse<TestContent>>(`/practice-tests/${testId}/content`);
  return response.data;
}

/**
 * Lấy URL để tải đề thi dưới dạng file (PDF/DOCX)
 * @param {number} testId - ID của đề thi
 * @param {string} format - Định dạng 'pdf' hoặc 'docx'
 */
export async function downloadTest(testId: number, format: 'pdf' | 'docx' = 'pdf'): Promise<APIResponse<{url: string}>> {
  const response = await apiClient.get<APIResponse<{url: string}>>(`/practice-tests/${testId}/download`, {
    params: { format }
  });
  return response.data;
}
