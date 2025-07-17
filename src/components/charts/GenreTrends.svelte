<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  export let imdbCSV = [];
  let container;
  let tooltip;
  let selectedGenres = ['Drama', 'Action', 'Comedy', 'Thriller', 'Romance'];

  let allGenres = [];

  function drawChart() {
    const margin = { top: 40, right: 150, bottom: 60, left: 60 };
    const width = 1000;
    const height = 400;

    d3.select(container).selectAll('*').remove();

    const svg = d3
      .select(container)
      .append('svg')
      .attr('width', width)
      .attr('height', height)
      .attr('viewBox', `0 0 ${width} ${height}`)
      .attr('preserveAspectRatio', 'xMidYMid meet')
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const dataByYear = d3.rollup(
      imdbCSV,
      v => {
        const genreCounts = {};
        v.forEach(d => {
          const genres = d.Genre ? d.Genre.split(',').map(g => g.trim()) : [];
          genres.forEach(genre => {
            genreCounts[genre] = (genreCounts[genre] || 0) + 1;
          });
        });
        return genreCounts;
      },
      d => +d.Released_Year
    );

    const years = Array.from(dataByYear.keys()).sort((a, b) => a - b);
    const genresSet = new Set();
    dataByYear.forEach(counts => Object.keys(counts).forEach(g => genresSet.add(g)));
    allGenres = Array.from(genresSet);

    allGenres.sort((a, b) => {
      const sumA = d3.sum(years.map(year => (dataByYear.get(year)?.[a] || 0)));
      const sumB = d3.sum(years.map(year => (dataByYear.get(year)?.[b] || 0)));
      return sumB - sumA;
    });

    const genres = selectedGenres;

    const stackedData = years.map(year => {
      const base = { year };
      const yearData = dataByYear.get(year) || {};
      genres.forEach(g => base[g] = yearData[g] || 0);
      return base;
    });

    const stackedSeries = d3.stack().keys(genres)(stackedData);

    const x = d3.scaleLinear()
      .domain(d3.extent(years))
      .range([0, innerWidth]);

    const y = d3.scaleLinear()
      .domain([0, d3.max(stackedSeries, layer => d3.max(layer, d => d[1]))])
      .range([innerHeight, 0]);

    const color = d3.scaleOrdinal()
      .domain(genres)
      .range(d3.schemeCategory10.concat(d3.schemeSet3));

    const area = d3.area()
      .x(d => x(d.data.year))
      .y0(d => y(d[0]))
      .y1(d => y(d[1]))
      .curve(d3.curveCatmullRom);

    svg.selectAll('path')
      .data(stackedSeries)
      .enter()
      .append('path')
      .attr('d', area)
      .attr('fill', d => color(d.key))
      .attr('opacity', 0.85)
      .on('mouseover', function (event, d) {
        d3.select(this).attr('opacity', 1);
        tooltip.style('opacity', 1).html(`<strong>Genre:</strong> ${d.key}`);
      })
      .on('mousemove', function (event) {
        tooltip.style('left', event.offsetX + 20 + 'px')
               .style('top', event.offsetY - 20 + 'px');
      })
      .on('mouseout', function () {
        d3.select(this).attr('opacity', 0.85);
        tooltip.style('opacity', 0);
      });

    svg.append('g')
      .attr('transform', `translate(0,${innerHeight})`)
      .call(d3.axisBottom(x).tickFormat(d3.format("d")))
      .selectAll('text')
      .style('fill', 'white')
      .style('font-size', '13px');

    svg.append('g')
      .call(d3.axisLeft(y).ticks(5))
      .selectAll('text')
      .style('fill', 'white')
      .style('font-size', '13px');

    svg.append('text')
      .attr('text-anchor', 'middle')
      .attr('x', innerWidth / 2)
      .attr('y', innerHeight + 40)
      .text('Year')
      .attr('fill', '#facc15')
      .style('font-size', '16px');

    svg.append('text')
      .attr('text-anchor', 'middle')
      .attr('transform', `translate(-40, ${innerHeight / 2}) rotate(-90)`)
      .text('Movies Released per Genre')
      .attr('fill', '#facc15')
      .style('font-size', '16px');

    tooltip = d3.select(container)
      .append('div')
      .style('position', 'absolute')
      .style('background', '#facc15')
      .style('color', '#000')
      .style('padding', '6px 10px')
      .style('font-size', '13px')
      .style('border-radius', '5px')
      .style('pointer-events', 'none')
      .style('opacity', 0);

    const legend = svg.append('g')
      .attr('transform', `translate(${innerWidth + 20}, 0)`);

    genres.forEach((genre, i) => {
      legend.append('circle')
        .attr('cx', 6)
        .attr('cy', i * 20 + 6)
        .attr('r', 6)
        .attr('fill', color(genre));

      legend.append('text')
        .attr('x', 18)
        .attr('y', i * 20 + 10)
        .text(genre)
        .attr('fill', 'white')
        .style('font-size', '12px');
    });
  }

  function toggleGenre(genre) {
    if (selectedGenres.includes(genre)) {
      selectedGenres = selectedGenres.filter(g => g !== genre);
    } else {
      selectedGenres = [...selectedGenres, genre];
    }
  }

  $: selectedGenres, drawChart();
</script>

<style>
  .chart-card {
    background-color: #1e1e1e;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(255, 255, 255, 0.05);
    width: 100%;
    max-width: 1000px;
    margin: 3rem auto 2rem;
    position: relative;
  }

  .title {
    color: #facc15;
    font-weight: bold;
    font-size: 1.3rem;
    margin-bottom: 1rem;
    text-align: center;
  }

  .checkbox-list {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    margin-bottom: 1rem;
    max-height: 180px;
    overflow-y: auto;
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
  <div class="title">Genre Trends Over Time</div>
  <p style="color:white; font-weight: bold;">Select Genres:</p>
  <div class="checkbox-list">
    {#each allGenres as genre}
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
  <div bind:this={container} style="width: 100%; height: 100%; position: relative;"></div>
</div>
