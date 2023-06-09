"""
This is a script for manually entering users with WCA IDs. Run the script and enter IDs as prompted.
The server must be running to use this utility.
"""
import requests
from models import Person, Result
from app import db

while True:
    wca_id = input('Enter ID: ')
    state = input('Enter state or territory: ')
    user_data = requests.get(f'https://www.worldcubeassociation.org/api/v0/persons/{wca_id}').json()
    person = Person(
        name=user_data['person']['name'],
        wca_id=wca_id,
        avatar=user_data['person']['avatar']['thumb_url'],
        country=user_data['person']['country']['iso2'],
        state=state
    )
    db.session.add(person)
    db.session.commit()

    raw_results = user_data['personal_records']
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