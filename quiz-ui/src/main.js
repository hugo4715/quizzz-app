import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap'; import 'bootstrap/dist/css/bootstrap.min.css';
import 'animate.css';
import HomePage from "@/pages/HomePage";
import QuizzzPage from "@/pages/QuizzzPage";
import { createRouter, createWebHashHistory } from 'vue-router'
import NewQuizzzPage from "@/pages/NewQuizzzPage";
import ResultsPage from "@/pages/ResultsPage";
import LoginPage from "@/pages/QuizzzLoginPage";
import AdminPage from "@/pages/AdminPage";
import EditQuestionPage from "@/pages/EditQuestionPage";
import NewQuestionPage from "@/pages/NewQuestionPage";

const routes = [
    { path: '/', component: HomePage },
    { path: '/newquizzz', component: NewQuizzzPage},
    { path: '/quizzz', component: QuizzzPage },
    { path: '/results', component: ResultsPage },
    { path: '/login', component: LoginPage },
    { path: '/admin', component: AdminPage },
    { path: '/admin/edit/:id', component: EditQuestionPage },
    { path: '/admin/new', component: NewQuestionPage },

]

const router = createRouter({
    history: createWebHashHistory(),
    routes,
})

let app = createApp(App);
app.use(router)
app.mount('#app');
