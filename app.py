from flask import Flask, request, render_template, session
from flask_session import Session  # セッション情報の管理
from openai import ChatCompletion, set_openai_key  # OpenAIのGPT-3を使用するためのライブラリ
import os
import random

# OpenAIのAPIキーを設定
set_openai_key('your_openai_key_here')

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
            chat = ChatCompletion.create(model="text-davinci-003", messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Please think of a topic for a game of 20 questions."}])
            session['topic'] = chat['choices'][0]['message']['content']
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
                chat = ChatCompletion.create(model="text-davinci-003", messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": f'The user is trying to guess a topic. They asked: "{question}". The topic is: "{session["topic"]}". Does their question apply to the topic?'}])
                answer = chat['choices'][0]['message']['content']
                return render_template('index.html', message=answer)
            else:
                return render_template('index.html', message="まずPlayを押してください")
    else:
        return render_template('index.html', message="Playを押してください")

if __name__ == '__main__':
    app.run(debug=True)
