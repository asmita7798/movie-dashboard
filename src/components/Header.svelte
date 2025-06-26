<script>
    import FlipCard from './FlipCard.svelte';
  export let imdbCSV = [];

  // Filter valid rows
  const validRows = imdbCSV.filter(row =>
    row['IMDB_Rating'] && row['Released_Year'] && row['Runtime']
  );

  const totalMovies = validRows.length;

  const avgRating = (
    validRows.reduce((sum, row) => sum + parseFloat(row['IMDB_Rating']), 0) / totalMovies
  ).toFixed(1);

  const avgDuration = (
    validRows.reduce((sum, row) => {
      const match = row['Runtime'].match(/\d+/);
      return sum + (match ? parseInt(match[0]) : 0);
    }, 0) / totalMovies
  ).toFixed(0);

  const yearCounts = {};
  validRows.forEach(row => {
    const year = row['Released_Year'];
    yearCounts[year] = (yearCounts[year] || 0) + 1;
  });
  const commonYear = Object.entries(yearCounts).reduce((a, b) => a[1] > b[1] ? a : b)[0];
  // Unique genre count
const genreSet = new Set();
validRows.forEach(row => {
  row['Genre']?.split(',').forEach(g => genreSet.add(g.trim()));
});
const genreCount = genreSet.size;

// Avg Gross Revenue
const grossValues = validRows
  .map(row => parseFloat(row['Gross']?.replace(/[$,]/g, '')))
  .filter(val => !isNaN(val));
const avgGross = (
  grossValues.reduce((sum, val) => sum + val, 0) / grossValues.length
).toLocaleString('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });


// Most frequent Director
const directorCount = {};
validRows.forEach(row => {
  const d = row['Director'];
  if (d) directorCount[d] = (directorCount[d] || 0) + 1;
});
const popularDirector = Object.entries(directorCount).reduce((a, b) => a[1] > b[1] ? a : b)[0];

// Most frequent Star (from Star1–4)
const starCount = {};
['Star1', 'Star2', 'Star3', 'Star4'].forEach(col => {
  validRows.forEach(row => {
    const s = row[col];
    if (s) starCount[s] = (starCount[s] || 0) + 1;
  });
});
const popularStar = Object.entries(starCount).reduce((a, b) => a[1] > b[1] ? a : b)[0];

// Top 5 movies from commonYear
const topMoviesInYear = validRows
  .filter(row => row['Released_Year'] === commonYear)
  .sort((a, b) => parseFloat(b['IMDB_Rating']) - parseFloat(a['IMDB_Rating']))
  .slice(0, 5)
  .map(movie => ({
    title: movie['Series_Title'],
    rating: movie['IMDB_Rating']
  }));

// Rating min/max
const ratings = validRows.map(row => parseFloat(row['IMDB_Rating']));
const minRating = Math.min(...ratings).toFixed(1);
const maxRating = Math.max(...ratings).toFixed(1);

// Duration min/max
const durations = validRows
  .map(row => parseInt(row['Runtime'].match(/\d+/)?.[0] || 0))
  .filter(d => d > 0);
const minDuration = Math.min(...durations);
const maxDuration = Math.max(...durations);

</script>

<style>
  :global(body) {
    margin: 0;
    font-family: 'Montserrat', sans-serif;
    background-color: #000;
    color: white;
  }

  .header {
    padding: 2rem;
    background: linear-gradient(to right, #000, #111);
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
  }

  .header h1 {
    font-size: 2.5rem;
    font-weight: 700;
    color: #facc15;
  }

  .header-icon {
    width: 120px;
    height: 120px;
    margin-right: 0.75rem;
  }
  
  .subtitle {
    text-align: center;
    font-size: 1.7rem;
    font-weight: 400;
    margin-top: 0.25rem;
    color: #d1d5db;
  }

.stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  padding: 2rem;
  justify-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.stat-card {
  background-color: #1a1a1a;
  padding: 1.5rem 1rem;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
  text-align: center;
  min-width: 180px;
  max-width: 260px;
  width: 100%;
  
}
.stat-card:hover {
  transform: scale(1.05);
  box-shadow: 0 0 15px rgba(255, 255, 0, 0.3);
}

.stat-value {
  font-size: 1.9rem;
  font-weight: bold;
  color: #facc15;
  white-space: nowrap;
  overflow-wrap: break-word;
}

.stat-label {
  font-size: 1.2rem;
  color: #ccc;
  margin-top: 0.3rem;
}

</style>

<div class="header">
  <img class="header-icon" src="/header_icon.png" alt="Movie Icon" />
  <h1><span style="font-weight: 800;">IMDb</span> Movie Dashboard</h1>
</div>
<div class="subtitle">Discover trends, genres, and legends from the top 1000 IMDb titles over a span of 100 years.</div>

<div class="stats">
  <div class="stat-card">
    <div class="stat-value">{totalMovies}</div>
    <div class="stat-label">Total Movies</div>
  </div>

  <!-- IMDb Rating -->
<FlipCard>
  <div slot="front">
    <div class="stat-value">{avgRating}</div>
    <div class="stat-label">Avg IMDb Rating</div>
  </div>
  <div slot="back">
    <div class="stat-label">Rating Range</div>
    <div style="font-size: 1.1rem; margin-top: 0.3rem;">{minRating} ⭐ — {maxRating} ⭐</div>
  </div>
</FlipCard>

  <!-- Most Frequent Year -->
<FlipCard>
  <div slot="front">
    <div class="stat-value">{commonYear}</div>
    <div class="stat-label">Top Release Year</div>
  </div>
  <div slot="back">
    <div class="stat-label">Top 5 Movies in {commonYear}</div>
    <ul style="margin-top: 0.5rem; font-size: 0.9rem; padding: 0; list-style: none;">
      {#each topMoviesInYear as movie}
        <li>{movie.title} ({movie.rating})</li>
      {/each}
    </ul>
  </div>
</FlipCard>

<!-- Avg Duration -->
<FlipCard>
  <div slot="front">
    <div class="stat-value">{avgDuration}m</div>
    <div class="stat-label">Avg Duration</div>
  </div>
  <div slot="back">
    <div class="stat-label">Duration Range</div>
    <div style="font-size: 1.1rem; margin-top: 0.3rem;">{minDuration}m — {maxDuration}m</div>
  </div>
</FlipCard>

  <div class="stat-card">
    <div class="stat-value">{genreCount}</div>
    <div class="stat-label">Genres</div>
  </div>
  <div class="stat-card">
    <div class="stat-value">{avgGross}</div>
    <div class="stat-label">Avg Gross</div>
  </div>
  <div class="stat-card">
    <div class="stat-value">{popularDirector}</div>
    <div class="stat-label">Top Director</div>
  </div>
  <div class="stat-card">
    <div class="stat-value">{popularStar}</div>
    <div class="stat-label">Top Star</div>
  </div>
</div>
