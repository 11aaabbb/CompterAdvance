from django.http import JsonResponse
from sklearn import linear_model
import pandas as pd  # package for high-performance, easy-to-use data structures and data analysis // 数据处理库
import numpy as np  # fundamental package for scientific computing with Python
from search.documents import *
from operator import attrgetter
import operator
# 画图
# Create your views here.
def quary(request):
    if request.method == "GET":
        request.params = request.GET
        city = request.params["c"]
        province = request.params['p']
        death = DeathDocument.search().query('match', city = city).query('match', province = province)
        confirmed = ConfirmedDocument.search().query('match', city = city).query('match', province = province)
        datas = []
        for l in death:
            data = {}
            temp = l.Range.replace("\n","").replace("Index", "").replace(" ", "").replace("dtype='object',", "").replace("([", "").replace("]", "").replace(")", "").split("'")
            data["X"] = temp[1]
            data["Y"] = l.death.replace("\n", "").replace("[", "").replace("]", "").split()
            datas.append(data)
        for l in confirmed:
            data = {}
            temp = temp = l.Range.replace("\n","").replace("Index", "").replace(" ", "").replace("dtype='object',", "").replace("([", "").replace("]", "").replace(")", "").split("'")
            data["X"] = temp[1]
            data["Y"] = l.confirmed.replace("\n", "").replace("[", "").replace("]", "").split()
            datas.append(data)  
        return JsonResponse({
                "result": datas
            })      
             
    else:
        return JsonResponse({
            "msg": "wrong method"
        })


def listcity(request):
    if request.method == "GET":
        request.params = request.GET
        state = request.params["state"]
        type = request.params["type"]
        if type == "confirmed":
            s = ConfirmedDocument.search().query('match', province=state)[0:1000]
            print(s)
            confirmed = []
            for l in s:
                data = {}
                m = l.confirmed.replace("\n", " ")
                k = m.split(" ")
                data["city"] = l.city
                data["confirmed"] = k[len(k) - 1][:-1]
                confirmed.append(data)
            return JsonResponse({
                "msg": "200",
                "data": confirmed
            })
        elif type == "death":
            s = DeathDocument.search().query('match', province=state)[0:1000]
            print(s)
            death = []
            data = {}
            for l in s:
                data = {}
                m = l.death.replace("\n", " ")
                k = m.split(" ")
                data["city"] = l.city
                data["death"] = k[len(k) - 1][:-1]
                death.append(data)
            return JsonResponse({
                "msg": "200",
                "data": death
            })
    else:
        return JsonResponse({
            "msg": "wrong method"
        })


def state(request):
    s = StatesDocument.search().query('match_all')[0:1000]
    data = []
    for l in s:
        datas = {}
        datas['province'] = l.province
        datas["updateTime"] = l.updateTime
        datas["confirmed"] = l.confirmed
        datas["death"] = l.death
        datas["recovered"] = l.recovered
        datas["active"] = l.active
        datas["rate"] = l.rate
        data.append(datas)  
        data.sort(key = lambda x:x["confirmed"], reverse = True)
    return JsonResponse({
        "msg": "200",
        "data": data
    })


def prodict(request):
    if request.method == "GET":
        request.params = request.GET
        city = request.params["c"]
        province = request.params["p"]
        type=request.params["type"]
        datelen = request.params["len"]

        if type == "confirmed":
            confirmed = ""
            s = ConfirmedDocument.search().query('match', province = province).query('match', city = city) 
            for i in s:
                confirmed = i.confirmed
            if len(confirmed) > 0: 
                confirmed = confirmed.replace("[", "").replace("]", "").replace("\n", "").split(" ")
                time = np.array(range(len(confirmed))).reshape(-1,1)
                lenth = np.array(range(len(confirmed), len(confirmed) + int(datelen))).reshape(-1, 1)
                prodicts=linear_model_main(time,confirmed,lenth)
                return JsonResponse(prodicts)
            else:
                return JsonResponse({}) 
        elif type == "death":
            death = ""
            s = DeathDocument.search().query('match', city = city).query('match', province = province)
            for i in s:
                death = i.death
            if len(death) > 0:
                death = death.replace("[", "").replace("]", "").replace("\n", "").split(" ")
                time = np.array(range(len(death))).reshape(-1,1)
                lenth = np.array(range(len(death), len(death) + int(datelen))).reshape(-1, 1)
                prodicts = linear_model_main(time, death, lenth)
                return JsonResponse(prodicts)
            else:
                return JsonResponse({})
    else:
        return JsonResponse({
            "msg": "wrong method"
        })   



def linear_model_main(X_parameters, Y_parameters, predict_value):
    regr = linear_model.LinearRegression()
    regr.fit(X_parameters, Y_parameters)
    predict_outcome = regr.predict(predict_value)
    predictions = {}
    predictions['intercept'] = regr.intercept_
    predictions['coefficient'] = list(regr.coef_)
    predictions['predicted_value'] = list(predict_outcome)

    return predictions