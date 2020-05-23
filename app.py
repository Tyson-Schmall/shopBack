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

# Below the tables are being built. These tables are structured to withhold and store certain types of data
# in certain combinations, to create certain behaviours and reactions when users perform specific actions.

# The first table, 'Owner', this is for the owner of a shop. This individual will be the owner of the shop, the one who employs
# everyone else. We need to be able to store their information as a user, so the database acquires this information.
# First&Last name, email, password, these are all crucial identifying factors that should be unique.

# The 'king' and 'children' variables, are for different purposes. The 'king' variable, is a Boolean data type. This means 'true' or 'false'.
# With 'king' in place, we are able to perform checks when certain users want to perform certain actions. For example, if the Owner needs to
# remove an employee who recently vacated their position, the Owner should be able to do that. Right? But what ensures that an 'Artist' doesn't
# go and try to do the same thing? That's what 'king' is for. 'King' will be unique to the 'Owner' class, and the only way this system will
# allow the removal of an artist, is if the 'king' value is set to 'True'. We will build the rest of that functionality out later, but for
# now, this is where we begin creating the 'king' functionality we will seek later on.

class Owner(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(16), nullable=False)
  last_name = db.Column(db.String(16), nullable=False)
  email = db.Column(db.String(48), nullable=False)
  password = db.Column(db.String(32), nullable=False)
  king = db.Column(db.Boolean)
  children = db.relationship("Artist", backref="owner")

  # Below, the __init__ is us stating that for each time we 'instantiate' this class into a variable, we want the 'instance' of this class to be
  # unique to whatever variable we have instantiated the class into. So if a shop has two Owner's, each one would be able to create their own 
  # user information, because each owner would be creating their own 'instance' of a user. Tyson would create his own instance with his own user 
  # credentials, and Joe would create his own instance with his user credentials. They would be totally individual of each other.

  def __init__(self, first_name, last_name, email, password, king):
    self.first_name = first_name
    self.last_name = last_name
    self.email = email
    self.password = password
    self.king = king


# Below we have the Artist class. An "Artist" can only be created by an "Owner". The Artist will need certain information put in by an "Owner"
# in order to get up and running initially. 

class Artist(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(16), nullable=False)
  last_name = db.Column(db.String(16), nullable=False)
  email = db.Column(db.String(48), nullable=False)
  password = db.Column(db.String(32), nullable=False)
  auth = db.Column(db.Boolean)
  owner_id = db.Column(db.Integer, db.ForeignKey("owner.id"), nullable=False)
  children = db.relationship("ArtistContent", backref="artist")

  # Artist's will have a children relationship with the "ArtistContent" table. This will ensure that Artist's are allowed to udpate aspects
  # of their online portfolio/profile page.

  def __init__(self, first_name, last_name, email, password, auth):
    self.first_name = first_name
    self.last_name = last_name
    self.email = email
    self.password = password
    self.auth = auth

# Below table is not finished out yet, I had to put this on hold temporarily. Will put in further work and description of said work when 
# further time is available. Thanks!

class ArtistContent(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  cover_image = db.Column(db.String(500), nullable=False)
  artist_name = db.Column(db.String(64), nullable=False)
  bio = db.Column(db.String(666), nullable=False)



