import efibuild
import efitest
import pytest

def test_efi_fwts_kerneloops():
	'''High-level u-boot/efi smoke test.

	Does EFI boot using qemu/u-boot and check if working OK.
	'''

	efibuild.config()
	efibuild.build()

	qemu = efitest.qemu()
	console = qemu.console

	console.expect_busybox()

	console.sendline('fwts oops')
	console.expect('2 passed')
	console.expect_prompt()

	console.sendline('poweroff')

	qemu.close()
