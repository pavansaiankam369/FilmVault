import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LogOut, Film } from 'lucide-react';

const Navbar = () => {
	const { user, logout } = useAuth();
	const navigate = useNavigate();

	const handleLogout = () => {
		logout();
		navigate('/login');
	};

	return (
		<nav className="fixed w-full top-0 z-50 bg-slate-950/80 backdrop-blur-md border-b border-slate-800/50 supports-[backdrop-filter]:bg-slate-950/60">
			<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
				<div className="flex items-center justify-between h-16">
					<Link to="/" className="flex items-center gap-2 group">
						<div className="bg-indigo-600 p-1.5 rounded-lg group-hover:scale-110 transition-transform duration-300">
							<Film className="w-5 h-5 text-white" />
						</div>
						<span className="font-bold text-xl bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400 group-hover:to-white transition-all">MovieDB</span>
					</Link>

					<div className="flex items-center gap-6">
						{user ? (
							<>
								<div className="flex items-center gap-2 px-3 py-1.5 bg-slate-900/50 rounded-full border border-slate-800">
									<div className="w-6 h-6 rounded-full bg-indigo-500/20 flex items-center justify-center text-xs font-bold text-indigo-400">
										{user.username.charAt(0).toUpperCase()}
									</div>
									<span className="text-slate-300 text-sm hidden sm:block font-medium">{user.username}</span>
								</div>

								{user.role === 'admin' && (
									<Link to="/admin" className="text-slate-400 hover:text-indigo-400 text-sm font-medium transition-colors">Admin</Link>
								)}
								<Link to="/watchlist" className="text-slate-400 hover:text-indigo-400 text-sm font-medium transition-colors">Watchlist</Link>
								<button
									onClick={handleLogout}
									className="flex items-center gap-2 text-slate-400 hover:text-red-400 transition-colors group"
								>
									<LogOut className="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
								</button>
							</>
						) : (
							<div className="flex items-center gap-4">
								<Link to="/login" className="text-slate-300 hover:text-white font-medium text-sm transition-colors">Login</Link>
								<Link to="/register" className="bg-indigo-600 hover:bg-indigo-500 text-white px-5 py-2 rounded-full text-sm font-medium transition-all shadow-lg shadow-indigo-500/20 hover:shadow-indigo-500/30">
									Sign Up
								</Link>
							</div>
						)}
					</div>
				</div>
			</div>
		</nav>
	);
};

export default Navbar;
