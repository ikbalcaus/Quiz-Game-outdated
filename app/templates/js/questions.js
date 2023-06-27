{% block questionsScript %}
    let listOfQuestionsId = [];

    {% for question in quiz.questions %}
        listOfQuestionsId.push({{question.id}});
    {% endfor %}

    function addQuestion(){
        if($("#question-to-add").val() && $("#question-to-add").val().length <= 100){
            let idToAdd = 1;
            if(listOfQuestionsId.length > 0) idToAdd = listOfQuestionsId[listOfQuestionsId.length - 1] + 1;
            listOfQuestionsId.push(idToAdd);
            $.ajax({
                url: "/add-question",
                type: "post",
                contentType: "application/json",
                data: JSON.stringify({
                    "quizId": "{{quiz.id}}",
                    "name": $("#question-to-add").val(),
                    "passwordToSubmit": "{{passwordToSubmit}}"
                })
            });
            $("#all-questions").append(`
                <li id="question` + idToAdd + `">
                    <div class="input-group mt-2">
                        <input type="text" id="question-input` + idToAdd + `" class="form-control border-top-0 border-start-0" value="` + $("#question-to-add").val() + `" onchange="updateQuestion(` + idToAdd + `)" maxlength="100" spellcheck="false" autocomplete="off">
                        <button class="btn btn-sm btn-secondary" onclick="removeQuestion(` + idToAdd + `)">
                            <i class="fas fa-minus"></i>
                        </button>
                    </div>
                    <div class="input-group input-group-sm answer-to-add">
                        <input type="text" id="answer-to-add` + idToAdd + `" class="form-control border-top-0 border-start-0" placeholder="Add answer" maxlength="50" spellcheck="false" autocomplete="off">
                        <button class="btn btn-sm btn-secondary" onclick="addAnswer(` + idToAdd + `)">
                            <i class="fas fa-plus"></i>
                        </button>
                    </div>
                    <div id="answers` + idToAdd + `" class="answers"></div>
                </li>`
            );
            $("#question-to-add").val("");
            $("#question-to-add").focus();
        }
    }

    function removeQuestion(questionId){
        listOfQuestionsId.splice(listOfQuestionsId.indexOf(questionId), 1);
        $.ajax({
            url: "/remove-question",
            type: "post",
            contentType: "application/json",
            data: JSON.stringify({
                "quizId": "{{quiz.id}}",
                "questionId": questionId,
                "passwordToSubmit": "{{passwordToSubmit}}"
            })
        });
        $("#question" + questionId).remove();
    }

    function updateQuestion(questionId){
        if($("#question-input" + questionId).val() && $("#question-input" + questionId).val().length <= 100){
            $.ajax({
                url: "/update-question",
                type: "post",
                contentType: "application/json",
                data: JSON.stringify({
                    "quizId": "{{quiz.id}}",
                    "questionId": questionId,
                    "name": $("#question-input" + questionId).val(),
                    "passwordToSubmit": "{{passwordToSubmit}}"
                })
            });
        }
    }
{% endblock %}
