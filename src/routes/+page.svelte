<script>
  import Header from '../components/Header.svelte';
  import MoviesPerYear from '../components/charts/MoviesPerYear.svelte';
  import GenreBubbleChart from '../components/charts/GenreBubbleChart.svelte';
  import TopGrossingMovies from '../components/charts/TopGrossingMovies.svelte';
  import AvgGrossPerDecade from '../components/charts/AvgGrossPerDecade.svelte';
  import TopDirectorsbyMovies from '../components/charts/TopDirectorsbyMovies.svelte';
  import TopDirectorsbyGrossRevenue from '../components/charts/TopDirectorsbyGrossRevenue.svelte';
  import StarDirectorNetwork from '../components/charts/StarDirectorNetwork.svelte';
  import RatingsOverTime from '../components/charts/RatingsOverTime.svelte';
  import StarHeatmap from '../components/charts/StarHeatmap.svelte';

  export let data;
  const { imdbCSV } = data;
</script>

<Header {imdbCSV} />

<section class="chart-section">
  <div class="container">

    <!-- Row 1: three charts -->
    <div class="flex-row three-charts">
      <div class="flex-item"><MoviesPerYear {imdbCSV} /></div>
      <div class="flex-item"><AvgGrossPerDecade {imdbCSV} /></div>
      <div class="flex-item"><TopGrossingMovies {imdbCSV} /></div>
    </div>

    <!-- Row 2: full-width Genre Bubble chart -->
    <div class="flex-row full-width">
      <div class="flex-item bubble-box"><GenreBubbleChart {imdbCSV} /></div>
    </div>

    <!-- Row 3: three charts -->
    <div class="flex-row three-charts">
      <div class="flex-item"><RatingsOverTime {imdbCSV} /></div>
      <div class="flex-item"><TopDirectorsbyMovies {imdbCSV} /></div>
      <div class="flex-item"><TopDirectorsbyGrossRevenue {imdbCSV} /></div>
    </div>

    <!-- Row 4: two charts -->
    <div class="flex-row two-charts">
      <div class="flex-item"><StarHeatmap {imdbCSV} /></div>
      <div class="flex-item"><StarDirectorNetwork {imdbCSV} /></div>
    </div>

  </div>
</section>

<footer class="sticky-footer">
  © 2025 <strong>Asmita Sengupta</strong>
</footer>

<style>
  .chart-section {
    padding: 2rem 2rem;
    background: #0a0a0a;
  }

  .container {
    max-width: 1300px;
    margin: 0 auto;
    padding: 0 1rem;
  }

  .flex-row {
    display: flex;
    justify-content: space-between;
    gap: 2rem;
    margin-bottom: 2rem; /* spacing between rows */
    flex-wrap: nowrap;
  }

  /* Row 1 & Row 3 (3 charts each) */
  .three-charts .flex-item {
    flex: 1 1 30%;
    height: 400px;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .three-charts .flex-item > :global(*) {
    width: 100% !important;
    height: 100% !important;
  }

  /* Row 2 (full width Genre Bubble chart) */
  .full-width .flex-item.bubble-box {
    flex: 1 1 100%;
    min-height: 400px;
    display: flex;
    justify-content: center;
    align-items: flex-start; /* align top */
    padding: 1rem; /* uniform top/bottom/left/right */
    box-sizing: border-box;
  }
  /* Adjust internal bubble chart width like top row */
  .full-width .flex-item.bubble-box > :global(*) {
    width: 95% !important;
    height: auto !important;
  }
  /* Adjust title spacing */
  .full-width .flex-item.bubble-box :global(.title) {
    margin-bottom: 0.75rem;
  }

  /* Row 4 (two charts) */
  .two-charts .flex-item {
    flex: 1 1 48%;
    height: 400px;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .two-charts .flex-item > :global(*) {
    width: 100% !important;
    height: 100% !important;
  }

  /* Responsive breakpoints */
  @media (max-width: 1100px) {
    .flex-row {
      flex-wrap: wrap;
    }
    .three-charts .flex-item,
    .two-charts .flex-item,
    .full-width .flex-item {
      flex: 1 1 100%;
      height: 350px;
      margin-bottom: 2rem;
    }
    .full-width .flex-item.bubble-box {
      min-height: 500px;
    }
  }

  @media (max-width: 700px) {
    .three-charts .flex-item,
    .two-charts .flex-item,
    .full-width .flex-item {
      flex: 1 1 100%;
      height: 300px;
    }
    .full-width .flex-item.bubble-box {
      min-height: 450px;
    }
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
  }
</style>
