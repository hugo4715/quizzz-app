<template>
  <div class="quiz row animate__animated animate__bounceInDown">
    <div class="card quizz-card col-md-12 mx-auto">
      <div class="card-body">
        <h5 class="card-title">User infos</h5>
        <div class="card-text">
          <input type="text" class="form-control" id="inputUsername" aria-describedby="usernameHelp" placeholder="Username" v-model="username">
          <div id="usernameHelp" class="form-text">Used to display your score in the leaderboard</div>
        </div>
      </div>
      <div class="button-container col-md-3 mx-auto right pb-4">
        <button @click="startQuizzz" class="btn btn-primary" v-bind:disabled="this.username === ''">Start Quizzz</button>
      </div>
    </div>

  </div>
</template>

<script>
import storage from '@/storage';

export default {
  name: "HomePage",
  data() {
    return {
      username: ''
    };
  },
  methods: {
    startQuizzz() {
      storage.savePlayerName(this.username);
      this.$router.push('/quizzz');
    }
  }
}
</script>

<style scoped>

</style>