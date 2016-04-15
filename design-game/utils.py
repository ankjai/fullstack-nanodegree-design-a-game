import endpoints

from models import User


def get_user(user_name):
    user = User.query(User.user_name == user_name).get()
    if not user:
        raise endpoints.NotFoundException('ERR_USER_NOT_FOUND')
    return user
