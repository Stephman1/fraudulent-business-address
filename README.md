# Companies House
Companies House data project by Stephen and Ashika.

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

# Do not upload virtual env folder, authentication.txt
git status
git pull 
git add requirements.txt
git commit -m "comment"
git push 
```

## Style Guide

We will use pep8 style guide for our naming convention

## Instructions

Go to retrieval/company_search.py and run the file. You can use either the searchAll or searchAddress functions. The results of the search will be automatically saved in csv files in a data folder that will be created for you. All data is linked by company number, officer number or charge codes. You can modify the search query by inputting any string into the function parameter.

You will need to create a Companies House account (no cost involved), get a developer api key and save this api key in a file called authentication.txt in the top level of the folder structure. You will not be able to use this application unless you have your own api key.

[Companies House API](https://developer-specs.company-information.service.gov.uk/)
[Companies House website: follow links to create an account](https://find-and-update.company-information.service.gov.uk/)

The above instructions are only meant to be temporary. The goal is to create a user interface using a Django framework, so that users have an easier experience interacting with the Companies House api. The end goal is to allow users to use this application without having to create a developer account. Users will be able to sign up for alerts by email that will notify them if any business has been registered at their address without their authorisation.
