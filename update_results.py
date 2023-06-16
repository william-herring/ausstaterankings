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
            if r in ['333mbf', '333ft', 'magic', 'mmagic']:
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
                    person_id=person.id
                )
            elif single is not None:
                result = Result(
                    event=r,
                    single=single,
                    single_rank=raw_results[r]['single']['world_rank'],
                    person_id=person.id
                )
            else:
                result = Result(
                    event=r,
                    average=average,
                    average_rank=r[r]['average']['world_rank'],
                    person_id=person.id
                )

            results.append(result)

        person.results = results
        db.session.add(person)
        db.session.commit()
