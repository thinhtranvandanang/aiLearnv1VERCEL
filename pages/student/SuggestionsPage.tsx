
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getSuggestions } from '../../services/result.service.ts';
import { LearningSuggestionOut } from '../../types/result.types.ts';
import { Card, Badge, Button, LoadingOverlay } from '../../components/common/UI.tsx';
import { ROUTES } from '../../constants/routes.ts';

export const SuggestionsPage: React.FC = () => {
  const { submissionId } = useParams<{ submissionId: string }>();
  const navigate = useNavigate();
  
  const [suggestions, setSuggestions] = useState<LearningSuggestionOut[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!submissionId) return;
    const fetchSuggestions = async () => {
      try {
        const res = await getSuggestions(parseInt(submissionId));
        if (res.status === 'success' && res.data) setSuggestions(res.data);
      } finally {
        setLoading(false);
      }
    };
    fetchSuggestions();
  }, [submissionId]);

  if (loading) return <LoadingOverlay />;

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="mb-12">
        <h1 className="text-3xl font-black text-gray-900 tracking-tight mb-2">Phân tích lộ trình học tập ✨</h1>
        <p className="text-gray-500">Dựa trên kết quả bài làm, AI EduNexia gợi ý bạn cần tập trung vào các mảng kiến thức sau:</p>
      </div>

      <div className="space-y-6">
        {suggestions.length === 0 ? (
          <Card className="p-12 text-center text-gray-400 italic">
            Tuyệt vời! Bạn không có mảng kiến thức nào cần đặc biệt lưu ý sau bài thi này.
          </Card>
        ) : (
          suggestions.map((item, idx) => (
            <Card key={idx} className="p-8 hover:shadow-md transition group">
              <div className="flex flex-col md:flex-row items-start gap-6">
                <div className={`w-14 h-14 rounded-2xl flex items-center justify-center font-black text-xl flex-shrink-0 transition group-hover:scale-110 ${
                  item.priority === 1 ? 'bg-red-100 text-red-600' : 
                  item.priority === 2 ? 'bg-amber-100 text-amber-600' : 'bg-blue-100 text-blue-600'
                }`}>
                  {item.priority === 1 ? '!' : '#'}
                </div>
                <div className="flex-1">
                  <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-3 gap-2">
                    <h2 className="text-xl font-bold text-gray-800">{item.topic}</h2>
                    <Badge variant={item.priority === 1 ? 'danger' : item.priority === 2 ? 'warning' : 'info'}>
                      {item.priority === 1 ? 'Ưu tiên cao' : item.priority === 2 ? 'Cần chú ý' : 'Nâng cao'}
                    </Badge>
                  </div>
                  <p className="text-gray-600 leading-relaxed mb-6">
                    {item.content}
                  </p>
                  <div className="flex flex-wrap gap-4">
                    <Button variant="outline" className="text-xs">Xem tài liệu</Button>
                    <Button variant="outline" className="text-xs">Luyện tập thêm mảng này</Button>
                  </div>
                </div>
              </div>
            </Card>
          ))
        )}
      </div>

      <div className="mt-12 pt-8 border-t flex justify-between items-center">
        <button onClick={() => navigate(-1)} className="text-gray-500 font-bold hover:text-indigo-600 transition">
          ← Quay lại kết quả
        </button>
        <Button onClick={() => navigate(ROUTES.PROTECTED.DASHBOARD)}>Hoàn thành & Về trang chủ</Button>
      </div>
    </div>
  );
};
