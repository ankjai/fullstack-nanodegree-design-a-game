import endpoints
from protorpc import remote, messages

from models import User
from messages import StringMessage

USER_REQUEST = endpoints.ResourceContainer(user_name=messages.StringField(1), email=messages.StringField(2))

package = 'API'


@endpoints.api(name='userapi', version='v1')
class UserApi(remote.Service):
    """User APIs"""

    @endpoints.method(request_message=USER_REQUEST,
                      response_message=StringMessage,
                      path='user',
                      name='create_user',
                      http_method='POST')
    def create_user(self, request):
        """
        Create user w/ unique username and email.
        :param request: obj containing query params as requested in USER_REQUEST
        :return: StringMessage
        """
        # check for unique username
        if User.query(User.user_name == request.user_name).get():
            raise endpoints.ConflictException('User with username \'{}\' already exists, choose different username!'
                                              .format(request.user_name))

        # check if user is already registered
        if User.query(User.email == request.email).get():
            raise endpoints.ConflictException('User with email \'{}\' already exists!'.format(request.email))

        # create user
        user = User(user_name=request.user_name, email=request.email)
        user.put()

        return StringMessage(message="User with user_name={user_name} and email={email} created."
                             .format(user_name=request.user_name, email=request.email))


api = endpoints.api_server([UserApi])
