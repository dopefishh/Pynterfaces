#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import wizards
from interfaces import interfaces


def mainparser(args):
    parser = argparse.ArgumentParser(
        description='Edit /etc/network/interfaces via CLI\n\
            Help for every command can be accessed by -h after the command'
        )
    parser.add_argument(
        'command',
        action='store',
        help='Command',
        choices=['list', 'add', 'rm'],
        type=str
        )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='More verbose output'
        )
    parser.add_argument(
        '--input',
        action='store',
        default='/etc/network/interfaces',
        metavar='PATH',
        help='Use an alternate input file instead of /etc/network/interfaces,\
              - for stdin',
        type=str
        )
    parser.add_argument(
        '--output',
        action='store',
        default='/etc/network/interfaces',
        metavar='PATH',
        help='Use an alternate output file instead of /etc/network/interfaces,\
              - for stdout, when exists backup is created.',
        type=str
        )
    return parser.parse_args(args)


def secondaryparser(args, opttype):
    if opttype == 'rm':
        parser = argparse.ArgumentParser(
            description='Help file for rm command',
            usage='%(prog)s [OPTIONS] rm [-h] name'
            )
        parser.add_argument(
            '--regex', '-r',
            action='store_true',
            help='Use python regexes and remove all matching interfaces'
            )
        parser.add_argument(
            'name',
            action='store',
            help='Removes the interface given'
            )
    elif opttype == 'list':
        parser = argparse.ArgumentParser(
            description='Help file for list command',
            usage='%(prog)s [OPTIONS] list [-h]'
            )
    else:
        parser = argparse.ArgumentParser(
            description='Help file for add command',
            usage='%(prog)s [OPTIONS] add [-h] \
                {loopback, device, network} [key=value]'
            )
        parser.add_argument(
            '--scriptpath',
            action='store',
            metavar='PATH',
            help='Script location to store the mapping scripts, default: \
                  /etc/network/mapping\nPlease use a full path and no ~'
            )
        parser.add_argument(
            'type',
            action='store',
            help='Enter the type of interface/defice you want to add',
            choices=['loopback', 'device', 'network'],
            )
        parser.add_argument(
            'kwargs',
            action='store',
            help='Args: key1=value1,key2=value2...keyn=valuen',
            nargs='?')
    return parser.parse_args(args)

if __name__ == '__main__':
    index = sys.argv.index('rm') if 'rm' in sys.argv else\
        sys.argv.index('list') if 'list' in sys.argv else\
        sys.argv.index('add') if 'add' in sys.argv else len(sys.argv)
    ms = mainparser(sys.argv[1:(index+1)])
    os = secondaryparser(sys.argv[index+1:], ms.command)

    intfile = interfaces(ms.input)

    if ms.command == 'list':
        if ms.verbose:
            print 'List command applied'
        print intfile
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
