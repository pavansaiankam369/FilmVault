import { useEffect, useState } from 'react';
import api from '../api/axiosClient';
import { Trash2, CheckCircle, XCircle } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const AdminDashboard = () => {
	const { user } = useAuth();
	const navigate = useNavigate();
	const [users, setUsers] = useState([]);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		if (!user || user.role !== 'admin') {
			navigate('/');
			return;
		}

		const fetchData = async () => {
			try {
				const usersRes = await api.get('/users/all');
				setUsers(usersRes.data);
			} catch (err) {
				console.error(err);
			} finally {
				setLoading(false);
			}
		};
		fetchData();
	}, [user, navigate]);

	const deleteUser = async (id) => {
		if (!window.confirm("Are you sure you want to suspend this user?")) return;
		try {
			await api.delete(`/users/${id}`);
			setUsers(users.map(u => u.id === id ? { ...u, status: 'suspended' } : u));
		} catch (err) {
			console.error(err);
		}
	};

	if (loading) return <div className="text-center py-20 text-slate-400">Loading admin panel...</div>;

	return (
		<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
			<h1 className="text-3xl font-bold text-white mb-8 border-b border-slate-700 pb-4">Admin Dashboard</h1>

			<div className="bg-slate-900 rounded-xl shadow-2xl border border-slate-800 overflow-hidden">
				<div className="p-6 border-b border-slate-800 bg-slate-900/50 backdrop-blur flex justify-between items-center">
					<h2 className="text-xl font-bold text-white">User Management</h2>
                    <span className="text-xs text-slate-500 font-mono">Total Users: {users.length}</span>
				</div>
				<div className="overflow-x-auto">
					<table className="w-full text-left border-collapse">
						<thead className="bg-slate-950 text-slate-400 text-xs uppercase tracking-wider font-semibold">
							<tr>
								<th className="px-6 py-4">ID</th>
								<th className="px-6 py-4">Username</th>
								<th className="px-6 py-4">Email</th>
								<th className="px-6 py-4">Role</th>
								<th className="px-6 py-4">Status</th>
								<th className="px-6 py-4 text-right">Actions</th>
							</tr>
						</thead>
						<tbody className="divide-y divide-slate-800 text-slate-300 text-sm">
							{users.map((u) => (
								<tr key={u.id} className="hover:bg-slate-800/40 transition-colors group">
									<td className="px-6 py-4 font-mono text-slate-500">#{u.id}</td>
									<td className="px-6 py-4 font-medium text-white group-hover:text-indigo-400 transition-colors">{u.username}</td>
									<td className="px-6 py-4">{u.email}</td>
									<td className="px-6 py-4">
										<span className={`px-2.5 py-1 rounded-full text-xs font-bold ${u.role === 'admin' ? 'bg-indigo-500/20 text-indigo-400 border border-indigo-500/30' : 'bg-slate-700/30 text-slate-400 border border-slate-700'}`}>
											{u.role}
										</span>
									</td>
									<td className="px-6 py-4">
										<span className={`flex items-center gap-1.5 font-medium ${u.status === 'active' ? 'text-green-400' : 'text-red-400'}`}>
											{u.status === 'active' ? <CheckCircle className="w-3.5 h-3.5" /> : <XCircle className="w-3.5 h-3.5" />}
											<span className="capitalize">{u.status}</span>
										</span>
									</td>
									<td className="px-6 py-4 text-right">
										{u.status === 'active' && u.role !== 'admin' && (
											<button 
                                                onClick={() => deleteUser(u.id)} 
                                                className="text-slate-500 hover:text-red-500 transition-colors p-2 hover:bg-red-500/10 rounded-full" 
                                                title="Suspend User"
                                            >
												<Trash2 className="w-4 h-4" />
											</button>
										)}
									</td>
								</tr>
							))}
						</tbody>
					</table>
				</div>
			</div>
		</div>
	);
};

export default AdminDashboard;
