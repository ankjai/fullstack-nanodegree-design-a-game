## Project: Design a Game
Designed a scalable game(hangman) app using Google App Engine backed by Google Datastore.

---


#### How to play 'Hangman'
Hangman is a paper and pencil guessing game for two or more players. One player thinks of a word, phrase or sentence and the other tries to guess it by suggesting letters or numbers, within a certain number of guesses.

This implementation is a one player game. The word is provided by the app and player has to guess char in every step, if user is unable to guess the word in 6 steps player looses.

For more information on game, check wikipedia page [here](https://en.wikipedia.org/wiki/Hangman_%28game%29)

For actual 'Hangman' game app (consuming these APIs), checkout [hangman_game_frontend](https://github.com/ankjai/hangman_game_frontend) project.

---

#### How to access APIs
`Method: POST`  
`Content-Type: application/json`  
```
BASE_URL = "https://design-game.appspot.com/_ah/api"
```

Read full API usage [here](docs/api_usage.md)  

---

#### Cron Job
`/crons/send_email_reminders`  
Send reminders to players who have not made any move in past 24 hrs.  
Scheduled everyday at: `06:00 GMT`  

---

#### Frontend to test APIs  
Refer [hangman_game_frontend](https://github.com/ankjai/hangman_game_frontend) backbone.js UI project which is designed using APIs exposed by this project.  
