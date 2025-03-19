## STARR THE PROJECT 

### START BUILF THE IMAGE 
 `1 - docker-compose build `

### Start build the container
`` 2 - docker-compose up -d ``

### Show all container running
` 3 - docker-compose ps`

## Stop the container
``docker-compose down``

## Delete the conatiner
``docker-compose rm``

## Delete the data on volumen
```docker volume rm $(docker volume ls -qf dangling=true)```

## TODO TESTE API

### Create a todo
``curl -X POST -H "Content-Type: application/json" -d '{"title": "New todo", "description": "Descrição do novo todo"}' http://localhost:8000/todos``

### List all todos
`` curl -X GET http://localhost:8000/todos``

### Get one todo date
`` curl -X GET http://localhost:8000/todos/1``

### Update the todo date 
``curl -X PUT -H "Content-Type: application/json" -d '{"title": "Novo título", "description": "Nova descrição"}' http://localhost:8000/todos/1``

### Delete the todo data
``curl -X DELETE http://localhost:8000/todos/1``

