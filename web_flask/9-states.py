#!/usr/bin/python3
"""starts a Flask web application"""

from flask import Flask, render_template
import models

app = Flask("__name__")


@app.teardown_appcontext
def refresh(exception):
        models.storage.close()


@app.route('/states/<id>', strict_slashes=False)
def state_cities(id):
    state = storage.get(State, id)
    if state:
        return render_template('9-states.html', state=state)
    else:
        return render_template('9-states.html', not_found=True)



@app.route("/states/<id>", strict_slashes=False)
def route_city():
        pep_fix = models.dummy_classes["State"]
        data = models.storage.all(cls=pep_fix)
        states = data.values()
        return render_template('8-cities_by_states.html', states_list=states)


if __name__ == "__main__":
        app.run()
