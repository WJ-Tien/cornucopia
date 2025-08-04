import React, { useState } from 'react';

// --- TS 型別定義 ---
interface LoginFormProps {
  onLogin: (username: string, password: string) => void;
  loading: boolean;
  error: string | null;
}

// --- SVG 圖示元件 ---
const CornucopiaIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-white">
        <path d="M18.33 6.34C17.36 5.37 16.2 4.73 14.94 4.34C12.42 3.56 9.73 4.22 7.77 6.18C5.81 8.14 5.15 10.83 5.93 13.35C6.32 14.61 6.96 15.77 7.93 16.74C9.22 18.03 10.88 19 12.67 19H15C15.53 19 16.04 18.89 16.5 18.72"/>
        <path d="M9.5 12A2.5 2.5 0 0 1 12 9.5A2.5 2.5 0 0 1 14.5 12V19"/>
        <path d="M8 22a2 2 0 0 0 2-2V13"/>
        <path d="M12 22a2 2 0 0 0 2-2v-3"/>
        <path d="M16 22a2 2 0 0 0 2-2v-5"/>
    </svg>
);

const UserIcon: React.FC<{ className: string }> = ({ className }) => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
        <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" />
        <circle cx="12" cy="7" r="4" />
    </svg>
);

const LockIcon: React.FC<{ className: string }> = ({ className }) => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
        <rect width="18" height="11" x="3" y="11" rx="2" ry="2" />
        <path d="M7 11V7a5 5 0 0 1 10 0v4" />
    </svg>
);

// --- 登入表單元件 ---
const LoginForm: React.FC<LoginFormProps> = ({ onLogin, loading, error }) => {
    const [username, setUsername] = useState<string>('');
    const [password, setPassword] = useState<string>('');

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (!username || !password) return;
        onLogin(username, password);
    };

    return (
        <div className="w-full max-w-md bg-white/10 backdrop-blur-md rounded-2xl shadow-2xl p-8 space-y-6">
            <div className="flex flex-col items-center space-y-2">
                <CornucopiaIcon />
                <h1 className="text-3xl font-bold text-white tracking-wider">Cornucopia</h1>
                <p className="text-gray-300">歡迎回來，請登入您的帳戶</p>
            </div>
            
            {error && (
                <div className="bg-red-500/50 text-white p-3 rounded-lg text-center animate-pulse">
                    {error}
                </div>
            )}
            
            <form onSubmit={handleSubmit} className="space-y-6">
                <div className="relative">
                    <UserIcon className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
                    <input
                        type="text"
                        placeholder="使用者名稱"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                        className="w-full bg-gray-900/50 text-white border border-gray-600 rounded-lg pl-12 pr-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all duration-300"
                    />
                </div>
                <div className="relative">
                    <LockIcon className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
                    <input
                        type="password"
                        placeholder="密碼"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        className="w-full bg-gray-900/50 text-white border border-gray-600 rounded-lg pl-12 pr-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all duration-300"
                    />
                </div>
                <button
                    type="submit"
                    disabled={loading}
                    className="w-full bg-purple-600 text-white font-bold py-3 rounded-lg hover:bg-purple-700 disabled:bg-purple-800 disabled:cursor-not-allowed transition-all duration-300 transform hover:scale-105 flex items-center justify-center"
                >
                    {loading ? (
                        <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                    ) : (
                        '登入'
                    )}
                </button>
            </form>
        </div>
    );
};

export default LoginForm;