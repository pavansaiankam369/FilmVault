import { useState } from 'react';
import api from '../api/axiosClient';
import { useNavigate, Link } from 'react-router-dom';

const Register = () => {
	const [formData, setFormData] = useState({
		username: '',
		email: '',
		password: '',
		confirmPassword: ''
	});
	const [error, setError] = useState('');
	const navigate = useNavigate();

	const handleChange = (e) => {
		setFormData({ ...formData, [e.target.name]: e.target.value });
	};

	const handleSubmit = async (e) => {
		e.preventDefault();
		setError('');

		if (formData.password !== formData.confirmPassword) {
			return setError("Passwords do not match");
		}

		try {
			await api.post('/auth/register', {
				username: formData.username,
				email: formData.email,
				password: formData.password
			});
			// Auto login or redirect to login
			navigate('/login');
		} catch (err) {
			setError(err.response?.data?.detail || 'Registration failed. Please try again.');
		}
	};

	return (
		<div className="min-h-screen pt-16 flex items-center justify-center relative overflow-hidden my-8">
			{/* Background Decorations */}
			<div className="absolute top-0 right-1/4 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl -z-10 mix-blend-screen"></div>
			<div className="absolute bottom-0 left-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl -z-10 mix-blend-screen"></div>

			<div className="bg-slate-900/50 backdrop-blur-xl p-8 md:p-10 rounded-2xl shadow-2xl w-full max-w-md border border-slate-800 relative z-10">
				<div className="mb-8 text-center">
					<h2 className="text-3xl font-bold text-white mb-2">Create Account</h2>
					<p className="text-slate-400">Join MovieDB to track your favorite films</p>
				</div>

				{error && (
					<div className="bg-red-500/10 border border-red-500/20 text-red-500 p-4 rounded-lg mb-6 text-sm text-center flex items-center justify-center gap-2">
						<span className="font-bold">Error:</span> {error}
					</div>
				)}

				<form onSubmit={handleSubmit} className="space-y-4">
					<div>
						<label className="block text-slate-300 text-sm font-medium mb-1">Username</label>
						<input
							type="text"
							name="username"
							required
							className="w-full bg-slate-950/50 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all"
							placeholder="johndoe"
							value={formData.username}
							onChange={handleChange}
						/>
					</div>
					<div>
						<label className="block text-slate-300 text-sm font-medium mb-1">Email Address</label>
						<input
							type="email"
							name="email"
							required
							className="w-full bg-slate-950/50 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all"
							placeholder="you@example.com"
							value={formData.email}
							onChange={handleChange}
						/>
					</div>
					<div>
						<label className="block text-slate-300 text-sm font-medium mb-1">Password</label>
						<input
							type="password"
							name="password"
							required
							className="w-full bg-slate-950/50 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all"
							placeholder="••••••••"
							value={formData.password}
							onChange={handleChange}
						/>
					</div>
					<div>
						<label className="block text-slate-300 text-sm font-medium mb-1">Confirm Password</label>
						<input
							type="password"
							name="confirmPassword"
							required
							className="w-full bg-slate-950/50 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all"
							placeholder="••••••••"
							value={formData.confirmPassword}
							onChange={handleChange}
						/>
					</div>
					<button
						type="submit"
						className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-bold py-3 rounded-lg transition-all shadow-lg shadow-indigo-600/20 hover:shadow-indigo-600/30 hover:scale-[1.02] active:scale-[0.98] mt-2"
					>
						Sign Up
					</button>
				</form>

				<div className="mt-8 text-center border-t border-slate-800 pt-6">
					<p className="text-slate-400 text-sm">
						Already have an account? <Link to="/login" className="text-indigo-400 hover:text-indigo-300 font-medium hover:underline">Log in</Link>
					</p>
				</div>
			</div>
		</div>
	);
};

export default Register;
