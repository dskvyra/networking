# -*- coding: utf-8 -*-
# import ipdb

class IncorrectIpAddress(Exception): pass
class IncorrectLength(Exception): pass

max_int = 4294967295

#place for dict: cidr->int and back 

class IpV4Address(object):
    def __init__(self, ip_addr):
        self._int = self.__to_valid(ip_addr)
        
    def __repr__(self):
        return self.str

    @property
    def list(self):
        octets = [int((self.int >> 24) & 255),\
                int((self.int >> 16) & 255), int((self.int >> 8) & 255),\
                int(self.int  & 255)]

        return octets

    @property
    def str(self):
        str_ip = '.'.join([str(octet) for octet in self.list])

        return str_ip

    @property
    def int(self):
        return self._int

    def __to_valid(self, ip_addr_to_check):
        """
        (int) -> int
        (list) -> int
        (tuple) -> int
        (str) -> int
        """
        octets = []

        if type(ip_addr_to_check) is int or type(ip_addr_to_check) is long:
            if ip_addr_to_check > max_int or ip_addr_to_check < 0:
                raise IncorrectIpAddress
            return ip_addr_to_check
        elif type(ip_addr_to_check) is list:
            octets = ip_addr_to_check
        elif type(ip_addr_to_check) is tuple:
            octets = list(ip_addr_to_check)
        elif type(ip_addr_to_check) is str:
            octets = [int(octet) for octet in ip_addr_to_check.split('.')]
        else:
            raise TypeError

        if len(octets) < 4:
            for i in range(0, 4 - len(octets)):
                octets.append(0)
        elif len(octets) > 4:
            raise IncorrectIpAddress

        for octet in octets:
            if int(octet) > 255 or int(octet) < 0:
                raise IncorrectIpAddress

        int_ip = int(octets[0]) * pow(2, 24) \
                + int(octets[1]) * pow(2, 16) \
                + int(octets[2]) * pow(2, 8) \
                + int(octets[3])

        return int_ip

class IncorrectMask(Exception): pass

class IpV4Mask(IpV4Address):
    def __init__(self, netmask):
        if type(netmask) is int and netmask <= 32 and netmask >= 0:
            self._cidr = netmask
            IpV4Address.__init__(self, max_int - (2 ** (32 - netmask) - 1))
        elif type(netmask) is int and netmask < 2147483648:
            raise IncorrectMask
        else:
            IpV4Address.__init__(self, netmask)
            bits = bin(self.int)[2:]
            self._cidr = len(bits) - len(bits.lstrip('1'))
            self._int = (max_int - (2 ** (32 - self._cidr) - 1)) # verifying by cidr

    def __repr__(self):
        return str(self._cidr)


    @property
    def cidr(self):
        return self._cidr

if __name__ == '__main__':
    print "\nCreating some IpV4Address objects:"
    
    #Correct data
    ip = IpV4Address([192, 168, 220, 1]) 
    mask = IpV4Mask('255.255.230.0')

    # ip = IpV4Address([192, '168', 220, 78])
    # ip = IpV4Address((225, 168, 220, 96))
    # ip = IpV4Address('250.168.220')

    # Incorrect data
    # ip = IpV4Address(32322918455)
    # ip = IpV4Address(-628391)
    # ip = IpV4Address('192.168.-220.98')
    # ip = IpV4Address('500.168.-220.98')
    # ip = IpV4Address([192, '168', -220, 78])
    # ip = IpV4Address([192, '600', 220, 78])
    # ip = IpV4Address((-225, 168, 220, 96))
    # ip = IpV4Address((225, 368, 220, 96))

    print "\nGetting str:"
    print ip.str
    print mask.str

    print "\nGetting list:"
    print ip.list
    print mask.list

    print "\nGetting int:"
    print ip.int
    print mask.int

    "\nGetting mask cidr:"
    print mask.cidr


    print 'Broadcast:', IpV4Address(IpV4Address('192.168.220.0').int | ( ~IpV4Address('255.255.255.0').int & 0xffff))

    