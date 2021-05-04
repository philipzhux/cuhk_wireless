from django.shortcuts import render
import django.contrib.staticfiles
from .fetch import run as data
import time
import sys
sys.path.append('..')
import config
# import configurations
LOCATION_LIB = config.LOCATION_LIB
CSV_PATH = config.CSV_PATH
INTERVAL = config.INTERVAL
CACHE_INTERVAL = config.CACHE_INTERVAL
comparator = config.comparator
weight_adder = config.weight_adder
status_converter = config.status_converter

def index(request):
    loc_list = []
    for i in range(len(LOCATION_LIB)):
        caption = LOCATION_LIB[i][0]
        pic_path = 'assets/img/portfolio/'+str(i)+'.jpg'
        loc_list.append({"id":i,"caption":caption,"pic":pic_path})
    context = {"loc_list":loc_list}
    return render(request,"index.html",context)

def htt(location,request,keywords):
    load,ap_list = data.view_info(CSV_PATH,INTERVAL,CACHE_INTERVAL,comparator,weight_adder,keywords)
    color_list = config.COLOR_LIST
    status_list = config.STATUS_LIST
    print(load)
    status_i = status_converter(load)
    context = {"title":location,
    "load":str(load),"ap_list":ap_list,"color":color_list[int(status_i)],"status":status_list[int(status_i)]}
    return render(request,"1.html",context)

def httx(request,loc):
    location,keywords = LOCATION_LIB[loc]
    return htt(location,request,keywords)