import endpoints

from user import user_api
from game import game_api

api = endpoints.api_server([user_api, game_api])
