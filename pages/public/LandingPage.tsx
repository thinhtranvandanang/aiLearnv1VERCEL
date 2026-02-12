
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext.tsx';
import { ROUTES } from '../../constants/routes.ts';
import { Button, Card } from '../../components/common/UI.tsx';

export const LandingPage: React.FC = () => {
  const { token } = useAuth();
  const navigate = useNavigate();

  const handleCTA = () => {
    if (token) {
      navigate(ROUTES.PROTECTED.DASHBOARD);
    } else {
      navigate(ROUTES.PUBLIC.LOGIN);
    }
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Header thon gọn */}
      <nav className="border-b bg-white/80 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 h-16 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <span className="text-2xl font-black text-indigo-600 italic tracking-tighter">EduNexia</span>
          </div>
          <div className="flex items-center gap-4">
            {!token ? (
              <>
                <button 
                  onClick={() => navigate(ROUTES.PUBLIC.LOGIN)}
                  className="text-sm font-bold text-gray-600 hover:text-indigo-600 transition"
                >
                  Đăng nhập
                </button>
                <Button onClick={() => navigate(ROUTES.PUBLIC.LOGIN)} className="text-sm">Tham gia ngay</Button>
              </>
            ) : (
              <Button onClick={() => navigate(ROUTES.PROTECTED.DASHBOARD)} variant="outline" className="text-sm">Vào Dashboard</Button>
            )}
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative pt-20 pb-32 overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 text-center relative z-10">
          <div className="inline-block px-4 py-1.5 mb-6 rounded-full bg-indigo-50 border border-indigo-100 text-indigo-600 text-xs font-black uppercase tracking-widest animate-bounce">
            AI Powered Learning Platform
          </div>
          <h1 className="text-5xl md:text-7xl font-black text-gray-900 leading-[1.1] tracking-tighter mb-8">
            Nâng Tầm Tri Thức <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-violet-600">Với Công Nghệ AI</span>
          </h1>
          <p className="max-w-2xl mx-auto text-lg text-gray-500 mb-10 font-medium leading-relaxed">
            Hệ thống luyện tập thông minh giúp cá nhân hóa lộ trình học tập, 
            tự động tạo đề thi và phân tích lỗ hổng kiến thức trong tích tắc.
          </p>
          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <Button onClick={handleCTA} className="px-10 py-5 text-lg rounded-2xl shadow-xl shadow-indigo-200">
              {token ? 'Tiếp tục học tập' : 'Bắt đầu miễn phí'}
            </Button>
            <Button variant="outline" className="px-10 py-5 text-lg rounded-2xl">Xem bản demo</Button>
          </div>
        </div>
        
        {/* Background Decor */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full -z-0 opacity-20 pointer-events-none">
          <div className="absolute top-20 left-10 w-72 h-72 bg-indigo-400 rounded-full blur-[120px]"></div>
          <div className="absolute bottom-20 right-10 w-96 h-96 bg-violet-400 rounded-full blur-[120px]"></div>
        </div>
      </section>

      {/* Features */}
      <section className="py-24 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-black text-gray-900 tracking-tight">Tính năng đột phá</h2>
            <div className="h-1.5 w-20 bg-indigo-600 mx-auto mt-4 rounded-full"></div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Card className="p-8 group hover:-translate-y-2 transition duration-300">
              <div className="w-14 h-14 bg-indigo-100 text-indigo-600 rounded-2xl flex items-center justify-center text-2xl mb-6 group-hover:bg-indigo-600 group-hover:text-white transition">
                🎯
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">Luyện tập thông minh</h3>
              <p className="text-gray-500 leading-relaxed">AI tự động lắp ráp đề thi dựa trên mục tiêu và độ khó bạn mong muốn.</p>
            </Card>

            <Card className="p-8 group hover:-translate-y-2 transition duration-300">
              <div className="w-14 h-14 bg-violet-100 text-violet-600 rounded-2xl flex items-center justify-center text-2xl mb-6 group-hover:bg-violet-600 group-hover:text-white transition">
                📸
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">Chấm điểm OCR</h3>
              <p className="text-gray-500 leading-relaxed">Chỉ cần chụp ảnh bài làm, hệ thống sẽ tự động nhận diện và chấm điểm ngay.</p>
            </Card>

            <Card className="p-8 group hover:-translate-y-2 transition duration-300">
              <div className="w-14 h-14 bg-blue-100 text-blue-600 rounded-2xl flex items-center justify-center text-2xl mb-6 group-hover:bg-blue-600 group-hover:text-white transition">
                📊
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">Phân tích lộ trình</h3>
              <p className="text-gray-500 leading-relaxed">Gợi ý kiến thức cần ôn tập dựa trên các lỗi sai thường gặp trong quá khứ.</p>
            </Card>
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="py-20 bg-indigo-600 text-white">
        <div className="max-w-7xl mx-auto px-4 grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          <div>
            <p className="text-4xl font-black mb-1">10K+</p>
            <p className="text-indigo-100 text-sm font-bold uppercase tracking-widest">Học sinh</p>
          </div>
          <div>
            <p className="text-4xl font-black mb-1">50K+</p>
            <p className="text-indigo-100 text-sm font-bold uppercase tracking-widest">Đề thi</p>
          </div>
          <div>
            <p className="text-4xl font-black mb-1">98%</p>
            <p className="text-indigo-100 text-sm font-bold uppercase tracking-widest">Hài lòng</p>
          </div>
          <div>
            <p className="text-4xl font-black mb-1">24/7</p>
            <p className="text-indigo-100 text-sm font-bold uppercase tracking-widest">Hỗ trợ AI</p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 border-t">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <span className="text-2xl font-black text-indigo-600 italic tracking-tighter">EduNexia</span>
          <p className="text-gray-400 text-sm mt-4 font-medium">&copy; 2024 EduNexia Smart Learning System.</p>
        </div>
      </footer>
    </div>
  );
};
