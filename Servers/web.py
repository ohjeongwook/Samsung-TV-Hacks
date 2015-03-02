import SocketServer

resp01="""HTTP/1.1 200 OK\r\n\
CONTENT-LANGUAGE: UTF-8\r\n\
CONTENT-TYPE: text/xml; charset="utf-8"\r\n\
CONTENT-LENGTH: %d\r\n\
Date: Thu, 01 Jan 1970 00:01:13 GMT\r\n\
connection: close\r\n\
Application-URL: http://172.16.0.1:80/ws/app/\r\n\
SERVER: SHP, UPnP/1.0, Samsung UPnP SDK/1.0\r\n\
\r\n"""

resp01_body="""<?xml version="1.0"?>\r\n\
<root xmlns='urn:schemas-upnp-org:device-1-0' xmlns:sec='http://www.sec.co.kr/dlna' xmlns:dlna='urn:schemas-dlna-org:device-1-0'>\r\n\
 <specVersion>\r\n\
  <major>1</major>\r\n\
  <minor>0</minor>\r\n\
 </specVersion>\r\n\
 <device>\r\n\
  <deviceType>urn:samsung.com:device:RemoteControlReceiver:1</deviceType>\r\n\
  <friendlyName>[TV]Samsung LED56</friendlyName>\r\n\
  <manufacturer>Samsung Electronics</manufacturer>\r\n\
  <manufacturerURL>http://www.samsung.com/sec</manufacturerURL>\r\n\
  <modelDescription>Samsung TV RCR</modelDescription>\r\n\
  <modelName>UN55F6300</modelName>\r\n\
  <modelNumber>1.0</modelNumber>\r\n\
  <modelURL>http://www.samsung.com/sec</modelURL>\r\n\
  <serialNumber>20090804RCS</serialNumber>\r\n\
  <UDN>uuid:0a21fe81-00aa-1000-8787-f47b5e7620f1</UDN>\r\n\
  <sec:deviceID>BDCHCBZODCVXU</sec:deviceID>\r\n\
  <sec:ProductCap>Resolution:1920X1080,ImageZoom,ImageRotate,Y2013</sec:ProductCap>\r\n\
  <serviceList>\r\n\
   <service>\r\n\
    <serviceType>urn:samsung.com:service:MultiScreenService:1</serviceType>\r\n\
    <serviceId>urn:samsung.com:serviceId:MultiScreenService</serviceId>\r\n\
    <controlURL>/smp_8_</controlURL>\r\n\
    <eventSubURL>/smp_9_</eventSubURL>\r\n\
    <SCPDURL>/smp_7_</SCPDURL>\r\n\
   </service>\r\n\
  </serviceList>\r\n\
 </device>\r\n\
</root>"""

class MyTCPHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		self.data = self.request.recv(1024)
		print self.data
		self.request.sendall(resp01 % len(resp01_body) + resp01_body)

if __name__ == "__main__":
	HOST, PORT = "", 7676

	server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
	server.serve_forever()
