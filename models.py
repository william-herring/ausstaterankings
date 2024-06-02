from app import db


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    wca_id = db.Column(db.String(10), unique=True, nullable=True)
    avatar = db.Column(db.String(300), nullable=False)
    country = db.Column(db.String(2), nullable=False)
    state = db.Column(db.String(30), nullable=True)
    last_competition = db.Column(db.String(200), nullable=True)
    results = db.relationship('Result', backref='person', lazy=True)

    def __repr__(self):
        return f'<Person {self.wca_id}>'


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    event = db.Column(db.String(5), nullable=False)
    single = db.Column(db.Float)
    average = db.Column(db.Float)
    single_rank = db.Column(db.Integer)
    average_rank = db.Column(db.Integer)

    def __repr__(self):
        return f'<Result {self.event} Person {self.person_id}>'


class KinchRank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(30), nullable=False)
    k_333 = db.Column(db.Float)
    k_222 = db.Column(db.Float)
    k_444 = db.Column(db.Float)
    k_555 = db.Column(db.Float)
    k_666 = db.Column(db.Float)
    k_777 = db.Column(db.Float)
    k_333bf = db.Column(db.Float)
    k_333fm = db.Column(db.Float)
    k_333oh = db.Column(db.Float)
    k_clock = db.Column(db.Float)
    k_minx = db.Column(db.Float)
    k_pyram = db.Column(db.Float)
    k_skewb = db.Column(db.Float)
    k_sq1 = db.Column(db.Float)
    k_444bf = db.Column(db.Float)
    k_555bf = db.Column(db.Float)
