

Vue.component('modal', {
    template: '#modal-template',
    delimiters: ['[[', ']]'],
    data: function () {
        return {
            question_type: "",
            question: {
                type: "",
                question: "",
                answer: ""
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
            this.question.answer.push("ola");
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