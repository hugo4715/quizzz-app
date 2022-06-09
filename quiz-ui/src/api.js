import storage from '@/storage';
const host = process.env.VUE_APP_QUIZ_API_URL;

export default {
    getQuizInfo() {
        return fetch(host + 'quiz-info')
            .then(response => response.json())
    },
    getQuestions() {
        return fetch(host + 'questions')
            .then(response => response.json())
    },
    getQuestion(id) {
        return fetch(host + 'questions/' + id)
            .then(response => response.json())
    },
    postAnswers(answers) {
        return fetch(host + 'participations', {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: 'POST',
            body: JSON.stringify({
                'playerName': storage.getPlayerName(),
                'answers': answers
            })
        }).then(response => response.json())
    },
    login(password){
        return fetch(host + 'login', {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: 'POST',
            body: JSON.stringify({
                'password': password,
            })
        })
    },
    deleteQuestion(id) {
        return fetch(host + 'questions/' + id, {
            headers: {
                'Authorization': storage.getAdminToken()
            },
            method: 'DELETE'
        })
    },
    updateQuestion(id, question) {
        return fetch(host + 'questions/' + id, {
            headers: {
                'Authorization': storage.getAdminToken(),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(question),
            method: 'PUT'
        })
    },
    createQuestion(question) {
        return fetch(host + 'questions', {
            headers: {
                'Authorization': storage.getAdminToken(),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(question),
            method: 'POST'
        })
    }
};