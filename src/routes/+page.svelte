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

  export let data;
  const { imdbCSV } = data;
</script>

<Header {imdbCSV} />

<section class="chart-section">
  <div class="section-heading-clean">🎬 Understanding Trends Over Time</div>

  <div class="container">

    <!-- First row: two charts side by side -->
    <div class="flex-row">
      <div class="flex-item">
        <MoviesPerYear {imdbCSV} />
      </div>
      <div class="flex-item">
        <TopGrossingMovies {imdbCSV} />
      </div>
    </div>

    <!-- Second row: two charts side by side -->
    <div class="flex-row">
      <div class="flex-item">
        <TopDirectorsbyMovies {imdbCSV} />
      </div>
      <div class="flex-item">
        <TopDirectorsbyGrossRevenue {imdbCSV} />
      </div>
    </div>

    
    <!-- Rest of the charts -->
    <div class="chart-grid">
      <RatingsOverTime {imdbCSV} />
    </div>

    <div class="chart-wrapper">
      <GenreBubbleChart {imdbCSV} />
    </div>

    <div class="chart-wrapper">
      <AvgGrossPerDecade {imdbCSV} />
    </div>

    <div class="chart-wrapper">
      <StarDirectorNetwork {imdbCSV} />
    </div>

  </div>
</section>

<footer class="sticky-footer">
  © 2025 <strong>Asmita Sengupta</strong>
</footer>

<style>
  :global(body) {
    overflow-x: hidden; /* prevent horizontal scroll globally */
  }

  .chart-section {
    padding: 2rem;
    background: #0a0a0a;
  }

  .container {
    max-width: 1300px;
    margin: 0 auto;
    padding: 0 1rem;
  }

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

  /* Flex container for side by side charts */
  .flex-row {
    display: flex;
    justify-content: space-between;
    gap: 2rem;
    margin-bottom: 2rem;
    flex-wrap: wrap;
  }

  /* Each chart takes about half width, limited max */
  .flex-item {
    flex: 1 1 48%;
    max-width: 600px;
    box-sizing: border-box;
  }

  /* Make chart components responsive */
  .flex-item > :global(*) {
    width: 100% !important;
    height: auto !important;
  }

  .chart-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 2rem;
    justify-content: center;
    align-items: flex-start;
    margin-bottom: 2rem;
  }

  .chart-wrapper {
    display: flex;
    justify-content: center;
    margin-bottom: 2rem;
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

  /* Responsive stacking on narrow viewports */
  @media (max-width: 700px) {
    .flex-row {
      flex-direction: column;
    }
    .flex-item {
      max-width: 100%;
      flex-basis: 100%;
    }
  }
</style>
