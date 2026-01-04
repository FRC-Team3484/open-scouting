# Development Installation

Clone the repository:
```bash
git clone https://github.com/FRC-Team3484/open-scouting
cd open-scouting
```

## Frontend
Install the dependencies:
```bash
cd frontend
npm install
```

Create the `.env.development` file:
```bash
cp .env.development.template .env.development
```

Set the value of `TBA_API_KEY` in that file to the API key you must create on your [TBA account page](https://www.thebluealliance.com/account)

Start the frontend:
```bash
npm run dev -- --open
```
Alternatively, use the `Start SvelteKit Frontend` task in VSCode

## Backend
Create a new Python virtual environment, and install the dependencies:
```bash
cd backend
python -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
```

Create the `.env.development` file:
```bash
cp .env.development.template .env.development
```

In a new terminal in the project root, start the postgres DB server:
```bash
docker compose -f docker-compose.dev.yml up
```
Alternatively, use the `Start Postgres DB Server` task in VSCode

Once the DB has been fully pulled and started, initialize the database:
```bash
aerich init-db
```

Start the backend:
```bash
uvicorn app.main:app --reload
```
Alternatively, use the `Start FastAPI Backend` task in VSCode

## User Setup
Now that the frontend and backend is running, configure your superuser account.

1. Navigate to the [authentication page](http://localhost:5173/authentication)
2. Create your account
3. Navigate to the [FastAPI docs](http://localhost:8000/docs)
4. Click `Authorize` in the top right, and enter the username and password for the account you just created. Ignore `client_id` and `client_secret`
5. Find the `/users/md/set_superuser` route in the list, expand the dropdown, and click `Try it out`
6. Finally, click `Execute`

You'll probably want to set up some seasons, fields, and game pieces in the [admin dashboard](http://localhost:5173/admin).