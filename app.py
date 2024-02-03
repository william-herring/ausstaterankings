from flask import Flask, render_template, request, session, jsonify, copy_current_request_context
import os
import requests
from threading import Thread
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Person, Result
from manual_entry import add_user
from update_results import update_results


with app.app_context():
    db.create_all()
    db.session.commit()

admins = ['2019HERR14', '2018NGHA02', '2019LUCA01', '2016CULF01', '2022FETH01', '2021OTSU01', '2022CUIA01']


@app.route('/')
def index():
    event = request.args.get('event')
    state = request.args.get('state')
    result_type = request.args.get('result_type')

    if state is None:
        state = 'nsw'
    if event is None:
        event = '333'
    if result_type is None:
        result_type = 'single'

    if result_type == 'average':
        results = Result.query.filter(Result.event == event, Result.person.has(state=state), Result.average.isnot(None)).order_by(Result.average_rank.asc()).limit(100)
    else:
        results = Result.query.filter(Result.event == event, Result.person.has(state=state), Result.single.isnot(None)).order_by(Result.single_rank.asc()).limit(100)

    parsed_results = []

    if result_type == 'average':
        rank = 1
        for r in results:
            parsed_results.append({
                'rank': rank,
                'name': r.person.name,
                'wca_id': r.person.wca_id,
                'time': r.average
            })
            rank += 1
    else:
        rank = 1
        for r in results:
            parsed_results.append({
                'rank': rank,
                'name': r.person.name,
                'wca_id': r.person.wca_id,
                'time': r.single
            })
            rank += 1

    return render_template('index.html', rankings=parsed_results, state=state)


@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/person/<wca_id>')
def profile(wca_id):
    person = Person.query.filter(Person.wca_id == wca_id).first()
    is_admin = person.wca_id in admins
    rankings = {}
    for r in person.results:
        if r.average is not None:
            average_rank = Result.query.filter(Result.event == r.event, Result.person.has(state=person.state), Result.average.isnot(None)).order_by(Result.average_rank.asc()).all().index(r)
        else:
            average_rank = 0
        single_rank = Result.query.filter(Result.event == r.event, Result.person.has(state=person.state), Result.single.isnot(None)).order_by(Result.single_rank.asc()).all().index(r)

        rankings[r.event] = (single_rank + 1, average_rank + 1)

    return render_template('profile.html', person=person, is_admin=is_admin, rankings=rankings)

@app.route('/preferences')
def preferences():
    state = None
    if session['user']['wca_id'] is not None:
        state = Person.query.filter(Person.wca_id == session['user']['wca_id']).first().state
    return render_template('preferences.html', state=state)


@app.route('/update-prefs', methods=['POST'])
def update_preferences():
    person = Person.query.filter(Person.wca_id == session['user']['wca_id']).first()
    person.state = request.json['state']
    db.session.commit()
    return f"Preferences updated for user {person.wca_id}", 200


@app.route('/account-redirect')
def account_redirect():
    code = request.args.get('code')
    token = requests.post('https://www.worldcubeassociation.org/oauth/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),
        'redirect_uri': request.base_url + '?redirectUrl=' + request.args.get('redirectUrl')
    }).json()['access_token']
    session['token'] = token
    user_data = requests.get('https://www.worldcubeassociation.org/api/v0/me',
                             headers={'Authorization': f'Bearer {token}'}).json()['me']

    if db.session.query(Person).filter(Person.wca_id == user_data['wca_id']).first() is None and user_data['wca_id'] is not None:
        last_competition = requests.get(f'https://www.worldcubeassociation.org/api/v0/persons/{user_data["wca_id"]}/competitions').json()[-1]
        user = Person(
            name=user_data['name'],
            wca_id=user_data['wca_id'],
            avatar=user_data['avatar']['thumb_url'],
            country=user_data['country']['iso2'],
            last_competition=last_competition['id']
        )
        db.session.add(user)
        db.session.commit()

        raw_results = requests.get(f'https://www.worldcubeassociation.org/api/v0/persons/{user_data["wca_id"]}').json()[
            'personal_records']
        results = []
        for r in raw_results.keys():
            if r == '333mbf':
                continue

            try:
                single = raw_results[r]['single']['best']
            except KeyError:
                single = None
            try:
                average = raw_results[r]['average']['best']
            except KeyError:
                average = None

            # Validate that user has single/average results (not DNF)
            if single is not None and average is not None:
                result = Result(
                    event=r,
                    single=single,
                    average=average,
                    single_rank=raw_results[r]['single']['world_rank'],
                    average_rank=raw_results[r]['average']['world_rank'],
                    person_id=user.id
                )
            elif single is not None:
                result = Result(
                    event=r,
                    single=single,
                    single_rank=raw_results[r]['single']['world_rank'],
                    person_id=user.id
                )
            else:
                result = Result(
                    event=r,
                    average=average,
                    average_rank=raw_results[r]['average']['world_rank'],
                    person_id=user.id
                )

            results.append(result)

        user.results = results
        db.session.add(user)
        db.session.commit()

    session['user'] = {'name': user_data['name'], 'avatar': user_data['avatar']['thumb_url'], 'wca_id': user_data['wca_id'], 'country': user_data['country']['iso2']}
    return render_template('account-redirect.html')

@app.route('/kinch')
def kinch():
    return render_template('kinch.html')

@app.route('/manual-entry')
def manual_entry():
    if session['user']['wca_id'] in admins:
        wca_id = request.args.get('wca_id')
        state = request.args.get('state')

        if wca_id is not None and state is not None:
            req = add_user(wca_id, state)
            if req != 200:
                return req

        return render_template('manual-entry-interface.html')
    return 'Access forbidden', 403

@app.route('/update-results-manual')
def update_results_manual():
    if session['user']['wca_id'] in admins:
        people_updated = update_results()

        return render_template('manual-entry-interface.html', people=people_updated)
    return 'Access forbidden', 403

@app.route('/update-results')
def update_results_api():
    @copy_current_request_context
    def process():
        update_results()

    if request.args.get('key') == os.getenv('SCHEDULER_KEY'):
        Thread(target=process).start()

        return 'Started update', 200
    return 'Access forbidden', 403
