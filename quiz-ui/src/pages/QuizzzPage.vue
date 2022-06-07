<template>
  <div v-if="loading" class="loading">
    <div class="spinner-border" role="status">
      <span class="sr-only"></span>
    </div>
  </div>
  <div v-else>
    <div class="quiz row animate__animated animate__bounceInDown">
      <div class="card quizz-card col-md-12 mx-auto">
        <div class="card-body">
          <QuestionDisplay :question-number="currentQuestion.position" :question="currentQuestion" v-model="selectedAnswer"></QuestionDisplay>
        </div>
        <div class="button-container col-md-3 mx-auto right pb-4">
          <button v-if="!this.isFinished" @click="nextQuestion" class="btn btn-primary" :disabled="this.animating">Confirm ✔</button>
          <button v-else @click="checkAnswer" class="btn btn-primary" >Finish ✔</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import JSConfetti from "js-confetti";
import api from "@/api";
import QuestionDisplay from "@/components/QuestionDisplay";
import storage from "@/storage";

export default {
  name: "QuizzzPage",
  components: {QuestionDisplay},
  data() {
    return {
      loading: true,
      selectedQuestionIndex: 0,
      quiz: [],
      answers: [],
      result: null,
      jsConfetti: null,
      animating: false,
      selectedAnswer: 0,
    };
  },
  created() {
    this.jsConfetti = new JSConfetti()
    api.getQuestions().then(data => {
      this.loading = false;
      this.quiz = data;
    });
  },
  computed: {
    currentQuestion() {
      return this.quiz[this.selectedQuestionIndex];
    },
    isFinished(){
      return this.selectedQuestionIndex === this.quiz.length-1;
    }
  },
  methods: {
    wrongAnswerParticles(){
      const canvas = document.getElementById('#app')
      this.jsConfetti.addConfetti({
        canvas,
        emojis: ['❌','❌','😭'],
        emojiSize: 70,
        confettiNumber: 70,
      })
    },
    correctAnswerParticles() {
      const canvas = document.getElementById('#app')
      let r = Math.random();
      if(r < .25){
        this.jsConfetti.addConfetti({
          canvas,
          emojis: ['🦄','🦄','🦄','🅑🅡🅐🅥🅞'],
          emojiSize: 60,
          confettiNumber: 70,
        })
      }else if(r < .6){
        this.jsConfetti.addConfetti({
          canvas,
          emojis: ['🌈', '⚡️', '💥', '✨', '💫', '🌸'],
          emojiSize: 50,
          confettiNumber: 150,
        })
      }else{
        this.jsConfetti.addConfetti({canvas})
      }

    },
    isCorrectAnswer(){
      let answers = this.currentQuestion.possibleAnswers;
      for (let i = 0; i < answers.length; i++) {
        if(answers[i].isCorrect){
          return i === this.selectedAnswer;
        }
      }
      return false;
    },
    nextQuestion(){
      if (this.isCorrectAnswer()) {
        this.correctAnswerParticles()
        this.animateCSS('.quiz', 'bounceOutLeft', () => {
          this.selectedQuestionIndex++;
          this.animating = false;
        });
      }else{
        this.wrongAnswerParticles()
        this.animateCSS('.quiz', 'hinge', () => {
          this.selectedQuestionIndex++;
          this.animating = false;
        });
      }
      this.animating = true;

      window.cameraNextPosition();
      this.answers.push(this.selectedAnswer);
    },
    checkAnswer() {
      this.answers.push(this.selectedAnswer);
      api.postAnswers(this.answers)
          .then(data => {
            storage.saveParticipationScore(data['score'])
            this.$router.push('/results')
          });
    },
    animateCSS(element, animation, callback = function(){},  prefix = 'animate__') {
      new Promise((resolve) => {
        const animationName = `${prefix}${animation}`;
        const node = document.querySelector(element);

        node.classList.add(`${prefix}animated`, animationName);

        function handleAnimationEnd(event) {
          event.stopPropagation();
          node.classList.remove(`${prefix}animated`, animationName);
          callback();
          resolve('Animation ended');
        }

        node.addEventListener('animationend', handleAnimationEnd, {once: true});
      });
    },
  }
}
</script>
