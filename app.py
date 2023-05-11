from flask import Flask, request, render_template, session
from flask_session import Session
import os
import random
import spacy

# Flask and Flask-Session configuration
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = os.path.join(os.getcwd(), 'flask_session')
Session(app)

# Topics and responses
topics = ["ラーメン", "東京タワー", "ハリーポッター", "スズメ", "ビートルズ", "サッカー", "ビートルズ", "チョコレート", "ピアノ", "エッフェル塔"]

# Load the natural language understanding model
nlp = spacy.load('en_core_web_sm')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if "play" in request.form:
            session['topic'] = random.choice(topics)
            return render_template('index.html', message="私が考えているのは何でしょう？質問して当ててみて")
        elif "question" in request.form:
            if 'topic' in session:
                question = request.form['question']
                # Check if the user has guessed the topic
                if question == session['topic']:
                    return render_template('index.html', message="正解です！私が考えていたのは" + session['topic'] + "でした！", answer=session['topic'])
                else:
                    # Use natural language understanding to determine if the question is related to the topic
                    doc = nlp(question)
                    if session['topic'] in [token.lemma_ for token in doc]:
                        return render_template('index.html', message="はい")
                    else:
                        return render_template('index.html', message="いいえ")
            else:
                return render_template('index.html', message="まずPlayを押してください")
    else:
        return render_template('index.html', message="Playを押してください")

if __name__ == '__main__':
    app.run(debug=True)
