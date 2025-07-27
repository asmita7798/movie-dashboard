<script>
  export let imdbCSV = [];
  export let currentView;

  const validRows = imdbCSV.filter(row =>
    row['IMDB_Rating'] && row['Released_Year'] && row['Runtime']
  );

  const totalMovies = validRows.length;
  const avgRating = (
    validRows.reduce((sum, row) => sum + parseFloat(row['IMDB_Rating']), 0) / totalMovies
  ).toFixed(1);

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
    position: relative;
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
    font-size: 1.5rem;
    font-weight: 800;
    margin: 0;
  }

  .recommend-btn {
    position: absolute;
    right: 2rem;
    top: 50%;
    transform: translateY(-50%);
    background: #111;
    color: #facc15;
    border: none;
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
    border-radius: 6px;
    cursor: pointer;
    box-shadow: 0 2px 6px rgba(0,0,0,0.4);
    transition: all 0.2s ease;
  }
  .recommend-btn:hover {
    background: #333;
    transform: translateY(-50%) scale(1.05);
  }

  .stats.single-row {
    display: grid;
    grid-template-columns: repeat(10, 1fr);
    gap: 0.8rem;
    width: 100%;
    padding: 1rem 2rem;
    box-sizing: border-box;
  }
  .horizontal-divider {
    border: none;
    border-top: 2px solid #facc15;
    margin: 1.5rem 2rem;
    width: calc(100% - 4rem);
  }

  .stat-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: #111;
    border-radius: 10px;
    height: 80px;
    width: 100%;
    box-shadow: 0px 3px 8px rgba(0, 0, 0, 0.6);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }
  .stat-card:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.7);
  }
  .stat-value {
    font-size: 1.1rem;
    font-weight: bold;
    color: #facc15;
    text-align: center;
  }
  .stat-label {
    font-size: 0.85rem;
    color: #ccc;
    text-align: center;
  }

  @media (max-width: 1200px) {
    .stats.single-row {
      grid-template-columns: repeat(5, 1fr);
    }
  }
  @media (max-width: 768px) {
    .stats.single-row {
      grid-template-columns: repeat(2, 1fr);
    }
  }
</style>

<div class="header-full">
  <div class="header-content">
    <h1>IMDb Top 1000 Movie Dashboard</h1>
    <button class="recommend-btn" on:click={() => currentView = 'recommendations'}>
      Explore
    </button>
  </div>
</div>

{#if currentView === 'dashboard'}
  <div class="stats single-row">
    <div class="stat-card"><div class="stat-value">{totalMovies}</div><div class="stat-label">Total Movies</div></div>
    <div class="stat-card"><div class="stat-value">{avgRating}</div><div class="stat-label">Avg IMDb Rating</div></div>
    <div class="stat-card"><div class="stat-value">{totalDirectors}</div><div class="stat-label">Directors</div></div>
    <div class="stat-card"><div class="stat-value">{totalStars}</div><div class="stat-label">Stars</div></div>
    <div class="stat-card"><div class="stat-value">{avgRuntime} min</div><div class="stat-label">Avg Runtime</div></div>
    <div class="stat-card"><div class="stat-value">{genreCount}</div><div class="stat-label">Genres</div></div>
    <div class="stat-card"><div class="stat-value">{popularDirector}</div><div class="stat-label">Most Movies Directed</div></div>
    <div class="stat-card"><div class="stat-value">{popularStar}</div><div class="stat-label">Most Appeared Star</div></div>
    <div class="stat-card"><div class="stat-value">{topGenre}</div><div class="stat-label">Genre with Most Movies</div></div>
    <div class="stat-card"><div class="stat-value">{topRatedMovie}</div><div class="stat-label">Top IMDb Movie</div></div>
  </div>
  <hr class="horizontal-divider" />
{/if}
