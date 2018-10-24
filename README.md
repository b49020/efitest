efitest - u-boot efi boot tests
===============================

Collection of fully automated u-boot efi boot tests that uses qemu for
aarch64 as a reference platform.

efitest is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either [version 2 of the
License](LICENSE.md), or (at your option) any later version.

Many thanks to Daniel Thompson as most of the test framework is reused
from [kgdbtest](https://github.com/daniel-thompson/kgdbtest).

Prerequisites
-------------

efitest requires a few special command lines tools together with some
additional python libraries.

On Fedora systems these can be installed as follows:

~~~
sudo dnf install -y \
	python3 \
	python3-pexpect \
	python3-pytest \
	socat
~~~

Likewise on debian systems:

~~~
sudo apt install -y \
	python3 \
	python3-pexpect \
	python3-pytest \
	socat
~~~

Buildroot
---------

efitest relies on buildroot filesystems, used here as root filesystem.
efitest uses aarch64_efi_defconfig config file to regenerate the
filesystem from scratch. The Makefile also has a few convenience rules
to help construct the filesystem.

As grub support for aarch64 is currently being upstreamed, so use this
[Buildroot](https://github.com/b49020/buildroot) repo instead.

~~~
BUILDROOT=/path/to/buildroot/ make buildroot-config
make buildroot
~~~

Alternatively once buildroot-config has been run it is possible
to run all buildroot rules directly from the build directory:

~~~
make -C buildroot menuconfig
~~~

Finally the Makefile has a special rule, `buildroot-tidy`, that
saves diskspace by deleting files that are not needed to run
efitest.

Running tests
-------------

efitest currently relies upon external environment variables. These are
set up automatically by the `Makefile`.

Assuming `$EFITESTDIR` points to the directory where efitest is
installed, then from a pristine (or mrproper'ed) u-boot source
directory try:

~~~
make -C $EFITESTDIR ARCH=arm CROSS_COMPILE=aarch64-linux-gnu-
~~~

This will run the default `test` rule, which will scan efitest for all
available tests and run them.

The Makefile behaviour can be made more verbose using `V=1` or `V=2`. At
level 1 the names of each test case are displayed as the test is run.
At level 2 all stdio capture is disabled, meaning the pexpect output
will be displayed live as the test runs.

The set of tests can be restricted using `K=<condition>`. A condition is
either a sub-string to match in the test name or a python operator. For
example:

~~~
make -C $EFITESTDIR V=2 K='efi and smoke' ARCH=arm CROSS_COMPILE=aarch64-linux-gnu-
~~~

Interacting with the EFI booted system
--------------------------------------

efitest also provides a quick means to fire up a u-boot and interact
with a Buildroot system booted via EFI for aarch64. This is useful for
ad-hoc experiments and to gather information to add new tests to
efitest itself.

To launch a u-boot and interact with EFI booted system try:

~~~
make -C $EFITESTDIR interact ARCH=arm CROSS_COMPILE=aarch64-linux-gnu-
~~~
