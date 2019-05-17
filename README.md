# FinallySomethingWork
This program with basic REST API coded with  python3  
To write this code i used frameworks/libraries:

* ```sqlite3```,```flask```,```flask_restful```
* ```jwt```,```os```,```time```,```uuid```

## POST /login
Example request :
```
{
"username": "admin",
"password": ';--!s@fepassw0rd'
}
```
Example response:
```
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.itwsXqRDZxuOT7cSEcusCHoc3yrvhDGUbgu0bFGg-Ok"
}
```
## POST /palindrome/solve
Example request :
```
{
"value": 7777777
}
```
Example response:
```
{
    "is_palindrome": "True"
}
```
## GET /palindrome/history
Example response:  
**ORDERED BY ID**
```
[
    {
        "date": "Fri May 17 22:47:17 2019",
        "id": "c1684508-78df-48d7-8741-37bddfb68ab5",
        "is_palindrome": "False",
        "value": "abcb"
    },
    {
        "date": "Fri May 17 22:47:26 2019",
        "id": "4105a4de-4d75-4a87-a677-1b3a64a8dd23",
        "is_palindrome": "True",
        "value": "12321"
    },
    {
        "date": "Fri May 17 22:47:35 2019",
        "id": "de19e7b5-99da-4802-8a14-69f1c9f1205b",
        "is_palindrome": "False",
        "value": "abcd2asda"
    },
    {
        "date": "Fri May 17 22:47:40 2019",
        "id": "98ce63aa-d5e7-4805-b73f-14c762433f0f",
        "is_palindrome": "True",
        "value": "7777777"
    }
]
```

## DELETE /palindrome/{id}
Example URL: http://localhost:5000/palindrome/ffac09e2-4cb9-4881-b982-dac7499c5ab1  
Example response:
```
{
    "status": "Success"
}
```
