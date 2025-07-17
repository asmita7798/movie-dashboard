<script>
  import Header from '../components/Header.svelte';
  import MoviesPerYear from '../components/charts/MoviesPerYear.svelte';
  import AvgRatingOverYear from '../components/charts/AvgRatingOverTime.svelte';
  import MetaScoreOverYear from '../components/charts/MetaScoreOverTime.svelte';
  import GenreTrends from '../components/charts/GenreTrends.svelte';
  import GenreBubbleChart from '../components/charts/GenreBubbleChart.svelte';
  import TopGrossingMovies from '../components/charts/TopGrossingMovies.svelte';
  import AvgGrossPerDecade from '../components/charts/AvgGrossPerDecade.svelte';
  import TopDirectors from '../components/charts/TopDirectors.svelte';
  import StarDirectorNetwork from '../components/charts/StarDirectorNetwork.svelte';

  export let data;
  const { imdbCSV } = data;
</script>

<!-- Header Section -->
<Header {imdbCSV} />

<!-- Chart Section: Understanding Trends Over Time -->
<section style="padding: 2rem;">
  <div class="section-heading-clean">
    🎬 Understanding Trends Over Time
  </div>

  <!-- Chart 1: Films Released Each Year -->
  <div
    style="
      display: flex;
      justify-content: center;
      margin-bottom: 2rem;
    "
  >
    <MoviesPerYear {imdbCSV} />
  </div>
  <div style="margin-top: 3rem;">
  <TopDirectors {imdbCSV} />
</div>
  <!-- Chart 2 & 3: Side-by-side Rating Comparisons -->
  <div
    style="
      display: flex;
      flex-wrap: wrap;
      gap: 2rem;
      justify-content: center;
      align-items: flex-start;
      margin-bottom: 2rem;
    "
  >
    <AvgRatingOverYear {imdbCSV} />
    <MetaScoreOverYear {imdbCSV} />
  </div>

  <!-- Chart 4: Genre Trends -->
<GenreTrends {imdbCSV} />

<!-- Chart 5: Genre-Year IMDb Bubble Chart -->
<div style="margin-top: 3rem;">
  <GenreBubbleChart {imdbCSV} />
</div>

<!-- Chart 6: Top Grossing Movies -->
<div style="margin-top: 3rem;">
  <TopGrossingMovies {imdbCSV} />
</div>

<!-- Chart 7: Avg Gross Revenue Per Decade -->
 <div style="margin-top: 3rem;">
  <AvgGrossPerDecade {imdbCSV} />
</div>
<!-- Chart 8: Star-Director / Star-Star Network Map -->
<div style="margin-top: 3rem;">
  <StarDirectorNetwork {imdbCSV} />
</div>
</section>
<footer class="sticky-footer">
  © 2025 <strong>Asmita Sengupta</strong>
</footer>

<style>
  .section-heading-clean {
    color: #facc15;
    font-weight: bold;
    font-size: 1.6rem;
    text-align: center;
    margin-top: 2rem;
    margin-bottom: 2.5rem;
    position: relative;
  }

  .section-heading-clean::after {
    content: '';
    display: block;
    width: 220px;
    height: 4px;
    background: #facc15;
    margin: 10px auto 0;
    border-radius: 2px;
  }
  .sticky-footer {
  position: fixed;
  bottom: 0;
  width: 100%;
  background-color: #facc15;
  color: black;
  text-align: left;
  padding: 12px;
  font-size: 14px;
  z-index: 9999;
  font-family: 'Segoe UI', sans-serif;
}

</style>
