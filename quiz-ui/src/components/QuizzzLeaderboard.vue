<template>
  <div v-if="this.loaded && this.infos['scores'].length > 0" class="table-container">
    <h3>Scores</h3>
      <table class="table table-responsive">
        <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Username</th>
          <th scope="col">Score</th>
          <th scope="col">Date</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(score,index) in this.infos['scores']" :style="this.isColored(index) ? 'font-weight: bold' : ''" :key="score['date']" :class="this.isColored(index) ? 'table-primary' : ''">
          <th scope="row">{{ index+1 }}</th>
          <td>{{ score['playerName'] }}</td>
          <td>{{ score['score'] }}</td>
          <td>{{ score['date']}}</td>
        </tr>
        </tbody>
      </table>
  </div>
</template>

<script>
import api from "@/api";
import storage from "@/storage";

export default {
  name: "QuizzzLeaderboard",
  props: {
    showPlayer: {
      type: Boolean
    }
  },
  data() {
    return {
      loaded: false,
      infos: undefined
    };
  },
  created(){
    this.username = storage.getPlayerName();
    api.getQuizInfo().then(data => {
      this.infos = data;
      this.loaded = true;
    });
  },
  computed: {
    latestScoreRow(){
      let sortedScores = this.infos['scores'].slice();
      sortedScores.forEach((el, index) => {el['realIndex'] = index});
      sortedScores.sort(function(a,b){
        return new Date(a['date']) - new Date(b['date'])
      })
      for (let i = sortedScores.length-1; i >= 0; i--) {
        if(sortedScores[i]['playerName'] === this.username)return sortedScores[i]['realIndex'];
      }
      return -1;
    }
  },
  methods: {
    isColored(index){
      return this.showPlayer && index === this.latestScoreRow;
    }
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