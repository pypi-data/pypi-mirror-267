## Flask-SQLAlchemySession2024

[![Run tests](https://github.com/e-c-d/flask-sqlalchemy-session2024/actions/workflows/python-package.yml/badge.svg)](https://github.com/e-c-d/flask-sqlalchemy-session2024/actions/workflows/python-package.yml)

This is a fork of the excellent
[Flask-SQLAlchemySession](https://github.com/dtheodor/flask-sqlalchemy-session/)
package by Dimitris Theodorou, which has unfortunately gone unpatched for a
few years.

Provides an SQLAlchemy scoped session that creates
unique sessions per Flask request, following the guidelines documented at
[Using Custom Created Scopes](https://docs.sqlalchemy.org/en/20/orm/contextual.html).

### TODO

- coverage
- docs

### Usage

Initialize a `flask_scoped_session` as you would a
`scoped_session`, with the addition of a Flask
app. Then use the resulting session to query models:

```python
from flask import Flask, abort, jsonify
from flask_sqlalchemy_session import flask_scoped_session

app = Flask(__name__)
session = flask_scoped_session(session_factory, app)

@app.route("/users/<int:user_id>")
def user(user_id):
    user = session.query(User).get(user_id)
    if user is None:
        abort(404)
    return flask.jsonify(**user.to_dict())
```

The `current_session` is also provided as a convenient accessor to the session
of the current request, in the same spirit of `flask.request` and
`flask.current_app`.

```python
from flask_sqlalchemy_session import current_session

@app.route("/users/<int:user_id>")
def user(user_id):
    user = current_session.query(User).get(user_id)
    if user is None:
        abort(404)
    return flask.jsonify(**user.to_dict())
```


### Tests

You can run the tests by invoking `PYTHONPATH=. py.test tests/` in the repository root.
