<script setup lang="ts">
import { RouterView } from "vue-router";
</script>

<template>
  <RouterView />
</template>

<style>
body {
  background: rgb(255, 173, 0);
  background-repeat: no-repeat;
  background-size: cover;
  background: linear-gradient(
    0deg,
    rgba(255, 173, 0, 1) 0%,
    rgba(255, 229, 0, 1) 95%,
    rgba(255, 255, 255, 1) 99%
  );
  min-width: calc(
    100vw - env(safe-area-inset-right) - env(safe-area-inset-left)
  );
  min-height: calc(
    100vh - env(safe-area-inset-bottom) - env(safe-area-inset-top)
  );
  min-height: -webkit-fill-available;
  padding: env(safe-area-inset-top) env(safe-area-inset-right)
    env(safe-area-inset-bottom) env(safe-area-inset-left);
}
</style>
