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


class CompanyInfoRetriever():
    
    def __init__(self, company_number: str, authentication_fp=None):
        self.company_num = company_number
        if authentication_fp is None:
            self.api_key = self.getApiKey()
        else:
            self.api_key = self.getApiKey(authentication_fp)

    """
    Get company profile info from CH and save it in three CSV files:
    sic_codes.csv
    prev_companies.csv
    company_profile.csv
    The primary key is the company number.
    """
    def getCompanyInfo(self) -> any:
        company_data = requests.get(
            url=urljoin('https://api.company-information.service.gov.uk/company/',self.company_num),
            auth=HTTPBasicAuth(self.api_key, '')
        )

        json_object = json.loads(company_data.text)
        
        # Get sic codes
        sic_codes = json_object.get('sic_codes')
        
        if not sic_codes is None:
            self.getSICCodes(sic_codes,self.company_num)
                
        # Get previous company names
        prev_companies = json_object.get('previous_company_names')
        
        if not prev_companies is None:
            self.getPreviousCompanies(prev_companies,self.company_num)

        df = pd.json_normalize(json_object)
        
        # Exclude sic codes and previous company names
        mod_df = df.loc[:, ~df.columns.isin(['sic_codes', 'previous_company_names'])]
        
        data_file = self.getDataFolderLocation(self.company_num + '_company_profile.csv')

        mod_df.to_csv(data_file, index=False)


    """
    Get SIC codes
    """
    def getSICCodes(self, sic_codes: any, company_num: str) -> any:
        sic_file = self.getDataFolderLocation(self.company_num + '_sic_codes.csv')
        
        with open(sic_file,"w") as sf:
            sf.write("company_number,sic_codes\n")
            for sic in sic_codes:
                sf.write(f"{company_num},{sic}\n")


    """
    Get previous companies
    """
    def getPreviousCompanies(self, prev_companies: any, company_num: str) -> any:
        prev_file = self.getDataFolderLocation(self.company_num + '_prev_companies.csv')
        
        with open(prev_file,"w") as pf:
            pf.write("company_number,ceased_on,effective_from,name\n")
            for prev in prev_companies:
                pf.write(f"{company_num},{prev.get('ceased_on')},{prev.get('effective_from')},{prev.get('name')}\n")


    """
    Get CH authentication key.
    """
    def getApiKey(self, authentication_fp=None) -> str:
        if authentication_fp is None:
            auth_file = self.getFileParDir('authentication.txt')
        else:
            auth_file = authentication_fp
        with open(auth_file,'r') as f:
            auth_dict = json.loads(f.read())
        return auth_dict['api_key']


    """
    Get the full path of a file in the parent directory.
    """
    def getFileParDir(self, file_name: str) -> str:
        parent_dir = os.path.abspath(os.path.join(os.pardir,os.getcwd()))
        full_fp = os.path.join(parent_dir, file_name)
        return full_fp
    
    """
    Get the location of the data folder or create it if it doesn't exist.
    """
    def getDataFolderLocation(self, file_name: str, folder_name: str = "data") -> str:
        parent_dir = os.path.abspath(os.path.join(os.pardir, os.getcwd()))
        data_folder = os.path.join(parent_dir, folder_name)
        
        # Create the 'data' folder if it doesn't exist
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)

        full_fp = os.path.join(data_folder, file_name)
        return full_fp
    
    
    """
    Change the company number.
    """
    def setCompanyNumber(self, company_number: str) -> any:
        self.company_num = company_number

    """
    Change the api key by entering a new file path for the authentication file.    
    """
    def setAuthenticationFilePath(self, auth_fp: any) -> any:
        self.api_key = self.getApiKey(auth_fp)


"""
Run the program to return company information using the Companies House API.
"""
def main():
    # The first time the user retrieves company information
    first_company = True
    company_info_retriever = None
    while True:
        company_number = input("Enter the company number: ")
        print("You entered:", company_number)
        company_number = company_number.strip()
        
        if not company_number.isalnum():
           print("This company number does not look valid. Please retry.")
        else:
            if first_company:
                company_info_retriever = initialInfoRetrieval(company_number)
                first_company = False
            else:
                company_info_retriever.setCompanyNumber(company_number)
                company_info_retriever.getCompanyInfo()
            continue_or_exit = input(f"Would you like to retrieve information for another company? Enter Yes to "
                                        f"continue searching or leave blank to exit the program: ")
            print("You entered:", continue_or_exit)
            continue_or_exit = continue_or_exit.strip().lower()
            if (continue_or_exit == "yes" or continue_or_exit == "y"):
                continue
            else:
                return


def initialInfoRetrieval(company_num: str) -> CompanyInfoRetriever:
    authentication_fp = input(f"Enter the full path of the authentication file or leave blank if it is in the "
                                      f"parent directory and named authenticaton.txt: ")
    print("You entered:", authentication_fp)
    authentication_fp = authentication_fp.strip()
    if not authentication_fp:
        company_info_retriever = CompanyInfoRetriever(company_num) 
    else:
        company_info_retriever = CompanyInfoRetriever(company_num,authentication_fp)
    company_info_retriever.getCompanyInfo()
    return company_info_retriever
    

if __name__ == '__main__':
    """
    'MAN UTD supporters club Scandinavia': 'OE025157', 
    'Dundonald Church': '07496944'
    'MAN UTD football club ltd': '00095489'
    'MAN UTD ltd': '02570509'
    'Swaravow Ltd' = '15192197'
    """
    main()
