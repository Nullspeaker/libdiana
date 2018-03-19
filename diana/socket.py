import socket
from . import packet

BLOCKSIZE = 4096

def connect(host, port=2010, connect=socket.create_connection):
	sock = connect((host, port))
	def tx(pack):
		sock.send(packet.encode(pack))
	def rx():
		buf = b''
		while True:
			data = sock.recv(BLOCKSIZE)
			buf += data
			try:
				packets, buf = packet.decode(data)
			except ValueError:
				print("Value Error! Packet problems!")
				continue
			for received_packet in packets:
				yield received_packet
	return tx, rx()

