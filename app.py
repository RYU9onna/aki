from flask import Flask, request, render_template, session
import openai
import os
import random

app = Flask(__name__)
app.secret_key = os.urandom(24)

openai.api_key = os.getenv("OPENAI_API_KEY")

topics = ["ラーメン", "東京タワー", "ハリーポッター", "スズメ", "ビートルズ", "サッカー", "ビートルズ", "チョコレート", "ピアノ", "エッフェル塔"]
responses = {
    "はい": ["はい", "その通りです", "間違いありません"],
    "いいえ": ["いいえ", "違います", "そうではありません"],
    "どちらともいえない": ["どちらともいえない", "一概には言えません", "その質問は答えにくいです"]
}

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if "play" in request.form:
            session['topic'] = random.choice(topics)
            return render_template('index.html', message="私が考えているのは何でしょう？質問して当ててみて")
        elif "question" in request.form:
            question = request.form['question']
            answer = openai.Completion.create(engine="text-davinci-002", prompt=f"この文は{session['topic']}についてのものですか？ {question}", max_tokens=1).choices[0].text.strip()
            return render_template('index.html', message=random.choice(responses[answer]), answer=session['topic'] if answer == "はい" else "")
    else:
        return render_template('index.html', message="Playを押してください")

if __name__ == '__main__':
    app.run(debug=True)
