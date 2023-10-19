from secedgar.cik_lookup import get_cik_map
import pandas as pd
from secedgar.core import DailyFilings, QuarterlyFilings
from datetime import date

cik_map = get_cik_map()
cik_map = pd.DataFrame.from_dict(cik_map['ticker'],  orient='index')
# cik_map.reset_index(inplace=True)
# cik_map.columns = ['company_name', 'cik']
# print(cik_map.company_name)
# print(cik_map.index[0])

# headers = {
# "User-Agent": "jo boulement jo@gmx.at",
# "Accept-Encoding": "gzip, deflate" 
# }

def get_company_a_filings(cik_map):
    for i in range(len(cik_map)):
        if (cik_map.index[i] == "AAPL"):
            print(cik_map.index[i])
            return cik_map.index[i] == "AAPL"
    # return cik_map.company_name == "AAPL"

# get_company_a_filings(cik_map)

d = QuarterlyFilings(year=2021,
                     quarter=2,
                     entry_filter=get_company_a_filings(cik_map),
                     user_agent= "jo boulement jo@gmx.at")

print(d.get_urls())