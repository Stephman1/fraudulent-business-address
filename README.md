# Companies House
Companies House data project by Stephen and Ashika.

## Description
User can search for their address from the UI and this application will call the companies house Api and
return a table of all companies that is registered under their addresss. The goal is to help citizens in
the UK to fight against crimes. 
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

## Running the Backend Server
```
cd backend
python manage.py runserver
```
The backend server is starting at [http://127.0.0.1:8000](http://127.0.0.1:8000/)


## Style Guide

We will use pep8 style guide for our naming convention

## Instructions

Go to retrieval/company_search.py and run the file. You can use either the searchAll or searchAddress functions. The results of the search will be automatically saved in csv files in a data folder that will be created for you. All data is linked by company number, officer number or charge codes. You can modify the search query by inputting any string into the function parameter.

You will need to create a Companies House account (no cost involved), get a [developer api key](https://developer.company-information.service.gov.uk/manage-applications) and save this api key in a file called authentication.txt in the top level of the folder structure. You will not be able to use this application unless you have your own api key.

[Companies House API](https://developer-specs.company-information.service.gov.uk/)

[Companies House website: follow links to create an account](https://find-and-update.company-information.service.gov.uk/)

The above instructions are only meant to be temporary. The goal is to create a user interface using a Django framework, so that users have an easier experience interacting with the Companies House api. The end goal is to allow users to use this application without having to create a developer account. Users will be able to sign up for alerts by email that will notify them if any business has been registered at their address without their authorisation.
