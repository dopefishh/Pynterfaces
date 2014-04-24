#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import wizards
from interfaces import interfaces


def mainparser(args):
    parser = argparse.ArgumentParser(
        description="""\
pynterfaces version 0.08\n
edit interfaces file via command line interface in an interactive or\
non-interactive way\
""",
        formatter_class=argparse.RawTextHelpFormatter
        )
    parser.add_argument(
        'command',
        action='store',
        help="""\
main command to execute
list - dummy command to list the interfaces file
rm   - to remove interfaces, mappings and devices by name or regex
add  - to add device or network to the current configuration""",
        choices=['list', 'add', 'rm'],
        type=str
        )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='enable the more verbose output'
        )
    parser.add_argument(
        '--input',
        action='store',
        default='/etc/network/interfaces',
        metavar='PATH',
        help="""\
specify the input file to read from, - for stdin
default: /etc/network/interfaces""",
        type=str
        )
    parser.add_argument(
        '--output',
        action='store',
        default='/etc/network/interfaces',
        metavar='PATH',
        help="""\
specify the output file to write to, - for stdout.
a backup file is created with the .bak suffix if the specified file already \
exists\ndefault: /etc/network/interfaces""",
        type=str
        )
    return parser.parse_args(args)


def secondaryparser(args, opttype):
    if opttype == 'rm':
        parser = argparse.ArgumentParser(
            description="""\
remove an interface, mapping or devices by name or regex""",
            usage='%(prog)s [OPTIONS] rm [-h] name',
            formatter_class=argparse.RawTextHelpFormatter
            )
        parser.add_argument(
            '--regex', '-r',
            action='store_true',
            help="""\
remove all matching interfaces, mappings or devices using a regex match \
instead of a literal match.
default: literal match"""
            )
        parser.add_argument(
            'name',
            action='store',
            help="""\
Remove the interface(s), mapping(s) or device(s) matching the given\
name/pattern"""
            )
    elif opttype == 'list':
        parser = argparse.ArgumentParser(
            description="""\
list the interfaces file to standard out without doing anything""",
            usage='%(prog)s [OPTIONS] list [-h]',
            formatter_class=argparse.RawTextHelpFormatter
            )
    else:
        parser = argparse.ArgumentParser(
            description="""\
add a device or network""",
            usage="""\
%(prog)s [OPTIONS] add [-h] {loopback, device, network} [key=value]""",
            formatter_class=argparse.RawTextHelpFormatter
            )
        parser.add_argument(
            '--scriptpath',
            action='store',
            metavar='PATH',
            help="""\
path to store the script files created by the program, shell expansions not\
allowed
default: /etc/network/mapping/""",
            )
        parser.add_argument(
            'type',
            action='store',
            help="""\
specify the type of addition you want to make
loopback - loopback interface for a local host
device   - device that can either be a mapping device or a fixed device
network  - network that is picked by an already specified mapping script""",
            choices=['loopback', 'device', 'network'],
            )
        parser.add_argument(
            'kwargs',
            action='store',
            help="""\
key value pairs to make the process non interactive
they have to be of the format: key1=value1,key2=value2...keyn=valuen
general options:
    auto    - {True, False} mark the addition as auto
loopback:
    name    - name for the interface, default: 'lo' or 'lo:n'
    address - address for the interface, default: '192.168.n.1'
    netmask - netmask for the interface, default: '255.255.255.0'
    network - network for the interface, default: '192.168.n.0'
        where n is the next available number form {1, 1, ...}
device:
    name    - hardware name of the device to add to the configuration
    script  - {none, list, PATH} mapping script, default: none
              none - no mapping script used, the device is treated as a network
                     and the args for the network apply
              list - list the predefined scripts
              PATH - the exact path of the script
network:
    todo...""",
            nargs='?')
    return parser.parse_args(args)

if __name__ == '__main__':
    index = sys.argv.index('rm') if 'rm' in sys.argv else\
        sys.argv.index('list') if 'list' in sys.argv else\
        sys.argv.index('add') if 'add' in sys.argv else len(sys.argv)
    ms = mainparser(sys.argv[1:(index + 1)])
    os = secondaryparser(sys.argv[index + 1:], ms.command)

    intfile = interfaces(ms.input)

    if ms.command == 'list':
        if ms.verbose:
            print 'List command applied'
        ms.output = "-"
    elif ms.command == 'add':
        if ms.verbose:
            print 'Add command applied'
        kw = dict() if not os.kwargs else\
            dict(i.split('=') for i in os.kwargs.split(','))
        if ms.verbose:
            print 'kwargs parsed: %s' % str(kw)
        if os.type == 'loopback':
            wizards.addloopback(intfile, ms.verbose, **kw)
        if os.type == 'device':
            wizards.adddevice(intfile, os.scriptpath if os.scriptpath else
                              '/etc/network/mapping', ms.verbose, **kw)
        if os.type == 'network':
            wizards.addnetwork(intfile, ms.verbose, **kw)
    elif ms.command == 'rm':
        if ms.verbose:
            print 'Remove command applied'
        intfile.remove(os.name, os.regex, ms.verbose)
    intfile.tofile(ms.output)
