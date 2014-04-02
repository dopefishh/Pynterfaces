# -*- coding: utf-8 -*-

s = {
    "ssid": ("Pick the script according to the ssid, logical interface will be called as the ssid, configfiles should be named ssid.conf",
             """#!/bin/bash
{ awk 'BEGIN{f=0}/%(interface)s/{f=1}/^$/{f=0}{if(f&&$1=="map")print $2}' /etc/network/interfaces | sort | uniq; iwlist wlan0 scan | grep -Po "(?<=ESSID:\\").*(?=\\")"; } | sort | uniq -d | head -1""")
    }
