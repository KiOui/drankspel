<template>
  <Bubbles style="z-index: -1;" class="fixed"></Bubbles>
  <div v-if="loading" class="fixed h-screen w-screen flex justify-center items-center flex-row">

  </div>
  <div class="flex justify-center items-center min-h-screen w-screen flex-row p-2 xl:p-10" v-on:click="clickedScreen($event)">
    <div v-if="!playing && currentGame === null" class="p-10 mx-auto text-center">
      <h1 class="text-4xl font-primary uppercase">Drinking Game</h1>
      <h2 class="mb-5 text-4xl font-primary uppercase">Picker</h2>
      <div>
        <button class="jittery p-5 rounded-md font-bold bg-black text-white" @click="start($event)">Pick a random game!</button>
      </div>
    </div>
    <div v-else-if="currentGame !== null" class="bg-white xl:p-5 p-4 rounded-md pt-5 pb-5 mt-5 mb-5" style="width: 42rem">
      <h2 class="game-title font-primary uppercase text-4xl text-center" v-bind:style="{ 'min-width': showExplanation ? 0 : '100%' }">{{ currentGame.name }}</h2>
      <div class="toggle-explanation underline cursor-pointer text-center" v-on:click="showExplanation = true;" v-bind:style="{ 'max-height': showExplanation ? 0 : '2em' }">Show explanation</div>
      <div class="mt-3 explanation-container" v-html="currentGame.description" v-bind:style="{ 'max-height': showExplanation ? getExplanationHeight() : 0 }" ref="explanation"></div>
      <div>
        <button @click="dismiss" type="button" class="uppercase mt-3 w-full p-2 rounded-md text-center mx-auto block bg-black text-white" v-bind:class="{ 'max-w-md': !showExplanation }">
          Dismiss
        </button>
      </div>
    </div>
    <div v-on:click="clickedScreen($event)" v-else class="p-6 mx-auto text-center rounded-md">
      <span v-on:click="clickedScreen($event)" class="text-black uppercase text-2xl font-primary cursor-pointer">{{ games[currentGameIndex].name }}</span>
    </div>
  </div>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";
import Bubbles from "@/components/Bubbles.vue";
import GamesApiService from "@/common/games.api.service";
import shuffle from "@/util/shuffle";
import Game from "@/models/game.model";

@Options({
  name: "Index",
  data () {
    return {
      games: [],
      loading: true,
      playing: false,
      currentGameIndex: null,
      intervalId: null,
      currentGame: null,
      showExplanation: false,
    }
  },
  components: {
    Bubbles,
  },
  mounted() {
    GamesApiService.getGames().then((result) => {
      this.games = result;
      this.loading = false;
    }).catch(() => {
      window.alert("An error occurred while getting available games, please " +
        "refresh this page.");
    });
  },
  methods: {
    start(event: Event) {
      if (this.games.length > 0) {
        this.nextGame();
        this.playing = true;
        this.startWheel();
        if (event) {
          event.stopPropagation();
        }
      }
      else {
        window.alert("There are no registered games, please refresh this page.")
      }
    },
    clickedScreen(event: Event) {
      if (this.playing) {
        this.stop();
        if (event) {
          event.stopPropagation();
        }
      }
    },
    stop() {
      this.currentGame = this.games[this.currentGameIndex];
      this.stopWheel();
    },
    dismiss() {
      this.currentGame = null;
      this.showExplanation = false;
    },
    nextGame() {
      let nextGameIndex = this.currentGameIndex + 1;
      if (nextGameIndex >= this.games.length) {
        nextGameIndex = 0;
      }
      this.currentGameIndex = nextGameIndex;
    },
    startWheel() {
      this.games = shuffle(this.games);
      this.currentGameIndex = 0;
      this.intervalId = window.setInterval(this.nextGame, 250);
    },
    stopWheel() {
      clearInterval(this.intervalId);
      this.intervalId = null;
      this.playing = false;
    },
    getExplanationHeight() {
      return `${this.$refs.explanation.scrollHeight}px`;
    }
  }
})
export default class Index extends Vue {}
</script>

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
  transition: max-height .5s ease-in-out;
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

.explanation-container h4, .explanation-container h5, .explanation-container h6 {
  font-weight: bold;
}

.explanation-container p {
  margin-bottom: 1rem;
}

.explanation-container ul, .explanation-container ol {
  margin-bottom: 1rem;
  margin-block-start: 1em;
  margin-block-end: 1em;
  margin-inline-start: 0;
  margin-inline-end: 0;
  padding-inline-start: 40px;
  display: block;
}

.explanation-container ul li {
  list-style-type: '\1F37A';
}

.explanation-container ul li, .explanation-container ol li {
  display: list-item;
  text-align: match-parent;
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