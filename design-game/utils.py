import endpoints
from google.appengine.ext import ndb

from models import (
    User,
    Game,
    Score,
    GameHistory
)


def get_user(user_name):
    user = User.query(User.user_name == user_name).get()

    if not user:
        raise endpoints.NotFoundException('ERR_USER_NOT_FOUND')

    return user


def get_game(urlsafe_key, user_name):
    #  get game
    game = ndb.Key(urlsafe=urlsafe_key).get()

    # get games by ancestor
    game_filtered_by_ancestor = get_user_games(user_name)

    # create filter
    game_filter = ndb.query.FilterNode('game_id', '=', game.game_id)

    # filter ancestor games
    filtered_game = game_filtered_by_ancestor.filter(game_filter).get()

    if filtered_game is None:
        raise endpoints.UnauthorizedException('ERR_UNAUTHORIZED')

    return filtered_game


def get_user_games(user_name):
    # get game by ancestor
    return Game.query(ancestor=ndb.Key(User, user_name))


def get_game_score(user_name, game):
    # get score by ancestor
    score_filtered_by_ancestor = get_user_score(user_name)

    # create score filter
    score_filter = ndb.query.FilterNode('game_key', '=', game.key)

    # filter ancestor scores
    score = score_filtered_by_ancestor.filter(score_filter).get()

    return score


def get_user_score(user_name):
    # get score by ancestor
    return Score.query(ancestor=ndb.Key(User, user_name))


def get_user_score_orderby_game_score(user_name):
    query = get_user_score(user_name)

    # order by game_score
    query.order(Score.game_score)

    return query.fetch()


def get_all_scores(fetch):
    # query by kind
    query = Score.query()

    # order by game_score
    query.order(Score.game_score)

    # fetch no. of result as requested
    if fetch is not None:
        return query.fetch(fetch)
    else:
        return query.fetch()


def get_all_users(fetch):
    # query by kind
    query = User.query()

    # order by mu
    query.order(User.mu)

    # fetch no. of result as requested
    if fetch is not None:
        return query.fetch(fetch)
    else:
        return query.fetch()


def get_game_history(game):
    # query by kind
    query = GameHistory.query(ancestor=game.key)

    # order by timestamp
    query.order(GameHistory.step_timestamp)

    return query.fetch()
