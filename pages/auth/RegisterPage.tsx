
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext.tsx';
import { Card, Button, Input, LoadingOverlay } from '../../components/common/UI.tsx';
import { ROUTES } from '../../constants/routes.ts';
import { GoogleLoginButton } from '../../components/auth/GoogleLoginButton.tsx';

export const RegisterPage: React.FC = () => {
  const { register, isLoading } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);

  const handleRegisterSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    const formData = new FormData(e.currentTarget);
    const password = formData.get('password') as string;
    const confirmPassword = formData.get('confirmPassword') as string;

    if (password !== confirmPassword) {
      setError('Mật khẩu xác nhận không trùng khớp.');
      return;
    }

    try {
      await register({
        full_name: formData.get('fullName') as string,
        email: formData.get('email') as string,
        username: formData.get('username') as string,
        password: password,
        role: 'student'
      });
      navigate(ROUTES.PROTECTED.DASHBOARD);
    } catch (err: any) {
      setError(err.message || 'Đăng ký thất bại. Vui lòng thử lại sau.');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
      {isLoading && <LoadingOverlay />}

      <div className="w-full max-w-[480px]">
        <div className="bg-white rounded-[2rem] shadow-xl p-8 md:p-10 border border-gray-200">
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-indigo-600 rounded-2xl mb-4 shadow-lg">
              <span className="text-3xl font-black text-white italic">E</span>
            </div>
            <h1 className="text-2xl font-black text-gray-900 tracking-tight">Tạo tài khoản mới</h1>
            <p className="text-gray-500 text-sm mt-1">Bắt đầu lộ trình học tập thông minh ngay hôm nay</p>
          </div>

          <div className="space-y-6">
            <GoogleLoginButton />

            <div className="flex items-center gap-4 py-2">
              <div className="flex-1 h-px bg-gray-200"></div>
              <span className="text-[10px] font-black text-gray-400 uppercase px-2">Hoặc đăng ký thủ công</span>
              <div className="flex-1 h-px bg-gray-200"></div>
            </div>

            <form onSubmit={handleRegisterSubmit} className="space-y-4">
              <Input name="fullName" label="Họ và tên" placeholder="Nguyễn Văn A" required className="rounded-xl" />
              <div className="grid grid-cols-2 gap-4">
                <Input name="username" label="Username" placeholder="user123" required className="rounded-xl" />
                <Input name="email" label="Email" type="email" placeholder="abc@gmail.com" required className="rounded-xl" />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <Input name="password" label="Mật khẩu" type="password" placeholder="••••••••" required className="rounded-xl" />
                <Input name="confirmPassword" label="Xác nhận" type="password" placeholder="••••••••" required className="rounded-xl" />
              </div>

              {error && (
                <div className="p-3 bg-red-50 text-red-600 text-xs font-bold rounded-xl border border-red-200">
                  {error}
                </div>
              )}

              <Button type="submit" isLoading={isLoading} className="w-full py-3.5 rounded-xl font-black shadow-lg shadow-indigo-100">
                Đăng ký tài khoản
              </Button>
            </form>
            
            <div className="text-center pt-2">
              <p className="text-sm text-gray-500 font-medium">
                Đã có tài khoản? <Link to={ROUTES.PUBLIC.LOGIN} className="font-bold text-indigo-600 hover:underline">Đăng nhập</Link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
