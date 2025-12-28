import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api/axiosClient';
import { Star, Calendar, Plus, Check } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const MovieDetail = () => {
    const { id } = useParams();
    const { user } = useAuth();
    const [movie, setMovie] = useState(null);
    const [reviews, setReviews] = useState([]);
    const [inWatchlist, setInWatchlist] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchDetails = async () => {
            try {
                const [movieRes, reviewsRes] = await Promise.all([
                    api.get(`/movies/${id}`),
                    api.get(`/reviews/by-movie/${id}`)
                ]);
                setMovie(movieRes.data);
                setReviews(reviewsRes.data);
                
                if (user) {
                     const watchlistRes = await api.get(`/watchlist/${id}/status`);
                     setInWatchlist(watchlistRes.data.in_watchlist);
                }
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        fetchDetails();
    }, [id, user]);

    const addToWatchlist = async () => {
        try {
            await api.post(`/watchlist/${id}`);
            setInWatchlist(true);
        } catch (err) {
            console.error(err);
        }
    };
    
    const removeFromWatchlist = async () => {
        try {
            await api.delete(`/watchlist/${id}`);
            setInWatchlist(false);
        } catch (err) {
            console.error(err);
        }
    };

    if (loading || !movie) return <div className="text-center py-20 text-slate-400">Loading details...</div>;

    return (
        <div className="relative min-h-screen">
            {/* Backdrop Hero */}
            <div className="relative h-[50vh] w-full overflow-hidden">
                <div className="absolute inset-0 bg-slate-900">
                    <img 
                        src={movie.poster_url || "https://via.placeholder.com/300x450?text=No+Poster"} 
                        alt="Backdrop" 
                        className="w-full h-full object-cover opacity-30 blur-sm"
                    />
                </div>
                <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/60 to-transparent"></div>
            </div>

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative -mt-64 z-10 pb-20">
                <div className="flex flex-col md:flex-row gap-8 items-start">
                    {/* Poster */}
                    <div className="w-full md:w-[300px] flex-shrink-0">
                        <img 
                            src={movie.poster_url || "https://via.placeholder.com/300x450?text=No+Poster"} 
                            alt={movie.title}
                            className="w-full rounded-xl shadow-2xl border-4 border-slate-800"
                        />
                    </div>
                    
                    {/* Details */}
                    <div className="flex-1 pt-4 md:pt-12">
                         <h1 className="text-4xl md:text-5xl font-extrabold text-white mb-4 drop-shadow-md leading-tight">{movie.title}</h1>
                         
                         <div className="flex flex-wrap items-center gap-4 text-slate-300 mb-8">
                            <span className="flex items-center gap-1.5 bg-yellow-500/20 text-yellow-500 px-3 py-1 rounded-full text-sm font-bold border border-yellow-500/30">
                                <Star className="w-4 h-4 fill-yellow-500" /> {movie.rating}
                            </span>
                             <span className="flex items-center gap-1.5"><Calendar className="w-4 h-4 text-slate-400"/> {movie.release_year}</span>
                             <span className="bg-slate-800/80 backdrop-blur px-3 py-1 rounded-full text-sm border border-slate-700">{movie.genre}</span>
                         </div>
                         
                         <div className="prose prose-invert max-w-none mb-8">
                            <p className="text-lg text-slate-300 leading-relaxed font-light">{movie.description}</p>
                         </div>
                         
                         <div className="flex flex-wrap gap-8 mb-8 p-6 bg-slate-900/50 rounded-xl border border-slate-800 backdrop-blur-sm">
                            <div>
                                <h4 className="text-slate-500 text-xs font-bold uppercase tracking-wider mb-1">Director</h4>
                                <span className="text-white font-medium">{movie.director}</span>
                            </div>
                            <div>
                                <h4 className="text-slate-500 text-xs font-bold uppercase tracking-wider mb-1">Language</h4>
                                <span className="text-white font-medium">{movie.language}</span>
                            </div>
                         </div>

                         <div className="flex gap-4">
                             {user && (
                                 inWatchlist ? (
                                     <button onClick={removeFromWatchlist} className="flex items-center gap-2 bg-green-600 hover:bg-green-500 text-white px-8 py-3 rounded-full font-bold transition-all shadow-lg shadow-green-900/40 hover:scale-105 active:scale-95">
                                         <Check className="w-5 h-5" /> Added to Watchlist
                                     </button>
                                 ) : (
                                     <button onClick={addToWatchlist} className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white px-8 py-3 rounded-full font-bold transition-all shadow-lg shadow-indigo-900/40 hover:scale-105 active:scale-95">
                                         <Plus className="w-5 h-5" /> Add to Watchlist
                                     </button>
                                 )
                             )}
                         </div>
                    </div>
                </div>

                {/* Reviews Section */}
                <div className="mt-20">
                    <div className="flex items-center justify-between mb-8">
                        <h2 className="text-2xl font-bold text-white relative pl-4 border-l-4 border-indigo-500">Reviews & Ratings</h2>
                        {/* Potential 'Add Review' button could go here */}
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {reviews.length > 0 ? reviews.map(review => (
                            <div key={review.id} className="bg-slate-900 p-6 rounded-xl border border-slate-800 hover:border-slate-700 transition-colors">
                                <div className="flex items-center justify-between mb-4">
                                    <div className="flex items-center gap-3">
                                        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center font-bold text-white shadow-lg">
                                            {review.user_id ? "U" : "?"}
                                        </div>
                                        <div>
                                            <span className="block font-medium text-white text-sm">User {review.user_id}</span>
                                            <span className="block text-xs text-slate-500">Verified Viewer</span>
                                        </div>
                                    </div>
                                    <span className="flex items-center gap-1 bg-slate-800 px-2 py-1 rounded text-yellow-400 font-bold text-sm">
                                        <Star className="w-3 h-3 fill-yellow-400" /> {review.rating}
                                    </span>
                                </div>
                                <p className="text-slate-300 text-sm leading-relaxed">{review.comment}</p>
                            </div>
                        )) : (
                            <div className="col-span-full text-center py-12 bg-slate-900/50 rounded-xl border border-slate-800 border-dashed">
                                <p className="text-slate-500">No reviews yet. Be the first to share your thoughts!</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default MovieDetail;
