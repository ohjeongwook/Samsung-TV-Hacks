import httplib, urllib2


class TVControl:
	def __init__(self,hostname):
		self.Hostname=hostname

	def SendSOAP(self,method,body):
		print '*',method

		headers = {
			"Content-type": 'text/xml;charset="utf-8"', 
			"SOAPACTION": '"urn:samsung.com:service:MainTVAgent2:1#%s"' % method
		}

		conn = httplib.HTTPConnection(self.Hostname)
		conn.request("POST", "/smp_4_", body, headers)

		response = conn.getresponse()
		print(response.status, response.reason)

		data = response.read()

		print data
		print ''

		return data

	def GetSourceList(self):
		body='<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'+\
				'<s:Body>'+\
					'<u:GetSourceList xmlns:u="urn:samsung.com:service:MainTVAgent2:1"></u:GetSourceList>'+\
				'</s:Body>'+\
			'</s:Envelope>'
		self.SendSOAP('GetSourceList',body)

	def GetCurrentMainTVChannel(self):
		body='<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'+\
			 	'<s:Body>'+\
			 		'<u:GetCurrentMainTVChannel xmlns:u="urn:samsung.com:service:MainTVAgent2:1"></u:GetCurrentMainTVChannel>'+\
			 	'</s:Body>'+\
			 '</s:Envelope>'
		self.SendSOAP('GetCurrentMainTVChannel',body)

	def GetCurrentExternalSource(self):
		body='<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'+\
				'<s:Body>'+\
					'<u:GetCurrentExternalSource xmlns:u="urn:samsung.com:service:MainTVAgent2:1"></u:GetCurrentExternalSource>'+\
				'</s:Body>'+\
			'</s:Envelope>'
		self.SendSOAP('GetCurrentExternalSource',body)

	def SendMBRIRKey(self):
		body='<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'+\
				'<s:Body>'+\
					'<u:SendMBRIRKey xmlns:u="urn:samsung.com:service:MainTVAgent2:1">'+\
						'<MBRDevice>STB</MBRDevice>'+\
						'<MBRIRKey>0x01</MBRIRKey>'+\
						'<ActivityIndex>0</ActivityIndex>'+\
					'</u:SendMBRIRKey>'+\
				'</s:Body>'+\
			'</s:Envelope>'
		self.SendSOAP('SendMBRIRKey',body)

	def StartCloneView(self):
		body='<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'+\
			'<s:Body>'+\
				'<u:StartCloneView xmlns:u="urn:samsung.com:service:MainTVAgent2:1">'+\
					'<ForcedFlag>Normal</ForcedFlag>'+\
					'<DRMType>PrivateTZ</DRMType>'+\
				'</u:StartCloneView>'+\
			'</s:Body></s:Envelope>'
		self.SendSOAP('StartCloneView',body)

	def GetLiveStream(self,url):
		req = urllib2.urlopen(url)
		
		while True:
			chunk = req.read(512)
			if not chunk:
				break
			print len(chunk)

	def GetAvailableActions(self):
		body='<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'+\
				'<s:Body>'+\
					'<u:GetAvailableActions xmlns:u="urn:samsung.com:service:MainTVAgent2:1"></u:GetAvailableActions>'+\
				'</s:Body>'+\
			'</s:Envelope>'
		self.SendSOAP('GetAvailableActions',body)		

	def RunBrowser(self):
		body='<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'+\
				'<s:Body>'+\
					'<u:RunBrowser xmlns:u="urn:samsung.com:service:MainTVAgent2:1"></u:RunBrowser>'+\
				'</s:Body>'+\
			'</s:Envelope>'
		self.SendSOAP('RunBrowser',body)			

	def GetCurrentBrowserURL(self):
		body='<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'+\
				'<s:Body>'+\
					'<u:GetCurrentBrowserURL xmlns:u="urn:samsung.com:service:MainTVAgent2:1"></u:GetCurrentBrowserURL>'+\
				'</s:Body>'+\
			'</s:Envelope>'
		self.SendSOAP('GetCurrentBrowserURL',body)	

tvcontrol=TVControl("192.168.1.9:7676")

tvcontrol.GetAvailableActions()

tvcontrol.GetSourceList()
tvcontrol.GetCurrentExternalSource()
tvcontrol.SendMBRIRKey()
tvcontrol.StartCloneView()

tvcontrol.GetLiveStream('http://192.168.1.9:9090/liveStream/1')
