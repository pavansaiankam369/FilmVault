import { useEffect, useState } from 'react';
import api from '../api/axiosClient';
import { Link } from 'react-router-dom';
import { Star } from 'lucide-react';


const MovieList = () => {
    const [movies, setMovies] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchMovies = async () => {
            try {
                const res = await api.get('/movies/');
                setMovies(res.data);
            } catch (err) {
                console.error("Failed to fetch movies", err);
            } finally {
                setLoading(false);
            }
        };
        fetchMovies();
    }, []);

    if (loading) return <div className="text-center py-20 text-slate-400">Loading movies...</div>;

    return (
        <div className=" pb-20">
            {/* Hero Section */}
            <div className="relative h-[400px] w-full bg-gradient-to-br from-indigo-900 to-slate-900 overflow-hidden mb-12">
                <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1536440136628-849c177e76a1?q=80&w=2525&auto=format&fit=crop')] bg-cover bg-center opacity-20 mix-blend-overlay"></div>
                <div className="absolute inset-0 bg-gradient-to-t from-slate-950 to-transparent"></div>
                <div className="absolute bottom-0 left-0 w-full p-8 md:p-12">
                    <div className="max-w-7xl mx-auto">
                        <h1 className="text-5xl md:text-6xl font-extrabold text-white mb-4 tracking-tight drop-shadow-xl">
                            Discover <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">Cinematic</span> Gems
                        </h1>
                        <p className="text-xl text-slate-300 max-w-2xl drop-shadow-md">
                            Explore the latest top-rated movies, read reviews, and build your own personal watchlist.
                        </p>
                    </div>
                </div>
            </div>

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between mb-8">
                    <h2 className="text-2xl font-bold text-white flex items-center gap-2">
                        <span className="w-1 h-8 bg-indigo-500 rounded-full"></span>
                        Featured Movies
                    </h2>
                    {/* Add filters or sorting here if needed in future */}
                </div>

                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
                    {movies.map((movie) => (
                        <Link key={movie.id} to={`/movies/${movie.id}`} className="block group">
                            <div className="bg-slate-900 rounded-xl overflow-hidden shadow-lg border border-slate-800 transition-all duration-300 group-hover:-translate-y-2 group-hover:shadow-indigo-500/20 group-hover:border-indigo-500/30">
                                <div className="aspect-[2/3] relative overflow-hidden">
                                    <img
                                        src={movie.poster_url || "https://via.placeholder.com/300x450?text=No+Poster"}
                                        alt={movie.title}
                                        className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                                    />
                                    <div className="absolute inset-0 bg-gradient-to-t from-slate-900 via-transparent to-transparent opacity-60"></div>
                                    <div className="absolute top-2 right-2 bg-slate-950/80 backdrop-blur-md border border-slate-700 px-2 py-1 rounded-md flex items-center gap-1 text-yellow-400 text-xs font-bold shadow-sm">
                                        <Star className="w-3 h-3 fill-yellow-400" />
                                        {movie.rating}
                                    </div>
                                </div>
                                <div className="p-4">
                                    <h3 className="text-white font-bold truncate mb-1 group-hover:text-indigo-400 transition-colors">{movie.title}</h3>
                                    <div className="flex justify-between items-center text-xs text-slate-400">
                                        <span>{movie.release_year}</span>
                                        <span className="border border-slate-700 px-1.5 py-0.5 rounded bg-slate-800">{movie.genre}</span>
                                    </div>
                                </div>
                            </div>
                        </Link>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default MovieList;
