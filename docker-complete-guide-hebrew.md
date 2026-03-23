# מדריך Docker מקיף לסטודנטים: מהתחלה ועד רמה מתקדמת

## תוכן עניינים

1. [מבוא ל-Docker](#מבוא-ל-docker)
2. [התקנת Docker](#התקנת-docker)
3. [מושגים בסיסיים](#מושגים-בסיסיים)
4. [Docker Images ו-Dockerfile](#docker-images-ו-dockerfile)
5. [Docker Containers](#docker-containers)
6. [REST API עם Docker](#rest-api-עם-docker)
7. [Docker Compose](#docker-compose)
8. [רשתות ב-Docker](#רשתות-ב-docker)
9. [ניהול נתונים ו-Volumes](#ניהול-נתונים-ו-volumes)
10. [אופטימיזציה ו-Best Practices](#אופטימיזציה-ובest-practices)
11. [Debugging ופתרון בעיות](#debugging-ופתרון-בעיות)
12. [מקרים מתקדמים](#מקרים-מתקדמים)
13. [פרויקט מעשי מלא](#פרויקט-מעשי-מלא)
14. [משאבים נוספים](#משאבים-נוספים)

---

## מבוא ל-Docker

### מה זה Docker?

Docker היא פלטפורמת קונטיינריזציה המאפשרת לארוז אפליקציות עם כל התלותיות שלהן בסביבה מבודדת וניידת. במקום לומר "זה עובד אצלי במחשב", Docker מבטיח שהאפליקציה תעבוד באופר זהה בכל סביבה - מפיתוח ועד ייצור.

### למה להשתמש ב-Docker?

1. **עקביות**: אותה סביבה בכל מקום
2. **בידוד**: אפליקציות לא מתנגשות זו עם זו
3. **ניידות**: קל להעביר בין מכונות
4. **מהירות**: זמן אתחול מהיר ממכונות וירטואליות
5. **יעילות**: שימוש טוב יותר במשאבים

### ההבדל בין Docker למכונות וירטואליות

מכונות וירטואליות כוללות מערכת הפעלה שלמה, בעוד Docker קונטיינרים חולקים את מערכת ההפעלה של המארח ומשתמשים רק במה שצריך. זה הופך אותם לקלים יותר, מהירים יותר ויעילים יותר.

---

## התקנת Docker

### Windows

1. הורד את Docker Desktop מ-[docker.com](https://www.docker.com/products/docker-desktop)
2. הפעל את המתקין ופעל לפי ההוראות
3. הפעל WSL 2 (Windows Subsystem for Linux)
4. אתחל את המחשב לאחר ההתקנה

### macOS

1. הורד את Docker Desktop עבור Mac
2. גרור את הקובץ לתיקיית Applications
3. הפעל את Docker Desktop
4. המתן עד שהאייקון יופיע בסרגל הכלים

### Linux (Ubuntu/Debian)

```bash
# עדכון המערכת
sudo apt update

# התקנת תלותיות
sudo apt install apt-transport-https ca-certificates curl software-properties-common

# הוספת מפתח GPG של Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# הוספת repository
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# התקנת Docker
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io

# הוספת המשתמש לקבוצת docker
sudo usermod -aG docker $USER

# התקנת Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### אימות ההתקנה

```bash
# בדיקת גרסת Docker
docker --version

# בדיקת גרסת Docker Compose
docker-compose --version

# הרצת קונטיינר ראשון
docker run hello-world
```

---

## מושגים בסיסיים

### Image (תמונה)

Image היא תבנית לקריאה בלבד המכילה את כל מה שנדרש להפעלת אפליקציה: קוד, ספריות, תלותיות, משתני סביבה, והגדרות תצורה.

### Container (קונטיינר)

Container הוא מופע פעיל של Image. הוא מבודד, קל משקל ונייד. אפשר ליצור מספר קונטיינרים מאותה Image.

### Dockerfile

Dockerfile הוא קובץ טקסט עם הוראות לבניית Image אוטומטית. הוא מגדיר את כל השלבים ליצירת הסביבה.

### Registry (רישום)

Registry הוא מקום אחסון של Images. Docker Hub הוא הרישום הציבורי המרכזי, אך קיימים גם רישומים פרטיים.

### Volume (נפח)

Volume הוא אמצעי לאחסון נתונים מתמיד ששורד מעבר לחיי הקונטיינר.

---

## Docker Images ו-Dockerfile

### חיפוש Images

```bash
# חיפוש Images ב-Docker Hub
docker search nginx
docker search python
docker search postgres

# הורדת Image
docker pull nginx:latest
docker pull python:3.9-slim

# רשימת Images מקומיות
docker images
docker image ls
```

### Dockerfile בסיסי

```dockerfile
# Dockerfile דוגמה לאפליקציית Python פשוטה

# שלב 1: בחירת Image בסיס
FROM python:3.9-slim

# שלב 2: הגדרת ספריית עבודה
WORKDIR /app

# שלב 3: העתקת קבצי דרישות
COPY requirements.txt .

# שלב 4: התקנת תלותיות
RUN pip install --no-cache-dir -r requirements.txt

# שלב 5: העתקת קוד האפליקציה
COPY . .

# שלב 6: חשיפת פורט
EXPOSE 5000

# שלב 7: הגדרת פקודת הפעלה
CMD ["python", "app.py"]
```

### הוראות Dockerfile נפוצות

#### FROM
```dockerfile
FROM python:3.9-slim
FROM node:16-alpine
FROM ubuntu:20.04
```

#### WORKDIR
```dockerfile
WORKDIR /app
WORKDIR /usr/src/app
```

#### COPY ו-ADD
```dockerfile
# COPY - העתקת קבצים מהמארח לקונטיינר
COPY . /app
COPY requirements.txt /app/
COPY src/*.js /app/src/

# ADD - כמו COPY אבל תומך גם ב-URL וקבצי tar
ADD https://example.com/file.tar.gz /tmp/
ADD archive.tar.gz /app/
```

#### RUN
```dockerfile
# הרצת פקודות בזמן בניית ה-Image
RUN apt-get update && apt-get install -y curl
RUN pip install flask requests
RUN npm install
```

#### CMD ו-ENTRYPOINT
```dockerfile
# CMD - פקודת ברירת מחדל (ניתן לדרוס)
CMD ["python", "app.py"]
CMD ["npm", "start"]

# ENTRYPOINT - פקודה קבועה (קשה יותר לדרוס)
ENTRYPOINT ["python"]
CMD ["app.py"]
```

#### EXPOSE
```dockerfile
EXPOSE 5000
EXPOSE 8080
EXPOSE 3000
```

#### ENV
```dockerfile
ENV FLASK_ENV=production
ENV NODE_ENV=production
ENV DATABASE_URL=postgresql://user:pass@localhost/db
```

#### ARG
```dockerfile
ARG VERSION=latest
ARG BUILD_DATE
```

### בניית Image מ-Dockerfile

```bash
# בניית Image בסיסית
docker build -t myapp:1.0 .

# בנייה עם שם ותג
docker build -t username/appname:version .

# בנייה עם ARG
docker build --build-arg VERSION=2.0 -t myapp:2.0 .

# בנייה ללא cache
docker build --no-cache -t myapp:latest .

# בנייה עם Dockerfile מותאם
docker build -f Dockerfile.prod -t myapp:prod .
```

### Multi-stage builds

```dockerfile
# שלב 1: Build stage
FROM node:16-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# שלב 2: Production stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

## Docker Containers

### הפעלת Containers

```bash
# הפעלה בסיסית
docker run nginx

# הפעלה עם שם
docker run --name mynginx nginx

# הפעלה ברקע (detached)
docker run -d --name mynginx nginx

# הפעלה עם מיפוי פורטים
docker run -d -p 8080:80 --name mynginx nginx

# הפעלה עם משתני סביבה
docker run -e NODE_ENV=production nodeapp

# הפעלה עם volume
docker run -v /host/path:/container/path nginx
```

### ניהול Containers

```bash
# רשימת Containers פעילים
docker ps

# רשימת כל ה-Containers (כולל מופסקים)
docker ps -a

# הפסקת Container
docker stop container_name

# הפעלת Container מחדש
docker start container_name

# מחיקת Container
docker rm container_name

# כפל כפל מחיקה (כולל Containers פעילים)
docker rm -f container_name

# מחיקת כל ה-Containers המופסקים
docker container prune
```

### צפייה ב-Containers

```bash
# צפייה בלוגים
docker logs container_name

# צפייה בלוגים בזמן אמת
docker logs -f container_name

# צפייה בלוגים עם חותמת זמן
docker logs -t container_name

# צפייה במידע מפורט על ה-Container
docker inspect container_name

# צפייה בשימוש במשאבים
docker stats container_name
```

### כניסה ל-Containers

```bash
# כניסה עם shell אינטראקטיבי
docker exec -it container_name /bin/bash

# הרצת פקודה ב-Container פעיל
docker exec container_name ls -la

# הרצת פקודה ברקע
docker exec -d container_name python script.py
```

### העתקת קבצים

```bash
# העתקה מהמארח ל-Container
docker cp file.txt container_name:/path/in/container/

# העתקה מ-Container למארח
docker cp container_name:/path/in/container/file.txt ./local/path/
```

---

## REST API עם Docker

### פרויקט Flask REST API דוגמה

#### app.py
```python
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# הגדרות מסד נתונים
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# מודל משתמש
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'email': self.email}

# יצירת טבלאות
with app.app_context():
    db.create_all()

# נתיבים
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(name=data['name'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    db.session.commit()
    return jsonify(user.to_dict())

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return '', 204

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

#### requirements.txt
```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
psycopg2-binary==2.9.7
```

#### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# התקנת תלותיות מערכת
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# העתקת קובץ דרישות והתקנת תלותיות Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# העתקת קוד האפליקציה
COPY . .

# יצירת משתמש לא רוט
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app
USER app

# חשיפת פורט
EXPOSE 5000

# פקודת הפעלה
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

#### .dockerignore
```
__pycache__
*.pyc
.venv
.git
.gitignore
README.md
Dockerfile
.dockerignore
```

### בנייה והפעלה של ה-API

```bash
# בניית ה-Image
docker build -t flask-api:latest .

# הפעלת ה-API
docker run -d -p 5000:5000 --name flask-api flask-api:latest

# בדיקת ה-API
curl http://localhost:5000/health
curl http://localhost:5000/api/users
```

### שילוב עם מסד נתונים

#### Dockerfile עם PostgreSQL
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# התקנת תלותיות PostgreSQL
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app
USER app

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

#### הפעלה עם PostgreSQL
```bash
# הפעלת PostgreSQL
docker run -d \
    --name postgres-db \
    -e POSTGRES_DB=appdb \
    -e POSTGRES_USER=appuser \
    -e POSTGRES_PASSWORD=apppass \
    -p 5432:5432 \
    postgres:13

# הפעלת ה-API עם חיבור למסד הנתונים
docker run -d \
    --name flask-api \
    --link postgres-db:db \
    -e DATABASE_URL=postgresql://appuser:apppass@db/appdb \
    -p 5000:5000 \
    flask-api:latest
```

---

## Docker Compose

Docker Compose הוא כלי להגדרה והפעלה של אפליקציות מרובות-קונטיינרים באמצעות קובץ YAML אחד.

### docker-compose.yml בסיסי

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://appuser:apppass@db:5432/appdb
    depends_on:
      - db
    volumes:
      - ./app:/app
    restart: unless-stopped

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=appdb
      - POSTGRES_USER=appuser
      - POSTGRES_PASSWORD=apppass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
```

### פקודות Docker Compose

```bash
# הפעלת כל השירותים
docker-compose up

# הפעלה ברקע
docker-compose up -d

# בניית Images
docker-compose build

# הפסקת שירותים
docker-compose stop

# הפעלה מחדש
docker-compose start

# הפסקה והסרה
docker-compose down

# הסרה כולל volumes
docker-compose down -v

# צפייה בלוגים
docker-compose logs

# צפייה בלוגים של שירות ספציפי
docker-compose logs web

# צפייה בלוגים בזמן אמת
docker-compose logs -f

# הרצת פקודה בשירות
docker-compose exec web bash
docker-compose exec db psql -U appuser -d appdb

# קנה מידה
docker-compose up --scale web=3

# בנייה מחדש
docker-compose up --build
```

### דוגמה מתקדמת עם כמה שירותים

```yaml
version: '3.8'

services:
  # שירות ה-API
  api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://appuser:apppass@postgres:5432/appdb
      - REDIS_URL=redis://redis:6379/0
      - ELASTICSEARCH_URL=http://elasticsearch:9200
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
    volumes:
      - ./app:/app
      - api_logs:/app/logs
    restart: unless-stopped
    networks:
      - app-network

  # שירות PostgreSQL
  postgres:
    image: postgres:13-alpine
    environment:
      - POSTGRES_DB=appdb
      - POSTGRES_USER=appuser
      - POSTGRES_PASSWORD=apppass
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U appuser -d appdb"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - app-network

  # שירות Redis
  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped
    command: redis-server --appendonly yes
    networks:
      - app-network

  # שירות Elasticsearch
  elasticsearch:
    image: elasticsearch:7.14.0
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9200:9200"
    volumes:
      - es_data:/usr/share/elasticsearch/data
    restart: unless-stopped
    networks:
      - app-network

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - api
    restart: unless-stopped
    networks:
      - app-network

  # שירות עובדים (Workers)
  worker:
    build: .
    command: celery worker -A app.celery --loglevel=info
    environment:
      - DATABASE_URL=postgresql://appuser:apppass@postgres:5432/appdb
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis
    volumes:
      - ./app:/app
    restart: unless-stopped
    networks:
      - app-network

  # שירות מתזמן (Scheduler)
  scheduler:
    build: .
    command: celery beat -A app.celery --loglevel=info
    environment:
      - DATABASE_URL=postgresql://appuser:apppass@postgres:5432/appdb
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis
    volumes:
      - ./app:/app
    restart: unless-stopped
    networks:
      - app-network

volumes:
  postgres_data:
  redis_data:
  es_data:
  api_logs:

networks:
  app-network:
    driver: bridge
```

### סביבות שונות

#### docker-compose.dev.yml
```yaml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=development
      - DATABASE_URL=postgresql://appuser:apppass@postgres:5432/appdb_dev
    volumes:
      - .:/app
    command: flask run --host=0.0.0.0 --debugger --reload
    depends_on:
      - postgres

  postgres:
    image: postgres:13-alpine
    environment:
      - POSTGRES_DB=appdb_dev
      - POSTGRES_USER=appuser
      - POSTGRES_PASSWORD=apppass
    ports:
      - "5432:5432"
    volumes:
      - postgres_dev_data:/var/lib/postgresql/data

volumes:
  postgres_dev_data:
```

#### docker-compose.prod.yml
```yaml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile.prod
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://appuser:apppass@postgres:5432/appdb_prod
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M

  postgres:
    image: postgres:13-alpine
    environment:
      - POSTGRES_DB=appdb_prod
      - POSTGRES_USER=appuser
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_prod_data:/var/lib/postgresql/data
    deploy:
      resources:
        limits:
          memory: 1G

volumes:
  postgres_prod_data:
```

### שימוש במשתני סביבה

#### .env
```
DATABASE_URL=postgresql://appuser:apppass@postgres:5432/appdb
REDIS_URL=redis://redis:6379/0
SECRET_KEY=your-secret-key-here
DEBUG=false
```

#### docker-compose.yml עם משתני סביבה
```yaml
version: '3.8'

services:
  api:
    build: .
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - SECRET_KEY=${SECRET_KEY}
      - DEBUG=${DEBUG}
    env_file:
      - .env
```

---

## רשתות ב-Docker

### סוגי רשתות

1. **Bridge Network** (ברירת מחדל) - רשת פרטית לקונטיינרים על אותו מארח
2. **Host Network** - הקונטיינר חולק את רשת המארח
3. **Overlay Network** - רשת מרובת-מארחים ל-Docker Swarm
4. **None Network** - ללא גישה לרשת

### יצירת רשתות

```bash
# יצירת רשת bridge
docker network create my-network

# יצירת רשת עם תת-רשת מותאמת
docker network create --subnet=192.168.0.0/16 my-network

# יצירת רשת overlay
docker network create --driver overlay my-overlay-network

# רשימת רשתות
docker network ls

# מחיקת רשת
docker network rm my-network

# מידע על רשת
docker network inspect my-network
```

### חיבור קונטיינרים לרשתות

```bash
# חיבור קונטיינר לרשת
docker network connect my-network container_name

# ניתוק קונטיינר מרשת
docker network disconnect my-network container_name

# הפעלת קונטיינר ברשת ספציפית
docker run --network=my-network nginx
```

### תקשורת בין קונטיינרים

```bash
# הפעלת שני קונטיינרים באותה רשת
docker network create app-network
docker run -d --name web --network app-network nginx
docker run -d --name api --network app-network flask-api

# בדיקת תקשורת (מתוך קונטיינר web)
docker exec web ping api
docker exec web curl http://api:5000/health
```

### DNS ו-Service Discovery

Docker מספק DNS מובנה לגילוי שירותים:

```bash
# קונטיינרים יכולים למצוא זה את זו לפי שם
# בתוך קונטיינר A:
curl http://container-b:8080/api

# ב-Docker Compose, שמות השירותים הם שמות ה-DNS
# בקובץ docker-compose.yml:
services:
  web:
    # יכול לגשת ל: http://api:5000
  api:
    # יכול לגשת ל: http://db:5432
```

---

## ניהול נתונים ו-Volumes

### סוגי אחסון ב-Docker

1. **Volumes** - אחסון מנוהל על ידי Docker
2. **Bind Mounts** - קישור לתיקייה במערכת המארח
3. **tmpfs** - אחסון בזיכרון המארח בלבד

### Volumes

```bash
# יצירת volume
docker volume create my-data

# רשימת volumes
docker volume ls

# מידע על volume
docker volume inspect my-data

# מחיקת volume
docker volume rm my-data

# מחיקת volumes לא בשימוש
docker volume prune

# שימוש ב-volume
docker run -d -v my-data:/data nginx
```

### Bind Mounts

```bash
# שימוש ב-bind mount
docker run -d -v /host/path:/container/path nginx

# שימוש עם קריאה בלבד
docker run -d -v /host/path:/container/path:ro nginx

# ב-Docker Compose
volumes:
  - ./app:/app
  - /host/data:/container/data:ro
```

### דוגמה מעשית עם PostgreSQL

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:13
    environment:
      - POSTGRES_DB=appdb
      - POSTGRES_USER=appuser
      - POSTGRES_PASSWORD=apppass
    volumes:
      # Volume מנוהל לנתונים
      - postgres_data:/var/lib/postgresql/data
      # Bind mount לסקריפטים
      - ./init-scripts:/docker-entrypoint-initdb.d
      # Bind mount לגיבויים
      - ./backups:/backups
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

### גיבוי ושחזור נתונים

```bash
# גיבוי volume
docker run --rm -v postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres-backup.tar.gz -C /data .

# שחזור volume
docker run --rm -v postgres_data:/data -v $(pwd):/backup alpine tar xzf /backup/postgres-backup.tar.gz -C /data

# גיבוי מסד נתונים PostgreSQL
docker exec postgres-db pg_dump -U appuser appdb > backup.sql

# שחזור מסד נתונים
docker exec -i postgres-db psql -U appuser appdb < backup.sql
```

---

## אופטימיזציה ו-Best Practices

### אופטימיזציית Dockerfile

#### שימוש ב-Alpine Images
```dockerfile
# גודל קטן יותר
FROM python:3.9-alpine

# במקום
FROM python:3.9-slim
```

#### Multi-stage builds
```dockerfile
# Build stage
FROM node:16-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
```

#### צמצום שכבות
```dockerfile
# טוב
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# לא טוב
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git
```

#### סדר הוראות אופטימלי
```dockerfile
# משתנים ותלותיות קודם (משתנות לעיתים רחוקות)
COPY requirements.txt .
RUN pip install -r requirements.txt

# קוד אחר כך (משתנה לעיתים קרובות)
COPY . .
```

### אופטימיזציית Images

```bash
# בדיקת גודל Images
docker images

# בדיקת היסטוריית שכבות
docker history image_name

# ניקוי cache
docker builder prune

# ניקוי מערכת
docker system prune -a
```

### Best Practices

#### 1. שימוש במשתמש לא רוט
```dockerfile
FROM node:16-alpine
RUN useradd --create-home --shell /bin/bash app
WORKDIR /app
COPY . .
RUN chown -R app:app /app
USER app
```

#### 2. סריקת אבטחה
```bash
# סריקת Image לפגיעויות
docker scan image_name

# סריקה עם Trivy
trivy image image_name
```

#### 3. תגיות גרסאות
```bash
# תמיד השתמש בתגיות ספציפיות
FROM python:3.9.5-slim
# במקום
FROM python:3.9-slim
```

#### 4. Health Checks
```dockerfile
FROM nginx:alpine
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/ || exit 1
```

#### 5. ניהול סודות
```bash
# יצירת secret
echo "my-secret-password" | docker secret create db_password -

# שימוש ב-Docker Compose
secrets:
  db_password:
    external: true
```

---

## Debugging ופתרון בעיות

### כלים ל-Debugging

```bash
# צפייה בלוגים מפורטים
docker logs --details container_name

# צפייה במשאבים בזמן אמת
docker stats --no-stream

# בדיקת אירועים
docker events

# בדיקת מידע מפורט
docker inspect container_name
```

### בעיות נפוצות ופתרונות

#### 1. Permission Denied
```bash
# בעיה: permission denied while trying to connect to the Docker daemon socket
# פתרון: הוספת המשתמש לקבוצת docker
sudo usermod -aG docker $USER
# התחבר מחדש או הפעל מחדש
```

#### 2. Port Already in Use
```bash
# בעיה: port is already allocated
# פתרון: מציאת התהליך שמשתמש בפורט
netstat -tulpn | grep :8080
# או הפעלה עם פורט אחר
docker run -p 8081:80 nginx
```

#### 3. Out of Space
```bash
# בעיה: no space left on device
# פתרון: ניקוי Docker
docker system prune -a
docker volume prune
docker image prune -a
```

#### 4. Container Keeps Restarting
```bash
# בעיה: קונטיינר מופסק ומופעל מחדש
# פתרון: צפייה בלוגים
docker logs container_name
# הפעלה אינטראקטיבית ל-debug
docker run -it --entrypoint /bin/bash image_name
```

#### 5. Network Issues
```bash
# בעיה: קונטיינרים לא מתראים זה את זה
# פתרון: בדיקת רשתות
docker network ls
docker network inspect network_name
# הפעלה באותה רשת
docker run --network=network_name image_name
```

### Debugging ב-Docker Compose

```bash
# הפעלת שירות בודד במצב debug
docker-compose run --rm web bash

# הפעלה עם פורטים נוספים ל-debug
docker-compose run --service-ports --rm web

# בנייה מחדש עם verbose
docker-compose build --no-cache --progress=plain

# צפייה בלוגים של כל השירותים
docker-compose logs --tail=100 -f
```

### כלי Debugging מתקדמים

```bash
# Dive - ניתוח גודל שכבות
dive image_name

# ctop - ממשק לניהול קונטיינרים
ctop

# lazydocker - ממשק טרמינלי
lazydocker
```

---

## מקרים מתקדמים

### Docker Swarm

#### אתחול Swarm
```bash
# אתחול Swarm manager
docker swarm init

# הצטרפות worker ל-Swarm
docker swarm join --token <token> <manager-ip>:2377

# צפייה ב-nodes
docker node ls
```

#### Stack ב-Swarm
```yaml
# docker-stack.yml
version: '3.8'

services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=appdb
      - POSTGRES_USER=appuser
      - POSTGRES_PASSWORD=apppass
    deploy:
      replicas: 1
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

```bash
# הפעלת stack
docker stack deploy -c docker-stack.yml myapp

# צפייה ב-services
docker stack services myapp

# הפסקת stack
docker stack down myapp
```

### Kubernetes עם Docker

#### המרת Docker Compose ל-Kubernetes
```bash
# התקנת Kompose
curl -L https://github.com/kubernetes/kompose/releases/download/v1.26.0/kompose-linux-amd64 -o kompose
chmod +x kompose
sudo mv ./kompose /usr/local/bin/kompose

# המרה
kompose convert -f docker-compose.yml

# הפעלה ב-Kubernetes
kubectl apply -f deployments/
kubectl apply -f services/
```

### CI/CD עם Docker

#### GitHub Actions
```yaml
# .github/workflows/docker.yml
name: Build and Deploy

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Build Docker image
      run: docker build -t myapp:${{ github.sha }} .
    
    - name: Run tests
      run: |
        docker run --rm myapp:${{ github.sha }} pytest
    
    - name: Push to registry
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker push myapp:${{ github.sha }}
```

### Monitoring ו-Logging

#### Prometheus ו-Grafana
```yaml
version: '3.8'

services:
  app:
    build: .
    labels:
      - "prometheus.scrape=true"
      - "prometheus.port=5000"

  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  grafana_data:
```

#### ELK Stack
```yaml
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.14.0
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9200:9200"
    volumes:
      - es_data:/usr/share/elasticsearch/data

  logstash:
    image: docker.elastic.co/logstash/logstash:7.14.0
    ports:
      - "5044:5044"
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf

  kibana:
    image: docker.elastic.co/kibana/kibana:7.14.0
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200

volumes:
  es_data:
```

---

## פרויקט מעשי מלא

### פרויקט: מערכת ניהול משימות (Todo API)

#### מבנה הפרויקט
```
todo-app/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── utils.py
├── tests/
│   ├── test_api.py
│   └── test_models.py
├── migrations/
├── docker/
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   └── nginx.conf
├── scripts/
│   ├── init-db.sql
│   └── seed-data.py
├── docker-compose.yml
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── requirements.txt
├── .env.example
└── README.md
```

#### app/__init__.py
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # הגדרות תצורה
    if config_name == 'development':
        app.config['DEBUG'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///todo_dev.db')
    elif config_name == 'testing':
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    else:  # production
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # אתחול הרחבות
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # רישום נתיבים
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app
```

#### app/models.py
```python
from . import db
from datetime import datetime
from enum import Enum

class TaskStatus(Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'

class Priority(Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Enum(TaskStatus), default=TaskStatus.PENDING)
    priority = db.Column(db.Enum(Priority), default=Priority.MEDIUM)
    due_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status.value,
            'priority': self.priority.value,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data['title'],
            description=data.get('description'),
            status=TaskStatus(data.get('status', 'pending')),
            priority=Priority(data.get('priority', 'medium')),
            due_date=datetime.fromisoformat(data['due_date']) if data.get('due_date') else None
        )
```

#### app/routes.py
```python
from flask import Blueprint, request, jsonify
from . import db
from .models import Task, TaskStatus, Priority

api_bp = Blueprint('api', __name__)

@api_bp.route('/tasks', methods=['GET'])
def get_tasks():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status')
    priority = request.args.get('priority')
    
    query = Task.query
    
    if status:
        query = query.filter(Task.status == TaskStatus(status))
    if priority:
        query = query.filter(Task.priority == Priority(priority))
    
    tasks = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'tasks': [task.to_dict() for task in tasks.items],
        'total': tasks.total,
        'pages': tasks.pages,
        'current_page': tasks.page
    })

@api_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    task = Task.from_dict(data)
    db.session.add(task)
    db.session.commit()
    
    return jsonify(task.to_dict()), 201

@api_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict())

@api_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'status' in data:
        task.status = TaskStatus(data['status'])
    if 'priority' in data:
        task.priority = Priority(data['priority'])
    if 'due_date' in data:
        task.due_date = datetime.fromisoformat(data['due_date']) if data['due_date'] else None
    
    db.session.commit()
    return jsonify(task.to_dict())

@api_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return '', 204

@api_bp.route('/tasks/stats', methods=['GET'])
def get_stats():
    stats = {
        'total': Task.query.count(),
        'by_status': {},
        'by_priority': {}
    }
    
    for status in TaskStatus:
        stats['by_status'][status.value] = Task.query.filter_by(status=status).count()
    
    for priority in Priority:
        stats['by_priority'][priority.value] = Task.query.filter_by(priority=priority).count()
    
    return jsonify(stats)

@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'version': '1.0.0'})
```

#### docker/Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# התקנת תלותיות מערכת
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# התקנת תלותיות Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# העתקת קוד
COPY . .

# יצירת משתמש לא רוט
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app
USER app

# חשיפת פורט
EXPOSE 5000

# פקודת הפעלה
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:create_app()"]
```

#### docker-compose.yml
```yaml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: docker/Dockerfile
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://todo_user:todo_pass@postgres:5432/todo_db
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      postgres:
        condition: service_healthy
    restart: unless-stopped
    networks:
      - todo-network

  postgres:
    image: postgres:13-alpine
    environment:
      - POSTGRES_DB=todo_db
      - POSTGRES_USER=todo_user
      - POSTGRES_PASSWORD=todo_pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init-db.sql:/docker-entrypoint-initdb.d/init-db.sql
    ports:
      - "5432:5432"
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U todo_user -d todo_db"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - todo-network

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped
    command: redis-server --appendonly yes
    networks:
      - todo-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./docker/nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - api
    restart: unless-stopped
    networks:
      - todo-network

volumes:
  postgres_data:
  redis_data:

networks:
  todo-network:
    driver: bridge
```

#### docker/nginx.conf
```nginx
events {
    worker_connections 1024;
}

http {
    upstream api {
        server api:5000;
    }

    server {
        listen 80;
        
        location / {
            proxy_pass http://api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

#### tests/test_api.py
```python
import pytest
import json
from app import create_app, db

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_health_check(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_create_task(client):
    task_data = {
        'title': 'Test Task',
        'description': 'Test Description',
        'priority': 'high'
    }
    response = client.post('/api/tasks', 
                          data=json.dumps(task_data),
                          content_type='application/json')
    assert response.status_code == 201
    assert response.json['title'] == 'Test Task'

def test_get_tasks(client):
    # יצירת משימה ראשונה
    client.post('/api/tasks', 
               data=json.dumps({'title': 'Task 1'}),
               content_type='application/json')
    
    response = client.get('/api/tasks')
    assert response.status_code == 200
    assert len(response.json['tasks']) == 1
```

#### scripts/init-db.sql
```sql
-- הרחבות PostgreSQL לשיפור ביצועים
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- אינדקסים לשיפור ביצועים
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);
CREATE INDEX IF NOT EXISTS idx_tasks_created_at ON tasks(created_at);
CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date);
```

#### Makefile
```makefile
.PHONY: help build up down logs test clean

help:
	@echo "Available commands:"
	@echo "  build     - Build Docker images"
	@echo "  up        - Start services"
	@echo "  down      - Stop services"
	@echo "  logs      - Show logs"
	@echo "  test      - Run tests"
	@echo "  clean     - Clean up"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

test:
	docker-compose run --rm api pytest

clean:
	docker-compose down -v
	docker system prune -f
```

---

## משאבים נוספים

### תיעוד רשמי
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

### קורסים ומדריכים
- [Docker Mastery](https://www.udemy.com/course/docker-mastery/)
- [Play with Docker](https://labs.play-with-docker.com/)
- [Docker Curriculum](https://docker-curriculum.com/)

### כלים ותוספים
- [Dive](https://github.com/wagoodman/dive) - ניתוח גודל Images
- [ctop](https://github.com/bcicen/ctop) - ממשק לניהול קונטיינרים
- [lazydocker](https://github.com/jesseduffield/lazydocker) - ממשק טרמינלי
- [Portainer](https://www.portainer.io/) - ממשק וובי לניהול Docker

### קהילות ופורומים
- [Docker Community Forums](https://forums.docker.com/)
- [r/docker](https://www.reddit.com/r/docker/)
- [Stack Overflow Docker Tag](https://stackoverflow.com/questions/tagged/docker)

### תבניות ודוגמאות
- [Docker Samples](https://github.com/docker-samples)
- [Awesome Docker](https://github.com/veggiemonk/awesome-docker)
- [Dockerfile Best Practices](https://github.com/hexops/dockerfile)

---

## סיכום

מדריך זה כיסה את כל ההיבטים החשובים של Docker עבור מפתחי REST API:

1. **יסודות Docker** - Images, Containers, Dockerfile
2. **REST API עם Docker** - בנייה, הפעלה, ושילוב עם מסדי נתונים
3. **Docker Compose** - ניהול אפליקציות מרובות-שירותים
4. **רשתות ואחסון** - תקשורת בין קונטיינרים וניהול נתונים
5. **Best Practices** - אופטימיזציה ואבטחה
6. **מקרים מתקדמים** - Swarm, Kubernetes, CI/CD
7. **פרויקט מעשי** - יישום מלא של כל המושגים

עם הידע הזה, אתם מוכנים לפתח REST API מקצועיים עם Docker ברמה הגבוהה ביותר. המשיכו לתרגל, לחקור, ולבנות פרויקטים מורכבים יותר!

---

**זכויות יוצרים:** מדריך זה נכתב למטרות חינוך בלבד. אין להפיץ או למכור ללא רשות.

**עדכון אחרון:** מרץ 2026
