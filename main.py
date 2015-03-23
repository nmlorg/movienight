# Copyright 2015 Daniel Reed <n@ml.org>

import json
import logging
import urllib2
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb


class Movie(ndb.Model):
  data = ndb.JsonProperty()

  @classmethod
  def Fetch(cls, imdb_id):
    ent = cls.get_by_id(imdb_id)
    if not ent:
      req = urllib2.Request('http://www.omdbapi.com/?i=%s&tomatoes=true' % (imdb_id,))
      logging.info('Fetching %r.', req.get_full_url())
      data = json.loads(urllib2.urlopen(req).read())
      ent = cls(key=ndb.Key(cls, imdb_id), data=data)
      ent.put()
    return ent


class User(ndb.Model):
  movies = ndb.TextProperty(repeated=True)


class GetMovies(webapp2.RequestHandler):
  def get(self):
    current_user = users.get_current_user()
    if not current_user:
      return self.redirect(users.create_login_url())

    user = User.get_by_id(current_user.email().lower())
    if not user:
      user = User(key=ndb.Key(User, current_user.email().lower()))
      user.put()

    movies = sorted(key.id() for key in Movie.query().iter(keys_only=True))

    self.response.content_type = 'application/json'
    json.dump({'all': movies, 'ranked': user.movies}, self.response)

  def put(self):
    current_user = users.get_current_user()
    if not current_user:
      return self.redirect(users.create_login_url())

    user = User.get_by_id(current_user.email().lower())
    if not user:
      user = User(key=ndb.Key(User, current_user.email().lower()))

    user.movies = json.loads(self.request.get('movies'))
    user.put()

    self.response.content_type = 'application/json'
    json.dump(user.movies, self.response)


class GetMovie(webapp2.RequestHandler):
  def get(self):
    imdb_id = self.request.get('imdb_id')
    movie = Movie.Fetch(imdb_id)
    self.response.content_type = 'application/json'
    json.dump(movie.data, self.response)


class GetRankings(webapp2.RequestHandler):
  def get(self):
    movies = {}
    for movie in Movie.query():
      movies[movie.key.id()] = d = movie.data.copy()
      d['overall'] = 0

    for user in User.query():
      for i, imdb_id in enumerate(user.movies):
        movies[imdb_id]['overall'] += 1. / (i + 1)

    movies = sorted(movies.itervalues(), key=lambda ent: -ent['overall'])
    self.response.content_type = 'application/json'
    json.dump(movies, self.response)


app = webapp2.WSGIApplication([
    ('/movies', GetMovies),
    ('/movie', GetMovie),
    ('/rankings', GetRankings),
], debug=True)
