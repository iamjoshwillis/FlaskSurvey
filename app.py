from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config["SECRET_KEY"] = "2468"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

RESPONSES = "responses"


@app.route("/")
def title():
    return render_template("title.html", survey=survey)


@app.route("/start", methods=["POST"])
def start_survey():
    session[RESPONSES] = []
    return redirect("/questions/0")


@app.route("/answer", methods=["POST"])
def store_answer():
    choice = request.form["answer"]

    responses = session[RESPONSES]
    responses.append(choice)
    session[RESPONSES] = responses

    if len(responses) == len(survey.questions):
        return redirect("/thankyou")
    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/questions/<int:qnum>")
def question_display(qnum):
    responses = session[RESPONSES]

    if (responses is None):
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        return redirect("/thankyou")

    if (len(responses) != qnum):
        flash(f"Error with Question Number")
        return redirect(f"/questions/{len(responses)}")

    questions = survey.questions[qnum]
    return render_template("question-0.html", question_num=qnum, survey=survey, questions=questions)


@app.route("/thankyou")
def thankyou_page():
    return render_template("thankyou.html")
