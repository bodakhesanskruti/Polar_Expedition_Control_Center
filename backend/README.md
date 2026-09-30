# Expedition Control Center — Backend

FastAPI backend for the SIH problem statement **Integrated Polar Expedition Logistics and Asset Management System**.

## Modules

- Authentication / JWT
- Expedition planning
- Personnel management
- Cargo registration and tracking
- Inventory and stock transactions
- Personnel GPS locations
- Check-ins
- Alerts
- Emergency SOS / incident response
- Dashboard statistics
- WebSocket live channel

## 1. Create MySQL database

```sql
CREATE DATABASE polar_expedition_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 2. Configure environment

Copy `.env.example` to `.env` and change the MySQL username/password and JWT secret.

## 3. Install

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 4. Run

From the `backend` folder:

```powershell
uvicorn app.main:app --reload
```

API: http://127.0.0.1:8000
Swagger: http://127.0.0.1:8000/docs
Health: http://127.0.0.1:8000/api/health
WebSocket: ws://127.0.0.1:8000/ws/live

The application automatically creates missing tables on startup. It does not delete existing tables.

## Main endpoints

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`
- `GET/POST /api/expeditions`
- `GET/POST /api/personnel`
- `GET/POST /api/cargo`
- `POST /api/cargo/tracking`
- `GET /api/cargo/tracking`
- `GET/POST /api/inventory`
- `POST /api/inventory/{id}/transactions`
- `GET /api/inventory/low-stock`
- `GET /api/locations/live`
- `POST /api/locations/personnel`
- `POST /api/checkins`
- `GET/POST /api/alerts`
- `PATCH /api/alerts/{id}/resolve`
- `POST /api/emergency/sos`
- `POST /api/emergency/incidents/{id}/response`
- `PATCH /api/emergency/incidents/{id}/resolve`
- `GET /api/dashboard/stats`
