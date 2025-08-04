import { useAuth } from '../features/auth/useAuth';
import LoginForm from '../features/auth/components/LoginForm';
import Dashboard from '../features/auth/components/Dashboard';
// ... import icons ...

export default function LoginPage() {
  const { isLoggedIn, loading, error, username, handleLogin, handleLogout } = useAuth();
  
  // 這裡可以加入背景等頁面級別的樣式
  return (
    <div className="min-h-screen w-full bg-gray-900 text-white flex items-center justify-center p-4 bg-gradient-to-br from-gray-900 via-purple-900/50 to-gray-900">
      <div className="absolute top-0 left-0 w-full h-full bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-5"></div>
      {isLoggedIn ? (
        <Dashboard username={username} onLogout={handleLogout} />
      ) : (
        <LoginForm onLogin={handleLogin} loading={loading} error={error} />
      )}
    </div>
  );
}
