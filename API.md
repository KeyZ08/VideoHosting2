# API

### URLs
```
  /echo/            - GET,POST 	- при POST возвращает тело запроса, при GET возвращает все заголовки в формате json
  /hello/           - GET,POST 	- возвращает "Hello"
  /api/jsonrpc/	    - POST	- принимает json формата jsonrpc и в зависимости от method и params возвращает соответствующие данные
```

###### Обращение к /api/jsonrpc/ обязательно выглядят так:
```json
{
  "jsonrpc": "2.0", 
  "id": `jsonrpc_id`, 
  "method": `method_name`, 
  "params":{`params`}
}
```

## Содержание:
- Проверка валидности файлов
  - [Аватар пользователя](#user_avatar)
  - [Превью видео](#video_preview)
  - [Видеофайл](#video)
- Информация об объектах
  - [Все видео пользователя](#get_videos)
  - [Конкретное Видео](#get_video)
  - [Комментарии к видео](#get_comments)


### Например:
##### Проверка валидности файлов

- <a name="user_avatar"/>Для проверки корректное ли изображение выбрано в качестве аватара канала
```json
{
  "jsonrpc": "2.0", 
  "id": `jsonrpc_id`,
  "method": "check_file_valid", 
  "params": {
    "file": {
      "size": `size_bytes`, 
      "target": "avatar_image", 
      "name": `file_name_with_file_extension `
  }}
}

```
	
- <a name="video_preview"/>Для проверки корректное ли изображение выбрано в качестве превью видео
```json
{
  "jsonrpc": "2.0", 
  "id": `jsonrpc_id`,
  "method": "check_file_valid", 
  "params": {
    "file": {
      "size": `size_bytes`, 
      "target": "video_preview_image", 
      "name": `file_name_with_file_extension `
  }}
}
```

- <a name="video"/>Для проверки корректно ли загружаемое видео
```json
{
  "jsonrpc": "2.0", 
  "id": `jsonrpc_id`,
  "method": "check_file_valid", 
  "params": {
    "file": {
    "size": `size_bytes`, 
    "target": "video", 
    "name": `file_name_with_file_extension `
  }}
}
```

##### Информация об объектах
- <a name="get_video"/>Возвращает информацию о данном видео
```json
{
  "jsonrpc": "2.0", 
  "id": `jsonrpc_id`,
  "method": "get_video", 
  "params": {"id_video": `id_video`}
}
```

- <a name="get_comments"/>Возращает информацию о всех комментариях на данном видео
```json
{
  "jsonrpc": "2.0", 
  "id": `jsonrpc_id`,
  "method": "get_comments", 
  "params": {"id_video": `id_video`}
}
```

- Возращает информацию о всех роликах на данном канале
```json
{
  "jsonrpc": "2.0", 
  "id": `jsonrpc_id`,
  "method": "get_videos", 
  "params": {"username": `username`}}
}
```


 
 
 
 
 
 
 
 