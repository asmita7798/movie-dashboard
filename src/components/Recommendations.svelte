<script>
  export let imdbCSV = [];
  export let currentView;

  import { onMount } from 'svelte';

  let similarityData = {};
  let selectedMovie = '';
  let recommendedMovies = [];

  let popularPicks = [];
  let topIMDBMovies = [];
  let criticsPicks = [];
  let genres = [];
  let selectedGenre = '';
  let genreMovies = [];

  // Use BASE_URL for GitHub Pages
  const BASE_URL = import.meta.env.BASE_URL;

  function getPosterPath(title) {
    const fileName = title.replace(/[^a-zA-Z0-9]/g, '_').toLowerCase() + '.jpg';
    return `${BASE_URL}posters/${fileName}`;
  }

  function filterMoviesWithPoster(movies) {
    return movies.map(m => ({ ...m, Poster_Path: getPosterPath(m.Series_Title) }));
  }

  onMount(async () => {
    const res = await fetch(`${BASE_URL}similarity.json`);
    similarityData = await res.json();

    // Popular picks
    popularPicks = filterMoviesWithPoster(
      [...imdbCSV].sort((a, b) => parseInt(b.No_of_votes) - parseInt(a.No_of_votes)).slice(0, 50)
    );

    // Top IMDB
    topIMDBMovies = filterMoviesWithPoster(
      [...imdbCSV].sort((a, b) => parseFloat(b.IMDB_Rating) - parseFloat(a.IMDB_Rating)).slice(0, 50)
    );

    // Critics picks
    criticsPicks = filterMoviesWithPoster(
      [...imdbCSV]
        .filter(m => m.Meta_score && !isNaN(m.Meta_score))
        .sort((a, b) => parseFloat(b.Meta_score) - parseFloat(a.Meta_score))
        .slice(0, 50)
    );

    // Genres
    genres = [...new Set(
      imdbCSV
        .map(m => m.Genre)
        .filter(Boolean)
        .flatMap(g => g.split(',').map(x => x.trim()))
        .filter(x => x.length > 0)
    )].sort();
  });

  function updateRecommendations() {
    if (!selectedMovie || !similarityData[selectedMovie]) {
      recommendedMovies = [];
      return;
    }
    const recommendedTitles = similarityData[selectedMovie].map(r => r.title);
    const movies = imdbCSV.filter(m => recommendedTitles.includes(m.Series_Title)).slice(0, 50);
    recommendedMovies = filterMoviesWithPoster(movies);
  }

  function updateGenreMovies() {
    if (!selectedGenre) {
      genreMovies = [];
      return;
    }
    const movies = imdbCSV
      .filter(m => m.Genre && m.Genre.includes(selectedGenre))
      .sort((a, b) => parseFloat(b.IMDB_Rating) - parseFloat(a.IMDB_Rating))
      .slice(0, 50);
    genreMovies = filterMoviesWithPoster(movies);
  }
</script>

<div class="container">
  <div class="hero-header">
    <div class="hero-title">Discover Your Next Favorite Movie</div>
    <div class="movie-select">
      <label for="movieSelect">Select a movie:</label>
      <select id="movieSelect" bind:value={selectedMovie} on:change={updateRecommendations}>
        <option value="">-- Choose a movie --</option>
        {#each imdbCSV as movie}
          <option value={movie.Series_Title}>{movie.Series_Title}</option>
        {/each}
      </select>
    </div>
    <button class="home-btn" aria-label="Go Home" on:click={() => currentView = 'dashboard'}>
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
        stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M3 9L12 2L21 9V20a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V9z"></path>
        <polyline points="9 22 9 12 15 12 15 22"></polyline>
      </svg>
    </button>
  </div>

  {#if recommendedMovies.length}
    <h2>Because you watched <span class="highlight">{selectedMovie}</span></h2>
    <div class="scroll-row">
      {#each recommendedMovies as movie}
        <div class="card fade-in">
          <img src={movie.Poster_Path} loading="lazy" alt={movie.Series_Title}
               on:error={(e) => e.target.style.display='none'} />
          <div class="title">{movie.Series_Title}</div>
        </div>
      {/each}
    </div>
  {/if}

  <h2>Popular Picks</h2>
  <div class="scroll-row">
    {#each popularPicks as movie}
      <div class="card fade-in">
        <img src={movie.Poster_Path} alt={movie.Series_Title} loading="lazy"
             on:error={(e) => e.target.style.display='none'} />
        <div class="title">{movie.Series_Title}</div>
      </div>
    {/each}
  </div>

  <h2>Pick by Genre</h2>
  <div class="genre-select">
    <label for="genreSelect">Select Genre:</label>
    <select id="genreSelect" bind:value={selectedGenre} on:change={updateGenreMovies}>
      <option value="">-- Choose a genre --</option>
      {#each genres as g}
        <option value={g}>{g}</option>
      {/each}
    </select>
  </div>

  {#if genreMovies.length}
    <div class="scroll-row">
      {#each genreMovies as movie}
        <div class="card fade-in">
          <img src={movie.Poster_Path} alt={movie.Series_Title}
               on:error={(e) => e.target.style.display='none'} />
          <div class="title">{movie.Series_Title}</div>
        </div>
      {/each}
    </div>
  {/if}

  <h2>Top IMDb Movies</h2>
  <div class="scroll-row">
    {#each topIMDBMovies as movie}
      <div class="card fade-in">
        <img src={movie.Poster_Path} alt={movie.Series_Title}
             on:error={(e) => e.target.style.display='none'} />
        <div class="title">{movie.Series_Title}</div>
      </div>
    {/each}
  </div>

  <h2>Picks by Critics</h2>
  <div class="scroll-row">
    {#each criticsPicks as movie}
      <div class="card fade-in">
        <img src={movie.Poster_Path} alt={movie.Series_Title}
             on:error={(e) => e.target.style.display='none'} />
        <div class="title">{movie.Series_Title}</div>
      </div>
    {/each}
  </div>
</div>

<style>
  .hero-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 1rem;
    border-bottom: 1px solid #facc15;
    padding-bottom: 0.5rem;
  }
  .hero-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: #facc15;
  }
  .movie-select label {
    font-size: 0.85rem;
    font-weight: bold;
    color: #facc15;
    margin-right: 0.5rem;
  }
  .movie-select select {
    background: #111;
    color: #facc15;
    border: 2px solid #facc15;
    border-radius: 4px;
    padding: 0.3rem 0.6rem;
    font-size: 0.85rem;
    cursor: pointer;
  }
  .movie-select select:focus { outline: none; border-color: #ffd700; }

  .home-btn {
    background: #facc15;
    color: black;
    border: none;
    font-size: 1.4rem;
    padding: 0.3rem 0.6rem;
    border-radius: 0;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .home-btn:hover { background: #ffd700; }
  .home-btn svg { stroke: black; }

  h2 {
    font-size: 1.2rem;
    font-weight: 600;
    color: #facc15;
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
    padding-bottom: 0.2rem;
    border-bottom: 1px solid #333;
  }
  .highlight { color: #ffd700; }

  .scroll-row {
    display: flex;
    gap: 1rem;
    overflow-x: auto;
    padding-bottom: 0.5rem;
    scroll-behavior: smooth;
  }
  .scroll-row::-webkit-scrollbar { display: none; }
  .scroll-row { -ms-overflow-style: none; scrollbar-width: none; }

  .card {
    flex: 0 0 auto;
    width: 150px;
    background: transparent;
    color: #fff;
    border-radius: 4px;
    overflow: hidden;
    box-shadow: 0 3px 8px rgba(0,0,0,0.3);
    text-align: center;
    transition: transform 0.3s ease, opacity 0.3s ease;
    opacity: 0;
    transform: translateY(20px);
  }
  .fade-in { animation: fadeIn 0.5s forwards; }
  @keyframes fadeIn { to { opacity: 1; transform: translateY(0); } }
  img { width: 100%; height: 220px; object-fit: cover; }
  .title {
    font-weight: bold;
    font-size: 0.8rem;
    padding: 0.3rem;
    color: #facc15;
  }

  .genre-select { margin-bottom: 1rem; }
  .genre-select label {
    font-weight: bold;
    color: #facc15;
    margin-right: 0.5rem;
  }
  .genre-select select {
    background: #111;
    color: #facc15;
    border: 2px solid #facc15;
    border-radius: 4px;
    padding: 0.3rem 0.6rem;
    font-size: 0.85rem;
    cursor: pointer;
  }
  .genre-select select:focus { outline: none; border-color: #ffd700; }
</style>
