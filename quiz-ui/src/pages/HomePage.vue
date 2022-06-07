<template>
  <div class="quiz row animate__animated animate__bounceInDown">
    <div class="card quizz-card col-md-12 mx-auto">
      <div class="card-body">
        <h5 class="card-title"><img src="icon.png" style="width: 30px"/> ChocoQuizzz</h5>
        <p class="card-text">The best Quizzz ever! Proudly presented to you by team Nabla.</p>
        <QuizzzLeaderboard :show-player="false"/>
      </div>
      <div class="button-container col-md-3 mx-auto right pb-4">
        <router-link to="/newquizzz" class="btn btn-primary">Start Quizzz</router-link>
      </div>
    </div>

  </div>
</template>

<script>
import QuizzzLeaderboard from "@/components/QuizzzLeaderboard";
export default {
  name: "HomePage",
  components: {QuizzzLeaderboard}
}
</script>

<style scoped>

</style>