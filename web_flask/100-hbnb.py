#!/usr/bin/python3
"""
Starts a Flask web application.
Listens on 0.0.0.0  on port 5000.
Routes:
  *  /hbnb: Display the HTML page for hbnb home page.
"""
from flask import Flask
from flask import render_template
from models import storage
from sqlalchemy.sql import text

app = Flask(__name__)


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Display the HTML page for hbnb home page."""
    amenities = storage.all(text("Amenity"))
    places = storage.all(text("Place"))
    states = storage.all(text("State"))
    return render_template("100-hbnb.html",
                           amenities=amenities,
                           places=places,
                           states=states)


@app.teardown_appcontext
def teardown(excpt=None):
    """Remove the current SQLAlchemy Session."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
