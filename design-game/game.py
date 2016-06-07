import endpoints
from google.appengine.ext import ndb
from protorpc import (
    remote,
    messages
)
from random_words import RandomWords
from trueskill import (
    Rating,
    rate_1vs1
)

from messages import (
    NewGameForm,
    NewGameResponse,
    GetGameResponse,
    GuessCharForm,
    GetActiveGameResponseList,
    GetActiveGameResponse,
    GetGameHistoryResponseList,
    GetGameHistoryResponse
)
from models import (
    Game,
    GameStatus,
    User,
    Score,
    GameHistory
)
from utils import (
    get_user,
    get_game,
    get_game_score,
    get_user_games,
    get_game_history
)

GET_USER_REQUEST = endpoints.ResourceContainer(
    user_name=messages.StringField(1, required=True)
)
GET_USER_WITH_GAME_STATUS_REQUEST = endpoints.ResourceContainer(
    user_name=messages.StringField(1, required=True),
    game_status=messages.EnumField(GameStatus, 2)
)
NEW_GAME_REQUEST = endpoints.ResourceContainer(
    NewGameForm,
    user_name=messages.StringField(1, required=True)
)
GET_GAME_REQUEST = endpoints.ResourceContainer(
    user_name=messages.StringField(1, required=True),
    urlsafe_key=messages.StringField(2, required=True)
)
GUESS_CHAR_REQUEST = endpoints.ResourceContainer(
    GuessCharForm,
    user_name=messages.StringField(1, required=True),
    urlsafe_key=messages.StringField(2, required=True)
)

game_api = endpoints.api(name='game', version='v1')


@game_api.api_class(resource_name='game')
class GameApi(remote.Service):
    """Game APIs"""

    @endpoints.method(request_message=NEW_GAME_REQUEST,
                      response_message=NewGameResponse,
                      path='new_game',
                      name='new_game',
                      http_method='POST')
    def endpoint_new_game(self, request):
        """Create new game."""
        user = get_user(request.user_name)

        game = self._new_game(user, request.game_name)

        return NewGameResponse(urlsafe_key=game.key.urlsafe())

    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=GetGameResponse,
                      path='get_game',
                      name='get_game',
                      http_method='GET')
    def endpoint_get_game(self, request):
        """Get game using game's urlsafe_key"""
        game = get_game(request.urlsafe_key, request.user_name)

        return GetGameResponse(id=game.game_id,
                               game_name=game.game_name,
                               word=game.word,
                               guessed_chars_of_word=game.guessed_chars_of_word,
                               guesses_left=game.guesses_left,
                               game_over=game.game_over,
                               game_status=game.game_status,
                               urlsafe_key=game.key.urlsafe())

    @endpoints.method(request_message=GUESS_CHAR_REQUEST,
                      response_message=GetGameResponse,
                      path='guess_char',
                      name='guess_char',
                      http_method='POST')
    def endpoint_guess_char(self, request):
        """Guess char of the word"""
        # only single char supported
        if len(request.char) != 1:
            raise endpoints.ForbiddenException('ERR_BAD_CHAR_LENGTH')

        # only alphabet supported
        if not request.char.isalpha():
            raise endpoints.ForbiddenException('ERR_NOT_AN_ALPHABET')

        user = get_user(request.user_name)

        game = get_game(request.urlsafe_key, user.user_name)

        # only IN_SESSION game supported
        if game.game_status != GameStatus.IN_SESSION:
            raise endpoints.ForbiddenException('ERR_GAME_NOT_IN_SESSION')

        score = get_game_score(user.user_name, game)

        self._move_game(game, user, score, request.char)

        return GetGameResponse(id=game.game_id,
                               game_name=game.game_name,
                               word=game.word,
                               guessed_chars_of_word=game.guessed_chars_of_word,
                               guesses_left=game.guesses_left,
                               game_over=game.game_over,
                               game_status=game.game_status,
                               urlsafe_key=game.key.urlsafe())

    @endpoints.method(request_message=GET_USER_WITH_GAME_STATUS_REQUEST,
                      response_message=GetActiveGameResponseList,
                      path='get_user_games',
                      name='get_user_games',
                      http_method='GET')
    def endpoint_get_user_games(self, request):
        """Get user's games list"""
        # get user object
        user = get_user(request.user_name)

        # get all games of this user
        all_games = get_user_games(user.user_name)

        if request.game_status is not None:
            # create filter for active games
            if request.game_status == GameStatus.IN_SESSION:
                active_filter = ndb.query.FilterNode('game_status', '=', GameStatus.IN_SESSION.number)
            elif request.game_status == GameStatus.WON:
                active_filter = ndb.query.FilterNode('game_status', '=', GameStatus.WON.number)
            elif request.game_status == GameStatus.LOST:
                active_filter = ndb.query.FilterNode('game_status', '=', GameStatus.LOST.number)
            elif request.game_status == GameStatus.ABORTED:
                active_filter = ndb.query.FilterNode('game_status', '=', GameStatus.ABORTED.number)

            # fetch games of this user
            active_games = all_games.filter(active_filter).fetch()
        else:
            # fetch games of this user
            active_games = all_games.fetch()

        return GetActiveGameResponseList(
            games=[self._create_active_game_list(active_game) for active_game in active_games]
        )

    @endpoints.method(request_message=GET_USER_REQUEST,
                      response_message=GetActiveGameResponseList,
                      path='get_user_completed_games',
                      name='get_user_completed_games',
                      http_method='GET')
    def endpoint_get_user_completed_games(self, request):
        """Get user's completed game list"""
        # get user object
        user = get_user(request.user_name)

        # get all games of this user
        all_games = get_user_games(user.user_name)

        # create filter for completed games
        completed_filter = ndb.query.FilterNode('game_status', '!=', GameStatus.IN_SESSION.number)

        # fetch all completed games of this user
        completed_games = all_games.filter(completed_filter).order(Game.game_status, -Game.game_id).fetch()

        return GetActiveGameResponseList(
            games=[self._create_active_game_list(game) for game in completed_games]
        )

    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=GetActiveGameResponse,
                      path='cancel_game',
                      name='cancel_game',
                      http_method='PATCH')
    def endpoint_cancel_game(self, request):
        """Cancel active game"""
        game = get_game(request.urlsafe_key, request.user_name)

        # only IN_SESSION game supported
        if game.game_status != GameStatus.IN_SESSION:
            raise endpoints.ForbiddenException('ERR_GAME_NOT_IN_SESSION')

        self._cancel_game(game)

        return GetActiveGameResponse(game_urlsafe_key=game.key.urlsafe(),
                                     game_id=game.game_id,
                                     game_name=game.game_name,
                                     game_over=game.game_over,
                                     game_status=game.game_status)

    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=GetGameHistoryResponseList,
                      path='get_game_history',
                      name='get_game_history',
                      http_method='GET')
    def endpoint_get_game_history(self, request):
        game = get_game(request.urlsafe_key, request.user_name)

        steps = get_game_history(game)

        return GetGameHistoryResponseList(
            steps=[self._create_game_histroy_list(step) for step in steps]
        )

    def _new_game(self, user, game_name):
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
        # save game
        game.put()

        # score id
        score_id = Score.allocate_ids(size=1, parent=user_key)[0]

        # score key using generated score_id and user as its ancestor
        score_key = ndb.Key(Score, score_id, parent=user_key)

        # score entity for this game
        score = Score(key=score_key,
                      score_id=score_id,
                      game_key=game_key)
        # save score
        score.put()

        # capture game snapshot
        self._capture_game_snapshot(game, '')

        return game

    def _move_game(self, game, user, score, char):
        # continue only if game is not over
        if game.game_over:
            return

        # chk if char exists in the word
        if char in game.word:
            for pos, char_in_that_pos in enumerate(game.word):
                if char_in_that_pos == char:
                    game.guessed_chars_of_word[pos] = char
            if '*' not in game.guessed_chars_of_word:
                game.game_over = True
                game.game_status = GameStatus.WON
                score.game_score = game.guesses_left
                self._update_user_rating(user, True)
        # in case of miss, reduce guesses_left
        elif game.guesses_left > 0:
            game.guesses_left -= 1
            if game.guesses_left == 0:
                game.game_over = True
                game.game_status = GameStatus.LOST
                self._update_user_rating(user, False)

        # save the game
        game.put()

        # save the score
        score.put()

        # capture game snapshot
        self._capture_game_snapshot(game, char)

    def _cancel_game(self, game):
        # return if game is already over
        if game.game_over:
            return game
        # cancel game and update status accordingly
        else:
            game.game_status = GameStatus.ABORTED
            game.game_over = True

        # save the game
        game.put()

        # capture game snapshot
        self._capture_game_snapshot(game, '')

    @staticmethod
    def _update_user_rating(user, user_winner):
        # create rating obj from user's mu and sigma
        user_rating = Rating(mu=user.mu, sigma=user.sigma)

        # create default rating obj
        default_rating = Rating()

        if user_winner:
            user_rating, default_rating = rate_1vs1(user_rating, default_rating)
        else:
            default_rating, user_rating = rate_1vs1(default_rating, user_rating)

        # update w/ new user rating
        user.mu = user_rating.mu
        user.sigma = user_rating.sigma

        # save the user
        user.put()

    @staticmethod
    def _capture_game_snapshot(game, char):
        # game history is per game, so parent should be game and not the user
        # game history id
        history_id = GameHistory.allocate_ids(size=1, parent=game.key)[0]

        # game history key generated using history_id and game as its ancestor
        history_key = ndb.Key(GameHistory, history_id, parent=game.key)

        game_history = GameHistory(key=history_key,
                                   step_char=char,
                                   game_snapshot=game)
        # save game history
        game_history.put()

    @staticmethod
    def _create_active_game_list(active_game):
        active_game_resp = GetActiveGameResponse()

        for field in active_game_resp.all_fields():
            if field.name == 'game_urlsafe_key':
                setattr(active_game_resp, field.name, active_game.key.urlsafe())
            elif hasattr(active_game, field.name):
                setattr(active_game_resp, field.name, getattr(active_game, field.name))

        active_game_resp.check_initialized()

        return active_game_resp

    @staticmethod
    def _create_game_histroy_list(step):
        game_history_resp = GetGameHistoryResponse()

        for field in game_history_resp.all_fields():
            if hasattr(step, field.name):
                setattr(game_history_resp, field.name, getattr(step, field.name))
            elif hasattr(step.game_snapshot, field.name):
                setattr(game_history_resp, field.name, getattr(step.game_snapshot, field.name))

        game_history_resp.check_initialized()

        return game_history_resp
