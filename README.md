# Companies House

## Description

Users can search for their address from the UI and this application will call the Companies House Api and return a table of all companies that are registered under their address. The goal is to help citizens in the UK to fight against fraud.

Relevant info can be found from BBC News - [The leafy street in Leigh-on-Sea that 80 sham firms call home](https://www.bbc.co.uk/news/uk-england-essex-66773673)

[Demo video](https://youtu.be/l2ga_sPJe08)

## Table of Contents

- [Installation](#installation)
- [Getting Started with the Frontend](#getting-started-with-the-frontend)
- [Running the Development Server](#running-the-development-server)
- [Running the Backend Server](#running-the-backend-server)
- [Style Guide](#style-guide)
- [Instructions](#instructions)

## Installation

```
# Setting up a virtual Environment
python -m venv ch_env

# Activating the virtual Environment
source ch_env/bin/activate

# Installing relevant python packages 
pip install -r requirements.txt

# Saving relevant python packages in requirement
pip freeze > requirements.txt

# Do not upload virtual env folder or the .env file
# Do not expose your SECRET KEY from Django
git status
git pull 
git add requirements.txt
git commit -m "comment"
git push
```

## Prerequisites

```
Docker Engine
Node.js (v22.5.1)
```

## Getting Started with the Frontend

```
cd frontend

# Install all dependencies in `package.json`
- Using `npm`:
npm install

- Using `npm` build your project:
npm run build
```

## Create migrations for the database

You first need to create a database and input the database connection details into the .env file. You then need to generate migrations for your app, i.e., create the necessary tables in the database.

```
cd backend
python manage.py makemigrations address
python manage.py migrate
```

## Running the Backend and Frontend Servers as Docker services

The backend and frontend server code is run in two Docker containers. These containers are built and run as services using a Docker compose YAML file. Make sure that you are at the same level as the `docker-compose.yml` file in the folder structure.

```
# Build the images and start the Docker services:
docker compose up --build -d  # possibly docker-compose

# If you have already built the images and don't need to rebuild any of them then you can use:
docker compose up -d
```

The backend server is located at [http://<HOST_IP>:8000](http://<HOST_IP>:8000). The frontend server is located at [http://<HOST_IP>:3000](http://<HOST_IP>:3000). The host IP could be an EC2 instance, a local host, etc.

```
# To stop and clean up the containers, you can use:
docker compose down
```

## Style Guide

We will use pep8 style guide for our naming convention.

## Instructions

You will need to create a Companies House account (no cost involved) to get a [developer api key](https://developer.company-information.service.gov.uk/manage-applications) and save this api key in the .env file as an environment variable.

```
CH_API_KEY="enter-companies-house-api-key"
```

The SECRET_KEY can be generated in backend/backend/settings.py and then entered into the .env file as an environment variable. The full instructions are included in the settings.py file.

```
cd backend
python manage.py shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

[Companies House API](https://developer-specs.company-information.service.gov.uk/)

[Companies House website: follow links to create an account](https://find-and-update.company-information.service.gov.uk/)

The end goal is to allow users to use this application without having to create a developer account. Users will be able to sign up for alerts by email on a website. They will be notified if any business has been registered at their address without their authorisation.
