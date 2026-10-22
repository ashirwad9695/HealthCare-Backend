# Healthcare Backend API

A RESTful backend system for a healthcare application built with **Django**, **Django REST Framework (DRF)**, **PostgreSQL**, and **JWT Authentication** (`djangorestframework-simplejwt`).

The system enables secure user registration, token-based authentication, patient record management, doctor registry, and flexible patient-doctor assignments.

---

## 🚀 Features

- **JWT Authentication**: Secure user registration and login using industry-standard JWT tokens with token refresh capabilities.
- **Patient Management**: Multi-tenant patient record management with strict user-ownership permissions (users retrieve and manage patients they created).
- **Doctor Management**: Comprehensive doctor registry tracking specialization, experience, hospital affiliations, and contact details.
- **Patient-Doctor Mapping**: Assign doctors to patients, view doctors assigned to a specific patient, list all mappings, and unassign doctors.
- **Error Handling & Validation**: Centralized exception handler providing consistent, descriptive JSON error structures across all HTTP status codes (400, 401, 403, 404, 500).
- **Interactive API Documentation**: OpenAPI 3.0 specification with interactive **Swagger UI** (`/api/docs/`) and **Redoc** (`/api/redoc/`).
- **Postman Collection**: Pre-configured JSON collection (`Healthcare_Backend_API.postman_collection.json`) with automated token capture scripts.
- **PostgreSQL & Docker Ready**: Fully configured for PostgreSQL with environment variables, plus SQLite dev fallback and a ready-to-run `docker-compose.yml`.

---

## 🛠 Tech Stack

- **Framework**: Django 6.x
- **API Engine**: Django REST Framework (DRF)
- **Authentication**: `djangorestframework-simplejwt`
- **Database**: PostgreSQL (psycopg2-binary) / SQLite fallback
- **API Documentation**: `drf-spectacular` (OpenAPI 3.0 / Swagger UI)
- **Environment Management**: `python-dotenv`
- **Cross-Origin Handling**: `django-cors-headers`

---

## 📁 Project Structure

```text
Healthcare Backend/
├── authentication/             # User model, Auth serializers, Register & Login views
├── patients/                   # Patient model, owner-restricted CRUD APIs
├── doctors/                    # Doctor model and CRUD APIs
├── mappings/                   # Patient-Doctor Mapping model & APIs
├── healthcare_backend/         # Core settings, URL routing, custom exception handler
├── tests/                      # Automated test suite covering all endpoints
├── docker-compose.yml          # PostgreSQL container definition
├── Healthcare_Backend_API.postman_collection.json  # Importable Postman collection
├── seed_data.py                # Pre-populates sample doctors, patients, mappings & users
├── requirements.txt            # Python package requirements
├── .env.example                # Template for environment variables
├── .env                        # Active environment configurations
└── manage.py                   # Django management entry point
```

---

## ⚡ Quick Start & Running the Backend

### 1. Prerequisites
- Python 3.10+
- (Optional) Docker or PostgreSQL installed

### 2. Environment Setup
The virtual environment is located at `venv/`:
```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Linux / macOS
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Database Configuration
Edit your `.env` file:
```dotenv
# To run with PostgreSQL:
USE_SQLITE=False
DB_ENGINE=django.db.backends.postgresql
DB_NAME=healthcare_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Or to run with SQLite locally:
USE_SQLITE=True
```

To run PostgreSQL with Docker:
```bash
docker-compose up -d
```

### 4. Apply Migrations & Seed Sample Data
```bash
python manage.py migrate
python seed_data.py
```

### 5. Start the Development Server
```bash
python manage.py runserver
```
The server will start at: `http://127.0.0.1:8000/`

---

## 📖 API Documentation & Interactive UI

Once the server is running, explore and test the endpoints directly in your browser:

- **Swagger UI**: [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
- **Redoc UI**: [http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/)
- **OpenAPI Schema**: [http://127.0.0.1:8000/api/schema/](http://127.0.0.1:8000/api/schema/)

---

## 🔑 Pre-seeded Test Accounts

| Role | Email | Password |
| :--- | :--- | :--- |
| **Admin User** | `doctor.admin@healthcare.com` | `Admin@12345` |
| **Regular User** | `john.doe@example.com` | `Password@123` |

---

## 📡 API Reference

### 1. Authentication APIs
All protected endpoints require the header:
`Authorization: Bearer <your_access_token>`

#### Register a new user
- **Endpoint**: `POST /api/auth/register/`
- **Request Body**:
```json
{
  "name": "Jane Foster",
  "email": "jane.foster@healthcare.com",
  "password": "SecurePassword@123"
}
```
- **Response** (`201 Created`):
```json
{
  "success": true,
  "message": "User registered successfully.",
  "data": {
    "user": { "id": 3, "name": "Jane Foster", "email": "jane.foster@healthcare.com" },
    "tokens": { "refresh": "...", "access": "..." }
  }
}
```

#### Log in a user
- **Endpoint**: `POST /api/auth/login/`
- **Request Body**:
```json
{
  "email": "john.doe@example.com",
  "password": "Password@123"
}
```
- **Response** (`200 OK`):
```json
{
  "success": true,
  "message": "Login successful.",
  "data": {
    "user": { "id": 2, "name": "John Doe", "email": "john.doe@example.com" },
    "tokens": { "refresh": "...", "access": "..." }
  }
}
```

---

### 2. Patient Management APIs

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/patients/` | Add a new patient record (auto-assigns creator) | Yes |
| `GET` | `/api/patients/` | Retrieve all patients created by the authenticated user | Yes |
| `GET` | `/api/patients/<id>/` | Get details of a specific patient | Yes |
| `PUT` | `/api/patients/<id>/` | Update patient details | Yes |
| `DELETE` | `/api/patients/<id>/` | Delete a patient record | Yes |

#### Add Patient Example
- **Endpoint**: `POST /api/patients/`
- **Request Body**:
```json
{
  "name": "Michael Scott",
  "date_of_birth": "1965-03-15",
  "age": 59,
  "gender": "Male",
  "contact_number": "+15551239876",
  "email": "mscott@dundermifflin.com",
  "address": "Scranton, PA",
  "medical_history": "Seasonal allergies."
}
```

---

### 3. Doctor Management APIs

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/doctors/` | Add a new doctor | Yes |
| `GET` | `/api/doctors/` | Retrieve all doctors | Yes |
| `GET` | `/api/doctors/<id>/` | Get details of a specific doctor | Yes |
| `PUT` | `/api/doctors/<id>/` | Update doctor details | Yes |
| `DELETE` | `/api/doctors/<id>/` | Delete a doctor record | Yes |

#### Add Doctor Example
- **Endpoint**: `POST /api/doctors/`
- **Request Body**:
```json
{
  "name": "Cristina Yang",
  "specialization": "Cardiothoracic Surgery",
  "email": "cristina.yang@klausman.ch",
  "phone_number": "+15553334444",
  "years_of_experience": 14,
  "hospital_affiliation": "Klausman Institute",
  "bio": "Expert in complex cardiothoracic interventions."
}
```

---

### 4. Patient-Doctor Mapping APIs

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/mappings/` | Assign a doctor to a patient | Yes |
| `GET` | `/api/mappings/` | Retrieve all patient-doctor mappings | Yes |
| `GET` | `/api/mappings/<patient_id>/` | Get all doctors assigned to a specific patient | Yes |
| `DELETE` | `/api/mappings/<id>/` | Remove a doctor from a patient (mapping ID) | Yes |

#### Assign Doctor Example
- **Endpoint**: `POST /api/mappings/`
- **Request Body**:
```json
{
  "patient": 1,
  "doctor": 2,
  "notes": "Consultation regarding surgical procedure."
}
```

#### Get Doctors for Specific Patient
- **Endpoint**: `GET /api/mappings/1/`
- **Response** (`200 OK`):
```json
{
  "success": true,
  "patient_id": 1,
  "patient_name": "Alice Walker",
  "assigned_doctors_count": 1,
  "data": [
    {
      "mapping_id": 1,
      "assigned_date": "2026-10-22T18:18:27Z",
      "notes": "Patient referred for unexplained respiratory flare-ups.",
      "doctor": {
        "id": 1,
        "name": "Gregory House",
        "specialization": "Diagnostic Medicine & Nephrology",
        "email": "gregory.house@princeton.edu",
        "phone_number": "+15550192834",
        "years_of_experience": 22
      }
    }
  ]
}
```

---

## 🧪 Running Automated Tests

Run the full automated test suite covering all authentication, patient, doctor, and mapping APIs:
```bash
python manage.py test tests
```
Output:
```text
Ran 10 tests in ~0.5s - OK
```

---

## 📮 Postman Collection Setup

1. Open **Postman**.
2. Click **Import** and choose `Healthcare_Backend_API.postman_collection.json`.
3. The collection is pre-configured with the variable `base_url = http://127.0.0.1:8000`.
4. Run the **Login User** or **Register User** request; the test script automatically extracts and stores the JWT `access_token` and `refresh_token` so subsequent requests execute seamlessly without manual copy-pasting!
#   H e a l t h C a r e - B a c k e n d  
 