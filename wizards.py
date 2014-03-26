# -*- coding: utf-8 -*-

import itertools as it
import re

def inputname(default, string, predicate=lambda x:True):
	out = raw_input("%s? [default: %s]: " % (string, default)) or default
	return out if predicate(out) else inputname(default, string, predicate)

def isip4(string):
	try:
		return len(filter(None, (i>=0 and i<=255 for i in map(int, string.split('.')))))==4
	except:
		return False

def addnetwork(interfaces, verbose, **kwargs):
	pass

def adddevice(interfaces, verbose, **kwargs):
	if verbose: print "Add device wizard started"
	script = kwargs["script"] if "script" in kwargs else inputname("none", "mapping script, none, list or path")
	if script=="none":
		if verbose: print "No script specified"
	if script=="list":
		if verbose: print "Listing preconfigured scripts"
	else:
		if verbose: print "Path script specified"

def addloopback(interfaces, verbose, **kwargs):
	if verbose: print "Add loopback wizard started"
	loopbacks = [i[0] for i in interfaces.inter if i[2]=="loopback"]
	if not loopbacks:
		if verbose: print "No loopback interfaces added yet, adding default"
		name = kwargs["name"] if "name" in kwargs else "lo"
		interfaces.inter.add(name, "inet", "loopback", [])
		if verbose: print "No loopback interface present, creating '%s'." % name
	else:
		if verbose: print "Loopback interface found, generating new one"
		newname = it.ifilter(lambda x: "lo:%d" % x not in [i[0] for i in interfaces.inter if i[2]=="static"], it.count(10, 10)).next()
		name = kwargs["name"] if "name" in kwargs else inputname("lo:%d" % newname, "Name")
		address = kwargs["address"] if "address" in kwargs else inputname("192.168.%d.1" % newname, "Address", isip4)
		netmask = kwargs["netmask"] if "netmask" in kwargs else inputname("255.255.255.0", "Netmask", isip4)
		network = kwargs["network"] if "network" in kwargs else inputname("192.168.%d.0" % newname, "Network", isip4)
		data = ["address %s" % address, "netmask %s" % netmask, "network %s" % network]
		interfaces.inter.append( ("lo:%d" % newname, "inet", "static", data) )
		if verbose: print "Loopback interface %s added with %s as data" % (name, str(data))
	
	auto = kwargs["auto"] if "auto" in kwargs else inputname("True", "Auto", lambda x: x in ["True", "False"])
	if auto == "True":
		interfaces.autos.append(name)
		if verbose: print "Set %s as auto" % name
