CP = cp -r
RM = rm -r -f
MK = mkdir

RELEASEPATH = release
FOLDERS = modules templates
FILES = default_hsm.xml hsm_template.py

# Find 
CFILES=$(shell find ./ -name "*.cc") 
HFILES=$(shell find ./ -name "*.h") 

# Find all py files in given Folders to be copied
PYFILES := $(foreach DIR,$(FOLDERS),$(wildcard $(DIR)/*.py))

.PHONY: release copy

remove:
	# Remove all c files 
	$(RM) $(CFILES)
	# Remove all h files
	$(RM) $(HFILES)
	# Remove old release path
	$(RM) $(RELEASEPATH)

copy:
	# Make release path
	$(MK) $(RELEASEPATH)
	# create needed folders
	for i in $(FOLDERS); do $(MK) $(RELEASEPATH)/$$i; echo $(FILES);  done
	# copy py files from 
	for i in $(PYFILES); do $(CP) $$i $(RELEASEPATH)/$$i; done
	for i in $(FILES); do $(CP) $$i $(RELEASEPATH); done

release: remove copy

#Not used but maybe helpful in future
#CFILES := $(foreach DIR,$(DELFOLDERS),$(wildcard $(DIR)/*.cpp))
#HFILES := $(foreach DIR,$(DELFOLDERS),$(wildcard $(DIR)/*.h))
#for i in `find . -type d`; do hallo += "D=$$i"; done
#PYFILES_TEMP = $(wildcard templates/*.py)
#PYFILES_MOD  = $(wildcard modules/*.py)