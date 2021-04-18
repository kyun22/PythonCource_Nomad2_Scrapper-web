from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
from exporter import save_to_file

app = Flask("Super Scrapper")

db = {}

@app.route("/")         # @: 데코레이터, 바로 아래 '함수'만 본다.
def home():
    return render_template('potato.html')

# @app.route("/<username>")       # <> : placeholder, 이걸 이용해서 다이나믹 url 사용 가능
# def potato(username):
#     return f"Contact me! {username}"

# @app.route("/report")
# def report():
#     word = request.args.get('word')
#     if word:
#         word = word.lower()
#     else:                       # word가 존재하지 않을 경우 redirect
#         return redirect("/")
#     return render_template('report.html',
#                            searching_by = word)    # html에 데이터를 넘기는 방법

@app.route("/report")
def report():
    word = request.args.get('word')
    if word:
        word = word.lower()
        existing_jobs = db.get(word)
        if existing_jobs:
            jobs = existing_jobs
        else:
            jobs = get_jobs(word)
            db[word] = jobs
    else:                       # word가 존재하지 않을 경우 redirect
        return redirect("/")
    return render_template('report.html', searching_by=word, resultsNum=len(jobs), jobs=jobs)    # html에 데이터를 넘기는 방법

@app.route("/export")
def export():
    try:
        word = request.args.get('word')
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_file(jobs)           # save to file first
        return send_file('jobs.csv')
    except:
        return redirect("/")



app.run(host="localhost")