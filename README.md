# 🚜 Tractor Marketplace — Django Backend

A full marketplace backend for renting and selling tractors across India.

## Tech Stack
- **Django 4.2** + **Django REST Framework**
- **SQLite** (dev) → **PostgreSQL** (production)
- **Razorpay** for payments
- **Token Authentication**

---

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure environment
```bash
cp .env.example .env
# Edit .env with your secret key and DB settings
```

### 3. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create super admin
```bash
python manage.py createsuperuser
# Phone: 9999999999
# Name: Admin
# Password: yourpassword
```

### 5. Run server
```bash
python manage.py runserver
```

### 6. Open admin panel
```
http://localhost:8000/admin/
```

---

## API Endpoints

### Users
| Method | URL | Description |
|--------|-----|-------------|
| POST | `/api/users/register/` | Register (returns token) |
| POST | `/api/users/login/` | Login (returns token) |
| POST | `/api/users/logout/` | Logout |
| GET/PATCH | `/api/users/profile/` | My profile |
| GET | `/api/users/<id>/` | Public profile |
| POST | `/api/users/change-password/` | Change password |

### Tractors
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/tractors/` | List all tractors |
| POST | `/api/tractors/` | Create listing |
| GET | `/api/tractors/<id>/` | Tractor detail |
| PATCH | `/api/tractors/<id>/` | Update listing |
| DELETE | `/api/tractors/<id>/` | Soft-delete |
| GET | `/api/tractors/mine/` | My listings |

**Query params for listing:**
- `?search=mahindra` — search brand/model/location
- `?state=Punjab&district=Ludhiana`
- `?hp_min=35&hp_max=75`
- `?for_rent=true` or `?for_sale=true`

### Bookings
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/bookings/` | My bookings |
| POST | `/api/bookings/` | Create booking |
| GET | `/api/bookings/<id>/` | Booking detail |
| PATCH | `/api/bookings/<id>/status/` | Owner: confirm/complete |
| POST | `/api/bookings/<id>/cancel/` | Farmer: cancel |

### Payments
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/payments/` | My payments |
| POST | `/api/payments/initiate/` | Create Razorpay order |
| POST | `/api/payments/verify/` | Verify payment signature |

### Equipment
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/equipment/` | List equipment |
| POST | `/api/equipment/` | List equipment for rent/sale |
| GET/PATCH/DELETE | `/api/equipment/<id>/` | Detail |

### Reviews
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/reviews/?tractor=<id>` | Reviews for a tractor |
| POST | `/api/reviews/` | Write a review |
| DELETE | `/api/reviews/<id>/` | Delete own review |

---

## Authentication
All protected endpoints require:
```
Authorization: Token <your_token>
```

---

## User Roles
- **farmer** — rents tractors, creates bookings, writes reviews
- **owner** — lists tractors, confirms/completes bookings
- **dealer** — lists tractors for sale
- **admin** — full access via Django admin

---

## Booking Flow
```
Farmer creates booking → PENDING
Owner confirms → CONFIRMED
Farmer pays (Razorpay) → ACTIVE
Owner completes job → COMPLETED
Farmer writes review ✓
```

---

## Switching to PostgreSQL
In `.env`:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=tractor_marketplace
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
```

---

## Next Steps
- [ ] OTP login via SMS (Twilio/MSG91)
- [ ] Push notifications
- [ ] React / React Native frontend
- [ ] Geolocation search (tractors near me)
- [ ] Chat between farmer and owner
- [ ] AI crop advice feature
