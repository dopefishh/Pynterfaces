# -*- coding: utf-8 -*-

import itertools as it
import re
import os
import scripts
import subprocess


def inputname(default, string, predicate=lambda x: True):
    out = raw_input('%s? [default: %s]: ' % (string, default)) or default
    return out if predicate(out) else inputname(default, string, predicate)


def isip4(string):
    try:
        return len(filter(None, (i >= 0 and i <= 255 for i in
                   map(int, string.split('.'))))) == 4
    except:
        return False


def isnum(string, lower=0, higher=999):
    try:
        return int(string) >= lower and int(string) <= higher
    except:
        return False


def addnetwork(interfaces, verbose, mapnet=True, **kwargs):
    if verbose:
        print 'Add network wizard started'
    if mapnet:
        mappdevices = [i for i, _ in interfaces.mappi]
        device = kwargs['device'] if 'device' in kwargs else inputname(
            '', 'Pick the device to add it to, mappable devices: %s' %
            str(mappdevices), lambda x: x in mappdevices)
    logic = kwargs['logic'] if 'logic' in kwargs else inputname(
        '', 'Unique name for the logical interface', bool)
    if mapnet:
        output = kwargs['output'] if 'output' in kwargs else inputname(
            '', 'Value for the mapping script(SSID for ssidscript)', bool)
        if verbose:
            print 'map added to %s' % device
        interfaces.mappi[[
            i for i, _ in interfaces.mappi].index(device)][1].append(
            'map %s %s' % (logic, output))
    itype = kwargs['itype'] if 'itype' in kwargs else inputname(
        'inet', 'Pick the type [inet, inet6]',
        lambda x: x in ['inet', 'inet6'])
    if itype == 'inet':
        if verbose:
            print 'adding inet network'
        ipget = kwargs['ipget'] if 'ipget' in kwargs else inputname(
            'dhcp', 'Pick address acquisition method:\n%s' %
            sorted(options.keys()), lambda x: x in options.keys())
        ntype = kwargs['ntype'] if 'ntype' in kwargs else inputname(
            '', 'Pick network generation wizard [wifi, none]',
            lambda x: x in ['wifi', 'none'])
        interfaces.inter.append((logic, itype, ipget, list()))
        if ntype == 'wifi':
            print 'not yet implemented'
            spath = kwargs['spath'] if 'spath' in kwargs else inputname(
                '', 'WPA config path, generate for generation wizard', bool)
            if spath == 'generate':
                spath = generateconfig()
            interfaces.inter[-1][-1].append('wpa_conf %s' % spath)
        addoptions(interfaces, ipget)
    elif itype == 'inet6':
        print 'not yet implemented'
    addoptions(interfaces, 'iface')


def addoptions(interfaces, ipget):
    opts = options[ipget]
    getmanpageipget(ipget)
    while True:
        opt = inputname(
            'stop',
            'Enter an option from the list or stop or man\n%s'
            % sorted(opts.keys()),
            lambda x: x in opts.keys() + ['stop', 'man'])
        if opt == 'stop':
            break
        if opt == 'man':
            getmanpageipget(ipget)
            continue
        value = inputname(
            '',
            'Enter the value for %s' % opt,
            opts[opt])
        del[opts[opt]]
        interfaces.inter[-1][-1].append('%s %s' % (opt, value))


def generateconfig():
    print 'not yet implemented'
    exit()


def addauto(interfaces, name, verbose=False, **kwargs):
    auto = kwargs['auto'] if 'auto' in kwargs else\
        inputname('True', 'Auto', lambda x: x in ['True', 'False'])
    if auto == 'True':
        interfaces.autos.append(name)
        if verbose:
            print 'Set %s as auto' % name


def adddevice(interfaces, prefix, verbose=False, **kwargs):
    if verbose:
        print 'Add device wizard started'
    name = kwargs['name'] if 'name' in kwargs else inputname(
        '', 'Pick your network device from the detected unused devices: %s' %
        str([i for i in os.listdir('/sys/class/net') if i not in
            [j[0] for j in interfaces.inter + interfaces.mappi]]), bool)
    if verbose:
        print 'Name: %s picked' % name
    script = kwargs['script'] if 'script' in kwargs else\
        inputname('none', 'mapping script, none, list or path')
    if script == 'none':
        if verbose:
            print 'No script specified'
        kwargs['logic'] = name
        addnetwork(interfaces, verbose, False, **kwargs)
    else:
        if script == 'list':
            if verbose:
                print 'Listing preconfigured scripts\nmkdir -p %s' % prefix
            os.system('mkdir -p %s' % prefix)
            allscripts = list(enumerate(sorted(scripts.s.iteritems())))
            print 'Pick one of the predefined scripts\n'
            print '\n'.join('%d: %s\t%s' % (it, i, j[0])
                            for it, (i, j) in allscripts)
            pick = -1
            while pick < 0 or pick >= len(allscripts):
                pick = int(inputname('0', 'Pick the script by number', isnum))
            script = allscripts[pick][1][0]
            with open('%s/%s' % (prefix, script), 'w') as f:
                f.write(allscripts[pick][1][1][1] % {'interface': name})
            if verbose:
                print 'Script written to %s\nchmod +x %s/%s' %\
                    (prefix, prefix, script)
            os.system('chmod +x %s/%s' % (prefix, script))
        else:
            if verbose:
                print 'Path script specified'
        interfaces.mappi.append((name, ['script %s/%s' % (prefix, script)]))
        addauto(interfaces, name, verbose, **kwargs)


def addloopback(interfaces, verbose=False, **kwargs):
    if verbose:
        print 'Add loopback wizard started'
    loopbacks = [i[0] for i in interfaces.inter if i[2] == 'loopback']
    if not loopbacks:
        if verbose:
            print 'No loopback interfaces added yet, adding default'
        name = kwargs['name'] if 'name' in kwargs else 'lo'
        interfaces.inter.add(name, 'inet', 'loopback', [])
        if verbose:
            print 'No loopback interface present, creating \'%s\'.' % name
    else:
        if verbose:
            print 'Loopback interface found, generating new one'
        newname = it.ifilter(
            lambda x: 'lo:%d' % x not in
            [i[0] for i in interfaces.inter if i[2] == 'static'],
            it.count(10, 10)).next()
        name = kwargs['name'] if 'name' in kwargs else\
            inputname('lo:%d' % newname, 'Name')
        address = kwargs['address'] if 'address' in kwargs else\
            inputname('192.168.%d.1' % newname, 'Address', isip4)
        netmask = kwargs['netmask'] if 'netmask' in kwargs else\
            inputname('255.255.255.0', 'Netmask', isip4)
        network = kwargs['network'] if 'network' in kwargs else\
            inputname('192.168.%d.0' % newname, 'Network', isip4)
        data = ['address %s' % address, 'netmask %s' % netmask,
                'network %s' % network]
        interfaces.inter.append(('lo:%d' % newname, 'inet', 'static', data))
        if verbose:
            print 'Loopback interface %s added with %s as data' % (name,
                                                                   str(data))
    addauto(interfaces, name, verbose, **kwargs)


def getmanpageipget(method):
    found = False
    print ''
    if method == 'iface':
        for line in subprocess.check_output(['man', 'interfaces']).split('\n'):
            if found and re.search('IFACE OPTIONS', line):
                break
            if found and line or (not found and
                    line.strip().startswith(
                        'There exists for each of the above')):
                print line
                found = True
    else:
        for line in subprocess.check_output(['man', 'interfaces']).split('\n'):
            if found and re.search('(The .* Method|.*FAMILY)', line):
                break
            if found and line or\
                    (not found and
                     line.strip().startswith('The %s Method' % method)):
                print line
                found = True
    print ''

options = {
    'iface': {
        'pre-up': bool,
        'up': bool,
        'post-up': bool,
        'down': bool,
        'pre-down': bool,
        'post-down': bool
    }, 'static': {
        'address': isip4,
        'netmask': isip4,
        'broadcast': isip4,
        'metric': isnum,
        'gateway': isip4,
        'pointopoint address': bool,
        'hwaddress': bool,
        'mti': isnum,
        'scope': lambda x: x in ['global', 'link', 'host']
        }, 'manual': {
    }, 'dhcp': {
        'hostname': lambda x: x in ['pump', 'dhcpd', 'uphcpc'],
        'metric': bool,
        'leasehours': isnum,
        'leasetime': isnum,
        'vendor': bool,
        'client': bool,
        'hwaddress': bool
    }, 'bootp': {
        'bootfile': bool,
        'server': isip4,
        'hwaddr': bool
    }, 'tunnel': {

    }, 'ppp': {

    }, 'wvdial': {

    }, 'ipv4ll': {
    }}
