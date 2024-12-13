from flask import Flask, render_template, session, request, redirect, url_for
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'


# Helper function to load quiz data from JSON
def load_quiz_data(filename):
    try:
        with open(f'questions/{filename}', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return None


# Route: Homepage
@app.route('/')
def home():
    return render_template('home.html')


# Route: About Us
@app.route('/about')
def about():
    return render_template('about_us.html')


# Route: Contact Us
@app.route('/contact')
def contact():
    return render_template('contact_us.html')


# Route: Players Category
@app.route('/players')
def players():
    return render_template('player.html')


# Route: League Category
@app.route('/league')
def league():
    return render_template('league.html')


# Route: Competition Category
@app.route('/competition')
def competition():
    return render_template('competition.html')


# Route: Quiz Page
@app.route('/quiz/<quiz_name>')
def quiz(quiz_name):

    filename = f"{quiz_name}.json"
    quiz_data = load_quiz_data(filename)
    if not quiz_data or 'questions' not in quiz_data:
        return "Quiz not found or improperly formatted", 404

    # Initialize session variables
    session['questions'] = quiz_data['questions']
    session['quiz_name'] = quiz_name
    session['score'] = 0
    session['current_question'] = 0

    return render_template('quiz.html', question=quiz_data['questions'][0], current=0, total=len(quiz_data['questions']))


# Route: Process Quiz Submission
@app.route('/quiz_submit', methods=['POST'])
def quiz_submit():
    if 'questions' not in session or 'current_question' not in session:
        return redirect(url_for('home'))

    questions = session['questions']
    current_index = session['current_question']

    selected = request.form.get('answer')
    correct_answer = questions[current_index]['correct']

    # Update score if answer is correct
    if selected and selected == correct_answer:
        session['score'] += 1

    session['current_question'] += 1

    # Check if it's the last question
    if session['current_question'] >= len(questions):
        return redirect(url_for('result'))

    # Otherwise, load the next question
    return render_template(
        'quiz.html',
        question=questions[session['current_question']],
        current=session['current_question'],
        total=len(questions)
    )


# Route: Quiz Result
@app.route('/result')
def result():
    score = session.get('score', 0)
    total = len(session.get('questions', []))
    return render_template('result.html', score=score, total=total)


# Route: Reset Quiz
@app.route('/reset_quiz', methods=['POST'])
def reset_quiz():
    session.pop('questions', None)
    session.pop('current_question', None)
    session.pop('score', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
