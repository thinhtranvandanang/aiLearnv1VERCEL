
import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext.tsx';
import { ROUTES } from '../constants/routes.ts';

/**
 * RootRedirectPage: Xử lý điều hướng tại route gốc "/".
 * Đảm bảo các import đều có phần mở rộng .tsx/.ts.
 */
export const RootRedirectPage: React.FC = () => {
  const { token, isLoading } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isLoading) {
      if (token) {
        navigate(ROUTES.PROTECTED.DASHBOARD, { replace: true });
      } else {
        navigate(ROUTES.PUBLIC.LOGIN, { replace: true });
      }
    }
  }, [token, isLoading, navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-white">
      <div className="flex flex-col items-center">
        <div className="w-12 h-12 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin mb-6"></div>
        <div className="flex flex-col items-center gap-1">
          <span className="text-2xl font-black text-indigo-600 italic tracking-tighter">EduNexia</span>
          <span className="text-gray-400 text-[10px] font-black uppercase tracking-[0.3em]">AI Learning Engine</span>
        </div>
      </div>
    </div>
  );
};
