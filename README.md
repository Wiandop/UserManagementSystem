# Users Management System

Веб-приложение на **FastAPI** с хранением данных в **MySQL**.  
Позволяет просматривать список активных пользователей и искать их по логину или ID.  

---

## Возможности

- Просмотр списка всех **активных** пользователей (`/users`)
- Поиск пользователя по логину (`/by-login?login=admin`)
- Поиск пользователя по ID (`/by-id?id=1`)
- Главная страница со ссылками и поисковыми формами (`/`)
- Все HTML-данные экранируются с помощью `html.escape` для защиты от XSS

---

## Структура проекта

```
project/
│
├── main.py              # Основное приложение FastAPI
├── init-db.sql          # Скрипт инициализации БД
├── style/
│   └── style.css        # Стили для HTML
├── requirements.txt     # Зависимости
└── README.md            # Этот файл
```

---

## Установка MySQL (если не установлен)

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install mysql-server
sudo service mysql start
```

Проверьте, что сервер работает:
```bash
sudo service mysql status
```

---

### macOS
Если установлен **Homebrew**:
```bash
brew install mysql
brew services start mysql
```

---

## Установка

1. Склонируйте проект и перейди в каталог:

   ```bash
   git clone https://github.com/Wiandop/UserManagementSystem.git
   cd UserManagementSystem
   ```

2. Создайте и активируйте виртуальное окружение:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux / macOS
   .venv\Scripts\activate      # Windows
   ```

3. Установи зависимости:

   ```bash
   pip install -r requirements.txt
   ```

4. Подготовте базу данных MySQL:

   ```bash
   mysql -u root -p < init-db.sql
   ```

5. Убедись, что параметры подключения в `main.py` совпадают с твоими:
   ```python
   DATABASE_URL = "mysql+pymysql://root:@127.0.0.1:3306/app"
   ```
   Они будут отличаться только в случае, если у вас установлен пароль для MySQL

6. Запустите приложение
   ```bash
   uvicorn main:app --reload
   ```
   Приложение будет запущенно по адресу http://127.0.0.1:8000/
---

## Если команда `mysql -u root -p < init-db.sql` не работает

Если вы получаете ошибку при выполнении этой команды:

1. Убедитесь, что MySQL сервер запущен:
   ```bash
   sudo service mysql status
   ```
   или
   ```bash
   systemctl status mysql
   ```

2. Попробуйте подключиться вручную:
   ```bash
   mysql -u root -p
   ```
   Если не удаётся — значит, пароль root-пользователя неверный или сервер не запущен.

3. Если база данных `app` уже существует, можно пересоздать её:
   ```bash
   mysql -u root -p
   ```
   В интерактивной консоли MySQL:
   ```sql
   DROP DATABASE IF EXISTS app;
   SOURCE init-db.sql;
   ```

4. Если MySQL не принимает пароли, попробуйте запустить без `-p`:
   ```bash
   mysql -u root < init-db.sql
   ```