import csv
import socket
import json
import _thread as thread
import urllib.parse
SERVER_PORT = 12367

def get_term(org,text):
    start = org.find(text) + len(text)
    end = org.find('\n',start)
    return org[start:end]

def get_term_s(org,text):
    start = org.find(text) + len(text)
    end = org.find(' \n',start)
    return org[start:end]

def on_new_client(clientsocket,addr):
    while True:
        byt = clientsocket.recv(1024)
        text = byt.decode()
        start = text.find("x: ") + 3
        end = text.find('\n',start)
        text = urllib.parse.unquote_plus(text[start:end])
        if not ("AP" in text):
            break
        print(get_term(text,"AP Name:"))
        try:
            info = {"Time": get_term_s(text,"Time : "),
            "Location": get_term(text,"Location : "),
            "AP": get_term_s(text,"AP Name:"),
            "2.4 GHz": int(get_term(text,"STA_2G:")),
            "5 GHz": int(get_term(text,"STA_5G:")),
            "Total": int(get_term(text,"STA_2G:"))+int(get_term(text,"STA_5G:")),
            "Account": get_term(text,"Account : "),}
        except:
            break
        if ("No records found" in info['Location']) and ("UL" in info["AP"]):
            info["Location"] = "University Library"
        with open('wireless_record.csv', mode='a') as csv_file:
            fieldnames = ["Time", "Location", "AP","2.4 GHz","5 GHz","Total","Account"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow(info)
        break
    clientsocket.close()

def main():
    s = socket.socket()         
    port = SERVER_PORT                
    s.bind(('', port))         
    s.listen(5)     
    while True: 
        c, addr = s.accept()     
        thread.start_new_thread(on_new_client,(c,addr))
    s.close()

main()