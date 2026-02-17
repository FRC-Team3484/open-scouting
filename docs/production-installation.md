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
nano .env # Change the `TBA_API_KEY`, `SECRET_KEY` in this file. You may need to update `CORS_ORIGINS` and `PUBLIC_FAST_API_URL` as well
```

Log into the docker container registry. You will need to create a GitHub PAT:
```bash
docker login ghcr.io
```

Pull the images and start the containers:
```bash
docker compose pull
docker compose up -d
```

Finally, navigate to `<ip>/api/docs`, and run `/auth/signup`. Then run `/auth/me/set_superuser` to make your user a superuser. Navigate to the admin page `(<ip>/admin)` and start by creating some seasons.