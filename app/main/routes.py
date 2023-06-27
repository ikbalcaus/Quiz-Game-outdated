from flask import render_template, redirect, request, flash
from . import app, db
from .tables import Quizzes, Results
from datetime import datetime
from re import fullmatch

@app.route("/")
def indexRoute():
	if request.args.get("quiz"):
		quizzes = Quizzes.query.filter(Quizzes.name.contains(request.args.get("quiz"))).order_by(Quizzes.date.desc()).all()
	else:
		quizzes = Quizzes.query.order_by(Quizzes.date.desc()).all()
	return render_template("index.html",
		quizzes = quizzes
	)

@app.route("/info/<name>")
def infoRoute(name):
	if Quizzes.query.filter_by(name = name).first():
		return render_template("info.html",
			quiz = Quizzes.query.filter_by(name = name).first()
		)
	return redirect("/")

@app.route("/quiz/<name>", methods = ("GET", "POST"))
def quizRoute(name):
	if request.method == "POST":
		quiz = Quizzes.query.filter_by(name = name).first()
		if quiz.numberOfQuestions == 0:
			flash("Quiz cannot be stared. It does not have any question!")
			return redirect("/info/" + name)
		if request.form.get("nickname") and len(request.form.get("nickname")) <= 30:
			return render_template("quiz.html",
				quiz = quiz,
				nickname = request.form.get("nickname").strip()
			)
	return redirect("/info/" + name)

@app.route("/result/<name>", methods = ("GET", "POST"))
def resultRoute(name):
	if request.method == "POST":
		nickname = request.form.get("nickname")
		quiz = Quizzes.query.filter_by(name = name).first()
		countCorrect = 0
		for question in quiz.questions:
			if sorted([int(answer.id) for answer in question.answers if answer.isCorrect == 1]) == sorted([int(answerId) for answerId in request.form.getlist("answers" + str(question.id))]):
				countCorrect += 1
		correctAnswers = str(countCorrect) + "/" + str(quiz.numberOfQuestions)
		score = countCorrect / quiz.numberOfQuestions * 100
		db.session.add(Results(
			quizId = quiz.id,
			nickname = nickname,
			score = score,
			correctAnswers = correctAnswers,
			duration = request.form.get("duration"),
			date = datetime.now().strftime("%d.%m.%Y  %H:%M")
		))
		db.session.commit()
		return render_template("result.html",
			nickname = nickname,
			quiz = quiz,
			score = score,
			correctAnswers = correctAnswers
		)
	return redirect("/info/" + name)

@app.route("/results/<name>")
def resultsRoute(name):
	if Quizzes.query.filter_by(name = name).first():
		return render_template("results.html",
			quiz = Quizzes.query.filter_by(name = name).first()
		)
	return redirect("/")

@app.route("/make", methods = ("GET", "POST"))
def makeRoute():
	regex = "([A-Za-z1-9]|_){1,30}"
	if request.method == "POST":
		name = request.form.get("name").strip().capitalize().replace(" ", "_")
		if Quizzes.query.filter_by(name = name).first():
			flash("Changes are not saved. Quiz name must be unique!")
			return redirect("/make")
		if(
			not fullmatch(regex, request.form.get("name")) or
			len(request.form.get("description")) > 100 or
			len(request.form.get("duration")) == 0 or
			int(request.form.get("duration")) < 1 or int(request.form.get("duration")) > 60 or
			len(request.form.get("password")) > 30
		):
			flash("Changes are not saved. Data do not match validation rules!")
			return redirect("/make")
		db.session.add(Quizzes(
			name = name,
			description = request.form.get("description").strip(),
			numberOfQuestions = 0,
			duration = request.form.get("duration"),
			password = request.form.get("password"),
			color = request.form.get("color"),
			date = datetime.utcnow()
		))
		db.session.commit()
		return redirect("/edit/" + name)
	return render_template("make-edit.html",
		regex = regex
	)

@app.route("/edit/<oldName>", methods = ("GET", "POST"))
def editRoute(oldName):
	regex = "([A-Za-z1-9]|_){1,30}"
	if(
		request.method == "POST" and
		request.form.get("passwordToSubmit") == Quizzes.query.filter_by(name = oldName).first().password
	):
		newName = request.form.get("name").strip().capitalize().replace(" ", "_")
		if(
			Quizzes.query.filter_by(name = newName).first() and
			not Quizzes.query.filter_by(name = oldName).first().name == newName
		):
			flash("Changes are not saved. Quiz name must be unique!")
			return redirect("/info/" + oldName)
		if(
			not fullmatch(regex, request.form.get("name")) or
			len(request.form.get("description")) > 100 or
			len(request.form.get("duration")) == 0 or
			int(request.form.get("duration")) < 1 or int(request.form.get("duration")) > 60 or
			len(request.form.get("password")) > 30
		):
			flash("Changes are not saved. Data do not match validation rules!")
			return redirect("/info/" + oldName)
		quiz = Quizzes.query.filter_by(name = oldName).first()
		quiz.name = newName
		quiz.description = request.form.get("description").strip()
		quiz.duration = request.form.get("duration")
		quiz.password = request.form.get("password")
		quiz.color = request.form.get("color")
		quiz.date = datetime.utcnow()
		db.session.commit()
		return redirect("/info/" + newName)
	if(
		request.method == "POST" and
		request.form.get("passwordToContinue") == Quizzes.query.filter_by(name = oldName).first().password
	):
		return render_template("make-edit.html",
			quiz = Quizzes.query.filter_by(name = oldName).first(),
			passwordToSubmit = request.form.get("passwordToContinue"),
			regex = "([A-Za-z1-9]|_){1,30}"
		)
	if Quizzes.query.filter_by(name = oldName).first():
		return render_template("password.html",
			quiz = Quizzes.query.filter_by(name = oldName).first(),
			action = "edit"
		)
	return redirect("/")


@app.route("/delete/<name>", methods = ("GET", "POST"))
def deleteRoute(name):
	if(
		request.method == "POST" and
		request.form.get("passwordToContinue") == Quizzes.query.filter_by(name = name).first().password
	):
		db.session.delete(Quizzes.query.filter_by(name = name).first())
		db.session.commit()
		return redirect("/")
	return render_template("password.html",
		quiz = Quizzes.query.filter_by(name = name).first(),
		action = "delete"
	)