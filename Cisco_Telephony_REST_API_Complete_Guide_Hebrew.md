# מדריך מקיף ל-REST API בטלפוניה של סיסקו

## תוכן עניינים

### חלק 1: מבוא לטלפוניה של סיסקו
- סקירה כללית של שרתי סיסקו
- הקדמה ל-REST API
- סביבת Docker לפיתוח

### חלק 2: שרתי טלפוניה של סיסקו
- UCCX - Cisco Unified Contact Center Express
- CUCM - Cisco Unified Communications Manager
- IMP - Cisco Unified IM and Presence
- MP - Cisco Media Platform
- CMS - Cisco Meeting Server
- TGW - Telephony Gateway
- SBC - Session Border Controller
- Expressway

### חלק 3: פיתוח REST API
- יסודות REST API
- אימות והרשאות
- דוגמאות קוד
- שילוב עם Docker

---

# חלק 1: מבוא לטלפוניה של סיסקו

## פרק 1: סקירה כללית של מערכות טלפוניה של סיסקו

### 1.1 היסטוריה והתפתחות

סיסקו מערכות תקשורת היא אחת החברות המובילות בעולם בפתרונות תקשורת ארגוניים. החברה החלה את דרכה בשנות ה-80 של המאה ה-20 ומאז הפכה לגורם מרכזי בשוק הטלפוניה העסקית. מערכות טלפוניה של סיסקו מספקות פתרונות מתקדמים לתקשורת קולית, וידאו, ומסרים מיידיים עבור ארגונים מכל הגדלים.

המערכות המודרניות של סיסקו מבוססות על פרוטוקול IP (Internet Protocol), המאפשר גמישות רבה ויכולות מתקדמות שלא היו אפשריות במערכות טלפוניה מסורתיות. המעבר לטלפוניה מבוססת IP פתח צוהר לפיתוח יישומים ושירותים חדשים, כולל ממשקי REST API המאפשרים אינטגרציה עם מערכות אחרות.

### 1.2 ארכיטקטורה של מערכות סיסקו

מערכות טלפוניה של סיסקו בנויות על ארכיטקטורה מודולרית המאפשרת גמישות והתאמה אישית לצרכים של כל ארגון. הארכיטקטורה הבסיסית כוללת:

**שכבת התשתית (Infrastructure Layer)**:
- רשת IP ותשתית חומרה
- מתגים (Switches) ונתבים (Routers)
- שרתים ומערכות אחסון

**שכבת השירותים (Services Layer)**:
- שירותי קול ווידאו
- שירותי הודעות ונוכחות
- שירותי מרכזיות ושיחות ועידה

**שכבת היישומים (Applications Layer)**:
- יישומי לקוח (Softphones, WebRTC)
- ממשקי API לאינטגרציה
- יישומים עסקיים ייעודיים

### 1.3 סוגי שרתים עיקריים

במערכת טלפוניה של סיסקו קיימים מספר סוגי שרתים, כל אחד עם תפקיד ייעודי:

**CUCM (Cisco Unified Communications Manager)**
- השרת המרכזי לניהול שיחות קוליות
- אחראי על ניהול מכשירים, מספרי טלפון, וניתוב שיחות
- מספק שירותי רישום, אימות, וסינכרון

**UCCX (Cisco Unified Contact Center Express)**
- מרכז שירות לקוחות מתקדם
- כולל ניהול תורים (Queuing), הפצת שיחות, ודיווחים
- תומך ב-IVR וסקריפטים מתקדמים

**IMP (Cisco Unified IM and Presence)**
- שירותי מסרים מיידיים ונוכחות
- מאפשר לראות סטטוס משתמשים ולתקשר איתם
- משולב עם יישומי לקוח שונים

**CMS (Cisco Meeting Server)**
- שירותי ועידות וידאו מתקדמים
- תומך במספר רב של משתתפים
- מספק יכולות שיתוף מסך ושיתוף תוכן

### 1.4 יתרונות של מערכות סיסקו

**גמישות והתאמה אישית**:
מערכות סיסקו מאפשרות התאמה אישית רבה לצרכים של הארגון. ניתן להגדיר כללים מורכבים לניתוב שיחות, ליצור קבוצות משתמשים, ולהגדיר שירותים מיוחדים.

**אמינות וזמינות גבוהה**:
המערכות תוכננו לפעול 24/7 עם זמינות של 99.999%. קיימים מנגנוני גיבוי ושחזור מתקדמים המבטיחים רציפות פעולה גם במקרה של תקלות.

**אבטחה**:
סיסקו משקיעה משאבים רבים באבטחת המערכות. קיימים מנגנוני אימות מתקדמים, הצפנה, וניטור אבטחה.

**יכולת הרחבה**:
המערכות נבנו באופן מודולרי המאפשר הוספת שרתים ושירותים נוספים עם צמיחת הארגון.

### 1.5 REST API במערכות סיסקו

REST API (Representational State Transfer Application Programming Interface) הוא סטנדרט לתקשורת בין מערכות תוכנה שונות. במערכות סיסקו, REST API מאפשר למפתחים ליצור יישומים המתקשרים עם השרתים בצורה פשוטה וסטנדרטית.

**יתרונות REST API**:
- פשטות וקלות שימוש
- תמיכה בפורמטים סטנדרטיים (JSON, XML)
- יכולת אינטגרציה עם מערכות קיימות
- תיעוד מקיף ודוגמאות קוד
- תמיכה בשפות תכנות מגוונות

**שימושים נפוצים**:
- אוטומציה של ניהול מערכת
- יצירת יישומים עסקיים ייעודיים
- אינטגרציה עם מערכות CRM ו-ERP
- פיתוח פורטלים לשירות לקוחות
- יצירת דאשבורדים לניטור ובקרה

---

## פרק 2: הקדמה ל-REST API

### 2.1 מה זה REST API?

REST API הוא סגנון ארכיטקטוני לעיצוב מערכות מבוזרות. הוא מבוסס על עקרונות פשוטים המאפשרים תקשורת יעילה בין מערכות שונות. REST הוצג לראשונה על ידי Roy Fielding בשנת 2000 ומאז הפך לסטנדרט דה-פקטו לפיתוח API.

**עקרונות בסיסיים של REST**:

**Client-Server Architecture**:
הלקוח והשרת מופרדים זה מזה, מה שמאפשר פיתוח עצמאי של כל רכיב.

**Statelessness**:
כל בקשה מהלקוח לשרת מכילה את כל המידע הדרוש לעיבודה. השרת אינו שומר מצב של הלקוח בין בקשות.

**Cacheability**:
תגובות מהשרת יכולות להיות מאוחסנות ב-cache, מה שמשפר את הביצועים.

**Uniform Interface**:
ממשק אחיד המבוסס על פעולות סטנדרטיות (GET, POST, PUT, DELETE).

**Layered System**:
הארכיטקטורה יכולה לכלול מספר שכבות, כאשר כל שכבה אינה יודעת על קיומן של שכבות אחרות.

### 2.2 HTTP Methods ב-REST

REST משתמש בפעולות HTTP סטנדרטיות לביצוע פעולות CRUD (Create, Read, Update, Delete):

**GET**:
- משמש לקבלת מידע מהשרת
- בטוח לשימוש חוזר (idempotent)
- לא גורם לשינוי במצב השרת
- דוגמה: `GET /api/users/123`

**POST**:
- משמש ליצירת משאבים חדשים
- לא בטוח לשימוש חוזר
- גורם לשינוי במצב השרת
- דוגמה: `POST /api/users`

**PUT**:
- משמש לעדכון משאבים קיימים
- בטוח לשימוש חוזר
- גורם לשינוי במצב השרת
- דוגמה: `PUT /api/users/123`

**DELETE**:
- משמש למחיקת משאבים
- בטוח לשימוש חוזר
- גורם לשינוי במצב השרת
- דוגמה: `DELETE /api/users/123`

**PATCH**:
- משמש לעדכון חלקי של משאבים
- לא בטוח לשימוש חוזר
- גורם לשינוי במצב השרת
- דוגמה: `PATCH /api/users/123`

### 2.3 פורמטים נתמכים

REST API תומך במגוון פורמטים להעברת מידע:

**JSON (JavaScript Object Notation)**:
- הפורמט הפופולרי ביותר
- קל לקריאה וכתיבה
- נתמך בכל שפות התכנות המודרניות
- דוגמה:
```json
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+972-50-1234567"
}
```

**XML (eXtensible Markup Language)**:
- פורמט ותיק ומבוסס
- תומך בסכימות ו-validation
- פחות פופולרי ב-API חדשים
- דוגמה:
```xml
<user>
  <id>123</id>
  <name>John Doe</name>
  <email>john@example.com</email>
  <phone>+972-50-1234567</phone>
</user>
```

**Plain Text**:
- משמש למידע פשוט
- שימושי ללוגים והודעות פשוטות
- דוגמה: `"User created successfully"`

### 2.4 קודי סטטוס HTTP

HTTP מגדיר קודי סטטוס סטנדרטיים לתגובות מהשרת:

**קודי הצלחה (2xx)**:
- `200 OK` - הבקשה בוצעה בהצלחה
- `201 Created` - משאב נוצר בהצלחה
- `204 No Content` - הבקשה בוצעה אך אין תוכן להחזיר

**קודי הפניה (3xx)**:
- `301 Moved Permanently` - המשאב הועבר לצמיתות
- `302 Found` - המשאב הועבר זמנית

**קודי שגיאת לקוח (4xx)**:
- `400 Bad Request` - בקשה לא תקינה
- `401 Unauthorized` - נדרש אימות
- `403 Forbidden` - אין הרשאה לביצוע הפעולה
- `404 Not Found` - המשאב לא נמצא
- `429 Too Many Requests` - יותר מדי בקשות

**קודי שגיאת שרת (5xx)**:
- `500 Internal Server Error` - שגיאה פנימית בשרת
- `502 Bad Gateway` - השרת קיבל תגובה לא תקינה משרת אחר
- `503 Service Unavailable` - השירות אינו זמין

### 2.5 אימות והרשאות

אימות הוא תהליך אימות זהות הלקוח, בעוד הרשאות קובעות מה הלקוח רשאי לעשות.

**שיטות אימות נפוצות**:

**Basic Authentication**:
- שם משתמש וסיסמה ב-base64
- פשוט אך לא מאובטח
- מומלץ לשימוש עם HTTPS

**API Key**:
- מפתח ייחודי לכל לקוח
- נשלח ב-header או כפרמטר
- קל ליישום וניהול

**Bearer Token (JWT)**:
- טוקן JWT המכיל מידע על המשתמש
- חתום דיגיטלית
- תומך ב-expiration ו-refresh

**OAuth 2.0**:
- תקן מתקדם לאימות
- תומך ב-scopes ו-permissions
- מתאים לאפליקציות צד שלישי

---

## פרק 3: סביבת Docker לפיתוח

### 3.1 מה זה Docker?

Docker היא פלטפורמת קונטיינרים המאפשרת לעטוף יישומים עם כל התלותיות שלהם בסביבה בידודה. קונטיינרים הם קלי משקל, ניידים, ועקביים, מה שהופך אותם לאידיאליים לפיתוח ופריסה.

**יתרונות Docker**:

**בידוד**:
כל קונטיינר פועל בסביבה מבודדת משאר המערכת, מה שמונע התנגשויות בין תלותיות.

**ניידות**:
קונטיינרים עובדים באותו אופן בכל סביבה - מחשב פיתוח, שרת בדיקה, או סביבת ייצור.

**עקביות**:
סביבת הפיתוח זהה לסביבת הייצור, מה שמפחית בעיות "עובד במחשב שלי".

**יעילות**:
קונטיינרים צורכים פחות משאבים ממכונות וירטואליות מסורתיות.

**מהירות**:
הפעלת קונטיינרים מהירה משמעותית מהפעלת מכונות וירטואליות.

### 3.2 מושגים בסיסיים ב-Docker

**Image (תמונה)**:
תבנית קבועה המכילה את כל מה שנדרש להפעלת קונטיינר - קוד, ספריות, כלי עזר, וקבצי תצורה.

**Container (קונטיינר)**:
מופע פועל של image. קונטיינרים הם בדידים וניתנים להרצה.

**Dockerfile**:
קובץ טקסט המכיל הוראות לבניית image חדש.

**Docker Compose**:
כלי להגדרת והפעלת אפליקציות מרובות קונטיינרים.

**Registry**:
מאגר centralized לאחסון ושיתוף images (למשל Docker Hub).

### 3.3 התקנת Docker

**Windows**:
1. הורד את Docker Desktop מהאתר הרשמי
2. הפעל את התקנן ופעל לפי ההוראות
3. הפעל את Docker Desktop
4. ודא ש-Docker פועל באמצעות `docker --version`

**macOS**:
1. הורד את Docker Desktop מהאתר הרשמי
2. גרור את הקובץ לתיקיית Applications
3. הפעל את Docker Desktop
4. ודא את ההתקנה עם `docker --version`

**Linux**:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker

# CentOS/RHEL
sudo yum install docker docker-compose
sudo systemctl start docker
sudo systemctl enable docker
```

### 3.4 Dockerfile בסיסי

Dockerfile הוא קובץ טקסט המכיל הוראות לבניית image. הנה דוגמה בסיסית:

```dockerfile
# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "app.py"]
```

**הוראות נפוצות**:

**FROM**:
מגדיר את ה-image הבסיסי.

**WORKDIR**:
מגדיר את ספריית העבודה.

**COPY**:
מעתיק קבצים מהמחשב המארח ל-image.

**RUN**:
מפעיל פקודות בזמן בניית ה-image.

**EXPOSE**:
מצהיר על פורט שהקונטיינר יפתח.

**CMD**:
מגדיר את הפקודה שתופעל כשהקונטיינר מופעל.

### 3.5 Docker Compose

Docker Compose מאפשר הגדרת אפליקציות מרובות קונטיינרים בקובץ YAML פשוט:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=development
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=cisco_api
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

**פקודות Docker Compose**:

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs

# Execute command in container
docker-compose exec web bash
```

### 3.6 שימוש ב-Docker לפיתוח REST API

**יתרונות לפיתוח REST API**:

**סביבת פיתוח עקבית**:
כל המפתחים עובדים באותה סביבה, מה שמפחית בעיות תלות.

**בדיקות אוטומטיות**:
קל להפעיל סביבות בדיקה מבודדות.

**פריסה קלה**:
אותו קונטיינר יכול לפעול בסביבת פיתוח, בדיקה, וייצור.

**ניהול תלותיות**:
כל התלותיות מוגדרות במקום אחד ומנוהלות בצורה אוטומטית.

**דוגמה לפרויקט REST API עם Docker**:

```dockerfile
# Dockerfile
FROM node:16-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://user:pass@db:5432/cisco
    depends_on:
      - db
      - redis

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=cisco
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6-alpine

volumes:
  postgres_data:
```

---

# חלק 2: שרתי טלפוניה של סיסקו

## פרק 4: UCCX - Cisco Unified Contact Center Express

### 4.1 מבוא ל-UCCX

Cisco Unified Contact Center Express (UCCX) הוא פתרון מרכז שירות לקוחות מתקדם המיועד לארגונים קטנים עד בינוניים. UCCX מספק יכולות מתקדמות לניהול שיחות נכנסות, הפצת שיחות לסוכנים, ומתן שירות אוטומטי ללקוחות.

**תכונות עיקריות**:

**ניהול תורים (Queuing)**:
- תורים מרובים עם עדיפויות שונות
- הודעות מתקדמות ללקוחות ממתינים
- אסטרטגיות הפצה גמישות

**Interactive Voice Response (IVR)**:
- מערכת תגובה קולית אינטראקטיבית
- זיהוי קול וזיהוי דיבור
- אינטגרציה עם מסדי נתונים

**ניהול סוכנים**:
- ניהול זמינות סוכנים
- מיומנויות והכשרות
- מעקב ביצועים ודיווחים

**דיווחים ואנליטיקה**:
- דיווחים בזמן אמת
- ניתוח היסטוריית שיחות
- מדדי ביצועים מתקדמים

### 4.2 ארכיטקטורה של UCCX

**רכיבים עיקריים**:

**UCCX Engine**:
- הלב המרכזי של המערכת
- מטפל בכל שיחות נכנסות
- מפעיל סקריפטים וכללים

**CTI Server**:
- ממשק תקשורת טלפוניה ממוחשבת
- מאפשר אינטגרציה עם יישומים חיצוניים
- תומך בממשקי API מתקדמים

**Database**:
- מסד נתונים מובנה לאחסון הגדרות והיסטוריה
- תומך בגיבוי ושחזור
- מספק יכולות דיווח מתקדמות

**Administration Interface**:
- ממשק ניהול מבוסס ווב
- קונסולת ניהול סוכנים
- כלי עריכת סקריפטים

### 4.3 REST API ב-UCCX

UCCX מספק ממשק REST API מקיף המאפשר שליטה מלאה על פעולות המערכת. ה-API מאפשר אוטומציה של ניהול, אינטגרציה עם מערכות אחרות, ופיתוח יישומים ייעודיים.

**קטגוריות API עיקריות**:

**Agent API**:
- ניהול מצב סוכנים
- העברת שיחות
- מעקב ביצועים
- דוגמה:
```javascript
// Get agent status
GET /uccx/v2/agents/{agentId}

// Change agent state
PUT /uccx/v2/agents/{agentId}/state
{
  "state": "READY",
  "reasonCode": "0"
}
```

**Supervisor API**:
- ניהול צוותים
- מעקב שיחות בזמן אמת
- דיווחים וסטטיסטיקות
- דוגמה:
```javascript
// Get team statistics
GET /uccx/v2/teams/{teamId}/statistics

// Monitor agent call
POST /uccx/v2/agents/{agentId}/monitor
{
  "type": "SILENT_MONITOR"
}
```

**Configuration API**:
- ניהול תורים ומיומנויות
- הגדרות IVR
- ניהול סקריפטים
- דוגמה:
```javascript
// Create queue
POST /uccx/v2/queues
{
  "name": "Sales Queue",
  "description": "Sales department queue",
  "maxWaitTime": 300
}

// Update skill
PUT /uccx/v2/skills/{skillId}
{
  "name": "Technical Support",
  "description": "Technical support skill"
}
```

**Reporting API**:
- דיווחים היסטוריים
- סטטיסטיקות בזמן אמת
- יצוא נתונים
- דוגמה:
```javascript
// Get historical report
GET /uccx/v2/reports/agent-summary?startDate=2023-01-01&endDate=2023-01-31

// Get real-time statistics
GET /uccx/v2/statistics/realtime/queue/{queueId}
```

### 4.4 אימות ב-UCCX API

UCCX תומך במספר שיטות אימות:

**Basic Authentication**:
- שם משתמש וסיסמה
- מומלץ לשימוש בסביבות פיתוח
- דוגמה:
```javascript
headers: {
  'Authorization': 'Basic ' + btoa('username:password')
}
```

**JWT Token**:
- טוקן מאובטח עם expiration
- מתאים לאפליקציות צד שלישי
- דוגמה:
```javascript
// Get token
POST /uccx/v2/token
{
  "username": "admin",
  "password": "password"
}

// Use token
headers: {
  'Authorization': 'Bearer ' + token
}
```

**API Key**:
- מפתח ייחודי לכל אפליקציה
- ניתן לניהול דרך ממשק הניהול
- דוגמה:
```javascript
headers: {
  'X-API-Key': 'your-api-key-here'
}
```

### 4.5 דוגמת יישום ב-Python

הנה דוגמה מלאה ליישום המתקשר עם UCCX API:

```python
import requests
import json
from datetime import datetime, timedelta

class UCCXClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def get_agent_status(self, agent_id):
        """Get current agent status"""
        url = f"{self.base_url}/uccx/v2/agents/{agent_id}"
        response = self.session.get(url)
        return response.json()
    
    def set_agent_state(self, agent_id, state, reason_code="0"):
        """Change agent state"""
        url = f"{self.base_url}/uccx/v2/agents/{agent_id}/state"
        data = {
            "state": state,
            "reasonCode": reason_code
        }
        response = self.session.put(url, json=data)
        return response.json()
    
    def get_queue_statistics(self, queue_id):
        """Get real-time queue statistics"""
        url = f"{self.base_url}/uccx/v2/statistics/realtime/queue/{queue_id}"
        response = self.session.get(url)
        return response.json()
    
    def create_queue(self, name, description, max_wait_time=300):
        """Create new queue"""
        url = f"{self.base_url}/uccx/v2/queues"
        data = {
            "name": name,
            "description": description,
            "maxWaitTime": max_wait_time
        }
        response = self.session.post(url, json=data)
        return response.json()
    
    def get_agent_summary_report(self, start_date, end_date):
        """Get agent summary report"""
        url = f"{self.base_url}/uccx/v2/reports/agent-summary"
        params = {
            'startDate': start_date,
            'endDate': end_date
        }
        response = self.session.get(url, params=params)
        return response.json()

# Usage example
uccx = UCCXClient("https://uccx-server.example.com", "admin", "password")

# Get agent status
agent_status = uccx.get_agent_status("agent123")
print(f"Agent status: {agent_status}")

# Set agent to ready
uccx.set_agent_state("agent123", "READY")

# Get queue statistics
queue_stats = uccx.get_queue_statistics("sales_queue")
print(f"Queue stats: {queue_stats}")
```

### 4.6 שילוב עם Docker

הנה דוגמה להפעלת יישום UCCX עם Docker:

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "uccx_app.py"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  uccx-app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - UCCX_URL=https://uccx-server.example.com
      - UCCX_USERNAME=admin
      - UCCX_PASSWORD=password
    volumes:
      - ./logs:/app/logs

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"

volumes:
  logs:
```

---

## פרק 5: CUCM - Cisco Unified Communications Manager

### 5.1 מבוא ל-CUCM

Cisco Unified Communications Manager (CUCM) הוא המרכז השליטה והבקרה של מערכת התקשורת של סיסקו. CUCM הוא מערכת מבוססת IP המנהלת את כל היבטי התקשורת הקולית בארגון, כולל ניהול מכשירים, מספרי טלפון, ניתוב שיחות, ושירותים נלווים.

**תפקידים עיקריים**:

**ניהול מכשירים**:
- רישום וניהול טלפונים IP
- הגדרת פרופילים ותכונות
- עדכון קושחה ותצורה

**ניהול מספרים**:
- הקצאת מספרי טלפון ו-DID
- ניהול תבניות חיוג
- תכנון קידומותים וקידומות חיוג

**ניתוב שיחות**:
- ניתוב שיחות פנימיות וחיצוניות
- ניהול טראנקים וגייטוויים
- יישום כללי ניתוב

**שירותים נלווים**:
- דואר קולי
- הודעות מחכות
- שירותי אודיו-קונפרנס

### 5.2 ארכיטקטורה של CUCM

**רכיבים עיקריים**:

**CallManager Service**:
- השירות המרכזי לניהול שיחות
- מטפל ברישום מכשירים
- מבצע ניתוב שיחות

**Database**:
- מסד נתונים מובנה לאחסון הגדרות
- תומך ב-replication ו-clustering
- מספק גיבוי ושחזור

**CTI Manager**:
- מנהל חיבורי CTI
- תומך ביישומי צד שלישי
- מספק ממשקי API לאינטגרציה

**TFTP Service**:
- מספק קבצי תצורה למכשירים
- מפיץ קושחות ותמונות
- תומך במכשירים מגוונים

**CDR/CMR Services**:
- איסוף נתוני שיחות
- יצירת דיווחים מפורטים
- תמיכה בחיוב וניתוח

### 5.3 REST API ב-CUCM

CUCM מספק ממשק REST API רחב המאפשר ניהול מלא של המערכת. ה-API מאפשר אוטומציה של משימות ניהול, אינטגרציה עם מערכות אחרות, ופיתוח יישומים ייעודיים.

**קטגוריות API עיקריות**:

**Phone/Device API**:
- ניהול מכשירים וטלפונים
- הגדרת פרופילים ותכונות
- עדכון קושחה
- דוגמה:
```javascript
// Get phone details
GET /cucm/v2/phones/{phoneName}

// Add new phone
POST /cucm/v2/phones
{
  "name": "SEP001122334455",
  "description": "John Doe Phone",
  "product": "Cisco 8851",
  "devicePool": "Default"
}

// Update phone settings
PUT /cucm/v2/phones/{phoneName}
{
  "description": "Updated description",
  "callingSearchSpace": "Internal"
}
```

**Line/DN API**:
- ניהול מספרי טלפון ושורות
- הקצאת DID וקידומותים
- הגדרת תכונות שיחות
- דוגמה:
```javascript
// Get line details
GET /cucm/v2/lines/{pattern}/{partition}

// Add new line
POST /cucm/v2/lines
{
  "pattern": "1001",
  "partition": "Internal",
  "description": "John Doe Extension",
  "routePartition": "Internal"
}

// Update line settings
PUT /cucm/v2/lines/{pattern}/{partition}
{
  "description": "Updated line",
  "callForwardAll": "1002"
}
```

**User API**:
- ניהול משתמשים והרשאות
- הקצאת מכשירים ושורות
- ניהול קבוצות ותפקידים
- דוגמה:
```javascript
// Get user details
GET /cucm/v2/users/{userId}

// Add new user
POST /cucm/v2/users
{
  "userId": "jdoe",
  "firstName": "John",
  "lastName": "Doe",
  "primaryExtension": "1001"
}

// Assign device to user
PUT /cucm/v2/users/{userId}/devices
{
  "deviceName": "SEP001122334455"
}
```

**Route Pattern API**:
- ניהול תבניות ניתוב
- הגדרת קידומותים וטראנקים
- יישום כללי חיוג
- דוגמה:
```javascript
// Get route pattern
GET /cucm/v2/routePatterns/{pattern}/{partition}

// Add route pattern
POST /cucm/v2/routePatterns
{
  "pattern": "9.@",
  "partition": "PSTN",
  "description": "External calls",
  "routePartition": "PSTN",
  "gateway": "PSTN_GW"
}
```

**Gateway/Trunk API**:
- ניהול גייטוויים וטראנקים
- הגדרת SIP ו-H.323
- ניהול קיבולת וקידומותים
- דוגמה:
```javascript
// Get gateway details
GET /cucm/v2/gateways/{gatewayName}

// Add SIP trunk
POST /cucm/v2/sipTrunks
{
  "name": "PSTN_SIP_Trunk",
  "description": "PSTN SIP Trunk",
  "destination": "192.168.1.100",
  "port": 5060
}
```

### 5.4 אימות ב-CUCM API

CUCM תומך במספר שיטות אימות:

**AXL Authentication**:
- שם משתמש וסיסמה מ-CUCM
- דומה ל-AXL API המסורתי
- דוגמה:
```javascript
headers: {
  'Authorization': 'Basic ' + btoa('username:password')
}
```

**OAuth 2.0**:
- תקן מודרני לאימות
- תומך ב-scopes ו-permissions
- מתאים לאפליקציות צד שלישי
- דוגמה:
```javascript
// Get OAuth token
POST /cucm/v2/oauth/token
{
  "grant_type": "client_credentials",
  "client_id": "your_client_id",
  "client_secret": "your_client_secret"
}

// Use token
headers: {
  'Authorization': 'Bearer ' + access_token
}
```

**Certificate-based**:
- אימות מבוסס אישורים
- אבטחה גבוהה
- מתאים לסביבות ארגוניות

### 5.5 דוגמת יישום ב-Node.js

הנה דוגמה מלאה ליישום המתקשר עם CUCM API:

```javascript
const axios = require('axios');
const https = require('https');

class CUCMClient {
    constructor(base_url, username, password) {
        this.base_url = base_url;
        this.username = username;
        this.password = password;
        
        // Create HTTPS agent for self-signed certificates
        this.httpsAgent = new https.Agent({
            rejectUnauthorized: false
        });
        
        this.client = axios.create({
            baseURL: this.base_url,
            auth: {
                username: this.username,
                password: this.password
            },
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            httpsAgent: this.httpsAgent
        });
    }
    
    async getPhone(phoneName) {
        try {
            const response = await this.client.get(`/cucm/v2/phones/${phoneName}`);
            return response.data;
        } catch (error) {
            throw new Error(`Failed to get phone: ${error.message}`);
        }
    }
    
    async addPhone(phoneData) {
        try {
            const response = await this.client.post('/cucm/v2/phones', phoneData);
            return response.data;
        } catch (error) {
            throw new Error(`Failed to add phone: ${error.message}`);
        }
    }
    
    async updatePhone(phoneName, phoneData) {
        try {
            const response = await this.client.put(`/cucm/v2/phones/${phoneName}`, phoneData);
            return response.data;
        } catch (error) {
            throw new Error(`Failed to update phone: ${error.message}`);
        }
    }
    
    async deletePhone(phoneName) {
        try {
            const response = await this.client.delete(`/cucm/v2/phones/${phoneName}`);
            return response.data;
        } catch (error) {
            throw new Error(`Failed to delete phone: ${error.message}`);
        }
    }
    
    async getLine(pattern, partition) {
        try {
            const response = await this.client.get(`/cucm/v2/lines/${pattern}/${partition}`);
            return response.data;
        } catch (error) {
            throw new Error(`Failed to get line: ${error.message}`);
        }
    }
    
    async addLine(lineData) {
        try {
            const response = await this.client.post('/cucm/v2/lines', lineData);
            return response.data;
        } catch (error) {
            throw new Error(`Failed to add line: ${error.message}`);
        }
    }
    
    async getUser(userId) {
        try {
            const response = await this.client.get(`/cucm/v2/users/${userId}`);
            return response.data;
        } catch (error) {
            throw new Error(`Failed to get user: ${error.message}`);
        }
    }
    
    async addUser(userData) {
        try {
            const response = await this.client.post('/cucm/v2/users', userData);
            return response.data;
        } catch (error) {
            throw new Error(`Failed to add user: ${error.message}`);
        }
    }
    
    async assignDeviceToUser(userId, deviceName) {
        try {
            const response = await this.client.put(`/cucm/v2/users/${userId}/devices`, {
                deviceName: deviceName
            });
            return response.data;
        } catch (error) {
            throw new Error(`Failed to assign device: ${error.message}`);
        }
    }
}

// Usage example
async function main() {
    const cucm = new CUCMClient('https://cucm-server.example.com', 'admin', 'password');
    
    try {
        // Add new phone
        const phoneData = {
            name: 'SEP001122334455',
            description: 'John Doe Phone',
            product: 'Cisco 8851',
            devicePool: 'Default'
        };
        
        const phone = await cucm.addPhone(phoneData);
        console.log('Phone added:', phone);
        
        // Add new line
        const lineData = {
            pattern: '1001',
            partition: 'Internal',
            description: 'John Doe Extension'
        };
        
        const line = await cucm.addLine(lineData);
        console.log('Line added:', line);
        
        // Add new user
        const userData = {
            userId: 'jdoe',
            firstName: 'John',
            lastName: 'Doe',
            primaryExtension: '1001'
        };
        
        const user = await cucm.addUser(userData);
        console.log('User added:', user);
        
        // Assign phone to user
        await cucm.assignDeviceToUser('jdoe', 'SEP001122334455');
        console.log('Device assigned to user');
        
    } catch (error) {
        console.error('Error:', error.message);
    }
}

main();
```

### 5.6 שילוב עם Docker

הנה דוגמה להפעלת יישום CUCM עם Docker:

```dockerfile
# Dockerfile
FROM node:16-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["node", "cucm_app.js"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  cucm-app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - CUCM_URL=https://cucm-server.example.com
      - CUCM_USERNAME=admin
      - CUCM_PASSWORD=password
    volumes:
      - ./logs:/app/logs
      - ./config:/app/config

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"

volumes:
  logs:
  config:
```

---

## פרק 6: IMP - Cisco Unified IM and Presence

### 6.1 מבוא ל-IMP

Cisco Unified IM and Presence (IMP) הוא שירות מסרים מיידיים ונוכחות המשלים את מערכת התקשורת של סיסקו. IMP מאפשר למשתמשים לראות את סטטוס הנוכחות של עמיתים, לשלוח הודעות מיידיות, ולהשתתף בשיחות ועידה מתקדמות.

**תכונות עיקריות**:

**נוכחות (Presence)**:
- הצגת סטטוס משתמשים בזמן אמת
- מצבים שונים: זמין, עסוק, בפגישה, לא זמין
- אינטגרציה עם יומן ושיחות טלפון

**מסרים מיידיים (IM)**:
- שיחות פרטיות וקבוצתיות
- העברת קבצים ותמונות
- היסטוריית שיחות מאוחסנת

**שיחות ועידה**:
- ועידות וידאו ושמע
- שיתוף מסך ותוכן
- לוח לבן משותף

**אינטגרציה**:
- שילוב עם יישומי לקוח שונים
- תמיכה ב-Jabber ו-WebEx
- API לאינטגרציה עם מערכות צד שלישי

### 6.2 ארכיטקטורה של IMP

**רכיבים עיקריים**:

**Presence Engine**:
- מנוע הנוכחות המרכזי
- מטפל בעדכוני סטטוס
- מנהל חוקי נוכחות

**XMPP Server**:
- שרת הפרוטוקול המורחב למסרים מיידיים
- מנהל חיבורי לקוחות
- מספק שירותי ניתוב הודעות

**Database**:
- מסד נתונים לאחסון קשרים והיסטוריה
- תומך ב-replication
- מספק גיבוי ושחזור

**Client Applications**:
- Jabber for Windows/Mac
- Jabber for Mobile
- Web-based clients
- יישומי צד שלישי

### 6.3 REST API ב-IMP

IMP מספק ממשק REST API המאפשר ניהול נוכחות, מסרים מיידיים, ואינטגרציה עם מערכות אחרות. ה-API מאפשר פיתוח יישומים ייעודיים המשתמשים ביכולות התקשורת של IMP.

**קטגוריות API עיקריות**:

**Presence API**:
- קבלת סטטוס משתמשים
- עדכון סטטוס אישי
- הרשמה לעדכוני נוכחות
- דוגמה:
```javascript
// Get user presence
GET /imp/v2/users/{userId}/presence

// Update user presence
PUT /imp/v2/users/{userId}/presence
{
  "status": "Available",
  "activity": "Working"
}

// Subscribe to presence updates
POST /imp/v2/subscriptions/presence
{
  "userIds": ["user1", "user2", "user3"]
}
```

**Messaging API**:
- שליחת הודעות מיידיות
- קבלת היסטוריית שיחות
- ניהול קבוצות וחדרים
- דוגמה:
```javascript
// Send message
POST /imp/v2/messages
{
  "to": "user2@example.com",
  "from": "user1@example.com",
  "body": "Hello, how are you?",
  "type": "chat"
}

// Get conversation history
GET /imp/v2/conversations/{conversationId}/messages

// Create group chat
POST /imp/v2/rooms
{
  "name": "Project Team",
  "participants": ["user1", "user2", "user3"]
}
```

**Contact API**:
- ניהול אנשי קשר
- יצירת קבוצות קשר
- סנכרון אנשי קשר
- דוגמה:
```javascript
// Get contacts
GET /imp/v2/users/{userId}/contacts

// Add contact
POST /imp/v2/users/{userId}/contacts
{
  "userId": "newcontact@example.com",
  "displayName": "John Doe",
  "groups": ["Work", "Team"]
}

// Create contact group
POST /imp/v2/users/{userId}/groups
{
  "name": "Development Team",
  "description": "Team members"
}
```

**Conference API**:
- יצירת ועידות
- הזמנת משתתפים
- ניהול הגדרות ועידה
- דוגמה:
```javascript
// Create conference
POST /imp/v2/conferences
{
  "title": "Team Meeting",
  "startTime": "2023-01-01T10:00:00Z",
  "duration": 60,
  "participants": ["user1", "user2", "user3"]
}

// Join conference
POST /imp/v2/conferences/{conferenceId}/join
{
  "userId": "user1",
  "media": ["audio", "video"]
}
```

### 6.4 אימות ב-IMP API

IMP תומך במספר שיטות אימות:

**Basic Authentication**:
- שם משתמש וסיסמה
- פשוט ליישום
- מומלץ לסביבות פיתוח

**OAuth 2.0**:
- תקן מודרני ומאובטח
- תומך ב-scopes ו-permissions
- מתאים לאפליקציות צד שלישי

**SAML Integration**:
- אימות חד-פעמי (SSO)
- משולב עם מערכות ארגוניות
- תומך ב-Active Directory

### 6.5 דוגמת יישום ב-PHP

הנה דוגמה מלאה ליישום המתקשר עם IMP API:

```php
<?php

class IMPClient {
    private $base_url;
    private $username;
    private $password;
    private $token;
    
    public function __construct($base_url, $username, $password) {
        $this->base_url = $base_url;
        $this->username = $username;
        $this->password = $password;
    }
    
    private function makeRequest($method, $endpoint, $data = null) {
        $ch = curl_init();
        
        $url = $this->base_url . '/imp/v2' . $endpoint;
        
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json',
            'Accept: application/json',
            'Authorization: Basic ' . base64_encode($this->username . ':' . $this->password)
        ]);
        
        if ($data) {
            curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
        }
        
        $response = curl_exec($ch);
        $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        
        if (curl_errno($ch)) {
            throw new Exception('Curl error: ' . curl_error($ch));
        }
        
        curl_close($ch);
        
        if ($http_code >= 400) {
            throw new Exception('HTTP error: ' . $http_code . ' - ' . $response);
        }
        
        return json_decode($response, true);
    }
    
    public function getUserPresence($userId) {
        return $this->makeRequest('GET', "/users/{$userId}/presence");
    }
    
    public function updateUserPresence($userId, $status, $activity = null) {
        $data = [
            'status' => $status
        ];
        
        if ($activity) {
            $data['activity'] = $activity;
        }
        
        return $this->makeRequest('PUT', "/users/{$userId}/presence", $data);
    }
    
    public function sendMessage($to, $from, $body, $type = 'chat') {
        $data = [
            'to' => $to,
            'from' => $from,
            'body' => $body,
            'type' => $type
        ];
        
        return $this->makeRequest('POST', '/messages', $data);
    }
    
    public function getConversationHistory($conversationId, $limit = 50) {
        return $this->makeRequest('GET', "/conversations/{$conversationId}/messages?limit={$limit}");
    }
    
    public function createGroupChat($name, $participants) {
        $data = [
            'name' => $name,
            'participants' => $participants
        ];
        
        return $this->makeRequest('POST', '/rooms', $data);
    }
    
    public function getContacts($userId) {
        return $this->makeRequest('GET', "/users/{$userId}/contacts");
    }
    
    public function addContact($userId, $contactId, $displayName, $groups = []) {
        $data = [
            'userId' => $contactId,
            'displayName' => $displayName,
            'groups' => $groups
        ];
        
        return $this->makeRequest('POST', "/users/{$userId}/contacts", $data);
    }
    
    public function createConference($title, $startTime, $duration, $participants) {
        $data = [
            'title' => $title,
            'startTime' => $startTime,
            'duration' => $duration,
            'participants' => $participants
        ];
        
        return $this->makeRequest('POST', '/conferences', $data);
    }
    
    public function joinConference($conferenceId, $userId, $media = ['audio']) {
        $data = [
            'userId' => $userId,
            'media' => $media
        ];
        
        return $this->makeRequest('POST', "/conferences/{$conferenceId}/join", $data);
    }
}

// Usage example
try {
    $imp = new IMPClient('https://imp-server.example.com', 'admin', 'password');
    
    // Get user presence
    $presence = $imp->getUserPresence('user1@example.com');
    echo "User presence: " . $presence['status'] . "\n";
    
    // Update user presence
    $imp->updateUserPresence('user1@example.com', 'Available', 'Working');
    
    // Send message
    $message = $imp->sendMessage(
        'user2@example.com',
        'user1@example.com',
        'Hello, how are you?'
    );
    echo "Message sent: " . $message['id'] . "\n";
    
    // Create group chat
    $room = $imp->createGroupChat('Project Team', ['user1', 'user2', 'user3']);
    echo "Group chat created: " . $room['id'] . "\n";
    
    // Get contacts
    $contacts = $imp->getContacts('user1@example.com');
    echo "Contacts count: " . count($contacts) . "\n";
    
    // Create conference
    $conference = $imp->createConference(
        'Team Meeting',
        '2023-01-01T10:00:00Z',
        60,
        ['user1', 'user2', 'user3']
    );
    echo "Conference created: " . $conference['id'] . "\n";
    
} catch (Exception $e) {
    echo "Error: " . $e->getMessage() . "\n";
}

?>
```

### 6.6 שילוב עם Docker

הנה דוגמה להפעלת יישום IMP עם Docker:

```dockerfile
# Dockerfile
FROM php:8.0-apache

WORKDIR /var/www/html

# Install required extensions
RUN docker-php-ext-install curl json

COPY . .

EXPOSE 80

CMD ["apache2-foreground"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  imp-app:
    build: .
    ports:
      - "8080:80"
    environment:
      - IMP_URL=https://imp-server.example.com
      - IMP_USERNAME=admin
      - IMP_PASSWORD=password
    volumes:
      - ./logs:/var/log/apache2
      - ./cache:/var/www/html/cache

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"

volumes:
  logs:
  cache:
```

---

## פרק 7: MP - Cisco Media Platform

### 7.1 מבוא ל-MP

Cisco Media Platform (MP) הוא שרת מדיה מתקדם המספק שירותי עיבוד ואחסון מדיה עבור מערכות תקשורת של סיסקו. MP משמש כבסיס למגוון שירותים כולל דואר קולי, הקלטות שיחות, ועיבוד אודיו מתקדם.

**תכונות עיקריות**:

**עיבוד אודיו**:
- המרת פורמטים (codec conversion)
- עיבוד קול דיגיטלי (DSP)
- שיפור איכות אודיו
- זיהוי דיבור וסינתזה

**אחסון מדיה**:
- אחסון הקלטות שיחות
- ניהול דואר קולי
- גיבוי ושחזור מדיה
- ארכיון ארוך טווח

**שירותי הקלטה**:
- הקלטת שיחות פעילות
- הקלטת שיחות ועידה
- הקלטת איכות שיחה (QoM)
- הקלטת מסכים

**אינטגרציה**:
- שילוב עם CUCM ו-UCCX
- API לאינטגרציה עם מערכות צד שלישי
- תמיכה בפרוטוקולים סטנדרטיים

### 7.2 ארכיטקטורה של MP

**רכיבים עיקריים**:

**Media Engine**:
- מנוע עיבוד המדיה המרכזי
- מטפל בהמרות ועיבוד אודיו
- מנהל משאבי DSP

**Storage Manager**:
- מנהל אחסון מדיה
- מטפל בגיבוי ושחזור
- מנהל מדיניות אחסון

**Recording Service**:
- שירות הקלטת שיחות
- מטפל בהקלטות פעילות
- מנהל איכות הקלטה

**API Gateway**:
- שער כניסה ל-API
- מנהל אימות והרשאות
- מספק ממשקי REST

**Database**:
- מסד נתונים למטא-דאטה
- מאחסן הגדרות והיסטוריה
- תומך ב-replication

### 7.3 REST API ב-MP

MP מספק ממשק REST API מקיף המאפשר שליטה מלאה על פעולות מדיה, הקלטות, ועיבוד אודיו. ה-API מאפשר אוטומציה של ניהול מדיה, אינטגרציה עם מערכות אחרות, ופיתוח יישומים ייעודיים.

**קטגוריות API עיקריות**:

**Recording API**:
- הפעלת הקלטות
- ניהול הקלטות קיימות
- הפסקת הקלטות
- דוגמה:
```javascript
// Start recording
POST /mp/v2/recordings
{
  "callId": "call123",
  "participants": ["user1", "user2"],
  "quality": "high",
  "format": "mp3"
}

// Get recording details
GET /mp/v2/recordings/{recordingId}

// Stop recording
POST /mp/v2/recordings/{recordingId}/stop

// Download recording
GET /mp/v2/recordings/{recordingId}/download
```

**Media Processing API**:
- המרת פורמטים
- עיבוד אודיו
- שיפור איכות
- דוגמה:
```javascript
// Convert audio format
POST /mp/v2/media/convert
{
  "inputFile": "recording.wav",
  "outputFormat": "mp3",
  "quality": "high"
}

// Enhance audio quality
POST /mp/v2/media/enhance
{
  "inputFile": "recording.mp3",
  "noiseReduction": true,
  "volumeNormalization": true
}

// Transcribe audio
POST /mp/v2/media/transcribe
{
  "inputFile": "recording.mp3",
  "language": "en-US"
}
```

**Storage API**:
- ניהול אחסון מדיה
- גיבוי ושחזור
- מדיניות אחסון
- דוגמה:
```javascript
// Get storage usage
GET /mp/v2/storage/usage

// Backup recordings
POST /mp/v2/storage/backup
{
  "source": "recordings",
  "destination": "backup_server",
  "retention": "30d"
}

// Restore recordings
POST /mp/v2/storage/restore
{
  "backupId": "backup123",
  "target": "recordings"
}
```

**Configuration API**:
- הגדרות מערכת
- מדיניות הקלטה
- ניהול משאבים
- דוגמה:
```javascript
// Get system configuration
GET /mp/v2/configuration

// Update recording policy
PUT /mp/v2/configuration/recording
{
  "defaultQuality": "high",
  "autoDelete": "90d",
  "compressionEnabled": true
}

// Set storage policy
PUT /mp/v2/configuration/storage
{
  "maxStorage": "1TB",
  "compressionEnabled": true,
  "backupEnabled": true
}
```

### 7.4 אימות ב-MP API

MP תומך במספר שיטות אימות:

**API Key Authentication**:
- מפתח API ייחודי
- פשוט ליישום
- מתאים לאפליקציות פנימיות

**OAuth 2.0**:
- תקן מודרני ומאובטח
- תומך ב-scopes ו-permissions
- מתאים לאפליקציות צד שלישי

**Certificate-based**:
- אימות מבוסס אישורים
- אבטחה גבוהה
- מתאים לסביבות ארגוניות

### 7.5 דוגמת יישום ב-Go

הנה דוגמה מלאה ליישום המתקשר עם MP API:

```go
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io"
    "net/http"
    "os"
    "time"
)

type MPClient struct {
    BaseURL    string
    APIKey     string
    HTTPClient *http.Client
}

type Recording struct {
    ID          string    `json:"id"`
    CallID      string    `json:"callId"`
    Participants []string  `json:"participants"`
    Quality     string    `json:"quality"`
    Format      string    `json:"format"`
    StartTime   time.Time `json:"startTime"`
    EndTime     time.Time `json:"endTime"`
    Size        int64     `json:"size"`
    URL         string    `json:"url"`
}

type RecordingRequest struct {
    CallID      string   `json:"callId"`
    Participants []string `json:"participants"`
    Quality     string   `json:"quality"`
    Format      string   `json:"format"`
}

type MediaConvertRequest struct {
    InputFile    string `json:"inputFile"`
    OutputFormat string `json:"outputFormat"`
    Quality      string `json:"quality"`
}

type StorageUsage struct {
    Total     int64  `json:"total"`
    Used      int64  `json:"used"`
    Available int64  `json:"available"`
    Percentage float64 `json:"percentage"`
}

func NewMPClient(baseURL, apiKey string) *MPClient {
    return &MPClient{
        BaseURL: baseURL,
        APIKey:  apiKey,
        HTTPClient: &http.Client{
            Timeout: 30 * time.Second,
        },
    }
}

func (c *MPClient) makeRequest(method, endpoint string, body interface{}) (*http.Response, error) {
    var reqBody io.Reader
    
    if body != nil {
        jsonBody, err := json.Marshal(body)
        if err != nil {
            return nil, fmt.Errorf("error marshaling request body: %v", err)
        }
        reqBody = bytes.NewBuffer(jsonBody)
    }
    
    req, err := http.NewRequest(method, c.BaseURL+"/mp/v2"+endpoint, reqBody)
    if err != nil {
        return nil, fmt.Errorf("error creating request: %v", err)
    }
    
    req.Header.Set("Content-Type", "application/json")
    req.Header.Set("Accept", "application/json")
    req.Header.Set("X-API-Key", c.APIKey)
    
    return c.HTTPClient.Do(req)
}

func (c *MPClient) StartRecording(req RecordingRequest) (*Recording, error) {
    resp, err := c.makeRequest("POST", "/recordings", req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    if resp.StatusCode != http.StatusCreated {
        return nil, fmt.Errorf("unexpected status code: %d", resp.StatusCode)
    }
    
    var recording Recording
    if err := json.NewDecoder(resp.Body).Decode(&recording); err != nil {
        return nil, fmt.Errorf("error decoding response: %v", err)
    }
    
    return &recording, nil
}

func (c *MPClient) GetRecording(recordingID string) (*Recording, error) {
    resp, err := c.makeRequest("GET", "/recordings/"+recordingID, nil)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    if resp.StatusCode != http.StatusOK {
        return nil, fmt.Errorf("unexpected status code: %d", resp.StatusCode)
    }
    
    var recording Recording
    if err := json.NewDecoder(resp.Body).Decode(&recording); err != nil {
        return nil, fmt.Errorf("error decoding response: %v", err)
    }
    
    return &recording, nil
}

func (c *MPClient) StopRecording(recordingID string) error {
    resp, err := c.makeRequest("POST", "/recordings/"+recordingID+"/stop", nil)
    if err != nil {
        return err
    }
    defer resp.Body.Close()
    
    if resp.StatusCode != http.StatusOK {
        return fmt.Errorf("unexpected status code: %d", resp.StatusCode)
    }
    
    return nil
}

func (c *MPClient) ConvertMedia(req MediaConvertRequest) error {
    resp, err := c.makeRequest("POST", "/media/convert", req)
    if err != nil {
        return err
    }
    defer resp.Body.Close()
    
    if resp.StatusCode != http.StatusOK {
        return fmt.Errorf("unexpected status code: %d", resp.StatusCode)
    }
    
    return nil
}

func (c *MPClient) GetStorageUsage() (*StorageUsage, error) {
    resp, err := c.makeRequest("GET", "/storage/usage", nil)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    if resp.StatusCode != http.StatusOK {
        return nil, fmt.Errorf("unexpected status code: %d", resp.StatusCode)
    }
    
    var usage StorageUsage
    if err := json.NewDecoder(resp.Body).Decode(&usage); err != nil {
        return nil, fmt.Errorf("error decoding response: %v", err)
    }
    
    return &usage, nil
}

func (c *MPClient) DownloadRecording(recordingID, filename string) error {
    resp, err := c.makeRequest("GET", "/recordings/"+recordingID+"/download", nil)
    if err != nil {
        return err
    }
    defer resp.Body.Close()
    
    if resp.StatusCode != http.StatusOK {
        return fmt.Errorf("unexpected status code: %d", resp.StatusCode)
    }
    
    file, err := os.Create(filename)
    if err != nil {
        return fmt.Errorf("error creating file: %v", err)
    }
    defer file.Close()
    
    _, err = io.Copy(file, resp.Body)
    if err != nil {
        return fmt.Errorf("error saving file: %v", err)
    }
    
    return nil
}

func main() {
    client := NewMPClient("https://mp-server.example.com", "your-api-key")
    
    // Start recording
    recordingReq := RecordingRequest{
        CallID:      "call123",
        Participants: []string{"user1", "user2"},
        Quality:     "high",
        Format:      "mp3",
    }
    
    recording, err := client.StartRecording(recordingReq)
    if err != nil {
        fmt.Printf("Error starting recording: %v\n", err)
        return
    }
    
    fmt.Printf("Recording started: %s\n", recording.ID)
    
    // Wait for some time (in real scenario, you'd wait for the call to end)
    time.Sleep(5 * time.Second)
    
    // Stop recording
    err = client.StopRecording(recording.ID)
    if err != nil {
        fmt.Printf("Error stopping recording: %v\n", err)
        return
    }
    
    fmt.Printf("Recording stopped: %s\n", recording.ID)
    
    // Get recording details
    recordingDetails, err := client.GetRecording(recording.ID)
    if err != nil {
        fmt.Printf("Error getting recording: %v\n", err)
        return
    }
    
    fmt.Printf("Recording details: %+v\n", recordingDetails)
    
    // Convert media
    convertReq := MediaConvertRequest{
        InputFile:    recording.ID + ".wav",
        OutputFormat: "mp3",
        Quality:      "high",
    }
    
    err = client.ConvertMedia(convertReq)
    if err != nil {
        fmt.Printf("Error converting media: %v\n", err)
        return
    }
    
    fmt.Println("Media conversion completed")
    
    // Get storage usage
    usage, err := client.GetStorageUsage()
    if err != nil {
        fmt.Printf("Error getting storage usage: %v\n", err)
        return
    }
    
    fmt.Printf("Storage usage: %.2f%% used\n", usage.Percentage)
    
    // Download recording
    err = client.DownloadRecording(recording.ID, "recording.mp3")
    if err != nil {
        fmt.Printf("Error downloading recording: %v\n", err)
        return
    }
    
    fmt.Println("Recording downloaded successfully")
}
```

### 7.6 שילוב עם Docker

הנה דוגמה להפעלת יישום MP עם Docker:

```dockerfile
# Dockerfile
FROM golang:1.19-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN go build -o mp_app main.go

FROM alpine:latest

RUN apk --no-cache add ca-certificates

WORKDIR /root/

COPY --from=builder /app/mp_app .

EXPOSE 8080

CMD ["./mp_app"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  mp-app:
    build: .
    ports:
      - "8080:8080"
    environment:
      - MP_URL=https://mp-server.example.com
      - MP_API_KEY=your-api-key
    volumes:
      - ./recordings:/app/recordings
      - ./logs:/app/logs

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"

volumes:
  recordings:
  logs:
```

---

## פרק 8: CMS - Cisco Meeting Server

### 8.1 מבוא ל-CMS

Cisco Meeting Server (CMS) הוא פלטפורמת ועידות וידאו מתקדמת המספקת שירותי ועידה באיכות גבוהה עבור ארגונים. CMS תומך במגוון רחב של מכשירים ופרוטוקולים, מה שהופך אותו לפתרון גמיש ונייד לצרכי ועידות.

**תכונות עיקריות**:

**וידאו באיכות גבוהה**:
- תמיכה ב-4K ו-HD
- קידוד מתקדם (H.264, H.265)
- אופטימיזציה אוטומטית של רוחב פס

**מגוון פרוטוקולים**:
- SIP ו-H.323
- WebRTC
- ממשקי API פתוחים

**גמישות והתאמה אישית**:
- פריסה מבוזרת
- תמיכה ב-clustering
- אינטגרציה עם מערכות קיימות

**אבטחה**:
- הצפנה מקצה לקצה
- אימות מתקדם
- ניהול הרשאות מפורט

### 8.2 ארכיטקטורה של CMS

**רכיבים עיקריים**:

**Call Bridge**:
- מרכז הניתוב של שיחות ועידה
- מטפל במיקסור וידאו ואודיו
- מנהל משאבי מערכת

**XMPP Server**:
- מנהל חיבורי משתמשים
- מספק שירותי נוכחות
- תומך בשיחות קבוצתיות

**Web Bridge**:
- תמיכה ב-WebRTC
- ממשק ווב למשתמשים
- שיתוף מסך ותוכן

**Database**:
- אחסון הגדרות ומידע
- תמיכה ב-replication
- גיבוי ושחזור

### 8.3 REST API ב-CMS

CMS מספק ממשק REST API מקיף המאפשר שליטה מלאה על פעולות ועידה, ניהול משתמשים, ואינטגרציה עם מערכות אחרות.

**קטגוריות API עיקריות**:

**Conference API**:
- יצירת ועידות
- ניהול משתתפים
- שליטה בהגדרות ועידה
- דוגמה:
```javascript
// Create conference
POST /cms/v2/conferences
{
  "title": "Team Meeting",
  "startTime": "2023-01-01T10:00:00Z",
  "duration": 60,
  "participants": ["user1@domain.com", "user2@domain.com"],
  "settings": {
    "videoQuality": "HD",
    "recordEnabled": true
  }
}

// Get conference details
GET /cms/v2/conferences/{conferenceId}

// Add participant
POST /cms/v2/conferences/{conferenceId}/participants
{
  "userId": "user3@domain.com",
  "role": "participant"
}
```

**User API**:
- ניהול משתמשים
- הגדרת הרשאות
- ניהול קבוצות
- דוגמה:
```javascript
// Get user details
GET /cms/v2/users/{userId}

// Create user
POST /cms/v2/users
{
  "username": "jdoe",
  "displayName": "John Doe",
  "email": "john@example.com",
  "role": "user"
}

// Update user permissions
PUT /cms/v2/users/{userId}/permissions
{
  "permissions": ["create_conference", "join_conference"]
}
```

**Recording API**:
- הקלטת ועידות
- ניהול הקלטות
- הפצת הקלטות
- דוגמה:
```javascript
// Start recording
POST /cms/v2/conferences/{conferenceId}/recordings
{
  "format": "mp4",
  "quality": "HD"
}

// Get recording list
GET /cms/v2/conferences/{conferenceId}/recordings

// Download recording
GET /cms/v2/recordings/{recordingId}/download
```

**Configuration API**:
- הגדרות מערכת
- ניהול משאבים
- מדיניות אבטחה
- דוגמה:
```javascript
// Get system configuration
GET /cms/v2/configuration

// Update conference settings
PUT /cms/v2/configuration/conferences
{
  "maxParticipants": 100,
  "defaultDuration": 60,
  "recordingEnabled": true
}
```

### 8.4 אימות ב-CMS API

CMS תומך במספר שיטות אימות:

**Basic Authentication**:
- שם משתמש וסיסמה
- פשוט ליישום
- מתאים לסביבות פיתוח

**OAuth 2.0**:
- תקן מודרני ומאובטח
- תומך ב-scopes ו-permissions
- מתאים לאפליקציות צד שלישי

**JWT Token**:
- טוקן מאובטח עם expiration
- תומך ב-refresh tokens
- מתאים לאפליקציות ווב

### 8.5 דוגמת יישום ב-Ruby

הנה דוגמה מלאה ליישום המתקשר עם CMS API:

```ruby
require 'net/http'
require 'uri'
require 'json'

class CMSClient
  def initialize(base_url, username, password)
    @base_url = base_url
    @username = username
    @password = password
    @uri = URI.parse(base_url)
  end
  
  private
  
  def make_request(method, endpoint, data = nil)
    http = Net::HTTP.new(@uri.host, @uri.port)
    http.use_ssl = @uri.scheme == 'https'
    
    request = case method
    when 'GET'
      Net::HTTP::Get.new("/cms/v2#{endpoint}")
    when 'POST'
      Net::HTTP::Post.new("/cms/v2#{endpoint}")
    when 'PUT'
      Net::HTTP::Put.new("/cms/v2#{endpoint}")
    when 'DELETE'
      Net::HTTP::Delete.new("/cms/v2#{endpoint}")
    end
    
    request.basic_auth(@username, @password)
    request['Content-Type'] = 'application/json'
    request['Accept'] = 'application/json'
    
    if data
      request.body = data.to_json
    end
    
    response = http.request(request)
    
    case response.code
    when '200', '201'
      JSON.parse(response.body)
    when '204'
      true
    else
      raise "HTTP Error: #{response.code} - #{response.body}"
    end
  end
  
  public
  
  def create_conference(title, start_time, duration, participants, settings = {})
    data = {
      title: title,
      startTime: start_time,
      duration: duration,
      participants: participants,
      settings: settings
    }
    
    make_request('POST', '/conferences', data)
  end
  
  def get_conference(conference_id)
    make_request('GET', "/conferences/#{conference_id}")
  end
  
  def add_participant(conference_id, user_id, role = 'participant')
    data = {
      userId: user_id,
      role: role
    }
    
    make_request('POST', "/conferences/#{conference_id}/participants", data)
  end
  
  def start_recording(conference_id, format = 'mp4', quality = 'HD')
    data = {
      format: format,
      quality: quality
    }
    
    make_request('POST', "/conferences/#{conference_id}/recordings", data)
  end
  
  def get_recordings(conference_id)
    make_request('GET', "/conferences/#{conference_id}/recordings")
  end
  
  def create_user(username, display_name, email, role = 'user')
    data = {
      username: username,
      displayName: display_name,
      email: email,
      role: role
    }
    
    make_request('POST', '/users', data)
  end
  
  def get_user(user_id)
    make_request('GET', "/users/#{user_id}")
  end
  
  def update_user_permissions(user_id, permissions)
    data = {
      permissions: permissions
    }
    
    make_request('PUT', "/users/#{user_id}/permissions", data)
  end
  
  def get_configuration
    make_request('GET', '/configuration')
  end
  
  def update_conference_settings(settings)
    make_request('PUT', '/configuration/conferences', settings)
  end
end

# Usage example
begin
  cms = CMSClient.new('https://cms-server.example.com', 'admin', 'password')
  
  # Create conference
  conference = cms.create_conference(
    'Team Meeting',
    '2023-01-01T10:00:00Z',
    60,
    ['user1@example.com', 'user2@example.com'],
    {
      videoQuality: 'HD',
      recordEnabled: true
    }
  )
  
  puts "Conference created: #{conference['id']}"
  
  # Add participant
  cms.add_participant(conference['id'], 'user3@example.com')
  puts "Participant added"
  
  # Start recording
  cms.start_recording(conference['id'])
  puts "Recording started"
  
  # Get recordings
  recordings = cms.get_recordings(conference['id'])
  puts "Recordings: #{recordings.length}"
  
  # Create user
  user = cms.create_user('jdoe', 'John Doe', 'john@example.com')
  puts "User created: #{user['id']}"
  
  # Update user permissions
  cms.update_user_permissions(user['id'], ['create_conference', 'join_conference'])
  puts "User permissions updated"
  
  # Get configuration
  config = cms.get_configuration
  puts "System configuration retrieved"
  
rescue => e
  puts "Error: #{e.message}"
end
```

### 8.6 שילוב עם Docker

הנה דוגמה להפעלת יישום CMS עם Docker:

```dockerfile
# Dockerfile
FROM ruby:3.0-alpine

WORKDIR /app

COPY Gemfile .
RUN bundle install

COPY . .

EXPOSE 4567

CMD ["ruby", "cms_app.rb"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  cms-app:
    build: .
    ports:
      - "4567:4567"
    environment:
      - CMS_URL=https://cms-server.example.com
      - CMS_USERNAME=admin
      - CMS_PASSWORD=password
    volumes:
      - ./logs:/app/logs
      - ./recordings:/app/recordings

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"

volumes:
  logs:
  recordings:
```

---

## פרק 9: TGW - Telephony Gateway

### 9.1 מבוא ל-TGW

Cisco Telephony Gateway (TGW) הוא שער טלפוניה מתקדם המאפשר חיבור בין מערכות טלפוניה מסורתיות למערכות IP מודרניות. TGW מספק גשר בין עולם הטלפוניה האנלוגי והדיגיטלי לבין עולם ה-IP.

**תכונות עיקריות**:

**המרת פרוטוקולים**:
- SIP ל-H.323
- אנלוגי ל-IP
- TDM ל-VoIP

**ניתוב חכם**:
- Least Cost Routing (LCR)
- ניתוב מבוסס איכות
- גיבוי ונפילה אוטומטית

**אבטחה**:
- חומת אש משולבת
- הצפנת שיחות
- אימות מתקדם

**ניהול ובקרה**:
- ממשק ניהול מבוסס ווב
- REST API מלא
- מעקב ודיווחים

### 9.2 ארכיטקטורה של TGW

**רכיבים עיקריים**:

**Protocol Translation Engine**:
- מנוע המרת פרוטוקולים
- מטפל בתרגום SIP/H.323
- מנהל codec conversion

**Routing Engine**:
- מנוע ניתוב שיחות
- מבצע LCR
- מנהל טבלאות ניתוב

**Security Module**:
- מודול אבטחה
- מנהל חומת אש
- מטפל בהצפנה

**Management Interface**:
- ממשק ניהול
- REST API
- SNMP ו-Telnet

### 9.3 REST API ב-TGW

TGW מספק ממשק REST API המאפשר שליטה מלאה על פעולות הגייטווי, ניהול ניתוב, ואינטגרציה עם מערכות ניהול.

**קטגוריות API עיקריות**:

**Gateway Configuration API**:
- הגדרות גייטווי
- ניהול פרוטוקולים
- הגדרות רשת
- דוגמה:
```javascript
// Get gateway configuration
GET /tgw/v2/gateway/configuration

// Update SIP settings
PUT /tgw/v2/gateway/sip
{
  "bindAddress": "192.168.1.100",
  "bindPort": 5060,
  "transport": "UDP",
  "realm": "example.com"
}

// Configure H.323
PUT /tgw/v2/gateway/h323
{
  "gatekeeper": "gk.example.com",
  "rasPort": 1719,
  "h245Port": 1720
}
```

**Routing API**:
- ניהול טבלאות ניתוב
- כללי ניתוב
- ניתוב מבוסס עלות
- דוגמה:
```javascript
// Get routing table
GET /tgw/v2/routing/table

// Add route
POST /tgw/v2/routing/rules
{
  "pattern": "9.@",
  "destination": "sip:provider.com",
  "priority": 1,
  "cost": 0.05
}

// Update LCR settings
PUT /tgw/v2/routing/lcr
{
  "enabled": true,
  "timeout": 5,
  "fallbackEnabled": true
}
```

**Call Control API**:
- ניהול שיחות פעילות
- מעקב שיחות
- ניתוב מחדש
- דוגמה:
```javascript
// Get active calls
GET /tgw/v2/calls/active

// Get call details
GET /tgw/v2/calls/{callId}

// Redirect call
POST /tgw/v2/calls/{callId}/redirect
{
  "destination": "sip:user@example.com"
}

// Terminate call
DELETE /tgw/v2/calls/{callId}
```

**Security API**:
- ניהול חומת אש
- כללי אבטחה
- אימות משתמשים
- דוגמה:
```javascript
// Get firewall rules
GET /tgw/v2/security/firewall/rules

// Add firewall rule
POST /tgw/v2/security/firewall/rules
{
  "action": "ALLOW",
  "source": "192.168.1.0/24",
  "destination": "ANY",
  "protocol": "SIP",
  "port": 5060
}

// Configure authentication
PUT /tgw/v2/security/authentication
{
  "method": "DIGEST",
  "realm": "example.com",
  "nonceTimeout": 300
}
```

### 9.4 אימות ב-TGW API

TGW תומך במספר שיטות אימות:

**Basic Authentication**:
- שם משתמש וסיסמה
- פשוט ליישום
- מומלץ לסביבות פנימיות

**API Key**:
- מפתח API ייחודי
- ניתן לניהול מרכזי
- מתאים לאינטגרציות

**Certificate-based**:
- אימות מבוסס אישורים
- אבטחה גבוהה
- מתאים לסביבות ארגוניות

### 9.5 דוגמת יישום ב-Python

הנה דוגמה מלאה ליישום המתקשר עם TGW API:

```python
import requests
import json
from datetime import datetime

class TGWClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-API-Key': self.api_key
        })
    
    def get_gateway_configuration(self):
        """Get current gateway configuration"""
        url = f"{self.base_url}/tgw/v2/gateway/configuration"
        response = self.session.get(url)
        return response.json()
    
    def update_sip_settings(self, settings):
        """Update SIP configuration"""
        url = f"{self.base_url}/tgw/v2/gateway/sip"
        response = self.session.put(url, json=settings)
        return response.json()
    
    def update_h323_settings(self, settings):
        """Update H.323 configuration"""
        url = f"{self.base_url}/tgw/v2/gateway/h323"
        response = self.session.put(url, json=settings)
        return response.json()
    
    def get_routing_table(self):
        """Get current routing table"""
        url = f"{self.base_url}/tgw/v2/routing/table"
        response = self.session.get(url)
        return response.json()
    
    def add_routing_rule(self, rule):
        """Add new routing rule"""
        url = f"{self.base_url}/tgw/v2/routing/rules"
        response = self.session.post(url, json=rule)
        return response.json()
    
    def update_lcr_settings(self, settings):
        """Update LCR configuration"""
        url = f"{self.base_url}/tgw/v2/routing/lcr"
        response = self.session.put(url, json=settings)
        return response.json()
    
    def get_active_calls(self):
        """Get list of active calls"""
        url = f"{self.base_url}/tgw/v2/calls/active"
        response = self.session.get(url)
        return response.json()
    
    def get_call_details(self, call_id):
        """Get detailed information about a specific call"""
        url = f"{self.base_url}/tgw/v2/calls/{call_id}"
        response = self.session.get(url)
        return response.json()
    
    def redirect_call(self, call_id, destination):
        """Redirect an active call"""
        url = f"{self.base_url}/tgw/v2/calls/{call_id}/redirect"
        data = {"destination": destination}
        response = self.session.post(url, json=data)
        return response.json()
    
    def terminate_call(self, call_id):
        """Terminate an active call"""
        url = f"{self.base_url}/tgw/v2/calls/{call_id}"
        response = self.session.delete(url)
        return response.json()
    
    def get_firewall_rules(self):
        """Get firewall rules"""
        url = f"{self.base_url}/tgw/v2/security/firewall/rules"
        response = self.session.get(url)
        return response.json()
    
    def add_firewall_rule(self, rule):
        """Add new firewall rule"""
        url = f"{self.base_url}/tgw/v2/security/firewall/rules"
        response = self.session.post(url, json=rule)
        return response.json()
    
    def update_authentication(self, settings):
        """Update authentication settings"""
        url = f"{self.base_url}/tgw/v2/security/authentication"
        response = self.session.put(url, json=settings)
        return response.json()

# Usage example
tgw = TGWClient("https://tgw-server.example.com", "your-api-key")

# Get current configuration
config = tgw.get_gateway_configuration()
print(f"Gateway configuration: {config}")

# Update SIP settings
sip_settings = {
    "bindAddress": "192.168.1.100",
    "bindPort": 5060,
    "transport": "UDP",
    "realm": "example.com"
}
tgw.update_sip_settings(sip_settings)

# Add routing rule
routing_rule = {
    "pattern": "9.@",
    "destination": "sip:provider.com",
    "priority": 1,
    "cost": 0.05
}
tgw.add_routing_rule(routing_rule)

# Get active calls
active_calls = tgw.get_active_calls()
print(f"Active calls: {len(active_calls)}")

# Redirect specific call
if active_calls:
    call_id = active_calls[0]["id"]
    tgw.redirect_call(call_id, "sip:user@example.com")
    print(f"Call {call_id} redirected")

# Add firewall rule
firewall_rule = {
    "action": "ALLOW",
    "source": "192.168.1.0/24",
    "destination": "ANY",
    "protocol": "SIP",
    "port": 5060
}
tgw.add_firewall_rule(firewall_rule)
```

### 9.6 שילוב עם Docker

הנה דוגמה להפעלת יישום TGW עם Docker:

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "tgw_app.py"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  tgw-app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - TGW_URL=https://tgw-server.example.com
      - TGW_API_KEY=your-api-key
    volumes:
      - ./logs:/app/logs
      - ./config:/app/config

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"

volumes:
  logs:
  config:
```

---

## פרק 10: SBC - Session Border Controller

### 10.1 מבוא ל-SBC

Cisco Session Border Controller (SBC) הוא מכשיר רשת מתקדם המשמש כנקודת גבול בין רשתות IP שונות. SBC מספק אבטחה, ניתוב, ושליטה על תעבורת קול ווידאו על פני גבולות רשת.

**תכונות עיקריות**:

**אבטחה**:
- חומת אש מתקדמת
- הגנה מפני התקפות DoS
- הצפנה מקצה לקצה
- סינון תעבורה זדונית

**ניתוב ושליטה**:
- Policy-based routing
- Quality of Service (QoS)
- Load balancing
- Traffic shaping

**אינטרופרביליות**:
- תמיכה בפרוטוקולים מרובים
- המרת codecs
- NAT traversal
- Protocol translation

**ניהול ובקרה**:
- ממשק ניהול מתקדם
- REST API מלא
- מעקב ודיווחים מפורטים

### 10.2 ארכיטקטורה של SBC

**רכיבים עיקריים**:

**Signaling Plane**:
- מטפל ב-SIP signaling
- מבצע protocol translation
- מנהל session establishment

**Media Plane**:
- מטפל ב-media streams
- מבצע codec conversion
- מנהל QoS

**Security Engine**:
- מנוע אבטחה
- מסנן תעבורה
- מזהה איומים

**Policy Engine**:
- מנוע כללים
- מיישם מדיניות
- מנהל הרשאות

### 10.3 REST API ב-SBC

SBC מספק ממשק REST API מקיף המאפשר ניהול מלא של כללי אבטחה, פרופילים, ומדיניות ניתוב.

**קטגוריות API עיקריות**:

**Configuration API**:
- הגדרות מערכת
- ניהול פרופילים
- הגדרות רשת
- דוגמה:
```javascript
// Get system configuration
GET /sbc/v2/configuration

// Create SIP profile
POST /sbc/v2/profiles/sip
{
  "name": "Provider_SIP",
  "description": "SIP profile for external provider",
  "transport": "UDP",
  "port": 5060,
  "timeout": 30
}

// Update network settings
PUT /sbc/v2/configuration/network
{
  "interface": "eth0",
  "ipAddress": "192.168.1.100",
  "netmask": "255.255.255.0",
  "gateway": "192.168.1.1"
}
```

**Security API**:
- כללי חומת אש
- מדיניות אבטחה
- אימות והרשאות
- דוגמה:
```javascript
// Get security policies
GET /sbc/v2/security/policies

// Add firewall rule
POST /sbc/v2/security/firewall/rules
{
  "name": "Allow_Internal_SIP",
  "action": "ALLOW",
  "source": "192.168.1.0/24",
  "destination": "ANY",
  "protocol": "SIP",
  "port": 5060
}

// Configure authentication
PUT /sbc/v2/security/authentication
{
  "method": "DIGEST",
  "realm": "sbc.example.com",
  "nonceTimeout": 300
}
```

**Routing API**:
- כללי ניתוב
- policy-based routing
- load balancing
- דוגמה:
```javascript
// Get routing rules
GET /sbc/v2/routing/rules

// Add routing policy
POST /sbc/v2/routing/policies
{
  "name": "External_Calls",
  "priority": 100,
  "conditions": [
    {
      "field": "destination",
      "operator": "matches",
      "value": "9.@"
    }
  ],
  "actions": [
    {
      "type": "route",
      "destination": "sip:provider.com"
    }
  ]
}

// Configure load balancing
PUT /sbc/v2/routing/loadbalancing
{
  "algorithm": "round_robin",
  "healthCheck": true,
  "interval": 30
}
```

**Monitoring API**:
- מעקב ביצועים
- סטטיסטיקות
- logs ו-events
- דוגמה:
```javascript
// Get system status
GET /sbc/v2/monitoring/status

// Get performance metrics
GET /sbc/v2/monitoring/metrics

// Get call statistics
GET /sbc/v2/monitoring/calls/statistics

// Get logs
GET /sbc/v2/monitoring/logs?level=ERROR&limit=100
```

### 10.4 אימות ב-SBC API

SBC תומך במספר שיטות אימות:

**Certificate-based**:
- אימות מבוסס אישורים
- אבטחה גבוהה
- מתאים לסביבות ארגוניות

**API Key**:
- מפתח API ייחודי
- ניתן לניהול מרכזי
- מתאים לאינטגרציות

**OAuth 2.0**:
- תקן מודרני לאימות
- תומך ב-scopes ו-permissions
- מתאים לאפליקציות צד שלישי

### 10.5 דוגמת יישום ב-Java

הנה דוגמה מלאה ליישום המתקשר עם SBC API:

```java
import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.List;
import java.util.Map;
import com.fasterxml.jackson.databind.ObjectMapper;

public class SBCClient {
    private final String baseUrl;
    private final String apiKey;
    private final HttpClient httpClient;
    private final ObjectMapper objectMapper;
    
    public SBCClient(String baseUrl, String apiKey) {
        this.baseUrl = baseUrl;
        this.apiKey = apiKey;
        this.httpClient = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(30))
            .build();
        this.objectMapper = new ObjectMapper();
    }
    
    private HttpRequest.Builder createRequest(String method, String endpoint) {
        return HttpRequest.newBuilder()
            .uri(URI.create(baseUrl + "/sbc/v2" + endpoint))
            .header("Content-Type", "application/json")
            .header("Accept", "application/json")
            .header("X-API-Key", apiKey)
            .timeout(Duration.ofSeconds(30));
    }
    
    public Map<String, Object> getSystemConfiguration() throws IOException, InterruptedException {
        HttpRequest request = createRequest("GET", "/configuration").build();
        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
        
        if (response.statusCode() == 200) {
            return objectMapper.readValue(response.body(), Map.class);
        } else {
            throw new RuntimeException("HTTP Error: " + response.statusCode());
        }
    }
    
    public Map<String, Object> createSipProfile(Map<String, Object> profile) 
            throws IOException, InterruptedException {
        HttpRequest request = createRequest("POST", "/profiles/sip")
            .POST(HttpRequest.BodyPublishers.ofString(objectMapper.writeValueAsString(profile)))
            .build();
        
        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
        
        if (response.statusCode() == 201) {
            return objectMapper.readValue(response.body(), Map.class);
        } else {
            throw new RuntimeException("HTTP Error: " + response.statusCode());
        }
    }
    
    public void updateNetworkSettings(Map<String, Object> settings) 
            throws IOException, InterruptedException {
        HttpRequest request = createRequest("PUT", "/configuration/network")
            .PUT(HttpRequest.BodyPublishers.ofString(objectMapper.writeValueAsString(settings)))
            .build();
        
        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
        
        if (response.statusCode() != 200) {
            throw new RuntimeException("HTTP Error: " + response.statusCode());
        }
    }
    
    public List<Map<String, Object>> getSecurityPolicies() 
            throws IOException, InterruptedException {
        HttpRequest request = createRequest("GET", "/security/policies").build();
        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
        
        if (response.statusCode() == 200) {
            return objectMapper.readValue(response.body(), List.class);
        } else {
            throw new RuntimeException("HTTP Error: " + response.statusCode());
        }
    }
    
    public Map<String, Object> addFirewallRule(Map<String, Object> rule) 
            throws IOException, InterruptedException {
        HttpRequest request = createRequest("POST", "/security/firewall/rules")
            .POST(HttpRequest.BodyPublishers.ofString(objectMapper.writeValueAsString(rule)))
            .build();
        
        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
        
        if (response.statusCode() == 201) {
            return objectMapper.readValue(response.body(), Map.class);
        } else {
            throw new RuntimeException("HTTP Error: " + response.statusCode());
        }
    }
    
    public List<Map<String, Object>> getRoutingRules() 
            throws IOException, InterruptedException {
        HttpRequest request = createRequest("GET", "/routing/rules").build();
        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
        
        if (response.statusCode() == 200) {
            return objectMapper.readValue(response.body(), List.class);
        } else {
            throw new RuntimeException("HTTP Error: " + response.statusCode());
        }
    }
    
    public Map<String, Object> addRoutingPolicy(Map<String, Object> policy) 
            throws IOException, InterruptedException {
        HttpRequest request = createRequest("POST", "/routing/policies")
            .POST(HttpRequest.BodyPublishers.ofString(objectMapper.writeValueAsString(policy)))
            .build();
        
        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
        
        if (response.statusCode() == 201) {
            return objectMapper.readValue(response.body(), Map.class);
        } else {
            throw new RuntimeException("HTTP Error: " + response.statusCode());
        }
    }
    
    public Map<String, Object> getSystemStatus() 
            throws IOException, InterruptedException {
        HttpRequest request = createRequest("GET", "/monitoring/status").build();
        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
        
        if (response.statusCode() == 200) {
            return objectMapper.readValue(response.body(), Map.class);
        } else {
            throw new RuntimeException("HTTP Error: " + response.statusCode());
        }
    }
    
    public Map<String, Object> getPerformanceMetrics() 
            throws IOException, InterruptedException {
        HttpRequest request = createRequest("GET", "/monitoring/metrics").build();
        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
        
        if (response.statusCode() == 200) {
            return objectMapper.readValue(response.body(), Map.class);
        } else {
            throw new RuntimeException("HTTP Error: " + response.statusCode());
        }
    }
    
    public static void main(String[] args) {
        SBCClient sbc = new SBCClient("https://sbc-server.example.com", "your-api-key");
        
        try {
            // Get system configuration
            Map<String, Object> config = sbc.getSystemConfiguration();
            System.out.println("System configuration: " + config);
            
            // Create SIP profile
            Map<String, Object> sipProfile = Map.of(
                "name", "Provider_SIP",
                "description", "SIP profile for external provider",
                "transport", "UDP",
                "port", 5060,
                "timeout", 30
            );
            
            Map<String, Object> createdProfile = sbc.createSipProfile(sipProfile);
            System.out.println("Created SIP profile: " + createdProfile);
            
            // Add firewall rule
            Map<String, Object> firewallRule = Map.of(
                "name", "Allow_Internal_SIP",
                "action", "ALLOW",
                "source", "192.168.1.0/24",
                "destination", "ANY",
                "protocol", "SIP",
                "port", 5060
            );
            
            Map<String, Object> createdRule = sbc.addFirewallRule(firewallRule);
            System.out.println("Created firewall rule: " + createdRule);
            
            // Get routing rules
            List<Map<String, Object>> routingRules = sbc.getRoutingRules();
            System.out.println("Routing rules count: " + routingRules.size());
            
            // Get system status
            Map<String, Object> status = sbc.getSystemStatus();
            System.out.println("System status: " + status);
            
            // Get performance metrics
            Map<String, Object> metrics = sbc.getPerformanceMetrics();
            System.out.println("Performance metrics: " + metrics);
            
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
        }
    }
}
```

### 10.6 שילוב עם Docker

הנה דוגמה להפעלת יישום SBC עם Docker:

```dockerfile
# Dockerfile
FROM openjdk:17-jdk-slim

WORKDIR /app

COPY target/sbc-app.jar .

EXPOSE 8080

CMD ["java", "-jar", "sbc-app.jar"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  sbc-app:
    build: .
    ports:
      - "8080:8080"
    environment:
      - SBC_URL=https://sbc-server.example.com
      - SBC_API_KEY=your-api-key
    volumes:
      - ./logs:/app/logs
      - ./config:/app/config

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"

volumes:
  logs:
  config:
```

---

## פרק 11: Expressway

### 11.1 מבוא ל-Expressway

Cisco Expressway הוא פתרון מתקדם לחיבור ועידות וידאו ותקשורת מחוץ לרשת הארגונית. Expressway מאפשר גישה מאובטחת למשאבי תקשורת מכל מקום בעולם, תוך שמירה על אבטחה ואיכות.

**תכונות עיקריות**:

**גישה מרחוק**:
- חיבור משתמשים מרחוק
- Mobile and remote access
- B2B connectivity

**אבטחה**:
- חומת אש מתקדמת
- VPN-less access
- הצפנה מאובטחת

**אינטרופרביליות**:
- תמיכה במגוון פרוטוקולים
- חיבור למערכות צד שלישי
- Federation capabilities

**ניהול מרכזי**:
- ממשק ניהול מתקדם
- REST API מלא
- מעקב ודיווחים

### 11.2 ארכיטקטורה של Expressway

**רכיבים עיקריים**:

**Expressway-E (Edge)**:
- רכיב חיצוני
- מחבר לאינטרנט
- מטפל בחיבורי משתמשים

**Expressway-C (Core)**:
- רכיב פנימי
- מחבר לרשת הארגונית
- מתקשר עם מערכות פנימיות

**Traversal Client**:
- לקוח NAT traversal
- מטפל בחיבורים דרך NAT
- תומך ב-ICE ו-STUN

**Federation Services**:
- שירותי federation
- חיבור לארגונים אחרים
- שיתוף משאבים

### 11.3 REST API ב-Expressway

Expressway מספק ממשק REST API המאפשר ניהול מלא של חיבורים, משתמשים, ושירותי federation.

**קטגוריות API עיקריות**:

**Configuration API**:
- הגדרות מערכת
- ניהול רשת
- הגדרות אבטחה
- דוגמה:
```javascript
// Get system configuration
GET /expressway/v2/configuration

// Update network settings
PUT /expressway/v2/configuration/network
{
  "interface": "eth0",
  "ipAddress": "192.168.1.100",
  "netmask": "255.255.255.0",
  "gateway": "192.168.1.1",
  "dns": ["8.8.8.8", "8.8.4.4"]
}

// Configure security
PUT /expressway/v2/configuration/security
{
  "firewallEnabled": true,
  "encryptionLevel": "HIGH",
  "authenticationMethod": "DIGEST"
}
```

**User Management API**:
- ניהול משתמשים
- הרשאות וגישה
- קבוצות משתמשים
- דוגמה:
```javascript
// Get users
GET /expressway/v2/users

// Create user
POST /expressway/v2/users
{
  "username": "jdoe",
  "displayName": "John Doe",
  "email": "john@example.com",
  "password": "securePassword",
  "role": "user"
}

// Update user permissions
PUT /expressway/v2/users/{userId}/permissions
{
  "permissions": ["remote_access", "video_conference"]
}
```

**Federation API**:
- ניהול federation
- חיבור לארגונים חיצוניים
- שיתוף משאבים
- דוגמה:
```javascript
// Get federation domains
GET /expressway/v2/federation/domains

// Add federation domain
POST /expressway/v2/federation/domains
{
  "domain": "partner.example.com",
  "description": "Partner organization",
  "enabled": true,
  "authentication": "TLS"
}

// Configure federation settings
PUT /expressway/v2/federation/settings
{
  "allowIncoming": true,
  "allowOutgoing": true,
  "requireAuthentication": true
}
```

**Monitoring API**:
- מעקב חיבורים
- סטטיסטיקות
- logs ו-events
- דוגמה:
```javascript
// Get active connections
GET /expressway/v2/connections/active

// Get connection statistics
GET /expressway/v2/connections/statistics

// Get system logs
GET /expressway/v2/logs?level=INFO&limit=100

// Get performance metrics
GET /expressway/v2/monitoring/metrics
```

### 11.4 אימות ב-Expressway API

Expressway תומך במספר שיטות אימות:

**Basic Authentication**:
- שם משתמש וסיסמה
- פשוט ליישום
- מתאים לסביבות פיתוח

**OAuth 2.0**:
- תקן מודרני לאימות
- תומך ב-scopes ו-permissions
- מתאים לאפליקציות צד שלישי

**Certificate-based**:
- אימות מבוסס אישורים
- אבטחה גבוהה
- מתאים לסביבות ארגוניות

### 11.5 דוגמת יישום ב-C#

הנה דוגמה מלאה ליישום המתקשר עם Expressway API:

```csharp
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

public class ExpresswayClient
{
    private readonly HttpClient _httpClient;
    private readonly string _baseUrl;
    private readonly string _apiKey;
    
    public ExpresswayClient(string baseUrl, string apiKey)
    {
        _baseUrl = baseUrl;
        _apiKey = apiKey;
        _httpClient = new HttpClient();
        _httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
        _httpClient.DefaultRequestHeaders.Add("X-API-Key", apiKey);
    }
    
    private async Task<T> MakeRequestAsync<T>(HttpMethod method, string endpoint, object data = null)
    {
        var request = new HttpRequestMessage(method, $"{_baseUrl}/expressway/v2{endpoint}");
        
        if (data != null)
        {
            var json = JsonSerializer.Serialize(data);
            request.Content = new StringContent(json, Encoding.UTF8, "application/json");
        }
        
        var response = await _httpClient.SendAsync(request);
        
        if (!response.IsSuccessStatusCode)
        {
            throw new Exception($"HTTP Error: {response.StatusCode} - {await response.Content.ReadAsStringAsync()}");
        }
        
        var responseContent = await response.Content.ReadAsStringAsync();
        return JsonSerializer.Deserialize<T>(responseContent);
    }
    
    public async Task<Dictionary<string, object>> GetSystemConfiguration()
    {
        return await MakeRequestAsync<Dictionary<string, object>>(HttpMethod.Get, "/configuration");
    }
    
    public async Task UpdateNetworkSettings(Dictionary<string, object> settings)
    {
        await MakeRequestAsync<object>(HttpMethod.Put, "/configuration/network", settings);
    }
    
    public async Task UpdateSecuritySettings(Dictionary<string, object> settings)
    {
        await MakeRequestAsync<object>(HttpMethod.Put, "/configuration/security", settings);
    }
    
    public async Task<List<Dictionary<string, object>>> GetUsers()
    {
        return await MakeRequestAsync<List<Dictionary<string, object>>>(HttpMethod.Get, "/users");
    }
    
    public async Task<Dictionary<string, object>> CreateUser(Dictionary<string, object> user)
    {
        return await MakeRequestAsync<Dictionary<string, object>>(HttpMethod.Post, "/users", user);
    }
    
    public async Task UpdateUserPermissions(string userId, List<string> permissions)
    {
        var data = new { permissions = permissions };
        await MakeRequestAsync<object>(HttpMethod.Put, $"/users/{userId}/permissions", data);
    }
    
    public async Task<List<Dictionary<string, object>>> GetFederationDomains()
    {
        return await MakeRequestAsync<List<Dictionary<string, object>>>(HttpMethod.Get, "/federation/domains");
    }
    
    public async Task<Dictionary<string, object>> AddFederationDomain(Dictionary<string, object> domain)
    {
        return await MakeRequestAsync<Dictionary<string, object>>(HttpMethod.Post, "/federation/domains", domain);
    }
    
    public async Task UpdateFederationSettings(Dictionary<string, object> settings)
    {
        await MakeRequestAsync<object>(HttpMethod.Put, "/federation/settings", settings);
    }
    
    public async Task<List<Dictionary<string, object>>> GetActiveConnections()
    {
        return await MakeRequestAsync<List<Dictionary<string, object>>>(HttpMethod.Get, "/connections/active");
    }
    
    public async Task<Dictionary<string, object>> GetConnectionStatistics()
    {
        return await MakeRequestAsync<Dictionary<string, object>>(HttpMethod.Get, "/connections/statistics");
    }
    
    public async Task<Dictionary<string, object>> GetPerformanceMetrics()
    {
        return await MakeRequestAsync<Dictionary<string, object>>(HttpMethod.Get, "/monitoring/metrics");
    }
    
    public static async Task Main(string[] args)
    {
        var client = new ExpresswayClient("https://expressway-server.example.com", "your-api-key");
        
        try
        {
            // Get system configuration
            var config = await client.GetSystemConfiguration();
            Console.WriteLine("System configuration retrieved");
            
            // Update network settings
            var networkSettings = new Dictionary<string, object>
            {
                { "interface", "eth0" },
                { "ipAddress", "192.168.1.100" },
                { "netmask", "255.255.255.0" },
                { "gateway", "192.168.1.1" },
                { "dns", new List<string> { "8.8.8.8", "8.8.4.4" } }
            };
            
            await client.UpdateNetworkSettings(networkSettings);
            Console.WriteLine("Network settings updated");
            
            // Create user
            var user = new Dictionary<string, object>
            {
                { "username", "jdoe" },
                { "displayName", "John Doe" },
                { "email", "john@example.com" },
                { "password", "securePassword" },
                { "role", "user" }
            };
            
            var createdUser = await client.CreateUser(user);
            Console.WriteLine($"User created: {createdUser["id"]}");
            
            // Update user permissions
            await client.UpdateUserPermissions(createdUser["id"].ToString(), new List<string> { "remote_access", "video_conference" });
            Console.WriteLine("User permissions updated");
            
            // Add federation domain
            var federationDomain = new Dictionary<string, object>
            {
                { "domain", "partner.example.com" },
                { "description", "Partner organization" },
                { "enabled", true },
                { "authentication", "TLS" }
            };
            
            var createdDomain = await client.AddFederationDomain(federationDomain);
            Console.WriteLine($"Federation domain added: {createdDomain["id"]}");
            
            // Get active connections
            var connections = await client.GetActiveConnections();
            Console.WriteLine($"Active connections: {connections.Count}");
            
            // Get performance metrics
            var metrics = await client.GetPerformanceMetrics();
            Console.WriteLine("Performance metrics retrieved");
            
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error: {ex.Message}");
        }
    }
}
```

### 11.6 שילוב עם Docker

הנה דוגמה להפעלת יישום Expressway עם Docker:

```dockerfile
# Dockerfile
FROM mcr.microsoft.com/dotnet/runtime:6.0 AS base
WORKDIR /app

FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
WORKDIR /src
COPY ["ExpresswayApp.csproj", "./"]
RUN dotnet restore "./ExpresswayApp.csproj"
COPY . .
WORKDIR "/src/."
RUN dotnet build "ExpresswayApp.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "ExpresswayApp.csproj" -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "ExpresswayApp.dll"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  expressway-app:
    build: .
    ports:
      - "8080:8080"
    environment:
      - EXPRESSWAY_URL=https://expressway-server.example.com
      - EXPRESSWAY_API_KEY=your-api-key
    volumes:
      - ./logs:/app/logs
      - ./config:/app/config

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"

volumes:
  logs:
  config:
```

---

*המדריך ימשיך בחלק 3 עם סקירה מפורטת של פיתוח REST API מתקדם, דוגמאות קוד נוספות, ושילוב מלא עם Docker.*
