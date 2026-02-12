
/**
 * Yêu cầu nộp bài làm trực tuyến
 * Khớp với app.schemas.submission.OnlineSubmissionRequest
 */
export interface OnlineSubmissionRequest {
  /** Object ánh xạ question_id (string) sang student_answer (string) */
  answers: Record<string, string>;
  /** Thời gian bắt đầu làm bài (ISO string) */
  start_time: string;
  /** Thời gian kết thúc/nộp bài (ISO string) */
  end_time: string;
}

/**
 * Phản hồi sau khi nộp bài
 * Khớp với app.schemas.submission.SubmissionResponse
 */
export interface SubmissionResponse {
  id: number;
  /** pending, graded */
  status: string;
  /** Thời gian nộp bài (ISO string) */
  submitted_at: string;
  message: string;
}
