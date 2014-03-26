# -*- coding: utf-8 -*-

s = {"ssid": ("Pick the script according to the ssid, logical interface will be called as the ssid",
"""#!/bin/sh
ifconfig %(interface)s up 1> /dev/null && { iwlist %(interface)s scan | grep -o "\".*\"" | tr -d \'\" | sort | uniq; grep -o "map\ .*" /etc/network/interfaces | awk '{print $2}'; } | sort | uniq -d | head -1
""")
}
