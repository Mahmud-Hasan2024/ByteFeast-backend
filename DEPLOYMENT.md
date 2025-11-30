### 📄 `DEPLOYMENT.md`

# 🚀 Deployment Details

## 🌍 Live Links

- **Production:** [(https://byte-feast-react-w8qi.vercel.app/)](https://byte-feast-react-w8qi.vercel.app/)

- **Base API:** [(https://byte-feast-resturant-django-rest-ap.vercel.app/api/v1/)](https://byte-feast-resturant-django-rest-ap.vercel.app/api/v1/)

- **Swagger Documentation:** [(https://byte-feast-resturant-django-rest-ap.vercel.app/swagger/)](https://byte-feast-resturant-django-rest-ap.vercel.app/swagger/)

---

## 👤 Demo Accounts

| Role     | Email                    | Password   |
| -------- | ------------------------ | ---------- |
| Admin    | `admin@gmail.com`        | `kgb12345` |
| Customer | `doveb99651@besaies.com` | `kgb12345` |

Use these credentials to log in and explore the API in Swagger or Postman.

---

## 🧩 API Headers

When calling secure endpoints, include:

```makefile
Authorization: Bearer <your_token>
```

Tokens can be obtained via:

```bash
POST /accounts/login/
```

---

## 🧠 Notes

- Hosted on **Vercel**
- Backend powered by **Django + DRF + Djoser (JWT)**
- Database: **PostgreSQL (Production)**
- Payments: **SSLCommerz Sandbox (Configured)**
- Version: `v1` (Base URL: `/api/v1/`)

---
