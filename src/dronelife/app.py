from flask import Flask
from flask import render_template
from flask_appconfig.env import from_envvars
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask('dronelife')

# Load app config info from environment variables
from_envvars(app.config, prefix=app.name.upper() + '_')

# Compile less files into css
from flaskext.lesscss import lesscss
app.static_path = app.static_url_path # the version of flask-lesscss in PyPI is outdated
lesscss(app)

db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

