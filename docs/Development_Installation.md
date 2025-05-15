# Development Installation
Follow these steps to get the server running locally for contributing or development

First, view this repo on GitHub and click "Fork". In the page that appears, uncheck "Copy the main branch only" to ensure you have access to the development branch for the most up to date changes

Once you've made your fork, clone the repository to your local machine, and move to the development branch
```bash
git clone https://github.com/<your username>/open-scouting
cd open-scouting
git checkout development
```

Then, create a new python virtual environment
```bash
python3 -m venv .venv
```

Activate the virtual environment using the command for your system (Linux is used here) and install the required dependencies
```bash
source ./.venv/bin/activate
pip install -r scouting/requirements.txt
pip install -r scouting/requirements-dev.txt
```

Install the required `npm` libraries
```bash
npm install
```

Copy the `.env-template` file to a new file called `.env`.
```bash
cd scouting
cp .env.development.template .env.development
```
You should add your TBA Read API key here, and credentials for sending emails

- Information for obtaining this key is available [here](https://www.thebluealliance.com/apidocs)
- If you don't want your development server to send emails, simply set `EMAIL_ENABLED` to `False`

Next, create a django superuser and make and migrate the models
```bash
python manage.py migrate
python manage.py createsuperuser # Follow the steps to create your superuser when running this command
```

Now run the server using the following command, or run the `Start server` task in Visual Studio Code
```bash
python manage.py runserver
```

Now, navigate to the `./admin` page (usually `http://127.0.0.1:8000/admin`), add view the `User` models. Find the superuser you just created, scroll down, and fill out all the fields for the profile object to prevent any errors

Additionally, you should start the Tailwind CSS builder with the following command, or use the `Build CSS` task in Visual Studio Code
```bash
npm run build:css
```

Finally, navigate to the index page (usually `http://127.0.0.1`), open the menu in the bottom right corner, then select `Developer Settings > Network First Service Worker`. This ensures the client gets the most up to date changes while you're developing, instead of caching those pages for offline use.

## Development
### djlint
This project uses [`djlint`](https://github.com/djlint/djLint) to lint the Django templates. Install `djlint` to use in VSCode [here](https://marketplace.visualstudio.com/items?itemName=monosans.djlint)

You can run this using the following command
```bash
djlint scouting --reformat
```

### ruff
This project uses [`ruff`](https://docs.astral.sh/ruff/) to lint and format the python code.
You can run the following command to run the linter once
```bash
ruff check scouting --fix
```
For VS Code users, you can install the `ruff` extension [here](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff) to get linting and formatting on save.


### biome
[`biome`](https://biomejs.dev/) is used to format and lint the JavaScript files

You can check for any linting or formatting issues using the following command
```bash
biome check scouting
```

You can install biome as a VSCode extension [here](https://marketplace.visualstudio.com/items?itemName=biomejs.biome) to get linting and formatting on save.
