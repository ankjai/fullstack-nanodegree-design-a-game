import endpoints
from google.appengine.ext import ndb
from protorpc import (
    remote,
    messages,
    message_types
)
from trueskill import Rating

from messages import UserResponse, CreateUserForm, UpdateUserForm
from models import User
from utils import get_user

CREATE_USER_REQUEST = endpoints.ResourceContainer(CreateUserForm)
GET_USER_REQUEST = endpoints.ResourceContainer(
    user_name=messages.StringField(1, required=True)
)
UPDATE_USER_REQUEST = endpoints.ResourceContainer(
    UpdateUserForm,
    current_user_name=messages.StringField(1, required=True)
)

user_api = endpoints.api(name='user', version='v1')


@user_api.api_class(resource_name='user')
class UserApi(remote.Service):
    """User APIs"""

    @endpoints.method(request_message=CREATE_USER_REQUEST,
                      response_message=UserResponse,
                      path='create_user',
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

        # create rating obj for new user
        user_default_rating = Rating()

        # create user
        user = User(key=ndb.Key(User, request.user_name),
                    user_name=request.user_name,
                    email=request.email,
                    display_name=request.display_name,
                    mu=user_default_rating.mu,
                    sigma=user_default_rating.sigma)
        user.put()

        return UserResponse(user_name=user.user_name, email=user.email, display_name=user.display_name)

    @endpoints.method(request_message=GET_USER_REQUEST,
                      response_message=UserResponse,
                      path='get_user',
                      name='get_user',
                      http_method='GET')
    def get_user(self, request):
        """Get existing user"""
        user = get_user(request.user_name)
        return UserResponse(user_name=user.user_name, email=user.email, display_name=user.display_name)

    @endpoints.method(request_message=UPDATE_USER_REQUEST,
                      response_message=UserResponse,
                      path='update_user',
                      name='update_user',
                      http_method='PATCH')
    def update_user(self, request):
        """Update existing user"""
        user = get_user(request.current_user_name)

        for field in request.all_fields():
            # check if any field has been updated
            if getattr(request, field.name) and field.name is not 'current_user_name':
                setattr(user, field.name, getattr(request, field.name))

        user.put()

        return UserResponse(user_name=user.user_name, email=user.email, display_name=user.display_name)

    @endpoints.method(request_message=GET_USER_REQUEST,
                      response_message=message_types.VoidMessage,
                      path='delete_user',
                      name='delete_user',
                      http_method='DELETE')
    def delete_user(self, request):
        """Delete existing user"""
        user = get_user(request.user_name)

        # delete the entity
        user.key.delete()

        return message_types.VoidMessage()
