# import ipdb
from ipv4 import *

class Network(object):
    def __init__(self, ip_addr, mask_length):
        """ (str, int) -> """
        self._mask = IpV4Mask(mask_length)
        given_ip = IpV4Address(ip_addr)
        self._ip_addr = IpV4Address(given_ip.int & self._mask.int)

    def __repr__(self):
        return self.address + '/' + str(self._mask.cidr)

    def __eq__(self, network):
        return self.mask == network.mask and self.address == network.address
    
    def __ne__(self, network):
        return not self.__eq__(network)

    def __hash__(self):
        return hash(self.address) ^ hash(self.mask)

    def __contains__(self, address):
        return self.contains(address)

    @property
    def address(self):
        """ () -> str """
        return self._ip_addr.str
        # return self._ip_addr

    @property
    def mask(self):
        """ () -> str """
        return self._mask.str
        # return self._mask

    @property
    def mask_length(self):
        """ () -> int """
        return self._mask.cidr
    
    @property
    def broadcast_address(self):
        """ () -> str """
        broadcast = IpV4Address(self._ip_addr.int | ( ~ self._mask.int & 0xffffffff))

        return broadcast.str

    @property
    def first_usable_address(self):
        """ () -> str """
        if self._mask.cidr == 32:
            return self._ip_addr.str
        elif self._mask.cidr == 31:
            return None
        else:
            first = IpV4Address(self._ip_addr.int + 1)
            
            return first.str

    @property
    def last_usable_address(self):
        """ () -> str """
        if self._mask.cidr == 32:
            return self._ip_addr.str
        elif self._mask.cidr == 31:
            return None
        else:
            last = IpV4Address(self.broadcast_address)
            last.int -= 1

            return last.str

    @property
    def total_hosts(self):
        """ () -> int """
        if self._mask.cidr == 32: return 1
        else: return 2 ** (32 - self._mask.cidr) - 2

    def contains(self, ip_addr):
        """ (str) -> bool """
        return self._ip_addr.int == IpV4Address(ip_addr).int & self._mask.int

    def is_public(self):
        """ () -> bool """
        net1 = Network('10.0.0.0', 8)
        net2 = Network('172.16.0.0', 12)
        net3 = Network('192.168.0.0', 16)

        return not((self.address in net1) or (self.address in net2) or (self.address in net3))
        # return not self.address in net3

    def get_subnets(self):
        """() -> [ Network, Network ] """
        subnets_mask = IpV4Mask(self._mask.cidr + 1)
        subnets_ip = self._ip_addr
        
        index = self._mask.cidr / 8
        step = 256 - ( subnets_mask.list[index] )
        # ipdb.set_trace()
        # ((self.int >> 8) & 255)
        first = Network(subnets_ip.str, subnets_mask.cidr)
        octets = subnets_ip.list
        octets[index] += step
        subnets_ip = IpV4Address(octets)
        second = Network(subnets_ip.str, subnets_mask.cidr)
        
        return [first, second]

if __name__ == "__main__":
    print "\nCreating some nets..."
    
    try:
        net = Network('256.168.220.45', 23)
    except:
        net = Network('192.168.220.45', 23)
        # net = Network('192.168.220.0', 0)

    print 'Address: ' + net.address
    print 'Mask: ' + net.mask
    print 'Mask length: ' + str(net.mask_length)
    print 'Broadcast: ' + net.broadcast_address
    print 'First usable address in ' + net.address + ' is ' + net.first_usable_address
    print 'Last usable address in ' + net.address + ' is ' + net.last_usable_address
    print 'Total hosts in ' + net.address + ' is ' + str(net.total_hosts)
    print '192.168.221.78 in ' + net.address + '? :', net.contains('192.168.221.78')
    print '192.168.0.78 in ' + net.address + '? :', net.contains('192.168.0.78')
    print 'Network ' + net.address + ' is public? :', net.is_public()
    
    print "\nSubnets:"
    subnets = net.get_subnets()
    print subnets[0]
    print subnets[1]
    print 'Broadcast: ' + subnets[0].broadcast_address
    print 'First usable address in ' + subnets[0].address + ' is ' + subnets[0].first_usable_address
    print 'Last usable address in ' + subnets[0].address + ' is ' + subnets[0].last_usable_address
    print 'Total hosts in ' + subnets[0].address + ' is ' + str(subnets[0].total_hosts)

    print '\nBroadcast: ' + subnets[1].broadcast_address
    print 'First usable address in ' + subnets[1].address + ' is ' + subnets[1].first_usable_address
    print 'Last usable address in ' + subnets[1].address + ' is ' + subnets[1].last_usable_address
    print 'Total hosts in ' + subnets[1].address + ' is ' + str(subnets[1].total_hosts)