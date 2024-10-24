Web socket chat based on microservices architecture

To execute

`docker-compose up --build`

Login and generate token

`curl -X POST http://127.0.0.1:8000/login -u test@gmail.com:12345`

Open chat page

`http://127.0.0.1:8000/chat`

Add generated token into jwt cookie

