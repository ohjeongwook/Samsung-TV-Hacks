import socket

request = "M-SEARCH * HTTP/1.1\r\n" + \
	"HOST: 239.255.255.250:1900\r\n"+ \
	"MAN: \"ssdp:discover\"\r\n"+ \
	"MX: 1\r\n"+ \
	"ST: urn:samsung.com:device:RemoteControlReceiver:1\r\n"+ \
	"CONTENT-LENGTH: 0\r\n\r\n"

class SSDP:
	def interface_addresses(self,family=socket.AF_INET):
		for fam, _, _, _, sockaddr in socket.getaddrinfo('', None):
			if family == fam:
				yield sockaddr[0]


	def client(self,timeout=5, retries=5):
		socket.setdefaulttimeout(timeout)
		for addr in self.interface_addresses():
			print addr
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
			s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 3)
			s.bind((addr, 1025))
			
			for _ in xrange(5):
				s.sendto(request, ("239.255.255.250", 1900))

			try:
				data, addr = s.recvfrom(100)
				print 'got',data
			except socket.timeout:
				print 'timeout'
			else:
				print 'else',data
		
ssdp=SSDP()
ssdp.client()
