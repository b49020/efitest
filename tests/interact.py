#!/usr/bin/env python3

import argparse
import efibuild
import efitest
import sys

def main(argv):
	efibuild.config()
	efibuild.build()
	efitest.qemu(interactive=True)

if __name__ == '__main__':
	try:
		sys.exit(main(sys.argv))
	except KeyboardInterrupt:
		sys.exit(1)
	sys.exit(127)
