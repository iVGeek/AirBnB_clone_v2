#!/usr/bin/python3
"""
Return list of available states either from file or DB storage
"""
from models import storage
from flask import Flask, render_template
from models.state import State
import models


class StateInfo:
    """
    Interface that template receives regardless of storage type
    """
    def __init__(self, id, name, cities):
        """
        State ID and name
        """
        self.id = id
        self.name = name
        self.cities = cities


app = Flask(__name__)


@app.teardown_appcontext
def close_storage(exception):
    """
    Close file/DB storage on app teardown
    """
    storage.close()


@app.route("/states", strict_slashes=False)
def display_states():
    """
    Displays all states
    """
    states = []
    if models.storage_type == "db":
        results = storage.all("State").values()
    else:
        results = storage.all(State).values()
    for result in results:
        new_state = StateInfo(result.id, result.name, result.cities)
        states.append(new_state)
    states.sort(key=lambda s: s.name)
    return render_template("7-states_list.html",
                           states=states)


@app.route("/states/<string:id>", strict_slashes=False)
def display_state_with_id(id):
    """
    Display a state based on id passed
    """
    if models.storage_type == "db":
        results = list(storage.all("State").values())
    else:
        results = list(storage.all(State).values())
    try:
        result = [s for s in results if s.id == id][0]
        state = StateInfo(result.id, result.name, result.cities)
        state.cities.sort(key=lambda c: c.name)
    except:
        state = None
    return render_template("9-states.html",
                           state=state)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
