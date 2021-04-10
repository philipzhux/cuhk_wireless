import requests
import sys
class Wireless:
	def __init__(self):
		self.got = False
		try:
			r = requests.get('https://nt-r.cuhk.edu.cn')
			self.got = True
			self.t = r.text
		except:
			pass
	def refresh(self):
		i=0
		self.fail = True
		while True:
			try:
				r = requests.get('https://nt-r.cuhk.edu.cn')
				self.got = True
				self.t = r.text
				self.fail = False
				break
			except:
				i=i+1
				if i>4:
					print("\nTimeout when connecing to CUHK wireless system, please check whether you are connected to campus WiFi\n")
					break
	def getAny(self,name):
		i=0
		if(not self.got):
			self.refresh()
		if(self.fail):
			return
		t=self.t
		start = t.find(name+":<b>")+len(name+":<b>")
		end = end = t.find("</b>",start)
		return t[start:end];
	def getAnySpace(self,name):
		if(not self.got):
			self.refresh()
		if(self.fail):
			return
		t=self.t
		start = t.find(name+" : <b>")+len(name+" : <b>")
		end = end = t.find("</b>",start)
		return t[start:end];
	def getAnyStrong(self,name):
		if(not self.got):
			self.refresh()
		if(self.fail):
			return
		t=self.t
		start = t.find(name+" : <strong>")+len(name+" : <strong>")
		end = end = t.find("</strong>",start)
		return t[start:end];
	def getAP(self):
		if(not self.got):
			self.refresh()
		if(self.fail):
			return
		return self.getAny("AP Name")
	def getLoc(self):
		if(not self.got):
			self.refresh()
		if(self.fail):
			return
		return self.getAnySpace("Location")
	def getAccount(self):
		if(not self.got):
			self.refresh()
		if(self.fail):
			return
		return self.getAnySpace("Account")
	def getTime(self):
		if(not self.got):
			self.refresh()
		if(self.fail):
			return
		return self.getAnyStrong("Time")
	def getTg(self):
		if(not self.got):
			self.refresh()
		if(self.fail):
			return
		try:
			return int(self.getAny("STA_2G"))
		except:
			return

	def getFg(self):
		if(not self.got):
			self.refresh()
		if(self.fail):
			return
		try:
			return int(self.getAny("STA_5G"))
		except:
			return
	def getNum(self):
		if(not self.got):
			self.refresh()
		if(self.fail):
			return
		return self.getTg()+self.getFg()


	def getAll(self):
		if(not self.got):
			self.refresh()
		if(self.fail):
			return
		return {"Time":self.getTime(),"Location":self.getLoc(),"AP":self.getAP(),"2.4 GHz":self.getTg(),"5 GHz":self.getFg(),"Total":self.getNum(),"Account":self.getAccount()}

	def check(self):
		return (not self.fail)

