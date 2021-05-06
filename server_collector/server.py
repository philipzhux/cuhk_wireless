import csv
import socket
import json
import _thread as thread
SERVER_PORT = 12335

def on_new_client(clientsocket,addr):
    while True:
        byt = clientsocket.recv(1024)
        text = byt.decode()
        if not ("AP" in text):
            break
        print(text)
        info = json.loads(text)
        if ("No records found" in info['Location']) and ("UL" in info["AP"]):
            info["Location"] = "University Library"
        with open('wireless_record.csv', mode='a') as csv_file:
            fieldnames = ["Time", "Location", "AP","2.4 GHz","5 GHz","Total","Account"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow(info)
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