<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  export let imdbCSV = [];
  let container;
  let tooltip;

  onMount(() => {
    const margin = { top: 40, right: 40, bottom: 50, left: 60 };
    const width = 800;
    const height = 450;

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

    // --- Aggregate IMDb & Metascore by year ---
    const dataMap = new Map();
    imdbCSV.forEach(d => {
      const year = +d.Released_Year;
      if (!year || isNaN(year)) return;

      const imdb = +d.IMDB_Rating;
      const meta = +d.Meta_score;

      if (!dataMap.has(year)) {
        dataMap.set(year, { year, imdbSum: 0, metaSum: 0, count: 0 });
      }
      const entry = dataMap.get(year);
      entry.imdbSum += isNaN(imdb) ? 0 : imdb;
      entry.metaSum += isNaN(meta) ? 0 : meta;
      entry.count++;
    });

    const data = Array.from(dataMap.values())
      .map(d => ({
        year: d.year,
        imdb: d.count ? d.imdbSum / d.count : null,
        meta: d.count ? d.metaSum / d.count : null
      }))
      .filter(d => d.imdb && d.meta)
      .sort((a, b) => a.year - b.year);

    const x = d3.scaleLinear()
      .domain(d3.extent(data, d => d.year))
      .range([0, innerWidth]);

    const minScore = d3.min(data, d => Math.min(d.imdb, d.meta / 10));
    const maxScore = d3.max(data, d => Math.max(d.imdb, d.meta / 10));

    const y = d3.scaleLinear()
    .domain([Math.floor(minScore), Math.ceil(maxScore)])
    .range([innerHeight, 0]);


    svg.append('g')
      .attr('transform', `translate(0,${innerHeight})`)
      .call(d3.axisBottom(x).tickFormat(d3.format('d')))
      .selectAll('text')
      .style('fill', 'white')
      .style('font-size', '14px');

    svg.append('g')
      .call(d3.axisLeft(y))
      .selectAll('text')
      .style('fill', 'white')
      .style('font-size', '14px');

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
      .text('Rating (0–10)')
      .attr('fill', '#facc15')
      .style('font-size', '16px');

    // --- Line generators ---
    const lineImdb = d3.line()
      .x(d => x(d.year))
      .y(d => y(d.imdb))
      .curve(d3.curveMonotoneX);

    const lineMeta = d3.line()
      .x(d => x(d.year))
      .y(d => y(d.meta / 10)) // convert metascore to 0-10
      .curve(d3.curveMonotoneX);

    svg.append('path')
      .datum(data)
      .attr('fill', 'none')
      .attr('stroke', '#facc15')
      .attr('stroke-width', 2)
      .attr('d', lineImdb);

    svg.append('path')
      .datum(data)
      .attr('fill', 'none')
      .attr('stroke', '#fb923c') // Teal
      .attr('stroke-width', 2)
      .attr('d', lineMeta);

    // --- Tooltip and vertical line ---
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

    const hoverLine = svg.append('line')
      .attr('stroke', 'white')
      .attr('stroke-width', 1)
      .attr('y1', 0)
      .attr('y2', innerHeight)
      .style('opacity', 0);

    svg.append('rect')
      .attr('width', innerWidth)
      .attr('height', innerHeight)
      .style('fill', 'none')
      .style('pointer-events', 'all')
      .on('mousemove', (event) => {
        const [mx] = d3.pointer(event);
        const year = Math.round(x.invert(mx));

        const closest = data.reduce((a, b) =>
          Math.abs(b.year - year) < Math.abs(a.year - year) ? b : a
        );

        hoverLine
          .attr('x1', x(closest.year))
          .attr('x2', x(closest.year))
          .style('opacity', 1);

        tooltip
          .style('opacity', 1)
          .html(
            `<strong>Year:</strong> ${closest.year}<br/>
             <strong>IMDb:</strong> ${closest.imdb.toFixed(2)}<br/>
             <strong>Metascore:</strong> ${closest.meta.toFixed(0)}`
          )
          .style('left', event.offsetX + 15 + 'px')
          .style('top', event.offsetY - 28 + 'px');
      })
      .on('mouseout', () => {
        hoverLine.style('opacity', 0);
        tooltip.style('opacity', 0);
      });

    // --- Legend ---
    const legend = svg.append('g').attr('transform', `translate(${innerWidth - 120}, 10)`);
    legend.append('circle').attr('cx', 0).attr('cy', 0).attr('r', 6).attr('fill', '#facc15');
    legend.append('text').attr('x', 12).attr('y', 5).attr('fill', 'white').text('IMDb Rating');
    legend.append('circle').attr('cx', 0).attr('cy', 24).attr('r', 6).attr('fill', '#fb923c');
    legend.append('text').attr('x', 12).attr('y', 29).attr('fill', 'white').text('Metascore');
  });
</script>

<style>
  .chart-card {
    background-color: #1e1e1e;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(255, 255, 255, 0.05);
    width: 100%;
    max-width: 800px;
    margin: auto;
  }
</style>

<div class="chart-card">
  <div class="title" style="color:#facc15;font-weight:bold;font-size:1.3rem;margin-bottom:1rem;text-align:center;">
    IMDb vs Metascore Trends
  </div>
  <div bind:this={container} style="width: 100%; position: relative;"></div>
</div>
