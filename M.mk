##################################################################################################################
#*Author:*ivo@marvan.cz
##################################################################################################################

OPENCV_FLAGS_ESCAPED  := $(shell python opencv_cflags_libs.py)
OPENCV_CCLAGS 	:= $(subst *, ,$(word 1,$(OPENCV_FLAGS_ESCAPED)))
OPENCV_LIBS 	:= $(subst *, ,$(word 2,$(OPENCV_FLAGS_ESCAPED)))


.PHONY: info all

all: info

info:
	$(info    === Variables ====)
	$(info    OPENCV_FLAGS_ESCAPED	$(OPENCV_FLAGS_ESCAPED))
	$(info    OPENCV_CCLAGS 		$(OPENCV_CCLAGS))
	$(info    OPENCV_LIBS 			$(OPENCV_LIBS))
