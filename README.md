# Django DRF authentication using custom user model and OTP codes


## Test project django drf authentication with OTP

## Tools & Services:
- Django & DRF : for building the APIs
- Celery: For running background task (emailing OTP codes)
- Redis: A message broker for celery
- PostgreSQL: Relational DB
- Docker & Docker compose: Containerization

## Possibilities
- Signup new users
- Authenticate a user using email and password
- Authenticate a user using email and OTP code
- Authenticated users can view, updated, delete their profile.


## Clone repo:
```
git clone git@github.com:ASTimch/longev_auth.git
```

## Running locally in docker containers

Create a .env-prod file by copying the example.env-prod provided and run:
```
cd infra
docker-compose up --build

```

### Create superuser

```
sudo docker-compose exec backend python manage.py createsuperuser
```

### Admin panel available at:
```
http://localhost/admin/
```

### Run tests
Run descriptive tests in the container using:
```
docker-compose exec backend python manage.py test
```

### API docs available at:

```
http://localhost/swagger/
http://localhost/redoc/
```

### Shut down containers
```
sudo docker-compose down
```


## Running In a Virtual Env

#### Create a virtual environment using:
```
python -m venv venv
```

#### Activate virtual environment (Linux)
```
    source venv/bin/activate
```
#### Activate virtual environment (windows)
```
    source venv/Scripts/activate
```

#### Install dependencies from requirements.txt:
```
    cd longev_auth
    python -m pip install --upgrade pip
    pip install -r requirements.txt
```
#### Prepare .env file:

Create a .env file by copying the example.env-dev provided

#### Run migrations using:
```
python manage.py makemigrations
python manage.py migrate
```

#### Run tests
Run tests in the environment using:
```
python manage.py test
```

#### Run the server using:
```
python manage.py runserver
```

#### Run celery using:
```
celery -A longev_auth worker -l info
```

### API docs available at:

```
http://localhost:8000/swagger/
http://localhost:8000/redoc/
```
