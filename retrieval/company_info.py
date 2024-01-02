"""
GET request based on company number.
The authentication method uses an api key stored in a text file located in the parent directory.
Company information is exported to CSV files.
"""
import sys
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import json
import os
import csv
from urllib.parse import urljoin


class CompanyInfo():
    
    def __init__(self, company_number: str, authentication_fp=None):
        self._company_number = company_number
        base_url = 'https://api.company-information.service.gov.uk/'
        self._company_url = urljoin(base_url + 'company/', str(self._company_number))
        
        if authentication_fp is None:
            self.__api_key = self.getApiKey()
        else:
            self.__api_key = self.getApiKey(authentication_fp)
        
        company_data = self.getChData(self._company_url)
        # Links
        links = company_data.get('links')
        self._officers_url = urljoin(base_url, links.get('officers'))
        self._filing_history_url = urljoin(base_url, links.get('filing_history')) 
        self._charges_url = urljoin(base_url, links.get('charges')) 
        self._persons_significant_control_url = urljoin(base_url, links.get('persons_with_significant_control_statements'))
        # Company info
        self._company_status = str(company_data.get('company_status', ''))
        self._company_name = str(company_data.get('company_name', ''))
        self._jurisdiction = str(company_data.get('jurisdiction', ''))
        self._date_of_creation = str(company_data.get('date_of_creation', ''))
        self._has_insolvency_history = bool(company_data.get('date_of_creation', False))
        self._has_charges = bool(company_data.get('has_charges', False))
        self._has_been_liquidated = bool(company_data.get('has_been_liquidated', False))
        self._undeliverable_registered_office_address = bool(company_data.get('undeliverable_registered_office_address', False))
        self._registered_office_is_in_dispute = bool(company_data.get('registered_office_is_in_dispute', False))
        self._accounts_overdue = bool(company_data.get('accounts', {}).get('overdue', False))
        # Address
        self._address_line_1 = str(company_data.get('registered_office_address', {}).get('address_line_1', ''))
        self._postal_code = str(company_data.get('registered_office_address', {}).get('postal_code', '')) 
        self._locality = str(company_data.get('registered_office_address', {}).get('locality', ''))
        self._country = str(company_data.get('registered_office_address', {}).get('country', ''))
        
        # Officers
        self._officers = dict()
        
        
    @property
    def company_status(self):
        return self._company_status

    @property
    def company_name(self):
        return self._company_name

    @property
    def jurisdiction(self):
        return self._jurisdiction

    @property
    def date_of_creation(self):
        return self._date_of_creation

    @property
    def has_insolvency_history(self):
        return self._has_insolvency_history

    @property
    def has_charges(self):
        return self._has_charges

    @property
    def has_been_liquidated(self):
        return self._has_been_liquidated

    @property
    def undeliverable_registered_office_address(self):
        return self._undeliverable_registered_office_address

    @property
    def registered_office_is_in_dispute(self):
        return self._registered_office_is_in_dispute

    @property
    def accounts_overdue(self):
        return self._accounts_overdue

    @property
    def address_line_1(self):
        return self._address_line_1

    @property
    def postal_code(self):
        return self._postal_code

    @property
    def locality(self):
        return self._locality

    @property
    def country(self):
        return self._country
    
    @property
    def company_number(self):
        return self._company_number
    
    @property
    def company_url(self):
        return self._company_url
    
    @property 
    def officers_url(self):
        return self._officers_url

    @property
    def filing_history_url(self):
        return self._filing_history_url

    @property
    def charges_url(self):
        return self._charges_url

    @property
    def persons_significant_control_url(self):
        return self._persons_significant_control_url
    
    @property
    def api_key(self):
        return "Access denied"
    
    @property
    def officers(self):
        return self._officers
        
        
    def exportCompanyInfo(self) -> any:
        """
        Get company profile info from CH and export it to CSV files:
        {company_number}_sic_codes.csv
        {company_number}_prev_companies.csv
        {company_number}_company_profile.csv
        {company_number}_officers.csv
        The primary key is the company number.
        """
        company_data = self.getChData(self._company_url)
        
        # Get sic codes
        sic_codes = company_data.get('sic_codes')
        
        if not sic_codes is None:
            self.getSICCodes(sic_codes,self._company_number)
                
        # Get previous company names
        prev_companies = company_data.get('previous_company_names')
        
        if not prev_companies is None:
            self.getPreviousCompanies(prev_companies,self._company_number)

        df = pd.json_normalize(company_data)
        
        # Get officers
        self.getCompanyOfficers()
        
        # Exclude sic codes and previous company names
        mod_df = df.loc[:, ~df.columns.isin(['sic_codes', 'previous_company_names'])]
        
        data_file = self.getDataFolderLocation(self._company_number + '_company_profile.csv')

        mod_df.to_csv(data_file, index=False)
        
        
    def getSICCodes(self, sic_codes: any, company_num: str) -> any:
        """
        Get SIC codes
        """
        sic_file = self.getDataFolderLocation(f"{self._company_number}_sic_codes.csv")
        
        with open(sic_file,"w",newline='') as sf:
            sf.write("company_number,sic_codes\n")
            for sic in sic_codes:
                sf.write(f"{company_num},{sic}\n")


    def getPreviousCompanies(self, prev_companies: any, company_num: str) -> any:
        """
        Get previous companies
        """
        prev_file = self.getDataFolderLocation(f"{self._company_number}_prev_companies.csv")
        
        with open(prev_file,"w",newline='') as pf:
            pf.write("company_number,ceased_on,effective_from,name\n")
            for prev in prev_companies:
                pf.write(f"{company_num},{prev.get('ceased_on')},{prev.get('effective_from')},{prev.get('name')}\n")
                
                
    def getCompanyOfficers(self) -> any:
        """
        Get company officers
        """
        # Fetch new officers data
        officers_data = self.getChData(self._officers_url)
        officers = officers_data.get('items')

        # Update the _officers attribute with the new data
        self._officers = dict()

        with open(self.getDataFolderLocation(f"{self._company_number}_officers.csv"), "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["company_number", "officer_name", "officer_role", "nationality", "dob_month", "dob_year",
                                "premises", "address_line_1", "postal_code", "locality", "country", "country_of_residence", 
                                "occupation", "appointments"])

            for officer in officers:
                officer_name = officer.get('name')
                if officer_name is not None:
                    officer_name = str(officer_name)
                    self._officers[officer_name] = {
                        'officer_role': str(officer.get('officer_role')),
                        'nationality': str(officer.get('nationality')),
                        'date_of_birth_month': int(officer.get('date_of_birth', {}).get('month', 0)),
                        'date_of_birth_year': int(officer.get('date_of_birth', {}).get('year', 0)),
                        'address_premises': str(officer.get('address', {}).get('premises', '')),
                        'address_address_line_1': str(officer.get('address', {}).get('address_line_1', '')),
                        'address_postal_code': str(officer.get('address', {}).get('postal_code', '')),
                        'address_locality': str(officer.get('address', {}).get('locality', '')),
                        'address_country': str(officer.get('address', {}).get('country', '')),
                        'occupation': str(officer.get('occupation', '')),
                        'country_of_residence': str(officer.get('country_of_residence')),
                        'appointments': str(officer.get('links', {}).get('officer', {}).get('appointments', ''))
                    }
                    # Write data to CSV
                    csv_writer.writerow([
                        self._company_number,
                        officer_name,
                        self._officers[officer_name]['officer_role'],
                        self._officers[officer_name]['nationality'],
                        self._officers[officer_name]['date_of_birth_month'],
                        self._officers[officer_name]['date_of_birth_year'],
                        self.officers[officer_name]['address_premises'],
                        self._officers[officer_name]['address_address_line_1'],
                        self._officers[officer_name]['address_postal_code'],
                        self._officers[officer_name]['address_locality'],
                        self._officers[officer_name]['address_country'],
                        self._officers[officer_name]['country_of_residence'],
                        self._officers[officer_name]['occupation'],
                        self._officers[officer_name]['appointments']
                    ])
                else:
                    print("Warning: Officer name is None.")


    def getApiKey(self, authentication_fp=None) -> str:
        """
        Get CH authentication key.
        """
        if authentication_fp is None:
            auth_file = self.getFileParDir('authentication.txt')
        else:
            auth_file = authentication_fp
        with open(auth_file,'r') as f:
            auth_dict = json.loads(f.read())
        return auth_dict['api_key']


    
    def getFileParDir(self, file_name: str) -> str:
        """
        Get the full path of a file in the parent directory.
        """
        parent_dir = os.path.abspath(os.path.join(os.pardir,os.getcwd()))
        full_fp = os.path.join(parent_dir, file_name)
        return full_fp
    
    
    def getDataFolderLocation(self, file_name: str, folder_name: str = "data") -> str:
        """
        Get the location of the data folder or create it if it doesn't exist.
        """
        parent_dir = os.path.abspath(os.path.join(os.pardir, os.getcwd()))
        data_folder = os.path.join(parent_dir, folder_name)
        
        # Create the 'data' folder if it doesn't exist
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)

        full_fp = os.path.join(data_folder, file_name)
        return full_fp


    
    def setAuthenticationFilePath(self, auth_fp: any) -> any:
        """
        Change the api key by entering a new file path for the authentication file.    
        """
        self.__api_key = self.getApiKey(auth_fp)


    def getChData(self, url: str) -> dict:
        """
        Hits the Companies House API and returns data as a dictionary.
        """
        try:
            response = requests.get(url=url, auth=HTTPBasicAuth(self.__api_key, ''))
            response.raise_for_status()  # Raise an HTTPError for bad responses
            return response.json()
        except requests.RequestException as e:
            print(f"Error during API request: {e}")
            return {}
    

if __name__ == '__main__':
    """
    'MAN UTD supporters club Scandinavia': 'OE025157', 
    'Dundonald Church': '07496944'
    'MAN UTD football club ltd': '00095489'
    'MAN UTD ltd': '02570509'
    'Swaravow Ltd' = '15192197'
    """
    man_utd = CompanyInfo('07496944')
    man_utd.exportCompanyInfo()
