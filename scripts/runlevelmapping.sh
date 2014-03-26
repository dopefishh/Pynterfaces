#!/bin/sh
# Script originated from http://addisu.taddese.com/blog/mapping-in-linux-network-interfaces/
set -e
RL=""
which=""
INITTAB="/etc/inittab"

if [ -r $INITTAB ]; then
	RL="$(sed -n -e "/^id:[0-9]*:initdefault:/{s/^id://;s/:.*//;p}" $INITTAB || true)"
fi
if [ ! -n "$RL" ]; then
	exit 1;
fi

while read runl scheme; do
	if [ "$which" ]; then continue; fi
	if [ "$runl" = "$RL" ]; then which="$scheme"; fi
done
if [ "$which" ]; then echo $which; exit 0; fi
exit 1
