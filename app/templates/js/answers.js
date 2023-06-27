{% block answersScript %}
    let listOfAnswersId = [];

    {% for answer in quiz.answers %}
        listOfAnswersId.push({{answer.id}});
    {% endfor %}

    function addAnswer(questionId){
        if($("#answer-to-add" + questionId).val() && $("#answer-to-add" + questionId).val().length <= 50){
            let idToAdd = 1;
            if(listOfAnswersId.length > 0) idToAdd = listOfAnswersId[listOfAnswersId.length - 1] + 1;
            listOfAnswersId.push(idToAdd);
            $.ajax({
                url: "/add-answer",
                type: "post",
                contentType: "application/json",
                data: JSON.stringify({
                    "quizId": "{{quiz.id}}",
                    "questionId": questionId,
                    "name": $("#answer-to-add" + questionId).val(),
                    "passwordToSubmit": "{{passwordToSubmit}}"
                })
            });
            $("#answers" + questionId).append(`
                <div id="answer` + idToAdd + `" class="input-group input-group-sm answer">
                    <input type="checkbox" class="form-check-input" onclick="changeStateAnswer(` + idToAdd + `)">
                    <input type="text" id="answer-input` + idToAdd + `" class="form-control border-top-0 border-start-0" value=` + $("#answer-to-add" + questionId).val() + ` onchange="updateAnswer(` + idToAdd + `)"  maxlength="50" spellcheck="false" autocomplete="off">
                    <button class="btn btn-sm btn-secondary" onclick="removeAnswer(` + idToAdd + `)">
                        <i class="fas fa-minus"></i>
                    </button>
                </div>`
            );
            $("#answer-to-add" + questionId).val("");
            $("#answer-to-add" + questionId).focus();
        }
    }

    function removeAnswer(answerId){
        listOfAnswersId.splice(listOfAnswersId.indexOf(answerId), 1);
        $.ajax({
            url: "/remove-answer",
            type: "post",
            contentType: "application/json",
            data: JSON.stringify({
                "quizId": "{{quiz.id}}",
                "answerId": answerId,
                "passwordToSubmit": "{{passwordToSubmit}}"
            })
        });
        $("#answer" + answerId).remove();
    }

    function updateAnswer(answerId){
        if($("#answer-input" + answerId).val() && $("#answer-input" + answerId).val().length <= 50){
            $.ajax({
                url: "/update-answer",
                type: "post",
                contentType: "application/json",
                data: JSON.stringify({
                    "quizId": "{{quiz.id}}",
                    "answerId": answerId,
                    "name": $("#answer-input" + answerId).val(),
                    "passwordToSubmit": "{{passwordToSubmit}}"
                })
            });
        }
    }

    function changeStateAnswer(answerId){
        $.ajax({
            url: "/change-state-answer",
            type: "post",
            contentType: "application/json",
            data: JSON.stringify({
                "quizId": "{{quiz.id}}",
                "answerId": answerId,
                "passwordToSubmit": "{{passwordToSubmit}}"
            })
        });
    }
{% endblock %}