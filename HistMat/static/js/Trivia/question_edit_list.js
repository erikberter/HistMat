

Vue.component('modal', {
    template: '#modal-template',
    delimiters: ['[[', ']]'],
    data: function () {
        return {
            question: {
                type: "",
                question: "",
                answer: "",
                is_multiple_choice: false
            }
        }
    },
    methods: {
        set_type: function(type){
            if(type=="text"){
                this.question.answer="";
            }else if(type=="multi"){
                this.question.answer=[];
            }
        },
        create_option : function(){
            this.question.answer.push("");
        },
        create_question : function(){
              axios.post(window.location.pathname + 'create_question/', this.question)
              .then((response) => {
                console.log(response);
              }, (error) => {
                console.log(error);
                alert("Error trying to add Question");
              });
        }
    }
  })

var fab = new Vue({
    el: '#question_list',
    delimiters: ['[[', ']]'],
    data: {
        showModal: false,
        create_url: "{% url 'trivia:quiz_update' quiz.slug%}"
    },
    methods: {
        createQuestion: function (event) {
            window.location = this.create_url;
        }
    }
});