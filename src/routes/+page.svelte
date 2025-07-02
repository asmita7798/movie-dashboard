<script>
  import Header from '../components/Header.svelte';
  import MoviesPerYear from '../components/charts/MoviesPerYear.svelte';
  import AvgRatingOverYear from '../components/charts/AvgRatingOverTime.svelte';
  import GenreTrends from '../components/charts/GenreTrends.svelte'; // ⬅️ NEW chart import

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

  <div
    style="
      display: flex;
      flex-wrap: wrap;
      gap: 2rem;
      justify-content: center;
      align-items: flex-start;
    "
  >
    <MoviesPerYear {imdbCSV} />
    <AvgRatingOverYear {imdbCSV} />
  </div>

  <GenreTrends {imdbCSV} /> <!-- ⬅️ ADDED below the 2 charts -->
</section>

<style>
  .section-heading-clean {
    color: #facc15;
    font-weight: bold;
    font-size: 1.6rem;
    text-align: center;
    margin-top: 2rem;     /* 🔽 Reduced top space */
    margin-bottom: 2.5rem; /* 🔽 Increased bottom space for better gap with charts */
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
