#SIMPLE HTTP CHAT



## Основные сущности

Ниже перечислены основные сущности, которыми оперирует сервер.

### User

Пользователь приложения. Имеет следующие свойства:

* **id** - уникальный идентификатор пользователя
* **username** - уникальное имя пользователя
* **created_at** - время создания пользователя

### Chat

Отдельный чат. Имеет следующие свойства:

* **id** - уникальный идентификатор чата
* **name** - уникальное имя чата
* **users** - список пользователей в чате, отношение многие-ко-многим
* **created_at** - время создания

### Message

Сообщение в чате. Имеет следующие свойства:

* **id** - уникальный идентификатор сообщения
* **chat** - ссылка на идентификатор чата, в который было отправлено сообщение
* **author** - ссылка на идентификатор отправителя сообщения, отношение многие-к-одному
* **text** - текст отправленного сообщения
* **created_at** - время создания

## Основные API методы

Методы обрабатывают HTTP POST запросы c телом, содержащим все необходимые параметры в JSON.

### Добавить нового пользователя

Запрос:

```bash
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"username": "user_1"}' \
  http://localhost:9000/users/add
```

Ответ: `id` созданного пользователя или HTTP-код ошибки.

### Создать новый чат между пользователями

Запрос:

```bash
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"name": "chat_1", "users": ["<USER_ID_1>", "<USER_ID_2>"]}' \
  http://localhost:9000/chats/add
```

Ответ: `id` созданного чата или HTTP-код ошибки.

Количество пользователей не ограничено.

### Отправить сообщение в чат от лица пользователя

Запрос:

```bash
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"chat": "<CHAT_ID>", "author": "<USER_ID>", "text": "hi"}' \
  http://localhost:9000/messages/add
```

Ответ: `id` созданного сообщения или HTTP-код ошибки.

### Получить список чатов конкретного пользователя

Запрос:

```bash
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"user": "<USER_ID>"}' \
  http://localhost:9000/chats/get
```

Ответ: cписок всех чатов со всеми полями, отсортированный по времени создания последнего сообщения в чате (от позднего к раннему). Или HTTP-код ошибки.

### Получить список сообщений в конкретном чате

Запрос:

```bash
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"chat": "<CHAT_ID>"}' \
  http://localhost:9000/messages/get
```

Ответ: список всех сообщений чата со всеми полями, отсортированный по времени создания сообщения (от раннего к позднему). Или HTTP-код ошибки.

Для установки проекта необходим Docker<br>
Для начала необходим образ mysql:
```bash
sudo docker run \
 --name mysql -d \
 -e MYSQL_RANDOM_ROOT_PASSWORD=yes \
 -e MYSQL_DATABASE=chat \
 -e MYSQL_USER=avitochat \
 -e MYSQL_PASSWORD=<YOUR-PASSWORD-HERE> \
 mysql/mysql-server:5.7
```
После чего образ, непосредственно, чата:
```bash
sudo docker run \
 --name avitochat -d -p 8000:9000 \
 --rm --link mysql:dbserver \
 -e DATABASE_URI=mysql+pymysql://avitochat:<YOUR-PASSWORD-HERE>@dbserver/chat \
 avitochat:latest
```

Теперь по http://localhost:8000/ доступен API чата.
