from flask import request
from . import app, db
from .tables import Quizzes, Questions, Answers

@app.route("/add-question", methods = ["POST"])
def addQuestionRoute():
    quizId = request.json["quizId"]
    if request.json["passwordToSubmit"] == Quizzes.query.filter_by(id = quizId).first().password:
        db.session.add(Questions(
            quizId = quizId,
            name = request.json["name"].strip()
        ))
        Quizzes.query.filter_by(id = quizId).first().numberOfQuestions += 1
        db.session.commit()
    return ""

@app.route("/remove-question", methods = ["POST"])
def removeQuestionRoute():
    quizId = request.json["quizId"]
    if request.json["passwordToSubmit"] == Quizzes.query.filter_by(id = quizId).first().password:
        db.session.delete(Questions.query.filter_by(
            quizId = quizId,
            id = request.json["questionId"]
        ).first())
        Quizzes.query.filter_by(id = quizId).first().numberOfQuestions -= 1
        db.session.commit()
    return ""

@app.route("/update-question", methods = ["POST"])
def updateQuestionRoute():
    quizId = request.json["quizId"]
    if request.json["passwordToSubmit"] == Quizzes.query.filter_by(id = quizId).first().password:
        question = Questions.query.filter_by(id = request.json["questionId"]).first()
        question.name = request.json["name"]
        db.session.commit()
    return ""


@app.route("/add-answer", methods = ["POST"])
def addAnswerRoute():
    quizId = request.json["quizId"]
    if request.json["passwordToSubmit"] == Quizzes.query.filter_by(id = quizId).first().password:
        db.session.add(Answers(
            quizId = quizId,
            questionId = request.json["questionId"],
            name = request.json["name"].strip()
    ))
    db.session.commit()
    return ""

@app.route("/remove-answer", methods = ["POST"])
def removeAnswerRoute():
    quizId = request.json["quizId"]
    if request.json["passwordToSubmit"] == Quizzes.query.filter_by(id = quizId).first().password:
        db.session.delete(Answers.query.filter_by(
            quizId = quizId,
            id = request.json["answerId"]
        ).first())
        db.session.commit()
    return ""

@app.route("/update-answer", methods = ["POST"])
def updateAnswerRoute():
    quizId = request.json["quizId"]
    if request.json["passwordToSubmit"] == Quizzes.query.filter_by(id = quizId).first().password:
        answer = Answers.query.filter_by(id = request.json["answerId"]).first()
        answer.name = request.json["name"]
        db.session.commit()
    return ""

@app.route("/change-state-answer", methods = ["POST"])
def changeStateAnswerRoute():
    quizId = request.json["quizId"]
    if request.json["passwordToSubmit"] == Quizzes.query.filter_by(id = quizId).first().password:
        answer = Answers.query.filter_by(id = request.json["answerId"]).first()
        answer.isCorrect = 1 if answer.isCorrect == 0 else 0
        db.session.commit()
    return ""
