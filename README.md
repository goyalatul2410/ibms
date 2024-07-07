
# Intelligent Book Management System

## Overview
This project is an Intelligent Book Management System developed using FastAPI. The system allows users to add, retrieve, update, and delete books from a PostgreSQL database. It also manages user reviews and generates rating and review summaries for books. The system is accessible via a RESTful API and is designed to be deployed on AWS.

## Features
1. **Database Setup:**
   - Uses PostgreSQL to store book information.
   - `books` table with fields: `id`, `title`, `author`, `genre`, `year_published`, `summary`.
   - `reviews` table with fields: `id`, `book_id`, `user_id`, `review_text`, `rating`.

2. **RESTful API Endpoints:**
   - `POST /books`: Add a new book.
   - `GET /books`: Retrieve all books.
   - `GET /books/{id}`: Retrieve a specific book by its ID.
   - `PUT /books/{id}`: Update a book's information by its ID.
   - `DELETE /books/{id}`: Delete a book by its ID.
   - `POST /books/{id}/reviews`: Add a review for a book.
   - `GET /books/{id}/reviews`: Retrieve all reviews for a book.
   - `GET /books/{id}/summary`: Get a summary and aggregated rating for a book.
   - `POST /generate-summary`: Generate a summary for a given book content.

3   **AWS Deployment:**
   - Application is designed to be deployed on AWS using services such as EC2, Lambda, or ECS.
   - PostgreSQL database hosted on AWS RDS.
   - AWS S3 used for storing any model files if necessary.
   - CI/CD pipeline set up for automatic deployment.

4   **Authentication and Security:**
   - Basic authentication for the API.
   - Secure communication with the database and API endpoints.

5   **Bonus:**
   - Caching for the book information.
   - Unit and integration tests for the API endpoints.

## Project Structure
```
project/
├── app/
│   ├── __init__.py
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── routers/
│   │   ├── __init__.py
│   │   └── books.py
│   ├── schemas.py
│   └── middleware.py
├── tests/
│   ├── __init__.py
│   ├── test_crud.py
│   └── test_main.py
├── alembic/
│   ├── versions/
│   ├── env.py
│   ├── script.py.mako
│   └── README
├── .env
├── alembic.ini
├── Dockerfile
├── requirements.txt
└── README.md
```

## Setup and Installation
1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd project
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**
   - Create a PostgreSQL database.
   - Update the database URL in `app/database.py`.

5. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```

6. **Run the application:**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Running Tests
To run the tests, use the following command:
```bash
pytest
```

## Deployment on AWS
1. **Set up an AWS account and configure AWS CLI.**
2. **Create and configure AWS services:**
   - EC2, Lambda, or ECS for the application.
   - RDS for the PostgreSQL database.
   - S3 for storing model files if necessary.
3. **Set up a CI/CD pipeline using services like AWS CodePipeline, GitHub Actions, or GitLab CI.**

## Documentation
The API documentation is available at `/docs` when the application is running.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.

## License
This project is licensed under the MIT License.
