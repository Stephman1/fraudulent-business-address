"""
This is a test file with date formatting code unrelated to the Companies House project.

Returns:
    _type_: _description_
"""

import pandas as pd
import datetime

dates = pd.Series(["12-Jan-64", "10-Sep-78"])

format_dates = pd.to_datetime(dates)

print(format_dates)

def fix_date(x):

    if x.year > 2000:

        year = x.year - 100

    else:

        year = x.year

    return datetime.date(year,x.month,x.day)

dates = format_dates.apply(fix_date)

print(dates)

#dates = dates.datetime.strftime("%d/%m/%Y")
