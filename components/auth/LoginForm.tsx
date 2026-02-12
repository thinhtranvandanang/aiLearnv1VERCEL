
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Button, Input } from '../common/UI';
import { ROUTES } from '../../constants/routes';

export const LoginForm: React.FC = () => {
  const { login, isLoading } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    const formData = new FormData(e.currentTarget);
    const username = formData.get('username') as string;
    const password = formData.get('password') as string;

    try {
      await login({ username, password });
      navigate(ROUTES.PROTECTED.DASHBOARD);
    } catch (err: any) {
      setError(err.message || 'Đăng nhập thất bại. Kiểm tra lại thông tin.');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      <Input 
        name="username" 
        label="Tên đăng nhập" 
        placeholder="Nhập username của bạn" 
        className="bg-white border-gray-200 rounded-2xl"
        required 
      />
      <Input 
        name="password" 
        label="Mật khẩu" 
        type="password" 
        placeholder="••••••••" 
        className="bg-white border-gray-200 rounded-2xl"
        required 
      />

      {error && (
        <div className="p-4 bg-red-50 border border-red-100 text-red-600 text-xs rounded-xl font-bold flex items-center gap-3">
          <span className="w-5 h-5 bg-red-100 text-red-600 rounded-full flex items-center justify-center flex-shrink-0">!</span>
          {error}
        </div>
      )}

      <Button type="submit" isLoading={isLoading} className="w-full py-4 rounded-2xl shadow-lg shadow-indigo-100">
        Đăng nhập ngay
      </Button>
    </form>
  );
};
