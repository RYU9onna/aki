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
    if request.method == 'POST':
        if "play" in request.form:
            # GPT-3にトピックを考えさせる
            response = openai.Completion.create(engine="text-davinci-003", prompt="Please think of a topic for a game of 20 questions.", max_tokens=60)
            session['topic'] = response.choices[0].text.strip()
            return render_template('index.html', message="私が考えているのは何でしょう？質問して当ててみて")
        elif "surrender" in request.form:
            if 'topic' in session:
                return render_template('index.html', message="答えは" + session['topic'] + "でした", answer=session['topic'])
            else:
                return render_template('index.html', message="まずPlayを押してください")
        elif "question" in request.form:
            if 'topic' in session:
                question = request.form['question']
                # GPT-3に質問を評価させる
                response = openai.Completion.create(engine="text-davinci-003", prompt=f'The user is trying to guess a topic. They asked: "{question}". The topic is: "{session["topic"]}". Does their question apply to the topic?', max_tokens=60)
                answer = response.choices[0].text.strip()
                return render_template('index.html', message=answer)
            else:
                return render_template('index.html', message="まずPlayを押してください")
    else:
        return render_template('index.html', message="Playを押してください")

if __name__ == '__main__':
    app.run(debug=True)
