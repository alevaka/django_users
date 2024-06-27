# django_users
## Тестовое задание - создать приложение для управления пользователями.

## Список страниц приложения users

### Index
**URL:** [/accounts/](http://localhost:8000/accounts/)  
**Описание:** Отображает страницу со списком представлений.

### User List View
**URL:** [/accounts/user_list/](http://localhost:8000/accounts/user_list/)  
**Описание:** Отображает страницу со списком пользователей.

### User Detail View
**URL:** [/accounts/profile/user.pk/]()  
**Описание:** Отображает страницу профиля пользователя.

### Signup View
**URL:** [/accounts/signup/](http://localhost:8000/accounts/signup/)  
**Описание:** Форма регистрации нового пользователя.

### Login View
**URL:** [/accounts/login/](http://localhost:8000/accounts/login/)  
**Описание:** Форма для входа пользователя.

### Logout View
**URL:** [/accounts/logout/](http://localhost:8000/accounts/logout/)  
**Описание:** Завершает сеанс пользователя.

### Profile View
**URL:** [/accounts/profile/](http://localhost:8000/accounts/profile/)  
**Описание:** Отображает профиль авторизованного пользователя.

### Password Change View
**URL:** [/accounts/password_change/](http://localhost:8000/accounts/password_change/)  
**Описание:** Форма изменения пароля пользователя.

### Password Reset View
**URL:** [/accounts/password_reset/](http://localhost:8000/accounts/password_reset/)  
**Описание:** Форма запроса на сброс пароля пользователя.

### Cтэк технологий:
- Python
- Django
- PostgreSQL
- Docker
- nginx

### Запуск через Docker Compose локально (рекомендуемый способ запуска)
0. Клонируйте репозиторий себе на машину с помощью git clone.
1. Создайте файл `.env` и заполните его своими данными. Файл `.env` должен находиться в корневой папке проекта. Если вы решите не создавать свой `.env` файл - в проекте предусмотрен файл `.env_example`, обеспечивающий переменные для базовой работы на локальном уровне.
2. Собрерите и запустите докер-контейнеры через Docker Compose:
```bash
docker compose up -d --build
```
