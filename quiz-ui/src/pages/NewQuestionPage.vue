<template>
  <div class="quiz row animate__animated animate__bounceInDown">
    <div class="card quizz-card col-md-12 mx-auto">
      <div class="card-body">
        <h3>Question #{{ question.position }}</h3>

        <div v-if="!this.loading">
          <img v-if="question.image" :src="question.image" style="width: 30%;"/>
          <div class="pt-2">
            <ImageUpload @file-change="imageFileChangedHandler" />
          </div>
          <div class="row">
            <div class="col-md-6">
              <div class="form-group">
                <label for="inputTitle">Title</label>
                <input type="text" class="form-control" id="inputTitle" aria-describedby="titleHelp" placeholder="Enter Title" v-model="this.question.title">
              </div>
              <div class="form-group">
                <label for="inputQuestionText">Question Text</label>
                <input type="text" class="form-control" id="inputQuestionText" placeholder="Enter the text of the question" v-model="this.question.text">
              </div>
              <div class="form-group">
                <label for="inputQuestionNumber">Question Position</label>
                <input type="number" min="1" class="form-control" id="inputQuestionNumber" placeholder="Position" v-model="this.question.position">
              </div>
            </div>
            <div class="col-md-6">
              <div v-for="(answer,index) in question.possibleAnswers" :key="index">
                <div class="form-group">
                  <label :for="'inputQuestionNumber'+index">Answer #{{ index+1 }}<input type="checkbox" v-bind:checked="answer.isCorrect" @click="setAnswerCorrect(index)"/></label>
                  <textarea type="text" :class="answer.isCorrect ? 'form-control isgreen' : 'form-control'" :id="'inputQuestionNumber'+index" :placeholder="'Answer #'+(index+1)" v-model="answer.text"/>
                </div>
              </div>
            </div>
          </div>

          <router-link to="/admin" class="btn btn-danger" >Cancel</router-link>
          <button class="btn btn-success" @click="saveChanges" >Save changes</button>
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
  name: "NewQuestionPage",
  components: { ImageUpload },
  data() {
    return {
      question: undefined,
      loading: false,
    };
  },
  created() {
    this.question = {
      title: '',
      text: '',
      position: 1,
      image: '',
      possibleAnswers: [
        {
          text: '',
          isCorrect: true,
        },
        {
          text: '',
          isCorrect: false,
        },
        {
          text: '',
          isCorrect: false,
        },
        {
          text: '',
          isCorrect: false,
        },
      ]
    }
  },
  methods: {
    saveChanges() {
      this.loading = true;
      api.createQuestion(this.question).then(resp => {
        if(resp.ok){
          this.$router.push('/admin')
        }else if(resp.status === 401){
          this.$router.push('/login')
        }else{
          alert('Could not create question: Got code ' + resp.status);
          this.loading = false;
        }
      });
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