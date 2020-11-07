# TUMuch(Spaghetti)Code Python Server

- Use Python 3
- Use of python virtual environment suggested, something like:

```
python3 -m venv .venv
source .venv/bin/activate
```

## Installation

```
pip install -r requirements.txt
```

## Running

```
export FLASK_APP=main.py
export FLASK_ENV=development # Enable debugging & automatic reloading
flask run --host=0.0.0.0 # --host is added so the server can be seen on the network
```
