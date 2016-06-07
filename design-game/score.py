import endpoints
from protorpc import (
    remote,
    messages
)
from trueskill import TrueSkill

from messages import (
    GetScoreResponse,
    GetScoreForm,
    GetScoreForms,
    GetUserRankingResponse,
    GetUserRankingResponseList
)
from utils import (
    get_all_scores,
    get_game,
    get_game_score,
    get_all_users,
    get_user,
    get_user_score_orderby_game_score
)

GET_GAME_REQUEST = endpoints.ResourceContainer(
    user_name=messages.StringField(1, required=True),
    urlsafe_key=messages.StringField(2, required=True)
)
GET_USER_REQUEST = endpoints.ResourceContainer(
    user_name=messages.StringField(1, required=True)
)
GET_ALL_SCORE_REQUEST = endpoints.ResourceContainer(
    fetch=messages.IntegerField(1)
)

score_api = endpoints.api(name='score', version='v1')


@score_api.api_class(resource_name='score')
class ScoreApi(remote.Service):
    """Score APIs"""

    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=GetScoreResponse,
                      path='get_game_score',
                      name='get_game_score',
                      http_method='GET')
    def endpoint_get_game_score(self, request):
        """Get score of the game"""
        game = get_game(request.urlsafe_key, request.user_name)

        score = get_game_score(request.user_name, game)

        return GetScoreResponse(game_urlsafe_key=game.key.urlsafe(),
                                game_score=score.game_score,
                                timestamp=score.timestamp)

    @endpoints.method(request_message=GET_USER_REQUEST,
                      response_message=GetScoreForms,
                      path='get_user_scores',
                      name='get_user_scores',
                      http_method='GET')
    def endpoint_get_user_scores(self, request):
        """Get scores of a user ordered by game score"""
        scores = get_user_score_orderby_game_score(request.user_name)

        return GetScoreForms(
            items=[self._copy_score_to_form(score) for score in scores]
        )

    @endpoints.method(request_message=GET_ALL_SCORE_REQUEST,
                      response_message=GetScoreForms,
                      path='get_all_scores',
                      name='get_all_scores',
                      http_method='GET')
    def endpoint_get_all_scores(self, request):
        """Get all score ordered by game_score"""
        scores = get_all_scores(request.fetch)

        return GetScoreForms(
            items=[self._copy_score_to_form(score) for score in scores]
        )

    @endpoints.method(request_message=GET_USER_REQUEST,
                      response_message=GetUserRankingResponse,
                      path='get_user_ranking',
                      name='get_user_ranking',
                      http_method='GET')
    def endpoint_get_user_ranking(self, request):
        """Get ranking of a user"""
        user = get_user(request.user_name)

        # fetch only top 100 users
        users = get_all_users(100)

        # get leaderboard
        leaderboard = sorted(users, key=TrueSkill().expose, reverse=True)

        if user in leaderboard:
            user_ranking = leaderboard.index(user) + 1
        else:
            user_ranking = 0

        return GetUserRankingResponse(user_name=user.user_name,
                                      user_ranking=user_ranking,
                                      user_performance=user.mu)

    @endpoints.method(request_message=GET_ALL_SCORE_REQUEST,
                      response_message=GetUserRankingResponseList,
                      name='get_leaderboard',
                      path='get_leaderboard',
                      http_method='GET')
    def endpoint_get_leaderboard(self, request):
        """get leaderboard"""
        # fetch desired no. of users max 100
        if request.fetch > 100:
            users = get_all_users(100)
        else:
            users = get_all_users(request.fetch)

        # get leaderboard
        leaderboard = sorted(users, key=TrueSkill().expose, reverse=True)

        return GetUserRankingResponseList(
            rankings=[self._copy_ranking_response_to_list(user, leaderboard) for user in leaderboard]
        )

    @staticmethod
    def _copy_score_to_form(score):
        score_form = GetScoreForm()

        for field in score_form.all_fields():
            if field.name == 'urlsafe_game_key':
                setattr(score_form, field.name, getattr(score, 'game_key').urlsafe())
            elif hasattr(score, field.name):
                setattr(score_form, field.name, getattr(score, field.name))

        score_form.check_initialized()

        return score_form

    @staticmethod
    def _copy_ranking_response_to_list(user, leaderboard):
        user_ranking_resp = GetUserRankingResponse()

        for field in user_ranking_resp.all_fields():
            if field.name == 'user_performance':
                setattr(user_ranking_resp, field.name, user.mu)
            elif field.name == 'user_ranking':
                setattr(user_ranking_resp, field.name, leaderboard.index(user) + 1)
            elif hasattr(user, field.name):
                setattr(user_ranking_resp, field.name, getattr(user, field.name))

        user_ranking_resp.check_initialized()

        return user_ranking_resp
