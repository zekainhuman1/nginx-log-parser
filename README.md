# NGINX Log Parser

Цей проєкт містить скрипт для обробки логів NGINX, парсингу їх у формат CSV та завантаження результатів на GitHub. Ви можете запустити скрипт як окремо, так і через Docker.

---

## Запуск скрипта

Скрипт можна запускати різними способами з командного рядка:

1. **Запуск скрипта за замовчуванням**:
    ```bash
    python parse_nginx_log.py
    ```

2. **Вказати директорію з логами**:
    ```bash
    python parse_nginx_log.py --log-dir /path/to/logs
    ```

3. **Вказати директорію для збереження результатів**:
    ```bash
    python parse_nginx_log.py --output-dir /path/to/output
    ```

4. **Автоматичний режим** (обирає перший файл логів у директорії):
    ```bash
    python parse_nginx_log.py --auto
    ```

## Налаштування скрипта

У файлі `parse_nginx_log.py` перед використанням можна змінити параметр `git_repo_url`.  

### Що потрібно знати:
- **`git_repo_url`** – це необов'язковий параметр. Якщо ви хочете, щоб скрипт автоматично завантажував результати до віддаленого GitHub-репозиторію, потрібно вказати URL вашого репозиторію разом з токеном.
- Якщо `git_repo_url` **не вказано**, скрипт буде працювати коректно, але результати зберігатимуться локально в папці `output`, і відправка на віддалений репозиторій не виконуватиметься.

### Як налаштувати:
1. Відкрийте файл `parse_nginx_log.py`.
2. Знайдіть змінну `git_repo_url` у функції `push_to_github`:
   ```python
   git_repo_url = "YOUR_GIT_REPO_URL"
   ```
3. Замініть значення на токен + URL вашого репозиторію в такому форматі:
   ```python
   git_repo_url = "https://github_pat_YOUR_GIT_TOKEN@github.com/YOUR_GIT/_REPO_URL.git"
   ```
4. Якщо відправка на GitHub не потрібна, залиште `git_repo_url` порожнім:
   ```python
   git_repo_url = ""
   ```
У цьому випадку скрипт лише зберігатиме результати локально.

**Примітка: Якщо ви вказали git_repo_url, переконайтеся, що перед запуском налаштовані ваші ім'я користувача та електронна пошта для Git в Dockerfile:**


---

## Запуск через Docker

Якщо ви хочете запустити скрипт через Docker, вам необхідно створити образ Docker та запустити контейнер. Ось кроки:
### 1. Створення Docker образу
```bash
docker build -t nginx-log-parser .
```

### 2. Запуск Docker контейнера
```bash
docker run -v /path/to/logs:/app/logs -v /path/to/output:/app/output nginx-log-parser
```
> **Примітка:** При запуску через Docker, за замовчуванням скрипт виконується з параметром `--auto`, що автоматично обирає перший файл логів із наданої директорії.

---

## Налаштування Git у Docker
Якщо в скрипті вказано git_repo_url, то для коректної роботи необхідно налаштувати дані Git у Docker контейнері. Для цього потрібно вказати ваше ім'я та email в Dockerfile:
```dockerfile
RUN git config --global user.name "YOUR_NAME" && \
    git config --global user.email "YOUR_EMAIL" && \
    git config --global init.defaultBranch "main"
```
> **Примітка:** Якщо в скрипті не вказано `git_repo_url`, ці налаштування можна пропустити.

---

## Налаштування часової зони у Docker
В Dockerfile ви також можете налаштувати часову зону для вірного відображення таймштампу. Наприклад, для часового поясу Europe/Kiev додайте наступне в Dockerfile:
```dockerfile
ENV TZ=Europe/Kiev
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone
```
Ви можете замінити `Europe/Kiev` на свій часовий пояс.

---

## Приклад запуску Docker
```bash
docker run -v /path/to/logs:/app/logs -v /path/to/output:/app/output nginx-log-parser
```

---

## Зворотній зв'язок

Якщо у вас є питання чи пропозиції, відкрийте issue.
