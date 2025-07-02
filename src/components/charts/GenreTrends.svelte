<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  export let imdbCSV = [];
  let container;
  let tooltip;

  onMount(() => {
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
    const genres = Array.from(genresSet);

    genres.sort((a, b) => {
      const sumA = d3.sum(years.map(year => (dataByYear.get(year)?.[a] || 0)));
      const sumB = d3.sum(years.map(year => (dataByYear.get(year)?.[b] || 0)));
      return sumB - sumA;
    });

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
      .range([
        '#facc15', '#f59e0b', '#10b981', '#3b82f6', '#6366f1',
        '#ec4899', '#ef4444', '#14b8a6', '#eab308', '#c084fc',
        '#f472b6', '#22d3ee', '#a3e635', '#f97316', '#7c3aed'
      ]);

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
      .text('Movies Released per Genre (Stacked)')
      .attr('fill', '#facc15')
      .style('font-size', '16px');

    // Tooltip div
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

    // Legend
    const legend = svg.append('g')
      .attr('transform', `translate(${innerWidth + 20}, 0)`);

    genres.slice(0, 12).forEach((genre, i) => {
      legend.append('rect')
        .attr('x', 0)
        .attr('y', i * 20)
        .attr('width', 12)
        .attr('height', 12)
        .attr('fill', color(genre));

      legend.append('text')
        .attr('x', 18)
        .attr('y', i * 20 + 10)
        .text(genre)
        .attr('fill', 'white')
        .style('font-size', '12px');
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
</style>

<div class="chart-card">
  <div class="title">📊 Genre Trends Over Time</div>
  <div bind:this={container} style="width: 100%; height: 100%; position: relative;"></div>
</div>
