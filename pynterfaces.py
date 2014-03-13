#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from interfaces import interfaces


if __name__ == "__main__":
	intfile = interfaces()
	intfile.tofile("./int")
