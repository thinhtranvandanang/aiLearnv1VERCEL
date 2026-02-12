
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { generateTest } from '../../services/test.service.ts';
import { Card, Button, Input, LoadingOverlay } from '../../components/common/UI.tsx';
import { ROUTES } from '../../constants/routes.ts';

export const CreateTestPage: React.FC = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const formData = new FormData(e.currentTarget);
    const data = {
      subject: formData.get('subject') as string,
      topic: formData.get('topic') as string,
      level: formData.get('level') as any,
      question_count: parseInt(formData.get('count') as string)
    };

    try {
      const res = await generateTest(data);
      if (res.status === 'success' && res.data) {
        navigate(ROUTES.PROTECTED.PRACTICE_TEST.replace(':testId', res.data.test_id.toString()));
      } else {
        setError(res.message || 'Không thể tạo đề vào lúc này');
      }
    } catch (err: any) {
      setError(err.message || 'Đã xảy ra lỗi hệ thống');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto px-4 py-12">
      {loading && <LoadingOverlay />}
      
      <div className="mb-8 text-center">
        <h1 className="text-3xl font-black text-gray-900">Thiết lập đề luyện tập</h1>
        <p className="text-gray-500 mt-2">Chọn tiêu chí để AI lắp ráp đề thi phù hợp nhất với bạn.</p>
      </div>

      <Card className="p-8">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-2">Môn học</label>
              <select name="subject" className="w-full px-4 py-2 bg-gray-50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none" required>
                <option value="Toán học">Toán học</option>
                <option value="Vật lý">Vật lý</option>
                <option value="Hóa học">Hóa học</option>
                <option value="Tiếng Anh">Tiếng Anh</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-2">Độ khó</label>
              <select name="level" className="w-full px-4 py-2 bg-gray-50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none" required>
                <option value="easy">Dễ (Cơ bản)</option>
                <option value="medium">Trung bình (Vận dụng)</option>
                <option value="hard">Khó (Nâng cao)</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-bold text-gray-700 mb-2">Chủ đề cụ thể</label>
            <select name="topic" className="w-full px-4 py-2 bg-gray-50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none" required>
              <option value="">-- Chọn chủ đề --</option>
              <option value="Đạo hàm">Đạo hàm</option>
              <option value="Sóng cơ">Sóng cơ</option>
              <option value="Phản ứng oxi-hóa khử">Phản ứng oxi-hóa khử</option>
              <option value="Câu bị động">Câu bị động</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-bold text-gray-700 mb-2">Số lượng câu hỏi: <span className="text-indigo-600">1</span></label>
            <input type="range" name="count" min="1" max="3" defaultValue="1" className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-600" />
            <div className="flex justify-between text-xs text-gray-400 mt-2">
              <span>1 câu</span>
              <span>2 câu</span>
              <span>3 câu</span>
            </div>
          </div>

          {error && <div className="p-4 bg-red-50 text-red-600 rounded-xl text-sm font-bold">{error}</div>}

          <div className="pt-4 flex gap-4">
            <Button type="button" variant="outline" className="flex-1" onClick={() => navigate(-1)}>Quay lại</Button>
            <Button type="submit" className="flex-[2]">Bắt đầu làm bài</Button>
          </div>
        </form>
      </Card>
    </div>
  );
};
