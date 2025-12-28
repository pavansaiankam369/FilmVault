import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate, Link } from 'react-router-dom';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        try {
            await login(email, password);
            navigate('/');
        } catch (err) {
            setError('Invalid credentials. Please try again.');
        }
    };

    return (
        <div className="min-h-screen pt-16 flex items-center justify-center relative overflow-hidden">
            {/* Background Decorations */}
            <div className="absolute top-0 left-1/4 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl -z-10 mix-blend-screen"></div>
            <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl -z-10 mix-blend-screen"></div>

            <div className="bg-slate-900/50 backdrop-blur-xl p-8 md:p-10 rounded-2xl shadow-2xl w-full max-w-md border border-slate-800 relative z-10">
                <div className="mb-8 text-center">
                    <h2 className="text-3xl font-bold text-white mb-2">Welcome Back</h2>
                    <p className="text-slate-400">Sign in to continue to MovieDB</p>
                </div>
                
                {error && (
                    <div className="bg-red-500/10 border border-red-500/20 text-red-500 p-4 rounded-lg mb-6 text-sm text-center flex items-center justify-center gap-2">
                        <span className="font-bold">Error:</span> {error}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-5">
                    <div>
                        <label className="block text-slate-300 text-sm font-medium mb-2">Email Address</label>
                        <input
                            type="email"
                            required
                            className="w-full bg-slate-950/50 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all"
                            placeholder="you@example.com"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                    </div>
                    <div>
                        <div className="flex justify-between items-center mb-2">
                            <label className="block text-slate-300 text-sm font-medium">Password</label>
                            <Link to="#" className="text-xs text-indigo-400 hover:text-indigo-300 transition-colors">Forgot password?</Link>
                        </div>
                        <input
                            type="password"
                            required
                            className="w-full bg-slate-950/50 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all"
                            placeholder="••••••••"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </div>
                    <button
                        type="submit"
                        className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-bold py-3 rounded-lg transition-all shadow-lg shadow-indigo-600/20 hover:shadow-indigo-600/30 hover:scale-[1.02] active:scale-[0.98]"
                    >
                        Sign In
                    </button>
                </form>
                
                <div className="mt-8 text-center border-t border-slate-800 pt-6">
                    <p className="text-slate-400 text-sm">
                        Don't have an account? <Link to="/register" className="text-indigo-400 hover:text-indigo-300 font-medium hover:underline">Sign up</Link>
                    </p>
                </div>
            </div>
        </div>
    );
};

export default Login;
