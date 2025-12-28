import { createContext, useState, useEffect, useContext } from 'react';
import api from '../api/axiosClient';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
	const [user, setUser] = useState(null);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		const checkUser = async () => {
			const token = localStorage.getItem('token');
			if (token) {
				try {
					// Decoded from token or fetched from /me endpoint if available
					// For now, let's just assume valid if token exists, or decode strictly
					// Better: fetch user profile
					// const res = await api.get('/auth/me'); 
					// setUser(res.data);

					// Temporary: decode logic or persistence if we saved user in localStorage
					const storedUser = localStorage.getItem('user');
					if (storedUser) setUser(JSON.parse(storedUser));
				} catch (error) {
					console.error("Auth check failed", error);
					localStorage.removeItem('token');
				}
			}
			setLoading(false);
		};
		checkUser();
	}, []);

	const login = async (email, password) => {
		const res = await api.post('/auth/authenticate', { email, password });
		localStorage.setItem('token', res.data.access_token);
		if (res.data.user) {
			localStorage.setItem('user', JSON.stringify(res.data.user));
			setUser(res.data.user);
		}
		return res.data;
	};

	const logout = () => {
		localStorage.removeItem('token');
		localStorage.removeItem('user');
		setUser(null);
	};

	return (
		<AuthContext.Provider value={{ user, login, logout, loading }}>
			{!loading && children}
		</AuthContext.Provider>
	);
};

export const useAuth = () => useContext(AuthContext);
