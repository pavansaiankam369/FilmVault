import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Login from './pages/Login';
import Register from './pages/Register';
import MovieList from './pages/MovieList';
import MovieDetail from './pages/MovieDetail';
import Watchlist from './pages/Watchlist';
import AdminDashboard from './pages/AdminDashboard';
import AdminCreateMovie from "./pages/AdminCreateMovie";



function App() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-50 font-sans selection:bg-indigo-500/30 selection:text-indigo-200">
      <Navbar />
      <main className="flex-1 w-full">
        <Routes>
           
           <Route path="/" element={<MovieList />} />
           <Route path="/login" element={<Login />} />
           <Route path="/register" element={<Register />} />
           <Route path="/movies/:id" element={<MovieDetail />} />
           <Route path="/watchlist" element={<Watchlist />} />
           <Route path="/admin" element={<AdminDashboard />} />
           <Route path="/admin/movies/create" element={<AdminCreateMovie />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
