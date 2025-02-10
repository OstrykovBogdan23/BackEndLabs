## Опис
Цей проєкт є базовим Flask-додатком з реалізованим ендпоінтом `/healthcheck`, який перевіряє стан сервісу. Додаток контейнеризовано за допомогою Docker та налаштовано для деплою на Render.

---

## Вимоги
- Python 3.11+
- pip
- Docker
- Docker Compose

---

## 1. Локальний запуск

### 1.1. Встановлення залежностей
```bash
python -m venv env
source env/bin/activate  # Для Windows: .\env\Scripts\activate
pip install -r requirements.txt
```

### 1.2. Запуск застосунку
```bash
python run.py
```
Перевірити у браузері: [http://127.0.0.1:5000/healthcheck](http://127.0.0.1:5000/healthcheck)

---

## 2. Запуск у Docker

### 2.1. Збирання Docker-образу
```bash
docker build -t flask-app .
```

### 2.2. Запуск контейнера
```bash
docker run -p 5000:5000 flask-app
```
Перевірка: [http://127.0.0.1:5000/healthcheck](http://127.0.0.1:5000/healthcheck)

---

## 3. Використання Docker Compose

### 3.1. Запуск
```bash
docker-compose up --build
```

### 3.2. Зупинка
```bash
docker-compose down
```

---

## 4. Деплой на Render
1. Завантажити проєкт у GitHub.
2. Створити Web Service на [Render](https://render.com/).
3. Вказати репозиторій та гілку для деплою.
4. Дочекатися завершення збірки та перевірити роботу сервісу за наданим URL.

---

## 5. Ендпоінт

- **GET /healthcheck** – перевірка стану сервісу.

```json
{
    "status": "ok",
    "date": "2025-01-27T12:00:00.000Z"
}
```

---

## 6. Структура проєкту
```
/project
  |-- app/
      |-- __init__.py
      |-- views.py
  |-- requirements.txt
  |-- Dockerfile
  |-- docker-compose.yaml
  |-- run.py
  |-- README.md
```

---

## 7. Ліцензія
Цей проєкт є відкритим та доступним для використання.

