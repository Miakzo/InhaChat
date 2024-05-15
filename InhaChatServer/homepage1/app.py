from flask import Flask, jsonify, request, render_template, url_for, redirect, session
from openai import OpenAI
from dotenv import load_dotenv
import os
import time
import pymysql
from flask_session import Session

conn, cur = None, None

def connect():
    return pymysql.connect(host='127.0.0.1', user='root', password='0000', db='user_threadDB.sql', charset='utf8')

load_dotenv()
API_KEY = os.environ['OPENAI_API_KEY']
client = OpenAI(api_key=API_KEY)

ASSISTANT_ID = os.environ['OPENAI_ASSISTANT_KEY']
app = Flask(__name__)
app.config['SECRET_KEY'] = '0000'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

THREAD_ID = None

# 메인 화면
@app.route('/main')
def main():
    thread = client.beta.threads.create()
    with open("thread.txt", "w") as file:
        file.write(thread.id)
    return render_template('index.html')

# 로그인 화면
@app.route('/login')
def login():
    return render_template('login.html')

# 로그인 정보 확인
@app.route('/check_login', methods=['POST'])
def login_check():
    data = request.json
    conn = connect()
    cur = conn.cursor()
    cur.execute(f"select thread_ID from chatbotuser where email='{data[0]['email']}' and password='{data[1]['password']}'")
    conn.commit()
    row = list(cur.fetchall())[0][0]
    print(row)
    session['thread_id'] = row
    conn.close()
    if row:
        return jsonify({'redirect': url_for('main')})
    else:
        return jsonify({'error': 'error'})

# 회원가입 창으로 이동
@app.route('/go_signUp', methods=['POST'])
def go_signUp():
    return jsonify({'redirect': url_for('signUp')})

# 회원가입 화면
@app.route('/signUp')
def signUp():
    return render_template('signUp.html')

# 회원가입
@app.route('/sign', methods=['POST'])
def sign():
    data = request.json
    name = data[0]['name']
    email = data[1]['email']
    password = data[2]['password']
    thread = client.beta.threads.create()
    print(thread)
    conn = connect()
    cur = conn.cursor()
    cur.execute(f"insert into chatbotuser values('{name}', '{email}', '{password}', '{thread.id}')")
    conn.commit()
    conn.close()
    return jsonify({'redirect': url_for('login')})

# 챗봇과 대화
@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data['question']
    
    if question == "안녕":
        answer = "안녕하세요!"
    elif question == "오늘 날씨는 어때?":
        answer = "오늘은 맑은 날씨예요."
    else:
        THREAD_ID = session.get('thread_id')
        print(THREAD_ID)
        client.beta.threads.messages.create(
            thread_id=THREAD_ID,
            role="user",
            content=question
        )
        run = client.beta.threads.runs.create(
            thread_id=THREAD_ID,
            assistant_id=ASSISTANT_ID
        )
        while run.status == "queued" or run.status == "in_progress":
            run = client.beta.threads.runs.retrieve(
                thread_id=THREAD_ID,
                run_id=run.id
            )
            time.sleep(0.5)
        messages = client.beta.threads.messages.list(
            thread_id=THREAD_ID,
            order="asc"
        )
        answer = messages.data[-1].content[0].text.value

    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)