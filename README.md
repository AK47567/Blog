
# 🧠 Quora-Inspired Q&A Platform (Backend)

This project is a Question & Answer platform built with **Django** and **Django REST Framework**. It allows users to register, log in, post questions, answer others' questions, and like answers — much like Quora.

---

## 🚀 Features

- 🔐 User Registration & Login 
- ❓ Post questions
- 👀 View all questions
- ✍️ Post answers to questions
- 👍 Like answers

---

## 🧱 Tech Stack

- **Python 3.x**
- **Django**
- **Django REST Framework**
- **PostgreSQL** (can be replaced with SQLite)
- **Custom User Model** (with phone number)

---

## 📦 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/quora-backend.git
cd quora-backend
```

### 2. Create virtual environment and activate

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> To generate a `requirements.txt` file if missing:
> ```bash
> pip freeze > requirements.txt
> ```

### 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create superuser (admin)

```bash
python manage.py createsuperuser
```

### 6. Start the server

```bash
python manage.py runserver
```

---

## 🔐 Authentication

This app uses Authentication. To register a user: 

```http
POST /api/user/registration/
```

To login:

```http
POST /api/user/login/
```

To logout

```http
POST /api/user/logout/
```

---

## 🧪 API Endpoints

| Method | Endpoint                          | Description                     | Auth Required |
|--------|-----------------------------------|----------------------------------|----------------|
| POST   | `/api/user/register/`             | Register new user               | ❌             |
| POST   | `/api/user/login/`                | Login and receive token         | ❌             |
| POST   | `/api/questions/`                 | Post a new question             | ✅             |
| GET    | `/api/questions/all/`             | Get all questions               | ❌             |
| POST   | `/questions/<id>/answer/`         | Post an answer to a question    | ✅             |
| POST   | `/answers/<id>/like/`             | Like an answer                  | ✅             |
| POST   | `/api/user/logout`                | Logout a user                   | ✅             | 
---

## 🔧 Models Overview

### `CustomUser`
- Extends Django's `AbstractUser`
- Adds `phoneNumber` field

### `Question`
- `user`: who asked the question
- `title`: question title
- `created_at`: timestamp

### `Answer`
- `question`: FK to Question
- `user`: who answered
- `content`: answer text
- `likes`: many-to-many with CustomUser
- `created_at`: timestamp

---

## ✨ Example API Payloads

### POST /questions/
```json
{
  "title": "What is Django REST Framework?"
}
```

### POST /questions/<id>/answer/
```json
{
  "content": "It's a powerful toolkit for building Web APIs."
}
```

---

## 📁 Project Structure

```
quora_backend/
├── your_app/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
├── quora_backend/
│   ├── settings.py
│   ├── urls.py
├── manage.py
└── README.md
```

---

