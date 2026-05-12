# API Endpoints

Base URL: `/`

Todos los endpoints salvo `/auth/*` requieren header:
```
Authorization: Bearer <token>
```

## Enums
- `rol`: `paciente` | `medico` | `admin`
- `estado`: `pendiente` | `confirmada` | `cancelada` | `rechazada`
- `dia`: `lunes` | `martes` | `miercoles` | `jueves` | `viernes` | `sabado` | `domingo`

## Auth
### POST /auth/login
Request:
```json
{
  "identificacion": "1234567890",
  "contrasena": "Secret123"
}
```
Response:
```json
{
  "access_token": "<jwt>",
  "token_type": "bearer",
  "usuario": {
    "id_usuario": 1,
    "nombre": "Juan Perez",
    "correo": "juan@example.com",
    "rol": "paciente"
  }
}
```

### GET /auth/me
Response:
```json
{
  "id_usuario": 1,
  "nombre": "Juan Perez",
  "correo": "juan@example.com",
  "rol": "paciente"
}
```

### POST /auth/registro/validar
Request:
```json
{
  "identificacion": "1234567890"
}
```
Response:
```json
{
  "message": "Identificacion valida.",
  "correo": "juan@example.com"
}
```

### POST /auth/registro/consulta
Request:
```json
{
  "identificacion": "1234567890"
}
```
Response:
```json
{
  "message": "OTP enviado.",
  "correo": "juan@example.com",
  "expira_en": "2026-05-04T12:00:00"
}
```

### POST /auth/otp/verificar
Request:
```json
{
  "identificacion": "1234567890",
  "codigo": "123456"
}
```
Response:
```json
{
  "message": "OTP valido.",
  "expira_en": "2026-05-04T12:00:00",
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

### POST /auth/otp/set-password
Request:
```json
{
  "identificacion": "1234567890",
  "codigo": "123456",
  "contrasena": "Secret123"
}
```
Response:
```json
{
  "message": "Contrasena actualizada."
}
```

## Usuarios
### POST /usuarios
Request:
```json
{
  "nombre": "Ana Ruiz",
  "correo": "ana@example.com",
  "rol": "paciente",
  "contrasena": "Secret123"
}
```
Response:
```json
{
  "id_usuario": 2,
  "nombre": "Ana Ruiz",
  "correo": "ana@example.com",
  "rol": "paciente"
}
```

### GET /usuarios
Response:
```json
[
  {
    "id_usuario": 1,
    "nombre": "Juan Perez",
    "correo": "juan@example.com",
    "rol": "paciente"
  }
]
```

### GET /usuarios/{id_usuario}
Response:
```json
{
  "id_usuario": 1,
  "nombre": "Juan Perez",
  "correo": "juan@example.com",
  "rol": "paciente"
}
```

### PATCH /usuarios/{id_usuario}
Request (campos opcionales):
```json
{
  "nombre": "Juan P.",
  "correo": "juan.p@example.com",
  "rol": "paciente",
  "contrasena": "Nuevo123"
}
```
Response:
```json
{
  "id_usuario": 1,
  "nombre": "Juan P.",
  "correo": "juan.p@example.com",
  "rol": "paciente"
}
```

### DELETE /usuarios/{id_usuario}
Response: `204 No Content`

## Especialidades
### POST /especialidades
Request:
```json
{
  "nombre": "Cardiologia"
}
```
Response:
```json
{
  "id_especialidad": 1,
  "nombre": "Cardiologia"
}
```

### GET /especialidades
Response:
```json
[
  {
    "id_especialidad": 1,
    "nombre": "Cardiologia"
  }
]
```

### GET /especialidades/{id_especialidad}
Response:
```json
{
  "id_especialidad": 1,
  "nombre": "Cardiologia"
}
```

### PATCH /especialidades/{id_especialidad}
Request:
```json
{
  "nombre": "Cardiologia Pediatrica"
}
```
Response:
```json
{
  "id_especialidad": 1,
  "nombre": "Cardiologia Pediatrica"
}
```

### DELETE /especialidades/{id_especialidad}
Response: `204 No Content`

## Medicos
### POST /medicos
Request:
```json
{
  "id_usuario": 3,
  "especialidad_id": 1
}
```
Response:
```json
{
  "id_medico": 1,
  "id_usuario": 3,
  "especialidad_id": 1
}
```

### GET /medicos
Response:
```json
[
  {
    "id_medico": 1,
    "id_usuario": 3,
    "especialidad_id": 1,
    "especialidad": "Cardiologia",
    "data": {
      "nombre": "Dra. Lopez",
      "rol": "medico"
    }
  }
]
```

### GET /medicos/{id_medico}
Response:
```json
{
  "id_medico": 1,
  "id_usuario": 3,
  "especialidad_id": 1,
  "especialidad": "Cardiologia",
  "data": {
    "nombre": "Dra. Lopez",
    "rol": "medico"
  }
}
```

### PATCH /medicos/{id_medico}
Request (campos opcionales):
```json
{
  "id_usuario": 3,
  "especialidad_id": 2
}
```
Response:
```json
{
  "id_medico": 1,
  "id_usuario": 3,
  "especialidad_id": 2
}
```

### DELETE /medicos/{id_medico}
Response: `204 No Content`

## Horarios
### POST /horarios
Request:
```json
{
  "id_medico": 1,
  "dia": "lunes",
  "hora_inicio": "09:00:00",
  "hora_fin": "12:00:00"
}
```
Response:
```json
{
  "id_horario": 1,
  "id_medico": 1,
  "dia": "lunes",
  "hora_inicio": "09:00:00",
  "hora_fin": "12:00:00"
}
```

### GET /horarios
Response:
```json
[
  {
    "id_horario": 1,
    "id_medico": 1,
    "dia": "lunes",
    "hora_inicio": "09:00:00",
    "hora_fin": "12:00:00"
  }
]
```

### GET /horarios/medico/{id_medico}/disponibilidad
Response:
```json
[
  {
    "id_horario": 1,
    "id_medico": 1,
    "dia": "lunes",
    "hora_inicio": "09:00:00",
    "hora_fin": "12:00:00"
  }
]
```

### GET /horarios/{id_horario}
Response:
```json
{
  "id_horario": 1,
  "id_medico": 1,
  "dia": "lunes",
  "hora_inicio": "09:00:00",
  "hora_fin": "12:00:00"
}
```

### PATCH /horarios/{id_horario}
Request (campos opcionales):
```json
{
  "dia": "martes",
  "hora_inicio": "10:00:00",
  "hora_fin": "13:00:00"
}
```
Response:
```json
{
  "id_horario": 1,
  "id_medico": 1,
  "dia": "martes",
  "hora_inicio": "10:00:00",
  "hora_fin": "13:00:00"
}
```

### DELETE /horarios/{id_horario}
Response: `204 No Content`

## Citas
### POST /citas
Request:
```json
{
  "id_paciente": 4,
  "id_medico": 1,
  "fecha": "2026-05-04",
  "hora": "09:30:00",
  "estado": "pendiente"
}
```
Response:
```json
{
  "id_cita": 1,
  "id_paciente": 4,
  "id_medico": 1,
  "fecha": "2026-05-04",
  "hora": "09:30:00",
  "estado": "pendiente",
  "medico": {
    "id_medico": 1,
    "id_usuario": 3,
    "especialidad_id": 1,
    "especialidad": "Cardiologia",
    "data": {
      "nombre": "Dra. Lopez",
      "rol": "medico"
    }
  }
}
```

### GET /citas
Query params opcionales: `paciente_id`, `medico_id`
Response:
```json
[
  {
    "id_cita": 1,
    "id_paciente": 4,
    "id_medico": 1,
    "fecha": "2026-05-04",
    "hora": "09:30:00",
    "estado": "pendiente",
    "medico": {
      "id_medico": 1,
      "id_usuario": 3,
      "especialidad_id": 1,
      "especialidad": "Cardiologia",
      "data": {
        "nombre": "Dra. Lopez",
        "rol": "medico"
      }
    }
  }
]
```

### GET /citas/mis-citas
Response:
```json
[
  {
    "id_cita": 1,
    "id_paciente": 4,
    "id_medico": 1,
    "fecha": "2026-05-04",
    "hora": "09:30:00",
    "estado": "pendiente",
    "medico": {
      "id_medico": 1,
      "id_usuario": 3,
      "especialidad_id": 1,
      "especialidad": "Cardiologia",
      "data": {
        "nombre": "Dra. Lopez",
        "rol": "medico"
      }
    }
  }
]
```

### GET /citas/{id_cita}
Response:
```json
{
  "id_cita": 1,
  "id_paciente": 4,
  "id_medico": 1,
  "fecha": "2026-05-04",
  "hora": "09:30:00",
  "estado": "pendiente",
  "medico": {
    "id_medico": 1,
    "id_usuario": 3,
    "especialidad_id": 1,
    "especialidad": "Cardiologia",
    "data": {
      "nombre": "Dra. Lopez",
      "rol": "medico"
    }
  }
}
```

### PATCH /citas/{id_cita}
Request (campos opcionales):
```json
{
  "estado": "confirmada"
}
```
Response:
```json
{
  "id_cita": 1,
  "id_paciente": 4,
  "id_medico": 1,
  "fecha": "2026-05-04",
  "hora": "09:30:00",
  "estado": "confirmada",
  "medico": {
    "id_medico": 1,
    "id_usuario": 3,
    "especialidad_id": 1,
    "especialidad": "Cardiologia",
    "data": {
      "nombre": "Dra. Lopez",
      "rol": "medico"
    }
  }
}
```

### DELETE /citas/{id_cita}
Response: `204 No Content`
