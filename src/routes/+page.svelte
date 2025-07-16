<script>
  import Header from '../components/Header.svelte';
  import MoviesPerYear from '../components/charts/MoviesPerYear.svelte';
  import AvgRatingOverYear from '../components/charts/AvgRatingOverTime.svelte';
  import MetaScoreOverYear from '../components/charts/MetaScoreOverTime.svelte'; // ✅ import this
  import GenreTrends from '../components/charts/GenreTrends.svelte';
  import GenreBubbleChart from '../components/charts/GenreBubbleChart.svelte';

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
</section>

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
</style>
