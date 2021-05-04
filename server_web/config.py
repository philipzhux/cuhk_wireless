import time
import random
# constant setting goes here
TIME_ZONE = +8
LOCATION_LIB = [("1/F University Library",["UL-1F"]),("5/F University Library",["UL-5F"]),("2/F University Library",["UL-2F"]),("3/F University Library",["UL-3F"]),
("4/F University Library",["UL-4F"]),("3/F Startup Library",["5D-3F"]),("1/F Startup Library",["5D-1F"]),("4/F Startup Library",["5D-4F"])
,("Upper Campus Study Room",["PZ-2F"]),("Liwen Hall",["5D-2F"])]
CSV_PATH = "/Users/philip/Downloads/wireless_record.csv"
INTERVAL = 20
CACHE_INTERVAL = 3
COLOR_LIST = ["#05fc43","#05fc43","#9400d3","#fc031c"]
STATUS_LIST = ["Quiet","Comfortable","Slightly Crowded","Crowded"]

# function object goes here
def comparator(ap_time,interval):
    predict_para = 1
    current_time = time.time()
    diff = current_time-ap_time
    return ((diff+86400*predict_para)%(86400*predict_para)<interval*60 or abs(diff-86400*predict_para)%(86400*predict_para)<interval*60)

def weight_adder(ap_time):
    weight = 25
    current_time = time.time()
    current_day = current_time//86400
    ap_day = ap_time//86400
    diff_day = abs(current_day-ap_day)
    week_offset = diff_day%7
    if(week_offset==0):
        weight+=25
        if(diff_day==0):
            weight+=50
    return weight

def status_converter(load):
    return load//26

def load_calculator(load_by_max,load_by_avg):
    print(load_by_max)
    print(load_by_avg)
    return max(0,int(load_by_max*0.88262526-0.00297941))

def absolute_calculator(avg_client):
    if(avg_client<10):
        return random.randint(16,30)
    elif(avg_client<20):
        return random.randint(25,40)
    else:
        return min(int(avg_client*3.5-45),random.randint(96,99)) 
    
    # with a large avg_client it is unlikely to use the absolute calculator
    # except for the first time any data is captured
    # so this calculation may be very rough, but has a very limited on the 
    # overall result