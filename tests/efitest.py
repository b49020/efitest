import os
import pexpect
import sys
import time
from types import MethodType

def expect_boot(self, bootloader=()):
	for msg in bootloader:
		self.expect(msg)
	self.expect('Linux version.*$')
	self.expect('Calibrating delay loop')
	self.expect('NET: Registered protocol family 2')
	self.expect('io scheduler [^ ]* registered .default.')
        # We need a wildcard here because some newer kernels now
        # "Free unused kernel image memory".
	self.expect('Freeing unused kernel.*memory')

def expect_busybox(self):
	self.expect('Starting logging')
	self.expect('OK')
	self.expect('Welcome to Buildroot')
	self.expect('buildroot login:')
	self.sendline('root')

	self.expect_prompt()

def expect_prompt(self):
	self.expect('# ')

def expect_uboot(self):
	self.expect('Hit any key to stop autoboot:')
	self.sendline('')

	self.expect('=> ')

def bind_methods(c):
	# TODO: Can we use introspection to find methods to bind?
	c.expect_boot = MethodType(expect_boot, c)
	c.expect_busybox = MethodType(expect_busybox, c)
	c.expect_prompt = MethodType(expect_prompt, c)
	c.expect_uboot = MethodType(expect_uboot, c)

class ConsoleWrapper(object):
	def __init__(self, console):
		bind_methods(console)
		self.console = console
	
	def close(self):
		self.console.close()

def qemu(interactive=False):
	'''Create a qemu instance and provide pexpect channels to control it'''

	cmd = 'qemu-system-aarch64'
	cmd += ' -accel tcg,thread=multi '
	cmd += ' -M virt -cpu cortex-a57'
	cmd += ' -bios u-boot.bin'

	cmd += ' -m 1G'
	cmd += ' -smp 2'
	cmd += ' -nographic'
	cmd += ' -monitor none'
	cmd += ' -chardev stdio,id=mon,mux=on,signal=off -serial chardev:mon'
	cmd += ' -drive if=none,format=raw,file={}/buildroot/images/disk.img,id=mydisk'.format(os.environ['TEST_DIR'])
	cmd += ' -device ich9-ahci,id=ahci -device ide-drive,drive=mydisk,bus=ahci.0'

	if interactive:
		print('+| ' + cmd)
		os.system(cmd)
		return None

	print('+| ' + cmd)
	qemu = pexpect.spawn(cmd, encoding='utf-8', logfile=sys.stdout)

	return ConsoleWrapper(qemu)
