# Copyright 2015 Daniel Reed <n@ml.org>

import json
import logging
import urllib2
import webapp2
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


class GetMovies(webapp2.RequestHandler):
  def get(self):
    ret = [key.id() for key in Movie.query().iter(keys_only=True)]
    self.response.content_type = 'application/json'
    json.dump(ret, self.response)


class GetMovie(webapp2.RequestHandler):
  def get(self):
    imdb_id = self.request.get('imdb_id')
    movie = Movie.Fetch(imdb_id)
    self.response.content_type = 'application/json'
    json.dump(movie.data, self.response)


app = webapp2.WSGIApplication([
    ('/movies', GetMovies),
    ('/movie', GetMovie),
], debug=True)
