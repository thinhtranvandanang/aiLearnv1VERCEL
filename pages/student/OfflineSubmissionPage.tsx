
import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { submitOffline } from '../../services/submission.service.ts';
import { Card, Button, LoadingOverlay } from '../../components/common/UI.tsx';
import { ROUTES } from '../../constants/routes.ts';

export const OfflineSubmissionPage: React.FC = () => {
  const { testId } = useParams<{ testId: string }>();
  const navigate = useNavigate();
  
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      const reader = new FileReader();
      reader.onloadend = () => setPreview(reader.result as string);
      reader.readAsDataURL(selectedFile);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file || !testId) return;

    setLoading(true);
    setError(null);

    try {
      const res = await submitOffline(parseInt(testId), file);
      if (res.status === 'success') {
        alert('Nộp bài thành công! AI đang tiến hành chấm điểm bài làm của bạn.');
        navigate(ROUTES.PROTECTED.DASHBOARD);
      } else {
        setError(res.message || 'Gửi ảnh bài làm thất bại.');
      }
    } catch (err: any) {
      setError(err.message || 'Đã xảy ra lỗi khi gửi dữ liệu.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto px-4 py-12">
      {loading && <LoadingOverlay />}
      
      <div className="mb-8 flex items-center gap-4">
        <button onClick={() => navigate(-1)} className="p-2 hover:bg-gray-100 rounded-full transition">
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
        </button>
        <h1 className="text-3xl font-black text-gray-900">Nộp bài qua ảnh chụp</h1>
      </div>

      <Card className="p-8">
        <form onSubmit={handleSubmit} className="space-y-6">
          <p className="text-gray-500 text-sm">
            Vui lòng chụp ảnh rõ nét toàn bộ trang bài làm của bạn. Đảm bảo ánh sáng tốt và không bị rung nhòe để AI chấm điểm chính xác nhất.
          </p>

          <div className="relative border-2 border-dashed border-gray-300 rounded-2xl p-4 min-h-[300px] flex flex-col items-center justify-center bg-gray-50 hover:bg-gray-100 transition group">
            {preview ? (
              <div className="w-full flex flex-col items-center">
                <img src={preview} alt="Preview" className="max-h-[400px] rounded-lg shadow-sm mb-4" />
                <button 
                  type="button" 
                  onClick={() => { setFile(null); setPreview(null); }}
                  className="text-red-600 font-bold text-sm hover:underline"
                >
                  Xóa và chọn ảnh khác
                </button>
              </div>
            ) : (
              <div className="text-center">
                <div className="w-16 h-16 bg-indigo-100 text-indigo-600 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition">
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                </div>
                <p className="font-bold text-gray-700">Tải ảnh bài làm</p>
                <p className="text-xs text-gray-400 mt-1">Hỗ trợ JPG, PNG, PDF (Max 10MB)</p>
              </div>
            )}
            <input 
              type="file" 
              accept="image/*,application/pdf" 
              onChange={handleFileChange} 
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            />
          </div>

          {error && <div className="p-4 bg-red-50 text-red-600 rounded-xl text-sm font-bold">{error}</div>}

          <div className="pt-4 flex gap-4">
            <Button type="button" variant="outline" className="flex-1" onClick={() => navigate(-1)}>Hủy bỏ</Button>
            <Button type="submit" className="flex-[2]" disabled={!file}>Gửi bài làm</Button>
          </div>
        </form>
      </Card>
    </div>
  );
};
