
import { apiClient } from './api.config.ts';
import { OnlineSubmissionRequest, SubmissionResponse } from '../types/submission.types.ts';
import { APIResponse } from '../types/api.types.ts';

/**
 * Nộp đáp án bài làm trực tiếp trên giao diện web
 * @param {number} testId - ID đề thi
 * @param {OnlineSubmissionRequest} data - Đáp án và thời gian làm bài
 */
export async function submitOnline(testId: number, data: OnlineSubmissionRequest): Promise<APIResponse<{submission_id: number}>> {
  const response = await apiClient.post<APIResponse<{submission_id: number}>>(`/practice-tests/${testId}/submit-online`, data);
  return response.data;
}

/**
 * Nộp bài làm qua ảnh chụp hoặc file (Nghiệp vụ Offline)
 * @param {number} testId - ID đề thi
 * @param {File} file - File ảnh hoặc PDF bài làm
 */
export async function submitOffline(testId: number, file: File): Promise<APIResponse<{submission_id: number}>> {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await apiClient.post<APIResponse<{submission_id: number}>>(`/practice-tests/${testId}/submit-offline`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
}
