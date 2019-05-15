# Library
Application to store book information

Requirements
------------

* **Python**        : 3.4+
* **Django**        : 2.0+
* **DRF**           : 3.8+
* **Docker**        : 18+
* **Postgresql**    : 10+

Database setting
----------------
Before we start installation make sure your postgres installed in your system and it's allow to connect on local ip address.

Method to enable postgresql to access on local ip address.

Locate postgres configuration file in your system.

Set listen_addresses = '*' in postgresql.conf file.

Add following line in pg_hba.conf file.

    host    all             all             0.0.0.0/0               md5

    host    all             all             ::/0                    md5

Restart the postgres server.

Connect postgresql using host ip

    sudo -u postgres psql -h <ip_address>

Create default database called library in psql terminal

    CREATE DATABASE library;

Installation
------------
Installation in local environment. Redirect to project folder

1. Create virtual environment

    python3 -m venv .env

2. Enable environment

    source .env/bin/activate

3. Install dependancies

    pip install -r requirements.txt

4. Configure postgres database configuration in project settings file (library/settings.py)

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'library',
            'USER': '<db_user>',
            'PASSWORD': '<db_password>',
            'HOST': '<host_ip>',
            'PORT': 5432,
        }
    }

5. Run migrations to create default fields and table in database.

    python manage.py migrate

6. Run fixtures to load default user data (OPTIONAL).

    python manage.py loaddata fixtures/user.json

7. Create super user for django admin access (OPTIONAL)

    python manage.py createsuperuser

8. Run server in your local machine

    python manage.py runserver


Installation Using Docker
-------------------------

1. Enable docker service in local system.

    sudo systemctl status docker

2. Redirect to project folder. Build docker image from project using following command

    docker-compose build

3. Once it's done run docker image

    docker-compose up

API documentation
-----------------

API documentation is present in following swagger and redoc link. Swagger also allow the user to try out api by passing request data.

http://<ip_address>/swagger

http://<ip_address>/redoc

There are total 6 api end point

1. http://<ip_address>/register - POST

User registration data 

Header: {
    "content-type": "application/json"}

Example:

Request body:
    {
        "username": "siddhesh",
        "first_name": "siddhesh",
        "last_name": "gore",
        "email": "sidh711@gmail.com",
        "password": "sidh@123"
    }

Response:
    201: {'message': 'User generated successfully'}

2. http://<ip_address>/login - POST

User login detail

Header: {
    "content-type": "application/json"}

Example:

Request body:
    {
        "username": "siddhesh",
        "password": "sidh@123"
    }

Response:
    200: 
        {
            "id": 1,
            "email": "sidh711@gmail.com",
            "first_name": "",
            "last_name": "",
            "authentication_code": "b9388f20fc33cc2b133aa3f46f93808bc3773e79"
        }

3. http://<ip_address>/books - POST

Create book detail

Header: {
    "content-type": "application/json",
    "authorization": "Token 943045a070c4c385064cb91bd8364dfee4b47388"}

Example:

Request body:
    {
        "title": "Two Scoops of Django: Best Practices for Django 1.8",
        "publisher": "Two Scoops Press",
        "author": "Daniel Roy Greenfeld",
        "pages": 532,
        "tags" : ["Python","Development","Django",2017]
    }

Response:
    201:
        {
            "id": 3,
            "title": "Two Scoops of Django: Best Practices for Django 1.8",
            "publisher": "Two Scoops Press",
            "author": "Daniel Roy Greenfeld",
            "pages": 532,
            "tags": [
                "Python",
                "Development",
                "Django",
                2017
            ],
            "created_at": "2019-05-14T23:12:24.909517Z",
            "updated_at": "2019-05-14T23:12:24.909548Z"
        }

4. http://<ip_address>/books?title=<book_name> - GET

Fetch book details

Header: {
    "content-type": "application/json",
    "authorization": "Token 943045a070c4c385064cb91bd8364dfee4b47388"}

Example:

    URL : http://127.0.0.1:8000/books?title=Two%20Scoops%20of%20Django:%20Best%20Practices%20for%20Django%201.8

Response:
    200: 
        {
            "id": 3,
            "title": "Two Scoops of Django: Best Practices for Django 1.8",
            "publisher": "Two Scoops Press",
            "author": "Daniel Roy Greenfeld",
            "pages": 532,
            "tags": [
                "Python",
                "Development",
                "Django",
                2017
            ],
            "created_at": "2019-05-14T23:12:24.909517Z",
            "updated_at": "2019-05-14T23:12:24.909548Z"
        }

4. http://<ip_address>/books?title=<book_name> - DELETE

Delete book detail

Header: {
    "content-type": "application/json",
    "authorization": "Token 943045a070c4c385064cb91bd8364dfee4b47388"}

Example:

    URL : http://127.0.0.1:8000/books?title=Two%20Scoops%20of%20Django:%20Best%20Practices%20for%20Django%201.8

    Method: DELETE

Response:
    204: <empty>

5. http://<ip_address>/books - PUT

Create/Update book detail

If book name is already available then book detail will update and response status is 200. Else it will create new and response status is 201

Header: {
    "content-type": "application/json",
    "authorization": "Token 943045a070c4c385064cb91bd8364dfee4b47388"}

Example:

Request body:
    {
        "title": "Two Scoops of Django: Best Practices for Django 1.8",
        "publisher": "Two Scoops Press",
        "author": "Daniel Roy Greenfeld",
        "pages": 532,
        "tags" : ["Python","Development","Django",2017]
    }

Response:
    200:
        {
            "id": 3,
            "title": "Two Scoops of Django: Best Practices for Django 1.8",
            "publisher": "Two Scoops Press",
            "author": "Daniel Roy Greenfeld",
            "pages": 532,
            "tags": [
                "Python",
                "Development",
                "Django",
                2017
            ],
            "created_at": "2019-05-14T23:12:24.909517Z",
            "updated_at": "2019-05-14T23:12:24.909548Z"
        }


Request body:
    {
        "title": "Two Scoops of Django: Best Practices for Django 1.9",
        "publisher": "Two Scoops Press",
        "author": "Daniel Roy Greenfeld",
        "pages": 532,
        "tags" : ["Python","Development","Django",2017]
    }

Response:
    201:
        {
            "id": 4,
            "title": "Two Scoops of Django: Best Practices for Django 1.9",
            "publisher": "Two Scoops Press",
            "author": "Daniel Roy Greenfeld",
            "pages": 532,
            "tags": [
                "Python",
                "Development",
                "Django",
                2017
            ],
            "created_at": "2019-05-14T23:12:24.909517Z",
            "updated_at": "2019-05-14T23:12:24.909548Z"
        }
