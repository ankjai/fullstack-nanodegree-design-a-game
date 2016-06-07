#### API Usage

```
BASE_URL = "https://design-game.appspot.com/_ah/api"
```

Note: Append the API endpoints to base URL to access them
```
For E.g.: https://design-game.appspot.com/_ah/api/user/v1/get_user?user_name=<data>
```

---

###### User APIs

**_Create User_**  
`POST /user/v1/create_user`   
`Content-Type: application/json`  

Request:
```
{
 "display_name": "<data>",
 "email": "<data>",
 "user_name": "<data>"
}
```  
Response:  
```
200 OK  
{
 "display_name": "<data>",
 "email": "<data>",
 "user_name": "<data>"
}
```

**_Get User_**  
`GET /user/v1/get_user?user_name=<data>`  

Response:  
```
200 OK  
{
 "display_name": "<data>",
 "email": "<data>",
 "user_name": "<data>"
}
```

**_Update User_**  
`PATCH /user/v1/update_user?current_user_name=<data>`  
`Content-Type: application/json`  
Request:
```
{
 "display_name": "<data>",
 "email": "<data>",
 "user_name": "<data>"
}
```
Response:  
```
200 OK  
{
 "display_name": "<data>",
 "email": "<data>",
 "user_name": "<data>"
}
```

**_Delete User_**  
`DELETE /user/v1/delete_user?user_name=<data>`  
Response:
```
204  
<NO CONTENT>
```


---


###### Score APIs

**_Get All Scores_**  
`GET /score/v1/get_all_scores?fetch=<no. of score items ordered by score desc>`  

Response:  
```
200 OK  
{
 "items": [
  {
   "game_score": "6",
   "score_id": "2",
   "timestamp": "2016-06-01T22:02:35.505889",
   "urlsafe_game_key": "ag9kZXZ-ZGVzaWduLWdhbWVyKwsSBFVzZXIiF2Fua2l0LmphaXN3YWxAZ21haWwuY29tDAsSBEdhbWUYAQw"
  }
 ]
}
```  

**_Get Game Score_**  
`GET /score/v1/get_game_score?user_name=<data>&urlsafe_key=<data>`  

Response:  
```
200 OK  
{
 "game_score": "6",
 "game_urlsafe_key": "ag9kZXZ-ZGVzaWduLWdhbWVyKwsSBFVzZXIiF2Fua2l0LmphaXN3YWxAZ21haWwuY29tDAsSBEdhbWUYAQw",
 "timestamp": "2016-06-01T22:02:35.505889"
}
```  

**_Get Leaderboard_**  
`GET /score/v1/get_leaderboard?fetch=<no. of score items ordered by score desc>`  

Response:  
```
200 OK  
{
 "rankings": [
  {
   "user_name": "<data>",
   "user_performance": 29.39583201999916,
   "user_ranking": "1"
  }
 ]
}
```  

**_Get User Ranking_**  
`GET /score/v1/get_user_ranking?user_name=<data>`  

Response:  
```
200 OK  
{
 "user_name": "<data>",
 "user_performance": 29.39583201999916,
 "user_ranking": "1"
}
```  

**_Get User Scores_**  
`GET /score/v1/get_user_scores?user_name=<data>`  

Response:  
```
200 OK  
{
 "items": [
  {
   "game_score": "6",
   "score_id": "2",
   "timestamp": "2016-06-01T22:02:35.505889",
   "urlsafe_game_key": "ag9kZXZ-ZGVzaWduLWdhbWVyKwsSBFVzZXIiF2Fua2l0LmphaXN3YWxAZ21haWwuY29tDAsSBEdhbWUYAQw"
  },
  {
   "game_score": "0",
   "score_id": "12",
   "timestamp": "2016-06-01T22:03:26.264853",
   "urlsafe_game_key": "ag9kZXZ-ZGVzaWduLWdhbWVyKwsSBFVzZXIiF2Fua2l0LmphaXN3YWxAZ21haWwuY29tDAsSBEdhbWUYCww"
  }
 ]
}
```  


---


###### Game APIs

**_Get Game_**  
`GET /game/v1/get_game?user_name=<data>&urlsafe_key=<data>`  

Response:  
```
200 OK  
{
 "game_name": "1464818604901",
 "game_over": false,
 "game_status": "IN_SESSION",
 "guessed_chars_of_word": [
  "*",
  "*",
  "*",
  "*",
  "*",
  "*"
 ],
 "guesses_left": "6",
 "id": "11",
 "urlsafe_key": "ag9kZXZ-ZGVzaWduLWdhbWVyKwsSBFVzZXIiF2Fua2l0LmphaXN3YWxAZ21haWwuY29tDAsSBEdhbWUYCww",
 "word": "clouds"
}
```  

**_Get Game History_**  
`GET /game/v1/get_game_history?user_name=<data>&urlsafe_key=<data>`  

Response:  
```
200 OK  
{
 "steps": [
  {
   "game_over": false,
   "game_status": "IN_SESSION",
   "guessed_chars_of_word": [
    "*",
    "*",
    "*",
    "*",
    "*",
    "*"
   ],
   "guesses_left": "6",
   "step_char": "",
   "step_timestamp": "2016-06-01T22:03:26.276687",
   "word": "clouds"
  }
 ]
}
```  

**_Get User Completed Games_**  
`GET /game/v1/get_user_completed_games?user_name=<data>`  

Response:  
```
200 OK  
{
 "games": [
  {
   "game_id": "1",
   "game_name": "1464818555467",
   "game_over": true,
   "game_status": "WON",
   "game_urlsafe_key": "ag9kZXZ-ZGVzaWduLWdhbWVyKwsSBFVzZXIiF2Fua2l0LmphaXN3YWxAZ21haWwuY29tDAsSBEdhbWUYAQw"
  }
 ]
}
```  

**_Get User Games_**  
`GAME STATUS VALUES: 'IN_SESSION', 'WON', 'LOST' and 'ABORTED'`  
`GET /game/v1/get_user_games?user_name=<data>&game_status=<data>`  

Response:  
```
200 OK  
{
 "games": [
  {
   "game_id": "11",
   "game_name": "1464818604901",
   "game_over": false,
   "game_status": "IN_SESSION",
   "game_urlsafe_key": "ag9kZXZ-ZGVzaWduLWdhbWVyKwsSBFVzZXIiF2Fua2l0LmphaXN3YWxAZ21haWwuY29tDAsSBEdhbWUYCww"
  }
 ]
}
```  

**_Guess Char_**  
`POST /game/v1/guess_char?user_name=<data>&urlsafe_key=<data>`  
`Content-Type: application/json`  

Request:
```
{
 "char": "z"
}
```  
Response:  
```
200 OK  
{
 "game_name": "1464818604901",
 "game_over": false,
 "game_status": "IN_SESSION",
 "guessed_chars_of_word": [
  "*",
  "*",
  "*",
  "*",
  "*",
  "*"
 ],
 "guesses_left": "5",
 "id": "11",
 "urlsafe_key": "ag9kZXZ-ZGVzaWduLWdhbWVyKwsSBFVzZXIiF2Fua2l0LmphaXN3YWxAZ21haWwuY29tDAsSBEdhbWUYCww",
 "word": "clouds"
}
```  

**_New Game_**  
`POST /game/v1/new_game?user_name=<data>`  
`Content-Type: application/json`  

Request:
```
{
 "game_name": "<data>"
}
```  
Response:  
```
200 OK  
{
 "urlsafe_key": "ag9kZXZ-ZGVzaWduLWdhbWVyGAsSBFVzZXIiBHRlc3QMCxIER2FtZRgPDA"
}
```  

**_Cancel Game_**  
`PATCH /game/v1/cancel_game?user_name=<data>&urlsafe_key=<data>`  

Response:  
```
200 OK  
{
 "game_id": "15",
 "game_name": "test",
 "game_over": true,
 "game_status": "ABORTED",
 "game_urlsafe_key": "ag9kZXZ-ZGVzaWduLWdhbWVyGAsSBFVzZXIiBHRlc3QMCxIER2FtZRgPDA"
}
```  
