#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import datetime

import webapp2
from google.appengine.api import mail
from google.appengine.ext import ndb

from models import GameStatus
from utils import (
    get_all_users,
    get_user_games
)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')


class SendEmailReminderHandler(webapp2.RequestHandler):
    @staticmethod
    def get_email_list():
        email_list = []

        timestamp = datetime.datetime.now() - datetime.timedelta(hours=24)

        users = get_all_users(100)

        for user in users:
            all_games = get_user_games(user.user_name)
            # filter for active games
            active_game_filter = ndb.query.FilterNode('game_status', '=', GameStatus.IN_SESSION.number)
            # filter for timestamp
            timestamp_filter = ndb.query.FilterNode('timestamp', '<', timestamp)
            # fetch filtered games of this user
            filtered_games = all_games.filter(active_game_filter, timestamp_filter).fetch()
            if filtered_games:
                email_list.append(user.email)

        return email_list

    @staticmethod
    def get():
        email_list = SendEmailReminderHandler.get_email_list()
        for email in email_list:
            mail.send_mail(sender="ankit.jaiswal@gmail.com",
                           to=email,
                           subject="Make your move!",
                           body="""
                           Dear Player,

                           You have not made your move in past 24 hrs. Login to your game account
                           and guess a char.

                           Regards,
                           Hangman Game Team
                           """)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/crons/send_email_reminders', SendEmailReminderHandler)
], debug=True)
