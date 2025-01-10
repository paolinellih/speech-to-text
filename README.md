project-root/
│
├── api/ # API Layer (handles HTTP requests)
│ ├── api.py # FastAPI entry point
│ ├── routes/ # Route handlers
│ ├── dependencies/ # Dependencies (auth, etc.)
│ └── **init**.py
│
├── application/ # Application layer (business logic)
│ ├── services/ # Business logic (user registration, etc.)
│ ├── **init**.py
│
├── domain/ # Domain layer (models, schemas, etc.)
│ ├── models/ # Domain models
│ ├── schemas/ # Pydantic schemas
│ └── **init**.py
│
├── infrastructure/ # Infrastructure layer (database, external services)
│ ├── database/ # Database connection and setup
│ ├── **init**.py
│
├── utils/ # Utility functions (hashing, email, etc.)
│ ├── **init**.py
│
├── tests/ # Unit and integration tests
│
├── .env # Environment variables
├── requirements.txt # Project dependencies
├── main.py # Main entry point for FastAPI
└── README.md # Documentation
