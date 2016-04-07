from protorpc import messages


class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)


class NewGameForm(messages.Message):
    """New Game"""
    user_name = messages.StringField(1, required=True)
