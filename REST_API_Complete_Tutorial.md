# מדריך REST API מקיף - מהתחלה עד הסוף

## תוכן עניינים

1. [מבוא ל-REST API](#מבוא-ל-rest-api)
2. [יסודות HTTP](#יסודות-http)
3. [מתודות HTTP](#מתודות-http)
4. [סטטוס קודים](#סטטוס-קודים)
5. [עיצוב API](#עיצוב-api)
6. [אימות והרשאות](#אימות-והרשאות)
7. [Versioning](#versioning)
8. [Pagination ו-Filtration](#pagination--filtration)
9. [Error Handling](#error-handling)
10. [Security](#security)
11. [Testing](#testing)
12. [Documentation](#documentation)
13. [Best Practices](#best-practices)
14. [Tools ו-Frameworks](#tools--frameworks)
15. [פרויקט מעשי](#פרויקט-מעשי)

---

## מבוא ל-REST API

### מה זה REST API?

REST (Representational State Transfer) הוא סגנון ארכיטקטוני לעיצוב מערכות מבוזרות. REST API הוא ממשק תכנות יישומים שעוקב אחר עקרונות REST ומאפשר תקשורת בין מערכות שונות דרך רשת האינטרנט.

### עקרונות REST

**1. Client-Server Architecture**
- הפרדה בין הלקוח לשרת
- הלקוח אחראי על ממשק המשתמש
- השרת אחראי על עיבוד נתונים ולוגיקה עסקית

**2. Stateless**
- כל בקשה מהלקוח צריכה להכיל את כל המידע הנדרש לעיבודה
- השרת לא שומר מצב של הלקוח בין בקשות
- זה מאפשר סקלביליות גבוהה

**3. Cacheable**
- תגובות מהשרת צריכות להגדיר אם הן ניתנות למטמון
- משפר ביצועים ומפחית עומס על השרת

**4. Uniform Interface**
- שימוש במתודות HTTP סטנדרטיות
- משאבים מזוהים על ידי URI
- שימוש ב-representations (JSON, XML)

**5. Layered System**
- הארכיטקטורה יכולה לכלול שכבות ביניים
- הלקוח לא יודע אם הוא מתקשר ישירות לשרת או דרך מתווך

**6. Code on Demand (אופציונלי)**
- השרת יכול לשלוח קוד שמתבצע בצד הלקוח

### למה REST API?

- **סטנדרטיזציה**: פרוטוקול HTTP סטנדרטי שכולם מכירים
- **סקלביליות**: ארכיטקטורה stateless מאפשרת הרחבה קלה
- **גמישות**: עובד עם כל טכנולוגיה שתומכת ב-HTTP
- **פשטות**: קל ללמוד וליישם
- **תמיכה**: תמיכה רחבה בכלים וספריות

---

## יסודות HTTP

### HTTP Protocol

HTTP (Hypertext Transfer Protocol) הוא פרוטוקול תקשורת שמשמש את האינטרנט. REST API משתמש ב-HTTP כבסיס לתקשורת.

### מבנה בקשת HTTP

```
GET /api/users/123 HTTP/1.1
Host: example.com
Authorization: Bearer token123
Content-Type: application/json
Accept: application/json

{
  "name": "John Doe"
}
```

**רכיבי בקשה:**
- **Method**: סוג הפעולה (GET, POST, PUT, DELETE)
- **URI**: כתובת המשאב
- **Headers**: מידע נוסף על הבקשה
- **Body**: נתונים שנשלחים לשרת (במקרים מסוימים)

### מבנה תגובת HTTP

```
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 123
Date: Mon, 23 Mar 2026 23:00:00 GMT

{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com"
}
```

**רכיבי תגובה:**
- **Status Line**: גרסת פרוטוקול + סטטוס קוד + הודעה
- **Headers**: מידע על התגובה
- **Body**: נתונים שחוזרים מהשרת

### Headers חשובים

**Request Headers:**
- `Content-Type`: סוג התוכן ב-body
- `Accept`: סוגי תוכן שהלקוח מקבל
- `Authorization`: מידע אימות
- `User-Agent`: מידע על הלקוח
- `X-API-Key`: מפתח API

**Response Headers:**
- `Content-Type`: סוג התוכן בתגובה
- `Content-Length`: גודל התוכן
- `Cache-Control`: הוראות מטמון
- `ETag`: גרסת המשאב
- `Last-Modified`: תאריך שינוי אחרון

---

## מתודות HTTP

### GET - קבלת מידע

משמש לקבלת מידע מהשרת. בטוח לשימוש חוזר (idempotent).

```http
GET /api/users
GET /api/users/123
GET /api/products?category=electronics&sort=price
```

**דוגמאות:**
```javascript
// קבלת כל המשתמשים
fetch('/api/users')
  .then(response => response.json())
  .then(users => console.log(users));

// קבלת משתמש ספציפי
fetch('/api/users/123')
  .then(response => response.json())
  .then(user => console.log(user));
```

### POST - יצירת משאב חדש

משמש ליצירת משאב חדש. לא בטוח לשימוש חוזר.

```http
POST /api/users
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "age": 30
}
```

**דוגמה:**
```javascript
fetch('/api/users', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'John Doe',
    email: 'john@example.com',
    age: 30
  })
})
.then(response => response.json())
.then(user => console.log(user));
```

### PUT - עדכון משאב שלם

משמש לעדכון משאב קיים או יצירת משאב חדש אם לא קיים. בטוח לשימוש חוזר.

```http
PUT /api/users/123
Content-Type: application/json

{
  "name": "John Updated",
  "email": "john.updated@example.com",
  "age": 31
}
```

### PATCH - עדכון חלקי של משאב

משמש לעדכון חלקי של משאב קיים. בטוח לשימוש חוזר.

```http
PATCH /api/users/123
Content-Type: application/json

{
  "age": 32
}
```

### DELETE - מחיקת משאב

משמש למחיקת משאב. בטוח לשימוש חוזר.

```http
DELETE /api/users/123
```

### OPTIONS - בדיקת אפשרויות

משמש לבדיקת המתודות הנתמכות עבור משאב.

```http
OPTIONS /api/users

HTTP/1.1 200 OK
Allow: GET, POST, PUT, PATCH, DELETE, OPTIONS
```

### HEAD - קבלת headers בלבד

משמש לקבלת headers בלי את ה-body.

```http
HEAD /api/users/123
```

---

## סטטוס קודים

### סטטוס קודים מרכזיים

**1xx - Informational**
- `100 Continue`: השרת קיבל את חלק הבקשה וממתין להמשך

**2xx - Success**
- `200 OK`: הבקשה הצליחה
- `201 Created`: משאב נוצר בהצלחה
- `202 Accepted`: הבקשה התקבלה לעיבוד
- `204 No Content`: הבקשה הצליחה אין תוכן להחזיר

**3xx - Redirection**
- `301 Moved Permanently`: משאב הועבר לנצח
- `302 Found`: משאב הועבר זמנית
- `304 Not Modified`: משאב לא השתנה מאז הבקשה האחרונה

**4xx - Client Error**
- `400 Bad Request`: בקשה לא תקינה
- `401 Unauthorized`: נדרש אימות
- `403 Forbidden`: אין הרשאה
- `404 Not Found`: משאב לא נמצא
- `405 Method Not Allowed`: מתודה לא נתמכת
- `409 Conflict`: קונפליקט בנתונים
- `422 Unprocessable Entity`: בקשה תקינה אך לא ניתן לעבד
- `429 Too Many Requests`: יותר מדי בקשות

**5xx - Server Error**
- `500 Internal Server Error`: שגיאת שרת כללית
- `501 Not Implemented`: פונקציונליות לא מיושמת
- `502 Bad Gateway`: שרת שער לא תקין
- `503 Service Unavailable`: שירות לא זמין
- `504 Gateway Timeout`: תם הזמן המוקצב לשער

### שימוש נכון בסטטוס קודים

```javascript
// GET - קבלת משאב
app.get('/users/:id', (req, res) => {
  const user = findUserById(req.params.id);
  if (user) {
    res.status(200).json(user);
  } else {
    res.status(404).json({ error: 'User not found' });
  }
});

// POST - יצירת משאב
app.post('/users', (req, res) => {
  const user = createUser(req.body);
  res.status(201).json(user);
});

// PUT - עדכון משאב
app.put('/users/:id', (req, res) => {
  const user = updateUser(req.params.id, req.body);
  if (user) {
    res.status(200).json(user);
  } else {
    res.status(404).json({ error: 'User not found' });
  }
});

// DELETE - מחיקת משאב
app.delete('/users/:id', (req, res) => {
  const deleted = deleteUser(req.params.id);
  if (deleted) {
    res.status(204).send();
  } else {
    res.status(404).json({ error: 'User not found' });
  }
});
```

---

## עיצוב API

### עקרונות עיצוב

**1. Resource Naming**
- השתמש בשמות משאבים ברורים
- השתמש בריבוי (plural nouns)
- הימנע מפעלים (verbs)

```http
// טוב
GET /api/users
GET /api/products
GET /api/orders

// רע
GET /api/getUsers
GET /api/listProducts
GET /api/retrieveOrders
```

**2. URI Structure**
- השתמש בהיררכיה לוגית
- הפרד משאבים באמצעות `/`
- השתמש ב-query parameters לפילטור ומיון

```http
// טוב
GET /api/users/123/orders
GET /api/products?category=electronics&sort=price
GET /api/orders?status=pending&date_from=2023-01-01

// רע
GET /api/getUserOrders/123
GET /api/products/electronics/sort/price
```

**3. HTTP Methods**
- השתמש במתודות נכונות לפי הפעולה
- GET לקבלת מידע
- POST ליצירה
- PUT/PATCH לעדכון
- DELETE למחיקה

**4. Versioning**
- השתמש ב-versioning לשמירה על תאימות לאחור
- הכנס גרסה ב-URI או ב-header

```http
// URI versioning
GET /api/v1/users
GET /api/v2/users

// Header versioning
GET /api/users
Accept: application/vnd.api+json;version=1
```

### דוגמת עיצוב API שלם

```javascript
// Users API
app.get('/api/v1/users', getAllUsers);           // קבלת כל המשתמשים
app.get('/api/v1/users/:id', getUser);          // קבלת משתמש ספציפי
app.post('/api/v1/users', createUser);          // יצירת משתמש חדש
app.put('/api/v1/users/:id', updateUser);       // עדכון משתמש שלם
app.patch('/api/v1/users/:id', patchUser);      // עדכון חלקי
app.delete('/api/v1/users/:id', deleteUser);    // מחיקת משתמש

// Nested resources
app.get('/api/v1/users/:id/orders', getUserOrders);
app.post('/api/v1/users/:id/orders', createUserOrder);

// Query parameters
app.get('/api/v1/users', (req, res) => {
  const { page = 1, limit = 10, sort = 'name', filter } = req.query;
  // לוגיקת פגינציה, מיון ופילטור
});
```

### Data Formats

**JSON Format**
```json
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com",
  "createdAt": "2023-01-01T00:00:00Z",
  "updatedAt": "2023-01-02T12:00:00Z",
  "links": {
    "self": "/api/v1/users/123",
    "orders": "/api/v1/users/123/orders"
  }
}
```

**Collection Format**
```json
{
  "data": [
    {
      "id": 123,
      "name": "John Doe",
      "email": "john@example.com"
    },
    {
      "id": 124,
      "name": "Jane Smith",
      "email": "jane@example.com"
    }
  ],
  "meta": {
    "total": 2,
    "page": 1,
    "limit": 10,
    "totalPages": 1
  },
  "links": {
    "self": "/api/v1/users?page=1",
    "next": null,
    "prev": null
  }
}
```

---

## אימות והרשאות

### סוגי אימות

**1. API Key**
- פשוט וקל ליישום
- מתאים ל-API פשוטים
- פחות בטוח מפתרונות מתקדמים

```http
GET /api/users
X-API-Key: abc123def456
```

**2. Basic Authentication**
- שימוש ב-username ו-password מקודדים ב-base64
- חייב להשתמש עם HTTPS

```http
GET /api/users
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
```

**3. Bearer Token (JWT)**
- השיטה הפופולרית ביותר
- מאפשרת stateless authentication
- תומכת ב-claims ו-expiration

```http
GET /api/users
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### JWT (JSON Web Tokens)

JWT הוא תקן פתוח לייצוג claims בצורה מאובטחת.

**מבנה JWT:**
```
Header.Payload.Signature
```

**Header:**
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload:**
```json
{
  "sub": "1234567890",
  "name": "John Doe",
  "email": "john@example.com",
  "role": "user",
  "iat": 1516239022,
  "exp": 1516242622
}
```

**דוגמת יצירת JWT:**
```javascript
const jwt = require('jsonwebtoken');

const payload = {
  sub: user.id,
  name: user.name,
  email: user.email,
  role: user.role
};

const token = jwt.sign(payload, process.env.JWT_SECRET, {
  expiresIn: '24h'
});
```

**דוגמת אימות JWT:**
```javascript
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'Access token required' });
  }

  jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
    if (err) {
      return res.status(403).json({ error: 'Invalid token' });
    }
    req.user = user;
    next();
  });
};
```

### OAuth 2.0

OAuth 2.0 הוא פרוטוקול הרשאות שמאפשר ליישומים לגשת למשאבים בשם המשתמש.

**זרימת Authorization Code:**
1. המשתמש מנותב ל-provider לאימות
2. המשתמש מאשר גישה
3. המערכת מקבלת authorization code
4. המערכת מחליפה את ה-code ב-access token
5. המערכת משתמשת ב-token לגישה ל-API

**דוגמה:**
```javascript
app.get('/auth/google', passport.authenticate('google', {
  scope: ['profile', 'email']
}));

app.get('/auth/google/callback', 
  passport.authenticate('google', { failureRedirect: '/login' }),
  (req, res) => {
    // יצירת JWT והחזרתו ללקוח
    const token = generateJWT(req.user);
    res.json({ token });
  }
);
```

### Role-Based Access Control (RBAC)

```javascript
const authorize = (roles) => {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({ error: 'Authentication required' });
    }

    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }

    next();
  };
};

// שימוש
app.get('/api/admin/users', 
  authenticateToken, 
  authorize(['admin']), 
  getAllUsers
);

app.get('/api/users/profile', 
  authenticateToken, 
  authorize(['user', 'admin']), 
  getUserProfile
);
```

---

## Versioning

### סוגי Versioning

**1. URI Versioning**
```http
GET /api/v1/users
GET /api/v2/users
```

**יתרונות:**
- ברור וקל להבין
- קל לנתב לגרסאות שונות
- נתמך בכל ה-clients

**חסרונות:**
- מזהם את ה-URI
- דורש שינוי בכל ה-endpoints

**2. Query Parameter Versioning**
```http
GET /api/users?version=1
GET /api/users?version=2
```

**יתרונות:**
- לא מזהם את ה-URI
- קל לשנות גרסה

**חסרונות:**
- פחות נקי מ-URI versioning
- יכול להתבלבל עם פרמטרים אחרים

**3. Header Versioning**
```http
GET /api/users
Accept: application/vnd.api+json;version=1
```

**יתרונות:**
- URI נקי
- גמישות גבוהה
- תואם ל-HATEOAS

**חסרונות:**
- פחות נפוץ
- קשה יותר ל-debug
- לא כל ה-clients תומכים

### אסטרטגיות Versioning

**1. Semantic Versioning**
- `MAJOR.MINOR.PATCH`
- `MAJOR`: שינויים שוברים תאימות
- `MINOR`: תכונות חדשות, תואם לאחור
- `PATCH`: תיקוני באגים, תואם לאחור

**2. Deprecation Strategy**
```javascript
app.get('/api/v1/users', (req, res) => {
  res.setHeader('Deprecation', 'true');
  res.setHeader('Sunset', '2024-01-01');
  res.setHeader('Link', '</api/v2/users>; rel="successor-version"');
  
  // החזרת נתונים מגרסה 1
});

app.get('/api/v2/users', (req, res) => {
  // החזרת נתונים מגרסה 2
});
```

**3. Backward Compatibility**
```javascript
// גרסה 1
{
  "user_name": "John",
  "user_email": "john@example.com"
}

// גרסה 2 - תומך בשני הפורמטים
{
  "userName": "John",
  "userEmail": "john@example.com",
  // שדות ישנים לתאימות
  "user_name": "John",
  "user_email": "john@example.com"
}
```

---

## Pagination ו-Filtration

### Pagination

**1. Offset-based Pagination**
```http
GET /api/users?page=2&limit=10
```

```javascript
app.get('/api/users', async (req, res) => {
  const page = parseInt(req.query.page) || 1;
  const limit = parseInt(req.query.limit) || 10;
  const offset = (page - 1) * limit;

  const users = await User.findAll({
    limit,
    offset
  });

  const total = await User.count();

  res.json({
    data: users,
    meta: {
      total,
      page,
      limit,
      totalPages: Math.ceil(total / limit)
    },
    links: {
      self: `/api/users?page=${page}`,
      next: page < Math.ceil(total / limit) 
        ? `/api/users?page=${page + 1}` 
        : null,
      prev: page > 1 
        ? `/api/users?page=${page - 1}` 
        : null
    }
  });
});
```

**2. Cursor-based Pagination**
```http
GET /api/users?cursor=abc123&limit=10
```

```javascript
app.get('/api/users', async (req, res) => {
  const cursor = req.query.cursor;
  const limit = parseInt(req.query.limit) || 10;

  const query = {};
  if (cursor) {
    query.id = { [Op.gt]: cursor };
  }

  const users = await User.findAll({
    where: query,
    order: [['id', 'ASC']],
    limit: limit + 1
  });

  const hasMore = users.length > limit;
  const data = hasMore ? users.slice(0, -1) : users;
  const nextCursor = hasMore ? users[users.length - 1].id : null;

  res.json({
    data,
    meta: {
      hasMore,
      nextCursor
    }
  });
});
```

### Filtration

**1. Basic Filtering**
```http
GET /api/users?status=active&role=admin
```

```javascript
app.get('/api/users', async (req, res) => {
  const filters = {};
  
  if (req.query.status) {
    filters.status = req.query.status;
  }
  
  if (req.query.role) {
    filters.role = req.query.role;
  }

  const users = await User.findAll({ where: filters });
  res.json({ data: users });
});
```

**2. Advanced Filtering**
```http
GET /api/users?filter[name]=John&filter[age][gt]=25&filter[status]=active
```

```javascript
app.get('/api/users', async (req, res) => {
  const filter = req.query.filter || {};
  const where = {};

  Object.keys(filter).forEach(key => {
    const value = filter[key];
    
    if (typeof value === 'object') {
      Object.keys(value).forEach(operator => {
        switch (operator) {
          case 'gt':
            where[key] = { [Op.gt]: value[operator] };
            break;
          case 'lt':
            where[key] = { [Op.lt]: value[operator] };
            break;
          case 'gte':
            where[key] = { [Op.gte]: value[operator] };
            break;
          case 'lte':
            where[key] = { [Op.lte]: value[operator] };
            break;
          case 'like':
            where[key] = { [Op.like]: value[operator] };
            break;
        }
      });
    } else {
      where[key] = value;
    }
  });

  const users = await User.findAll({ where });
  res.json({ data: users });
});
```

### Sorting

```http
GET /api/users?sort=name,asc&sort=age,desc
```

```javascript
app.get('/api/users', async (req, res) => {
  const sortParams = req.query.sort || [];
  const order = [];

  if (typeof sortParams === 'string') {
    const [field, direction] = sortParams.split(',');
    order.push([field, direction.toUpperCase()]);
  } else if (Array.isArray(sortParams)) {
    sortParams.forEach(param => {
      const [field, direction] = param.split(',');
      order.push([field, direction.toUpperCase()]);
    });
  }

  const users = await User.findAll({ order });
  res.json({ data: users });
});
```

### Searching

```http
GET /api/users?search=John&fields=name,email
```

```javascript
app.get('/api/users', async (req, res) => {
  const { search, fields } = req.query;
  
  if (!search) {
    return res.json({ data: await User.findAll() });
  }

  const searchFields = fields ? fields.split(',') : ['name', 'email'];
  const searchConditions = searchFields.map(field => ({
    [field]: { [Op.like]: `%${search}%` }
  }));

  const users = await User.findAll({
    where: {
      [Op.or]: searchConditions
    }
  });

  res.json({ data: users });
});
```

---

## Error Handling

### עיצוב Error Response

**פורמס סטנדרטי:**
```json
{
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "User with ID 123 not found",
    "details": {
      "field": "id",
      "value": 123
    },
    "timestamp": "2023-01-01T12:00:00Z",
    "path": "/api/users/123"
  }
}
```

### סוגי Errors

**1. Validation Errors**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "errors": [
        {
          "field": "email",
          "message": "Invalid email format"
        },
        {
          "field": "age",
          "message": "Age must be between 18 and 120"
        }
      ]
    }
  }
}
```

**2. Business Logic Errors**
```json
{
  "error": {
    "code": "INSUFFICIENT_BALANCE",
    "message": "Insufficient balance for this transaction",
    "details": {
      "required": 1000,
      "available": 500
    }
  }
}
```

**3. System Errors**
```json
{
  "error": {
    "code": "DATABASE_ERROR",
    "message": "Internal server error",
    "details": null
  }
}
```

### יישום Error Handling

**Middleware ל-error handling:**
```javascript
const errorHandler = (err, req, res, next) => {
  let error = { ...err };
  error.message = err.message;

  // Mongoose validation error
  if (err.name === 'ValidationError') {
    const message = Object.values(err.errors).map(val => val.message);
    error = {
      code: 'VALIDATION_ERROR',
      message: 'Validation Error',
      details: { errors: message }
    };
    return res.status(400).json({ error });
  }

  // Mongoose duplicate key
  if (err.code === 11000) {
    const field = Object.keys(err.keyValue)[0];
    const value = err.keyValue[field];
    error = {
      code: 'DUPLICATE_FIELD',
      message: `${field} already exists`,
      details: { field, value }
    };
    return res.status(400).json({ error });
  }

  // Mongoose cast error
  if (err.name === 'CastError') {
    error = {
      code: 'INVALID_ID',
      message: 'Invalid ID format',
      details: { field: err.path, value: err.value }
    };
    return res.status(400).json({ error });
  }

  // Default error
  res.status(error.statusCode || 500).json({
    error: {
      code: error.code || 'INTERNAL_ERROR',
      message: error.message || 'Internal Server Error',
      timestamp: new Date().toISOString(),
      path: req.path
    }
  });
};
```

**Custom Error Classes:**
```javascript
class AppError extends Error {
  constructor(message, statusCode, code) {
    super(message);
    this.statusCode = statusCode;
    this.code = code;
    this.isOperational = true;

    Error.captureStackTrace(this, this.constructor);
  }
}

class ValidationError extends AppError {
  constructor(message, details) {
    super(message, 400, 'VALIDATION_ERROR');
    this.details = details;
  }
}

class NotFoundError extends AppError {
  constructor(resource, id) {
    super(`${resource} with ID ${id} not found`, 404, 'NOT_FOUND');
    this.resource = resource;
    this.id = id;
  }
}

// שימוש
app.get('/users/:id', async (req, res, next) => {
  try {
    const user = await User.findById(req.params.id);
    if (!user) {
      throw new NotFoundError('User', req.params.id);
    }
    res.json({ data: user });
  } catch (error) {
    next(error);
  }
});
```

### Global Exception Handling

```javascript
process.on('uncaughtException', (err) => {
  console.log('UNCAUGHT EXCEPTION! 💥 Shutting down...');
  console.log(err.name, err.message);
  process.exit(1);
});

process.on('unhandledRejection', (err) => {
  console.log('UNHANDLED REJECTION! 💥 Shutting down...');
  console.log(err.name, err.message);
  server.close(() => {
    process.exit(1);
  });
});
```

---

## Security

### איומי אבטחה עיקריים

**1. Injection Attacks**
- SQL Injection
- NoSQL Injection
- Command Injection

**2. Authentication Issues**
- Weak passwords
- Brute force attacks
- Session hijacking

**3. Authorization Issues**
- Broken access control
- Privilege escalation

**4. Data Exposure**
- Sensitive data leakage
- Insufficient encryption

**5. DoS Attacks**
- Rate limiting bypass
- Resource exhaustion

### הגנות אבטחה

**1. Input Validation**
```javascript
const Joi = require('joi');

const userSchema = Joi.object({
  name: Joi.string().min(2).max(50).required(),
  email: Joi.string().email().required(),
  age: Joi.number().integer().min(18).max(120),
  password: Joi.string().min(8).pattern(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/).required()
});

const validateUser = (req, res, next) => {
  const { error } = userSchema.validate(req.body);
  if (error) {
    return res.status(400).json({
      error: {
        code: 'VALIDATION_ERROR',
        message: 'Invalid input data',
        details: error.details.map(d => ({
          field: d.path[0],
          message: d.message
        }))
      }
    });
  }
  next();
};
```

**2. Rate Limiting**
```javascript
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 דקות
  max: 100, // מקסימום 100 בקשות
  message: {
    error: {
      code: 'TOO_MANY_REQUESTS',
      message: 'Too many requests, please try again later'
    }
  },
  standardHeaders: true,
  legacyHeaders: false
});

app.use('/api/', limiter);
```

**3. CORS**
```javascript
const cors = require('cors');

const corsOptions = {
  origin: process.env.ALLOWED_ORIGINS?.split(',') || 'http://localhost:3000',
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true
};

app.use(cors(corsOptions));
```

**4. Helmet**
```javascript
const helmet = require('helmet');

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"]
    }
  }
}));
```

**5. Password Hashing**
```javascript
const bcrypt = require('bcrypt');

const hashPassword = async (password) => {
  const saltRounds = 12;
  return await bcrypt.hash(password, saltRounds);
};

const comparePassword = async (password, hash) => {
  return await bcrypt.compare(password, hash);
};
```

**6. HTTPS Enforcement**
```javascript
app.use((req, res, next) => {
  if (req.header('x-forwarded-proto') !== 'https') {
    res.redirect(`https://${req.header('host')}${req.url}`);
  } else {
    next();
  }
});
```

### Security Headers

```javascript
app.use((req, res, next) => {
  // Prevent clickjacking
  res.setHeader('X-Frame-Options', 'DENY');
  
  // Prevent MIME type sniffing
  res.setHeader('X-Content-Type-Options', 'nosniff');
  
  // Enable XSS protection
  res.setHeader('X-XSS-Protection', '1; mode=block');
  
  // Strict transport security
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  
  // Content security policy
  res.setHeader('Content-Security-Policy', "default-src 'self'");
  
  next();
});
```

---

## Testing

### סוגי Tests

**1. Unit Tests**
- בדיקת פונקציות בודדות
- בדיקת לוגיקה עסקית
- בדיקת validation

**2. Integration Tests**
- בדיקת אינטראקציה בין רכיבים
- בדיקת database operations
- בדיקת middleware

**3. End-to-End Tests**
- בדיקת תהליכים מלאים
- בדיקת API endpoints
- בדיקת user workflows

### כלים ל-Testing

**1. Jest**
- Framework ל-unit ו-integration tests
- Mocking capabilities
- Coverage reports

**2. Supertest**
- ספרייה לבדיקת HTTP endpoints
- תומך ב-express
- קל לשימוש

**3. Mocha/Chai**
- Alternative ל-Jest
- גמישות גבוהה
- Assertion library חזקה

### דוגמת Tests

**Unit Test Example:**
```javascript
const { validateUser } = require('../validators/userValidator');
const { ValidationError } = require('../utils/errors');

describe('User Validator', () => {
  test('should validate valid user data', () => {
    const userData = {
      name: 'John Doe',
      email: 'john@example.com',
      age: 30,
      password: 'Password123'
    };

    expect(() => validateUser(userData)).not.toThrow();
  });

  test('should throw error for invalid email', () => {
    const userData = {
      name: 'John Doe',
      email: 'invalid-email',
      age: 30,
      password: 'Password123'
    };

    expect(() => validateUser(userData)).toThrow(ValidationError);
  });

  test('should throw error for weak password', () => {
    const userData = {
      name: 'John Doe',
      email: 'john@example.com',
      age: 30,
      password: 'weak'
    };

    expect(() => validateUser(userData)).toThrow(ValidationError);
  });
});
```

**Integration Test Example:**
```javascript
const request = require('supertest');
const app = require('../app');
const User = require('../models/User');

describe('User API', () => {
  beforeEach(async () => {
    await User.destroy({ where: {} });
  });

  describe('POST /api/users', () => {
    test('should create a new user', async () => {
      const userData = {
        name: 'John Doe',
        email: 'john@example.com',
        age: 30,
        password: 'Password123'
      };

      const response = await request(app)
        .post('/api/users')
        .send(userData)
        .expect(201);

      expect(response.body.data.name).toBe(userData.name);
      expect(response.body.data.email).toBe(userData.email);
      expect(response.body.data).not.toHaveProperty('password');
    });

    test('should return 400 for invalid data', async () => {
      const userData = {
        name: 'John',
        email: 'invalid-email',
        age: 15,
        password: 'weak'
      };

      const response = await request(app)
        .post('/api/users')
        .send(userData)
        .expect(400);

      expect(response.body.error.code).toBe('VALIDATION_ERROR');
    });
  });

  describe('GET /api/users/:id', () => {
    test('should return user by ID', async () => {
      const user = await User.create({
        name: 'John Doe',
        email: 'john@example.com',
        age: 30,
        password: 'hashedpassword'
      });

      const response = await request(app)
        .get(`/api/users/${user.id}`)
        .expect(200);

      expect(response.body.data.name).toBe(user.name);
    });

    test('should return 404 for non-existent user', async () => {
      const response = await request(app)
        .get('/api/users/999')
        .expect(404);

      expect(response.body.error.code).toBe('NOT_FOUND');
    });
  });
});
```

**End-to-End Test Example:**
```javascript
describe('User Workflow E2E', () => {
  test('should complete full user lifecycle', async () => {
    // 1. Create user
    const createResponse = await request(app)
      .post('/api/users')
      .send({
        name: 'John Doe',
        email: 'john@example.com',
        age: 30,
        password: 'Password123'
      })
      .expect(201);

    const userId = createResponse.body.data.id;

    // 2. Get user
    const getResponse = await request(app)
      .get(`/api/users/${userId}`)
      .expect(200);

    expect(getResponse.body.data.name).toBe('John Doe');

    // 3. Update user
    const updateResponse = await request(app)
      .patch(`/api/users/${userId}`)
      .send({ age: 31 })
      .expect(200);

    expect(updateResponse.body.data.age).toBe(31);

    // 4. Delete user
    await request(app)
      .delete(`/api/users/${userId}`)
      .expect(204);

    // 5. Verify deletion
    await request(app)
      .get(`/api/users/${userId}`)
      .expect(404);
  });
});
```

### Test Coverage

```javascript
// jest.config.js
module.exports = {
  collectCoverage: true,
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html'],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },
  testEnvironment: 'node',
  setupFilesAfterEnv: ['<rootDir>/tests/setup.js']
};
```

---

## Documentation

### סוגי Documentation

**1. API Reference**
- Endpoint descriptions
- Request/response formats
- Authentication requirements
- Error codes

**2. Guides**
- Getting started
- Authentication guide
- Best practices
- Troubleshooting

**3. Examples**
- Code samples
- Use cases
- Integration examples

### כלים ל-Documentation

**1. Swagger/OpenAPI**
```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0
  description: API for managing users

paths:
  /users:
    get:
      summary: Get all users
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
    post:
      summary: Create a new user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUser'
      responses:
        '201':
          description: User created successfully
        '400':
          description: Validation error

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
        email:
          type: string
        age:
          type: integer
    CreateUser:
      type: object
      required:
        - name
        - email
        - password
      properties:
        name:
          type: string
        email:
          type: string
        password:
          type: string
        age:
          type: integer
```

**2. Postman Collections**
```json
{
  "info": {
    "name": "User API",
    "description": "Collection for User API testing"
  },
  "item": [
    {
      "name": "Get All Users",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "{{baseUrl}}/api/users",
          "host": ["{{baseUrl}}"],
          "path": ["api", "users"]
        }
      }
    },
    {
      "name": "Create User",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"name\": \"John Doe\",\n  \"email\": \"john@example.com\",\n  \"password\": \"Password123\"\n}"
        },
        "url": {
          "raw": "{{baseUrl}}/api/users",
          "host": ["{{baseUrl}}"],
          "path": ["api", "users"]
        }
      }
    }
  ],
  "variable": [
    {
      "key": "baseUrl",
      "value": "http://localhost:3000"
    }
  ]
}
```

### Code Documentation

**JSDoc Comments:**
```javascript
/**
 * Creates a new user in the database
 * @param {Object} userData - User data to create
 * @param {string} userData.name - User name (2-50 characters)
 * @param {string} userData.email - User email (valid email format)
 * @param {number} userData.age - User age (18-120)
 * @param {string} userData.password - User password (min 8 chars)
 * @returns {Promise<Object>} Created user object
 * @throws {ValidationError} If validation fails
 * @throws {DatabaseError} If database operation fails
 * @example
 * const user = await createUser({
 *   name: 'John Doe',
 *   email: 'john@example.com',
 *   age: 30,
 *   password: 'Password123'
 * });
 */
const createUser = async (userData) => {
  // Implementation
};
```

### README Template

```markdown
# User API

RESTful API for managing users with authentication and authorization.

## Features

- User CRUD operations
- JWT authentication
- Role-based access control
- Input validation
- Rate limiting
- Comprehensive error handling

## Getting Started

### Prerequisites

- Node.js 14+
- MongoDB
- npm or yarn

### Installation

```bash
git clone https://github.com/username/user-api.git
cd user-api
npm install
```

### Environment Variables

Create a `.env` file:

```
NODE_ENV=development
PORT=3000
MONGODB_URI=mongodb://localhost:27017/user-api
JWT_SECRET=your-secret-key
JWT_EXPIRES_IN=24h
```

### Running the API

```bash
# Development
npm run dev

# Production
npm start
```

## API Documentation

### Authentication

Most endpoints require authentication. Include the JWT token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

### Endpoints

#### Users

- `GET /api/users` - Get all users (admin only)
- `GET /api/users/:id` - Get user by ID
- `POST /api/users` - Create new user
- `PUT /api/users/:id` - Update user (admin or owner)
- `DELETE /api/users/:id` - Delete user (admin only)

#### Authentication

- `POST /api/auth/login` - Login user
- `POST /api/auth/register` - Register new user
- `POST /api/auth/refresh` - Refresh JWT token

### Examples

#### Create User

```bash
curl -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "Password123",
    "age": 30
  }'
```

#### Login

```bash
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "Password123"
  }'
```

## Error Handling

The API returns consistent error responses:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field": "email",
      "message": "Invalid email format"
    }
  }
}
```

## Testing

```bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run specific test file
npm test -- user.test.js
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License
```

---

## Best Practices

### עקרונות כלליים

**1. Consistency**
- השתמש במוסכמות עקביות בכל ה-API
- שמות endpoints, פורמט תגובות, error handling
- הקפד על סטנדרטים אחידים

**2. Simplicity**
- שמור על ה-API פשוט וקל לשימוש
- הימנע מפיצ'רים מיותרים
- עיצוב אינטואיטיבי

**3. Performance**
- אופטימיזציה של queries ל-database
- שימוש נכון ב-caching
- pagination יעיל

**4. Security**
- אימות והרשאות נכונים
- validation של כל ה-inputs
- שימוש ב-HTTPS

### Naming Conventions

**Endpoints:**
```http
// טוב
GET /api/users
GET /api/users/123
GET /api/users/123/orders

// רע
GET /api/getAllUsers
GET /api/user/123
GET /api/orders/byUser/123
```

**JSON Fields:**
```json
// טוב - camelCase
{
  "firstName": "John",
  "lastName": "Doe",
  "createdAt": "2023-01-01T00:00:00Z"
}

// רע - inconsistent
{
  "first_name": "John",
  "lastName": "Doe",
  "created_at": "2023-01-01T00:00:00Z"
}
```

### Response Format

**Success Response:**
```json
{
  "data": {
    "id": 123,
    "name": "John Doe"
  },
  "meta": {
    "timestamp": "2023-01-01T12:00:00Z"
  }
}
```

**Collection Response:**
```json
{
  "data": [...],
  "meta": {
    "total": 100,
    "page": 1,
    "limit": 10,
    "totalPages": 10
  },
  "links": {
    "self": "/api/users?page=1",
    "next": "/api/users?page=2",
    "prev": null
  }
}
```

**Error Response:**
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Resource not found",
    "timestamp": "2023-01-01T12:00:00Z",
    "path": "/api/users/999"
  }
}
```

### Performance Best Practices

**1. Database Optimization**
```javascript
// רע - N+1 query problem
const getUsersWithOrders = async () => {
  const users = await User.findAll();
  for (const user of users) {
    user.orders = await Order.findAll({ where: { userId: user.id } });
  }
  return users;
};

// טוב - eager loading
const getUsersWithOrders = async () => {
  return await User.findAll({
    include: [{ model: Order, as: 'orders' }]
  });
};
```

**2. Caching Strategy**
```javascript
const redis = require('redis');
const client = redis.createClient();

const getCachedUser = async (id) => {
  const cacheKey = `user:${id}`;
  
  // Try cache first
  const cached = await client.get(cacheKey);
  if (cached) {
    return JSON.parse(cached);
  }
  
  // Get from database
  const user = await User.findById(id);
  if (user) {
    // Cache for 1 hour
    await client.setex(cacheKey, 3600, JSON.stringify(user));
  }
  
  return user;
};
```

**3. Pagination Optimization**
```javascript
// רע - offset pagination for large datasets
const getUsers = async (page, limit) => {
  const offset = (page - 1) * limit;
  return await User.findAll({ offset, limit });
};

// טוב - cursor pagination for large datasets
const getUsers = async (cursor, limit) => {
  const where = cursor ? { id: { [Op.gt]: cursor } } : {};
  return await User.findAll({
    where,
    order: [['id', 'ASC']],
    limit: limit + 1
  });
};
```

### Code Organization

**Folder Structure:**
```
src/
├── controllers/
│   ├── userController.js
│   ├── authController.js
│   └── orderController.js
├── models/
│   ├── User.js
│   ├── Order.js
│   └── index.js
├── routes/
│   ├── userRoutes.js
│   ├── authRoutes.js
│   └── index.js
├── middleware/
│   ├── auth.js
│   ├── validation.js
│   └── errorHandler.js
├── services/
│   ├── userService.js
│   ├── emailService.js
│   └── paymentService.js
├── utils/
│   ├── errors.js
│   ├── helpers.js
│   └── constants.js
├── validators/
│   ├── userValidator.js
│   └── orderValidator.js
└── app.js
```

**Controller Pattern:**
```javascript
// controllers/userController.js
const userService = require('../services/userService');

const userController = {
  getAllUsers: async (req, res, next) => {
    try {
      const users = await userService.getAllUsers(req.query);
      res.json({ data: users });
    } catch (error) {
      next(error);
    }
  },

  getUserById: async (req, res, next) => {
    try {
      const user = await userService.getUserById(req.params.id);
      res.json({ data: user });
    } catch (error) {
      next(error);
    }
  },

  createUser: async (req, res, next) => {
    try {
      const user = await userService.createUser(req.body);
      res.status(201).json({ data: user });
    } catch (error) {
      next(error);
    }
  }
};

module.exports = userController;
```

**Service Layer:**
```javascript
// services/userService.js
const User = require('../models/User');
const { NotFoundError, ValidationError } = require('../utils/errors');

const userService = {
  getAllUsers: async (filters) => {
    return await User.findAll({ where: filters });
  },

  getUserById: async (id) => {
    const user = await User.findById(id);
    if (!user) {
      throw new NotFoundError('User', id);
    }
    return user;
  },

  createUser: async (userData) => {
    try {
      return await User.create(userData);
    } catch (error) {
      if (error.code === 11000) {
        throw new ValidationError('Email already exists');
      }
      throw error;
    }
  }
};

module.exports = userService;
```

---

## Tools ו-Frameworks

### Backend Frameworks

**1. Express.js**
```javascript
const express = require('express');
const app = express();

app.use(express.json());
app.use('/api/users', userRoutes);

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

**יתרונות:**
- פשוט וקל ללמוד
- גמישות גבוהה
- קהילה גדולה
- מגוון רחב של middleware

**2. NestJS**
```typescript
import { Controller, Get, Post, Body } from '@nestjs/common';
import { UserService } from './user.service';

@Controller('users')
export class UserController {
  constructor(private readonly userService: UserService) {}

  @Get()
  getAllUsers() {
    return this.userService.findAll();
  }

  @Post()
  createUser(@Body() createUserDto: CreateUserDto) {
    return this.userService.create(createUserDto);
  }
}
```

**יתרונות:**
- TypeScript out of the box
- ארכיטקטורה מובנית
- Dependency injection
- קל לבדיקות

**3. Fastify**
```javascript
const fastify = require('fastify')({ logger: true });

fastify.get('/users', async (request, reply) => {
  const users = await getUsers();
  return { data: users };
});

fastify.post('/users', {
  schema: {
    body: {
      type: 'object',
      properties: {
        name: { type: 'string' },
        email: { type: 'string', format: 'email' }
      },
      required: ['name', 'email']
    }
  }
}, async (request, reply) => {
  const user = await createUser(request.body);
  reply.code(201).send({ data: user });
});
```

**יתרונות:**
- ביצועים גבוהים
- Validation מובנה
- Type safety
- קל להרחבה

### Database Options

**1. MongoDB with Mongoose**
```javascript
const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
  name: { type: String, required: true, minlength: 2, maxlength: 50 },
  email: { type: String, required: true, unique: true },
  age: { type: Number, min: 18, max: 120 },
  password: { type: String, required: true, minlength: 8 }
}, {
  timestamps: true
});

const User = mongoose.model('User', userSchema);
```

**2. PostgreSQL with Sequelize**
```javascript
const { DataTypes } = require('sequelize');

const User = sequelize.define('User', {
  name: {
    type: DataTypes.STRING,
    allowNull: false,
    validate: {
      len: [2, 50]
    }
  },
  email: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true,
    validate: {
      isEmail: true
    }
  },
  age: {
    type: DataTypes.INTEGER,
    validate: {
      min: 18,
      max: 120
    }
  }
});
```

### Authentication Libraries

**1. Passport.js**
```javascript
const passport = require('passport');
const LocalStrategy = require('passport-local').Strategy;
const JwtStrategy = require('passport-jwt').Strategy;

passport.use(new LocalStrategy(
  async (username, password, done) => {
    try {
      const user = await User.findOne({ email: username });
      if (!user || !await user.comparePassword(password)) {
        return done(null, false);
      }
      return done(null, user);
    } catch (error) {
      return done(error);
    }
  }
));

passport.use(new JwtStrategy({
  jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
  secretOrKey: process.env.JWT_SECRET
}, async (payload, done) => {
  try {
    const user = await User.findById(payload.sub);
    if (!user) {
      return done(null, false);
    }
    return done(null, user);
  } catch (error) {
    return done(error);
  }
}));
```

**2. Auth0**
```javascript
const { auth } = require('express-oauth2-jwt-bearer');

const checkJwt = auth({
  audience: process.env.AUTH0_AUDIENCE,
  issuerBaseURL: process.env.AUTH0_ISSUER_BASE_URL,
});

app.get('/api/users', checkJwt, (req, res) => {
  res.json({ data: users });
});
```

### Testing Tools

**1. Jest Setup**
```javascript
// jest.config.js
module.exports = {
  testEnvironment: 'node',
  setupFilesAfterEnv: ['<rootDir>/tests/setup.js'],
  testMatch: ['**/__tests__/**/*.js', '**/?(*.)+(spec|test).js'],
  collectCoverageFrom: [
    'src/**/*.js',
    '!src/**/*.test.js'
  ]
};
```

**2. Supertest Usage**
```javascript
const request = require('supertest');
const app = require('../src/app');

describe('API Tests', () => {
  test('should create user', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({
        name: 'John Doe',
        email: 'john@example.com',
        password: 'Password123'
      })
      .expect(201);

    expect(response.body.data.name).toBe('John Doe');
  });
});
```

### Monitoring ו-Logging

**1. Winston Logging**
```javascript
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.simple()
  }));
}
```

**2. Morgan HTTP Logger**
```javascript
const morgan = require('morgan');

app.use(morgan('combined', {
  stream: {
    write: (message) => logger.info(message.trim())
  }
}));
```

---

## פרויקט מעשי

### תיאור הפרויקט

נבנה API מלא לניהול חנות אונליין עם:
- מוצרים
- משתמשים
- הזמנות
- סל קניות
- תשלומים

### מבנה הפרויקט

```
online-store-api/
├── src/
│   ├── controllers/
│   │   ├── authController.js
│   │   ├── userController.js
│   │   ├── productController.js
│   │   ├── orderController.js
│   │   └── cartController.js
│   ├── models/
│   │   ├── User.js
│   │   ├── Product.js
│   │   ├── Order.js
│   │   ├── Cart.js
│   │   └── CartItem.js
│   ├── routes/
│   │   ├── authRoutes.js
│   │   ├── userRoutes.js
│   │   ├── productRoutes.js
│   │   ├── orderRoutes.js
│   │   └── cartRoutes.js
│   ├── middleware/
│   │   ├── auth.js
│   │   ├── validation.js
│   │   ├── errorHandler.js
│   │   └── rateLimit.js
│   ├── services/
│   │   ├── authService.js
│   │   ├── emailService.js
│   │   ├── paymentService.js
│   │   └── productService.js
│   ├── validators/
│   │   ├── userValidator.js
│   │   ├── productValidator.js
│   │   └── orderValidator.js
│   └── utils/
│       ├── errors.js
│       ├── helpers.js
│       └── constants.js
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docs/
│   ├── api.yaml
│   └── README.md
├── package.json
├── .env.example
└── .gitignore
```

### Models

**User Model:**
```javascript
const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

const userSchema = new mongoose.Schema({
  firstName: {
    type: String,
    required: true,
    trim: true,
    minlength: 2,
    maxlength: 50
  },
  lastName: {
    type: String,
    required: true,
    trim: true,
    minlength: 2,
    maxlength: 50
  },
  email: {
    type: String,
    required: true,
    unique: true,
    lowercase: true,
    trim: true
  },
  password: {
    type: String,
    required: true,
    minlength: 8
  },
  role: {
    type: String,
    enum: ['customer', 'admin'],
    default: 'customer'
  },
  addresses: [{
    street: String,
    city: String,
    state: String,
    zipCode: String,
    country: String,
    isDefault: Boolean
  }],
  isActive: {
    type: Boolean,
    default: true
  }
}, {
  timestamps: true
});

userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();
  this.password = await bcrypt.hash(this.password, 12);
  next();
});

userSchema.methods.comparePassword = async function(password) {
  return await bcrypt.compare(password, this.password);
};

module.exports = mongoose.model('User', userSchema);
```

**Product Model:**
```javascript
const mongoose = require('mongoose');

const productSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
    trim: true,
    maxlength: 200
  },
  description: {
    type: String,
    required: true,
    maxlength: 2000
  },
  price: {
    type: Number,
    required: true,
    min: 0
  },
  category: {
    type: String,
    required: true,
    enum: ['electronics', 'clothing', 'books', 'home', 'sports']
  },
  brand: {
    type: String,
    required: true,
    trim: true
  },
  images: [{
    url: String,
    alt: String
  }],
  inventory: {
    quantity: {
      type: Number,
      required: true,
      min: 0
    },
    reserved: {
      type: Number,
      default: 0
    }
  },
  specifications: {
    weight: Number,
    dimensions: {
      length: Number,
      width: Number,
      height: Number
    },
    color: String,
    size: String
  },
  ratings: {
    average: {
      type: Number,
      default: 0,
      min: 0,
      max: 5
    },
    count: {
      type: Number,
      default: 0
    }
  },
  isActive: {
    type: Boolean,
    default: true
  }
}, {
  timestamps: true
});

productSchema.virtual('availableQuantity').get(function() {
  return this.inventory.quantity - this.inventory.reserved;
});

module.exports = mongoose.model('Product', productSchema);
```

**Order Model:**
```javascript
const mongoose = require('mongoose');

const orderItemSchema = new mongoose.Schema({
  product: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Product',
    required: true
  },
  quantity: {
    type: Number,
    required: true,
    min: 1
  },
  price: {
    type: Number,
    required: true
  },
  total: {
    type: Number,
    required: true
  }
});

const orderSchema = new mongoose.Schema({
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  items: [orderItemSchema],
  shippingAddress: {
    street: { type: String, required: true },
    city: { type: String, required: true },
    state: { type: String, required: true },
    zipCode: { type: String, required: true },
    country: { type: String, required: true }
  },
  paymentMethod: {
    type: String,
    enum: ['credit_card', 'paypal', 'bank_transfer'],
    required: true
  },
  paymentStatus: {
    type: String,
    enum: ['pending', 'processing', 'completed', 'failed', 'refunded'],
    default: 'pending'
  },
  orderStatus: {
    type: String,
    enum: ['pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled'],
    default: 'pending'
  },
  subtotal: {
    type: Number,
    required: true
  },
  tax: {
    type: Number,
    required: true
  },
  shipping: {
    type: Number,
    required: true
  },
  total: {
    type: Number,
    required: true
  },
  trackingNumber: String,
  notes: String
}, {
  timestamps: true
});

module.exports = mongoose.model('Order', orderSchema);
```

### Controllers

**Product Controller:**
```javascript
const productService = require('../services/productService');
const { ValidationError } = require('../utils/errors');

const productController = {
  getAllProducts: async (req, res, next) => {
    try {
      const {
        page = 1,
        limit = 20,
        category,
        brand,
        minPrice,
        maxPrice,
        sort = 'createdAt',
        order = 'desc',
        search
      } = req.query;

      const filters = {};
      if (category) filters.category = category;
      if (brand) filters.brand = brand;
      if (minPrice || maxPrice) {
        filters.price = {};
        if (minPrice) filters.price.$gte = parseFloat(minPrice);
        if (maxPrice) filters.price.$lte = parseFloat(maxPrice);
      }
      if (search) {
        filters.$or = [
          { name: { $regex: search, $options: 'i' } },
          { description: { $regex: search, $options: 'i' } }
        ];
      }
      filters.isActive = true;

      const products = await productService.getProducts(filters, {
        page: parseInt(page),
        limit: parseInt(limit),
        sort,
        order
      });

      res.json({
        data: products.data,
        meta: products.meta,
        links: products.links
      });
    } catch (error) {
      next(error);
    }
  },

  getProductById: async (req, res, next) => {
    try {
      const product = await productService.getProductById(req.params.id);
      res.json({ data: product });
    } catch (error) {
      next(error);
    }
  },

  createProduct: async (req, res, next) => {
    try {
      const product = await productService.createProduct(req.body);
      res.status(201).json({ data: product });
    } catch (error) {
      next(error);
    }
  },

  updateProduct: async (req, res, next) => {
    try {
      const product = await productService.updateProduct(req.params.id, req.body);
      res.json({ data: product });
    } catch (error) {
      next(error);
    }
  },

  deleteProduct: async (req, res, next) => {
    try {
      await productService.deleteProduct(req.params.id);
      res.status(204).send();
    } catch (error) {
      next(error);
    }
  }
};

module.exports = productController;
```

**Order Controller:**
```javascript
const orderService = require('../services/orderService');
const { authorize } = require('../middleware/auth');

const orderController = {
  createOrder: async (req, res, next) => {
    try {
      const order = await orderService.createOrder(req.user.id, req.body);
      res.status(201).json({ data: order });
    } catch (error) {
      next(error);
    }
  },

  getUserOrders: async (req, res, next) => {
    try {
      const { page = 1, limit = 10, status } = req.query;
      const orders = await orderService.getUserOrders(req.user.id, {
        page: parseInt(page),
        limit: parseInt(limit),
        status
      });
      res.json({ data: orders.data, meta: orders.meta });
    } catch (error) {
      next(error);
    }
  },

  getOrderById: async (req, res, next) => {
    try {
      const order = await orderService.getOrderById(req.params.id, req.user.id);
      res.json({ data: order });
    } catch (error) {
      next(error);
    }
  },

  updateOrderStatus: async (req, res, next) => {
    try {
      const order = await orderService.updateOrderStatus(
        req.params.id,
        req.body.status,
        req.body.notes
      );
      res.json({ data: order });
    } catch (error) {
      next(error);
    }
  }
};

module.exports = orderController;
```

### Services

**Product Service:**
```javascript
const Product = require('../models/Product');
const { NotFoundError, ValidationError } = require('../utils/errors');

const productService = {
  getProducts: async (filters, options) => {
    const {
      page = 1,
      limit = 20,
      sort = 'createdAt',
      order = 'desc'
    } = options;

    const skip = (page - 1) * limit;
    const sortOrder = order === 'desc' ? -1 : 1;

    const [products, total] = await Promise.all([
      Product.find(filters)
        .sort({ [sort]: sortOrder })
        .skip(skip)
        .limit(limit)
        .populate('category'),
      Product.countDocuments(filters)
    ]);

    const totalPages = Math.ceil(total / limit);

    return {
      data: products,
      meta: {
        total,
        page: parseInt(page),
        limit: parseInt(limit),
        totalPages
      },
      links: {
        self: `/api/products?page=${page}&limit=${limit}`,
        next: page < totalPages ? `/api/products?page=${page + 1}&limit=${limit}` : null,
        prev: page > 1 ? `/api/products?page=${page - 1}&limit=${limit}` : null
      }
    };
  },

  getProductById: async (id) => {
    const product = await Product.findById(id);
    if (!product || !product.isActive) {
      throw new NotFoundError('Product', id);
    }
    return product;
  },

  createProduct: async (productData) => {
    try {
      const product = new Product(productData);
      await product.save();
      return product;
    } catch (error) {
      if (error.code === 11000) {
        throw new ValidationError('Product with this name already exists');
      }
      throw error;
    }
  },

  updateProduct: async (id, updateData) => {
    const product = await Product.findByIdAndUpdate(
      id,
      updateData,
      { new: true, runValidators: true }
    );
    
    if (!product) {
      throw new NotFoundError('Product', id);
    }
    
    return product;
  },

  deleteProduct: async (id) => {
    const product = await Product.findById(id);
    if (!product) {
      throw new NotFoundError('Product', id);
    }
    
    // Soft delete
    product.isActive = false;
    await product.save();
  },

  updateInventory: async (productId, quantity, operation = 'reserve') => {
    const product = await Product.findById(productId);
    if (!product) {
      throw new NotFoundError('Product', productId);
    }

    if (operation === 'reserve') {
      if (product.availableQuantity < quantity) {
        throw new ValidationError('Insufficient inventory');
      }
      product.inventory.reserved += quantity;
    } else if (operation === 'release') {
      product.inventory.reserved -= quantity;
    } else if (operation === 'deduct') {
      product.inventory.quantity -= quantity;
      product.inventory.reserved -= quantity;
    }

    await product.save();
    return product;
  }
};

module.exports = productService;
```

### Routes

**Product Routes:**
```javascript
const express = require('express');
const productController = require('../controllers/productController');
const { authenticate, authorize } = require('../middleware/auth');
const { validateProduct } = require('../validators/productValidator');

const router = express.Router();

// Public routes
router.get('/', productController.getAllProducts);
router.get('/:id', productController.getProductById);

// Protected admin routes
router.post('/', 
  authenticate, 
  authorize(['admin']), 
  validateProduct, 
  productController.createProduct
);

router.put('/:id', 
  authenticate, 
  authorize(['admin']), 
  validateProduct, 
  productController.updateProduct
);

router.delete('/:id', 
  authenticate, 
  authorize(['admin']), 
  productController.deleteProduct
);

module.exports = router;
```

### Main App

```javascript
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const rateLimit = require('express-rate-limit');
const mongoose = require('mongoose');

const authRoutes = require('./routes/authRoutes');
const userRoutes = require('./routes/userRoutes');
const productRoutes = require('./routes/productRoutes');
const orderRoutes = require('./routes/orderRoutes');
const cartRoutes = require('./routes/cartRoutes');

const errorHandler = require('./middleware/errorHandler');

const app = express();

// Security middleware
app.use(helmet());
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || 'http://localhost:3000',
  credentials: true
}));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  message: {
    error: {
      code: 'TOO_MANY_REQUESTS',
      message: 'Too many requests, please try again later'
    }
  }
});
app.use('/api/', limiter);

// Logging
app.use(morgan('combined'));

// Body parsing
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Routes
app.use('/api/auth', authRoutes);
app.use('/api/users', userRoutes);
app.use('/api/products', productRoutes);
app.use('/api/orders', orderRoutes);
app.use('/api/cart', cartRoutes);

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

// Error handling
app.use(errorHandler);

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({
    error: {
      code: 'NOT_FOUND',
      message: 'Endpoint not found',
      path: req.originalUrl
    }
  });
});

module.exports = app;
```

### Server Start

```javascript
const mongoose = require('mongoose');
const app = require('./src/app');

const PORT = process.env.PORT || 3000;

mongoose.connect(process.env.MONGODB_URI)
  .then(() => {
    console.log('Connected to MongoDB');
    app.listen(PORT, () => {
      console.log(`Server running on port ${PORT}`);
    });
  })
  .catch(error => {
    console.error('Database connection error:', error);
    process.exit(1);
  });
```

### Testing

**Integration Test for Products:**
```javascript
const request = require('supertest');
const app = require('../../src/app');
const Product = require('../../src/models/Product');

describe('Product API', () => {
  beforeEach(async () => {
    await Product.deleteMany({});
  });

  describe('GET /api/products', () => {
    test('should return paginated products', async () => {
      // Create test products
      await Product.create([
        {
          name: 'Laptop',
          description: 'High performance laptop',
          price: 999,
          category: 'electronics',
          brand: 'Dell'
        },
        {
          name: 'Mouse',
          description: 'Wireless mouse',
          price: 29,
          category: 'electronics',
          brand: 'Logitech'
        }
      ]);

      const response = await request(app)
        .get('/api/products')
        .expect(200);

      expect(response.body.data).toHaveLength(2);
      expect(response.body.meta.total).toBe(2);
      expect(response.body.meta.page).toBe(1);
    });

    test('should filter products by category', async () => {
      await Product.create([
        {
          name: 'Laptop',
          description: 'High performance laptop',
          price: 999,
          category: 'electronics',
          brand: 'Dell'
        },
        {
          name: 'T-Shirt',
          description: 'Cotton t-shirt',
          price: 19,
          category: 'clothing',
          brand: 'Nike'
        }
      ]);

      const response = await request(app)
        .get('/api/products?category=electronics')
        .expect(200);

      expect(response.body.data).toHaveLength(1);
      expect(response.body.data[0].category).toBe('electronics');
    });
  });

  describe('POST /api/products', () => {
    test('should create new product with valid data', async () => {
      const productData = {
        name: 'Test Product',
        description: 'Test description',
        price: 99,
        category: 'electronics',
        brand: 'Test Brand'
      };

      const response = await request(app)
        .post('/api/products')
        .set('Authorization', `Bearer ${adminToken}`)
        .send(productData)
        .expect(201);

      expect(response.body.data.name).toBe(productData.name);
      expect(response.body.data.price).toBe(productData.price);
    });

    test('should return 400 for invalid data', async () => {
      const invalidData = {
        name: '',
        description: 'Test',
        price: -10
      };

      const response = await request(app)
        .post('/api/products')
        .set('Authorization', `Bearer ${adminToken}`)
        .send(invalidData)
        .expect(400);

      expect(response.body.error.code).toBe('VALIDATION_ERROR');
    });
  });
});
```

---

## סיכום

מדריך זה כיסה את כל ההיבטים החשובים של REST API:

1. **יסודות REST** - הבנה של עקרונות ו-concepts
2. **HTTP Methods** - שימוש נכון במתודות HTTP
3. **Status Codes** - החזרת סטטוס קודים רלוונטיים
4. **API Design** - עיצוב clean ו-intuitive
5. **Authentication** - אימות משתמשים בצורה מאובטחת
6. **Security** - הגנה על ה-API מפני איומים
7. **Testing** - בדיקות מקיפות להבטחת איכות
8. **Documentation** - תיעוד ברור ומקיף
9. **Best Practices** - עקרונות לפיתוח מקצועי
10. **Practical Project** - יישום מלא של כל ה-concepts

### טיפים אחרונים להצלחה:

- **התחל פשוט** - אל תנסה ליישם הכל בבת אחת
- **תרגל רבות** - בנה API קטנים והרחב אותם
- **קרא תיעוד** - למד מ-APIים קיימים
- **הצטרף לקהילה** - שתף ולמד מאחרים
- **המשך ללמוד** - העולם מתפתח כל הזמן

בהצלחה בפיתוח REST API! 🚀
