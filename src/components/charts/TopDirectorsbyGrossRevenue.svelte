<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  export let imdbCSV = [];
  let container;
  let tooltip;

  // Helper to split director names into two lines
  function splitName(name) {
    const words = name.split(' ');
    const half = Math.ceil(words.length / 2);
    return [words.slice(0, half).join(' '), words.slice(half).join(' ')];
  }

  onMount(() => {
    if (imdbCSV.length) drawChart();
  });

  $: if (imdbCSV.length) drawChart();

  function drawChart() {
    if (!container) return;

    const margin = { top: 80, right: 30, bottom: 80, left: 100 };
    const width = 900;
    const height = 400;

    d3.select(container).selectAll('*').remove();

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
      .attr('width', '100%')
      .attr('height', height)
      .attr('viewBox', `0 0 ${width} ${height}`)
      .attr('preserveAspectRatio', 'xMidYMid meet')
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const selectedMetric = 'gross';

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

    // X Axis
    svg.append('g')
      .attr('transform', `translate(0, ${innerHeight})`)
      .call(d3.axisBottom(x))
      .selectAll('text')
      .style('fill', 'white');

    // Y Axis
    svg.append('g')
      .call(d3.axisLeft(y).ticks(5).tickFormat(d => `$${(d / 1e6).toFixed(0)}M`))
      .selectAll('text')
      .style('fill', 'white');

    // X axis label
    svg.append('text')
      .attr('x', innerWidth / 2)
      .attr('y', innerHeight + 50)
      .attr('text-anchor', 'middle')
      .text('Decade')
      .attr('fill', '#facc15')
      .style('font-size', '16px');

    // Y axis label
    svg.append('text')
      .attr('transform', `translate(-60, ${innerHeight / 2}) rotate(-90)`)
      .attr('text-anchor', 'middle')
      .text('Gross Revenue')
      .attr('fill', '#facc15')
      .style('font-size', '16px');

    // Bars
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
                 <strong>Gross Revenue:</strong> $${d3.format(',')(d.value)}`);
      })
      .on('mousemove', event => {
        tooltip
          .style('left', event.offsetX + 20 + 'px')
          .style('top', event.offsetY - 30 + 'px');
      })
      .on('mouseout', () => tooltip.style('display', 'none'));

    // Director names above bars (split into two lines)
    svg.selectAll('.director-label')
      .data(topDirectors)
      .join('text')
      .attr('class', 'director-label')
      .attr('x', d => x(`${d.decade}s`) + x.bandwidth() / 2)
      .attr('y', d => y(d.value) - 24)
      .attr('text-anchor', 'middle')
      .attr('fill', '#facc15')
      .style('font-size', '11px')
      .style('font-weight', 'bold')
      .style('pointer-events', 'none')
      .each(function(d) {
        const [line1, line2] = splitName(d.director);
        d3.select(this).html('');
        d3.select(this)
          .append('tspan')
          .attr('x', x(`${d.decade}s`) + x.bandwidth() / 2)
          .attr('dy', '0em')
          .text(line1);
        d3.select(this)
          .append('tspan')
          .attr('x', x(`${d.decade}s`) + x.bandwidth() / 2)
          .attr('dy', '1.2em')
          .text(line2);
      });

    // Chart title
    svg.append('text')
      .attr('x', innerWidth / 2)
      .attr('y', -40)
      .attr('text-anchor', 'middle')
      .text(`Top Director per Decade (Gross Revenue)`)
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
</style>

<div class="chart-card" bind:this={container}></div>
