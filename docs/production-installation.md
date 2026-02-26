# Production Installation
This page describes how to set up a production installation of Open Scouting.

First, clone the repository:
```bash
git clone https://github.com/FRC-Team3484/open-scouting
cd open-scouting
```

Setup the `.env` file:
```bash
cp .env.production.template .env
nano .env # Change the `TBA_API_KEY`, `SECRET_KEY` in this file. You may need to update `CORS_ORIGINS`, `PUBLIC_FAST_API_URL`, and `UPLOAD_ROOT` as well
```

Pull the images and start the containers:
```bash
docker compose pull
docker compose up -d
```

Finally, navigate to `<ip>/api/docs`, and run `/auth/signup`. The first user created on the server will be a superuser. Navigate to the admin page `(<ip>/admin)` and start by creating some seasons.