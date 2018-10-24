export UBOOT_DIR = $(PWD)
export TEST_DIR = $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

test :
	pytest-3 $(PYTEST_VERBOSE) $(PYTEST_RESTRICT) $(PYTEST_EXTRAFLAGS)

interact :
ifeq ("$(origin K)", "command line")
	tests/interact.py $(K)
else
	tests/interact.py
endif

ifeq ("$(origin K)", "command line")
  PYTEST_RESTRICT = -k '$(K)'
else
  PYTEST_RESTRICT =
endif

ifeq ("$(origin V)", "command line")
  PYTEST_VERBOSE = $(V)
else
  PYTEST_VERBOSE = 0
endif

ifeq ($(PYTEST_VERBOSE),2)
  PYTEST_VERBOSE = -v -s
else ifeq ($(PYTEST_VERBOSE),1)
  PYTEST_VERBOSE = -v
else
  PYTEST_VERBOSE =
endif

BUILDROOT ?= $(error BUILDROOT is not set)
buildroot-config :
	$(MAKE) -C $(BUILDROOT) O=$(TEST_DIR)/buildroot aarch64_efi_defconfig

BUILDROOT_INTERMEDIATES = \
		$(TEST_DIR)/buildroot/build \
		$(TEST_DIR)/buildroot/staging \
		$(TEST_DIR)/buildroot/target

# Remove intermediates, rather than doing a full clean, so we can (mostly)
# keep running tests whilst the rebuild happens
buildroot :
	$(RM) -r $(BUILDROOT_INTERMEDIATES)
	make -C $(TEST_DIR)/buildroot

# This is enough to save disk space (and force a rebuild) but leaves
# the cross-compilers and root images alone.
buildroot-tidy :
	$(RM) -r $(BUILDROOT_INTERMEDIATES)

.PHONY : buildroot-config buildroot buildroot-tidy
