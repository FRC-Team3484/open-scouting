# Development Installation

```
git clone https://github.com/FRC-Team3484/open-scouting
cd open-scouting
```

## Frontend
```
cd frontend
npm install

npm run dev -- --open
```

## Backend
```
cd backend
python -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt

uvicorn app.main:app --reload
```