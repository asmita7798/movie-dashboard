<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  export let imdbCSV = [];
  let container;
  let tooltip;
  let resizeObserver;

  function drawChart(width, height) {
    const margin = { top: 40, right: 30, bottom: 70, left: 80 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    d3.select(container).selectAll('*').remove();

    const svg = d3.select(container)
      .append('svg')
      .attr('width', width)
      .attr('height', height)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // --- Prepare decade-based data ---
    const parsed = imdbCSV
      .filter(d => {
        const year = +d.Released_Year;
        const gross = d.Gross && d.Gross !== 'NA' ? +d.Gross.replace(/,/g, '') : NaN;
        return !isNaN(year) && !isNaN(gross);
      })
      .map(d => {
        const year = +d.Released_Year;
        // Group all 2010–2020 movies into 2010 decade
        const decade = year >= 2020 ? 2010 : Math.floor(year / 10) * 10;
        return { decade, gross: +d.Gross.replace(/,/g, '') };
      });

    const revenueByDecade = Array.from(
      d3.rollups(parsed, v => d3.mean(v, d => d.gross), d => d.decade),
      ([decade, avg]) => ({ decade, avg })
    ).sort((a, b) => a.decade - b.decade);

    // --- Force domain cleanup (no 2020s tick) ---
    const filteredData = revenueByDecade.filter(d => d.decade <= 2010);
    const xDomain = Array.from(new Set(filteredData.map(d => `${d.decade}s`)));
    console.log("Final X Domain (no 2020s):", xDomain);

    // --- Scales ---
    const x = d3.scaleBand()
      .domain(xDomain)
      .range([0, innerWidth])
      .padding(0.4);

    const y = d3.scaleLinear()
      .domain([0, d3.max(filteredData, d => d.avg) * 1.1])
      .range([innerHeight, 0]);

    // --- Axes ---
    svg.append('g')
      .attr('transform', `translate(0,${innerHeight})`)
      .call(d3.axisBottom(x))
      .selectAll('text')
      .style('fill', 'white')
      .style('font-size', '13px')
      .attr('transform', 'rotate(-30)')
      .style('text-anchor', 'end');

    svg.append('g')
      .call(d3.axisLeft(y).tickFormat(d => `$${(d / 1e6).toFixed(0)}M`))
      .selectAll('text')
      .style('fill', 'white')
      .style('font-size', '13px');

    // Axis labels
    svg.append('text')
      .attr('text-anchor', 'middle')
      .attr('x', innerWidth / 2)
      .attr('y', innerHeight + 60)
      .text('Decade')
      .attr('fill', '#facc15')
      .style('font-size', '16px');

    svg.append('text')
      .attr('text-anchor', 'middle')
      .attr('transform', `translate(-60, ${innerHeight / 2}) rotate(-90)`)
      .text('Avg Gross Revenue')
      .attr('fill', '#facc15')
      .style('font-size', '16px');

    // Tooltip
    tooltip = d3.select(container)
      .append('div')
      .style('position', 'absolute')
      .style('background', '#facc15')
      .style('color', 'black')
      .style('padding', '6px 10px')
      .style('border-radius', '6px')
      .style('font-size', '12px')
      .style('pointer-events', 'none')
      .style('opacity', 0);

    // --- Lollipop chart (only filtered data) ---
    svg.selectAll('line.stem')
      .data(filteredData)
      .enter()
      .append('line')
      .attr('class', 'stem')
      .attr('x1', d => x(`${d.decade}s`) + x.bandwidth() / 2)
      .attr('x2', d => x(`${d.decade}s`) + x.bandwidth() / 2)
      .attr('y1', y(0))
      .attr('y2', d => y(d.avg))
      .attr('stroke', '#facc15')
      .attr('stroke-width', 2);

    svg.selectAll('circle.dot')
      .data(filteredData)
      .enter()
      .append('circle')
      .attr('class', 'dot')
      .attr('cx', d => x(`${d.decade}s`) + x.bandwidth() / 2)
      .attr('cy', d => y(d.avg))
      .attr('r', 6)
      .attr('fill', '#facc15')
      .on('mouseover', (event, d) => {
        tooltip
          .style('opacity', 1)
          .html(`<strong>${d.decade}s</strong><br/>Avg Gross: $${d3.format(',')(Math.round(d.avg))}`);
      })
      .on('mousemove', event => {
        tooltip
          .style('left', event.offsetX + 15 + 'px')
          .style('top', event.offsetY - 28 + 'px');
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
    font-size: 1.4rem;
    text-align: center;
    margin-bottom: 1rem;
  }
</style>

<div class="chart-card">
  <div class="title">Avg Gross Revenue by Decade</div>
  <div bind:this={container} style="width: 100%; height: calc(100% - 2rem); position: relative;"></div>
</div>
