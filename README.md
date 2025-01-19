# Speech-to-Text API

![Henrique Paolinelli - Speech to text](https://raw.githubusercontent.com/paolinellih/speech-to-text/refs/heads/main/speech-to-text.webp)

The **Speech-to-Text API** is a Python-based RESTful API built using **FastAPI**, following **Clean Architecture** principles and adhering to **SOLID** principles. The API provides functionality to convert speech (audio) to text and allows user registration, email verification, and password change functionalities.

```bash
speech-to-text-api/
├── api/
│   └── routes/          # FastAPI routes for API endpoints
├── domain/              # Domain models, repositories, services
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── repositories/
├── application/         # Use cases (business logic)
├── utils/               # Utility functions (e.g., hashing, email sending)
├── tests/               # Unit tests
├── Dockerfile           # Dockerfile to build the app container
├── docker-compose.yml   # Docker Compose configuration
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables for Docker
└── README.md            # Project documentation

```

The core objective of this project is to provide an API that accepts audio files, converts speech to text, and returns the transcription through the `/speech_to_text` endpoint. The application also supports user management, including authentication features like email validation and password changes.

## Features

- **Speech-to-Text**: Upload an audio file and receive a transcription of what was said.
- **User Registration**: Users can register with a username, email, and password.
- **Email Validation**: After registration, a confirmation email is sent to the user with a verification link.
- **Password Change**: Users can change their passwords via a secure endpoint.

This API uses **Clean Architecture** to structure the project, ensuring separation of concerns and promoting maintainable, testable, and extensible code. **Dependency Injection (DI)** and **Mocking** are used for unit testing to ensure a high level of test coverage and code reliability.

## Technologies Used

- **Python 3.9**
- **FastAPI**: For building the RESTful API.
- **SQLAlchemy**: For ORM and database interactions.
- **PostgreSQL**: Database used for storing user data and transcripts.
- **Pydantic**: Data validation using Pydantic models.
- **Uvicorn**: ASGI server for serving the FastAPI app.
- **Docker**: To containerize the application for easy deployment.
- **pytest**: For unit testing and mocking.

## Requirements

All required Python dependencies are listed in the `requirements.txt` file. The following dependencies will be installed automatically when you build the Docker container:

- `fastapi`
- `sqlalchemy`
- `psycopg2` (PostgreSQL adapter)
- `pydantic`
- `uvicorn`
- `pytest`
- `email-validator`
- `python-dotenv`
- Other necessary libraries.

## Running the Project with Docker

Follow the steps below to set up and run the project using Docker.

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/speech-to-text-api.git
cd speech-to-text-api
```

### Step 2: Configure Environment Variables

Create a .env file in the root of the project with the following variables (change the variables as you want):

```bash
DATABASE_URL=postgresql://tinit:password@postgres:5432/speech_to_text
DB_USER=tinit
DB_PASSWORD=password
DB_NAME=speech_to_text

ENCRYPTION_KEY=1your2encryption3key=

# If you going to use gmail SMTP read it https://support.google.com/mail/answer/185833?hl=en to create your passsword for your APP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=yourgmail@gmail.com
SMTP_PASSWORD=your pass word here

USERS_URL=http://localhost:8000/users
```

Make sure to replace tinit, password, and speech_to_text with your desired PostgreSQL user, password, and database name. Also, yourgmail@gmail.com and "your pass word here" for your SMTP settings.
To generate your encryption key and replace ENCRYPTION_KEY=1your2encryption3key=, run Windows PowerShell as Administrator and paste this code there:

```bash
# Generate 32 random bytes
$randomBytes = New-Object byte[] 32
[System.Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($randomBytes)

# Encode the bytes into a Base64 string
$encryptionKey = [Convert]::ToBase64String($randomBytes)

# URL-safe Base64 (optional)
$encryptionKey = $encryptionKey -replace '\+', '-' -replace '/', '_'

# Print the key
Write-Output "ENCRYPTION_KEY=$encryptionKey"
```

### Step 3: Build the Docker Containers

Run the following command to build the Docker containers:

```bash
docker-compose up --build
```

This will:

Build the app container with all dependencies installed from `requirements.txt`.
Set up the PostgreSQL container.
Start both containers and expose the API on port `8000`.

### Step 4: Access the API

After the containers are up, you can access the API at `http://localhost:8000/docs`. The API will be available through Swagger UI for testing all endpoints.

You can use Postman and create a `POST` request to the URL:

```bash
[http://localhost:8000/users/register
```

Then create the Request Body (in JSON format):

```bash
{
  "username": "testuser",
  "email": "testuser@example.com",
  "password": "securepassword"
}
```

After sending the request, you should receive a response that includes the user details.

License
This project is licensed under the MIT License - see the [LICENSE](https://mit-license.org/) file for details.

Acknowledgements
Thanks to the FastAPI and SQLAlchemy communities for their contributions.
Special thanks to the open-source contributors who made this project possible.
