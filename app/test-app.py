#! /usr/bin/env python

from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)

@app.route('/')
def hello_world():
  return render_template('example.html')

if __name__ == '__main__':
  Bootstrap(app)
  app.run(host="0.0.0.0")

