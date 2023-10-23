"""
GET request based on company number, 07496944 (THE CO-MISSION CHURCHES TRUST).
The authentication method uses an api key stored in a text file located in the parent directory.
Company information is saved into a CSV file.
"""
import sys
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import json
import os
from urllib.parse import urljoin


"""
Get company profile info from CH and save it in three CSV files:
sic_codes.csv
prev_companies.csv
company_profile.csv
The primary key is the company number.
"""
def getCompanyInfo(company_num: str) -> any:

    username = getApiKey()

    company_data = requests.get(
        url=urljoin('https://api.company-information.service.gov.uk/company/',company_num),
        auth=HTTPBasicAuth(username, '')
    )

    json_object = json.loads(company_data.text)
    
    # Get sic codes
    sic_codes = json_object.get('sic_codes')
    
    if not (sic_codes is None):
        sic_file = getFileParDir('sic_codes.csv')
    
        with open(sic_file,"w") as sf:
            sf.write("company_number,sic_codes\n")
            for sic in sic_codes:
                sf.write(f"{company_num},{sic}\n")
            
    # Get previous company names
    prev_companies = json_object.get('previous_company_names')
    
    if not (prev_companies is None):
        prev_file = getFileParDir('prev_companies.csv')
    
        with open(prev_file,"w") as pf:
            pf.write("company_number,ceased_on,effective_from,name\n")
            for prev in prev_companies:
                pf.write(f"{company_num},{prev.get('ceased_on')},{prev.get('effective_from')},{prev.get('name')}\n")

    df = pd.json_normalize(json_object)
    
    # Exclude sic codes and previous company names
    mod_df = df.loc[:, ~df.columns.isin(['sic_codes', 'previous_company_names'])]
    
    data_file = getFileParDir('company_profile.csv')

    mod_df.to_csv(data_file, index=False)


"""
Get the full path of a file in the parent directory.
"""
def getFileParDir(file_name: str) -> str:
    parent_fp = os.path.abspath(os.path.join(os.pardir,os.getcwd()))
    full_fp = os.path.join(parent_fp, file_name)
    return full_fp


"""
Get CH authentication key.
"""
def getApiKey() -> str:
    auth_file = getFileParDir('authentication.txt')
    with open(auth_file,'r') as f:
        auth_dict = json.loads(f.read())
    return auth_dict['api_key']


if __name__ == '__main__':
    """
    'MAN UTD supporters club Scandinavia': 'OE025157', 
    'Dundonald Church': '07496944'
    'MAN UTD football club ltd': '00095489'
    'MAN UTD ltd': '02570509'
    'Swaravow Ltd' = '15192197'
    """
    company = '07496944'
    getCompanyInfo(company)
