##################################################################################################################
# Author: ivo@marvan.cz
##################################################################################################################

X := $(shell python3  'opencv_cflags_libs.py')
CCLAGS := $(word 1,$(x))
LIBS := $(word 2,$(x))

.PHONY: info all

all: info

info:
	$(info    === Variables ====)
	$(info    CCLAGS	$(CCLAGS))
	$(info    LIBS 		$(LIBS))
	$(info    X 		$(X))
	$(info    Y 		$(Y))