<template>
  <Background3D>
    <QuizzzNavbar/>
    <div id="app" class="container">
      <router-view></router-view>
    </div>
  </Background3D>

</template>
<script>
import Background3D from "@/components/Background3D";
import QuizzzNavbar from "@/components/Navbar";

export default {
  name: 'App',
  components: {QuizzzNavbar, Background3D},
};
</script>

<style>
html, body{
  height: 100%;
  font-family: "Times New Roman", Times, serif;
  font-size: 20px;
}
.quiz{
  padding-left: 20%;
  padding-right: 20%;
}

li {
  list-style-type: none;
}

.quizz-card {
  background-color: rgba(245, 245, 245, 0.9) !important;
}
</style>
