<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  export let imdbCSV = [];
  let container;
  let tooltip;
  let resizeObserver;

  function drawChart(width, height) {
    const margin = { top: 40, right: 40, bottom: 70, left: 60 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    d3.select(container).selectAll('*').remove();

    const svg = d3.select(container)
      .append('svg')
      .attr('width', width)
      .attr('height', height)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Aggregate IMDb & Metascore per year
    const dataMap = new Map();
    imdbCSV.forEach(d => {
      const year = +d.Released_Year;
      if (!year) return;
      const imdb = +d.IMDB_Rating;
      const meta = +d.Meta_score;
      if (!dataMap.has(year)) dataMap.set(year, { year, imdbSum: 0, metaSum: 0, count: 0 });
      const entry = dataMap.get(year);
      entry.imdbSum += isNaN(imdb) ? 0 : imdb;
      entry.metaSum += isNaN(meta) ? 0 : meta;
      entry.count++;
    });

    const data = Array.from(dataMap.values())
      .map(d => ({ year: d.year, imdb: d.imdbSum / d.count, meta: d.metaSum / d.count }))
      .filter(d => d.imdb && d.meta)
      .sort((a, b) => a.year - b.year);

    const x = d3.scaleLinear().domain(d3.extent(data, d => d.year)).range([0, innerWidth]);
    const y = d3.scaleLinear()
      .domain([
        Math.floor(d3.min(data, d => Math.min(d.imdb, d.meta / 10))),
        Math.ceil(d3.max(data, d => Math.max(d.imdb, d.meta / 10)))
      ])
      .range([innerHeight, 0]);

    // Axes
    svg.append('g')
      .attr('transform', `translate(0,${innerHeight})`)
      .call(d3.axisBottom(x).tickFormat(d3.format('d')))
      .selectAll('text')
      .style('fill', 'white')
      .attr('transform', 'rotate(-30)')
      .style('text-anchor', 'end')
      .style('font-size', '12px');

    svg.append('g')
      .call(d3.axisLeft(y))
      .selectAll('text')
      .style('fill', 'white')
      .style('font-size', '12px');

    // Labels
    svg.append('text')
      .attr('x', innerWidth / 2)
      .attr('y', innerHeight + 50)
      .attr('text-anchor', 'middle')
      .style('fill', '#facc15')
      .style('font-size', '14px')
      .text('Year');

    svg.append('text')
      .attr('transform', `translate(-40, ${innerHeight / 2}) rotate(-90)`)
      .attr('text-anchor', 'middle')
      .style('fill', '#facc15')
      .style('font-size', '14px')
      .text('Rating (0–10)');

    // Lines
    const lineImdb = d3.line().x(d => x(d.year)).y(d => y(d.imdb)).curve(d3.curveMonotoneX);
    const lineMeta = d3.line().x(d => x(d.year)).y(d => y(d.meta / 10)).curve(d3.curveMonotoneX);

    svg.append('path').datum(data).attr('fill', 'none').attr('stroke', '#facc15').attr('stroke-width', 2).attr('d', lineImdb);
    svg.append('path').datum(data).attr('fill', 'none').attr('stroke', '#fb923c').attr('stroke-width', 2).attr('d', lineMeta);

    // Tooltip
    tooltip = d3.select(container).append('div')
      .style('position', 'absolute').style('background', '#facc15').style('color', 'black')
      .style('padding', '5px 8px').style('border-radius', '6px')
      .style('font-size', '12px').style('pointer-events', 'none').style('opacity', 0);

    const hoverLine = svg.append('line').attr('stroke', 'white').attr('stroke-width', 1).attr('y1', 0).attr('y2', innerHeight).style('opacity', 0);

    svg.append('rect')
      .attr('width', innerWidth)
      .attr('height', innerHeight)
      .style('fill', 'none')
      .style('pointer-events', 'all')
      .on('mousemove', (event) => {
        const [mx] = d3.pointer(event);
        const year = Math.round(x.invert(mx));
        const closest = data.reduce((a, b) => Math.abs(b.year - year) < Math.abs(a.year - year) ? b : a);
        hoverLine.attr('x1', x(closest.year)).attr('x2', x(closest.year)).style('opacity', 1);
        tooltip.style('opacity', 1)
          .html(`<strong>${closest.year}</strong> <br/>IMDb: ${closest.imdb.toFixed(2)}<br/>Metascore: ${closest.meta.toFixed(0)}`)
          .style('left', event.offsetX + 15 + 'px').style('top', event.offsetY - 28 + 'px');
      })
      .on('mouseout', () => { hoverLine.style('opacity', 0); tooltip.style('opacity', 0); });

    // Legend
    const legend = svg.append('g').attr('transform', `translate(${innerWidth - 120}, -10)`);
    legend.append('circle').attr('cx', 6).attr('cy', 0).attr('r', 4).attr('fill', '#facc15');
    legend.append('text').attr('x', 18).attr('y', 5).attr('fill', 'white').style('font-size', '12px').text('IMDb Rating');
    legend.append('circle').attr('cx', 6).attr('cy', 14).attr('r', 4).attr('fill', '#fb923c');
    legend.append('text').attr('x', 18).attr('y', 19).attr('fill', 'white').style('font-size', '12px').text('Metascore');
  }

  onMount(() => {
    resizeObserver = new ResizeObserver(entries => {
      for (const entry of entries) {
        drawChart(entry.contentRect.width, entry.contentRect.height);
      }
    });
    resizeObserver.observe(container);
  });
</script>

<style>
  .chart-card {
    background-color: #1e1e1e;
    padding: 1rem;
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
  <div class="title">IMDb vs Metascore Trends</div>
  <div bind:this={container} style="width: 100%; height: calc(100% - 2rem); position: relative;"></div>
</div>
