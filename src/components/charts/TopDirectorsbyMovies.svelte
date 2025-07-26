<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  export let imdbCSV = [];
  let container;
  let tooltip;
  let resizeObserver;

  function splitName(name) {
    const words = name.split(' ');
    const half = Math.ceil(words.length / 2);
    return [words.slice(0, half).join(' '), words.slice(half).join(' ')];
  }

  function drawChart(width, height) {
    const margin = { top: 60, right: 30, bottom: 60, left: 80 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    d3.select(container).selectAll('*').remove();

    tooltip = d3.select(container)
      .append('div')
      .style('position', 'absolute')
      .style('background', '#facc15')
      .style('color', '#000')
      .style('padding', '8px 10px')
      .style('border-radius', '8px')
      .style('font-size', '13px')
      .style('display', 'none')
      .style('pointer-events', 'none');

    const svg = d3.select(container)
      .append('svg')
      .attr('width', width)
      .attr('height', height)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    const parsed = imdbCSV
      .filter(d => d.Director && d.Released_Year && !isNaN(+d.Released_Year))
      .map(d => ({
        director: d.Director.trim(),
        decade: Math.floor(+d.Released_Year / 10) * 10,
        gross: d.Gross && d.Gross !== 'NA' ? +d.Gross.replace(/,/g, '') : 0
      }));

    const nested = d3.rollup(
      parsed,
      v => ({ movies: v.length, gross: d3.sum(v, d => d.gross) }),
      d => d.decade,
      d => d.director
    );

    let topDirectors = Array.from(nested, ([decade, directors]) => {
      const sorted = Array.from(directors, ([director, data]) => ({
        decade,
        director,
        value: data.movies
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
      .attr('transform', `translate(0,${innerHeight})`)
      .call(d3.axisBottom(x))
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

    svg.append('text')
      .attr('transform', `translate(-50,${innerHeight / 2}) rotate(-90)`)
      .attr('text-anchor', 'middle')
      .text('Total Movies')
      .attr('fill', '#facc15')
      .style('font-size', '14px');

    svg.append('text')
  .attr('x', innerWidth / 2)
  .attr('y', innerHeight + 55)  // position below the axis ticks
  .attr('text-anchor', 'middle')
  .text('Year')
  .attr('fill', '#facc15')
  .style('font-size', '14px');


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
        tooltip.style('display', 'block').html(
          `<strong>Director:</strong> ${d.director}<br/>
           <strong>Decade:</strong> ${d.decade}s<br/>
           <strong>Total Movies:</strong> ${d.value}`
        );
      })
      .on('mousemove', event => {
  tooltip
    .style('left', (event.pageX + 20) + 'px')
    .style('top', (event.pageY - 40) + 'px');
})

      .on('mouseout', () => tooltip.style('display', 'none'));

    svg.selectAll('.director-label')
      .data(topDirectors)
      .join('text')
      .attr('class', 'director-label')
      .attr('x', d => x(`${d.decade}s`) + x.bandwidth() / 2)
      .attr('y', d => y(d.value) - 20)
      .attr('text-anchor', 'middle')
      .attr('fill', '#facc15')
      .style('font-size', d => `${Math.min(12, x.bandwidth() / 4)}px`)
      .style('font-weight', 'bold')
      .style('pointer-events', 'none')
      .each(function (d) {
        const [line1, line2] = splitName(d.director);
        d3.select(this).text(null)
          .append('tspan').attr('x', x(`${d.decade}s`) + x.bandwidth() / 2).text(line1);
        if (line2) {
          d3.select(this)
            .append('tspan').attr('x', x(`${d.decade}s`) + x.bandwidth() / 2).attr('dy', '1.2em').text(line2);
        }
      });

    svg.append('text')
      .attr('x', innerWidth / 2)
      .attr('y', -40)
      .attr('text-anchor', 'middle')
      .text('Top Director by Total Movies')
      .attr('fill', '#facc15')
      .style('font-size', '20px')
      .style('font-weight', 'bold');
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
    background: #1e1e1e;
    padding: 1rem;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(255, 255, 255, 0.05);
    width: 100%;
    height: 100%;
  }
</style>

<div class="chart-card" bind:this={container}></div>
