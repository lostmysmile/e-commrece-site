# Flask E-Commerce Site

A simple e-commerce web application built with Flask, featuring a REST API backend and a web frontend.

## Quick Start

**To run the application, simply double-click `run.bat`** - this will start both the web frontend (port 5000) and the API backend (port 5001).

Once running, open your browser to `http://localhost:5000`.

---

## Project Structure

```
flask e-commrece/
├── apps/
│   ├── api/          # REST API backend
│   │   ├── app.py    # API app entry point
│   │   ├── config.py # Database configuration
│   │   ├── errors.py # Error handlers
│   │   ├── database/
│   │   │   ├── services/    # Business logic (user_service, product_service)
│   │   │   └── src/models/  # SQLAlchemy models (User, Product, Category)
│   │   └── routes/  # API endpoints (user_routes, product_routes)
│   │
│   └── web/          # Web frontend
│       ├── app.py    # Web app entry point
│       ├── routes.py # Page routes (home, shop, cart, login, signup)
│       ├── services.py # Data fetching services
│       ├── pages/    # HTML templates
│       └── assets/   # CSS and JavaScript files
│
├── instance/         # SQLite database storage
└── readme.md         # This file
```

## Architecture

This project uses a **two-app architecture**:

1. **API App** (Port 5001) - Handles data and business logic
   - RESTful endpoints for users and products
   - SQLite database for data persistence
   - SQLAlchemy ORM for database operations

2. **Web App** (Port 5000) - Handles the user interface
   - Server-side rendered HTML pages
   - Consumes data from the API (or directly from database)

## Brief Logic

### API Layer (`apps/api/`)
- **Models**: Define database tables (User, Product, Category)
- **Services**: Contain business logic (user_service.py, product_service.py)
- **Routes**: Expose REST endpoints for CRUD operations
- **Database**: Uses SQLAlchemy with SQLite (`data.db`)

### Web Layer (`apps/web/`)
- **Routes**: Define pages (Home, Shop, Cart, Login, Signup)
- **Services**: Fetch data for display
- **Templates**: Jinja2 HTML templates
- **Assets**: CSS styling and JavaScript (cart functionality)

## Requirements

- Python 3.8+
- Flask
- Flask-SQLAlchemy

## Installation

1. Install dependencies:
```bash
pip install flask flask-sqlalchemy
```

## Usage

1. Run `run.bat` (or double-click it)
2. Open your browser to `http://localhost:5000`
3. Browse the shop, view products, and add items to cart
4. Use the login/signup pages for user authentication

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users` | Get all users |
| GET | `/api/users/<id>` | Get user by ID |
| POST | `/api/users` | Create new user |
| GET | `/api/products` | Get all products |
| GET | `/api/products/<id>` | Get product by ID |
| POST | `/api/products` | Create new product |

## Database

The application uses SQLite. On first run, the database (`instance/data.db`) is automatically created with all required tables.

## Customization

- Modify `apps/api/config.py` to change database settings
- Add new models in `apps/api/database/src/models/`
- Create new pages in `apps/web/pages/`
- Style the site in `apps/web/assets/css/styles.css`