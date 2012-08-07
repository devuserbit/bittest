# Makefile to release project
# v1.0

GET_CURRENT_SW_VERSION = $(shell python hsm_template.py -?)

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
SINGLEFILES = default_hsm.xml hsm_template.py README.txt
#Name of the release tar file
RELEASETARNAME = hsm_template_release_$(GET_CURRENT_SW_VERSION).tar

# #################################
# Git
# #################################
# Git - get branch name
GIT_GET_CURR_BRANCH = $(shell git symbolic-ref -q HEAD | cut -d"/" -f 3)

# Find .cc and .h files
STATESFOLDER = test/States
CFILES=$(shell find ./ -name "*.cc") 
HFILES=$(shell find ./ -name "*.h") 

# Find all py files in given py folders to be copied
PYFILES := $(foreach DIR, $(PYFOLDERS), $(wildcard $(DIR)/*.py))

.PHONY: help release copy create clean tar

help: welcome 
	@printf "\n\nFollowing commands are at your disposal:\n\n"
	@printf "       help      - Display this very usefull funky stylish super-script\n"
	@printf "       release   - Create folder release and save snapshot as .tar file (recommended)\n"
	@printf "       copy      - Copy snapshot files into release folder\n"
	@printf "       create    - Create release folder\n"
	@printf "       remove    - Remove *.cc and *h files, States and release folders\n"
	@printf "       tar       - Create and copy snapshot .tar into existing release folders\n"
	
	
release: welcome clean create copy tar

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
	
clean:
	# Remove all c files 
	$(RM) $(CFILES)
	# Remove all h files
	$(RM) $(HFILES)
	#Remove States folder
	$(RM) $(STATESFOLDER)
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
	tar -c --file=$(RELEASETARNAME) release
	$(RM) $(RELEASEFOLDER)/*
	$(CP) $(RELEASETARNAME) release
	$(RM) $(RELEASETARNAME)
