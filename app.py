from flask import Flask, request, session, render_template
import openai
import os
import random

app = Flask(__name__)
app.secret_key = os.urandom(24)  # セッションを安全に使用するための秘密鍵

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "play" in request.form:
            # 「Play」ボタンが押されたら新しいお題を生成
            session['theme'] = get_new_theme()
            session['message'] = "私が考えているのは何でしょう？質問して当ててみて"
        elif "question" in request.form:
            # 質問が送信されたら答えを生成
            question = request.form["question"]
            session['message'] = generate_answer(question, session['theme'])
    return render_template('index.html')  # HTML ファイルは適宜作成してください

def get_new_theme():
    openai.api_key = os.getenv('OPENAI_API_KEY')  # 環境変数からAPIキーを取得

    categories = ["有名人", "食べ物", "動物", "映画", "曲", "本"]
    category = random.choice(categories)

    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": "あなたは一つのテーマを考えるようになりました。"},
            {"role": "user", "content": f"{category}のお題を考えてください。"}
        ]
    )

    theme = response['choices'][0]['message']['content']
    return theme

def generate_answer(question, theme):
    openai.api_key = os.getenv('OPENAI_API_KEY')  # 環境変数からAPIキーを取得

    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": f"あなたが考えているお題は{theme}です。"},
            {"role": "user", "content": question}
        ]
    )

    answer = response['choices'][0]['message']['content']

    if theme in question:
        session['theme'] = None
        answer = f"正解です！私が考えていたのは{theme}です！"

    return answer

if __name__ == "__main__":
    app.run(debug=True)
