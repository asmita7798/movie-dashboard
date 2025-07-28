<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  export let imdbCSV = [];
  let container;

  const genreGroupMap = {
    Action: 'Action/Adventure', Adventure: 'Action/Adventure',
    Comedy: 'Comedy',
    Drama: 'Drama', Biography: 'Drama', History: 'Drama',
    Romance: 'Romance', Musical: 'Romance',
    Crime: 'Crime/Thriller', Thriller: 'Crime/Thriller', Mystery: 'Crime/Thriller', 'Film-Noir': 'Crime/Thriller',
    Fantasy: 'Fantasy/Sci-Fi', 'Sci-Fi': 'Fantasy/Sci-Fi', Animation: 'Fantasy/Sci-Fi',
    Family: 'Family/Kids', Music: 'Family/Kids',
    Horror: 'Horror',
    War: 'War/Western', Western: 'War/Western',
    Sport: 'Sport'
  };

  onMount(() => {
    d3.select(container).selectAll('*').remove();

    const margin = { top: 40, right: 40, bottom: 30, left: 140 };
    const width = 800;
    const height = 450;

    const svg = d3.select(container)
      .append('svg')
      .attr('width', '100%')
      .attr('height', '100%')
      .attr('viewBox', `0 0 ${width} ${height}`)
      .attr('preserveAspectRatio', 'xMidYMid meet')
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top-70})`);

    // Tooltip now on body for better stacking
    const tooltip = d3.select('body')
      .append('div')
      .attr('class', 'tooltip')
      .style('position', 'absolute')
      .style('background', '#facc15')
      .style('color', 'black')
      .style('padding', '6px 10px')
      .style('border-radius', '6px')
      .style('font-size', '12px')
      .style('pointer-events', 'none')
      .style('opacity', 0);

    // --- Data Prep ---
    const starGenreMap = new Map();
    imdbCSV.forEach(d => {
      if (d.Star1 && d.Genre) {
        const star = d.Star1.trim();
        d.Genre.split(',').forEach(g => {
          const genreGroup = genreGroupMap[g.trim()] || g.trim();
          const key = `${star}-${genreGroup}`;
          starGenreMap.set(key, (starGenreMap.get(key) || 0) + 1);
        });
      }
    });

    const starCounts = {};
    imdbCSV.forEach(d => {
      if (d.Star1) {
        const star = d.Star1.trim();
        starCounts[star] = (starCounts[star] || 0) + 1;
      }
    });

    const topStars = Object.entries(starCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(d => d[0]);

    const genres = Array.from(new Set(
      imdbCSV.flatMap(d => d.Genre
        ? d.Genre.split(',').map(g => genreGroupMap[g.trim()] || g.trim())
        : [])
    )).sort();

    const data = [];
    topStars.forEach(star => {
      genres.forEach(genre => {
        const key = `${star}-${genre}`;
        data.push({ star, genre, count: starGenreMap.get(key) || 0 });
      });
    });

    const x = d3.scaleBand()
      .domain(genres)
      .range([0, width - margin.left - margin.right])
      .padding(0.05);

    const y = d3.scaleBand()
      .domain(topStars)
      .range([0, height - margin.top - margin.bottom - 20]) // move chart up
      .padding(0.05);

    const color = d3.scaleSequential()
      .interpolator(d3.interpolateYlOrBr)
      .domain([0, d3.max(data, d => d.count)]);

    svg.append('g')
      .attr('transform', `translate(0,${height - margin.top - margin.bottom - 20})`)
      .call(d3.axisBottom(x))
      .selectAll('text')
      .attr('transform', 'rotate(-30)')
      .style('text-anchor', 'end')
      .style('font-size', '14px')
      .style('fill', 'white');

    svg.append('g')
      .call(d3.axisLeft(y))
      .selectAll('text')
      .attr('transform', 'rotate(-30)')
      .style('font-size', '14px')
      .style('fill', 'white');

    svg.selectAll('rect')
      .data(data)
      .enter()
      .append('rect')
      .attr('x', d => x(d.genre))
      .attr('y', d => y(d.star))
      .attr('width', x.bandwidth())
      .attr('height', y.bandwidth())
      .style('fill', d => d.count === 0 ? '#333' : color(d.count))
      .on('mouseover', (event, d) => {
        tooltip
          .style('opacity', 1)
          .html(`<strong>${d.star}</strong><br/>${d.genre}: ${d.count}`);
      })
      .on('mousemove', event => {
        tooltip
          .style('left', event.pageX + 20 + 'px')
          .style('top', event.pageY - 20 + 'px');
      })
      .on('mouseout', () => tooltip.style('opacity', 0));

    // X-axis label
svg.append('text')
  .attr('x', (width - margin.left - margin.right) / 2)
  .attr('y', height - margin.top + 40)
  .attr('text-anchor', 'middle')
  .style('fill', '#facc15')
  .style('font-size', '18px')
  .text('Genres');

// Y-axis label
svg.append('text')
  .attr('transform', 'rotate(-90)')
  .attr('x', -(height - margin.top - margin.bottom) / 2)
  .attr('y', -margin.left + 13)
  .attr('text-anchor', 'middle')
  .style('fill', '#facc15')
  .style('font-size', '18px')
  .text('Stars');


    // Legend moved up
    const legendWidth = 200;
    const legendHeight = 10;
    const legendData = d3.range(0, 1.01, 0.01);

    const legend = svg.append('g')
  .attr('transform', `translate(${width - margin.left - margin.right - legendWidth}, -30)`);


    legend.selectAll('rect')
      .data(legendData)
      .enter().append('rect')
      .attr('x', (d, i) => i * (legendWidth / legendData.length))
      .attr('y', 0)
      .attr('width', legendWidth / legendData.length)
      .attr('height', legendHeight)
      .attr('fill', d => color(d * d3.max(data, e => e.count)));

    legend.append('text')
      .attr('x', 0)
      .attr('y', -5)
      .style('fill', 'white')
      .style('font-size', '14px')
      .text('Low');

    legend.append('text')
      .attr('x', legendWidth)
      .attr('y', -5)
      .style('fill', 'white')
      .style('font-size', '14px')
      .attr('text-anchor', 'end')
      .text('High');
  });
</script>

<style>
  .chart-card {
    background-color: #1e1e1e;
    padding: 1rem;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(255, 255, 255, 0.05);
    width: 100%;
    height: 450px;
    max-width: 950px;
    margin: auto;
    text-align: center;
  }
</style>

<div class="chart-card">
  <div style="color:#facc15;font-weight:bold;font-size:1.3rem;margin-bottom:1rem;">
    Stars Across Genres
  </div>
  <div bind:this={container} style="width: 100%; height: 450px; position: relative;"></div>
</div>
