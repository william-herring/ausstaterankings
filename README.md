# Australian State/Territory Speedcubing Rankings
This is a site to keep track of Australian state and territory WCA rankings. Contributors are greatly appreciated,
please [contact me](mailto:william.herring.au@gmail.com) if you are familiar with Flask and/or the WCA API. 

## Setup
1. Clone this repository
2. Install Flask
```commandline
pip install Flask
```
3. Navigate to project directory and install NPM dependencies
```commandline
cd .../ausstaterankings
npm install
```
4. [Create Postgres database](https://www.postgresql.org/docs/current/sql-createdatabase.html) and configure .env
```commandline
touch .env
```
```
SECRET_KEY=ERWArfC+T3A32qFYyilbmw==

# OAuth
CLIENT_ID=[Contact to request access]
CLIENT_SECRET=[Contact to request access]

DATABASE_URI=postgresql://[url]
```
5. Start Tailwind
```commandline
npm run tailwind
```
6. Configure and run the app
```commandline
flask --app app run --debug
```
