#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import (
     Flask,
     render_template,
     request,
     Response,
     flash,
     redirect,
     url_for,abort
)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *

from flask_migrate import Migrate
from datetime import datetime

from models import db, Venue, Artist, Show
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
#db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app,db)

# TODO: connect to a local postgresql database

#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
# show = db.Table("show",
#       db.Column ("artist_id",db.Integer, db.ForeignKey("Artist.id") , primary_key=True),
#       db.Column ("venue_id",db.Integer, db.ForeignKey("Venue.id") , primary_key=True),
#       db.Column ("start_time",db.String(), nullable=False )
# )


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
###########################################################################################
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  data =[]
  venues = Venue.query.all()
  venues_list=[]
  cityState_set=set()
  for venue in venues:
      data_obj=[]
      city= venue.city
      state= venue.state
      cityState=(city,state)
      cityState_set.add((city,state))

  for address in cityState_set:
      data_obj=[]
      city=address[0]
      state=address[1]
      for venue in venues:
           if venue.city == city and venue.state == state :
               name = venue.name
               id = venue.id
               num_upcoming_shows= Show.query.filter(Show.venue_id == id).count()
               data_obj.append({"id":id, "name":name, "num_upcoming_shows":num_upcoming_shows})
      data.append({"city":city, "state":state, "venues":data_obj})

  return render_template('pages/venues.html', areas=data);
#####################################################################
@app.route('/venues/search', methods=['POST'])
def search_venues():############ need the upcoming shows
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search = request.form.get('search_term')
  looking_for = '%{0}%'.format(search)
  result = Venue.query.filter(Venue.name.ilike(looking_for))
  data=[]
  for venue in result:
      num_upcoming_shows= Show.query.filter('venue_id'==venue.id).count()
      data.append({"id":venue.id , "name":venue.name , "num_upcoming_shows":num_upcoming_shows } )
  count = Venue.query.filter(Venue.name.ilike(looking_for)).count()
  response= {"count": count, "data":data}

  # {
  #   "count": 1,
  #   "data": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  today=datetime.today().strftime('%Y-%m-%d %H:%M:%S')
  past_shows_list =[]
  upcoming_shows_list =[]
  data = []
  venue = Venue.query.get(venue_id)
  past_shows = Show.query.filter(Show.start_time < today).filter(Show.venue_id == venue_id)
  upcoming_shows = Show.query.filter(Show.start_time > today).filter (Show.venue_id == venue_id)
  past_shows_count=  Show.query.filter(Show.start_time < today).filter(Show.venue_id == venue_id).count()
  upcoming_shows_count = Show.query.filter(Show.start_time > today).filter (Show.venue_id == venue_id).count()

  for show in past_shows:
      artist = Artist.query.get(show.artist_id)
      past_shows_obj = {"artist_id": artist.id,
      "artist_name": artist.name ,
      "artist_image_link": artist.image_link,
      "start_time": show.start_time}
      past_shows_list.append(past_shows_obj)

  for show in upcoming_shows:
      artist = Artist.query.get(show.artist_id)
      upcoming_shows_obj = {"artist_id": artist.id,
      "artist_name": artist.name ,
      "artist_image_link": artist.image_link,
      "start_time": show.start_time}
      upcoming_shows_list.append(upcoming_shows_obj)

  data= {"id": venue.id, "name":venue.name,"genres":venue.genres,
         "address": venue.address,"city": venue.city,"state":venue.state,
         "phone": venue.phone,"facebook_link":venue.facebook_link,
         "image_link": venue.image_link,"past_shows":past_shows_list,
         "upcoming_shows":upcoming_shows_list,"past_shows_count":past_shows_count,
         "upcoming_shows_count":upcoming_shows_count}

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)
####################################################DONE###############
@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
    body={}
    error= False
    try:
        venue =Venue( name=request.form.get("name"),city=request.form.get('city'),
                      state=request.form.get('state'),address=request.form.get('address'),
                      phone=request.form.get('phone'),genres=request.form.get('genres'),
                      facebook_link =request.form.get('facebook_link') )
        db.session.add(venue)
        db.session.commit()
        body["name"]=venue.name
        flash('Venue ' + body['name'] + ' was successfully listed!')
    except:
        error=True
        db.session.rollback()
        flash('ERROR. Could not create venue ' + body['name'])
    finally:
        db.session.close()
    if error:
        abort (400)
  # on successful db insert, flash success
    else :
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data=[]
  result = Artist.query.all()
  for artist in result:
      data_obj={"id":artist.id,"name":artist.name}
      data.append(data_obj)

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  today=datetime.today().strftime('%Y-%m-%d %H:%M:%S')
  data =[]
  search = request.form.get('search_term')
  looking_for = '%{0}%'.format(search)
  result = Artist.query.filter(Artist.name.ilike(looking_for))
  count = Artist.query.filter(Artist.name.ilike(looking_for)).count()

  for artist in result:
      num_upcoming_shows = Show.query.filter(Show.start_time >= today).filter( Show.artist_id==artist.id).count()
      data_obj = {"id":artist.id , "name":artist.name, "num_upcoming_shows":num_upcoming_shows}
      data.append(data_obj)
  response= {"count": count, "data":data}

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  today=datetime.today().strftime('%Y-%m-%d %H:%M:%S')
  past_shows_list =[]
  upcoming_shows_list =[]
  data = []
  artist = Artist.query.get(artist_id)
  past_shows = Show.query.filter(Show.start_time < today ).filter(Show.artist_id==artist_id)
  upcoming_shows = Show.query.filter(Show.start_time  > today ).filter(Show.artist_id==artist_id)
  past_shows_count= Show.query.filter(Show.start_time  < today).filter(Show.artist_id==artist_id).count()
  upcoming_shows_count = Show.query.filter(Show.start_time  > today ).filter(Show.artist_id==artist_id).count()

  for show in past_shows:
      venue = Venue.query.get(show.venue_id)
      past_shows_obj = {"venue_id": venue.id,
      "venue_name": venue.name ,
      "venue_image_link": venue.image_link,
      "start_time": show.start_time}
      past_shows_list.append(past_shows_obj)

  for show in upcoming_shows:
      venue = Venue.query.get(show.venue_id)
      upcoming_shows_obj = {"venue_id": venue.id,
      "venue_name": venue.name ,
      "venue_image_link": venue.image_link,
      "start_time": show.start_time}
      upcoming_shows_list.append(upcoming_shows_obj)

  data= {"id": artist.id, "name":artist.name,"genres":artist.genres,
         "city": artist.city,"state":artist.state,
         "phone": artist.phone,"facebook_link":artist.facebook_link,
         "image_link": artist.image_link,"past_shows":past_shows_list,
         "upcoming_shows":upcoming_shows_list,"past_shows_count":past_shows_count,
         "upcoming_shows_count":upcoming_shows_count}

  #data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist=Artist.query.get(artist_id)

  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  artist = Artist.query.get(artist_id)

  name =  request.form.get("name")
  genres =  request.form.get("genres")
  city =  request.form.get("city")
  state =  request.form.get("state")
  phone =  request.form.get("phone")
  facebook_link =  request.form.get("facebook_link")
  image_link= request.form.get("image_link")

  artist.name=name
  artist.genres=genres
  artist.city=city
  artist.state=state
  artist.phone=phone
  artist.image_link = image_link
  artist.facebook_link=facebook_link

  db.session.commit()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()

  venue = Venue.query.get(venue_id)

  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
   venue = Venue.query.get(venue_id)

   name =  request.form.get("name")
   genres =  request.form.get("genres")
   city =  request.form.get("city")
   state =  request.form.get("state")
   phone =  request.form.get("phone")
   address = request.form.get("address")
   facebook_link = request.form.get("facebook_link")
   image_link= request.form.get("image_link")

   venue.name=name
   venue.genres=genres
   venue.city=city
   venue.state=state
   venue.phone=phone
   venue.address = address
   venue.image_link = image_link
   venue.facebook_link=facebook_link

   db.session.commit()

   return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():

  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
    body={}
    error=False
    try:
        artist = Artist(name=request.form.get('name'),city=request.form.get('city'),
                    state=request.form.get('state'),phone=request.form.get('phone'),
                    genres=request.form.get('genres'),
                    facebook_link =request.form.get('facebook_link') )
        db.session.add(artist)
        db.session.commit()
        body["name"]=artist.name
        flash('Artist ' + body['name'] + ' was successfully listed!')
    except:
        error=True
        db.session.rollback()
        flash('ERROR. Could not create artist ' + body['name'])
    finally:
        db.session.close()
    if error:
        abort (400)
    else :
  # TODO: on unsuccessful db insert, flash an error instead.
        return render_template('pages/home.html')
#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data =[]
  shows= Show.query.all()
  for show in shows:
      venue = Venue.query.get(show.venue_id)
      artist = Artist.query.get(show.artist_id)
      data_obj = {"venue_id":venue.id, "venue_name":venue.name,
                  "artist_id": artist.id, "artist_name": artist.name,
                  "artist_image_link": artist.image_link,
                  "start_time":show.start_time}
      data.append(data_obj)

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  body={}
  error= False
  try:
      show = Show(artist_id=request.form.get('artist_id'),
                  venue_id=request.form.get('venue_id'),
                  start_time=request.form.get('start_time'))
      db.session.add(show)
      db.session.commit()
      flash('Show was successfully listed!')
  except:
      error=True
      db.session.rollback()
      flash('ERROR. Could not create show ')
  finally:
      db.session.close()
  if error:
      abort (400)
  else:
      return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
