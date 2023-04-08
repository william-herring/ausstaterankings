from flask import Flask, render_template, request, session
import os
import requests

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


def get_user_data():
    try:
        token = session["token"]
        user_data = requests.get('https://www.worldcubeassociation.org/api/v0/me',
                                 headers={'Authorization': f'Bearer {token}'}).json()['me']
    except KeyError:
        user_data = {}

    return user_data


@app.route('/')
def index():
    return render_template('index.html', **get_user_data())


@app.route('/faq')
def faq():
    return render_template('faq.html', **get_user_data())


@app.route('/preferences')
def preferences():
    return render_template('preferences.html', **get_user_data())


@app.route('/account-redirect')
def account_redirect():
    code = request.args.get('code')
    print(request.args.get('redirectUrl'))
    token = requests.post('https://www.worldcubeassociation.org/oauth/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),
        'redirect_uri': 'http://localhost:5000/account-redirect?redirectUrl=' + request.args.get('redirectUrl')
    }).json()['access_token']
    session['token'] = token
    return render_template('account-redirect.html', token=token)
