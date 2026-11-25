enb

```
cd backend
python -m uvicorn app.main:app --reload
```

```
cd frontend
npm run dev
```

login

```
admin@lotusstudio.dev
```

pass

```
Admin123!
```

env mk

backend

```
DATABASE_URL=
SECRET_KEY=
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
SALT_ROUNDS=12
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
ENVIRONMENT=development
DEBUG=true
APP_NAME=Lotus Studio
APP_VERSION=1.0.0
ADMIN_EMAIL=admin@lotusstudio.dev
TOTP_ISSUER=LotusStudio
CSRF_SECRET=
RATE_LIMIT_PER_MINUTE=60
```

other

```
# Lotus Studio Environment
# Backend
BACKEND_PORT=8000
BACKEND_HOST=0.0.0.0

# Frontend
NUXT_PUBLIC_API_BASE=http://localhost:8000
NUXT_PORT=3000

# Database
DATABASE_URL=sqlite:///./lotus_studio.db

# Security
SECRET_KEY=
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# App
APP_NAME=Lotus Studio
APP_VERSION=1.0.0
ENVIRONMENT=development
ADMIN_EMAIL=admin@lotusstudio.dev
```

for dev use hands and DeepSeek v4.1 Flash
