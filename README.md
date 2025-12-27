# 🍽️ ByteFeast Restaurant

**ByteFeast** is a Django RESTful API project for a restaurant-style food ordering platform. It provides endpoints for menu categories, food items, shopping cart, orders, reviews, and admin analytics.

---

## 🌍 Live Links

- **Production:** [byte-feast-react-w8qi.vercel.app](https://byte-feast-react-w8qi.vercel.app/)

- **Base API:** [byte-feast-resturant-django-rest-ap.vercel.app/api/v1/](https://byte-feast-resturant-django-rest-ap.vercel.app/api/v1/)

- **Swagger Documentation:** [byte-feast-resturant-django-rest-ap.vercel.app/swagger/](https://byte-feast-resturant-django-rest-ap.vercel.app/swagger/)

---

## 👤 Demo Accounts

| Role     | Email                    | Password   |
| -------- | ------------------------ | ---------- |
| Admin    | `admin@gmail.com`        | `kgb12345` |
| Customer | `doveb99651@besaies.com` | `kgb12345` |

Use these credentials to log in and explore the API in Swagger or Postman.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Database Migrations](#database-migrations)
  - [Running the Server](#running-the-server)
- [API Endpoints](#api-endpoints)
  - [Authentication](#authentication)
  - [Menu](#menu)
  - [Cart](#cart)
  - [Orders](#orders)
  - [Reviews](#reviews)
  - [Analytics](#analytics)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## 🌟 Features

- **Menu Management**: Categories & FoodItems with filtering, searching, pagination, and special pricing.
- **Shopping Cart**: One cart per user; add, update, and remove items.
- **Order Processing**: Create orders from cart, cancel orders, admin status updates.
- **Reviews**: Authenticated users can review foods; one review per user per food.
- **Analytics Dashboard** (Admin only): Last week's orders, top-rated foods, trending foods.
- **API Docs**: Auto-generated Swagger & Redoc UI.

---

## 🛠️ Tech Stack

- Python 3.13
- Django 5.1.5
- Django REST Framework
- Djoser (JWT Authentication & email verification)
- django-filter
- drf-yasg (Swagger / Redoc)
- PostgreSQL
- Django Debug Toolbar (development)

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip (or pipenv/poetry)

### Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/byte_feast.git
cd byte_feast

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root with:

```env
SECRET_KEY=<your_django_secret_key>
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Email settings for Djoser
EMAIL_BACKEND=smtp
EMAIL_HOST=smtp.gmail.com
EMAIL_USE_TLS=True
EMAIL_PORT=587
EMAIL_HOST_USER=<your_email>
EMAIL_HOST_PASSWORD=<your_email_password>
```

### Database Migrations

```bash
# Apply migrations
django-admin migrate
```

### Running the Server

```bash
# Start development server
django-admin runserver
```

Browse the API root at `http://127.0.0.1:8000/api/v1/` and Swagger docs at `http://127.0.0.1:8000/swagger/`.

---

## API Endpoints

### Authentication

- `POST /auth/jwt/create/` & `POST /auth/jwt/refresh/`
- `POST /auth/users/` (register)
- `POST /auth/users/activation/`
- `POST /auth/users/reset_password/` etc.

### Menu

- `GET /api/v1/categories/`
- `GET /api/v1/foods/`
- Filtering: `?category_id=`, `?price__lt=`, `?is_special=`
- Search: `?search=`; Ordering: `?ordering=`

### Cart

- `POST /api/v1/carts/` (create)
- `GET /api/v1/carts/me/`
- `DELETE /api/v1/carts/{cart_id}/`
- `POST /api/v1/carts/{cart_id}/items/`
- `PATCH /api/v1/carts/{cart_id}/items/{item_id}/`
- `DELETE /api/v1/carts/{cart_id}/items/{item_id}/`

### Orders

- `POST /api/v1/orders/` (create from cart)
- `GET /api/v1/orders/` (list user orders)
- `GET /api/v1/orders/{order_id}/`
- `DELETE /api/v1/orders/{order_id}/` (admin only)
- `POST /api/v1/orders/{order_id}/cancel/`
- `PATCH /api/v1/orders/{order_id}/` (admin status update)

### Reviews

- `GET /api/v1/foods/{food_id}/reviews/`
- `POST /api/v1/foods/{food_id}/reviews/`
- `PATCH /api/v1/foods/{food_id}/reviews/{review_id}/`
- `DELETE /api/v1/foods/{food_id}/reviews/{review_id}/`

### Analytics

- `GET /api/v1/analytics/dashboard/` (admin only)
  - `orders_last_week`, `mostly_liked_foods`, `trending_foods`

---

## Testing

```bash
# Run Django tests
pytest  # if using pytest
# or
python manage.py test
```

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m "feat: add ..."`)
4. Push to branch (`git push origin feature/my-feature`)
5. Open a Pull Request

---

## Deployment

For deployment instructions, refer to the [DEPLOYMENT.md](DEPLOYMENT.md) file.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Mahamud Hasan**
Northern University Bangladesh

See [About_Me](About_Author.md) for details about the author.

---
