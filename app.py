from flask import Flask, render_template, request
import os
import requests
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.route('/preferences')
def preferences():
    code = request.args.get('code')
    token = requests.post('https://www.worldcubeassociation.org/oauth/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),
        'redirect_uri': 'http://localhost:5000/preferences'
    }).json()['access_token']
    print(token)
    return render_template('preferences.html', token=token)
