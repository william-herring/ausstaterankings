from flask import Flask, render_template, request, session
import os
import requests
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Person, Result

with app.app_context():
    db.create_all()
    db.session.commit()


@app.route('/')
def index():
    persons = Person.query.all()
    return render_template('index.html', persons=persons)


@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.route('/preferences')
def preferences():
    return render_template('preferences.html')


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
    user_data = requests.get('https://www.worldcubeassociation.org/api/v0/me',
                             headers={'Authorization': f'Bearer {token}'}).json()['me']

    if db.session.query(Person).filter(Person.wca_id == user_data['wca_id']).first() is None and user_data['wca_id'] is not None:
        user = Person(
            name=user_data['name'],
            wca_id=user_data['wca_id'],
            avatar=user_data['avatar']['thumb_url'],
            country=user_data['country']['iso2'],
        )
        db.session.add(user)
        db.session.commit()

        raw_results = requests.get(f'https://www.worldcubeassociation.org/api/v0/persons/{user_data["wca_id"]}').json()[
            'personal_records']
        results = []
        for r in raw_results.keys():
            print(r['single']['best'])
            result = Result(
                event=r,
                single=r['single']['best'],
                average=r['average']['best'],
                single_rank=r['single']['world_rank'],
                average_rank=r['average']['world_rank'],
                person_id=user.id
            )
            results.append(result)

        user.results = results
        db.session.add(user)
        db.session.commit()
    session['user'] = {'name': user_data['name'], 'avatar': user_data['avatar']['thumb_url']}
    return render_template('account-redirect.html')
