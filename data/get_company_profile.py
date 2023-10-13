"""
GET request based on company number, 07496944 (THE CO-MISSION CHURCHES TRUST).

The authentication method uses an api key stored in a text file located in the parent directory.
"""

import requests
from requests.auth import HTTPBasicAuth
import json
import os
from urllib.parse import urljoin

def getCompanyInfo(company_num: str) -> str:

    # Get api key
    auth_fp = os.path.abspath(os.path.join(os.pardir,os.getcwd()))
    auth_file = os.path.join(auth_fp, 'authentication.txt')
    f = open(auth_file,'r')
    auth_dict = json.loads(f.read())
    username = auth_dict['api_key']

    company_data = requests.get(
        url=urljoin('https://api.company-information.service.gov.uk/company/',company_num),
        auth=HTTPBasicAuth(username, '')
    )

    json_object = json.loads(company_data.text)

    json_formatted_str = json.dumps(json_object, indent=2)

    return json_formatted_str
    
if __name__ == '__main__':
    company = '07496944'    
    print(getCompanyInfo(company))
