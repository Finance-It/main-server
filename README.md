# Finance-It Main server

Main server for managing all the services in the project.


## Prerequisites

This project is built on top of docker containers. So ensure that you have
Docker and Docker Compose installed on your system For installation
instructions refer: https://docs.docker.com/install/


## Starting the Server

Start PostgreSQL and Redis first:
```sh
docker-compose up -d db redis
```
Then start whole project:
```
docker-compose up
```

## Execute Commands

To execute any commands inside django docker container, follow this format:

```
docker-compose run app sh -c "command here"
```

### Examples

* Create Super User: 

    `docker-compose run app sh -c "python manage.py create superuser"`
* Add New App: 

    `docker-compose run app sh -c "python manage.py startapp polls"`

## API Documentation
API documentation is done using swagger visit **`/swagger`** for API documentation
It is also hosted at https://api.financeit.cf/swagger

## System Architecture

![System Architecture](https://github.com/Finance-It/Finance-It/raw/main/assets/arch.png)

