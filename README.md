REST API, предоставляющее возможность ведения блога.  
API имеет минимум сущности:  
Пользователь  
Пост  
Комментарий  

Пользователь имеет возможность:  
создать  
прочитать  
изменить  
удалить пост  

Задание выполнено с помощью фреймворка Flask.

Инструкция:  
Запустите файл main.py  
Приложение поддерживает следуюищие типы запросов: GET, POST, PUT, DELETE  
Для заботы с приложением отправьте HTTP запрос при помощи программы Postman (или аналогичных) в следующих форматах:  
Тест работы сервера: GET http://127.0.0.1:5000/ping body:{}  
Созлать твит: POST http://127.0.0.1:5000/twit body: {"id": "1", "body": "Hello world", "author": "User1", "comments": []}  
Получить список всех твитов: GET http://127.0.0.1:5000/twit body: {}  
Прочитать конкретный твит: GET http://127.0.0.1:5000/twit/1 body: {}  
Добавить комментарий к твиту: POST http://127.0.0.1:5000/twit/1/comment body: {"id": "1", "author": "John Doe", "message": "cool post"}  
Удалить комментарий к твиту: DELETE http://127.0.0.1:5000/twit/1/1 body: {}  
Редактировать твит: PUT http://127.0.0.1:5000/twit/1 body: {"body": "goodbye world", "author": "Anon"}  
Удалить твит: DELETE http://127.0.0.1:5000/twit/1 body: {}
