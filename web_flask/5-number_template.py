#!/usr/bin/python3
"""Write a script that starts a Flask web application:
    Your web application must be listening on 0.0.0.0 , port 5000
    Routes:
        / : display “Hello HBNB!”
"""
from flask import Flask, render_template

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


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text='is cool'):
    """/python/<text> : display “Python ”,
    followed by the value of the text variable (replace
    underscore _ symbols with a space )
    /"""
    text = text.replace("_", " ")
    return f"Python {text}"


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """/number/<n> : display “ n is a number”
    only if n is an integer
    You must use the option strict_slashes=False
    in your route definition"""
    if type(n) is int:
        return f"{n} is a number"


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    if type(n) is int:
        return render_template("5-number.html", n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
