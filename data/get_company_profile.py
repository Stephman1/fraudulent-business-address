"""
GET request based on company number, 07496944 (THE CO-MISSION CHURCHES TRUST).
The authentication method uses an api key stored in a text file located in the parent directory.
Company information is saved into a CSV file.
"""

import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import json
import os
from urllib.parse import urljoin

"""
Get company profile info from CH and save it in a CSV file.
"""
def getCompanyInfo(company_num: str) -> any:
    # Get api key
    auth_file = getFileParDir("authentication.txt")
    f = open(auth_file,'r')
    auth_dict = json.loads(f.read())
    username = auth_dict['api_key']

    company_data = requests.get(
        url=urljoin('https://api.company-information.service.gov.uk/company/',company_num),
        auth=HTTPBasicAuth(username, '')
    )

    json_object = json.loads(company_data.text)

    df = pd.json_normalize(json_object)
    
    data_file = getFileParDir("company_profile.csv")

    df.to_csv(data_file, index=False)
    
"""
Get the full path of a file in the parent directory.
"""
def getFileParDir(file_name: str) -> str:
    parent_fp = os.path.abspath(os.path.join(os.pardir,os.getcwd()))
    full_fp = os.path.join(parent_fp, file_name)
    return full_fp
    
if __name__ == '__main__':
    company = '07496944'
    # Put company profile data into CSV file.
    getCompanyInfo(company)
