<template>
  <div>
    <img v-if="question.image" :src="question.image" style="width: 30%;"/>
    <h5 class="card-title">Question #{{ questionNumber }} - {{ question.title}}</h5>
    <p class="card-text">{{ question.text }}</p>
    <div class="row d-flex flex-column align-items-stretch justify-content-evenly">
      <div class="form-check" v-for="(answer,index) in question.possibleAnswers" v-bind:key="answer">
        <input type="radio" class="btn-check" name="options-outlined" :id="'answer-radio-' + index" autocomplete="off" v-model="selectedAnswer"  :value="index" @change="selectedAnswerChanged">
        <label class="btn btn-outline-primary" :for="'answer-radio-' + index" style="width: 100%; height: 100%;">{{ answer.text }}</label>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "QuestionDisplay",
  emits: ['update:modelValue'],
  props: {
    modelValue: {
      type: Number
    },
    question: {
      type: Object
    },
    questionNumber: {
      type: Number
    }
  },
  data() {
    return {
      selectedAnswer: this.modelValue
    };
  },
  methods: {
    selectedAnswerChanged(){
      this.$emit('update:modelValue', this.selectedAnswer);
    }
  }
}
</script>

<style scoped>

</style>