# Banking App

# Technical Specifications
## Backend:
* Python 3.12
* PostgreSQL database
* SQLAlchemy for ORM, Alembic
* Asynchronous programming withFastAPI
# Authentication:
* JWT-based authentication mechanism
# Deployment:
* Use Docker for containerization
* Deploy the application on AWS ECS (Elastic Container Service)
* Ensure the application can scale with user demand
# CI/CD:
* Implement continuous integration and continuous deployment using GitHub Actions

----------------------------------------
# Alembic
## To run migrations 
```docker-compose exec backend alembic upgrade head```
## To create migrations 
```alembic revision --autogenerate -m "name of migration"```