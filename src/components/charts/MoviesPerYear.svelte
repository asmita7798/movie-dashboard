<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  export let imdbCSV = [];
  let container;
  let tooltip;

  onMount(() => {
    const margin = { top: 40, right: 30, bottom: 50, left: 60 };
    const width = 500;
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

    const moviesPerYear = d3.rollups(
      imdbCSV.filter(d => d.Released_Year),
      v => v.length,
      d => +d.Released_Year
    ).sort((a, b) => a[0] - b[0]);

    const years = moviesPerYear.map(d => d[0]);
    const counts = moviesPerYear.map(d => d[1]);

    const x = d3.scaleLinear().domain(d3.extent(years)).range([0, innerWidth]);
    const y = d3.scaleLinear().domain([0, d3.max(counts) + 5]).range([innerHeight, 0]);

    svg.append('g')
      .attr('transform', `translate(0,${innerHeight})`)
      .call(d3.axisBottom(x).tickFormat(d3.format("d")).tickSize(0))
      .selectAll('text')
      .style('fill', 'white')
      .style('font-size', '14px')
      .attr('dy', '1em')
      .attr('dx', '0.5em');

    svg.append('g')
      .call(d3.axisLeft(y).tickSize(0))
      .selectAll('text')
      .style('fill', 'white')
      .style('font-size', '14px')
      .attr('dx', '-0.5em')
      .attr('dy', '0.25em');

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
      .text('Number of Movies')
      .attr('fill', '#facc15')
      .style('font-size', '16px');

    const line = d3.line()
      .x(d => x(d[0]))
      .y(d => y(d[1]))
      .curve(d3.curveMonotoneX);

    svg.append('path')
      .datum(moviesPerYear)
      .attr('fill', 'none')
      .attr('stroke', '#facc15')
      .attr('stroke-width', 2)
      .attr('d', line);

    // Tooltip styling
    tooltip = d3.select(container)
      .append('div')
      .style('position', 'absolute')
      .style('background', '#facc15')
      .style('color', 'black')
      .style('padding', '5px 8px')
      .style('border-radius', '6px')
      .style('font-size', '12px')
      .style('pointer-events', 'none')
      .style('opacity', 0);

    svg.selectAll('circle')
      .data(moviesPerYear)
      .enter()
      .append('circle')
      .attr('cx', d => x(d[0]))
      .attr('cy', d => y(d[1]))
      .attr('r', 3)
      .attr('fill', '#facc15')
      .on('mouseover', (event, d) => {
        tooltip
          .style('opacity', 1)
          .html(`<strong>Year:</strong> ${d[0]}<br/><strong>Total Movies:</strong> ${d[1]}`);
      })
      .on('mousemove', event => {
        tooltip
          .style('left', event.offsetX + 15 + 'px')
          .style('top', event.offsetY - 28 + 'px');
      })
      .on('mouseout', () => {
        tooltip.style('opacity', 0);
      });
  });
</script>

<style>
  .chart-card {
    background-color: #1e1e1e;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(255, 255, 255, 0.05);
    width: 100%;
    height: 450px;
    max-width: 500px;
    flex: 1 1 400px;
    margin: auto;
  }

  .title {
    color: #facc15;
    font-weight: bold;
    font-size: 1.3rem;
    margin-bottom: 1rem;
    text-align: center;
  }
</style>

<div class="chart-card">
  <div class="title">🎥 Films Released Each Year</div>
  <div bind:this={container} style="width: 100%; position: relative;"></div>
</div>
