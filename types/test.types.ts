
/**
 * Yêu cầu tạo đề luyện tập mới
 * Khớp với app.schemas.test.TestGenerateRequest
 */
export interface TestGenerateRequest {
  subject: string;
  topic: string;
  level: 'easy' | 'medium' | 'hard';
  /** Số lượng câu hỏi (mặc định 10) */
  question_count?: number;
}

/**
 * Tóm tắt thông tin đề thi
 * Khớp với app.schemas.test.TestSummary
 */
export interface TestSummary {
  id: number;
  title: string;
  subject: string;
  question_count: number;
  duration_minutes: number;
  status: 'ready' | 'completed';
}

/**
 * Nội dung một câu hỏi
 * Khớp với app.schemas.test.QuestionOut
 */
export interface QuestionOut {
  id: number;
  content: string;
  /** JSON string chứa các lựa chọn (A, B, C, D) */
  options: string | null;
}

/**
 * Nội dung đầy đủ của một đề thi bao gồm câu hỏi
 * Khớp với app.schemas.test.TestContent
 */
export interface TestContent extends TestSummary {
  questions: QuestionOut[];
}
