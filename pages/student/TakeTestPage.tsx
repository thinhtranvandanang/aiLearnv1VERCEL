
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getTestContent } from '../../services/test.service.ts';
import { submitOnline } from '../../services/submission.service.ts';
import { TestContent, QuestionOut } from '../../types/test.types.ts';
import { Card, Button, Badge, LoadingOverlay } from '../../components/common/UI.tsx';
import { ROUTES } from '../../constants/routes.ts';

interface ProcessedQuestion extends Omit<QuestionOut, 'options'> {
  parsedOptions: Record<string, string>;
}

interface ProcessedTest extends Omit<TestContent, 'questions'> {
  questions: ProcessedQuestion[];
}

export const TakeTestPage: React.FC = () => {
  const { testId } = useParams<{ testId: string }>();
  const navigate = useNavigate();
  
  const [test, setTest] = useState<ProcessedTest | null>(null);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [timeLeft, setTimeLeft] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [startTime] = useState(new Date().toISOString());

  useEffect(() => {
    if (!testId) return;
    const fetchTest = async () => {
      try {
        const res = await getTestContent(parseInt(testId));
        if (res.status === 'success' && res.data) {
          const processedQuestions: ProcessedQuestion[] = res.data.questions.map(q => ({
            ...q,
            parsedOptions: q.options ? JSON.parse(q.options) : { A: '', B: '', C: '', D: '' }
          }));
          
          setTest({
            ...res.data,
            questions: processedQuestions
          });
          setTimeLeft(res.data.duration_minutes * 60);
        } else {
          setError(res.message || 'Không thể tải đề thi');
        }
      } catch (err: any) {
        setError(err.message || 'Đã xảy ra lỗi khi kết nối máy chủ');
      } finally {
        setLoading(false);
      }
    };
    fetchTest();
  }, [testId]);

  useEffect(() => {
    if (timeLeft <= 0 || !test) return;
    const timer = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 1) {
          clearInterval(timer);
          handleSubmit(true);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(timer);
  }, [timeLeft, test]);

  const handleOptionSelect = (questionId: number, optionKey: string) => {
    setAnswers(prev => ({ ...prev, [questionId.toString()]: optionKey }));
  };

  const handleSubmit = async (isAuto = false) => {
    if (!testId || isSubmitting) return;
    if (!isAuto && !window.confirm('Bạn có chắc chắn muốn nộp bài?')) return;

    setIsSubmitting(true);
    try {
      const res = await submitOnline(parseInt(testId), {
        answers,
        start_time: startTime,
        end_time: new Date().toISOString()
      });
      if (res.status === 'success' && res.data) {
        navigate(ROUTES.PROTECTED.RESULT.replace(':submissionId', res.data.submission_id.toString()));
      }
    } catch (err: any) {
      alert(err.message || 'Nộp bài thất bại');
    } finally {
      setIsSubmitting(false);
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (loading) return <LoadingOverlay />;
  if (error) return <div className="p-20 text-center text-red-600 font-bold">{error}</div>;
  if (!test) return null;

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      <nav className="bg-white border-b sticky top-0 z-40 shadow-sm p-4">
        <div className="max-w-5xl mx-auto flex justify-between items-center">
          <div>
            <h1 className="font-black text-gray-900">{test.title}</h1>
            <Badge variant="info">{test.subject}</Badge>
          </div>
          <div className={`px-6 py-2 rounded-2xl font-black text-xl border-2 ${timeLeft < 300 ? 'border-red-500 text-red-600 animate-pulse' : 'border-indigo-600 text-indigo-600'}`}>
            {formatTime(timeLeft)}
          </div>
          <Button onClick={() => handleSubmit()} isLoading={isSubmitting}>Nộp bài</Button>
        </div>
      </nav>

      <div className="max-w-3xl mx-auto px-4 py-8 space-y-8">
        {test.questions.map((q, idx) => (
          <Card key={q.id} className="p-8">
            <div className="flex gap-4 mb-6">
              <span className="w-10 h-10 bg-indigo-600 text-white rounded-xl flex items-center justify-center font-black flex-shrink-0">
                {idx + 1}
              </span>
              <p className="text-lg font-bold text-gray-800 leading-relaxed pt-1">{q.content}</p>
            </div>
            <div className="grid grid-cols-1 gap-3 ml-14">
              {Object.entries(q.parsedOptions).map(([key, value]) => (
                <button
                  key={key}
                  onClick={() => handleOptionSelect(q.id, key)}
                  className={`p-4 rounded-xl border-2 text-left transition-all flex items-center gap-4 group ${
                    answers[q.id.toString()] === key 
                    ? 'border-indigo-600 bg-indigo-50 text-indigo-700' 
                    : 'border-gray-100 hover:border-indigo-200 hover:bg-gray-50 text-gray-600'
                  }`}
                >
                  <span className={`w-8 h-8 rounded-lg flex items-center justify-center font-black text-sm border-2 transition-colors ${
                    answers[q.id.toString()] === key ? 'bg-indigo-600 text-white border-indigo-600' : 'bg-white border-gray-200 group-hover:border-indigo-300'
                  }`}>
                    {key}
                  </span>
                  <span className="font-medium">{value}</span>
                </button>
              ))}
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
