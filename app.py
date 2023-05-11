@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if "play" in request.form:
            # GPT-3にトピックを考えさせる
            chat = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "system", "content": "あなたは私の20問ゲームの対戦相手です。今から1つの答えを考えてください。"}, {"role": "user", "content": "20問ゲームにあう答えを１つ決めてください。"}])
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
                # GPT-4に質問を評価させる
                chat = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "system", "content": "あなたは私の20問ゲームの対戦相手です。「はい」「少しそう」「どちらでもない」「違います」「少し違う」のいずれかだけで返事をします。"}, {"role": "user", "content": f'答えは"{session["topic"]}"です。私は答えに対して"{question}"と質問しました。質問に対する最も適切な返事をしてください。'}])
                answer = chat['choices'][0]['message']['content']
                return render_template('index.html', message=answer)
            else:
                return render_template('index.html', message="まずPlayを押してください")
    else:
        return render_template('index.html', message="Playを押してください")

if __name__ == '__main__':
    app.run(debug=True)
