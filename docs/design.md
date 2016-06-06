#### Design Document

###### NDB Models

Code Path: `/fullstack-nanodegree-design-a-game/design-game/models.py`

`Enum: GameStatus`

| Value | Number | 
|---|---|
| IN_SESSION | 1 |
| WON | 2 |
| LOST | 3 |
| ABORTED | 4 |

`Model: User`

| Key | Property |
|---|---|
| user_name | StringProperty |
| email | StringProperty |
| display_name | StringProperty |
| mu | FloatProperty |
| sigma | FloatProperty |

`Model: Score`

| Key | Property |
|---|---|
| score_id | IntegerProperty |
| game_key | KeyProperty |
| timestamp | DateTimeProperty |
| game_score | IntegerProperty |

`Model: Game`

| Key | Property |
|---|---|
| game_id | IntegerProperty |
| game_name | StringProperty |
| word | StringProperty |
| guessed_chars_of_word | StringProperty |
| guesses_left | IntegerProperty |
| game_over | BooleanProperty |
| game_status | EnumProperty |
| timestamp | DateTimeProperty |

`Model: GameHistory`

| Key | Property |
|---|---|
| step_timestamp | DateTimeProperty |
| step_char | StringProperty |
| game_snapshot | StructuredProperty |


---


###### Messages/Resource Containers

Not going to list all response messages and forms for resource container here, but you can refer them in `messages.py`  
Code Path: `/fullstack-nanodegree-design-a-game/design-game/messages.py`

---


###### Endpoints

For the 'Hangman Game', I have exposed 3 APIs:

| API | Path | Version | Endpoints |
|---|---|---|---|
| User | /user | /v1 | /create_user, /get_user, /update_user, /delete_user |
| Score | /score | /v1 | /get_game_score, /get_user_scores, /get_all_scores, /get_user_ranking, /get_leaderboard |
| Game | /game | /v1 | /new_game, /get_game, /guess_char, /get_user_games, /get_user_completed_games, /cancel_game, /get_game_history |

Full API usage [here](docs/api_usage.md)

---


###### Scoring Impl

Current scoring logic is straight forward, no. of guesses left when player guesses the word is his/her score. But down the path we will have score game depending upon the word length/toughness.

---


###### Ranking Impl

For ranking players, game is using [TrueSkill](http://trueskill.org/). 

TrueSkill is a rating system among game players. It was developed by Microsoft Research and has been used on Xbox LIVE for ranking and matchmaking service. This system quantifies players’ TRUE skill points by the Bayesian inference algorithm. It also works well with any type of match rule including N:N team game or free-for-all.

The game is using [Head-to-head (1 vs. 1)](http://trueskill.org/#head-to-head-1-vs-1-match-rule) match rule to rank players.