# **Documentation: Flask REST API Project Setup & Run Guide (Docker)**
1. Project Overview
This is a Flask-based REST API project with PostgreSQL as the database. The project is containerized using Docker and supports full CRUD operations on a `Product` model via API endpoints.
2. Install Required Tools
Ensure the following tools are installed on your system:
- Docker
- Docker Compose
- Postman for API testing

3. Project Structure
The project contains:
- Flask application (`app/`)
- Models, routes, and configuration files
- Docker and Docker Compose files for easy deployment

4. Environment Variables
Inside the Docker Compose file, environment variables are defined for the database service:
- DB_HOST: Host name of the DB service (e.g., `db`)
- DB_NAME: Name of the PostgreSQL database
- DB_USER: Username for the DB
- DB_PASS: Password for the DB
These variables are used inside the Flask app to build the SQLAlchemy connection string.

5. Start the Application
Clone git repo
```
git clone https://github.com/speedytech121/ProductMgmtApi.git
```
Create virtual environment (optional if not running with docker)
```
Python -m venv env
```
Activate virtual environment (optional if not running with docker)
```
Windows : ./venv/Scripts/activate
Linux: source ./env/bin/activate
```
Run Docker Desktop Engine First (Make Sure It should be in running stage).
Run the following command to down the running containers if running
```
docker-compose down
```

Run the following command in the project root to start all services:
```
docker-compose up --build
```
This spins up:
- The Flask web service
- A PostgreSQL database container
6. Initialize the Database
After the containers are up, execute the following steps to initialize the database:
1. Get the web container ID:
Open command prompt and run below command to show running containers.
```
docker ps
```
2. Enter into the container:
```
docker exec -it <web_container_id> bash
```
3. Run Python shell and initialize DB tables:
```
python
>>> from app import create_app
>>> from app.models import db
>>> app = create_app()
>>> app.app_context().push()
>>> db.create_all()
>>> exit()
```
7. Verify API is Running
Access the health check endpoint in Postman to ensure everything is working:
```
GET http://localhost:5000/api/health
```
 

8. Test API Endpoints with Postman
Import these endpoints in Postman:
- GET all products:
  `http://localhost:5000/products`
 
- GET single product by ID:
  `http://localhost:5000/products/<id>`
 
- POST new product:
  `http://localhost:5000/products`
  (Include JSON body with product data)
 
- PUT update product:
  `http://localhost:5000/products/<id>`
  (Include updated JSON body)
 
- DELETE product:
  `http://localhost:5000/products/<id>`
 
9. Notes 
- It is portable and works identically across environments due to Docker.
- API routes follow RESTful design principles.
- Error handling is managed via Flask’s built-in mechanisms.
- Database configuration is dynamic via environment variables.
