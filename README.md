Выбранная тема: Социальная сеть
ФИО: Ефимов Никита Андреевич
Группа: БПМИ2210

### Запуск тестов
```bash
make build_api-gateway test_api-gateway
make build_user-service test_user-service
```

### Запуск проекта

Нужно настроить docker-compose а после этого запустить контейнеры

```bash
docker-compose up -d
```

### Пример запросов

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \ 
    -H "Content-Type: application/json" \
    -d '{
        "username": "testuser",
        "password": "testpass",
        "email": "test@example.com"
    }'
{"user_id":"4437bb20-f529-4fef-b173-5f29edeb376d","session_id":"243c8e53-03e4-47ca-9d9b-aec2b476d6fa","expires_at":"2025-03-07T20:08:40.743752+00:00"}
```

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \  
    -H "Content-Type: application/json" \
    -d '{
        "username": "testuser",
        "password": "testpass",
        "email": "test@example.com"
    }'
{"detail":"Username already registered"}
```

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \ 
    -H "Content-Type: application/json" \
    -d '{
        "username": "testuser",
        "password": "testpass" 
    }'
{"user_id":"4437bb20-f529-4fef-b173-5f29edeb376d","session_id":"373f5556-c922-4e22-b653-83fa1cbc55bc","expires_at":"2025-03-07T20:14:05.229832"}
```

```bash
curl -X GET http://localhost:8000/api/v1/profile/me \   
    -H "Session-ID: 373f5556-c922-4e22-b653-83fa1cbc55bc"
{"first_name":null,"last_name":null,"date_of_birth":null,"phone_number":null,"username":"testuser","email":"test@example.com","created_at":"2025-03-07T19:38:40.738859Z","updated_at":null}
```

```bash
curl -X PATCH http://localhost:8000/api/v1/profile/me \   
    -H "Content-Type: application/json" \
    -H "Session-ID: 373f5556-c922-4e22-b653-83fa1cbc55bc" \
    -d '{
        "email": "test1@example.com"
    }'
{"first_name":null,"last_name":null,"date_of_birth":null,"phone_number":null,"username":"testuser","email":"test1@example.com","created_at":"2025-03-07T19:38:40.738859Z","updated_at":"2025-03-07T19:47:42.533819Z"}
```
