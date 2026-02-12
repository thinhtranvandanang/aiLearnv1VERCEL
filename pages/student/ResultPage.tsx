
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getResult } from '../../services/result.service.ts';
import { ResultOut } from '../../types/result.types.ts';
import { Card, Badge, Button, LoadingOverlay } from '../../components/common/UI.tsx';
import { ROUTES } from '../../constants/routes.ts';

export const ResultPage: React.FC = () => {
  const { submissionId } = useParams<{ submissionId: string }>();
  const navigate = useNavigate();
  
  const [result, setResult] = useState<ResultOut | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!submissionId) return;
    const fetchResult = async () => {
      try {
        const res = await getResult(parseInt(submissionId));
        if (res.status === 'success' && res.data) {
          // Parse feedback_details from JSON string to array
          const resultData = {
            ...res.data,
            feedback: JSON.parse((res.data as any).feedback_details || '[]')
          };
          setResult(resultData);
        }
      } catch (err) {
        console.error('Error fetching result:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchResult();
  }, [submissionId]);

  if (loading) return <LoadingOverlay />;
  if (!result) return <div className="p-20 text-center">Không tìm thấy kết quả.</div>;

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="text-center mb-12">
        <div className="inline-flex items-center justify-center w-32 h-32 rounded-full border-8 border-indigo-50 bg-white shadow-xl mb-6">
          <span className="text-5xl font-black text-indigo-600">{result.score}</span>
          <span className="text-xl font-bold text-gray-400">/10</span>
        </div>
        <h1 className="text-3xl font-black text-gray-900 uppercase tracking-tight">Kết quả bài luyện tập</h1>
        <p className="text-gray-500 mt-2">Chúc mừng bạn đã hoàn thành bài thi! Hãy xem lại các lỗi sai.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <Card className="p-6 text-center bg-green-50 border-green-100">
          <p className="text-xs font-bold text-green-600 uppercase">Câu đúng</p>
          <p className="text-3xl font-black text-green-700">{result.correct_answers}</p>
        </Card>
        <Card className="p-6 text-center bg-red-50 border-red-100">
          <p className="text-xs font-bold text-red-600 uppercase">Câu sai</p>
          <p className="text-3xl font-black text-red-700">{result.wrong_answers}</p>
        </Card>
        <Card className="p-6 text-center bg-indigo-50 border-indigo-100">
          <p className="text-xs font-bold text-indigo-600 uppercase">Tổng số câu</p>
          <p className="text-3xl font-black text-indigo-700">{result.total_questions}</p>
        </Card>
      </div>

      <div className="space-y-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold text-gray-800">Chi tiết từng câu</h2>
          <Button onClick={() => navigate(ROUTES.PROTECTED.SUGGESTIONS.replace(':submissionId', submissionId!))}>
            Xem gợi ý từ AI ✨
          </Button>
        </div>

        {result.feedback.map((fb, idx) => (
          <Card key={fb.question_id} className={`p-6 border-l-4 ${fb.is_correct ? 'border-green-500' : 'border-red-500'}`}>
            <div className="flex justify-between items-start mb-4">
              <span className="font-bold text-gray-400">Câu {idx + 1}</span>
              <Badge variant={fb.is_correct ? 'success' : 'danger'}>
                {fb.is_correct ? 'Chính xác' : 'Chưa đúng'}
              </Badge>
            </div>
            
            <div className="space-y-4">
              <div className="flex flex-col md:flex-row gap-4">
                <div className="flex-1">
                  <p className="text-sm text-gray-500 mb-1">Đáp án của bạn:</p>
                  <p className={`font-bold ${fb.is_correct ? 'text-green-600' : 'text-red-600'}`}>{fb.student_answer || 'Chưa trả lời'}</p>
                </div>
                {!fb.is_correct && (
                  <div className="flex-1">
                    <p className="text-sm text-gray-500 mb-1">Đáp án đúng:</p>
                    <p className="font-bold text-green-600">{fb.correct_answer}</p>
                  </div>
                )}
              </div>

              <div className="bg-gray-50 p-4 rounded-xl">
                <p className="text-xs font-bold text-gray-400 uppercase mb-2">Lời giải thích:</p>
                <p className="text-sm text-gray-700 italic leading-relaxed">{fb.explanation}</p>
              </div>
            </div>
          </Card>
        ))}
      </div>

      <div className="mt-12 flex justify-center gap-4">
        <Button variant="outline" onClick={() => navigate(ROUTES.PROTECTED.DASHBOARD)}>Về Dashboard</Button>
        <Button onClick={() => navigate(ROUTES.PROTECTED.PRACTICE_SETUP)}>Làm đề mới</Button>
      </div>
    </div>
  );
};
