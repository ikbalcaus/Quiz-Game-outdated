from . import db
from datetime import datetime

class Quizzes(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(30), nullable = False, unique = True)
	description = db.Column(db.String(100))
	numberOfQuestions = db.Column(db.Integer, nullable = False)
	duration = db.Column(db.Integer)
	password = db.Column(db.String(30))
	color = db.Column(db.String(7), nullable = False)
	date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow())
	results = db.relationship("Results", backref = "quizzes", cascade = "all,delete")
	questions = db.relationship("Questions", backref = "quizzes", cascade = "all,delete")
	answers = db.relationship("Answers", backref = "quizzes", cascade = "all,delete")

class Results(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	quizId = db.Column(db.Integer, db.ForeignKey("quizzes.id"))
	nickname = db.Column(db.String(30), nullable = False)
	score = db.Column(db.Integer, nullable = False)
	correctAnswers = db.Column(db.String(10), nullable = False)
	date = db.Column(db.String(17), nullable = False)
	duration = db.Column(db.Integer, nullable = False)

class Questions(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	quizId = db.Column(db.Integer, db.ForeignKey("quizzes.id"))
	name = db.Column(db.String(100), nullable = False)
	answers = db.relationship("Answers", backref = "questions", cascade = "all,delete")

class Answers(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	quizId = db.Column(db.Integer, db.ForeignKey("quizzes.id"))
	questionId = db.Column(db.Integer, db.ForeignKey("questions.id"))
	name = db.Column(db.String(50), nullable = False)
	isCorrect = db.Column(db.Integer, nullable = False, default = 0)