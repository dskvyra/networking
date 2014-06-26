from network import *

class Route:
	def __init__(self, given_network, gateway, interface_name, metric):
		""" (network, string, string, int) -> () """
		if str(given_network.__class__) == 'network.Network':
			self._network = given_network
		else:
			raise TypeError
		if gateway == None:
			self._gateway = IpV4Address(0)
		else:
			self._gateway = IpV4Address(gateway)
		if type(interface_name) is str:
			self._interface = interface_name
		else:
			raise TypeError
		if type(metric) is int and metric > 0:
			self._metric = metric
		else:
			raise TypeError

	def __repr__(self):
		if self._gateway.int == 0:
			represent = 'net: %s, interface: %s, metric: %s' % (str(self.network), self.interface_name, str(self.metric))
		else:
			represent = 'net: %s, gateway: %s, interface: %s, metric: %s' % (str(self.network), self.gateway, self.interface_name, str(self.metric))
		
		return represent

	def __eq__(self, route):
		return str(self.network) == str(route.network) and self.gateway == route.gateway \
		and self.interface_name == route.interface_name and self.metric == route.metric
	
	def __ne__(self, route):
		return not self.__eq__(route)

	def __hash__(self):
		return hash(self.network) ^ hash(self.gateway) ^ hash(self.interface_name) ^ hash(self.metric)

	@property
	def gateway(self):
		""" () -> string """
		return self._gateway.str

	@property
	def interface_name(self):
		""" () -> string """
		return self._interface
	
	@property
	def metric(self):
		""" () -> int """
		return self._metric

	@property
	def network(self):
		""" () -> Network """
		return self._network

if __name__ == "__main__":
	net = Network('192.168.220.0', 23)
	route = Route(net, '192.168.220.5', 'bge0', 5)
	route2 = Route(net, '192.168.220.5', 'bge0', 5)
	print route
	print route.network
	print route.interface_name
	print route.metric
	print route.network
	print "route == route2 is %s" % (route == route2)
