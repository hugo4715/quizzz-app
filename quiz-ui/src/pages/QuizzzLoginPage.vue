<template>
  <div class="quiz row animate__animated animate__bounceInDown">
    <div class="card quizz-card col-md-12 mx-auto">
      <div class="card-body">
        <h5 class="card-title">Login</h5>
        <div v-if="this.error !== ''" class="alert alert-warning" role="alert">
          {{ this.error }}
        </div>
        <div class="card-text">
          <input type="password" class="form-control" id="inputPassword" aria-describedby="passwordHelp" placeholder="Password" v-model="password">
          <div id="passwordHelp" class="form-text">Administrator password</div>
        </div>
      </div>
      <div class="button-container col-md-3 mx-auto right pb-4">
        <button @click="login" class="btn btn-primary" v-bind:disabled="this.password === ''">Login</button>
      </div>
    </div>

  </div>
</template>

<script>

import api from "@/api";
import storage from "@/storage";

export default {
  name: "LoginPage",
  data() {
    return {
      password: '',
      error: ''
    };
  },
  methods: {
    login() {
      this.error = '';
      api.login(this.password).then(resp => {
        if(resp.ok){
          resp.json().then(json => {
            console.log(json);
            const token = json['token'];
            storage.saveAdminToken(token);
            this.$router.push('/admin');
          })
        }else if(resp.status === 401){
          this.error = 'Could not login: Invalid password!';
        }else{
          this.error = 'Could not login: Got code ' + resp.statusCode
        }
      })
    }
  }
}
</script>

<style scoped>

</style>