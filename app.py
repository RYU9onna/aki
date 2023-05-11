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
            chat = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "system", "content": "あなたは私の20問ゲームの対戦相手です。今から1つの道具、家電、物体、食べ物、生き物、日本の有名人などから名前だけを考えてください。その名前だけ返事してください。"}, {"role": "user", "content": "名前を１つ決めてください。その名前だけ返事してください。"}], temperature=1.0)
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
                # ユーザーが直接答えを推測した場合
                if question == session['topic']:
                    return render_template('index.html', message=f"正解です！答えは {session['topic']} でした！", answer=session['topic'])
                # GPT-4に質問を評価させる
                chat = openai.ChatCompletion.create(model="gpt-3.5-turbo-0301", messages=[
                    {"role": "system", "content": "あなたは私の20問ゲームの対戦相手です。「はい」「少しそう」「どちらでもない」「違います」「少し違う」のいずれかだけで返事をします。"},
                    {"role": "user", "content": f'あなたは答えに"{session["topic"]}"を選んでいます。私は答えに対して"{question}"と質問しました。'}
                ])
                answer = chat['choices'][0]['message']['content']
                return render_template('index.html', message=answer)
            else:
                return render_template('index.html', message="まずPlayを押してください")
    else:
        return render_template('index.html', message="Playを押してください")

if __name__ == '__main__':
    app.run(debug=True)
