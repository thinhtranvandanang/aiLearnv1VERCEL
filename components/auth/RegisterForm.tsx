
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Button, Input } from '../common/UI';
import { ROUTES } from '../../constants/routes';

export const RegisterForm: React.FC = () => {
  const { register, isLoading } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    const formData = new FormData(e.currentTarget);
    
    const fullName = formData.get('fullName') as string;
    const email = formData.get('email') as string;
    const username = formData.get('username') as string;
    const password = formData.get('password') as string;
    const confirmPassword = formData.get('confirmPassword') as string;

    if (password !== confirmPassword) {
      setError('Mật khẩu xác nhận không trùng khớp.');
      return;
    }

    try {
      await register({
        full_name: fullName,
        email: email,
        username: username,
        password: password,
        role: 'student'
      });
      navigate(ROUTES.PROTECTED.DASHBOARD);
    } catch (err: any) {
      setError(err.message || 'Đăng ký thất bại. Vui lòng thử lại sau.');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input name="fullName" label="Họ và tên" placeholder="Ví dụ: Nguyễn Văn A" className="rounded-2xl" required />
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Input name="email" label="Email" type="email" placeholder="email@example.com" className="rounded-2xl" required />
        <Input name="username" label="Tên đăng nhập" placeholder="hocsinh_01" className="rounded-2xl" required />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Input name="password" label="Mật khẩu" type="password" placeholder="••••••••" className="rounded-2xl" required />
        <Input name="confirmPassword" label="Nhập lại mật khẩu" type="password" placeholder="••••••••" className="rounded-2xl" required />
      </div>

      {error && (
        <div className="p-3 bg-red-50 border border-red-100 text-red-600 text-xs rounded-xl font-bold">
          {error}
        </div>
      )}

      <Button type="submit" isLoading={isLoading} className="w-full py-4 rounded-2xl shadow-md">
        Đăng ký tài khoản
      </Button>
    </form>
  );
};
