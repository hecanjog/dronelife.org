from flask import Flask
from flask import render_template

import os
import subprocess

app = Flask(__name__)

# Compile less files into css
from flaskext.lesscss import lesscss
app.static_path = app.static_url_path # the version of flask-lesscss in PyPI is outdated
lesscss(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':

    app.run(debug=True)

