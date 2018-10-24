import os
import traceback
import sys

def run(cmd, failmsg=None):
	'''Run a command (synchronously) raising an exception on
	failure.

	'''

	# Automatically manage bisect skipping
	if failmsg:
		try:
			run(cmd)
			return
		except:
			skip(failmsg)

	print('+ ' + cmd)
	(exit_code) = os.system(cmd)
	if exit_code != 0:
		raise Exception

def skip(msg):
	"""Report a catastrophic build error.

        A catastrophic build error occurs when we cannot build the software
        under test. This makes testing of any form impossible. We treat this
        specially (and completely out of keeping with pytest philosophy because
        it allows us to return a special error code that will cause git bisect
        to look for a kernel we can compile.
        """
	traceback.print_exc()
	print('### SKIP: %s ###' % (msg,))
	sys.exit(125)

def config():
	os.chdir(os.environ['UBOOT_DIR'])

	run('make qemu_arm64_defconfig',
		'Cannot configure u-boot (wrong directory)')

def build():
	run('make -j `nproc`',
		'Cannot compile u-boot')
