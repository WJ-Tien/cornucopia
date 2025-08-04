import React from 'react';

// --- TS 型別定義 ---
interface DashboardProps {
  username: string | null;
  onLogout: () => void;
}

// --- SVG 圖示元件 ---
// 為了讓元件自給自足，我們再次加入圖示
const CornucopiaIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-white">
        <path d="M18.33 6.34C17.36 5.37 16.2 4.73 14.94 4.34C12.42 3.56 9.73 4.22 7.77 6.18C5.81 8.14 5.15 10.83 5.93 13.35C6.32 14.61 6.96 15.77 7.93 16.74C9.22 18.03 10.88 19 12.67 19H15C15.53 19 16.04 18.89 16.5 18.72"/>
        <path d="M9.5 12A2.5 2.5 0 0 1 12 9.5A2.5 2.5 0 0 1 14.5 12V19"/>
        <path d="M8 22a2 2 0 0 0 2-2V13"/>
        <path d="M12 22a2 2 0 0 0 2-2v-3"/>
        <path d="M16 22a2 2 0 0 0 2-2v-5"/>
    </svg>
);

// --- 儀表板元件 ---
const Dashboard: React.FC<DashboardProps> = ({ username, onLogout }) => {
    return (
        <div className="w-full max-w-md bg-white/10 backdrop-blur-md rounded-2xl shadow-2xl p-8 text-center space-y-6 animate-fade-in">
            <div className="flex flex-col items-center space-y-4">
                <CornucopiaIcon />
                <h1 className="text-3xl font-bold text-white">登入成功！</h1>
                <p className="text-gray-200 text-lg">
                    歡迎回來，
                    <span className="font-bold text-purple-400 mx-2">
                        {username || '使用者'}
                    </span>
                    ！
                </p>
            </div>
            <div className="text-left text-gray-300 bg-gray-900/50 p-4 rounded-lg">
                <h2 className="text-lg font-semibold text-white mb-2">下一步</h2>
                <ul className="list-disc list-inside space-y-1">
                    <li>您可以開始瀏覽受保護的頁面。</li>
                    <li>這裡是您個人化的儀表板。</li>
                    <li>盡情探索 Cornucopia 的功能吧！</li>
                </ul>
            </div>
            <button
                onClick={onLogout}
                className="w-full bg-red-600 text-white font-bold py-3 rounded-lg hover:bg-red-700 transition-all duration-300 transform hover:scale-105"
            >
                登出
            </button>
        </div>
    );
};

export default Dashboard;