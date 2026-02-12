
import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext.tsx';
import { ROUTES } from '../constants/routes.ts';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

/**
 * ProtectedRoute: Bảo vệ các tài nguyên yêu cầu Authentication.
 */
export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { token, isLoading } = useAuth();
  const location = useLocation();

  // Hiển thị trạng thái loading nếu AuthContext chưa load xong dữ liệu từ LocalStorage/API
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="w-12 h-12 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  // Nếu không có token, redirect về login và lưu lại trang đang truy cập để quay lại sau
  if (!token) {
    return <Navigate to={ROUTES.PUBLIC.LOGIN} state={{ from: location }} replace />;
  }

  return <>{children}</>;
};
