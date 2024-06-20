# Companies House

## Description
Users can search for their address from the UI and this application will call the Companies House Api and return a table of all companies that are registered under their address. The goal is to help citizens in the UK to fight against fraud.

Relevant info can be found from BBC News - [The leafy street in Leigh-on-Sea that 80 sham firms call home](https://www.bbc.co.uk/news/uk-england-essex-66773673)

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

# Do not upload virtual env folder, authentication.txt. 
# Do not expose your SECRET KEY from Django
git status
git pull 
git add requirements.txt
git commit -m "comment"
git push
```

## Getting Started with the Frontend
```
cd frontend

# Install all dependencies in `package.json`
- Using `npm`:
npm install


- Using `yarn`
yarn install
```

## Running the Development Server
```
- Using `npm`:
npm run dev

- Using `yarn`:
yarn dev

```
This will start the Vite development server, and you can view your application in the browser at [http://localhost:5173](http://localhost:5173)

## Running migrations for PostgreSQL database
If running the version of this repo that connects to a local PostgreSQL database. Then you will first need to install PostgreSQL, create a database, input the database connection details into the backend/backend/settings.py file and then generate migrations for your app, i.e., create the necessary tables in the database.
```
cd backend
python manage.py makemigrations address
python manage.py migrate 
```

## Running the Backend Server
```
cd backend
python manage.py runserver
```
The backend server is starting at [http://127.0.0.1:8000](http://127.0.0.1:8000/)

## Style Guide

We will use pep8 style guide for our naming convention

## Instructions

You will need to create a Companies House account (no cost involved) to get a [developer api key](https://developer.company-information.service.gov.uk/manage-applications) and save this api key in a file called backend/authentication.txt. You will not be able to use this application unless you have your own api key. Please input the following into your backend/authentication.txt file:

```
{
  "api_key": "your-companies-house-api-key"
}
```

The SECRET_KEY from backend/backend/settings.py also needs to be generated. The full instructions are included in the settings.py file.

```
cd backend
python manage.py shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Then place this generated secret key into the SECRET_KEY variable in the backend/backend/settings.py file.

[Companies House API](https://developer-specs.company-information.service.gov.uk/)

[Companies House website: follow links to create an account](https://find-and-update.company-information.service.gov.uk/)

The end goal is to allow users to use this application without having to create a developer account. Users will be able to sign up for alerts by email on a website. They will be notified if any business has been registered at their address without their authorisation.
