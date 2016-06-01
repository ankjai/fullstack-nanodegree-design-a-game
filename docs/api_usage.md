###### User APIs

**_Create User_**  
`/user/v1/create_user`  

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
`/user/v1/get_user`

Request:
```
{
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

**_Update User_**  
`/user/v1/update_user`  
Request:
```
{
 "current_user_name": "<data>",
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
`/user/v1/delete_user`  
Request:
```
{
 "user_name": "<data>"
}
```  
Response:
```
204  
<NO CONTENT>
```


---


###### Score APIs

**_Get All Scores_**  
`/score/v1/get_all_scores`  

Request:
```
{
 "fetch": "<no. of score items ordered by score desc>"
}
```  
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
`/score/v1/get_game_score`  

Request:
```
{
 "urlsafe_key": "ag9kZXZ-ZGVzaWduLWdhbWVyKwsSBFVzZXIiF2Fua2l0LmphaXN3YWxAZ21haWwuY29tDAsSBEdhbWUYAQw",
 "user_name": "<data>"
}
```  
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
`/score/v1/get_leaderboard`  

Request:
```
{
 "fetch": "<no. of rankings ordered by user_ranking asc>"
}
```  
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
`/score/v1/get_user_ranking`  

Request:
```
{
 "user_name": "<data>"
}
```  
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
`/score/v1/get_user_scores`  

Request:
```
{
 "user_name": "<data>"
}
```  
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
`/game/v1/get_game`  

Request:
```
{
 "urlsafe_key": "ag9kZXZ-ZGVzaWduLWdhbWVyKwsSBFVzZXIiF2Fua2l0LmphaXN3YWxAZ21haWwuY29tDAsSBEdhbWUYCww",
 "user_name": "<data>"
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
 "guesses_left": "6",
 "id": "11",
 "urlsafe_key": "ag9kZXZ-ZGVzaWduLWdhbWVyKwsSBFVzZXIiF2Fua2l0LmphaXN3YWxAZ21haWwuY29tDAsSBEdhbWUYCww",
 "word": "clouds"
}
```  

**_Get Game History_**  
`/game/v1/get_game_history`  

Request:
```
{
 "urlsafe_key": "ag9kZXZ-ZGVzaWduLWdhbWVyKwsSBFVzZXIiF2Fua2l0LmphaXN3YWxAZ21haWwuY29tDAsSBEdhbWUYCww",
 "user_name": "<data>"
}
```  
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
`/game/v1/get_user_completed_games`  

Request:
```
{
 "user_name": "<data>"
}
```  
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
`/game/v1/get_user_games`  

Request:
```
{
 "game_status": 1,       //int values = 1 (IN_SESSION), 2 (WON), 3 (LOST), 4 (ABORTED)
 "user_name": "<data>"
}
```  
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
`/game/v1/guess_char`  

Request:
```
{
 "char": "z",
 "urlsafe_key": "ag9kZXZ-ZGVzaWduLWdhbWVyKwsSBFVzZXIiF2Fua2l0LmphaXN3YWxAZ21haWwuY29tDAsSBEdhbWUYCww",
 "user_name": "ankit.jaiswal@gmail.com"
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
`/game/v1/new_game`  

Request:
```
{
 "game_name": "<data>",
 "user_name": "<data>"
}
```  
Response:  
```
200 OK  
{
 "urlsafe_key": "ag9kZXZ-ZGVzaWduLWdhbWVyGAsSBFVzZXIiBHRlc3QMCxIER2FtZRgPDA"
}
```  

**_New Game_**  
`/game/v1/new_game`  

Request:
```
{
 "game_name": "<data>",
 "user_name": "<data>"
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
`/game/v1/cancel_game`  

Request:
```
{
 "urlsafe_key": "ag9kZXZ-ZGVzaWduLWdhbWVyGAsSBFVzZXIiBHRlc3QMCxIER2FtZRgPDA",
 "user_name": "<data>"
}
```  
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
