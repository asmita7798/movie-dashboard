<script>
  export let imdbCSV = [];

  const validRows = imdbCSV.filter(row =>
    row['IMDB_Rating'] && row['Released_Year'] && row['Runtime']
  );

  const totalMovies = validRows.length;

  const avgRating = (
    validRows.reduce((sum, row) => sum + parseFloat(row['IMDB_Rating']), 0) / totalMovies
  ).toFixed(1);

  const ratings = validRows.map(row => parseFloat(row['IMDB_Rating']));
  const minRating = Math.min(...ratings).toFixed(1);
  const maxRating = Math.max(...ratings).toFixed(1);

  const genreSet = new Set();
  validRows.forEach(row => row['Genre']?.split(',').forEach(g => genreSet.add(g.trim())));
  const genreCount = genreSet.size;

  const directorCount = {};
  validRows.forEach(row => {
    const d = row['Director'];
    if (d) directorCount[d] = (directorCount[d] || 0) + 1;
  });
  const totalDirectors = Object.keys(directorCount).length;
  const popularDirector = Object.entries(directorCount).reduce((a, b) => a[1] > b[1] ? a : b)[0];

  const starCount = {};
  ['Star1', 'Star2', 'Star3', 'Star4'].forEach(col =>
    validRows.forEach(row => {
      const s = row[col];
      if (s) starCount[s] = (starCount[s] || 0) + 1;
    })
  );
  const totalStars = Object.keys(starCount).length;
  const popularStar = Object.entries(starCount).reduce((a, b) => a[1] > b[1] ? a : b)[0];

  const avgRuntime = (
    validRows.reduce((sum, row) => sum + parseInt(row['Runtime']), 0) / totalMovies
  ).toFixed(0);

  const genreCountMap = {};
  validRows.forEach(row =>
    row['Genre']?.split(',').forEach(g => {
      const genre = g.trim();
      genreCountMap[genre] = (genreCountMap[genre] || 0) + 1;
    })
  );
  const topGenre = Object.entries(genreCountMap).reduce((a, b) => a[1] > b[1] ? a : b)[0];

  const topRatedMovie = validRows.sort((a, b) =>
    parseFloat(b['IMDB_Rating']) - parseFloat(a['IMDB_Rating'])
  )[0]?.Series_Title;
</script>

<style>
  .header-full {
    background-color: #facc15;
    border-bottom: 4px solid #eab308;
    width: 100%;
    padding: 0.8rem 0;
  }
  .header-content {
    display: flex;
    align-items: center;
    justify-content: center;
    max-width: 1300px;
    margin: 0 auto;
    padding: 0 2rem;
  }
  .header-content h1 {
    color: black;
    font-size: 2.5rem;
    font-weight: 800;
    margin: 0;
  }
  .subtitle {
    text-align: center;
    font-size: 1.4rem;
    font-weight: 400;
    margin-top: 0.5rem;
    color: #d1d5db;
  }

  /* Compact headings */
  .section-heading {
    color: #facc15;
    font-weight: bold;
    font-size: 1.4rem;
    text-align: center;
    margin: 0.8rem 0 0.5rem; /* reduced spacing */
  }
  .section-heading:first-of-type {
    margin-top: 0.5rem; /* make Overview closer to subtitle */
  }

  /* Card grid layouts */
  .stats.overview {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 0.6rem; /* tighter spacing */
    max-width: 1000px;
    margin: 0 auto;
    padding: 0.5rem; /* reduced padding */
  }
  .stats.insights {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.6rem;
    max-width: 800px;
    margin: 0 auto;
    padding: 0.5rem;
  }

  /* Card styling */
  .stat-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: #111;
    border-radius: 10px;
    height: 80px;  /* slightly shorter */
    width: 100%;
    box-shadow: 0px 3px 8px rgba(0, 0, 0, 0.6);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }
  .stat-card:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.7);
  }

  .stat-value {
    font-size: 1.1rem; /* slightly smaller for compactness */
    font-weight: bold;
    color: #facc15;
    text-align: center;
  }
  .stat-label {
    font-size: 0.85rem;
    color: #ccc;
    text-align: center;
  }
  .label-explanation {
  display: block; /* moves to next line */
  font-size: 0.75rem; /* smaller font */
  color: #aaa;       /* lighter color */
  margin-top: 0.2rem;
}

</style>

<div class="header-full">
  <div class="header-content">
    <h1>IMDb Movie Dashboard</h1>
  </div>
</div>
<div class="subtitle">
  Discover trends, genres, and legends from the top 1000 IMDb titles over a span of 100 years.
</div>

<!-- Overview Cards -->
<div class="section-heading">Key Stats at a Glance</div>
<div class="stats overview">
  <div class="stat-card">
    <div class="stat-value">{totalMovies}</div>
    <div class="stat-label">Total Movies</div>
  </div>
  <div class="stat-card">
    <div class="stat-value">{avgRating}</div>
    <div class="stat-label">Avg IMDb Rating</div>
  </div>
  <div class="stat-card">
    <div class="stat-value">{totalDirectors}</div>
    <div class="stat-label">Directors</div>
  </div>
  <div class="stat-card">
    <div class="stat-value">{totalStars}</div>
    <div class="stat-label">Stars</div>
  </div>
  <div class="stat-card">
    <div class="stat-value">{avgRuntime} min</div>
    <div class="stat-label">Avg Runtime</div>
  </div>
  <div class="stat-card">
    <div class="stat-value">{genreCount}</div>
    <div class="stat-label">Genres</div>
  </div>
</div>

<!-- Insight Cards -->
<div class="section-heading">Top Performers & Trends</div>
<div class="stats insights">
  <div class="stat-card">
    <div class="stat-value">{popularDirector}</div>
    <div class="stat-label">
  Top Director <span class="label-explanation">(by total movies)</span>
</div>
  </div>
  <div class="stat-card">
    <div class="stat-value">{popularStar}</div>
    <div class="stat-label">
  Top Star <span class="label-explanation">(by total appearances)</span>
</div>
  </div>
  <div class="stat-card">
    <div class="stat-value">{topGenre}</div>
    <div class="stat-label">
  Top Genre <span class="label-explanation">(by total movies)</span>
</div>
  </div>
  <div class="stat-card">
    <div class="stat-value">{topRatedMovie}</div>
    <div class="stat-label">
  Top Rated Movie <span class="label-explanation">(by IMDb rating)</span>
</div>
  </div>
</div>
