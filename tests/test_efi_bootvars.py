import efibuild
import efitest
import pytest
import time

@pytest.mark.xfail(reason = "Missing support in u-boot", run = False)
def test_bootvars():
	'''Test efi boot-time non-volatile variables.
	'''

	efibuild.config()
	efibuild.build()

	qemu = efitest.qemu()
	console = qemu.console

	console.expect_uboot()
	console.sendline('run scsi_init; load scsi 0:1 ${kernel_addr_r} '
			 'efi/boot/Shell.efi; bootefi ${kernel_addr_r} '
			 '${fdtcontroladdr}')
	console.expect('or any other key to continue.')
	console.sendline('\x1b\x1b')
	console.expect('Shell> ')
	console.sendline('setvar BootNext -bs -nv =0000\r')
	console.expect('Shell> ')
	console.sendline('reset\r')

	console.expect_uboot()
	console.sendline('run scsi_init; load scsi 0:1 ${kernel_addr_r} '
			 'efi/boot/Shell.efi; bootefi ${kernel_addr_r} '
			 '${fdtcontroladdr}')
	console.expect('or any other key to continue.')
	console.sendline('\x1b\x1b')
	console.expect('Shell> ')
	console.sendline('setvar BootNext\r')
	console.expect('BootNext - 0002 Bytes')

	qemu.close()
