# NatHabit Assignment - Backend Developer Task

## Objective

Build a RESTful API for an online bookstore using Django. The API should handle operations related to books, authors, and customers.

## Features

1. **CRUD Operations**:
   - Implement Create, Read, Update, and Delete (CRUD) operations for books, authors, and customers.

2. **Order Placement**:
   - First-time users are eligible for a discount (flat/percentage) controlled from the environment variable or database.
   - Implement an endpoint to place an order, which includes creating a new order, calculating the total amount, and updating the stock of the ordered books.

3. **Authentication & Authorization**:
   - Implement a basic authentication system for authors and customers.
   - Auth systems for customers and authors are separate; customers cannot log into the author system and vice versa.

4. **Search & Filter**:
   - Implement search functionality to find books by title or author.
   - Implement filters for price range and publication date.

## Database

- **Database**: Uses SQLite. (can migrate to Postgresql easily.)

## Installation and Setup

### Prerequisites

- Docker (for containerization)
- Docker Compose (for managing multi-container Docker applications)
- Git (for cloning the repository)

### Clone the Repository

```bash
git clone https://github.com/ugauniyal/NatHabit-Assignment.git
cd NatHabit-Assignment
```

### Build the Docker Image


```bash
docker build -t bookstore-app .
```


### Create a .env file
```bash
DISCOUNT_TYPE=flat  # or percentage
DISCOUNT_VALUE=10    # Discount value
```


### Run The Docker Container

```bash
docker run -p 8000:8000 --env-file .env bookstore-app
```


## Database Setup and Migrations

### SQLite Setup

1. **Apply Migrations**

   Run the following command to apply database migrations and create the necessary tables:

   ```bash
   docker exec -it <container-id> python manage.py migrate
   ```

    Replace \<container-id> with the actual ID or name of your Docker container. This command will create the SQLite database file and apply the migrations to set up the schema.

2. **Create a Superuser**
    
    Create a superuser for accessing the Django admin:

    ```bash
    docker exec -it <container-id> python manage.py createsuperuser
    ```

