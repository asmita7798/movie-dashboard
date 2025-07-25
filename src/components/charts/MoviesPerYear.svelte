<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  export let imdbCSV = [];
  let container;
  let tooltip;
  let resizeObserver;

  function movingAverage(data, windowSize = 5) {
    return data.map((d, i, arr) => {
      const start = Math.max(0, i - Math.floor(windowSize / 2));
      const end = Math.min(arr.length, i + Math.ceil(windowSize / 2));
      const slice = arr.slice(start, end);
      const avg = d3.mean(slice, x => x[1]);
      return [d[0], avg];
    });
  }

  function drawChart(width, height) {
    const margin = { top: 40, right: 30, bottom: 50, left: 60 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    d3.select(container).selectAll('*').remove();

    const svg = d3
      .select(container)
      .append('svg')
      .attr('width', width)
      .attr('height', height)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    const rawCounts = d3.rollups(
      imdbCSV.filter(d => d.Released_Year),
      v => v.length,
      d => +d.Released_Year
    );

    const yearMap = new Map(rawCounts);
    const allYears = d3.range(1920, 2021);
    const filledData = allYears.map(year => [year, yearMap.get(year) || 0]);
    const smoothedData = movingAverage(filledData, 5);

    const x = d3.scaleLinear().domain(d3.extent(allYears)).range([0, innerWidth]);
    const y = d3.scaleLinear().domain([0, d3.max(filledData, d => d[1]) + 5]).range([innerHeight, 0]);

    svg.append('g')
      .attr('transform', `translate(0,${innerHeight})`)
      .call(d3.axisBottom(x).tickFormat(d3.format("d")))
      .selectAll('text').style('fill', 'white').style('font-size', '12px').attr('transform', 'rotate(45)')
      .style('text-anchor', 'start');

    svg.append('g')
      .call(d3.axisLeft(y))
      .selectAll('text').style('fill', 'white').style('font-size', '12px');

    svg.append('text')
      .attr('text-anchor', 'middle')
      .attr('x', innerWidth / 2)
      .attr('y', innerHeight + 50)
      .text('Year')
      .attr('fill', '#facc15');

    svg.append('text')
      .attr('text-anchor', 'middle')
      .attr('transform', `translate(-40, ${innerHeight / 2}) rotate(-90)`)
      .text('Count of Movies')
      .attr('fill', '#facc15');

    const gradient = svg.append("defs").append("linearGradient")
      .attr("id", "area-gradient")
      .attr("x1", "0%").attr("y1", "0%")
      .attr("x2", "0%").attr("y2", "100%");
    gradient.append("stop").attr("offset", "0%").attr("stop-color", "#facc15").attr("stop-opacity", 0.7);
    gradient.append("stop").attr("offset", "100%").attr("stop-color", "#facc15").attr("stop-opacity", 0.15);

    const area = d3.area()
      .x(d => x(d[0])).y0(innerHeight).y1(d => y(d[1]))
      .curve(d3.curveCatmullRom);
    const line = d3.line()
      .x(d => x(d[0])).y(d => y(d[1]))
      .curve(d3.curveCatmullRom);

    svg.append('path').datum(smoothedData).attr('fill', 'url(#area-gradient)').attr('d', area);
    svg.append('path').datum(smoothedData).attr('fill', 'none').attr('stroke', '#facc15').attr('stroke-width', 2).attr('d', line);

    tooltip = d3.select(container).append('div')
      .style('position', 'absolute').style('background', '#facc15')
      .style('color', 'black').style('padding', '5px 8px').style('border-radius', '6px')
      .style('font-size', '12px').style('pointer-events', 'none').style('opacity', 0);

    svg.selectAll('circle').data(filledData).enter().append('circle')
      .attr('cx', d => x(d[0])).attr('cy', d => y(d[1]))
      .attr('r', 2).attr('fill', '#facc15').attr('fill-opacity', 0.5)
      .on('mouseover', (event, d) => {
        tooltip.style('opacity', 1)
          .html(`<strong>Year:</strong> ${d[0]}<br/><strong>Total Movies:</strong> ${d[1]}`);
      })
      .on('mousemove', event => {
        tooltip.style('left', event.offsetX + 15 + 'px').style('top', event.offsetY - 28 + 'px');
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
    margin-bottom: 1rem;
    text-align: center;
  }
</style>

<div class="chart-card">
  <div class="title">IMDb Top 1000 Release Trends</div>
  <div bind:this={container} style="width: 100%; height: calc(100% - 2rem); position: relative;"></div>
</div>
