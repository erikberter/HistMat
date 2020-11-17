
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.xsrfCookieName = 'csrftoken';


var vm = new Vue({
    el: '#quiz-app',
    delimiters: ['[[', ']]'],
    data: {
       quiz : {
          name : "",
          n_question : 0,
          questions : [],
       },
       quiz_status : {
          act_question : 0,
          q_answer : ""
       },

       loading: true,
       errored: false
    },
    created(){
      axios({
         method: 'get',
         url: window.location.pathname, 
         data: {
         },
         xsrfHeaderName : 'X-CSRFToken',
         xsrfCookieName : 'csrftoken',
         headers: {
            "X-Requested-With": 'XMLHttpRequest', 
         }
      })
      .then(response => {
      console.log(response);
        this.quiz.name = response.data.quiz_name;
        console.log("New quiz name is " + this.quiz.name);
        this.quiz.questions = response.data.questions;
        console.log("Questions are " + this.quiz.questions[0]["answer"]);
        this.quiz.n_question = this.quiz.questions.length ;
        console.log("We received  " + this.quiz.n_question + " questions");
      })
      .catch(error => {
        console.log(error)
        this.errored = true
      })
      .finally(() => this.loading = false)
    }
 });