from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "hush"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route("/")
def survey_start():
    return render_template("survey_start.html", survey=survey)

@app.route("/begin", methods=["POST"])
def start():
    session[RESPONSES_KEY] = []
    return redirect("/questions/0")

@app.route("/questions/<int:qid>")
def show_question(qid):
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect("/")
    if (len(responses)== len(survey.questions)):
        return redirect("/complete")
    if (len(responses) != qid):
        flash(f"Invalid")
        return redirect(f"/questions/{len(responses)}")
    
    question = survey.questions[qid]
    return render_template(
        "question.html", question_num=qid, question=question)

@app.route("/answer", methods=["POST"])
def answers():
    choice = request.form['answer']
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses 
    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    else: 
        return redirect(f"/questions/{len(responses)}")
    
@app.route("/complete")
def complete():
    return render_template("completion.html")