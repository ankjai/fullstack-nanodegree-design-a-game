from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from protorpc import messages


class User(ndb.Model):
    """User Profile"""
    user_name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    display_name = ndb.StringProperty()
    mu = ndb.FloatProperty(required=True)
    sigma = ndb.FloatProperty(required=True)


class GameStatus(messages.Enum):
    """Game Statuses Enum"""
    IN_SESSION = 1
    WON = 2
    LOST = 3
    ABORTED = 4


class Game(ndb.Model):
    """Game Model"""
    game_id = ndb.IntegerProperty(required=True)
    game_name = ndb.StringProperty()
    word = ndb.StringProperty(required=True)
    guessed_chars_of_word = ndb.StringProperty(repeated=True)
    guesses_left = ndb.IntegerProperty(default=6)
    game_over = ndb.BooleanProperty(default=False)
    game_status = msgprop.EnumProperty(GameStatus, default=GameStatus.IN_SESSION)
    timestamp = ndb.DateTimeProperty(required=True, auto_now=True)


class Score(ndb.Model):
    """Score Model"""
    score_id = ndb.IntegerProperty(required=True)
    game_key = ndb.KeyProperty(required=True, kind='Game')
    timestamp = ndb.DateTimeProperty(required=True, auto_now_add=True)
    game_score = ndb.IntegerProperty(required=True, default=0)


class GameHistory(ndb.Model):
    """Game History Model"""
    step_timestamp = ndb.DateTimeProperty(required=True, auto_now_add=True)
    step_char = ndb.StringProperty()
    game_snapshot = ndb.StructuredProperty(Game)
