import socket
import struct

MCAST_GRP="239.255.255.250"

request = "M-SEARCH * HTTP/1.1\r\n" + \
	"HOST: 239.255.255.250:1900\r\n"+ \
	"MAN: \"ssdp:discover\"\r\n"+ \
	"MX: 1\r\n"+ \
	"ST: urn:samsung.com:device:RemoteControlReceiver:1\r\n"+ \
	"CONTENT-LENGTH: 0\r\n\r\n"

location = "HTTP/1.1 200 OK\r\n" + \
	"CACHE-CONTROL: max-age=1800\r\n" + \
	"Date: Thu, 01 Jan 1970 00:24:51 GMT\r\n" + \
	"EXT:\r\n" + \
	"LOCATION: http://192.168.1.17:7676/smp_6_\r\n" + \
	"SERVER: SHP, UPnP/1.0, Samsung UPnP SDK/1.0\r\n" + \
	"ST: urn:samsung.com:device:RemoteControlReceiver:1\r\n" + \
	"USN: uuid:0a21fe81-00aa-1000-8787-f47b5e7620f1::urn:samsung.com:device:RemoteControlReceiver:1\r\n" + \
	"Content-Length: 0\r\n"

class SSDP:
	def interface_addresses(self,family=socket.AF_INET):
		print socket.getaddrinfo('', None)
		for fam, a, b, c, sockaddr in socket.getaddrinfo('', None):
			if family == fam:
				yield sockaddr[0]


	def client(self,timeout=5, retries=5):
		socket.setdefaulttimeout(timeout)
		#for addr in self.interface_addresses():
		addr="172.16.0.1"
		if 1==1:
			print addr
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
			s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 3)
			s.bind((addr, 1025))
			
			for _ in xrange(5):
				s.sendto(request, ("239.255.255.250", 1900))

			try:
				data, addr = s.recvfrom(1024)
				print addr
				print data
			except socket.timeout:
				print 'timeout'

	def server(self, timeout=5):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
		s.bind(('', 1900))
		
		mreq = struct.pack('4sl', socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
		s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

		while 1:
			data, addr = s.recvfrom(1024)
			print 'Packet from : ',addr
			print data
			s.sendto(location,addr)
		
	def dummy_server(self, addr, timeout=5):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
		s.bind(('', 1900))
		
		mreq = struct.pack('4sl', socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
		s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

		while 1:
			s.sendto(location,addr)

ssdp=SSDP()
#ssdp.client()
ssdp.server()

