#!/usr/bin/python3
"""Write a script that starts a Flask web application:
    Your web application must be listening on 0.0.0.0 , port 5000
    Routes:
        / : display “Hello HBNB!”
"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """ Hello HBNB! output for hello route /"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """HBNB! output for hello route /"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    """HBNB! output for hello route /"""
    text = text.replace("_", " ")
    return f"C {text}"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
