
# Auth service
```
/login/ 		- GET,POST 	- аутентификация
/register/ 		- GET,POST 	- регистрация
```

# Account service
```
/account/ 			- GET, POST		- личный кабинет пользователя, изменение данных о канале
/account/history/		- GET			- страница с историей посещений видео
/accounts/ 			- GET			- страница со всеми каналами 
/accounts/<str:username>/	- GET			- страница конкретного канала
```

##### Служебные
```
/account/avatar_upload/		- POST 		- сохранение нового аватара пользователя
/account/reset_avatar/		- POST		- сброс аватара до значения по умолчанию
/account/video_upload/		- POST		- загрузка нового видео
```

# Video service

```
host 								- GET 		- главная страница
/videos/							- GET 		- страница cо всеми видео на платформе
/videos/<str:id_video>/ 					- GET 		- страница просмотра видео
/videos/<str:id_video>/change/					- GET,POST	- изменение данных о видео
```

##### Служебные
```
/videos/<str:id_video>/delete/					- POST		- удалить видео
/videos/<str:id_video>/like/					- POST 		- поставить/удалить лайк
/videos/<str:id_video>/dislike/					- POST 		- поставить/удалить дизлайк
/videos/<str:id_video>/add-comment/				- POST		- добавить комментарий к видео
/videos/<str:id_video>/delete-comment/<int:comment_id>/		- POST		- удалить комментарий к видео
```
