#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import wizards
from interfaces import interfaces

def mainparser(args):
	parser = argparse.ArgumentParser(description="Edit /etc/network/interfaces via CLI\n Help for every command can be accessed by -h after the command")
	parser.add_argument("command", 
			action="store", 
			help="Command", 
			choices=["list", "add", "rm"], 
			type=str)
	parser.add_argument("-v", "--verbose",
			action="store_true",
			help="More verbose messaging")
	parser.add_argument("--input", 
			action="store", 
			default="/etc/network/interfaces",
			metavar="PATH",
			help="Input filepath for interfaces file, backup is always created if file exists", 
			type=str)
	parser.add_argument("--output",
			action="store",
			default="/etc/network/interfaces",
			metavar="PATH",
			help="Output filepath for interfaces file, - for stdout",
			type=str)
	return parser.parse_args(args)

def secondaryparser(args, opttype):
	if opttype == "rm":
		parser = argparse.ArgumentParser(description="Help file for rm command", 
				usage="%(prog)s [OPTIONS] rm [-h] name")
		parser.add_argument("name",
				action="store",
				help="Removes the interface given")
	elif opttype == "list":
		parser = argparse.ArgumentParser(description="Help file for list command",
				usage="%(prog)s [OPTIONS] list [-h]")
	else:
		parser = argparse.ArgumentParser(description="Help file for add command",
				usage="%(prog)s [OPTIONS] add [-h] {loopback, cabled, wifi-device, wifi-network} [key=value]")
		parser.add_argument("type",
				action="store",
				help="Enter the type of interface/defice you want to add",
				choices=["loopback", "cabled", "wifi-device", "wifi-network"],
				)
		parser.add_argument("kwargs",
				action="store",
				help="Prefill questions in the format: key1=value1,key2=value2...keyn=valuen",
				nargs="?")
	return parser.parse_args(args)

if __name__ == "__main__":
	index = sys.argv.index("rm") if "rm" in sys.argv else sys.argv.index("list") if "list" in sys.argv else sys.argv.index("add") if "add" in sys.argv else len(sys.argv)
	ms = mainparser(sys.argv[1:(index+1)])
	os = secondaryparser(sys.argv[index+1:], ms.command)

	intfile = interfaces(ms.input)

	if ms.command == "list":
		if ms.verbose: print "List command applied"
		print intfile
	elif ms.command == "add":
		if ms.verbose: print "Add command applied"
		kw = dict() if not os.kwargs else dict(i.split('=') for i in os.kwargs.split(','))
		if ms.verbose: print "kwargs parsed: %s" % str(kw)
		if os.type == "loopback":
			wizards.addlo(intfile, ms.verbose, **kw)
	elif ms.command == "rm":
		if ms.verbose: print "Remove command applied"
		intfile.remove(os.name, ms.verbose)
	
	intfile.tofile(ms.output)
