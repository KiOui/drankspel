<script setup lang="ts">
import { onMounted, ref } from "vue";
import Bubbles from "@/components/BubblesBackground.vue";
import GamesApiService from "@/common/games.api.service";
import shuffle from "@/util/shuffle";
import type { Game } from "@/models/game.model";

const games = ref<Game[]>([]);
const loading = ref(true);
const playing = ref(false);
const currentGameIndex = ref<number | null>(null);
const intervalId = ref<number | null>(null);
const currentGame = ref<Game | null>(null);
const showExplanation = ref(false);
const explanation = ref<HTMLElement | null>(null);

onMounted(() => {
  GamesApiService.getGames()
    .then((result) => {
      games.value = result;
      loading.value = false;
    })
    .catch(() => {
      window.alert(
        "An error occurred while getting available games, please refresh this page.",
      );
    });
});

function start(event?: Event) {
  if (games.value.length > 0) {
    nextGame();
    playing.value = true;
    startWheel();
    if (event) {
      event.stopPropagation();
    }
  } else {
    window.alert("There are no registered games, please refresh this page.");
  }
}

function clickedScreen(event?: Event) {
  if (playing.value) {
    stop();
    if (event) {
      event.stopPropagation();
    }
  }
}

function stop() {
  currentGame.value = games.value[currentGameIndex.value ?? 0]!;
  stopWheel();
}

function dismiss() {
  currentGame.value = null;
  showExplanation.value = false;
}

function nextGame() {
  let nextGameIndex = (currentGameIndex.value ?? -1) + 1;
  if (nextGameIndex >= games.value.length) {
    nextGameIndex = 0;
  }
  currentGameIndex.value = nextGameIndex;
}

function startWheel() {
  games.value = shuffle(games.value);
  currentGameIndex.value = 0;
  intervalId.value = window.setInterval(() => {
    nextGame();
  }, 250);
}

function stopWheel() {
  if (intervalId.value !== null) {
    clearInterval(intervalId.value);
  }
  intervalId.value = null;
  playing.value = false;
}

function getExplanationHeight() {
  return `${explanation.value?.scrollHeight ?? 0}px`;
}
</script>

<template>
  <Bubbles style="z-index: -1" class="fixed"></Bubbles>
  <div
    v-if="loading"
    class="fixed h-screen w-screen flex justify-center items-center flex-row"
  ></div>
  <div
    class="flex justify-center items-center min-h-screen w-screen flex-row p-2 xl:p-10"
    v-on:click="clickedScreen($event)"
  >
    <div
      v-if="!playing && currentGame === null"
      class="p-10 mx-auto text-center"
    >
      <h1 class="text-4xl font-primary uppercase">Drinking Game</h1>
      <h2 class="mb-5 text-4xl font-primary uppercase">Picker</h2>
      <div>
        <button
          class="jittery p-5 rounded-md font-bold bg-black text-white"
          @click="start($event)"
        >
          Pick a random game!
        </button>
      </div>
    </div>
    <div
      v-else-if="currentGame !== null"
      class="bg-white xl:p-5 p-4 rounded-md pt-5 pb-5 mt-5 mb-5"
      style="width: 42rem"
    >
      <h2
        class="game-title font-primary uppercase text-4xl text-center"
        v-bind:style="{ 'min-width': showExplanation ? 0 : '100%' }"
      >
        {{ currentGame.name }}
      </h2>
      <div
        class="toggle-explanation underline cursor-pointer text-center"
        v-on:click="showExplanation = true"
        v-bind:style="{ 'max-height': showExplanation ? 0 : '2em' }"
      >
        Show explanation
      </div>
      <div
        class="mt-3 explanation-container"
        v-html="currentGame.description"
        v-bind:style="{
          'max-height': showExplanation ? getExplanationHeight() : 0,
        }"
        ref="explanation"
      ></div>
      <div>
        <button
          @click="dismiss"
          type="button"
          class="uppercase mt-3 w-full p-2 rounded-md text-center mx-auto block bg-black text-white"
          v-bind:class="{ 'max-w-md': !showExplanation }"
        >
          Dismiss
        </button>
      </div>
    </div>
    <div
      v-on:click="clickedScreen($event)"
      v-else
      class="p-6 mx-auto text-center rounded-md"
    >
      <span
        v-on:click="clickedScreen($event)"
        class="text-black uppercase text-2xl font-primary cursor-pointer"
        >{{ games[currentGameIndex!]!.name }}</span
      >
    </div>
  </div>
  <footer
    v-if="!playing && currentGame === null"
    class="fixed bottom-0 my-2 w-full block flex justify-center"
  >
    <a
      href="https://github.com/KiOui/drankspel"
      class="underline opacity-80 mx-auto text-black"
      >Check the source code on GitHub</a
    >
  </footer>
</template>

<style>
.jittery {
  animation: jittery 4s infinite;
}

.game-title {
  display: inline-block;
  transition: min-width 1s ease-in-out;
}

.toggle-explanation {
  position: relative;
  bottom: 0;
  overflow: hidden;
  transition: max-height 0.5s ease-in-out;
}

.explanation-container {
  overflow: hidden;
  transition: max-height 1s ease-in-out;
}

.explanation-container h1 {
  font-size: 2.25rem;
  line-height: 2.5rem;
  text-transform: uppercase;
  font-weight: bold;
}

.explanation-container h2 {
  font-size: 1.5rem;
  line-height: 2rem;
  text-transform: uppercase;
  font-weight: bold;
}

.explanation-container h3 {
  font-size: 1.125rem;
  line-height: 1.75rem;
  text-transform: uppercase;
}

.explanation-container h4,
.explanation-container h5,
.explanation-container h6 {
  font-weight: bold;
}

.explanation-container p {
  margin-bottom: 1rem;
}

.explanation-container ul,
.explanation-container ol {
  margin-bottom: 1rem;
  margin-block-start: 1em;
  margin-block-end: 1em;
  margin-inline-start: 0;
  margin-inline-end: 0;
  padding-inline-start: 40px;
  display: block;
}

.explanation-container ul li {
  list-style-type: "\1F37A";
}

.explanation-container ul li,
.explanation-container ol li {
  display: list-item;
  text-align: match-parent;
}

.explanation-container a {
  text-decoration: underline;
}

@keyframes jittery {
  5%,
  50% {
    transform: scale(1);
  }
  10% {
    transform: scale(0.9);
  }
  15% {
    transform: scale(1.15);
  }
  20% {
    transform: scale(1.15) rotate(-5deg);
  }
  25% {
    transform: scale(1.15) rotate(5deg);
  }
  30% {
    transform: scale(1.15) rotate(-3deg);
  }
  35% {
    transform: scale(1.15) rotate(2deg);
  }
  40% {
    transform: scale(1.15) rotate(0);
  }
}
</style>
