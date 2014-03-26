# -*- coding: utf-8 -*-

import itertools as it
import re
import os
import scripts

def inputname(default, string, predicate=lambda x:True):
	out = raw_input("%s? [default: %s]: " % (string, default)) or default
	return out if predicate(out) else inputname(default, string, predicate)

def isip4(string):
	try:
		return len(filter(None, (i>=0 and i<=255 for i in map(int, string.split('.')))))==4
	except:
		return False

def isnum(string, lower=0, higher=999):
	try:
		return int(string)>=lower and int(string)<=higher
	except: 
		return False

def addnetwork(interfaces, verbose, **kwargs):
	pass

def adddevice(interfaces, prefix, verbose=False, **kwargs):
	if verbose: print "Add device wizard started"
	name = kwargs["name"] if "name" in kwargs else\
			inputname("", "Pick your network device from the detected unused devices: %s" % \
			str([i for i in os.listdir("/sys/class/net") if i not in [j[0] for j in interfaces.inter+interfaces.mappi]]),
			bool)
	if verbose: print "Name: %s picked" % name
	script = kwargs["script"] if "script" in kwargs else\
			inputname("none", "mapping script, none, list or path")
	if script=="none":
		if verbose: print "No script specified"
		pass
	else:
		if script=="list":
			if verbose: print "Listing preconfigured scripts\nmkdir -p %s" % prefix
			os.system("mkdir -p %s" % prefix)
			allscripts = list(enumerate(sorted(scripts.s.iteritems())))
			print "Pick one of the predefined scripts\n" 
			print "\n".join("%d: %s\t%s" % (it, i, j[0]) for it, (i, j) in allscripts)
			pick = -1
			while pick<0 or pick>=len(allscripts):
				pick = int(inputname("0", "Pick the script by number", isnum))
			script = allscripts[pick][1][0]
			with open("%s/%s" % (prefix, script), "w") as f:
				f.write(allscripts[pick][1][1][1])
			if verbose: print "Script written to %s\nchmod +x %s/%s" % (prefix, prefix, script)
		else:
			if verbose: print "Path script specified"
		interfaces.mappi.append( (name, ["script %s" % script]) )
	print 'scr: "%s"' % script

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
