<template>
  <div class="quiz row animate__animated animate__bounceInDown">
    <div class="card quizz-card col-md-12 mx-auto">
      <div class="card-body">
        <h2 style="text-align: center" class="card-title">Your score is {{ this.score }}</h2>
        <div class="card-text">
          <QuizzzLeaderboard :show-player="true"/>
        </div>
      </div>
      <div class="button-container col-md-3 mx-auto right pb-4">
        <router-link to="/" class="btn btn-primary">Back to home</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import storage from '@/storage';
import QuizzzLeaderboard from "@/components/QuizzzLeaderboard";

export default {
  name: "ResultsPage",
  components: {QuizzzLeaderboard},
  data() {
    return {
      score: 0,
      playerName: '',
    };
  },
  created() {
    this.score = storage.getParticipationScore();
    this.playerName = storage.getPlayerName();
  },
  methods: {

  }
}
</script>

<style scoped>

</style>