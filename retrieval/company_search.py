from companies_house_api import ChAPI
from company_info import CompanyInfo
from datetime import datetime
import csv

class CompanySearch():
    """
    Search for companies by keyword.
    """
    
    def __init__(self, authentication_fp: str = None) -> None:
        self._company_headers = ["company_number", "company_name", "company_status", "company_type", "jurisdiction", 
                                 "is_foreign_company", "date_of_creation", "etag", "external_registration_number", 
                                 "address_line_1", "locality", "postal_code", "country", "accounts_overdue", "has_been_liquidated", 
                                 "has_charges", "has_insolvency_history", "registered_office_is_in_dispute", 
                                 "undeliverable_registered_office_address"]
        self._sic_code_headers = ["company_number", "sic_codes"]
        self._previous_company_names_headers = ["company_number","ceased_on","effective_from","name"]
        self._company_officers_headers = ["company_number", "officer_surname", "officer_forename", "officer_other_forenames", 
                                          "officer_name", "officer_role", "nationality", "appointed_on", "dob_month", "dob_year", 
                                          "premises","address_line_1", "postal_code", "locality", "country", "country_of_residence", 
                                          "occupation", "appointments", "officer_id", "appointment_kind", "is_corporate_officer", 
                                          "total_company_appointments"] 
        self._officer_appointments_headers = ["officer_id", "company_number", "company_name", "company_status", "officer_role", 
                                              "appointed_on"]
        self._significant_persons_headers = ["company_number","name","title","surname","forename","other_forenames", "dob_month",
                                             "dob_year","kind","notified_on","nationality","country_of_residence","address_premises",
                                             "address_line_1","address_line_2","address_locality","address_postal_code",
                                             "address_country","etag","registration_number","legal_form","legal_authority",
                                             "country_registered","place_registered"]
        self._natures_of_control_headers = ["etag","nature_of_control"]
        self._company_charges_headers = ["company_number", "charge_code", "classification_description", "charge_number", "status", "delivered_on", 
                                         "created_on", "particulars_description", "contains_fixed_charge", "contains_floating_charge",
                                         "floating_charge_covers_all", "contains_negative_pledge"]
        self._charges_persons_entitled_headers = ["charge_code", "persons_entitled"]
        self._charges_transactions_headers = ["charge_code", "filing_type", "delivered_on", "links"]
        
        if authentication_fp is None:
            self.__api_key = ChAPI.getApiKey()
        else:
            self.__api_key = ChAPI.getApiKey(authentication_fp)
        
    
    def searchAll(self, query: str, items_per_page: int = 25, start_index: int = 0) -> None:
        """
        This methods returns results for a search of Companies House data using the search 
        all function. The results are returned in csv files.
        
        Args:
            query (str): This is the search term that the user inputs, e.g., Arsenal
            items_per_page (int, optional): This is the number of results returned. Defaults to 100.
            start_index (int, optional): Defaults to 0.
        """
        if len(query) == 0:
            print("Please enter a search query.")
            return
        
        url = r'https://api.company-information.service.gov.uk/search'
        
        params = {"q":query, "items_per_page":items_per_page, "start_index":start_index}
        search = ChAPI.getChData(url=url, api_key=self.__api_key, params=params)
        
        # current date and time
        now = datetime.now()
        timestamp = str(datetime.timestamp(now))
        
        padded_query = query + "____"
        prefix = padded_query[:5]
        self.insertHeaders(prefix, timestamp)
        
        for item in search.get('items', []):
            company_no = item.get('company_number') 
            if company_no:
                CompanyInfo(str(company_no), timestamp, prefix=prefix).exportCompanyInfo()
    
    
    def insertHeaders(self, prefix: str, timestamp: str):
        """
        Create csv files and insert headers.

        Args:
            prefix (str): the prefix for the csv files, usually the search term
            timestamp (str): the timestamp for when the search was made
        """
        # Company information
        company_fp = ChAPI.getDataFolderLocation(prefix + '_companies_' + timestamp + '.csv')
        with open(company_fp,"w",newline='') as company_file:
            company_writer = csv.writer(company_file)
            company_writer.writerow(self._company_headers)
        # Officers
        officers_fp = ChAPI.getDataFolderLocation(prefix + '_company_officers_' + timestamp + '.csv')
        with open(officers_fp,"w",newline='') as officers_file:
            officers_writer = csv.writer(officers_file)
            officers_writer.writerow(self._company_officers_headers) 
        # Officers' appointments
        appointments_fp = ChAPI.getDataFolderLocation(prefix + '_officer_appointments_' + timestamp + '.csv')
        with open(appointments_fp,"w",newline='') as appointments_file:
            appointments_writer = csv.writer(appointments_file)
            appointments_writer.writerow(self._officer_appointments_headers) 
        # SIC codes
        sic_codes_fp = ChAPI.getDataFolderLocation(prefix + '_sic_codes_' + timestamp + '.csv')
        with open(sic_codes_fp,"w",newline='') as sic_file:
            sic_writer = csv.writer(sic_file)
            sic_writer.writerow(self._sic_code_headers) 
        # Previous company names
        prev_fp = ChAPI.getDataFolderLocation(prefix + '_previous_company_names_' + timestamp + '.csv')
        with open(prev_fp,"w",newline='') as prev_file:
            prev_writer = csv.writer(prev_file)
            prev_writer.writerow(self._previous_company_names_headers)  
        # Persons with significant control
        significant_control_fp = ChAPI.getDataFolderLocation(prefix + '_persons_significant_control_' + timestamp + '.csv')
        with open(significant_control_fp,"w",newline='') as sig_file:
            sig_writer = csv.writer(sig_file)
            sig_writer.writerow(self._significant_persons_headers)
        # Natures of control
        natures_fp = ChAPI.getDataFolderLocation(prefix + '_natures_of_control_' + timestamp + '.csv')
        with open(natures_fp,"w",newline='') as natures_file:
            natures_writer = csv.writer(natures_file)
            natures_writer.writerow(self._natures_of_control_headers)
        # Company charges
        charges_fp = ChAPI.getDataFolderLocation(prefix + '_company_charges_' + timestamp + '.csv')
        with open(charges_fp,"w", newline='') as charges_file:
            charges_writer = csv.writer(charges_file)
            charges_writer.writerow(self._company_charges_headers)
        # Charges persons entitled
        entitled_fp = ChAPI.getDataFolderLocation(prefix + '_charges_persons_entitled_' + timestamp + '.csv')
        with open(entitled_fp,"w", newline='') as entitled_file:
            entitled_writer = csv.writer(entitled_file)
            entitled_writer.writerow(self._charges_persons_entitled_headers) 
        # Charges transactions
        transactions_fp = ChAPI.getDataFolderLocation(prefix + '_charges_transactions_' + timestamp + '.csv')
        with open(transactions_fp,"w", newline='') as transactions_file:
            transactions_writer = csv.writer(transactions_file)
            transactions_writer.writerow(self._charges_transactions_headers)

if __name__ == '__main__':
    CompanySearch().searchAll("Swara")
