from . import packet as p

class Tracker:
	def __init__(self):
		self.objects = {}
		self._observers = []
		
	def bind_to_updates(self,callback):
		self._observers.append(callback)

	@property
	def player_ship(self):
		for _obj in self.objects.values():
			if _obj['type'] == p.ObjectType.player_vessel:
				return _obj
		return {}

	def update_object(self, record):
		try:
			oid = record['object']
		except KeyError:
			return
		else:
			self.objects.setdefault(oid, {}).update(record)
			for callback in self._observers:
				callback(oid)

	def remove_object(self, oid):
		try:
			del self.objects[oid]
		except KeyError:
			pass

	def rx(self, packet):
		if isinstance(packet, p.ObjectUpdatePacket):
			for record in packet.records:
				self.update_object(record)
		elif isinstance(packet, p.DestroyObjectPacket):
			self.remove_object(packet.object)
		elif isinstance(packet, p.IntelPacket):
			self.update_object({'object': packet.object,'type': p.ObjectType.other_ship, 'intel': packet.intel})

