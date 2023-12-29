# companies-house
Companies House data project by Stephen and Ashika.

## Setting up a virtual Environment
python -m venv ch_env

## Activating the virtual Environment
source ch_env/bin/activate

## Installing relevant python packages 
pip install -r requirements.txt

## Saving relevant python packages in requirement
pip freeze > requirements.txt

## Do not upload virtual env folder, authentication.txt
git status
git pull 
git add requirements.txt
git commit -m "comment"
git push 

## We will use pep8 style guide for our naming convention
