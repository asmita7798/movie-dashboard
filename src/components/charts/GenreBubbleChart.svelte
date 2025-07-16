<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';
  export let imdbCSV = [];

  let container;
  let selectedGenres = ['Action/Adventure', 'Comedy', 'Drama', 'Crime/Thriller']; // default
  const genreGroupMap = {
    Action: 'Action/Adventure', Adventure: 'Action/Adventure',
    Comedy: 'Comedy',
    Drama: 'Drama', Biography: 'Drama', History: 'Drama',
    Romance: 'Romance', Musical: 'Romance',
    Crime: 'Crime/Thriller', Thriller: 'Crime/Thriller', Mystery: 'Crime/Thriller', 'Film-Noir': 'Crime/Thriller',
    Fantasy: 'Fantasy/Sci-Fi', 'Sci-Fi': 'Fantasy/Sci-Fi', Animation: 'Fantasy/Sci-Fi',
    Family: 'Family/Kids', Music: 'Family/Kids',
    Horror: 'Horror',
    War: 'War/Western', Western: 'War/Western',
    Sport: 'Sport'
  };

  const genreOptions = Array.from(new Set(Object.values(genreGroupMap))).sort();

  function toggleGenre(genre) {
    if (selectedGenres.includes(genre)) {
      selectedGenres = selectedGenres.filter(g => g !== genre);
    } else {
      selectedGenres = [...selectedGenres, genre];
    }
  }

  function drawChart() {
    d3.select(container).selectAll('*').remove();

    const margin = { top: 40, right: 200, bottom: 60, left: 80 };
    const width = 960;
    const height = 540;
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const svg = d3
      .select(container)
      .append('svg')
      .attr('width', width)
      .attr('height', height)
      .attr('viewBox', `0 0 ${width} ${height}`)
      .attr('preserveAspectRatio', 'xMidYMid meet')
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    const genreYearMap = new Map();

    imdbCSV.forEach(d => {
      const year = +d.Released_Year;
      const genres = d.Genre ? d.Genre.split(',').map(g => g.trim()) : [];
      const rating = parseFloat(d.IMDB_Rating);
      if (!isNaN(year) && rating && genres.length) {
        genres.forEach(genre => {
          const grouped = genreGroupMap[genre] || genre;
          const key = `${grouped}-${year}`;
          if (!genreYearMap.has(key)) {
            genreYearMap.set(key, { genre: grouped, year, totalRating: 0, count: 0 });
          }
          const entry = genreYearMap.get(key);
          entry.totalRating += rating;
          entry.count += 1;
        });
      }
    });

    let data = Array.from(genreYearMap.values())
      .map(d => ({
        genre: d.genre,
        year: d.year,
        avgRating: d.totalRating / d.count,
        count: d.count
      }))
      .filter(d => !isNaN(d.avgRating));

    if (selectedGenres.length > 0) {
      data = data.filter(d => selectedGenres.includes(d.genre));
    }

    const x = d3.scaleLinear()
      .domain(d3.extent(data, d => d.year))
      .range([0, innerWidth]);

    const y = d3.scaleLinear()
      .domain([5, 10])
      .range([innerHeight, 0]);

    const r = d3.scaleSqrt()
      .domain([0, d3.max(data, d => d.count)])
      .range([3, 20]);

    const color = d3.scaleOrdinal(d3.schemeCategory10);

    svg.append('g')
      .attr('transform', `translate(0,${innerHeight})`)
      .call(d3.axisBottom(x).tickFormat(d3.format('d')))
      .selectAll('text')
      .style('fill', 'white');

    svg.append('g')
      .call(d3.axisLeft(y))
      .selectAll('text')
      .style('fill', 'white');

    svg.append('text')
      .attr('x', innerWidth / 2)
      .attr('y', innerHeight + 50)
      .attr('text-anchor', 'middle')
      .style('fill', '#facc15')
      .style('font-size', '16px')
      .text('Released Year');

    svg.append('text')
      .attr('transform', `rotate(-90)`) 
      .attr('x', -innerHeight / 2)
      .attr('y', -60)
      .attr('text-anchor', 'middle')
      .style('fill', '#facc15')
      .style('font-size', '16px')
      .text('Average IMDb Rating');

    const tooltip = d3.select(container)
      .append('div')
      .style('position', 'absolute')
      .style('background', '#facc15')
      .style('color', 'black')
      .style('padding', '6px 10px')
      .style('border-radius', '6px')
      .style('font-size', '12px')
      .style('pointer-events', 'none')
      .style('opacity', 0);

    svg.selectAll('circle')
      .data(data)
      .enter()
      .append('circle')
      .attr('cx', d => x(d.year))
      .attr('cy', d => y(d.avgRating))
      .attr('r', d => r(d.count))
      .attr('fill', d => color(d.genre))
      .attr('opacity', 0.7)
      .on('mouseover', (event, d) => {
        tooltip
          .style('opacity', 1)
          .html(`<strong>${d.genre}</strong><br/>Year: ${d.year}<br/>Rating: ${d.avgRating.toFixed(2)}<br/>Movies: ${d.count}`);
      })
      .on('mousemove', event => {
        tooltip
          .style('left', event.offsetX + 15 + 'px')
          .style('top', event.offsetY - 28 + 'px');
      })
      .on('mouseout', () => {
        tooltip.style('opacity', 0);
      });

    const legend = svg.append('g')
      .attr('transform', `translate(${innerWidth + 30}, 0)`);

    const genresInView = [...new Set(data.map(d => d.genre))];

    genresInView.forEach((genre, i) => {
      legend.append('circle')
        .attr('cx', 0)
        .attr('cy', i * 24)
        .attr('r', 6)
        .attr('fill', color(genre));

      legend.append('text')
        .attr('x', 12)
        .attr('y', i * 24 + 5)
        .attr('fill', 'white')
        .style('font-size', '12px')
        .text(genre);
    });
  }

  onMount(drawChart);
  $: selectedGenres, drawChart();
</script>

<style>
  .chart-card {
    background-color: #1e1e1e;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(255, 255, 255, 0.05);
    max-width: 1200px;
    margin: auto;
    text-align: center;
  }

  .title {
    color: #facc15;
    font-weight: bold;
    font-size: 1.4rem;
    margin-bottom: 1.5rem;
  }

  .checkbox-list {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    justify-content: center;
    max-height: 180px;
    overflow-y: auto;
    margin-bottom: 1rem;
  }

  .checkbox-item {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    color: white;
    font-size: 13px;
  }

  input[type="checkbox"] {
    accent-color: #facc15;
    width: 14px;
    height: 14px;
  }
</style>

<div class="chart-card">
  <div class="title">📊 Genre Popularity: Year vs IMDb Rating</div>
  <p style="color:white; font-weight: bold;">Select Genre Groups:</p>
  <div class="checkbox-list">
    {#each genreOptions as genre}
      <div class="checkbox-item">
        <input
          type="checkbox"
          id={genre}
          value={genre}
          on:change={() => toggleGenre(genre)}
          checked={selectedGenres.includes(genre)}
        />
        <label for={genre}>{genre}</label>
      </div>
    {/each}
  </div>
  <div bind:this={container} style="width: 100%; position: relative;"></div>
</div>
