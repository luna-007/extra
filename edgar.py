import requests
import pandas as pd
import matplotlib.pyplot as plt
# from secedgar import get_ticker_cik


def get_ticker_cik():
    #make a request to get the json
    res = requests.get("https://www.sec.gov/files/company_tickers.json")
    res = res.json()

    #create a df with columns: "cik_str","tiker","title" 
    res=pd.DataFrame.from_dict(res, orient="index")
    #create a df that maps the cik to the ticker
    fromCik=pd.DataFrame([res["ticker"].values],columns=res["cik_str"].values)
    #create a df that maps the ticker to the cik
    fromTicker=pd.DataFrame([res["cik_str"].values],columns=res["ticker"].values)
    return fromCik, fromTicker

#USAGE:
fromCik,fromTicker=get_ticker_cik()
print(fromTicker["AAPL"][0]) #returns "320193"
print(fromCik[320193][0]) #returns "AAPL"

def get_fundamentals(cik, fact, form):
    #we pad the cik with 0, the api requires the cik to be 10 characters long
    cik=str(cik).rjust(10,"0")
    url=f'https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/us-gaap/{fact}.json'

    res = requests.get(url, headers={"User-Agent":"Java-http-client/"})
    res = res.json()
    res=res["units"]["USD"]
    res=pd.DataFrame(res)
    #filtering the dataframe by frame type ("10-Q" or "10-K")
    res=res[res["form"]==form]
    #tranforming the type from string to date
    res["end"]=res["end"].astype('datetime64[ns]')
    #we index the dataframe by the date which the historical value refers
    res.index=res["end"]
    #sort by date
    res=res.sort_index()
    return res

#USAGE:
fromCik,fromTicker=get_ticker_cik()
values=get_fundamentals(fromTicker["AAPL"][0],"Assets","10-Q")
print(values.to_string())
plt.plot(values["val"])
plt.ylabel("Assets value")
plt.show()