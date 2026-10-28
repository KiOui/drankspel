<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from "vue";

defineOptions({
  name: "BubblesBackground",
});

interface BubbleCircle {
  pos: { x: number; y: number };
  alpha: number;
  scale: number;
  speed: number;
  color: string;
  draw: () => void;
}

const props = withDefaults(
  defineProps<{
    options?: Record<string, unknown>;
  }>(),
  {
    options: () => ({}),
  },
);

const canvas = ref<HTMLCanvasElement | null>(null);
const circles = ref<BubbleCircle[]>([]);
const requestAniId = ref<number | null>(null);
const width = ref(window.innerWidth);
const height = ref(window.innerHeight);

const opts = computed(() => ({
  color: "rgba(255, 255, 255, 0.3)",
  radius: 30,
  density: 0.3,
  clearOffset: 0.8,
  ...props.options,
}));

function randomColor() {
  const r = Math.floor(Math.random() * 255);
  const g = Math.floor(Math.random() * 255);
  const b = Math.floor(Math.random() * 255);
  const alpha = Math.random().toPrecision(2);
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

function resize() {
  width.value = window.innerWidth;
  height.value = window.innerHeight;
}

function resetCircle(circle: BubbleCircle) {
  const settings = opts.value;
  circle.pos.x = Math.random() * width.value;
  circle.pos.y = height.value + Math.random() * 100;
  circle.alpha = 0.1 + Math.random() * Number(settings.clearOffset);
  circle.scale = 0.1 + Math.random() * 0.3;
  circle.speed = Math.random();
  circle.color =
    settings.color === "random" ? randomColor() : String(settings.color);
}

function makeCircle(): BubbleCircle {
  const settings = opts.value;
  const circle: BubbleCircle = {
    pos: { x: 0, y: 0 },
    alpha: 0,
    scale: 0,
    speed: 0,
    color: "",
    draw() {
      const ctx = canvas.value?.getContext("2d");
      if (!ctx) return;

      if (circle.alpha <= 0) {
        resetCircle(circle);
      }

      circle.pos.y -= circle.speed;
      circle.alpha -= 0.0005;

      ctx.beginPath();
      ctx.arc(
        circle.pos.x,
        circle.pos.y,
        circle.scale * Number(settings.radius),
        0,
        2 * Math.PI,
        false,
      );
      ctx.fillStyle = circle.color;
      ctx.fill();
      ctx.closePath();
    },
  };

  resetCircle(circle);
  return circle;
}

function animate() {
  const ctx = canvas.value?.getContext("2d");
  if (!ctx) return;

  if (requestAniId.value !== null) {
    cancelAnimationFrame(requestAniId.value);
  }

  ctx.clearRect(0, 0, width.value, height.value);

  for (const circle of circles.value) {
    circle.draw();
  }

  requestAniId.value = requestAnimationFrame(animate);
}

onMounted(() => {
  const settings = opts.value;

  for (let x = 0; x < width.value * Number(settings.density); x++) {
    circles.value.push(makeCircle());
  }

  animate();
  window.addEventListener("resize", resize);
});

onBeforeUnmount(() => {
  if (requestAniId.value !== null) {
    cancelAnimationFrame(requestAniId.value);
  }

  window.removeEventListener("resize", resize);
});
</script>

<template>
  <canvas
    ref="canvas"
    :width="width"
    :height="height"
    style="position: fixed; top: 0; left: 0"
  ></canvas>
</template>
