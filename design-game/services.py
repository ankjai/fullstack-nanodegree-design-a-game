import endpoints

from game import game_api
from score import score_api
from user import user_api

api = endpoints.api_server([user_api, game_api, score_api])
