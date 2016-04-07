import endpoints
from protorpc import remote, messages

from messages import StringMessage
from models import User

USER_REQUEST = endpoints.ResourceContainer(user_name=messages.StringField(1), email=messages.StringField(2))

user_api = endpoints.api(name='user', version='v1')


@user_api.api_class(resource_name='user')
class UserApi(remote.Service):
    """User APIs"""

    @endpoints.method(request_message=USER_REQUEST,
                      response_message=StringMessage,
                      path='user',
                      name='create_user',
                      http_method='POST')
    def create_user(self, request):
        """Create user w/ unique username and email."""
        # check for unique username
        if User.query(User.user_name == request.user_name).get():
            raise endpoints.ConflictException('ERR_USERNAME_EXISTS: {}'
                                              .format(request.user_name))

        # check if user is already registered
        if User.query(User.email == request.email).get():
            raise endpoints.ConflictException('ERR_EMAIL_EXISTS: {}'.format(request.email))

        # create user
        user = User(user_name=request.user_name, email=request.email)
        user.put()

        return StringMessage(message="User with user_name={user_name} and email={email} created."
                             .format(user_name=request.user_name, email=request.email))
