import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axiosClient";
import { useAuth } from "../context/AuthContext";

const AdminCreateMovie = () => {
	const { user } = useAuth();
	const navigate = useNavigate();

	// Block non-admins from accessing page
	if (!user || user.role !== "admin") {
		return (
			<div className="text-center py-20 text-red-400 text-xl">
				Access Denied — Admins Only
			</div>
		);
	}

	const [form, setForm] = useState({
		title: "",
		description: "",
		genre: "",
		language: "",
		director: "",
		release_year: "",
		rating: "",
		poster_url: "",
		approved: true,   // admins create approved by default
	});

	const [loading, setLoading] = useState(false);

	const handleChange = (e) => {
		const { name, value } = e.target;
		setForm({ ...form, [name]: value });
	};

	const handleSubmit = async (e) => {
		e.preventDefault();
		setLoading(true);

		try {
			await api.post("/movies", {
				...form,
				release_year: Number(form.release_year),
				rating: Number(form.rating),
			});

			alert("Movie created successfully 🎬");
			navigate("/movies");
		} catch (err) {
			console.error(err);
			alert("Failed to create movie");
		} finally {
			setLoading(false);
		}
	};

	return (
		<div className="max-w-3xl mx-auto px-4 py-12">
			<h1 className="text-3xl font-bold text-white mb-8">
				Add New Movie
			</h1>

			<form
				onSubmit={handleSubmit}
				className="bg-slate-900 p-8 rounded-xl border border-slate-800 space-y-6"
			>
				<div>
					<label className="text-slate-300 text-sm">Title</label>
					<input
						name="title"
						value={form.title}
						onChange={handleChange}
						required
						className="w-full mt-1 p-2 rounded bg-slate-800 border border-slate-700 text-white"
					/>
				</div>

				<div>
					<label className="text-slate-300 text-sm">Description</label>
					<textarea
						name="description"
						value={form.description}
						onChange={handleChange}
						rows={4}
						className="w-full mt-1 p-2 rounded bg-slate-800 border border-slate-700 text-white"
					/>
				</div>

				<div className="grid grid-cols-2 gap-4">
					<div>
						<label className="text-slate-300 text-sm">Genre</label>
						<input
							name="genre"
							value={form.genre}
							onChange={handleChange}
							className="w-full mt-1 p-2 rounded bg-slate-800 border border-slate-700 text-white"
						/>
					</div>

					<div>
						<label className="text-slate-300 text-sm">Language</label>
						<input
							name="language"
							value={form.language}
							onChange={handleChange}
							className="w-full mt-1 p-2 rounded bg-slate-800 border border-slate-700 text-white"
						/>
					</div>
				</div>

				<div>
					<label className="text-slate-300 text-sm">Director</label>
					<input
						name="director"
						value={form.director}
						onChange={handleChange}
						className="w-full mt-1 p-2 rounded bg-slate-800 border border-slate-700 text-white"
					/>
				</div>

				<div className="grid grid-cols-2 gap-4">
					<div>
						<label className="text-slate-300 text-sm">Release Year</label>
						<input
							type="number"
							name="release_year"
							value={form.release_year}
							onChange={handleChange}
							className="w-full mt-1 p-2 rounded bg-slate-800 border border-slate-700 text-white"
						/>
					</div>

					<div>
						<label className="text-slate-300 text-sm">Rating</label>
						<input
							type="number"
							step="0.1"
							name="rating"
							value={form.rating}
							onChange={handleChange}
							className="w-full mt-1 p-2 rounded bg-slate-800 border border-slate-700 text-white"
						/>
					</div>
				</div>

				<div>
					<label className="text-slate-300 text-sm">Poster URL</label>
					<input
						name="poster_url"
						value={form.poster_url}
						onChange={handleChange}
						className="w-full mt-1 p-2 rounded bg-slate-800 border border-slate-700 text-white"
					/>
				</div>

				<button
					type="submit"
					disabled={loading}
					className="bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-3 rounded-lg font-semibold disabled:opacity-60"
				>
					{loading ? "Saving..." : "Create Movie"}
				</button>
			</form>
		</div>
	);
};

export default AdminCreateMovie;
