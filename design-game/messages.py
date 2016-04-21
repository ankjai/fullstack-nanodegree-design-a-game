from protorpc import messages, message_types

from models import GameStatus


class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)


class UserResponse(messages.Message):
    user_name = messages.StringField(1, required=True)
    email = messages.StringField(2, required=True)
    display_name = messages.StringField(3)


class NewGameResponse(messages.Message):
    urlsafe_key = messages.StringField(1, required=True)


class GetGameResponse(messages.Message):
    game_name = messages.StringField(1)
    word = messages.StringField(2)
    guessed_chars_of_word = messages.StringField(3, repeated=True)
    guesses_left = messages.IntegerField(4)
    game_over = messages.BooleanField(5)
    game_status = messages.EnumField(GameStatus, 6)
    urlsafe_key = messages.StringField(7, required=True)


class GetScoreResponse(messages.Message):
    game_urlsafe_key = messages.StringField(1)
    game_score = messages.IntegerField(2)
    timestamp = message_types.DateTimeField(3)


class GetActiveGameResponse(messages.Message):
    game_urlsafe_key = messages.StringField(1)
    game_id = messages.IntegerField(2)
    game_name = messages.StringField(3)
    game_over = messages.BooleanField(4)
    game_status = messages.EnumField(GameStatus, 5)


class GetActiveGameResponseList(messages.Message):
    games = messages.MessageField(GetActiveGameResponse, 1, repeated=True)


class GetUserRankingResponse(messages.Message):
    user_name = messages.StringField(1, required=True)
    user_ranking = messages.IntegerField(2, required=True)
    user_performance = messages.FloatField(3, required=True)


class GetUserRankingResponseList(messages.Message):
    rankings = messages.MessageField(GetUserRankingResponse, 1, repeated=True)


class GetGameHistoryResponse(messages.Message):
    step_timestamp = message_types.DateTimeField(1, required=True)
    step_char = messages.StringField(2)
    guessed_chars_of_word = messages.StringField(3, repeated=True)
    guesses_left = messages.IntegerField(4)
    game_over = messages.BooleanField(5)
    game_status = messages.EnumField(GameStatus, 6)
    word = messages.StringField(7)


class GetGameHistoryResponseList(messages.Message):
    steps = messages.MessageField(GetGameHistoryResponse, 1, repeated=True)


# ------ Forms ---------
class CreateUserForm(messages.Message):
    """Create User"""
    user_name = messages.StringField(1, required=True)
    email = messages.StringField(2, required=True)
    display_name = messages.StringField(3)


class UpdateUserForm(messages.Message):
    """Update User"""
    current_user_name = messages.StringField(1, required=True)
    user_name = messages.StringField(2)
    email = messages.StringField(3)
    display_name = messages.StringField(4)


class GetUserForm(messages.Message):
    """Get User"""
    user_name = messages.StringField(1, required=True)


class NewGameForm(messages.Message):
    """New Game"""
    user_name = messages.StringField(1, required=True)
    game_name = messages.StringField(2)


class GetGameForm(messages.Message):
    """Get Game"""
    user_name = messages.StringField(1, required=True)
    urlsafe_key = messages.StringField(2, required=True)


class GuessCharForm(messages.Message):
    """Guess Char of the Word"""
    user_name = messages.StringField(1, required=True)
    urlsafe_key = messages.StringField(2, required=True)
    char = messages.StringField(3, required=True)


class GetScoreForm(messages.Message):
    """Get Score"""
    score_id = messages.IntegerField(1, required=True)
    urlsafe_game_key = messages.StringField(2, required=True)
    timestamp = message_types.DateTimeField(3)
    game_score = messages.IntegerField(4)


class GetScoreForms(messages.Message):
    """Multi GetScoreForm"""
    items = messages.MessageField(GetScoreForm, 1, repeated=True)


class GetAllScoreForm(messages.Message):
    """Get All Scores"""
    fetch = messages.IntegerField(1)
