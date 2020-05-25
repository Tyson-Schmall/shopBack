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
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # This simply removes a warning that generates when running certain commands in the terminal.

# CORS is short for cross origin resource sharing. This is a fancy title, it let's us communicate across
# multiple platforms.

CORS(app)

# Below, we instantiate our SQLAlchemy import and our Marshmallow imports into variables. These variables will
# be called on at a later time to structure our database models, as well as building out our database schema(s).

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Below the tables are being built. These tables are structured to withhold and store certain types of data
# in certain combinations, to create certain behaviours and reactions when users perform specific actions.

# The first table, 'Artist', this is for the artists of a shop. The individual with the 'admin_artist' value set to
# 'true', will be the owner of the shop, and will be able to remove other Artist's if they so choose. 

# If the head of the shop (owner, manager, whichever title they carry) needs to remove another Artist due to their position
# being vacated, I will have the system check the 'admin_artist' attribute, and allow the removal of another Artist, only
# if the requesting Artist has the 'admin_artist' attribute set to 'true'.

class Artist(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(16), nullable=False)
  last_name = db.Column(db.String(16), nullable=False)
  email = db.Column(db.String(48), nullable=False)
  password = db.Column(db.String(32), nullable=False)
  admin_artist = db.Column(db.Boolean)

  # Below, the __init__ is us stating that for each time we 'instantiate' this class into a variable, we want the 'instance' of this class to be
  # unique to whatever variable we have instantiated the class into. So if a shop has two Owner's, each one would be able to create their own 
  # user information, because each owner would be creating their own 'instance' of a user. Tyson would create his own instance with his own user 
  # credentials, and Joe would create his own instance with his user credentials. They would be totally individual of each other.

  def __init__(self, first_name, last_name, email, password, admin_artist):
    self.first_name = first_name
    self.last_name = last_name
    self.email = email
    self.password = password
    self.admin_artist = admin_artist

# Below is our Schema for the Artist class. Marshmallow is the dependency that allows for us to make up a Schema class. The Schema class
# is what maps out our database model,

class ArtistSchema(ma.Schema):
  class Meta:
    fields = ("id", "first_name", "last_name", "email", "password", "admin_artist")

# Below, the declared ArtistSchema class has been instantiated into two separate variables. The first, will be used to query for a specific 
# Artist. The second, is used to query for ALL registered Artists within the database. 

artist_schema = ArtistSchema()
artists_schema = ArtistSchema(many=True)

# Below table is for the content that each artist should have entailed on the website about them. An image,
# a short-ish bio, their name, and the 'artist_id' column is for the purpose of the relationship between the
# below table, and the above one. The 'artist_id' interacts directly with 'children' in the above table. 

class ArtistContent(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  cover_image = db.Column(db.String(500), nullable=False)
  artist_name = db.Column(db.String(64), nullable=False)
  bio = db.Column(db.String(666), nullable=False)

  def __init__(self, cover_image, artist_name, bio, artist_id):
    self.cover_image = cover_image
    self.artist_name = artist_name
    self.bio = bio

# Just like the prior Schema class we built out, the below is a Schema for the ArtistContent class above. 
# We then take the schema class, and instantiate it into two variables. One to query for a single schema,
# the other to query for all information contained within this specific schema class.

class ArtistContentSchema(ma.Schema):
  class Meta:
    fields = ("id", "cover_image", "artist_name", "bio")

content_schema = ArtistContentSchema()
all_content_schema = ArtistContentSchema(many=True)

# Below, is the beginning of our routes being built. These routes will dictate where a user is sent when clicking in certain places,
# or on certain buttons/in certain fields of our app. The first one you see here, is simply a test. This allows me to make use of
# a program called 'postman', which let's me check from my local environment whether or not these routes are functioning the way we
# intend for them to.

@app.route("/")
def home_page():
  return "<h3>Test route, test is successful<h3>"

# Below, is the route we are building in that allows an individual to see every single artist that is registered and logged in
# this database. I tested it in Postman, and it functions as it needs to.

@app.route("/artists", methods=["GET"])
def render_artists():
  all_artists = Artist.query.all()
  result = artists_schema.dump(all_artists)

  return jsonify(result)

# Below, the route listed is to display a single artist, that can be specifically requested by a user operating the front-end of
# this app. The below has been tested in Postman and funcitons as it needs to. 

@app.route("/artist/<id>", methods=["GET"])
def render_artist(id):
  artist = Artist.query.get(id)
  result = artist_schema.dump(artist)

  return jsonify(result)

# The below route is how to add a user into the database dynamically, but the issue for now is that the children attribute on line
# 149 is causing hiccups. I must have an error with the way 'children' was established up top, so i will have to look into this.
# In the meantime, will push to github since everything else prior to the below block of code functions properly.

@app.route("/add_artist", methods=["POST"])
def add_artist():
  first_name = request.json["first_name"]
  last_name = request.json["last_name"]
  email = request.json["email"]
  password = request.json["password"]
  admin_artist = request.json["admin_artist"]

  new_artist = Artist(first_name, last_name, email, password, admin_artist)

  db.session.add(new_artist)
  db.session.commit()
  
  artist = Artist.query.get(new_artist.id)
  return artist_schema.jsonify(artist)

# The below route is called a PATCH route. This allows for artist's to edit pieces of their 
# identifying information that is stored in this database. Tested in Postman, works as expected.

@app.route("/artist/<id>", methods=["PATCH"])
def edit_artist(id):
  artist = Artist.query.get(id)
  
  new_first_name = request.json["first_name"]
  new_last_name = request.json["last_name"]
  new_email = request.json["email"]
  new_password = request.json["password"]

  artist.first_name = new_first_name
  artist.last_name = new_last_name
  artist.email = new_email
  artist.password = new_password
  
  db.session.commit()
  return artist_schema.jsonify(artist)

# The below route is a DELETE route, and is used to assist in the removal of any artists/users that
# may leave the shop for any reason. Tested in Postman and works as expected. 

@app.route("/remove_artist/<id>", methods=["DELETE"])
def remove_artist(id):
  artist = Artist.query.get(id)

  db.session.delete(artist)
  db.session.commit()

  return jsonify("This artist has been removed")


if __name__=="__main__":
  app.debug = True
  app.run()








  



