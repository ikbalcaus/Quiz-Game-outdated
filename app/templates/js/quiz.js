{% block quizScript %}
    setInterval(() => {
        $("#duration").val(parseInt($("#duration").val()) + 1);
    }, 60000);

    setTimeout(() => {
        $("#btn-submit").click();
    }, {{quiz.duration}} * 60000);
{% endblock %}