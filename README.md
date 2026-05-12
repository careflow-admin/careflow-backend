# CareFlow Backend

Backend FastAPI para CareFlow con autenticacion JWT, registro con OTP y gestion de citas medicas.

## Funcionalidades
- Autenticacion con JWT y flujo de registro via OTP.
- CRUD de usuarios, medicos, especialidades, horarios y citas.
- Envio de correos SMTP para OTP.
- Modelos SQLAlchemy con base SQLite por defecto.

## Inicio rapido
### Crear entorno virtual
```bash
python -m venv venv
.\venv\Scripts\activate
```

### Instalar dependencias
```bash
pip install fastapi uvicorn sqlalchemy pydantic python-dotenv email-validator
```

### Variables de entorno
```bash
DATABASE_URL=sqlite:///./careflow.db
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=tu_usuario
SMTP_PASSWORD=tu_password
SMTP_FROM_EMAIL=tu_correo
SMTP_FROM_NAME=CareFlow
SMTP_USE_TLS=true
SMTP_TIMEOUT=20
JWT_SECRET=change-me
JWT_ALGORITHM=HS256
JWT_EXPIRES_MINUTES=60
```

### Ejecutar
```bash
uvicorn app.main:app --reload
```

Notas:
- Las tablas se crean automaticamente al iniciar la app.
- La documentacion OpenAPI esta disponible en `/docs`.

## Flujo de autenticacion (OTP + JWT)
1. `POST /auth/registro/validar` verifica la identificacion.
2. `POST /auth/registro/consulta` envia OTP y retorna `expira_en`.
3. `POST /auth/otp/verificar` valida OTP y entrega `access_token`.
4. `POST /auth/otp/set-password` registra la contrasena.
5. `POST /auth/login` entrega `access_token` para sesiones posteriores.
6. En endpoints protegidos usar `Authorization: Bearer <token>`.

## Documentacion
- Mapa de endpoints con ejemplos: docs/api.md
- Diagrama de datos (Mermaid): docs/data-model.md

## Tests
```bash
python -m unittest
```
