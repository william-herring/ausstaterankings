# Australian State/Territory Speedcubing Rankings
This is a site to keep track of Australian state and territory WCA rankings.

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
