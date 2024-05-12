from flask import Flask, jsonify, request, render_template
from openai import OpenAI
from dotenv import load_dotenv
import os
import time

load_dotenv()
API_KEY = os.environ['OPENAI_API_KEY']
client = OpenAI(api_key=API_KEY)

ASSISTANT_ID = os.environ['OPENAI_ASSISTANT_KEY']
app = Flask(__name__)

@app.route('/')
def main():
    thread = client.beta.threads.create()
    with open("thread.txt", "w") as file:
        file.write(thread.id)
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    
    return render_template('login.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data['question']
    
    if question == "안녕":
        answer = "안녕하세요!"
    elif question == "오늘 날씨는 어때?":
        answer = "오늘은 맑은 날씨예요."
    else:
        with open("thread.txt", "r") as file:
            THREAD_ID = file.read()
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