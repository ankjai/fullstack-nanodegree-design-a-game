import endpoints
from google.appengine.ext import ndb
from protorpc import remote

from messages import GetUserForm, NewGameForm, NewGameResponse, GetGameForm, GetGameResponse, GuessCharForm, \
    GetScoreResponse, GetScoreForm, GetScoreForms, GetAllScoreForm
from models import User, Game, Score

GET_USER_REQUEST = endpoints.ResourceContainer(GetUserForm)
NEW_GAME_REQUEST = endpoints.ResourceContainer(NewGameForm)
GET_GAME_REQUEST = endpoints.ResourceContainer(GetGameForm)
GUESS_CHAR_REQUEST = endpoints.ResourceContainer(GuessCharForm)
GET_ALL_SCORE_REQUEST = endpoints.ResourceContainer(GetAllScoreForm)

game_api = endpoints.api(name='game', version='v1')


@game_api.api_class(resource_name='game')
class GameApi(remote.Service):
    """Game APIs"""

    @endpoints.method(request_message=NEW_GAME_REQUEST,
                      response_message=NewGameResponse,
                      path='new_game',
                      name='new_game',
                      http_method='POST')
    def new_game(self, request):
        """Create new game."""
        user = User.query(User.user_name == request.user_name).get()

        if not user:
            raise endpoints.NotFoundException('ERR_USER_NOT_FOUND')

        game = Game.new_game(user, request.game_name)

        return NewGameResponse(urlsafe_key=game.key.urlsafe())

    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=GetGameResponse,
                      path='get_game',
                      name='get_game',
                      http_method='POST')
    def get_game(self, request):
        """Get game using game's urlsafe_key"""
        game = self._get_game(request)

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
    def guess_char(self, request):
        """Guess char of the word"""
        game = self._get_game(request)

        score = self._get_game_score(request, game)

        game = game.move_game(score, request.char)

        return GetGameResponse(game_name=game.game_name,
                               word=game.word,
                               guessed_chars_of_word=game.guessed_chars_of_word,
                               guesses_left=game.guesses_left,
                               game_over=game.game_over,
                               game_status=game.game_status,
                               urlsafe_key=game.key.urlsafe())

    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=GetScoreResponse,
                      path='get_game_score',
                      name='get_game_score',
                      http_method='POST')
    def get_game_score(self, request):
        """Get score of the game"""
        game = self._get_game(request)

        score = self._get_game_score(request, game)

        return GetScoreResponse(game_urlsafe_key=game.key.urlsafe(),
                                game_score=score.game_score,
                                timestamp=score.timestamp)

    @endpoints.method(request_message=GET_USER_REQUEST,
                      response_message=GetScoreForms,
                      path='get_user_scores',
                      name='get_user_scores',
                      http_method='POST')
    def get_user_scores(self, request):
        """Get scores of a user"""
        scores = self._get_user_score(request)
        return GetScoreForms(
            items=[self._copy_score_to_form(score) for score in scores]
        )

    @endpoints.method(request_message=GET_ALL_SCORE_REQUEST,
                      response_message=GetScoreForms,
                      path='get_all_scores',
                      name='get_all_scores',
                      http_method='POST')
    def get_all_scores(self, request):
        """Get all score ordered by game_score"""
        scores = self._get_all_scores(request)
        return GetScoreForms(
            items=[self._copy_score_to_form(score) for score in scores]
        )

    @staticmethod
    def _get_game(request):
        #  get game
        game = ndb.Key(urlsafe=request.urlsafe_key).get()

        # get games by ancestor
        game_filtered_by_ancestor = Game.query(ancestor=ndb.Key(User, request.user_name))

        # create filter
        game_filter = ndb.query.FilterNode('game_id', '=', game.game_id)

        # filter ancestor games
        filtered_game = game_filtered_by_ancestor.filter(game_filter).get()

        if filtered_game is None:
            raise endpoints.UnauthorizedException('ERR_UNAUTHORIZED')

        return filtered_game

    @staticmethod
    def _get_game_score(request, game):
        # get score by ancestor
        score_filtered_by_ancestor = GameApi._get_user_score(request)

        # create score filter
        score_filter = ndb.query.FilterNode('game_key', '=', game.key)

        # filter ancestor scores
        score = score_filtered_by_ancestor.filter(score_filter).get()

        return score

    @staticmethod
    def _get_user_score(request):
        # get score by ancestor
        return Score.query(ancestor=ndb.Key(User, request.user_name))

    @staticmethod
    def _get_all_scores(request):
        # query by kind
        query = Score.query()

        # order by game_score
        query.order(Score.game_score)

        # fetch no. of result as requested
        if request.fetch is not None:
            return query.fetch(request.fetch)
        else:
            return query.fetch()

    @staticmethod
    def _copy_score_to_form(score):
        gsf = GetScoreForm()

        for field in gsf.all_fields():
            if field.name == 'urlsafe_game_key':
                setattr(gsf, field.name, getattr(score, 'game_key').urlsafe())
            elif hasattr(score, field.name):
                setattr(gsf, field.name, getattr(score, field.name))

        gsf.check_initialized()

        return gsf
