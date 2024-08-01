# Mesob Recipe API

> Mesob Recipe API server built with Django Rest Framework.

### Tools Used
- Django
- Celery
- RabbitMQ
- Docker
- PostgreSQL


### Tasks
- [x] Docker Integration
- [ ] Testing and Coverage Report
- [x] Asynchronous Task Handling with Celery
- [x] Email Queue Implementation
- [x] Logging Framework
- [x] API Improvements
- [ ] Performance Optimization

### Live version link
- API server: http://13.233.99.194:8000
- RabbitMQ Management Console: http://13.233.99.194:15672

### Local Setup
1. Clone the repository
2. Run RabbitMQ and PostgreSQL containers `docker compose up -d rabbitmq pg-db`
3. Run `docker compose up -d --build server` to build the images and run the containers
4. Run `docker exec recipe-server python manage.py migrate` to apply the migrations
5. Run celery worker and beat `docker compose up -d celery-worker celery-beat`