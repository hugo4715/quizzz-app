<template>
  <nav class="navbar navbar-expand-lg text-black container">
    <a class="navbar-brand" href="#"><img src="icon.png" style="width: 30px;margin-right: 10px;"/>ChocoQuizzz</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>

    <ul class="navbar-nav mr-auto">
      <li class="nav-item active">
        <a class="nav-link" href="#" @click="home">Home <span class="sr-only"></span></a>
      </li>
      <li class="nav-item">
        <router-link to="/login" class="nav-link" href="#" @click="login">Admin</router-link>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: "QuizzzNavbar",
  methods: {
    login(){
      this.$router.push('/login');
    },
    home(){
      this.$router.push('/');
    }
  }
}
</script>

<style scoped>
a {
  color: black;
  padding: 10px 30px 10px 30px;
  margin: 10px;
  background-color: rgba(255,255,255,0.5);
  border-radius: 10px;
}

a:hover {
  background-color: rgba(255,255,255,1);
}
</style>