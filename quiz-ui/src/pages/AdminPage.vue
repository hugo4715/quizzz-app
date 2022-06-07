<template>
  <div class="quiz row animate__animated animate__bounceInDown">
    <div class="card quizz-card col-md-12 mx-auto">
      <div class="card-body">
        <h5 class="card-title">Admin - Question editor</h5>
        <div v-if="this.error !== ''" class="alert alert-warning" role="alert">
          {{ this.error }}
        </div>
        <router-link to="/admin/new" class="btn btn-primary">New question</router-link>
        <div v-if="!this.loading" class="card-text table-container">
          <table class="table table-striped">
            <thead>
            <tr>
              <th scope="col">Position</th>
              <th scope="col">Title</th>
              <th scope="col">Actions</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="question in this.quiz" :key="question.position">
              <th scope="row">{{ question.position }}</th>
              <td>{{ question.title }}</td>
              <td><button class="btn btn-primary" @click="this.$router.push('/admin/edit/' + question.position)">Edit</button></td>
            </tr>
            </tbody>
          </table>
        </div>
        <div v-else class="spinner-border text-primary" role="status">
          <span class="sr-only"></span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/api";

export default {
  name: "AdminPage",
  data() {
    return {
      quiz: undefined,
      loading: true,
      error: ''
    };
  },
  created() {
    api.getQuestions().then(data => {
      this.quiz = data;
      this.loading = false;
    })
  }
}
</script>

<style scoped>
.table{
  text-align: center;
}
.table-container{
  overflow-y: scroll;
  max-height: 500px;
}
</style>