# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import enum
from flask_migrate import Migrate
from datetime import datetime
from sqlalchemy import DateTime

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# TODO: connect to a local postgresql database

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#

class StateList(enum.Enum):
    AL = "AL"
    AK = "AK"
    AZ = "AZ"
    AR = "AR"
    CA = "CA"
    CO = "CO"
    CT = "CT"
    DE = "DE"
    DC = "DC"
    FL = "FL"
    GA = "GA"
    HI = "HI"
    ID = "ID"
    IL = "IL"
    IN = "IN"
    IA = "IA"
    KS = "KS"
    KY = "KY"
    LA = "LA"
    ME = "ME"
    MT = "MT"
    NE = "NE"
    NV = "NV"
    NH = "NH"
    NJ = "NJ"
    NM = "NM"
    NY = "NY"
    NC = "NC"
    ND = "ND"
    OH = "OH"
    OK = "OK"
    OR = "OR"
    MD = "MD"
    MA = "MA"
    MI = "MI"
    MN = "MN"
    MS = "MS"
    MO = "MO"
    PA = "PA"
    RI = "RI"
    SC = "SC"
    SD = "SD"
    TN = "TN"
    TX = "TX"
    UT = "UT"
    VT = "VT"
    VA = "VA"
    WA = "WA"
    WV = "WV"
    WI = "WI"
    WY = "WY"


class GenresList(enum.Enum):
    Alternative = "Alternative"
    Blues = "Blues"
    Classical = "Classical"
    Country = "Country"
    Electronic = "Electronic"
    Folk = "Folk"
    Funk = "Funk"
    Hip_Hop = "Hip-Hop"
    Heavy_Metal = "Heavy Metal"
    Instrumental = "Instrumental"
    Jazz = "Jazz"
    Musical_Theatre = "Musical Theatre"
    Pop = "Pop"
    Punk = "Punk"
    RandB = "R&B"
    Reggae = "Reggae"
    Rock_n_Roll = "Rock n Roll"
    Soul = "Soul"
    Other = "Other"


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.Enum(StateList))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.Enum(GenresList)))
    website = db.Column(db.String(120))
    seeking_description = db.Column(db.String(120), nullable=True)
    seeking_talent = db.Column(db.Boolean, nullable=False)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.Enum(StateList))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.Enum(GenresList)))
    website = db.Column(db.String(120))
    seeking_description = db.Column(db.String(120), nullable=True)
    seeking_talent = db.Column(db.Boolean, nullable=False)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en_US')


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    data = []
    try:
        GroupList = db.session.query(Venue.state, Venue.city).group_by(Venue.state, Venue.city).all()
        CurrentTime = datetime.now()
        for GroupItem in GroupList:
            data2 = []
            VenueList = Venue.query.filter_by(state=GroupItem.state.value, city=GroupItem.city).all()
            for VenueItem in VenueList:
                VenueShows = db.session.query(Show.artist_id, Show.venue_id, Show.start_time).filter_by(
                    venue_id=VenueItem.id).all()
                UpcomingShows = []
                if len(VenueShows) > 0:
                    UpcomingShows = list(filter(lambda Show: Show.start_time > CurrentTime, VenueShows))
                data2.append({'id': VenueItem.id, 'name': VenueItem.name, 'num_upcoming_shows': len(UpcomingShows)})
            data.append({'city': GroupItem.city, 'state': GroupItem.state.value, 'venues': data2})
    except:
        db.session.rollback()
        data = []
    finally:
        db.session.close()

    return render_template('pages/venues.html', areas=data);


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    data = []
    search_term = ''
    try:
        search_term = request.form.get('search_term', '')
        search = "%{}%".format(search_term)
        CurrentTime = datetime.now()
        VenueList = Venue.query.filter(Venue.name.like(search)).all()
        for VenueItem in VenueList:
            VenueShows = db.session.query(Show.id, Show.start_time).filter_by(venue_id=VenueItem.id).all()
            UpcomingShowsList = list(filter(lambda Show: Show.start_time > CurrentTime, VenueShows))
            data.append({"id": VenueItem.id, "name": VenueItem.name, "num_upcoming_shows": len(UpcomingShowsList)})
    except:
        data = []
        db.session.rollback()
    finally:
        db.session.close()
    response = {
        "count": len(data),
        "data": data
    }
    return render_template('pages/search_venues.html', results=response, search_term=search_term)


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    data = {}
    try:
        VenueItem = Venue.query.get(venue_id)
        VenueShows = db.session.query(Show.id, Show.artist_id, Show.venue_id, Show.start_time).filter_by(
            venue_id=VenueItem.id).all()
        CurrentTime = datetime.now()
        UpcomingShowsData = []
        PastShowsData = []
        if len(VenueShows) > 0:
            UpcomingShowsList = list(filter(lambda Show: Show.start_time > CurrentTime, VenueShows))
            PastShowsList = list(filter(lambda Show: Show.start_time <= CurrentTime, VenueShows))
            for UpcomingShow in UpcomingShowsList:
                ArtistItem = db.session.query(Artist.id, Artist.name, Artist.image_link).filter_by(
                    id=UpcomingShow.artist_id).first()
                UpcomingShowsData.append({'artist_id': ArtistItem.id, 'artist_name': ArtistItem.name,
                                          'artist_image_link': ArtistItem.image_link,
                                          'start_time': str(UpcomingShow.start_time)})
            for PastShow in PastShowsList:
                ArtistItem = db.session.query(Artist.id, Artist.name, Artist.image_link).filter_by(
                    id=PastShow.artist_id).first()
                PastShowsData.append({'artist_id': ArtistItem.id, 'artist_name': ArtistItem.name,
                                      'artist_image_link': ArtistItem.image_link,
                                      'start_time': str(PastShow.start_time)})
        data = {"id": VenueItem.id, "name": VenueItem.name, "genres": [VenueItem.genres[0].value],
                "address": VenueItem.address, "city": VenueItem.city,
                "state": VenueItem.state, "phone": VenueItem.phone, "website": VenueItem.website,
                "facebook_link": VenueItem.facebook_link,
                "seeking_talent": VenueItem.seeking_talent, "seeking_description": VenueItem.seeking_description,
                "image_link": VenueItem.image_link, "past_shows": PastShowsData, "upcoming_shows": UpcomingShowsData,
                "past_shows_count": len(PastShowsData), "upcoming_shows_count": len(UpcomingShowsData)}
    except:
        db.session.rollback()
        data = {}
    finally:
        db.session.close()
    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    try:
        name = request.form.get('name')
        city = request.form.get('city')
        state = request.form.get('state')
        address = request.form.get('address')
        phone = request.form.get('phone')
        image_link = request.form.get('image_link')
        facebook_link = request.form.get('facebook_link')
        GenreItem = []
        GenreItem.append(request.form.get('genres'))
        genres = GenreItem
        # genres = request.form.get('genres')
        # genres = form.genres.data
        website = request.form.get('website')
        seeking_description = request.form.get('seeking_description')
        seeking_talent = request.form.get('seeking_talent')
        seeking_talent_final = False
        if seeking_talent == "y":
            seeking_talent_final = True
        venue = Venue(name=name, city=city, state=state, address=address, phone=phone, image_link=image_link,
                      facebook_link=facebook_link, genres=genres, website=website,
                      seeking_description=seeking_description,
                      seeking_talent=seeking_talent_final)
        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + name + ' was successfully listed!')
    except:
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
        db.session.rollback()
    finally:
        db.session.close()
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    name = ''
    message = ''
    try:
        name = Venue.query.filter_by(id=venue_id).first().name
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
        message = 'Venue ' + name + ' got deleted!'
        flash(message)
    except:
        db.session.rollback()
        message = 'Venue ' + name + ' did not deleted successfully!'
        flash(message)
    finally:
        db.session.close()
    return message


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    data = []
    try:
        ArtistList = Artist.query.all()
        for ArtistItem in ArtistList:
            data.append({'id': ArtistItem.id, 'name': ArtistItem.name})
    except:
        db.session.rollback()
        data = []
    finally:
        db.session.close()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    data = []
    search_term = ''
    try:
      search_term = request.form.get('search_term', '')
      search = "%{}%".format(search_term)
      CurrentTime = datetime.now()
      ArtistList = Artist.query.filter(Artist.name.like(search)).all()
      for ArtistItem in ArtistList:
        ArtistShows = db.session.query(Show.id, Show.start_time).filter_by(artist_id=ArtistItem.id).all()
        UpcomingShowsList = list(filter(lambda Show: Show.start_time > CurrentTime, ArtistShows))
        data.append({"id": ArtistItem.id, "name": ArtistItem.name, "num_upcoming_shows": len(UpcomingShowsList)})
    except:
      data = []
      db.session.rollback()
    finally:
      db.session.close()
    response = {
      "count": len(data),
      "data": data
    }
    return render_template('pages/search_artists.html', results=response, search_term=search_term)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  data = {}
  try:
    ArtistItem = Artist.query.get(artist_id)
    ArtistShows = db.session.query(Show.id, Show.artist_id, Show.venue_id, Show.start_time).filter_by(
      artist_id=ArtistItem.id).all()
    CurrentTime = datetime.now()
    UpcomingShowsData = []
    PastShowsData = []
    if len(ArtistShows) > 0:
      UpcomingShowsList = list(filter(lambda Show: Show.start_time > CurrentTime, ArtistShows))
      PastShowsList = list(filter(lambda Show: Show.start_time <= CurrentTime, ArtistShows))
      for UpcomingShow in UpcomingShowsList:
        VenueItem = db.session.query(Venue.id, Venue.name, Venue.image_link).filter_by(
          id=UpcomingShow.venue_id).first()
        UpcomingShowsData.append({'venue_id': VenueItem.id, 'venue_name': VenueItem.name,
                                  'venue_image_link': VenueItem.image_link,
                                  'start_time': str(UpcomingShow.start_time)})
      for PastShow in PastShowsList:
        VenueItem = db.session.query(Venue.id, Venue.name, Venue.image_link).filter_by(
          id=PastShow.venue_id).first()
        PastShowsData.append({'venue_id': VenueItem.id, 'venue_name': VenueItem.name,
                              'venue_image_link': VenueItem.image_link,
                              'start_time': str(PastShow.start_time)})
    data = {"id": ArtistItem.id, "name": ArtistItem.name, "genres": [ArtistItem.genres[0].value],
             "city": ArtistItem.city, "state": ArtistItem.state, "phone": ArtistItem.phone, "website": ArtistItem.website,
            "facebook_link": ArtistItem.facebook_link, "seeking_talent": ArtistItem.seeking_talent,
            "seeking_description": ArtistItem.seeking_description, "image_link": ArtistItem.image_link,
            "past_shows": PastShowsData, "upcoming_shows": UpcomingShowsData,"past_shows_count": len(PastShowsData),
            "upcoming_shows_count": len(UpcomingShowsData)}
  except:
    db.session.rollback()
    data = {}
  finally:
    db.session.close()
  return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = {}
    try:
      ArtistItem = Artist.query.get(artist_id)
      artist = {"id": ArtistItem.id, "name": ArtistItem.name, "genres": ArtistItem.genres, "city": ArtistItem.city,
               "state": ArtistItem.state, "phone": ArtistItem.phone, "website": ArtistItem.website,
               "facebook_link": ArtistItem.facebook_link, "seeking_talent": ArtistItem.seeking_talent,
               "seeking_description": ArtistItem.seeking_description, "image_link": ArtistItem.image_link}
    except:
      db.session.rollback()
      artist = {}
    finally:
      db.session.close()
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    try:
        artist = Artist.query.get(artist_id)
        artist.name = request.form.get('name')
        artist.city = request.form.get('city')
        artist.state = request.form.get('state')
        artist.phone = request.form.get('phone')
        artist.image_link = request.form.get('image_link')
        artist.facebook_link = request.form.get('facebook_link')
        GenreItem = []
        GenreItem.append(request.form.get('genres'))
        artist.genres = GenreItem
        artist.website = request.form.get('website')
        artist.seeking_description = request.form.get('seeking_description')
        seeking_talent = request.form.get('seeking_talent')
        seeking_talent_final = False
        if seeking_talent == "y":
            seeking_talent_final = True
        artist.seeking_talent = seeking_talent_final
        db.session.commit()
        flash('Artist ' + request.form.get('name') + ' was updated!')
    except:
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = {}
    try:
      VenueItem = Venue.query.get(venue_id)
      venue = {"id": VenueItem.id,"name": VenueItem.name,"genres": VenueItem.genres,"address": VenueItem.address,"city": VenueItem.city,
               "state": VenueItem.state,"phone": VenueItem.phone,"website": VenueItem.website,"facebook_link": VenueItem.facebook_link,
               "seeking_talent": VenueItem.seeking_talent,"seeking_description": VenueItem.seeking_description,"image_link": VenueItem.image_link}
    except:
        db.session.rollback()
        venue = {}
    finally:
        db.session.close()
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    try:
        venue = Venue.query.get(venue_id)
        venue.name = request.form.get('name')
        venue.city = request.form.get('city')
        venue.state = request.form.get('state')
        venue.address = request.form.get('address')
        venue.phone = request.form.get('phone')
        venue.image_link = request.form.get('image_link')
        venue.facebook_link = request.form.get('facebook_link')
        GenreItem = []
        GenreItem.append(request.form.get('genres'))
        venue.genres = GenreItem
        venue.website = request.form.get('website')
        venue.seeking_description = request.form.get('seeking_description')
        seeking_talent = request.form.get('seeking_talent')
        seeking_talent_final = False
        if seeking_talent == "y":
            seeking_talent_final = True
        venue.seeking_talent = seeking_talent_final
        db.session.commit()
        flash('Venue ' + request.form.get('name') + ' was updated!')
    except:
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    try:
        name = request.form.get('name')
        city = request.form.get('city')
        state = request.form.get('state')
        phone = request.form.get('phone')
        image_link = request.form.get('image_link')
        facebook_link = request.form.get('facebook_link')
        GenreItem = []
        GenreItem.append(request.form.get('genres'))
        genres = GenreItem
        website = request.form.get('website')
        seeking_description = request.form.get('seeking_description')
        seeking_talent = request.form.get('seeking_talent')
        seeking_talent_final = False
        if seeking_talent == "y":
            seeking_talent_final = True
        artist = Artist(name=name, city=city, state=state, phone=phone, image_link=image_link,
                        facebook_link=facebook_link, genres=genres, website=website,
                        seeking_description=seeking_description,
                        seeking_talent=seeking_talent_final)
        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + name + ' was successfully listed!')
    except:
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
        db.session.rollback()
    finally:
        db.session.close()
    return render_template('pages/home.html')

@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    name = ''
    message = ''
    try:
        name = Artist.query.filter_by(id=artist_id).first().name
        Artist.query.filter_by(id=artist_id).delete()
        db.session.commit()
        message = 'Artist ' + name + ' got deleted!'
        flash(message)
    except:
        db.session.rollback()
        message = 'Artist ' + name + ' did not deleted successfully!'
        flash(message)
    finally:
        db.session.close()
    return message

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  data = []
  try:
    ShowsList = db.session.query(Show.id, Show.artist_id, Show.venue_id, Show.start_time).all()
    for ShowItem in ShowsList:
      VenueItem = db.session.query(Venue.id, Venue.name).filter_by(id=ShowItem.venue_id).first()
      ArtistItem = db.session.query(Artist.id, Artist.name, Artist.image_link).filter_by(id=ShowItem.artist_id).first()
      data.append({'venue_id': VenueItem.id, 'venue_name': VenueItem.name, 'artist_id': ArtistItem.id,'artist_name': ArtistItem.name,
                   'artist_image_link': ArtistItem.image_link, 'start_time': str(ShowItem.start_time)})
  except:
    db.session.rollback()
    data = []
  finally:
    db.session.close()
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    try:
        artist_id = request.form.get('artist_id')
        venue_id = request.form.get('venue_id')
        start_time = request.form.get('start_time')
        VenueItem = Venue.query.get(venue_id)
        ArtistItem = Artist.query.get(artist_id)
        if VenueItem == None:
            flash('No Venue with such id.')
            db.session.rollback()
            db.session.close()
            return render_template('pages/home.html')
        if ArtistItem == None:
            flash('No Artist with such id.')
            db.session.rollback()
            db.session.close()
            return render_template('pages/home.html')
        show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
        db.session.add(show)
        db.session.commit()
        flash('Show was successfully listed!')
    except:
        flash('An error occurred. Show could not be listed.')
        db.session.rollback()
    finally:
        db.session.close()
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

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
