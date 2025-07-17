<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  export let imdbCSV = [];
  let container;
  let tooltip;
  let selectedMetric = 'movies'; 

  const metrics = {
    movies: 'Total Movies',
    gross: 'Total Gross Revenue'
  };

  $: if (imdbCSV.length) drawChart();

  function drawChart() {
    const margin = { top: 60, right: 30, bottom: 60, left: 100 };
    const width = 900;
    const height = 450;

    d3.select(container).selectAll('*').remove();

    // Tooltip div
    tooltip = d3.select(container)
      .append('div')
      .style('position', 'absolute')
      .style('background', '#facc15')
      .style('color', '#000')
      .style('padding', '10px')
      .style('border-radius', '10px')
      .style('font-weight', 'bold')
      .style('font-size', '13px')
      .style('display', 'none')
      .style('pointer-events', 'none');

    const svg = d3.select(container)
      .append('svg')
      .attr('width', width)
      .attr('height', height)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const parsed = imdbCSV
      .filter(d =>
        d.Director &&
        d.Released_Year &&
        d.Gross &&
        d.Gross !== 'NA' &&
        !isNaN(+d.Released_Year)
      )
      .map(d => ({
        director: d.Director.trim(),
        decade: Math.floor(+d.Released_Year / 10) * 10,
        gross: +d.Gross.replace(/,/g, '')
      }));

    const nested = d3.rollup(
      parsed,
      v => ({
        movies: v.length,
        gross: d3.sum(v, d => d.gross)
      }),
      d => d.decade,
      d => d.director
    );

    let topDirectors = Array.from(nested, ([decade, directors]) => {
      const sorted = Array.from(directors, ([director, data]) => ({
        decade,
        director,
        value: data[selectedMetric]
      })).sort((a, b) => b.value - a.value);
      return sorted[0];
    }).filter(Boolean);

    topDirectors = topDirectors.sort((a, b) => a.decade - b.decade);

    const x = d3.scaleBand()
      .domain(topDirectors.map(d => `${d.decade}s`))
      .range([0, innerWidth])
      .padding(0.3);

    const y = d3.scaleLinear()
      .domain([0, d3.max(topDirectors, d => d.value) * 1.2])
      .range([innerHeight, 0]);

    svg.append('g')
      .attr('transform', `translate(0, ${innerHeight})`)
      .call(d3.axisBottom(x))
      .selectAll('text')
      .style('fill', 'white');

    svg.append('g')
      .call(d3.axisLeft(y).ticks(5))
      .selectAll('text')
      .style('fill', 'white');

    svg.selectAll('.bar')
      .data(topDirectors)
      .join('rect')
      .attr('class', 'bar')
      .attr('x', d => x(`${d.decade}s`))
      .attr('y', d => y(d.value))
      .attr('width', x.bandwidth())
      .attr('height', d => innerHeight - y(d.value))
      .attr('fill', '#facc15')
      .on('mouseover', (event, d) => {
        tooltip
          .style('display', 'block')
          .html(`<strong>Decade:</strong> ${d.decade}s<br>
                 <strong>Director:</strong> ${d.director}<br>
                 <strong>${metrics[selectedMetric]}:</strong> ${
                   selectedMetric === 'gross'
                     ? '$' + d3.format(',')(d.value)
                     : d.value
                 }`);
      })
      .on('mousemove', event => {
        tooltip
          .style('left', event.offsetX + 20 + 'px')
          .style('top', event.offsetY - 30 + 'px');
      })
      .on('mouseout', () => tooltip.style('display', 'none'));

    svg.append('text')
      .attr('x', innerWidth / 2)
      .attr('y', -20)
      .attr('text-anchor', 'middle')
      .text(`Top Director per Decade (${metrics[selectedMetric]})`)
      .attr('fill', '#facc15')
      .style('font-size', '18px')
      .style('font-weight', 'bold');
  }
</script>

<style>
  .chart-card {
    background: #1e1e1e;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(255, 255, 255, 0.05);
    margin: 2rem auto;
    max-width: 960px;
    position: relative;
  }
  .dropdown {
    margin: 1rem auto;
    text-align: center;
  }
  select {
    background: #facc15;
    border: none;
    padding: 6px 12px;
    border-radius: 6px;
    font-weight: bold;
    cursor: pointer;
  }
</style>

<div class="chart-card">
  <div class="dropdown">
    <label for="metric">Select: </label>
    <select id="metric" bind:value={selectedMetric} on:change={drawChart}>
      <option value="movies">Total Movies</option>
      <option value="gross">Gross Revenue</option>
    </select>
  </div>
  <div bind:this={container}></div>
</div>