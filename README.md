# Hospital Doctor Appointment Booking

A small learning project built with **Python, FastAPI, MySQL, and Docker**. It lets you register doctors and patients, view available doctors, book appointments, and cancel appointments.

## 1. What happens when a patient books?

```text
Browser / API client
        | HTTP request (JSON)
        v
FastAPI route -> validate request (Pydantic)
        | calls
        v
Appointment service -> checks doctor, patient, and time conflict
        | uses
        v
SQLAlchemy session -> MySQL
```

The route handles HTTP, the schema checks incoming data, the service enforces booking rules, and the database stores records. Docker Compose starts the API and MySQL together.

## 2. Project layout

```text
appointment_booking/
├── app/
│   ├── main.py              # FastAPI app and route registration
│   ├── database.py          # MySQL connection and session
│   ├── models/              # SQLAlchemy database tables
│   ├── schemas/             # Request and response validation
│   ├── routers/             # HTTP endpoints
│   └── services/            # Booking rules
├── docker-compose.yml       # API + MySQL services
├── Dockerfile               # How to package the API
├── requirements.txt
└── .env.example             # Local configuration template
```

## 3. Run it

You need Docker Desktop (or Docker Engine with Compose).

1. Open a terminal in this `appointment_booking` folder.
2. Copy `.env.example` to `.env`. The example values are only for local development; change them before using this anywhere shared or public.
3. Start the containers:

   ```bash
   docker compose up --build
   ```

4. Wait for the API and database startup messages. The API is at `http://localhost:8000`.
5. Open `http://localhost:8000/docs` to try the endpoints interactively.
6. Stop with `Ctrl+C`, then run `docker compose down`. To also remove the local database data, use `docker compose down -v`.

The API waits for MySQL to report healthy before starting. On first launch, SQLAlchemy creates the starter tables automatically.

## 4. Learn the flow by trying it

Use Swagger at `/docs`; create records in this order:

1. **Create a doctor** with `POST /doctors`:

   ```json
   {"name":"Dr. Rao","specialty":"Cardiology","email":"rao@example.test"}
   ```

2. **Create a patient** with `POST /patients`:

   ```json
   {"name":"Asha Kumar","email":"asha@example.test","phone":"555-0101"}
   ```

3. **List doctors** with `GET /doctors` and note the returned doctor ID.
4. **Book an appointment** with `POST /appointments`, using the returned IDs and a future ISO 8601 time:

   ```json
   {"doctor_id":1,"patient_id":1,"starts_at":"2030-05-10T09:30:00","duration_minutes":30,"reason":"Consultation"}
   ```

5. **List appointments** with `GET /appointments?doctor_id=1`.
6. Try booking another appointment with the same doctor for an overlapping time. The API should return HTTP `409 Conflict`.
7. **Cancel** one with `DELETE /appointments/{appointment_id}`. Cancellation keeps the row for history and frees that time slot.

The sample timestamp is deliberately future-dated for repeatable demos. In a real service, accept timezone-aware timestamps and store them in UTC.

## 5. Implementation walkthrough

1. `docker-compose.yml` defines two services. MySQL persists its data in a named volume; the API connects to the database using the Compose service name `db`.
2. `app/database.py` builds the SQLAlchemy engine and provides one database session per request.
3. Files in `app/models/` describe the tables and their relationships. An appointment points to one doctor and one patient.
4. Files in `app/schemas/` describe the JSON clients can send and receive. Pydantic rejects invalid values before the service is called.
5. Files in `app/routers/` map HTTP methods and paths to Python functions.
6. `app/services/appointments.py` checks that both records exist and that the doctor has no active appointment with an overlapping interval. It then commits the appointment.
7. `app/main.py` creates the FastAPI application, creates the starter tables, and includes the routers.

## 6. Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/health` | Check API process |
| POST | `/doctors` | Add a doctor |
| GET | `/doctors` | List doctors |
| POST | `/patients` | Add a patient |
| GET | `/patients` | List patients |
| POST | `/appointments` | Book an appointment |
| GET | `/appointments` | List appointments; optionally filter by `doctor_id` or `patient_id` |
| DELETE | `/appointments/{id}` | Cancel an appointment |

## 7. Next steps for learning

- Add doctor working hours and reject bookings outside those hours.
- Add appointment status history and patient authentication.
- Add pagination and search to listing endpoints.
- Add Alembic migrations instead of `create_all` when the schema needs to evolve.
- Add automated tests and a production configuration (secrets, TLS, backups, logging, and monitoring) before real use.

This is an educational starter, not a production-ready hospital system. It does not implement authentication, authorization, audit logging, timezone policy, or healthcare privacy controls.
