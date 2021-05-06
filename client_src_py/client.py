from CUHK.Wireless import Wireless
import applescript, time, csv, os, socket, json, re, sys
SERVER = "138.128.215.15"
SERVER_PORT = 12335

def mac_on_boot():
	## Exclusivly for MacOS App Bundle; Start
	b = sys.executable
	for i in range(3):
		b = os.path.dirname(b)
	applescript.tell.app("System Events",'make new login item at end of login items with properties {path:"'+b+'"}',background=True)
	## Exclusivly for MacOS App Bundle; End

def win_on_boot():
	pass

def main():
	mac_on_boot()
	# win_on_boot()
	collector = Wireless()
	host = SERVER
	port = SERVER_PORT
	while True:
		try:
			collector.refresh()
		except:
			time.sleep(5*60)
			continue
		if collector.check():
			try:
				msg =  json.dumps(collector.getAll())
				if "AP" in msg:	
					c = socket.socket()
					c.connect((host, port))
					byt = msg.encode()
					c.send(byt)
					c.close() 
			except:
				pass
		time.sleep(4*60)

main()