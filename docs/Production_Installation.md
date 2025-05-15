# Production Installation
Follow these steps to get Open Scouting running on a server for production use

The installation and deployment process uses docker for simplicity.

First, ensure you have `docker`, `docker-compose`, and `git` installed on your system

> [!NOTE]
> The included build files assumes that the db data is located at `/mnt/db/postgres` for the db and `/mnt/db/backups` for database backups. Change these values in `docker-compose.yml` to adjust the database location

Next, clone this repository
```bash
git clone https://github.com/FRC-Team3484/open-scouting
cd open-scouting
```

Now, copy `.env-template` to a new file called `.env`
```bash
cp .env.production.template .env.production
```

You'll want to change several of these variables in `.env`
- **`DEBUG`** - `False`
- **`SECRET_KEY`** - Generate your secret key using `django.core.management.utils.get_random_secret_key()`
- **`ADMIN_PATH`** - Change this to a random string or something specific that only you would know, protects the admin page from attacks
- **`TBA_API_KEY`** - Replace with your TBA API key, generated [here](https://www.thebluealliance.com/account)
- **`SERVER_IP`** - Replace with the IP address and port that the server will be accessed at
- **`CSRF_TRUSTED_ORIGINS`** - Replace with a list containing the IP address that the server will be hosted on

- **`POSTGRES_PASSWORD`** - Replace with a password for the postgres database, this should be long and hard to guess
  
The following variables are for the superuser that is created when the server starts for the first time, this is the main administrator account that is used to access the `/admin` page.
- **`DJANGO_SUPERUSER_USERNAME`** - Replace with your superuser's username (Make this equal to your email if you want to use this account inside of Open Scouting for contributing)
- **`DJANGO_SUPERUSER_PASSWORD`** - Replace with your superuser's password
- **`DJANGO_SUPERUSER_EMAIL`** - Replace with your superuser's email

Additionally, you should configure the environment variables for setting up emails

> [!NOTE]
> If you're having issues with pip being able to resolve the DNS name, you may need to restart your docker daemon using `sudo systemctl restart docker`

Finally, building and running the server is as simple as running the following
```bash
docker compose up --build -d
```

Subsequent starts should be run using
```bash
docker compose up -d
```

The server should now be working!

You should navigate to the `/admin` page (or whatever your admin path is) and access your new superuser, and fill in some values for the `Profile` object to prevent any errors when attempting to use this account

#### Backups
If you'd like to enable backups on your sever, use a cron job to do so
```bash
crontab -e # Select the first option
```

Add these lines into the editor that opens
```bash
0 2 * * * docker exec -t postgres pg_dump -U postgres -F c -f /backups/db_backup_$(date +\%F).dump mydatabase
0 3 * * * find /mnt/db/backups -type f -name "db_backup_*.dump" -mtime +7 -exec rm {} \;
```