import csv
import time
import json
import sys
import random
sys.path.append('...')
import config
TIME_ZONE = config.TIME_ZONE

def updateInfo(csv_path,interval_m,comparator,weight_adder,keywords):
    current_time = time.time()
    total_dict = {}         #store total number for each AP
    current_dict = {} 
    total_count = {}         #store total number for each AP
    current_count = {}
    total_avg = {}
    total_max = {}
    current_avg = {}
    tghz_avg = {}
    current_tghz = {}
    keystring = str(interval_m)+"_"
    for keyword in keywords:
        keystring = keystring + keyword + "_"
    with open(csv_path, "r", encoding = "utf-8") as f:
        reader = csv.reader(f)
        for i in reader:
            pointed = False
            for keyword in keywords:
                if keyword in i[2]:
                    print(keyword)
                    pointed = True
                    break
            if pointed:
                ap_time = time.mktime(time.strptime(i[0],"%Y-%m-%d %H:%M:%S"))-TIME_ZONE*3600
                ap_name = i[2]
                ap_num = int(i[5])
                if ap_name in total_dict:
                    total_dict[ap_name] += ap_num
                    total_count[ap_name] += 1
                    if(ap_num>total_max[ap_name]):
                        total_max[ap_name]=ap_num
                else:
                    total_dict[ap_name] = ap_num
                    total_max[ap_name] = ap_num
                    total_count[ap_name] = 1
                print(i[0],(ap_time-current_time)//60)
                if comparator(ap_time,interval_m):
                    ap_tghz = int(i[3])
                    if ap_name in current_dict:
                        current_dict[ap_name] += ap_num*weight_adder(ap_time)
                        current_tghz[ap_name] += ap_tghz*weight_adder(ap_time)
                        current_count[ap_name] += 1*weight_adder(ap_time)
                    else:
                        current_dict[ap_name] = ap_num*weight_adder(ap_time)
                        current_tghz[ap_name] = ap_tghz*weight_adder(ap_time)
                        current_count[ap_name] = 1*weight_adder(ap_time)
        f.close()
    for ap in total_dict.keys():
        total_avg[ap] = total_dict[ap]//total_count[ap]
    for ap in current_dict.keys():
        current_avg[ap] = current_dict[ap]//current_count[ap]
        tghz_avg[ap] = current_tghz[ap]//current_count[ap]
        print(current_tghz[ap],current_count[ap],tghz_avg[ap])
    with open(keystring+"total_avg.log","w") as f:
        f.write(str(current_time)+'\n')
        f.write(json.dumps(total_avg))
        f.close()
    with open(keystring+"total_max.log","w") as f:
        f.write(str(current_time)+'\n')
        f.write(json.dumps(total_max))
        f.close()
    with open(keystring+"current_avg.log","w") as f:
        f.write(str(current_time)+'\n')
        f.write(json.dumps(current_avg))
        f.close()
    with open(keystring+"tghz_avg.log","w") as f:
        f.write(str(current_time)+'\n')
        f.write(json.dumps(tghz_avg))
        f.close()



def getInfo(csv_path,interval_m,update_m,comparator,weight_adder,keywords):
    keystring = str(interval_m)+"_"
    update_int = update_m * 60
    tghz_avg = {}
    current_avg = {}
    total_avg = {}
    for keyword in keywords:
        keystring = keystring + keyword + "_"
    current_time = time.time()
    while True:
        try:
            with open(keystring+"total_avg.log","r") as f:
                try:
                    prev_t = float(f.readline().strip())
                except:
                    updateInfo(csv_path,interval_m,comparator,weight_adder,keywords)
                    continue
                if(current_time-prev_t<update_int):
                    total_avg = json.loads(f.read())
                    break
                else:
                    updateInfo(csv_path,interval_m,comparator,weight_adder,keywords)
        except FileNotFoundError:
            updateInfo(csv_path,interval_m,comparator,weight_adder,keywords)
    current_time = time.time()
    while True:
        try:
            with open(keystring+"total_max.log","r") as f:
                try:
                    prev_t = float(f.readline().strip())
                except:
                    updateInfo(csv_path,interval_m,comparator,weight_adder,keywords)
                    continue
                if(current_time-prev_t<update_int):
                    total_max = json.loads(f.read())
                    break
                else:
                    updateInfo(csv_path,interval_m,comparator,weight_adder,keywords)
        except FileNotFoundError:
            updateInfo(csv_path,interval_m,comparator,weight_adder,keywords)
    while True:
        try:
            with open(keystring+"current_avg.log","r") as f:
                prev_t = float(f.readline().strip())
                if(current_time-prev_t<update_int):
                    current_avg = json.loads(f.read())
                    break
                else:
                    updateInfo(csv_path,interval_m,comparator,weight_adder,keywords)
        except FileNotFoundError:
            updateInfo(csv_path,interval_m,comparator,weight_adder,keywords)
    while True:
        try:
            with open(keystring+"tghz_avg.log","r") as f:
                prev_t = float(f.readline().strip())
                if(current_time-prev_t<update_int):
                    tghz_avg = json.loads(f.read())
                    break
                else:
                    updateInfo(csv_path,interval_m,comparator,weight_adder,keywords)
        except FileNotFoundError:
            updateInfo(csv_path,interval_m,comparator,weight_adder,keywords)

    return total_avg,current_avg,tghz_avg, total_max




def view_info(path,interval,updateint,comparator,weight_adder,keywords):
    total_avg,current_avg,tghz_avg, total_max = getInfo(path,interval,updateint,comparator,weight_adder,keywords)
    load_a_sum = 0.0
    load_m_sum = 0.0
    client_sum = 1
    ap_list = []
    for ap in current_avg.keys():   
        load_a_sum += current_avg[ap]/total_avg[ap]
        load_m_sum += current_avg[ap]/total_max[ap]
        client_sum += current_avg[ap]
        ap_list.append({"name":ap,"connection":str(current_avg[ap]),
        "tghz":str(tghz_avg[ap]),"fghz":str(current_avg[ap]-tghz_avg[ap]),"history":str(total_avg[ap])})
    
    if len(current_avg.keys()):
        client_avg = client_sum//len(current_avg.keys())
        load_by_avg = int(load_a_sum*100/len(current_avg.keys()))
        load_by_max = int(load_m_sum*100/len(current_avg.keys()))
        if(client_sum < 10 or load_by_avg ==load_by_max):
            # when the total client number is positive but quite small
            # or when maximum load equals avg load,
            # it means that it is not accurate to indicate people load
            # by ratio, so ABSOLUTE VALUE should be used instead
            load = config.absolute_calculator(client_avg)
        else:
            load = config.load_calculator(load_by_max,load_by_avg)
    else:
        load = 0
    return load,ap_list
    
