# Intermediate FastAPI Project

A FastAPI application with database integration and basic CRUD operations.

## Features

- **Database**: SQLAlchemy ORM with SQLite
- **CRUD Operations**: Create, Read, Update, Delete for items
- **Error Handling**: Basic HTTP exception handling
- **Auto-documentation**: Swagger UI and ReDoc automatically generated
- **Simple Structure**: Clean, easy-to-understand codebase

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
uvicorn main:app --reload
```

The server will start on `http://localhost:8000`

## API Endpoints

### Items
- `GET /items/` - List all available items
- `GET /items/{item_id}` - Get specific item
- `POST /items/` - Create new item
- `PUT /items/{item_id}` - Update item
- `DELETE /items/{item_id}` - Delete item

### System
- `GET /health` - Health check with database status
- `GET /` - Welcome message

## API Documentation

Once the server is running, you can access:
- **Swagger UI**: `http://localhost:8000/docs` - Interactive API testing
- **ReDoc**: `http://localhost:8000/redoc` - API documentation

## Database Model

### Item
- id (integer, primary key)
- name (string, indexed)
- description (string, optional)
- price (float)
- in_stock (boolean, default: True)
- created_at (datetime)

## Example Usage

1. Create an item:
```bash
curl -X POST "http://localhost:8000/items/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Book", "description": "A good book", "price": 19.99}'
```

2. Get all items:
```bash
curl "http://localhost:8000/items/"
```

3. Update an item:
```bash
curl -X PUT "http://localhost:8000/items/1" \
  -H "Content-Type: application/json" \
  -d '{"price": 24.99}'
```

4. Delete an item:
```bash
curl -X DELETE "http://localhost:8000/items/1"
```
