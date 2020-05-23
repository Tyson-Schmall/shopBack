#Below is a block of code importing the dependencies we need for this project. 

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku
from environs import Env
import os

# Below, we instantiate our Flask import, into a variable named 'app'.
# Below, we also instantiate our Heroku import, into a variable named 'heroku'.
# We will use these variables in a little bit.

app = Flask(__name__)
heroku = Heroku(app)

# Below, the 'basedir' variable, is declared with a value of a path within the operating system.
# This path, is what drops users at the appropriate starting point when they access our database/site.
# The config lines, are in place to configure paths and interaction between paths in our database.

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # This simply 

# CORS is short for cross origin resource sharing. This is a fancy title, it let's us communicate across
# multiple platforms.

CORS(app)

# Below, we instantiate our SQLAlchemy import and our Marshmallow imports into variables. These variables will
# be called on at a later time to structure our database models, as well as building out our database schema(s).

db = SQLAlchemy(app)
ma = Marshmallow(app)

