#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
from interfaces import interfaces

def mainparser(args):
	parser = argparse.ArgumentParser(description='Edit /etc/network/interfaces via CLI\n Help for every command can be accessed by -h after the command')
	parser.add_argument("command", 
			action="store", 
			help="Command", 
			choices=["list", "add", "rm"], 
			type=str)
	parser.add_argument("-s", "--simulate", 
			action="store_true", 
			help="Write to stdout instead of PATH")
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
			help="output filepath for interfaces file",
			type=str)
	return parser.parse_args(args)

def secondaryparser(args, opttype):
	if opttype == "rm":
		parser = argparse.ArgumentParser(description='Help file for rm command')
	elif opttype == "list":
		parser = argparse.ArgumentParser(description='Help file for list command')
	else:
		parser = argparse.ArgumentParser(description='Help file for add command')
	return parser.parse_args(args)

if __name__ == "__main__":
	index = sys.argv.index("rm") if "rm" in sys.argv else sys.argv.index("list") if "list" in sys.argv else sys.argv.index("add") if "add" in sys.argv else len(sys.argv)
	ms = mainparser(sys.argv[1:(index+1)])
	os = secondaryparser(sys.argv[index+1:], ms.command)
	
	if ms.command == "list":
		print "list"
		pass
	elif ms.command == "add":
		print "add"
		pass
	elif ms.command == "rm":
		print "rm"
		pass
#	intfile.tofile("./int")
