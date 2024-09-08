import os
from flask import Flask, render_template, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, time

app = Flask(__name__)

# Store votes in memory (replace with database in production)
votes = []

def reset_votes():
    global votes
    votes = []
    print("Votes have been reset.")

# Schedule the reset_votes function to run daily at 11:59 PM
scheduler = BackgroundScheduler()
scheduler.add_job(reset_votes, 'cron', hour=23, minute=59)
scheduler.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    votes.append(data)
    return jsonify({"message": "تم تسجيل الصوت", "all_votes": votes})

@app.route('/results')
def results():
    return jsonify(votes)

@app.route('/reset', methods=['POST'])
def manual_reset():
    global votes
    votes = []
    return jsonify({"message": "تمت إعادة تعيين الأصوات يدويًا"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
