from app import db


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    wca_id = db.Column(db.String(10), unique=True, nullable=True)
    avatar = db.Column(db.String(300), nullable=False)
    country = db.Column(db.String(2), nullable=False)
    state = db.Column(db.String(30), nullable=True)
    results = db.Column(db.JSON)

    def __repr__(self):
        return f'<Person {self.wca_id}>'
