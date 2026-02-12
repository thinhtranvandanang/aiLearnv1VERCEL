
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getHistory } from '../../services/student.service.ts';
import { HistorySummary, RecentTestSummary } from '../../types/result.types.ts';
import { Card, Badge, Button } from '../../components/common/UI.tsx';
import { useAuth } from '../../context/AuthContext.tsx';
import { ROUTES } from '../../constants/routes.ts';

export const DashboardPage: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [history, setHistory] = useState<HistorySummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await getHistory();
        if (res.status === 'success' && res.data) setHistory(res.data);
      } catch (err) {
        console.error("Dashboard: Error fetching history", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Chào buổi sáng, {user?.full_name}! 👋</h1>
        <p className="text-gray-500">Cùng xem hôm nay chúng ta có gì mới nào.</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card className="p-6 border-l-4 border-indigo-500">
              <p className="text-xs font-bold text-gray-400 uppercase">Tổng số bài</p>
              <p className="text-4xl font-black text-indigo-600 mt-1">{history?.total_tests || 0}</p>
            </Card>
            <Card className="p-6 border-l-4 border-green-500">
              <p className="text-xs font-bold text-gray-400 uppercase">Điểm trung bình</p>
              <p className="text-4xl font-black text-green-600 mt-1">{history?.average_score || 0}</p>
            </Card>
            <Card className="p-6 border-l-4 border-amber-500">
              <p className="text-xs font-bold text-gray-400 uppercase">Xu hướng</p>
              <p className="text-2xl font-black text-amber-600 mt-1 leading-tight">{history?.progress_trend || 'Chưa cập nhật'}</p>
            </Card>
          </div>

          <Card>
            <div className="p-6 border-b flex justify-between items-center bg-gray-50/50">
              <h2 className="font-bold text-gray-800">Lịch sử làm bài gần đây</h2>
              <Button variant="outline" className="text-sm">Xem tất cả</Button>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 text-left">
                  <tr>
                    <th className="px-6 py-4 text-xs font-bold text-gray-500 uppercase">Bài thi</th>
                    <th className="px-6 py-4 text-xs font-bold text-gray-500 uppercase text-center">Điểm</th>
                    <th className="px-6 py-4 text-xs font-bold text-gray-500 uppercase">Ngày làm</th>
                    <th className="px-6 py-4"></th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {loading ? (
                    <tr><td colSpan={4} className="p-12 text-center text-gray-400">Đang tải dữ liệu...</td></tr>
                  ) : !history || history.recent_tests.length === 0 ? (
                    <tr><td colSpan={4} className="p-12 text-center text-gray-400">Bạn chưa thực hiện bài thi nào.</td></tr>
                  ) : (
                    history.recent_tests.map((test: RecentTestSummary) => (
                      <tr key={test.id} className="hover:bg-gray-50 transition">
                        <td className="px-6 py-4 font-bold text-gray-800">{test.test_title}</td>
                        <td className="px-6 py-4 text-center">
                          <Badge variant={test.score >= 5 ? 'success' : 'danger'}>{test.score}/10</Badge>
                        </td>
                        <td className="px-6 py-4 text-gray-500">{new Date(test.submitted_at).toLocaleDateString('vi-VN')}</td>
                        <td className="px-6 py-4 text-right">
                          <Button 
                            variant="outline" 
                            className="text-xs px-3" 
                            onClick={() => navigate(ROUTES.PROTECTED.RESULT.replace(':submissionId', test.id.toString()))}
                          >
                            Chi tiết
                          </Button>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </Card>
        </div>

        <div className="space-y-6">
          <div className="bg-indigo-600 rounded-3xl p-8 text-white shadow-xl shadow-indigo-200 relative overflow-hidden">
            <div className="relative z-10">
              <h3 className="text-2xl font-black mb-2">Luyện tập ngay!</h3>
              <p className="text-indigo-100 mb-6 text-sm opacity-90">Hệ thống AI sẽ tạo đề thi cá nhân hóa dựa trên học lực của bạn.</p>
              <Button 
                variant="secondary" 
                className="w-full bg-white text-indigo-600 hover:bg-indigo-50" 
                onClick={() => navigate(ROUTES.PROTECTED.PRACTICE_SETUP)}
              >
                Tạo đề luyện tập
              </Button>
            </div>
            <div className="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -mr-16 -mt-16"></div>
          </div>

          <Card className="p-6">
            <h3 className="font-bold text-gray-800 mb-4">Phím tắt nhanh</h3>
            <div className="space-y-3">
              <button 
                className="w-full flex items-center gap-4 p-4 rounded-2xl border border-gray-100 hover:border-indigo-200 hover:bg-indigo-50/30 transition group"
                onClick={() => navigate(ROUTES.PROTECTED.PRACTICE_SETUP)}
              >
                <div className="w-10 h-10 bg-blue-100 text-blue-600 rounded-xl flex items-center justify-center group-hover:scale-110 transition">
                  🚀
                </div>
                <div className="text-left">
                  <p className="font-bold text-sm text-gray-800">Tạo đề mới</p>
                  <p className="text-xs text-gray-500">Cấu hình nhanh bởi AI</p>
                </div>
              </button>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};
