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

Now, set up the initial superuser, replacing `<ip>` with the server's ip, and filling in your information. The first user created on the server will be a superuser.
```bash
curl -X POST https://<ip>/api/auth/signup \
     -H "Content-Type: application/json" \
     -d '{
            "username": "username",
            "email": "user@example.com",
            "password": "string",
            "confirm_password": "string",
            "team_number": 0,
            "display_name": "string"
        }'
```

The server is now ready! Navigate to the admin page `(<ip>/admin)` and start by creating some seasons.