import endpoints
from google.appengine.ext import ndb
from protorpc import remote, messages

from messages import UserResponse
from models import User

USER_REQUEST = endpoints.ResourceContainer(user_name=messages.StringField(1),
                                           email=messages.StringField(2),
                                           display_name=messages.StringField(3))

user_api = endpoints.api(name='user', version='v1')


@user_api.api_class(resource_name='user')
class UserApi(remote.Service):
    """User APIs"""

    @endpoints.method(request_message=USER_REQUEST,
                      response_message=UserResponse,
                      path='user',
                      name='create_user',
                      http_method='POST')
    def create_user(self, request):
        """Create user w/ unique username and email."""
        # check for empty user_name
        if not request.user_name:
            raise endpoints.BadRequestException('ERR_EMPTY_USERNAME')

        # check for empty email
        if not request.email:
            raise endpoints.BadRequestException('ERR_EMPTY_EMAIL')

        # check for unique username
        if User.query(User.user_name == request.user_name).get():
            raise endpoints.ConflictException('ERR_USERNAME_EXISTS: {}'.format(request.user_name))

        # check if user is already registered
        if User.query(User.email == request.email).get():
            raise endpoints.ConflictException('ERR_EMAIL_EXISTS: {}'.format(request.email))

        # create user
        user = User(key=ndb.Key(User, request.user_name),
                    user_name=request.user_name,
                    email=request.email,
                    display_name=request.display_name)
        user.put()

        return UserResponse(user_name=user.user_name, email=user.email, display_name=user.display_name)
