from flask import Flask, request, render_template, session
from flask_session import Session  # セッション情報の管理
from textblob import TextBlob  # 自然言語理解のライブラリ
import os
import random

# FlaskとFlask-Sessionの設定
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# トピックと応答
topics = {
    "ラーメン": {"size": "small", "type": "food"},
    "東京タワー": {"size": "big", "type": "building"},
    "ハリーポッター": {"size": "medium", "type": "person"},
    "スズメ": {"size": "small", "type": "animal"},
    "ビートルズ": {"size": "medium", "type": "group"},
    "サッカー": {"size": "big", "type": "sport"},
    "チョコレート": {"size": "small", "type": "food"},
    "ピアノ": {"size": "big", "type": "instrument"},
    "エッフェル塔": {"size": "big", "type": "building"}
}

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if "play" in request.form:
            session['topic'] = random.choice(list(topics.keys()))
            return render_template('index.html', message="私が考えているのは何でしょう？質問して当ててみて")
        elif "surrender" in request.form:
            if 'topic' in session:
                return render_template('index.html', message="答えは" + session['topic'] + "でした", answer=session['topic'])
            else:
                return render_template('index.html', message="まずPlayを押してください")
        elif "question" in request.form:
            if 'topic' in session:
                question = request.form['question']
                # Check if the user has guessed the topic
                if question == session['topic']:
                    return render_template('index.html', message="正解です！私が考えていたのは" + session['topic'] + "でした！", answer=session['topic'])
                else:
                    # 自然言語理解を使用して、質問がトピックに関連しているかどうかを判断します
                    blob = TextBlob(question)
                    if "大きい" in blob.words:
                        if topics[session['topic']]['size'] == "big":
                            return render_template('index.html', message="はい")
                        else:
                            return render_template('index.html', message="いいえ")
                    elif "小さい" in blob.words:
                        if topics[session['topic']]['size'] == "small":
                            return render_template('index.html', message="はい")
                        else:
                            return render_template('index.html', message="いいえ")
                    else:
                        if session['topic'] in [word.lemma for word in blob.words]:
                            return render_template('index.html', message="はい")
                        else:
                            return render_template('index.html', message="いいえ")
            else:
                return render_template('index.html', message="まずPlayを押してください")
    else:
        return render_template('index.html', message="Playを押してください")

if __name__ == '__main__':
    app.run(debug=True)
