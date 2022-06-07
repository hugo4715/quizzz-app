<template>
  <div class="quiz row animate__animated animate__bounceInDown">
    <div class="card quizz-card col-md-12 mx-auto">
      <div class="card-body">
        <div v-if="this.loaded">
          <h3>Question #{{ question.position }}</h3>

          <div class="row">
            <div class="col-md-6">
              <img v-if="question.image" :src="question.image" style="width: 30%;"/>
              <div class="pt-2">
                <ImageUpload v-if="this.editing" @file-change="imageFileChangedHandler" />
              </div>
              <div class="form-group">
                <label for="inputTitle">Title</label>
                <input type="text" class="form-control" id="inputTitle" :disabled="!this.editing" aria-describedby="titleHelp" placeholder="Enter Title" v-model="this.question.title">
              </div>
              <div class="form-group">
                <label for="inputQuestionText">Question Text</label>
                <input type="text" class="form-control" id="inputQuestionText" :disabled="!this.editing" placeholder="Enter the text of the question" v-model="this.question.text">
              </div>
              <div class="form-group">
                <label for="inputQuestionNumber">Question Position</label>
                <input type="number" min="1" class="form-control" id="inputQuestionNumber" :disabled="!this.editing" placeholder="Position" v-model="this.question.position">
              </div>
            </div>
            <div class="col-md-6">
              <div v-for="(answer,index) in question.possibleAnswers" :key="index">
                <div class="form-group">
                  <label :for="'inputQuestionNumber'+index">Answer #{{ index+1 }}<input type="checkbox" v-bind:checked="answer.isCorrect" :disabled="!this.editing" @click="setAnswerCorrect(index)"/></label>
                  <textarea type="text" :class="answer.isCorrect ? 'form-control isgreen' : 'form-control'"  :id="'inputQuestionNumber'+index" :disabled="!this.editing" :placeholder="'Answer #'+(index+1)" v-model="answer.text"/>
                </div>
              </div>

            </div>
          </div>

          <div v-if="!this.editing" >
            <router-link to="/admin" class="btn btn-primary">Back</router-link>
            <button  class="btn btn-warning" @click="this.editing = true">Edit this question</button>
            <button class="btn btn-danger" @click="deleteQuestion" >Delete</button>
          </div>
          <div v-else>
            <button class="btn btn-danger" @click="cancelChanges" >Cancel</button>
            <button class="btn btn-success" @click="saveChanges" >Save changes</button>
          </div>
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
import ImageUpload from "@/components/ImageUpload";

export default {
  name: "EditQuestionPage",
  components: {ImageUpload},
  data() {
    return {
      id: this.$route.params.id,
      loaded: false,
      question: undefined,
      originQuestion: undefined,
      editing: false,
    };
  },
  created() {
    api.getQuestion(this.id).then(data => {
      this.question = data;
      this.originQuestion = structuredClone(data);
      this.loaded = true;
    })
  },
  methods: {
    saveChanges() {
      this.loaded = false;
      api.updateQuestion(this.id, this.question).then(() => {
        this.loaded = true;
        this.$router.push('/admin')
      });
      console.log(this.question.possibleAnswers);
    },
    cancelChanges() {
      this.editing = false;
      this.question = structuredClone(this.originQuestion);
    },
    deleteQuestion() {
      this.loaded = false;
      api.deleteQuestion(this.id).then(resp => {
        if(resp.ok){
          this.$router.push('/admin');
        }else if(resp.status === 401){
          this.$router.push('/login');
        }else{
          this.loaded = true;
          alert('Could not delete question: Got code ' + resp.status);
        }
      })
    },
    setAnswerCorrect(index) {
      for (let i = 0; i < this.question.possibleAnswers.length; i++) {
        this.question.possibleAnswers[i].isCorrect = index === i;
      }
    },
    imageFileChangedHandler(b64String) {
      this.question.image = b64String;
    }
  }
}
</script>

<style scoped>
.btn{
  margin: 20px 20px 0 0;
}
.isgreen{
  background-color: rgba(0,255,0,0.5) !important;
}
</style>