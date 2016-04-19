import endpoints
from google.appengine.ext import ndb
from protorpc import remote

from messages import GetUserForm, NewGameForm, NewGameResponse, GetGameForm, GetGameResponse, GuessCharForm, \
    GetActiveGameResponseList, GetActiveGameResponse
from models import Game, GameStatus
from utils import get_user, get_game, get_game_score, get_user_games

GET_USER_REQUEST = endpoints.ResourceContainer(GetUserForm)
NEW_GAME_REQUEST = endpoints.ResourceContainer(NewGameForm)
GET_GAME_REQUEST = endpoints.ResourceContainer(GetGameForm)
GUESS_CHAR_REQUEST = endpoints.ResourceContainer(GuessCharForm)

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

        game = Game.new_game(user, request.game_name)

        return NewGameResponse(urlsafe_key=game.key.urlsafe())

    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=GetGameResponse,
                      path='get_game',
                      name='get_game',
                      http_method='POST')
    def endpoint_get_game(self, request):
        """Get game using game's urlsafe_key"""
        game = get_game(request.urlsafe_key, request.user_name)

        return GetGameResponse(game_name=game.game_name,
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
        user = get_user(request.user_name)

        game = get_game(request.urlsafe_key, user.user_name)

        score = get_game_score(user.user_name, game)

        game.move_game(user, score, request.char)

        return GetGameResponse(game_name=game.game_name,
                               word=game.word,
                               guessed_chars_of_word=game.guessed_chars_of_word,
                               guesses_left=game.guesses_left,
                               game_over=game.game_over,
                               game_status=game.game_status,
                               urlsafe_key=game.key.urlsafe())

    @endpoints.method(request_message=GET_USER_REQUEST,
                      response_message=GetActiveGameResponseList,
                      path='get_user_active_games',
                      name='get_user_active_games',
                      http_method='POST')
    def endpoint_get_user_active_games(self, request):
        """Get user's active games list"""
        # get user object
        user = get_user(request.user_name)

        # get all games of this user
        all_games = get_user_games(user.user_name)

        # create filter for active games
        active_filter = ndb.query.FilterNode('game_status', '=', GameStatus.IN_SESSION.number)

        # fetch all active games of this user
        active_games = all_games.filter(active_filter).fetch()

        return GetActiveGameResponseList(
            games=[self._create_active_game_list(active_game) for active_game in active_games]
        )

    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=GetActiveGameResponse,
                      path='cancel_game',
                      name='cancel_game',
                      http_method='POST')
    def endpoint_cancel_game(self, request):
        """Cancel active game"""
        game = get_game(request.urlsafe_key, request.user_name)

        game.cancel_game()

        return GetActiveGameResponse(game_urlsafe_key=game.key.urlsafe(),
                                     game_id=game.game_id,
                                     game_name=game.game_name,
                                     game_over=game.game_over,
                                     game_status=game.game_status)

    @staticmethod
    def _create_active_game_list(active_game):
        gagr = GetActiveGameResponse()

        for field in gagr.all_fields():
            if field.name == 'game_urlsafe_key':
                setattr(gagr, field.name, active_game.key.urlsafe())
            elif hasattr(active_game, field.name):
                setattr(gagr, field.name, getattr(active_game, field.name))

        gagr.check_initialized()

        return gagr
