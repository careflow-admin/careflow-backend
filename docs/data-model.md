# Modelo relacional

Diagrama ER basado en los modelos SQLAlchemy.

```mermaid
erDiagram
    USUARIOS {
        int id_usuario PK
        string nombre
        string identificacion
        string correo
        string contrasena_hash
        string rol
    }

    MEDICOS {
        int id_medico PK
        int id_usuario FK
        int especialidad_id FK
    }

    ESPECIALIDADES {
        int id_especialidad PK
        string nombre
    }

    CITAS {
        int id_cita PK
        int id_paciente FK
        int id_medico FK
        date fecha
        time hora
        string estado
    }

    HORARIOS {
        int id_horario PK
        int id_medico FK
        string dia
        time hora_inicio
        time hora_fin
    }

    HISTORIAL_CLINICO {
        int id_historial PK
        int id_paciente FK
        int id_medico FK
        string motivo
        text diagnostico
        text sintomas
        text observaciones
        text tratamiento
        datetime fecha_creacion
        datetime ultima_actualizacion
    }

    RECETA_MEDICA {
        int id_receta PK
        int id_historial FK
        int id_medicamento FK
        string dosis
        string frecuencia
        string duracion
        text indicaciones
    }

    MEDICAMENTOS {
        int id_medicamento PK
        string nombre
        text descripcion
        int id_tipo_medicamento FK
        string dosis_recomendada
        text contraindicaciones
    }

    TIPOS_MEDICAMENTO {
        int id_tipo_medicamento PK
        string nombre
    }

    OTP_CODIGOS {
        int id_otp PK
        int id_usuario FK
        string codigo
        datetime creado_en
        datetime expira_en
        bool usado
    }

    USUARIOS ||--o| MEDICOS : "usuario"
    ESPECIALIDADES ||--o{ MEDICOS : "especialidad"
    USUARIOS ||--o{ CITAS : "paciente"
    MEDICOS ||--o{ CITAS : "medico"
    MEDICOS ||--o{ HORARIOS : "disponibilidad"
    USUARIOS ||--o{ OTP_CODIGOS : "otp"
    USUARIOS ||--o{ HISTORIAL_CLINICO : "paciente"
    MEDICOS ||--o{ HISTORIAL_CLINICO : "medico"
    HISTORIAL_CLINICO ||--o{ RECETA_MEDICA : "recetas"
    TIPOS_MEDICAMENTO ||--o{ MEDICAMENTOS : "tipo"
    MEDICAMENTOS ||--o{ RECETA_MEDICA : "medicamento"
```

## Tablas y campos

### usuarios
| columna | tipo | PK | FK | notas |
| --- | --- | --- | --- | --- |
| id_usuario | int | si |  |  |
| nombre | string(120) |  |  | not null |
| identificacion | string(20) |  |  | unique, not null |
| correo | string(255) |  |  | unique, not null |
| contrasena_hash | string(255) |  |  | nullable |
| rol | enum |  |  | valores: paciente, medico, admin |

### medicos
| columna | tipo | PK | FK | notas |
| --- | --- | --- | --- | --- |
| id_medico | int | si |  |  |
| id_usuario | int |  | usuarios.id_usuario | unique, not null |
| especialidad_id | int |  | especialidades.id_especialidad | not null |

### especialidades
| columna | tipo | PK | FK | notas |
| --- | --- | --- | --- | --- |
| id_especialidad | int | si |  |  |
| nombre | string(120) |  |  | unique, not null |

### citas
| columna | tipo | PK | FK | notas |
| --- | --- | --- | --- | --- |
| id_cita | int | si |  |  |
| id_paciente | int |  | usuarios.id_usuario | not null |
| id_medico | int |  | medicos.id_medico | not null |
| fecha | date |  |  | not null |
| hora | time |  |  | not null |
| estado | enum |  |  | valores: pendiente, confirmada, cancelada, rechazada |

### horarios
| columna | tipo | PK | FK | notas |
| --- | --- | --- | --- | --- |
| id_horario | int | si |  |  |
| id_medico | int |  | medicos.id_medico | not null |
| dia | enum |  |  | valores: lunes, martes, miercoles, jueves, viernes, sabado, domingo |
| hora_inicio | time |  |  | not null |
| hora_fin | time |  |  | not null |

### historial_clinico
| columna | tipo | PK | FK | notas |
| --- | --- | --- | --- | --- |
| id_historial | int | si |  |  |
| id_paciente | int |  | usuarios.id_usuario | not null |
| id_medico | int |  | medicos.id_medico | not null |
| motivo | string(50) |  |  | not null |
| diagnostico | text |  |  | not null |
| sintomas | text |  |  | not null |
| observaciones | text |  |  | not null |
| tratamiento | text |  |  | not null |
| fecha_creacion | datetime |  |  | default now |
| ultima_actualizacion | datetime |  |  | default now, on update now |

### receta_medica
| columna | tipo | PK | FK | notas |
| --- | --- | --- | --- | --- |
| id_receta | int | si |  |  |
| id_historial | int |  | historial_clinico.id_historial | not null |
| id_medicamento | int |  | medicamentos.id_medicamento | not null |
| dosis | string(120) |  |  | not null |
| frecuencia | string(120) |  |  | not null |
| duracion | string(120) |  |  | not null |
| indicaciones | text |  |  | not null |

### medicamentos
| columna | tipo | PK | FK | notas |
| --- | --- | --- | --- | --- |
| id_medicamento | int | si |  |  |
| nombre | string(120) |  |  | unique, not null |
| descripcion | text |  |  | not null |
| id_tipo_medicamento | int |  | tipos_medicamento.id_tipo_medicamento | not null |
| dosis_recomendada | string(120) |  |  | not null |
| contraindicaciones | text |  |  | not null |

### tipos_medicamento
| columna | tipo | PK | FK | notas |
| --- | --- | --- | --- | --- |
| id_tipo_medicamento | int | si |  |  |
| nombre | string(120) |  |  | unique, not null |

### otp_codigos
| columna | tipo | PK | FK | notas |
| --- | --- | --- | --- | --- |
| id_otp | int | si |  |  |
| id_usuario | int |  | usuarios.id_usuario | not null |
| codigo | string(10) |  |  | not null |
| creado_en | datetime |  |  | default utcnow |
| expira_en | datetime |  |  | not null |
| usado | bool |  |  | default false |

## Enumeraciones
| enum | valores |
| --- | --- |
| RolUsuario | paciente, medico, admin |
| EstadoCita | pendiente, confirmada, cancelada, rechazada |
| DiaSemana | lunes, martes, miercoles, jueves, viernes, sabado, domingo |
