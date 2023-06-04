"""
This is a scheduled function to be executed every Wednesday.
The purpose of this utility is to keep the results of every user up to date.
It can also be used to manually update results.
"""
import requests
from models import Person, Result
from app import db


def update_results():
    people = Person.query.all()
    Result.query.delete()

    for person in people:
        raw_results = requests.get(f'https://www.worldcubeassociation.org/api/v0/persons/{person.wca_id}').json()[
            'personal_records']
        results = []
        for r in raw_results.keys():
            result = Result(
                event=r,
                single=raw_results[r]['single']['best'],
                average=raw_results[r]['average']['best'],
                single_rank=raw_results[r]['single']['world_rank'],
                average_rank=raw_results[r]['average']['world_rank'],
                person_id=person.id
            )
            results.append(result)

        person.results = results

    db.session.commit()
