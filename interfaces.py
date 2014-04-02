# -*- coding: utf-8 -*-

import os
import re
import sys


class interfaces:
    """
    autos = auto entries
    allow = allow- entries
    inter = iface entries
    mappi = mapping entries
    """

    def __init__(self, filepath='/etc/network/interfaces'):
        """Constructor for interfaces file class

        filepath -- path to read from, - for stdin
        """
        self.inter, self.mappi, self.auto, self.allow = [[]]*4
        self.inter = list()
        self.mappi = list()
        self.autos = list()
        self.allow = list()
        filein = (sys.stdin if filepath == '-' else open(filepath, 'r'))
        for line in filein:
            if line[0] == '#':
                continue
            line = line.lstrip()
            if line.startswith('auto'):
                self.autos += line.lstrip().split()[1:]
            elif line.startswith('source'):
                print 'source not implemented yet'
            elif line.startswith('allow-'):
                items = line.split()
                allowfor = items[0].split('-')[-1]
                self.allow += [(allowfor, item) for item in items[1:]]
            elif line.startswith('iface'):
                items = line.split()[1:]
                self.inter.append((items[0], items[1], items[2], list()))
                cmode = 'i'
            elif line.startswith('mapping'):
                self.mappi.append((line.split()[1], list()))
                cmode = 'm'
            elif line:
                current = self.mappi[-1] if cmode == 'm' else self.inter[-1]
                current[-1].append(line.strip())
        if filepath != '-':
            filein.close()

    def remove(self, name, regex=False, verbose=False):
        """Remove some interfaces

        name    -- name or pattern to match interface
        regex   -- set to true if name is a regex pattern or string
        verbose -- more verbose output
        """
        if regex:
            name = re.compile(name) if isinstance(name, basestring) else name
        regf = lambda x: name.search(x[1]) if regex else x[1] == name
        for a in reversed(filter(regf, enumerate(self.autos))):
            if verbose:
                print 'removed auto: %s' % a[1]
            del(self.autos[a[0]])
        for a in reversed(filter(regf, enumerate(i for i, in self.mappi))):
            if verbose:
                print 'removed mapping: %s' % a[1]
            del(self.mappi[a[0]])
        for a in reversed(filter(regf, enumerate(i[0] for i in self.inter))):
            if verbose:
                print 'removed interface: %s' % a[1]
            del(self.inter[a[0]])

    def tofile(self, filepath='/etc/network/interfaces', verbose=False):
        """Writes the interfaces file to file

        filepath -- filepath to write to, - for stdout
        verbos   -- more verbose output
        """
        if filepath == '-':
            fileout = sys.stdout
        else:
            if os.path.isfile(filepath):
                if verbose:
                    print 'file exists, backup created...'
                os.system('mv %s %s.bak' % (filepath, filepath))
            fileout = open(filepath, 'w')
        fileout.write('# Generated by pynterfaces\n')
        if self.autos:
            fileout.write('auto %s\n' % ' '.join(sorted(self.autos)))
        if self.allow:
            fileout.writelines('allow-%s %s\n' % i for i in sorted(self.allow))
        for m in sorted(self.mappi):
            fileout.write('\nmapping %s\n' % m[0])
            fileout.writelines('\t%s\n' % o for o in m[-1])
        for i in sorted(self.inter):
            fileout.write('\niface %s %s %s\n' % i[:3])
            fileout.writelines('\t%s\n' % o for o in i[-1])
        if filepath != '-':
            fileout.close()
