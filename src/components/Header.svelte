<script>
  import FlipCard from './Flipcard.svelte';
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
  validRows.forEach(row => {
    row['Genre']?.split(',').forEach(g => genreSet.add(g.trim()));
  });
  const genreCount = genreSet.size;

  const directorCount = {};
  validRows.forEach(row => {
    const d = row['Director'];
    if (d) directorCount[d] = (directorCount[d] || 0) + 1;
  });
  const popularDirector = Object.entries(directorCount).reduce((a, b) => a[1] > b[1] ? a : b)[0];

  const starCount = {};
  ['Star1', 'Star2', 'Star3', 'Star4'].forEach(col => {
    validRows.forEach(row => {
      const s = row[col];
      if (s) starCount[s] = (starCount[s] || 0) + 1;
    });
  });
  const popularStar = Object.entries(starCount).reduce((a, b) => a[1] > b[1] ? a : b)[0];

  // Top Genre (most common)
const genreCountMap = {};
validRows.forEach(row => {
  row['Genre']?.split(',').forEach(g => {
    const genre = g.trim();
    genreCountMap[genre] = (genreCountMap[genre] || 0) + 1;
  });
});
const topGenre = Object.entries(genreCountMap).reduce((a, b) => a[1] > b[1] ? a : b)[0];

// Top movie by top director
const topDirectorMovie = validRows
  .filter(row => row['Director'] === popularDirector)
  .sort((a, b) => parseFloat(b['IMDB_Rating']) - parseFloat(a['IMDB_Rating']))[0]?.Series_Title;

// Top movie by top star
const topStarMovie = validRows
  .filter(row =>
    [row['Star1'], row['Star2'], row['Star3'], row['Star4']].includes(popularStar)
  )
  .sort((a, b) => parseFloat(b['IMDB_Rating']) - parseFloat(a['IMDB_Rating']))[0]?.Series_Title;

</script>


<style>
  :global(body) {
    margin: 0;
    font-family: 'Montserrat', sans-serif;
    background-color: #000;
    color: white;
  }

 .header {
  display: flex;
  flex-direction: row;       /* ← this is key */
  align-items: center;
  justify-content: flex-start;
  gap: 0rem;
  padding: 1.5rem 2rem;               /* ✅ Add some spacing inside */
  margin: 2rem 0; 
  max-width: 100%;
  width: 100%;
  background-color: #1a1a1a;
  border-radius: 0px;
  box-shadow: 0 4px 12px rgba(255, 255, 0, 0.15);
  box-sizing: border-box;
}


.header h1 {
  font-size: 2.2rem;
  margin: 0;
  color: #facc15;
  font-weight: 700;
}

.header-icon {
  width: 100px;
  height: 100px;
  margin-right: 1rem;
}

  
  .subtitle {
    text-align: center;
    font-size: 1.7rem;
    font-weight: 400;
    margin-top: 0.2rem;
    color: #d1d5db;
  }

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));  /* Match the min-width */
  gap: 2rem;
  padding: 2rem;
  max-width: 1300px;
  margin: 0 auto;
  width: 100%;
}

.stat-value {
  font-size: 2rem;
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

 <FlipCard>
  <div slot="front">
    <div class="stat-value">{genreCount}</div>
    <div class="stat-label">Genres</div>
  </div>
  <div slot="back">
    <div class="stat-label">Top Genre</div>
    <div style="font-size: 1.1rem; margin-top: 0.3rem;">{topGenre}</div>
  </div>
</FlipCard>

  
  <FlipCard>
  <div slot="front">
    <div class="stat-value">{popularDirector}</div>
    <div class="stat-label">Top Director</div>
  </div>
  <div slot="back">
    <div class="stat-label">Top Movie</div>
    <div style="font-size: 1.1rem; margin-top: 0.3rem;">{topDirectorMovie}</div>
  </div>
</FlipCard>

 <FlipCard>
  <div slot="front">
    <div class="stat-value">{popularStar}</div>
    <div class="stat-label">Top Star</div>
  </div>
  <div slot="back">
    <div class="stat-label">Top Movie</div>
    <div style="font-size: 1.1rem; margin-top: 0.3rem;">{topStarMovie}</div>
  </div>
</FlipCard>

</div>