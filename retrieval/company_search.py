from companies_house_api import ChAPI
import json

class CompanySearch():
    """
    Search for companies by keyword.
    """
    
    def __init__(self, authentication_fp=None) -> None:
        self._company_headers = ["company_number", "officer_surname", "officer_forename", "officer_other_forenames", 
                                 "officer_role", "nationality", "appointed_on", "dob_month", "dob_year", "premises",
                                 "address_line_1", "postal_code", "locality", "country", "country_of_residence", 
                                 "occupation", "appointments", "officer_id", "appointment_kind", "is_corporate_officer", 
                                 "total_company_appointments",]
        
        self._sic_code_headers = ["company_number", "sic_codes"]
        self._previous_company_names_headers = ["company_number","ceased_on","effective_from","name"]
        self._company_officers_headers = ["company_number", "officer_surname", "officer_forename", "officer_other_forenames", 
                                 "officer_role", "nationality", "appointed_on", "dob_month", "dob_year", "premises",
                                 "address_line_1", "postal_code", "locality", "country", "country_of_residence", 
                                 "occupation", "appointments", "officer_id", "appointment_kind", "is_corporate_officer", 
                                 "total_company_appointments",] 
        self._officer_appointments_headers = ["officer_id", "company_number", "company_name", "company_status", 
                                              "officer_role", "appointed_on"]
        self._significant_persons_headers = ["company_number","name","title","surname","forename","other_forenames",
                                             "dob_month","dob_year","kind","notified_on","nationality","country_of_residence",
                                             "address_premises","address_line_1","address_line_2","address_locality",
                                             "address_postal_code","address_country","etag","registration_number","legal_form",
                                             "legal_authority","country_registered","place_registered",]
        self._natures_of_control_headers = ["etag","nature_of_control"]
        
    
    def searchAll(self, query: str, items_per_page: int = 25, start_index: int = 0) -> None:
        api_key = ChAPI.getApiKey()
        url = r'https://api.company-information.service.gov.uk/search'
        
        params = {"q":query, "items_per_page":items_per_page, "start_index":start_index}
        search = ChAPI.getChData(url=url, api_key=api_key, params=params)
        
        for item in search.get('items', []):
            pass
        

if __name__ == '__main__':
    pass
