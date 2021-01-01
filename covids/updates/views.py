from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd  # package for high-performance, easy-to-use data structures and data analysis // 数据处理库
import numpy as np  # fundamental package for scientific computing with Python
from common.models import *
from search.documents import *
# Create your views here.
def updates(request):
    try:
        date = request.GET.date
        url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"
        dataset = pd.read_csv(url)
        dataset = dataset.fillna("0")
        for row in dataset.iterrows():
            uid = row[1].values[0]
            city = row[1].values[5]
            province = row[1].values[6]
            cityName = row[1].values[10]
            Range = str(row[1].keys()[12:])
            death = str(row[1].values[12:])
            print("===")
            timeSeriseDeath.objects.create(uid=uid, city=city, province=province, cityName=cityName, death=death,
                                           Range=Range)
        url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
        dataset = pd.read_csv("time_series_covid19_confirmed_US.csv")
        dataset = dataset.fillna("0")
        for row in dataset.iterrows():
            uid = row[1].values[0]
            city = row[1].values[5]
            province = row[1].values[6]
            cityName = row[1].values[10]
            Range = str(row[1].keys()[11:])
            confirmed = str(row[1].values[11:])
            timeSeriseConfirmed.objects.create(uid=uid, city=city, province=province, cityName=cityName,
                                               confirmed=confirmed, Range=Range)
        url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/"+date+".csv"
        dataset = pd.read_csv("12-26-2020.csv")
        dataset = dataset.fillna("0")
        for row in dataset.iterrows():
            province = row[1].values[0]
            Update = row[1].values[2]
            confirmed = row[1].values[5]
            death = row[1].values[6]
            recovered = row[1].values[7]
            active = row[1].values[8]
            rate = row[1].values[9]
            allStates.objects.create(province=province, Update=Update, confirmed=confirmed, death=death,
                                    recovered=recovered, active=active, rate=rate)
        return JsonResponse({
            "msg": "200",
            "data": "update successfully"
        })
    except:
        return JsonResponse({
            "msg": "303",
            "data": "data_not_found"
        })