# Production Installation
This page describes how to set up a production installation of Open Scouting.

First, clone the repository:
```bash
git clone https://github.com/FRC-Team3484/open-scouting
cd open-scouting
```

Setup the backend `.env`:
```bash
cd backend
cp .env.production.template .env.production
nano .env.production # Change the `SECRET_KEY` and `TBA_API_KEY` in this file
cd ..
```

Setup the frontend `.env`:
```bash
cd frontend
cp .env.production.template .env
nano .env # Change `PUBLIC_FAST_API_KEY` and `TBA_API_KEY` in this file
cd ..
```

Start and build the containers:
```bash
docker compose up --build -d
```

Setup the database:
```bash
cd backend
python -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
aerich upgrade
```

Finally, navigate to `<ip>/api/docs`, and run `/auth/signup`. Then run `/auth/me/set_superuser` to make your user a superuser. Navigate to the admin page `(<ip>/admin)` and start by creating some seasons.