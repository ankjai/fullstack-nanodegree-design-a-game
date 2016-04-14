from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from protorpc import messages
from random_words import RandomWords


class User(ndb.Model):
    """User Profile"""
    user_name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    display_name = ndb.StringProperty()


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

    @classmethod
    def new_game(cls, user, game_name):
        # retrieve key from user_name
        user_key = ndb.Key(User, user.user_name)

        # generate game_id
        game_id = Game.allocate_ids(size=1, parent=user_key)[0]

        # create key using generated game_id and user as its ancestor
        game_key = ndb.Key(Game, game_id, parent=user_key)

        # generate random word for this game
        rw = RandomWords()
        word = rw.random_word()

        guessed_chars_of_word = []

        # make this impl more 'pythonic' way
        for c in word:
            guessed_chars_of_word.append('*')

        game = Game(key=game_key,
                    game_id=game_id,
                    game_name=game_name,
                    word=word,
                    guessed_chars_of_word=guessed_chars_of_word)
        game.put()

        # score id
        score_id = Score.allocate_ids(size=1, parent=user_key)[0]

        # score key using generated score_id and user as its ancestor
        score_key = ndb.Key(Score, score_id, parent=user_key)

        # score entity for this game
        score = Score(key=score_key,
                      score_id=score_id,
                      game_key=game_key)
        score.put()

        return game

    def move_game(self, score, char):
        # continue only if game is not over
        if self.game_over:
            return self
        # chk if char exists in the word
        elif char in self.word:
            for pos, char_in_that_pos in enumerate(self.word):
                if char_in_that_pos == char:
                    self.guessed_chars_of_word[pos] = char
            if '*' not in self.guessed_chars_of_word:
                self.game_over = True
                self.game_status = GameStatus.WON
                score.game_score = self.guesses_left
        # in case of miss, reduce guesses_left
        elif self.guesses_left > 0:
            self.guesses_left -= 1
            if self.guesses_left == 0:
                self.game_over = True
                self.game_status = GameStatus.LOST

        # save the game
        self.put()

        # save the score
        score.put()

        return self


class Score(ndb.Model):
    """Score Model"""
    score_id = ndb.IntegerProperty(required=True)
    game_key = ndb.KeyProperty(required=True, kind='Game')
    timestamp = ndb.DateTimeProperty(required=True, auto_now_add=True)
    game_score = ndb.IntegerProperty(required=True, default=0)
