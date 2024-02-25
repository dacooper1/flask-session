from flask import Flask, render_template, request, redirect,  session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = "soccer"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route('/')
def home():
    session['answers'] = []
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('home.html', title=title, instructions=instructions)

@app.route('/start_survey', methods= ['POST'])
def begin():
    return redirect('/questions/0')

@app.route('/answers', methods=['POST'])
def handle_answers():
    survey_answer = request.form['answer']
    responses = session['answers']
    responses.append(survey_answer)
    session['answers'] = responses
    
    if len(satisfaction_survey.questions) != len(session['answers']):
        return redirect(f'/questions/{len(session['answers'])}')
    else:
        return render_template('/thank-you.html')

@app.route('/questions/<int:current_num>')
def questions(current_num):
    current_question = satisfaction_survey.questions[current_num]
    question_num = len(session['answers'])
    if session['answers'] is None:
        return redirect('/')
    if len(satisfaction_survey.questions) == len(session['answers']):
        return redirect('/thank-you.html')
    if current_num != len(session['answers']):
        flash("Please answer in order.")
        return redirect(f'/questions/{len(session['answers'])}')
    else:
        return render_template('questions.html', current_question = current_question, num = question_num)

