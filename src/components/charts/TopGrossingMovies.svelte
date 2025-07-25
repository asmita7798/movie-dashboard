<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  export let imdbCSV = [];
  let container;
  let tooltip;
  let resizeObserver;

  function drawChart(width, height) {
    const margin = { top: 20, right: 30, bottom: 60, left: 50 }; // moved chart up, extra bottom for labels
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    d3.select(container).selectAll('*').remove();

    const svg = d3.select(container)
      .append('svg')
      .attr('width', width)
      .attr('height', height)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    const filtered = imdbCSV
      .filter(d => d.Gross && d.Gross !== 'NA')
      .map(d => ({
        title: d.Series_Title,
        year: +d.Released_Year,
        gross: +d.Gross.replace(/,/g, '')
      }));

    // Sort highest grossing on top
    const top10 = filtered.sort((a, b) => b.gross - a.gross).slice(0, 10);

    const y = d3.scaleBand()
      .domain(top10.map(d => d.title))
      .range([0, innerHeight])
      .padding(0.3);

    const x = d3.scaleLinear()
      .domain([0, d3.max(top10, d => d.gross)])
      .nice()
      .range([0, innerWidth]);

    // Bars
    const bars = svg.selectAll('rect')
      .data(top10)
      .enter()
      .append('rect')
      .attr('y', d => y(d.title))
      .attr('height', y.bandwidth())
      .attr('x', 0)
      .attr('width', d => x(d.gross))
      .attr('fill', '#facc15');

    // Labels inside bars
    svg.selectAll('.bar-label')
      .data(top10)
      .enter()
      .append('text')
      .attr('class', 'bar-label')
      .attr('x', d => x(d.gross) - 5)
      .attr('y', d => y(d.title) + y.bandwidth() / 2)
      .attr('dy', '0.35em')
      .attr('text-anchor', 'end')
      .text(d => d.title)
      .style('fill', 'black')
      .style('font-size', d => {
        const barWidth = x(d.gross);
        return barWidth > 150 ? '11px' : barWidth > 100 ? '10px' : '8px';
      })
      .style('font-weight', '600');

    // X-axis with rotated labels
    svg.append('g')
      .attr('transform', `translate(0,${innerHeight})`)
      .call(d3.axisBottom(x).tickFormat(d => `$${d / 1e6}M`))
      .selectAll('text')
      .style('fill', 'white')
      .style('font-size', '12px')
      .attr('transform', 'rotate(45)')
      .attr('text-anchor', 'start')
      .attr('dx', '0.5em')
      .attr('dy', '0.5em');

    // X-axis label
    svg.append('text')
      .attr('text-anchor', 'middle')
      .attr('x', innerWidth / 2)
      .attr('y', innerHeight + 60)
      .text('Gross Revenue')
      .attr('fill', '#facc15')
      .style('font-size', '16px');

    // Tooltip
    tooltip = d3.select(container)
      .append('div')
      .style('position', 'absolute')
      .style('background', '#facc15')
      .style('color', 'black')
      .style('padding', '5px 10px')
      .style('border-radius', '6px')
      .style('font-size', '12px')
      .style('pointer-events', 'none')
      .style('opacity', 0);

    bars.on('mouseover', (event, d) => {
        tooltip
          .style('opacity', 1)
          .html(`<strong>${d.title}</strong><br/>Year: ${d.year}<br/>Gross: $${d3.format(',')(d.gross)}`);
      })
      .on('mousemove', event => {
        tooltip
          .style('left', event.offsetX + 20 + 'px')
          .style('top', event.offsetY - 20 + 'px');
      })
      .on('mouseout', () => tooltip.style('opacity', 0));
  }

  onMount(() => {
    resizeObserver = new ResizeObserver(entries => {
      for (const entry of entries) {
        const { width, height } = entry.contentRect;
        drawChart(width, height);
      }
    });
    resizeObserver.observe(container);
  });
</script>

<style>
  .chart-card {
    background-color: #1e1e1e;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(255, 255, 255, 0.05);
    width: 100%;
    height: 100%;
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
  <div bind:this={container} style="width: 100%; height: calc(100% - 2rem); position: relative;"></div>
</div>
