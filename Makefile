##################################################################################################################
# Author: ivo@marvan.cz
#
# - compile whycon.so package (use whycon_core from submodule)
# - compile and link python/package/whycon.so
##################################################################################################################

DEBUG_MAKEFILE := 0

ROOT_DIR 	:= $(shell realpath .)

.PHONY: make_dirs all clean python_package info info_local
all: make_dirs  python_package

# --- python_package --------------------------------------------------------------------------------------------------
PYTHON_HEADER_DIR	:= $(ROOT_DIR)/src
PYTHON_CPP_DIR 		:= $(ROOT_DIR)/src
PYTHON_BUILD_DIR 	:= $(ROOT_DIR)/build
RESULTS_BIN_DIR	:= $(ROOT_DIR)/bin

PYTHON_HEADER_FILES	:= $(wildcard $(PYTHON_HEADER_DIR)/*.h)
PYTHON_CPP_FILES	:= $(wildcard $(PYTHON_CPP_DIR)/*.cpp)
PYTHON_OBJ_FILES	:= $(patsubst $(PYTHON_CPP_DIR)/%.cpp, $(PYTHON_BUILD_DIR)/%.o, $(PYTHON_CPP_FILES))

# where is library *.so
SYS_INCLUDE_DIR := /usr/include
SYS_LIB_DIR 	:= /usr/lib/whycon
WHYCON_LIB 		:= $(SYS_LIB_DIR)/whycon_core.so

# where are *.o files
LIB_ROOT_DIR	:= $(ROOT_DIR)/whycon_core
LIB_CPP_DIR 	:= $(LIB_ROOT_DIR)/src
LIB_HEADER_DIR	:= $(LIB_ROOT_DIR)/src
LIB_BUILD_DIR 	:= $(LIB_ROOT_DIR)/build
LIB_CPP_FILES	:= $(wildcard $(LIB_CPP_DIR)/*.cpp)
LIB_HEADER_FILES:= $(wildcard $(LIB_HEADER_DIR)/*.h)
LIB_OBJ_FILES	:= $(patsubst $(LIB_CPP_DIR)/%.cpp, $(LIB_BUILD_DIR)/%.o, $(LIB_CPP_FILES))

# OpenCV flags for given instalation of python
OPENCV_FLAGS_ESCAPED  	:= $(shell python opencv_cflags_libs.py)
OPENCV_CXXFLAGS 		:= $(subst *, ,$(word 1,$(OPENCV_FLAGS_ESCAPED)))
OPENCV_LIBS 			:= $(subst *, ,$(word 2,$(OPENCV_FLAGS_ESCAPED)))
OPENCV_NAME 			:= $(subst *, ,$(word 3,$(OPENCV_FLAGS_ESCAPED)))
OPENCV_VERSION 			:= $(subst *, ,$(word 4,$(OPENCV_FLAGS_ESCAPED)))
export PKG_CONFIG_PATH	:= $(subst *, ,$(word 5,$(OPENCV_FLAGS_ESCAPED)))

# Pythons flags
PYTHON_CXXFLAGS 	:= $(shell python3-config --cflags)
PYTHON_LIBS 		:= $(shell python3-config --ldflags --libs)

# compile params
CXXFLAGS := -Wall -fPIC -O3 -shared -std=gnu++11
CXXFLAGS += -I$(SYS_INCLUDE_DIR) -I$(LIB_HEADER_DIR)	# for two posible places for headers
CXXFLAGS += $(OPENCV_CXXFLAGS) $(PYTHON_CXXFLAGS)

# linking params
LINK_FLAGS := -O3 -shared -std=gnu++11
LINK_FLAGS += $(OPENCV_LIBS) $(PYTHON_LIBS)

PYTHON_PACKAGE_NAME:=$(RESULTS_BIN_DIR)/whycon.so

info:	info_local
	$(MAKE) -C $(LIB_ROOT_DIR) OPENCV_CXXFLAGS="$(OPENCV_CXXFLAGS)" OPENCV_LIBS="$(OPENCV_LIBS)"  OPENCV_NAME="$(OPENCV_NAME)" info


info_local:
	$(info    )
	$(info    === Variables === $(ROOT_DIR) ===)
#	$(info    OPENCV_FLAGS_ESCAPED	$(OPENCV_FLAGS_ESCAPED))
	$(info    OPENCV_NAME 			$(OPENCV_NAME))
	$(info    OPENCV_VERSION 		$(OPENCV_VERSION))
	$(info    OPENCV_CXXFLAGS 		$(OPENCV_CXXFLAGS))
	$(info    OPENCV_LIBS 			$(OPENCV_LIBS))
	$(info    PKG_CONFIG_PATH		$(PKG_CONFIG_PATH))
	$(info    --------------------------------------------------)
	$(info    PYTHON_CXXFLAGS 		$(PYTHON_CXXFLAGS))
	$(info    PYTHON_LIBS 			$(PYTHON_LIBS))
	$(info    --------------------------------------------------)
	$(info    CXXFLAGS 				$(CXXFLAGS))
	$(info    LINK_FLAGS 			$(LINK_FLAGS))
	$(info    --------------------------------------------------)
	$(info    PYTHON_HEADER_DIR 	$(PYTHON_HEADER_DIR))
	$(info    PYTHON_CPP_DIR 		$(PYTHON_CPP_DIR))
	$(info    PYTHON_BUILD_DIR 		$(PYTHON_BUILD_DIR))
	$(info    PYTHON_HEADER_FILES 	$(PYTHON_HEADER_FILES))
	$(info    PYTHON_CPP_FILES 		$(PYTHON_CPP_FILES))
	$(info    PYTHON_OBJ_FILES 		$(PYTHON_OBJ_FILES))
	$(info    PYTHON_PACKAGE_NAME 	$(PYTHON_PACKAGE_NAME))
	$(info    --------------------------------------------------)
	$(info    SYS_INCLUDE_DIR 	    $(SYS_INCLUDE_DIR))
	$(info    SYS_LIB_DIR 		    $(SYS_LIB_DIR))
	$(info    LIB_ROOT_DIR 	        $(LIB_ROOT_DIR))
	$(info    LIB_CPP_DIR 	        $(LIB_CPP_DIR))
	$(info    LIB_BUILD_DIR 	    $(LIB_BUILD_DIR))
	$(info    LIB_OBJ_FILES 	    $(LIB_OBJ_FILES))
	$(info    ================== )



python_package: $(PYTHON_PACKAGE_NAME)

# compile C++ from python/package
$(PYTHON_BUILD_DIR)/%.o: $(PYTHON_CPP_DIR)/%.cpp $(PYTHON_HEADER_FILES) $(LIB_HEADER_FILES)
	$(CXX) -I$(PYTHON_HEADER_DIR) -I$(LIB_HEADER_DIR) $(CXXFLAGS) -o $@ -c $<

# compiling/linking library
$(LIB_OBJ_FILES): $(LIB_CPP_FILES) $(LIB_HEADER_DIR)
	$(MAKE) -C $(LIB_ROOT_DIR) OPENCV_CXXFLAGS="$(OPENCV_CXXFLAGS)" OPENCV_LIBS="$(OPENCV_LIBS)" OPENCV_NAME="$(OPENCV_NAME)"

# linking
$(PYTHON_PACKAGE_NAME): $(PYTHON_OBJ_FILES) $(LIB_OBJ_FILES)
	$(CXX) -o $(PYTHON_PACKAGE_NAME)  $(PYTHON_OBJ_FILES) $(LIB_OBJ_FILES) $(LINK_FLAGS)
	@echo "*******************************************************************"
	@echo "$(shell realpath $(PYTHON_PACKAGE_NAME)) was linked."
	@echo "*******************************************************************"

# --- all ----------------------------------------------------------------------------------------------------------
make_dirs:
	@mkdir -p $(LIB_BUILD_DIR) $(PYTHON_BUILD_DIR) $(MARK_GEN_BUILD_DIR) $(RESULTS_BIN_DIR)
	
clean:
	$(MAKE) -C $(LIB_ROOT_DIR) clean
	rm -rf $(RESULTS_BIN_DIR) $(PYTHON_BUILD_DIR)
	




	
