# Makefile to release project
# v1.0

CP = cp -r
RM = rm -r -f
MK = mkdir

# Folder to release to
RELEASEFOLDER = release
# Folders to look for py files to be copied
PYFOLDERS = modules templates
# Folder to copy complete
COMPLETEFOLDERS = external
# Folders to be created before copying
CREATEFOLDERS = $(PYFOLDERS)
# Single files to be copied
SINGLEFILES = default_hsm.xml hsm_template.py 

# Find .cc and .h files
CFILES=$(shell find ./ -name "*.cc") 
HFILES=$(shell find ./ -name "*.h") 

# Find all py files in given py folders to be copied
PYFILES := $(foreach DIR, $(PYFOLDERS), $(wildcard $(DIR)/*.py))

.PHONY: release copy create remove tar

release: welcome remove create copy tar

welcome:    
	#                           
	#.______       _______  __       _______     ___           _______. _______ 
	#|   _  \     |   ____||  |     |   ____|   /   \         /       ||   ____|
	#|  |_)  |    |  |__   |  |     |  |__     /  ^  \       |   (----`|  |__   
	#|      /     |   __|  |  |     |   __|   /  /_\  \       \   \    |   __|  
	#|  |\  \----.|  |____ |  `----.|  |____ /  _____  \  .----)   |   |  |____ 
	#| _| `._____||_______||_______||_______/__/     \__\ |_______/    |_______|
	#
	#.___  ___.      ___       __  ___  _______  _______  __   __       _______ 
	#|   \/   |     /   \     |  |/  / |   ____||   ____||  | |  |     |   ____|
	#|  \  /  |    /  ^  \    |  '  /  |  |__   |  |__   |  | |  |     |  |__   
	#|  |\/|  |   /  /_\  \   |    <   |   __|  |   __|  |  | |  |     |   __|  
	#|  |  |  |  /  _____  \  |  .  \  |  |____ |  |     |  | |  `----.|  |____ 
	#|__|  |__| /__/     \__\ |__|\__\ |_______||__|     |__| |_______||_______|
	#
	#___    ____  __       ___   
	#\   \  /   / /_ |     / _ \  
	# \   \/   /   | |    | | | | 
	#  \      /    | |    | | | | 
	#   \    /     | |  __| |_| | 
	#    \__/      |_| (__)\___/  
	#
	#	
	
remove:
	# Remove all c files 
	$(RM) $(CFILES)
	# Remove all h files
	$(RM) $(HFILES)
	# Remove old release path
	$(RM) $(RELEASEFOLDER)

create:
	# Create release path
	$(MK) $(RELEASEFOLDER)
	
copy:
	# create folders
	for i in $(CREATEFOLDERS); do $(MK) $(RELEASEFOLDER)/$$i; done
	# copy py files 
	for i in $(PYFILES); do $(CP) $$i $(RELEASEFOLDER)/$$i; done
	# copy additonal single files
	for i in $(SINGLEFILES); do $(CP) $$i $(RELEASEFOLDER); done
	# Copy complete folders
	for i in $(COMPLETEFOLDERS); do $(CP) $$i $(RELEASEFOLDER); done

tar:
	# tar that shit
	tar -c --file=release.tar release
	$(CP) release.tar release
	$(RM) release.tar
