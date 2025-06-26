<!-- FlipCard.svelte -->
<div class="flip-card">
  <div class="flip-card-inner">
    <div class="flip-card-front">
      <slot name="front" />
    </div>
    <div class="flip-card-back">
      <slot name="back" />
    </div>
  </div>
</div>

<style>
  .flip-card {
    perspective: 1000px;
    min-width: 180px;
    max-width: 260px;
    width: 100%;
    height: 130px;
  }

  .flip-card-inner {
    position: relative;
    width: 100%;
    height: 100%;
    transition: transform 0.8s ease;
    transform-style: preserve-3d;
  }

  .flip-card:hover .flip-card-inner {
    transform: rotateY(180deg);
  }

  .flip-card-front,
  .flip-card-back {
    position: absolute;
    width: 100%;
    height: 100%;
    padding: 1.5rem 1rem;
    border-radius: 12px;
    background-color: #1a1a1a;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
    text-align: center;
    backface-visibility: hidden;
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-sizing: border-box;
  }

  .flip-card-front {
    z-index: 2;
  }

  .flip-card-back {
    transform: rotateY(180deg);
    z-index: 1;
    color: #facc15;
    font-size: 0.95rem;
    line-height: 1.3;
  }
</style>
