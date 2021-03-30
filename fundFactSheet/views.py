from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
from django.http import HttpResponse

import pandas as pd
import json
import requests 
from pandas import json_normalize 
from pandas import ExcelWriter


headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '3a5189136390449dade9d8cadca3d0a5' # Don't forget to put your keys in xxxx
}

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def profile(request):
    data = {
        'name': 'Vitor',
        'location': 'Finland',
        'is_active': True,
        'count': 28
    }
    return JsonResponse(data)

def fund(request):
    response = requests.get('https://api.sec.or.th/FundFactsheet/fund/amc', headers = headers)
    amc = pd.read_json(response.content)
    all_funds = pd.DataFrame(columns=['proj_id', 'proj_abbr_name','proj_name_en', 'proj_name_th','unique_id','fund_status'])
    for unique_id in amc.unique_id:
        req = requests.get(f'https://api.sec.or.th/FundFactsheet/fund/amc/{unique_id}', headers = headers)
        projects = pd.read_json(req.content)
        projects = projects.loc[(projects['fund_status']!='CA') & (projects['fund_status']!='LI')]
        all_funds = all_funds.append(projects[{'proj_id', 'proj_abbr_name','proj_name_en', 'proj_name_th','unique_id','fund_status'}], ignore_index=True)
        
    return HttpResponse(all_funds.to_json(orient='records'), content_type="application/json") 

def fundByStatus(request):
    status = request.GET['status']
    status = status.rstrip()
    status = status.lstrip()
    print(status)
    response = requests.get('https://api.sec.or.th/FundFactsheet/fund/amc', headers = headers)
    amc = pd.read_json(response.content)
    # all_funds = pd.DataFrame(columns=['proj_id'])
    all_funds = pd.DataFrame(columns=['proj_id', 'proj_abbr_name','proj_name_en', 'proj_name_th','unique_id','fund_status'])
    for unique_id in amc.unique_id:
        req = requests.get(f'https://api.sec.or.th/FundFactsheet/fund/amc/{unique_id}', headers = headers)
        projects = pd.read_json(req.content)
        projects = projects.loc[(projects['fund_status']==status)]
        # all_funds = all_funds.append(projects[{'proj_id'}], ignore_index=True)
        all_funds = all_funds.append(projects[{'proj_id', 'proj_abbr_name','proj_name_en', 'proj_name_th','unique_id','fund_status'}], ignore_index=True)
        # print(all_funds)
    return HttpResponse(all_funds.to_json(orient='records'), content_type="application/json") 


def dividend(project_id):
    req = requests.get(f'https://api.sec.or.th/FundFactsheet/fund/{project_id}/dividend', headers = headers)
    dividend = pd.read_json(req.content)
    dividend = dividend.loc[(dividend['dividend_policy']=='Y')]
    print(dividend)
    return dividend