# Documentación del backend de Mergington High School API

## Finalidad del proyecto
Este proyecto provee un backend FastAPI para gestionar actividades extracurriculares de una escuela (Mergington High School). Los usuarios pueden:
- Obtener la lista de actividades (`GET /activities`)
- Inscribirse en una actividad (`POST /activities/{activity_name}/signup?email=...`)
- Eliminar participantes de una actividad (`DELETE /activities/{activity_name}/participants/{email}`)

El objetivo es demostrar un API REST simple con estado en memoria y una interfaz web estática.

---

## Documentación de funciones en `src/app.py`

### `root()`
- Endpoint: `GET /`
- Retorna un `RedirectResponse` hacia `/static/index.html` para servir la página de UI.

### `get_activities()`
- Endpoint: `GET /activities`
- Retorna el diccionario global `activities` con actividades, descripciones, horarios, límite y participantes.

### `signup_for_activity(activity_name: str, email: str)`
- Endpoint: `POST /activities/{activity_name}/signup`
- Parámetros: `activity_name` (ruta), `email` (query)
- Comportamiento:
  - Verifica que la actividad exista.
  - Rechaza duplicados de inscripción con 400.
  - Rechaza si ya alcanzó `max_participants` con 400.
  - Agrega el email a la lista de participantes y retorna mensaje de éxito.

### `remove_participant(activity_name: str, email: str)`
- Endpoint: `DELETE /activities/{activity_name}/participants/{email}`
- Parámetros: `activity_name` y `email` (ruta)
- Comportamiento:
  - Verifica que la actividad exista.
  - Verifica que el participante exista en la lista.
  - Lo remueve y retorna mensaje de éxito.

---

## Diagrama de flujo de la app (Mermaid)

```mermaid
flowchart TD
    A[Inicio: petición entrante] --> B{Ruta de petición}
    B -->|GET /| C[Redirect a /static/index.html]
    B -->|GET /activities| D[Retorna `activities` como JSON]
    B -->|POST /activities/{activity}/signup| E[Chequear actividad]
    E -->|No existe| F[HTTP 404 Activity not found]
    E -->|Existe| G[Chequear duplicado]
    G -->|Duplicado| H[HTTP 400 Student is already signed up]
    G -->|No duplicado| I[Chequear cupo]
    I -->|Lleno| J[HTTP 400 Activity is full]
    I -->|Disponible| K[Agregar email y HTTP 200 success]
    B -->|DELETE /activities/{activity}/participants/{email}| L[Chequear actividad]
    L -->|No existe| F
    L -->|Existe| M[Chequear participante]
    M -->|No existe| N[HTTP 404 Participant not found]
    M -->|Existe| O[Remover y HTTP 200 success]
```

---

## Patrón AAA en las pruebas
Cada prueba de `tests/backend/test_activities.py` sigue:
1. Arrange: preparar datos/fixture
2. Act: llamar endpoint (TestClient)
3. Assert: verificar status, respuesta y estado mutado de `activities`

---

## Cómo ejecutar pruebas
1. `pip install -r requirements.txt`
2. `pytest tests/backend/`
3. `pytest`
