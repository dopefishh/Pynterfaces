# -*- coding: utf-8 -*-

import itertools as it

def addlo(interfaces, verbose, **kwargs):
	if verbose: print "Add lo wizard started"
	loopbacks = [i[0] for i in interfaces.inter if i[2]=="loopback"]
	if not loopbacks:
		if verbose: print "No loopback interfaces added yet, adding default"
		name = kwargs["name"] if "name" in kwargs else "lo"
		interfaces.inter.add(name, "inet", "loopback", [])
		if verbose: print "No loopback interface present, creating '%s'." % name
	else:
		if verbose: print "Loopback interface found, generating new one"
		newname = it.ifilter(lambda x: "lo:%d" % x not in [i[0] for i in interfaces.inter if i[2]=="static"], it.count(10, 10)).next()
		name = kwargs["name"] if "name" in kwargs else raw_input("Name for loopback interface? [lo:%s] : " % newname) or "lo:%d" % newname
		address = kwargs["address"] if "address" in kwargs else raw_input("Address? [192.168.%d.1] : " % newname) or "192.168.%d.1" % newname
		netmask = kwargs["netmask"] if "netmask" in kwargs else raw_input("Netmask? [255.255.255.0] : ") or "255.255.255.0"
		network = kwargs["network"] if "network" in kwargs else raw_input("Network? [192.168.%d.0] : " % newname) or "192.168.%d.0" % newname
		data = ["address %s" % address, "netmask %s" % netmask, "network %s" % network]
		interfaces.inter.append( ("lo:%d" % newname, "inet", "static", data) )
		if verbose: print "Loopback interface %s added with %s as data" % (name, str(data))
	
	auto = kwargs["auto"] if "auto" in kwargs else raw_input("Set to auto? [True]") or "True"
	interfaces.autos.append(name)
	if verbose: print "Set %s as auto" % name
