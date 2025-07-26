<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  export let imdbCSV = [];
  let wrapper;     // for fullscreen target
  let container;   // network rendering area
  let tooltip;
  let zoomBehavior;
  let svgRoot;
  let highlightedNode = null;

  onMount(() => {
    if (imdbCSV.length) drawNetwork();
  });

  function toggleFullscreen(event) {
    event.stopPropagation(); // prevent zoom handler
    if (!document.fullscreenElement) {
      wrapper.requestFullscreen();
    } else {
      document.exitFullscreen();
    }
  }

  function resetZoom(event) {
    event.stopPropagation(); // prevent zoom handler
    const nodesGroup = svgRoot.select('g');
    const bounds = nodesGroup.node().getBBox();
    const fullWidth = container.clientWidth;
    const fullHeight = container.clientHeight;
    const width = bounds.width;
    const height = bounds.height;
    const midX = bounds.x + width / 2;
    const midY = bounds.y + height / 2;

    const scale = 0.85 / Math.max(width / fullWidth, height / fullHeight);
    const translate = [
      fullWidth / 2 - scale * midX,
      fullHeight / 2 - scale * midY
    ];

    svgRoot.transition().duration(750)
      .call(zoomBehavior.transform,
            d3.zoomIdentity.translate(translate[0], translate[1]).scale(scale));
  }

  function fitToScreen() {
    resetZoom(new Event("custom")); // initial fit
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
      .on('zoom', (event) => svg.attr('transform', event.transform));

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

    const nodeDegree = d => links.filter(l => l.source === d.id || l.target === d.id).length;
    const maxDegree = d3.max(nodes, nodeDegree);
    const sizeScale = d3.scaleLinear().domain([1, maxDegree]).range([5, 15]);
    const colorScale = d3.scaleLinear().domain([1, d3.max(links, d => d.value)]).range(["#aaa", "#f87171"]);

    const simulation = d3.forceSimulation(nodes)
      .force('link', d3.forceLink(links).id(d => d.id).distance(80))
      .force('charge', d3.forceManyBody().strength(-200))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .alpha(1).alphaDecay(0.05);

    const link = svg.append('g')
      .attr('stroke-opacity', 0.8)
      .selectAll('line')
      .data(links)
      .join('line')
      .attr('stroke-width', d => 2 + d.value * 1.5)
      .attr('stroke', d => colorScale(d.value))
      .on('mouseover', (event, d) => {
        tooltip.style('opacity', 1)
          .html(`<strong>${d.source.id}</strong> & <strong>${d.target.id}</strong><br/>Movies together: ${d.value}`);
      })
      .on('mousemove', event => tooltip.style('left', event.offsetX + 15 + 'px').style('top', event.offsetY - 28 + 'px'))
      .on('mouseout', () => tooltip.style('opacity', 0));

    const node = svg.append('g')
      .attr('stroke', '#fff')
      .attr('stroke-width', 1.5)
      .selectAll('circle')
      .data(nodes)
      .join('circle')
      .attr('r', d => d.type === 'director' ? sizeScale(nodeDegree(d)) + 4 : sizeScale(nodeDegree(d)))
      .attr('fill', d => d.type === 'director' ? '#facc15' : '#fb923c')
      .style('cursor', 'pointer')
      .on('mouseover', (event, d) => {
        tooltip.style('opacity', 1).html(`<strong>${d.type}:</strong> ${d.id}`);
      })
      .on('mousemove', event => tooltip.style('left', event.offsetX + 15 + 'px').style('top', event.offsetY - 28 + 'px'))
      .on('mouseout', () => tooltip.style('opacity', 0))
      .on('click', (event, d) => handleNodeClick(d));

    const label = svg.append('g')
      .selectAll('text')
      .data(nodes)
      .join('text')
      .text(d => d.id)
      .attr('font-size', 10)
      .attr('dx', 8)
      .attr('dy', 3)
      .style('fill', '#fff')
      .style('display', 'none')
      .style('pointer-events', 'none');

    simulation.on('tick', () => {
      link.attr('x1', d => d.source.x).attr('y1', d => d.source.y)
          .attr('x2', d => d.target.x).attr('y2', d => d.target.y);
      node.attr('cx', d => d.x).attr('cy', d => d.y);
      label.attr('x', d => d.x).attr('y', d => d.y);
    });

    simulation.on('end', () => fitToScreen());

    svgRoot.on('click', (event) => {
      if (event.target.tagName === 'svg') resetHighlight();
    });

    function resetHighlight() {
      highlightedNode = null;
      node.attr('fill', n => n.type === 'director' ? '#facc15' : '#fb923c');
      link.attr('stroke', d => colorScale(d.value)).attr('stroke-opacity', 0.8);
      label.style('display', 'none');
    }

    function handleNodeClick(d) {
      if (highlightedNode === d.id) {
        resetHighlight();
      } else {
        highlightedNode = d.id;
        const connected = new Set(links.filter(l => l.source.id === d.id || l.target.id === d.id)
          .flatMap(l => [l.source.id, l.target.id]));
        node.attr('fill', n => connected.has(n.id) ? (n.type === 'director' ? '#facc15' : '#fb923c') : '#444');
        link.attr('stroke', l => (l.source.id === d.id || l.target.id === d.id) ? '#facc15' : colorScale(l.value))
            .attr('stroke-opacity', l => (l.source.id === d.id || l.target.id === d.id) ? 1 : 0.2);
        label.style('display', n => connected.has(n.id) ? 'block' : 'none');

        const scale = 1.5;
        const translate = [
          container.clientWidth / 2 - d.x * scale,
          container.clientHeight / 2 - d.y * scale
        ];
        svgRoot.transition().duration(750)
          .call(zoomBehavior.transform, d3.zoomIdentity.translate(translate[0], translate[1]).scale(scale));
      }
    }

    node.call(d3.drag()
      .on('start', event => { if (!event.active) simulation.alphaTarget(0.3).restart(); event.subject.fx = event.subject.x; event.subject.fy = event.subject.y; })
      .on('drag', event => { event.subject.fx = event.x; event.subject.fy = event.y; })
      .on('end', event => { if (!event.active) simulation.alphaTarget(0); event.subject.fx = null; event.subject.fy = null; }));
  }
</script>

<style>
 .chart-card {
  background: radial-gradient(circle at center, #1e1e1e 40%, #111 100%);
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(255, 255, 255, 0.05);
  width: 100%;
  height: 450px;
  position: relative;
  overflow: hidden;
}

.title {
  color: #facc15;
  font-weight: bold;
  font-size: 1.2rem;
  text-align: center;
  position: absolute;
  top: 14px;
  width: 100%;
  pointer-events: none;
}

.reset-button, .fullscreen-button {
  position: absolute;
  top: 10px;
  width: 36px;
  height: 36px;
  background: #facc15;
  border: none;
  font-size: 1.2rem;
  font-weight: bold;
  border-radius: 6px;
  color: #1e1e1e;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
  z-index: 1000;         /* keeps above SVG */
  pointer-events: auto;  /* ensure clickable */
}

.reset-button { right: 10px; }
.fullscreen-button { right: 56px; }

.legend-box {
  position: absolute;
  bottom: 20px;
  left: 20px;
  background-color: rgba(0, 0, 0, 0.7);
  border-radius: 6px;
  padding: 8px 12px;
  font-size: 0.85rem;
  color: white;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.legend-item { display: flex; align-items: center; gap: 0.4rem; margin-bottom: 4px; }
.legend-circle { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
</style>

<div class="chart-card" bind:this={wrapper}>
  <div class="title">Star–Director Network</div>
  <button class="fullscreen-button" on:click={toggleFullscreen} aria-label="Full Screen">⛶</button>
  <button class="reset-button" on:click={resetZoom} aria-label="Reset Zoom">↻</button>
  <div class="legend-box">
    <div class="legend-item">
      <span class="legend-circle" style="background:#facc15;"></span> Director
    </div>
    <div class="legend-item">
      <span class="legend-circle" style="background:#fb923c;"></span> Star
    </div>
    <div class="legend-item">
      <svg width="80" height="10">
        <defs>
          <linearGradient id="edgeGradient" x1="0%" x2="100%">
            <stop offset="0%" stop-color="#aaa"/>
            <stop offset="100%" stop-color="#f87171"/>
          </linearGradient>
        </defs>
        <rect width="80" height="10" fill="url(#edgeGradient)"></rect>
      </svg>
      <span>1 → Max movies</span>
    </div>
  </div>
  <div bind:this={container} style="width: 100%; height: 100%; position: relative;"></div>
</div>
