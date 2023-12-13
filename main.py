from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
app.secret_key = 'auraa'
 


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/account')
def account():
    return render_template('account.html')


@app.route('/browse-resume')
def browse_res():
    return render_template('browse-resumes.html')


if __name__ == '__main__':
    app.run(debug=True)
