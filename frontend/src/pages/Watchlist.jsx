import { useEffect, useState } from 'react';
import api from '../api/axiosClient';
import { Link } from 'react-router-dom';
import { Trash2 } from 'lucide-react';

const Watchlist = () => {
	const [watchlist, setWatchlist] = useState([]);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		const fetchWatchlist = async () => {
			try {
				const res = await api.get('/watchlist/');
				setWatchlist(res.data);
			} catch (err) {
				console.error(err);
			} finally {
				setLoading(false);
			}
		};
		fetchWatchlist();
	}, []);

	const removeFromWatchlist = async (movieId) => {
		try {
			await api.delete(`/watchlist/${movieId}`);
			setWatchlist(watchlist.filter(item => item.movie.id !== movieId));
		} catch (err) {
			console.error(err);
		}
	};

	if (loading) return <div className="text-center py-20 text-slate-400">Loading watchlist...</div>;

	return (
		<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
			<h1 className="text-3xl font-bold text-white mb-8">My Watchlist</h1>

			{watchlist.length > 0 ? (
				<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
					{watchlist.map((item) => (
						<div key={item.id} className="bg-slate-900 rounded-xl overflow-hidden shadow-lg border border-slate-800 flex transition-all hover:bg-slate-800 hover:border-indigo-500/30 group">
							<div className="w-24 md:w-32 relative flex-shrink-0">
                                <img
                                    src={item.movie.poster_url || "https://via.placeholder.com/100x150"}
                                    alt={item.movie.title}
                                    className="w-full h-full object-cover"
                                />
                            </div>
							<div className="p-4 flex-1 flex flex-col justify-between">
								<div>
									<Link to={`/movies/${item.movie.id}`} className="font-bold text-lg text-white hover:text-indigo-400 transition-colors line-clamp-1 mb-1">{item.movie.title}</Link>
									<p className="text-slate-400 text-sm">{item.movie.release_year}</p>
								</div>
								<button
									onClick={() => removeFromWatchlist(item.movie.id)}
									className="self-start text-red-500 hover:text-red-400 text-sm flex items-center gap-1.5 mt-3 py-1 px-2 rounded hover:bg-red-500/10 transition-colors"
								>
									<Trash2 className="w-4 h-4" /> Remove
								</button>
							</div>
						</div>
					))}
				</div>
			) : (
				<p className="text-center text-slate-500 py-10">Your watchlist is empty.</p>
			)}
		</div>
	);
};

export default Watchlist;
