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

    const margin = { top: 40, right: 40, bottom: 60, left: 160 };
    const width = 800;
    const height = 450;

    const svg = d3.select(container)
      .append('svg')
      .attr('width', '100%')
      .attr('height', '100%')
      .attr('viewBox', `0 0 ${width} ${height}`)
      .attr('preserveAspectRatio', 'xMidYMid meet')
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top - 70})`);

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

    // Reverse mapping: Group -> Genres
    const groupToGenres = {};
    Object.entries(genreGroupMap).forEach(([genre, group]) => {
      if (!groupToGenres[group]) groupToGenres[group] = [];
      groupToGenres[group].push(genre);
    });

    const x = d3.scaleBand()
      .domain(genres)
      .range([0, width - margin.left - margin.right])
      .padding(0.05);

    const y = d3.scaleBand()
      .domain(topStars)
      .range([0, height - margin.top - margin.bottom - 20])
      .padding(0.05);

    // --- Color Scale ---
    const counts = data.map(d => d.count).filter(c => c > 0);
    const minNonZero = d3.min(counts);
    const maxCount = d3.max(counts);

    const customInterpolator = t => {
      if (t < 0.5) return d3.interpolate("#fff7cc", "#facc15")(t * 2);
      return d3.interpolate("#facc15", "#fb923c")((t - 0.5) * 2);
    };

    const color = d3.scaleSequential()
      .domain([minNonZero, maxCount])
      .interpolator(customInterpolator);

    // --- X-axis ---
    const xAxisGroup = svg.append('g')
      .attr('class', 'x-axis')
      .attr('transform', `translate(0,${height - margin.top - margin.bottom - 20})`)
      .call(d3.axisBottom(x).tickSize(0));

    xAxisGroup.select(".domain").remove();
    xAxisGroup.selectAll("text")
      .style('font-size', '14px')
      .style('fill', 'white')
      .attr('transform', 'rotate(-30)')
      .attr('dx', '-0.6em')
      .attr('dy', '0.5em')
      .style('text-anchor', 'end')
      .on("mouseover", (event, genre) => {
        const group = genreGroupMap[genre] || genre;
        const allGenres = groupToGenres[group] || [genre];
        tooltip.style("opacity", 1)
          .html(`<strong>Group:</strong> ${group}<br><strong>Genres:</strong> ${allGenres.join(', ')}`);
      })
      .on("mousemove", event => {
        tooltip
          .style("left", event.pageX + 20 + "px")
          .style("top", event.pageY - 20 + "px");
      })
      .on("mouseout", () => tooltip.style("opacity", 0));

    // --- Y-axis ---
    const yAxisGroup = svg.append('g')
      .attr('class', 'y-axis')
      .call(d3.axisLeft(y).tickSize(0));

    yAxisGroup.select(".domain").remove();
    yAxisGroup.selectAll("text")
      .style('font-size', '14px')
      .style('fill', 'white');

    // --- Rectangles ---
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
        tooltip.style('opacity', 1)
          .html(`<strong>${d.star}</strong><br/>${d.genre}: ${d.count}`);
      })
      .on('mousemove', event => {
        tooltip
          .style('left', event.pageX + 20 + 'px')
          .style('top', event.pageY - 20 + 'px');
      })
      .on('mouseout', () => tooltip.style('opacity', 0));

    // --- Axis Labels ---
    svg.append('text')
      .attr('x', (width - margin.left - margin.right) / 2)
      .attr('y', height - margin.top + 50)
      .attr('text-anchor', 'middle')
      .style('fill', '#facc15')
      .style('font-size', '18px')
      .text('Genres');

    svg.append('text')
      .attr('transform', 'rotate(-90)')
      .attr('x', -(height - margin.top - margin.bottom) / 2)
      .attr('y', -margin.left + 20)
      .attr('text-anchor', 'middle')
      .style('fill', '#facc15')
      .style('font-size', '18px')
      .text('Stars');

    // --- Legend ---
    const legendWidth = 200;
    const legendHeight = 10;

    const legend = svg.append('g')
      .attr('transform', `translate(${width - margin.left - margin.right - legendWidth}, -30)`);

    const legendGradient = legend.append('defs')
      .append('linearGradient')
      .attr('id', 'legendGradient');

    legendGradient.append('stop').attr('offset', '0%').attr('stop-color', '#fff7cc');
    legendGradient.append('stop').attr('offset', '50%').attr('stop-color', '#facc15');
    legendGradient.append('stop').attr('offset', '100%').attr('stop-color', '#fb923c');

    legend.append('rect')
      .attr('width', legendWidth)
      .attr('height', legendHeight)
      .style('fill', 'url(#legendGradient)');

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

    legend.append('text')
      .attr('x', legendWidth / 2)
      .attr('y', -20)
      .attr('text-anchor', 'middle')
      .style('fill', 'white')
      .style('font-size', '14px')
      .text('Genre Presence');
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
