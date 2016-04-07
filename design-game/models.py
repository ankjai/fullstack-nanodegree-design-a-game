from google.appengine.ext import ndb


class User(ndb.Model):
    """User Profile"""
    user_name = ndb.StringProperty(required=True)
    email = ndb.StringProperty()


class Game(ndb.Model):
    """Game Model"""
    user_key = ndb.KeyProperty(required=True, kind='User')
