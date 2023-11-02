#!/usr/bin/python3
""" Routes:
/states_list: display a HTML page: (inside the tag BODY)
H1 tag: “States”
UL tag: with the listof
all State objects present in DBStorage sorted by name (A->Z"""
from flask import Flask
from flask import render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states(id=None):
    flag = 404
    result = None
    ctxt = {'states': None, 'flag': 404}
    if id is None:
        all_states = list(storage.all(State).values())
        all_states.sort(key=lambda x: x.name)
        flag = 1
        ctxt = {'states': all_states,
                'flag': flag}
    else:
        all_states = list(storage.all(State).values())
        result = list(filter(lambda x: x.id == id, all_states))
        if len(result) > 0:
            flag = 2
            ctxt = {'states': result[0],
                    'flag': flag}
    return render_template('9-states.html', **ctxt)


@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy session."""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
