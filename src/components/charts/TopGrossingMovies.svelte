<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  export let imdbCSV = [];
  let container;
  let tooltip;

  onMount(() => {
    const margin = { top: 40, right: 30, bottom: 60, left: 260 };
    const width = 800;
    const height = 500;

    d3.select(container).selectAll('*').remove();

    const svg = d3.select(container)
      .append('svg')
      .attr('width', width)
      .attr('height', height)
      .attr('viewBox', `0 0 ${width} ${height}`)
      .attr('preserveAspectRatio', 'xMidYMid meet')
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    
    const filtered = imdbCSV
      .filter(d => d.Gross && d.Gross !== 'NA')
      .map(d => ({
        title: d.Series_Title,
        year: +d.Released_Year,
        gross: +d.Gross.replace(/,/g, '')
      }));

    const top10 = filtered.sort((a, b) => b.gross - a.gross).slice(0, 10).reverse(); // reverse for bottom-up bars

    const y = d3.scaleBand()
      .domain(top10.map(d => d.title))
      .range([innerHeight, 0])
      .padding(0.3);

    const x = d3.scaleLinear()
      .domain([0, d3.max(top10, d => d.gross)])
      .nice()
      .range([0, innerWidth]);

    svg.append('g')
      .call(d3.axisLeft(y))
      .selectAll('text')
      .style('fill', 'white')
      .style('font-size', '12px');

    svg.append('g')
      .attr('transform', `translate(0,${innerHeight})`)
      .call(d3.axisBottom(x).tickFormat(d => `$${d / 1e6}M`))
      .selectAll('text')
      .style('fill', 'white')
      .style('font-size', '12px');

    svg.selectAll('rect')
      .data(top10)
      .enter()
      .append('rect')
      .attr('y', d => y(d.title))
      .attr('x', 0)
      .attr('height', y.bandwidth())
      .attr('width', d => x(d.gross))
      .attr('fill', '#facc15')
      .on('mouseover', (event, d) => {
        tooltip
          .style('opacity', 1)
          .html(`<strong>${d.title}</strong><br/>Year: ${d.year}<br/>Gross: $${d3.format(',')(d.gross)}`);
      })
      .on('mousemove', event => {
        tooltip
          .style('left', event.offsetX + 20 + 'px')
          .style('top', event.offsetY - 20 + 'px');
      })
      .on('mouseout', () => {
        tooltip.style('opacity', 0);
      });

    svg.append('text')
      .attr('text-anchor', 'middle')
      .attr('x', innerWidth / 2)
      .attr('y', innerHeight + 50)
      .text('Gross Revenue')
      .attr('fill', '#facc15')
      .style('font-size', '16px');

    tooltip = d3.select(container)
      .append('div')
      .style('position', 'absolute')
      .style('background', '#facc15')
      .style('color', 'black')
      .style('padding', '5px 10px')
      .style('border-radius', '6px')
      .style('font-size', '13px')
      .style('pointer-events', 'none')
      .style('opacity', 0);
  });
</script>

<style>
  .chart-card {
    background-color: #1e1e1e;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(255, 255, 255, 0.05);
    max-width: 850px;
    margin: 2rem auto;
  }

  .title {
    color: #facc15;
    font-weight: bold;
    font-size: 1.3rem;
    text-align: center;
    margin-bottom: 1rem;
  }
</style>

<div class="chart-card">
  <div class="title">Top 10 Highest-Grossing Movies</div>
  <div bind:this={container} style="width: 100%; position: relative;"></div>
</div>
