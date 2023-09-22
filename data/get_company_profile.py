"""
GET request based on company number, 07496944 (THE CO-MISSION CHURCHES TRUST).
"""

import requests
from requests.auth import HTTPBasicAuth
import json

username = "ea96b774-700f-4ef6-b69a-592545426b56"

company_data = requests.get(
    url='https://api.company-information.service.gov.uk/company/07496944',
    auth=HTTPBasicAuth(username, '')
    )

json_object = json.loads(company_data.text)

json_formatted_str = json.dumps(json_object, indent=2)

print(json_formatted_str)
