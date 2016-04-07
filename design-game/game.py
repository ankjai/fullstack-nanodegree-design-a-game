import endpoints
from protorpc import remote

from messages import StringMessage, NewGameForm
from models import User

NEW_GAME_REQUEST = endpoints.ResourceContainer(NewGameForm)

game_api = endpoints.api(name='game', version='v1')


@game_api.api_class(resource_name='game')
class GameApi(remote.Service):
    """Game APIs"""

    @endpoints.method(request_message=NEW_GAME_REQUEST,
                      response_message=StringMessage,
                      path='game',
                      name='new_game',
                      http_method='POST')
    def new_game(self, request):
        """Create new game."""
        user_name = User.query(User.user_name == request.user_name).get()

        if not user_name:
            raise endpoints.NotFoundException('ERR_USER_NOT_FOUND')

        return StringMessage(message='user {} exists!'.format(user_name))
