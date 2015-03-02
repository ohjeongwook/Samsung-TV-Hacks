import socket
import base64
import struct
import pprint
import time

class Remote:
	def __init__(self,host,port):
		print 'Initializing Connection...'
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((host, port))

	def hello(self):		
		self.sock.send('\x01\x14\x00' + 'iphone..iapp.samsung' + '\x02\x00\x78\x00')
		data = self.sock.recv(1024)
		print data

	def auth(self,ip='',hostname='',mac=''):
		print 'Auth...'
		encoded_ip=base64.b64encode(ip)
		encoded_mac=base64.b64encode(mac)
		encoded_hostname=base64.b64encode(hostname)

		auth_body= '\x64\x00' + \
			struct.pack('H',len(encoded_ip)) + \
			encoded_ip + \
			struct.pack('H',len(encoded_mac)) + \
			encoded_mac + \
			struct.pack('H',len(encoded_hostname)) + \
			encoded_hostname
		
		auth_head='\x01\x14\x00' + 'iphone..iapp.samsung' + \
			struct.pack('H',len(auth_body))
		auth_str = auth_head + auth_body
		
		self.sock.send(auth_str)
		
		data = self.sock.recv(1024)
		pprint.pprint(data)

	def key(self,str):
		encoded_str=base64.b64encode(str)
		key_body= '\x00\x00\x00' + struct.pack('H',len(encoded_str)) + encoded_str
		key_head='\x01\x1d\x00' + 'iphone.UN55F6300.iapp.samsung' + \
			struct.pack('H',len(key_body))
		key_str = key_head + key_body
		
		print 'Sending key', str
		print '\t', pprint.pformat(key_str)
		self.sock.send(key_str)
		data,addr = self.sock.recvfrom(1024)
		time.sleep(0.5)

	def __fini__(self):
		self.sock.close()

if __name__=='__main__':
	import sys

	operation=sys.argv[1]
	HOST = sys.argv[2]
	PORT = 55000
	ip=sys.argv[3]
	hostname=sys.argv[4]
	mac=sys.argv[5]

	remote = Remote(HOST,PORT)
	remote.hello()
	remote.auth(ip,hostname,mac)

	if operation=='enter':
		remote.key('KEY_ENTER')
	if operation=='right':
		remote.key('KEY_RIGHT')
	elif operation=='exit':
		remote.key('KEY_EXIT')
		remote.key('KEY_EXIT')
		remote.key('KEY_EXIT')

	elif operation=='smart_hub':
		remote.key('KEY_MUTE')

	elif operation=='enter_sync_ip':
		remote.key('KEY_DOWN')
		remote.key('KEY_DOWN')
		remote.key('KEY_DOWN')
		remote.key('KEY_DOWN')
		remote.key('KEY_ENTER')	

		time.sleep(4)
		remote.key('KEY_UP')
		remote.key('KEY_RIGHT')
		remote.key('KEY_RIGHT')
		remote.key('KEY_RIGHT')
		remote.key('KEY_ENTER')
		
		remote.key('KEY_DOWN')
		remote.key('KEY_DOWN')
		remote.key('KEY_DOWN')
		remote.key('KEY_DOWN')
		remote.key('KEY_DOWN')
		remote.key('KEY_ENTER')

		remote.key('KEY_1')	
		remote.key('KEY_9')	
		remote.key('KEY_2')	
		remote.key('KEY_RIGHT')	
		remote.key('KEY_1')	
		remote.key('KEY_6')	
		remote.key('KEY_8')	
		remote.key('KEY_RIGHT')
		remote.key('KEY_1')	
		remote.key('KEY_RIGHT')	
		remote.key('KEY_2')	
		remote.key('KEY_0')	
		remote.key('KEY_2')	
		remote.key('KEY_ENTER')

	elif operation=='start_sync':
		remote.key('KEY_UP')
		remote.key('KEY_ENTER')

	elif operation=='change_dns':
		#Menu
		remote.key('KEY_MENU')

		#Go to Network Status menu item
		remote.key('KEY_DOWN')
		remote.key('KEY_DOWN')
		remote.key('KEY_DOWN')

		#Select to Network Status panel
		remote.key('KEY_ENTER')
		remote.key('KEY_ENTER')
		remote.key('KEY_LEFT')
		remote.key('KEY_LEFT')

		#Push button for IP Settings
		remote.key('KEY_ENTER')

		#IP Setting -> DNS
		remote.key('KEY_DOWN')
		remote.key('KEY_DOWN')
		remote.key('KEY_DOWN')
		remote.key('KEY_DOWN')
	
		#Chose DNS Server
		remote.key('KEY_ENTER')

		remote.key('KEY_1')	
		remote.key('KEY_RIGHT')	
		remote.key('KEY_1')	
		remote.key('KEY_RIGHT')
		remote.key('KEY_1')	
		remote.key('KEY_RIGHT')	
		remote.key('KEY_1')	
		remote.key('KEY_ENTER')	
		remote.key('KEY_DOWN')
	

		#Close Network Status
		remote.key('KEY_ENTER')	
		remote.key('KEY_EXIT')	
		remote.key('KEY_EXIT')	
		remote.key('KEY_EXIT')
	
