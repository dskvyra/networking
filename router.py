from route import *
from sets import Set


class TableEmpty(Exception): pass

class Router(object):
	def __init__(self, routes):
		"""([Route,]) ->"""
		if type(routes) is not Set:
			raise TypeError
		elif routes == []:
			raise TableEmpty
		self._table = routes

	def add_route(self, route):
		"""(Route) ->"""
		self._table.add(route)

	def get_route_for_address(self, address):
		"""(str) -> Route"""
		dest = IpV4Address(address)
		best_route = None
		longest_cidr = 0
		
		for route in self._table:
			# best encapsulation ever!
			# but my props network.mask and network.adress requested in string
			# let it be
			dest_net = IpV4Address(dest.int & route.network._mask.int)
			net_in_table = IpV4Address(route.network._ip_addr.int & route.network._mask.int)
			if dest_net.int == net_in_table.int and route.network._mask.cidr >= longest_cidr:
				best_route = route
				longest_cidr = route.network._mask.cidr
			# ipdb.set_trace()
			# fu metric

		return best_route

	@property
	def routes(self):
		"""() -> [Route,]"""
		return self._table

	def remove_route(self, route):
		"""(Route) ->"""
		try:
			self._table.remove(route)
		except:
			print "don't have route like yours"

if __name__ == '__main__':
	routes = Set([\
	Route(Network("192.168.220.0", 23), None, "bge0", 10),\
	Route(Network("0.0.0.0", 0), "192.168.220.5", "bge0", 10),\
	Route(Network("192.168.220.0", 24), None, "bge0", 10),\
	Route(Network("192.168.221.0", 24), None, "bge0", 10),\
	Route(Network("193.110.0.0", 16), "193.110.162.165", "bge1", 10),\
	Route(Network("193.110.162.0", 24), None, "bge1", 10)\
	])

	router = Router(routes)

	for route in router.routes:
		print route

	router.remove_route(Route(Network("193.110.162.0", 24), None, "bge1", 10))
	router.remove_route(Route(Network("193.110.162.0", 24), None, "bge1", 10))
	print "\nAfter remove_route():"

	for route in router.routes:
		print route

	print "\nAdding route:"
	router.add_route(Route(Network("193.110.162.0", 24), None, "bge1", 10))

	for route in router.routes:
		print route

	print "\nBest route for 192.168.221.178 is:"
	print router.get_route_for_address('192.168.221.178')