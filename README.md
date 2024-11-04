# E-Commerce Project

This is a full-featured eCommerce platform built with Django (Python) that provides core functionality for managing products, user accounts, and an interactive shopping experience. This project can be run both locally and in a Docker environment.

### Running Locally (Django)

Follow these steps to set up and run the project locally on your machine.

#### 1. Clone the Repository

```bash
git clone https://github.com/Maneesh63/Ecommerce-p.git
cd Ecommerce-p
```

#### 2. Create a Virtual Environment

```bash
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Set Up the Database

```bash
python manage.py migrate
```

#### 5. Create a Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to set up an admin username, email, and password.

#### 6. Run the Development Server

```bash
python manage.py runserver
```

Open your browser and go to `http://127.0.0.1:8000` to access the application.

### Running with Docker

If you prefer to run the project in a Docker container, follow these steps.

#### 1. Clone the Repository

```bash
git clone https://github.com/Maneesh63/Ecommerce-p.git
cd Ecommerce-p
```

#### 2. Build and Start the Docker Containers

```bash
docker-compose up --build
```

This command will:

- Build the Docker images for the project.
- Start the Django application in a Docker container.

#### 3. Run Migrations

Once the containers are up, open a new terminal window and run the following command to apply migrations:

```bash
docker-compose exec web python manage.py migrate
```

#### 4. Create a Superuser (Admin Account)

Run the following command to create an admin user:

```bash
docker-compose exec web python manage.py createsuperuser
```

Follow the prompts to set up an admin username, email, and password.

#### 5. Access the Application

- **Frontend**: Open your browser and go to `http://localhost:8000`
- **Admin Panel**: Go to `http://localhost:8000/admin` and log in with the superuser credentials you created.

#### 6. Stopping the Containers

To stop the containers, use:

```bash
docker-compose down
```

## Project Structure

```
Ecommerce-p/
├── common/
├── products/
├── media/
├── root/
├── Dockerfile
├── manage.py
├── docker-compose.yml
├── README.md
└── requirements.txt
```

## Technologies Used

- **Backend**: Django (Python)
- **Database**: SQLite (for local), PostgreSQL (for production)
- **Containerization**: Docker, Docker Compose
- **Frontend**: HTML, CSS, JavaScript (Django templates)

## License

# This project is licensed under the MIT License.

#Steps to run docker container

1 - docker compose build or docker-compose build
2 - docker compose up

#MIGRATIONS

Must follow while migrating ===> Mention app name while make migrations at first else leads to migrations inconsistent issues
Do:
python manage.py makemigrations common

python manage.py migrate common

following "python manage.py migrate" to migrate admin details

#MEDIA
To store images create a media directory gloablly
