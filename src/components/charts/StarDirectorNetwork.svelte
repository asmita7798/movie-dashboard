<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  export let imdbCSV = [];
  let container;
  let tooltip;
  let zoomBehavior;
  let svgRoot;

  onMount(() => {
    if (imdbCSV.length) drawNetwork();
  });

  function resetZoom() {
    svgRoot.transition().duration(750).call(zoomBehavior.transform, d3.zoomIdentity);
  }

  function drawNetwork() {
    const width = container.clientWidth;
    const height = container.clientHeight;

    d3.select(container).selectAll('*').remove();

    svgRoot = d3.select(container)
      .append('svg')
      .attr('width', '100%')
      .attr('height', '100%')
      .attr('viewBox', `0 0 ${width} ${height}`)
      .attr('preserveAspectRatio', 'xMidYMid meet');

    const svg = svgRoot.append('g');

    zoomBehavior = d3.zoom()
      .scaleExtent([0.2, 5])
      .translateExtent([[0, 0], [width, height]])
      .on('zoom', (event) => {
        svg.attr('transform', event.transform);
      });

    svgRoot.call(zoomBehavior);

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

    const nodeMap = new Map();
    const linkMap = new Map();

    imdbCSV.forEach(d => {
      const director = d.Director?.trim();
      const stars = [d.Star1, d.Star2, d.Star3, d.Star4].filter(Boolean).map(s => s.trim());
      if (!director) return;

      if (!nodeMap.has(director)) nodeMap.set(director, { id: director, type: 'director' });

      stars.forEach(star => {
        if (!nodeMap.has(star)) nodeMap.set(star, { id: star, type: 'star' });
        const key = `${director}::${star}`;
        linkMap.set(key, (linkMap.get(key) || 0) + 1);
      });
    });

    let nodes = Array.from(nodeMap.values());
    let links = Array.from(linkMap, ([key, value]) => {
      const [source, target] = key.split('::');
      return { source, target, value };
    });

    const degreeCount = new Map();
    links.forEach(link => {
      degreeCount.set(link.source, (degreeCount.get(link.source) || 0) + 1);
      degreeCount.set(link.target, (degreeCount.get(link.target) || 0) + 1);
    });

    const top10 = new Set(
      Array.from(degreeCount.entries())
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10)
        .map(d => d[0])
    );

    const relevantNodeIds = new Set();
    links.forEach(link => {
      if (top10.has(link.source) || top10.has(link.target)) {
        relevantNodeIds.add(link.source);
        relevantNodeIds.add(link.target);
      }
    });

    nodes = nodes.filter(n => relevantNodeIds.has(n.id));
    links = links.filter(l => relevantNodeIds.has(l.source) && relevantNodeIds.has(l.target));

    const simulation = d3.forceSimulation(nodes)
      .force('link', d3.forceLink(links).id(d => d.id).distance(80))
      .force('charge', d3.forceManyBody().strength(-200))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .alpha(1).alphaDecay(0.05);

    const link = svg.append('g')
      .attr('stroke', '#aaa')
      .selectAll('line')
      .data(links)
      .join('line')
      .attr('stroke-width', d => Math.sqrt(d.value));

    const node = svg.append('g')
      .attr('stroke', '#fff')
      .attr('stroke-width', 1.5)
      .selectAll('circle')
      .data(nodes)
      .join('circle')
      .attr('r', 6)
      .attr('fill', d => d.type === 'director' ? '#facc15' : '#60a5fa')
      .call(d3.drag()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended))
      .on('mouseover', (event, d) => {
        tooltip.style('opacity', 1).html(`<strong>${d.type}:</strong> ${d.id}`);
      })
      .on('mousemove', event => {
        tooltip.style('left', event.offsetX + 15 + 'px').style('top', event.offsetY - 28 + 'px');
      })
      .on('mouseout', () => tooltip.style('opacity', 0));

    const label = svg.append('g')
      .selectAll('text')
      .data(nodes)
      .join('text')
      .text(d => d.id)
      .attr('font-size', 9)
      .attr('dx', 8)
      .attr('dy', 3)
      .style('fill', '#facc15');

    simulation.on('tick', () => {
      link.attr('x1', d => d.source.x).attr('y1', d => d.source.y)
          .attr('x2', d => d.target.x).attr('y2', d => d.target.y);

      node.attr('cx', d => d.x).attr('cy', d => d.y);
      label.attr('x', d => d.x).attr('y', d => d.y);
    });

    function dragstarted(event) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      event.subject.fx = event.subject.x;
      event.subject.fy = event.subject.y;
    }
    function dragged(event) {
      event.subject.fx = event.x;
      event.subject.fy = event.y;
    }
    function dragended(event) {
      if (!event.active) simulation.alphaTarget(0);
      event.subject.fx = null;
      event.subject.fy = null;
    }
  }
</script>

<style>
  .chart-card {
    background-color: #1e1e1e;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(255, 255, 255, 0.05);
    width: 95vw;
    height: 600px;
    margin: auto;
    position: relative;
    overflow: hidden;
  }

  .title {
    color: #facc15;
    font-weight: bold;
    font-size: 1.3rem;
    margin-bottom: 1rem;
    text-align: center;
  }

  .reset-button {
    position: absolute;
    top: 10px;
    right: 10px;
    background: #facc15;
    border: none;
    padding: 6px 12px;
    font-size: 0.9rem;
    font-weight: bold;
    border-radius: 6px;
    color: #1e1e1e;
    cursor: pointer;
  }

  .legend-box {
    position: absolute;
    top: 10px;
    left: 10px;
    background-color: rgba(0, 0, 0, 0.7);
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 0.85rem;
    color: white;
  }

  .legend-item {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    margin-bottom: 4px;
  }

  .legend-circle {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    display: inline-block;
  }
</style>

<div class="chart-card">
  <div class="title">Star–Director Network</div>
  <button class="reset-button" on:click={resetZoom}>Reset Zoom</button>
  <div class="legend-box">
    <div class="legend-item">
      <span class="legend-circle" style="background:#facc15;"></span> Director
    </div>
    <div class="legend-item">
      <span class="legend-circle" style="background:#60a5fa;"></span> Star
    </div>
  </div>
  <div bind:this={container} style="width: 100%; height: 100%; position: relative;"></div>
</div>
