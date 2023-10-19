import requests
import json
import pandas as pd

url = 'https://data.sec.gov/api/xbrl/companyfacts/CIK0001326801.json'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
response = requests.get(url, headers=headers)

datas = json.loads(response.text)
final_list = []
print("Part One Done")

def get_input_list(data):
    # return pre_process_one
    pre_process = data['facts']['us-gaap'].keys()
    input_list = []
    for i in pre_process:
        input_list.append(i)
    print("Part two Done")
    return input_list

def get_data(input_list):
    print("Part three started")
    final_dict = {}
    processed = []
    global pre_process
    processed = None
    
    for i in input_list:
        url = f'https://data.sec.gov/api/xbrl/frames/us-gaap/{i}/USD/CY2019Q1I.json'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("Success")
        elif response.status_code != 200:
            print("server Overload")
            break
        pre_process = json.loads(response.text)
        pre_process = pre_process['data']
    print("First Round")
    
    for i in range(len(pre_process) - 1):
        processed = pre_process[i]
        if i == 50:
            print("50 done")
        elif i == 500:
            print("500 done")
            pass

            for i in processed:
                # print(type(i))
                final_dict = {i ," : ",processed[i]}
                final = pd.DataFrame()
                global final_df
                final_df = pd.DataFrame(final_dict)
                # final = {i: [processed[i]]}
                # pd.concat([final_df, final], axis=1, join='outer')
    print("Second Round")
    # df = pd.DataFrame(final_df)
    print("Final Part Done")        
    print(final_df)
    # return final_df

data = (get_data(get_input_list(datas)))
# df = pd.DataFrame.from_dict(get_data(get_input_list(datas)))
# data