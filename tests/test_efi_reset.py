import efibuild
import efitest
import pytest

def test_reset():
	'''Test efi reset implemented in u-boot.
	'''

	efibuild.config()
	efibuild.build()

	qemu = efitest.qemu()
	console = qemu.console

	console.expect_busybox()
	console.sendline('reboot')
	console.expect_busybox()
	console.sendline('poweroff')

	qemu.close()
