
/**
 * Tóm tắt một bài thi gần đây trong lịch sử
 */
export interface RecentTestSummary {
  id: number;
  test_title: string;
  score: number;
  submitted_at: string;
}

/**
 * Chi tiết feedback cho từng câu hỏi
 * Khớp với app.schemas.result.QuestionFeedback
 */
export interface QuestionFeedback {
  question_id: number;
  student_answer: string;
  correct_answer: string;
  is_correct: boolean;
  explanation: string;
}

/**
 * Kết quả chấm điểm đầy đủ
 * Khớp với app.schemas.result.ResultOut
 */
export interface ResultOut {
  submission_id: number;
  score: number;
  total_questions: number;
  correct_answers: number;
  wrong_answers: number;
  feedback: QuestionFeedback[];
}

/**
 * Gợi ý học tập
 * Khớp với app.schemas.result.LearningSuggestionOut
 */
export interface LearningSuggestionOut {
  topic: string;
  /** 1: high, 2: medium, 3: low */
  priority: number;
  content: string;
}

/**
 * Tổng hợp lịch sử học tập
 * Khớp với app.schemas.result.HistorySummary
 */
export interface HistorySummary {
  total_tests: number;
  average_score: number;
  progress_trend: string;
  /** Danh sách các bài thi gần đây đã được định nghĩa type */
  recent_tests: RecentTestSummary[];
}
