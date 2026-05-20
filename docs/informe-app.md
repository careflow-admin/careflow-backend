# Informe de CareFlow backend

## Resumen
Backend en FastAPI para gestion de usuarios, medicos, especialidades, horarios y citas, con autenticacion JWT y flujo de registro por OTP. Incluye envio de correos para OTP y un modelo de datos basado en SQLAlchemy.

## Stack y dependencias
- Framework API: FastAPI
- Servidor ASGI: Uvicorn
- ORM: SQLAlchemy
- Validacion: Pydantic v2
- Carga de variables: python-dotenv
- Validacion de correo: email-validator
- Driver DB adicional: psycopg2-binary (listado en requirements)
- Otros: anyio, starlette, typing-extensions

Listado actual de paquetes (requirements.txt):
- annotated-doc==0.0.4
- annotated-types==0.7.0
- anyio==4.13.0
- click==8.3.2
- colorama==0.4.6
- dnspython==2.8.0
- email-validator==2.3.0
- fastapi==0.136.0
- greenlet==3.4.0
- h11==0.16.0
- idna==3.11
- psycopg2-binary==2.9.11
- pydantic==2.13.2
- pydantic_core==2.46.2
- python-dotenv==1.2.2
- SQLAlchemy==2.0.49
- starlette==1.0.0
- typing-inspection==0.4.2
- typing_extensions==4.15.0
- uvicorn==0.44.0

## Configuracion y variables de entorno
Se cargan variables desde un archivo .env ubicado en app/.env (si existe). Variables usadas:
- DATABASE_URL (por defecto sqlite:///./careflow.db)
- SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD
- SMTP_FROM_EMAIL, SMTP_FROM_NAME
- SMTP_USE_TLS, SMTP_USE_SSL, SMTP_TIMEOUT
- RESEND_API_KEY, RESEND_FROM_EMAIL, RESEND_FROM_NAME, RESEND_TIMEOUT
- GMAIL_API_CLIENT_ID, GMAIL_API_CLIENT_SECRET, GMAIL_API_REFRESH_TOKEN
- GMAIL_API_FROM_EMAIL, GMAIL_API_FROM_NAME, GMAIL_API_TIMEOUT
- JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRES_MINUTES

## Punto de entrada y middleware
- La aplicacion se crea en app/main.py con titulo "CareFlow API".
- CORS habilitado con allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=True.
- Routers incluidos: /usuarios, /auth, /especialidades, /medicos, /citas, /horarios.

## Base de datos y sesion
- session.py crea engine, SessionLocal y Base (SQLAlchemy declarative).
- BaseModel agrega utilidades to_dict() y to_json().
- get_db expone una sesion por request.

## Modelo de datos (tablas principales)
- usuarios: id_usuario, identificacion, nombre, correo, contrasena_hash, rol
- medicos: id_medico, id_usuario, especialidad_id
- especialidades: id_especialidad, nombre
- horarios: id_horario, id_medico, dia, hora_inicio, hora_fin
- citas: id_cita, id_paciente, id_medico, fecha, hora, estado
- otp_codigos: id_otp, id_usuario, codigo, creado_en, expira_en, usado

Enums:
- RolUsuario: paciente | medico | admin
- EstadoCita: pendiente | confirmada | cancelada | rechazada
- DiaSemana: lunes | martes | miercoles | jueves | viernes | sabado | domingo

Relaciones clave:
- Usuario 1-1 Medico (para rol medico)
- Especialidad 1-N Medico
- Medico 1-N Horario y Cita
- Usuario 1-N Cita (como paciente)
- Usuario 1-N OtpCodigo

## Seguridad
- JWT HS256 firmado con JWT_SECRET, con claim exp en minutos.
- get_current_user valida header Authorization: Bearer, decodifica token y busca usuario.
- Hash de contrasena: SHA256 (comentado como reemplazable por hasher mas seguro).

## Autenticacion y OTP
Flujo principal:
1) /auth/registro/validar valida identificacion
2) /auth/registro/consulta genera OTP (TTL 10 min) y envia correo
3) /auth/otp/verificar valida OTP y entrega access_token
4) /auth/otp/set-password guarda contrasena
5) /auth/login autentica y devuelve access_token
6) /auth/me devuelve datos del usuario actual

## Envio de correos
- Prioridad de envio:
  1) Gmail API (si hay configuracion completa)
  2) Resend (si hay RESEND_API_KEY)
  3) SMTP clasico
- send_otp_email compone HTML y texto plano con codigo OTP.
- Manejo de errores con logging y excepciones.

## Endpoints (por modulo)
Auth:
- POST /auth/login
- GET /auth/me
- POST /auth/registro/validar
- POST /auth/registro/consulta
- POST /auth/otp/verificar
- POST /auth/otp/set-password

Usuarios:
- POST /usuarios
- GET /usuarios
- GET /usuarios/{id_usuario}
- PATCH /usuarios/{id_usuario}
- DELETE /usuarios/{id_usuario}

Especialidades:
- POST /especialidades
- GET /especialidades
- GET /especialidades/{id_especialidad}
- PATCH /especialidades/{id_especialidad}
- DELETE /especialidades/{id_especialidad}

Medicos:
- POST /medicos
- GET /medicos
- GET /medicos/{id_medico}
- PATCH /medicos/{id_medico}
- DELETE /medicos/{id_medico}

Horarios:
- POST /horarios
- GET /horarios
- GET /horarios/medico/{id_medico}/disponibilidad
- GET /horarios/{id_horario}
- PATCH /horarios/{id_horario}
- DELETE /horarios/{id_horario}

Citas:
- POST /citas
- GET /citas (filtros opcionales: paciente_id, medico_id)
- GET /citas/mis-citas
- GET /citas/{id_cita}
- PATCH /citas/{id_cita}
- DELETE /citas/{id_cita}

## Servicios (logica de negocio)
- AuthService: validacion de identificacion, OTP, set de contrasena, login.
- UsuarioService: CRUD y validacion de correo unico.
- EspecialidadService: CRUD con validacion de nombre unico.
- MedicoService: valida rol medico, especialidad, evita duplicados.
- HorarioService: valida medico y CRUD.
- CitaService: valida paciente/medico y arma respuesta enriquecida con datos del medico.

## Repositorios (acceso a datos)
- CRUD basico por entidad; CitaRepository usa joinedload para medico/usuario/especialidad.
- OtpRepository invalida OTPs previos y marca como usados.

## Esquemas (Pydantic)
- Base ORM con soporte Pydantic v1/v2.
- DTOs para Auth, Usuario, Medico, Especialidad, Horario, Cita.
- Respuestas de Cita incluyen medico y datos del usuario medico.

## Pruebas
- tests/test_email.py cubre envio SMTP basico, falta de configuracion y envio de OTP.

## Carpetas vacias
- app/auth
- app/interfaces
- app/middlewares

## Notas tecnicas
- Existe una funcion lifespan en app/main.py que no esta conectada al FastAPI(); por eso no se ejecuta automaticamente la carga de .env ni Base.metadata.create_all via lifespan.
- El endpoint PATCH /medicos/{id_medico} no recibe payload en el router, pero el servicio espera un MedicoUpdate.
- El modelo Usuario requiere identificacion, pero el schema UsuarioCreate no la incluye y el servicio no la asigna.
