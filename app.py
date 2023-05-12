from flask import Flask, request, render_template, session
from flask_session import Session  # セッション情報の管理
import openai
import os
import random

# OpenAIのAPIキーを設定
openai.api_key = os.getenv("OPENAI_API_KEY")

# FlaskとFlask-Sessionの設定
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    playing = False
    surrender = False
    if request.method == 'POST':
        if "play" in request.form:
            # ... (省略) ...
            playing = True
        elif "surrender" in request.form:
            if 'topic' in session:
                surrender = True
                return render_template('index.html', message="答えは" + session['topic'] + "でした", answer=session['topic'], surrender=surrender)
            else:
                return render_template('index.html', message="まずPlayを押してください")
        elif "question" in request.form:
            if 'topic' in session:
                # ... (省略) ...
                playing = True
            else:
                return render_template('index.html', message="まずPlayを押してください")
    else:
        return render_template('index.html', message="Playを押してください")

    return render_template('index.html', message=message, playing=playing)

if __name__ == '__main__':
    app.run(debug=True)
