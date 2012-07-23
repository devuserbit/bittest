#! /python27/python.exe
# -*- coding: utf-8 -*-
#

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    Copyright (c) 2012 BIT Analytical Instruments GmbH. All rights reserved
    
    Designed for Python V2.7.2
    
    
    @@@ ABSTRACT
        Defining the function to add states to existing hsm service
        
    @@@ REVISION HISTORY
    
        Vers.   Date            Name            Comment
    
        1.0     17.07.2012      APopescu        Initial version
        1.1     19.07.2012      BMOLL       	Make it easy make it pretty and it will work like a charm
    
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import os,sys
import re
pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd)


""" """"""""""""""""""""""""""""""""""""""""""""""""
    Imports
""" """"""""""""""""""""""""""""""""""""""""""""""""
from hsm_template import VERBOSE
from hsm_template import Print
from hsm_template import WriteToFile
from XML2Class import HSMStruct
from XML2Class import ParseXML
from classes import *

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \fn         ReadFromFile()

    \brief      Read and return file internals
    
    \params     path - path to the existing file

    \return     sread - the internal of the read file or None
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def ReadLinesFromFile(path):
    
    sread = None
    
    if path is None:
        return sread
    
    try:
        def_fd = open(path, 'r')
    except IOError as e:
        print "Unable to open {} ({} : {})".format(path, e.errno, e.strerror)
        return sread
    else:
        sread = def_fd.readlines()
        def_fd.close()
    
    return sread



def HeaderEntries(states):
    string = ""
    for state in states:
        string += r'#include "Template.C' + state.Name + r'State.h"' + "\n"
    return string

def EnumEntries(states):
    string = ""
    for state in states:
        string += r'        ' + state.Name.upper() + "_STATE,\n"
    return string    
    
def DefineEntries(states):
    string = ""
    for state in states:
        string += r'    nsTemplateService::C' + state.Name + 'State\t\t\t\t' + state.Name + "State; \n"
    return string    
    
def FriendEntries(states):
    string = ""
    for state in states:
        string += r'    friend class    nsTemplateService::C' + state.Name + "State;\n"
    return string    

def InitEntries(states):
    string = ""
    for state in states:
        string += r'    nStatus = ' + state.Name + r'State.Init(&PrimaryHSM, &' + state.Parent.Name +'State,' + state.Name.upper() + "_STATE);\n    ASSERT_RETURN_BAD_STATUS(nStatus);\n\n"
    return string    

def CtorEntries(states):
    string = ""
    for state in states:
        string += "                     "+state.Name + "State(this),\n"
    return string    


""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \fn         AddNewStatesToFile()

    \brief      Look for markers in file and add new states
    
    \params     Path - path to file
    
    \params     States - new states

    \return     
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def AddNewStatesToFile(Path, States):
    
    File = ReadLinesFromFile(Path)
    
    if File is None:
        Print(__function__ + " : Couldn't read .cc or .h service files! Aborting!\n", PrintLevels.CRITICAL)
        return ProjectFlags.STATUS_INVALID_PARAMETER
    
    # Get modified file after new states were added
    NewFile = ParseForMarkers(File, States)
    
    # Overwrite old file with new
    WriteToFile(Path, NewFile)
    
    return ProjectFlags.STATUS_OKAY


""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \fn         ParseForMarkers()

    \brief      parse line array for certain markers
    
    \params     File - Array of file lines
    
    \params     States - new states

    \return     string that contains new file
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def ParseForMarkers(File, States):
    NewFile = ""
    NewStateString = ""
    MarkerActive = False
    
    # Scan each line for marker
    for line in File:
        # Do some regex action on: " // #^ MARKER_NAME "
        if (re.compile(r'( *)//( *)#\^( *)[A-Za-z]+').match(line) is not None):  
			# We have a hit - get our marker. legit characters are A-Z, a-z and underscores     
			MarkerString = re.search(r'[A-Za-z_]+',line,0)        
			if MarkerString is not None:
				# We found a valid marker
				MarkerName = MarkerString.group()
				MarkerActive = True
				NewStateString = CreateStringOnMarker(MarkerName, States)
        
        # Look for closing marker
        if (re.compile(r'( *)//( *)\^#').match(line) is not None):
			if MarkerActive is True:
				# Add to string file
				NewFile += NewStateString
				MarkerActive = False
            
        NewFile +=line
        
    return NewFile      
 
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \fn         WriteToFile()

    \brief      write string to file
    
    \params     Path - path to write file to
    
    \params     String - string whcih contains new file content

    \return     
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def WriteToFile(Path, String):
    file = open(Path, 'w')
    file.write(String)
    file.close()


""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \fn         CreateStringOnMarker()

    \brief      create string depending on marker
    
    \params     marker - marker to look for
    
    \params     new_states - new states to be added

    \return     created string to add to file
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def CreateStringOnMarker(Marker, new_states):  
    ResultString = {
      r'CTOR_STATES'    :     lambda: CtorEntries(new_states),
      r'INIT_STATES'    :     lambda: InitEntries(new_states),
      r'INITIAL_STATE'  :     lambda: "",
      r'HEADERS'        :     lambda: HeaderEntries(new_states),
      r'ENUMS'          :     lambda: EnumEntries(new_states),
      r'FRIENDS'        :     lambda: FriendEntries(new_states),
      r'DEFINES'        :     lambda: DefineEntries(new_states)
    }[Marker.upper()]()
    return ResultString


""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \fn         AppendStatesToService()

    \brief      Add new states to a existing HSM service
    
    \params     service - class defining the service as described in the xml
    
    \params     target_path - path to the existing HSM service

    \return     SYSSTATUS
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def AppendStatesToService(service, target_path):
    
    __function__    = "AppendStatesToService()"
    
    h_file_path     = None
    h_file_read     = None
    cc_file_path    = None
    cc_file_read    = None
    new_states      = []
    
    """ Sanity check parameters """
    if service is None:
        Print(__function__ + " : service is None! Aborting!\n", PrintLevels.CRITICAL)
        return ProjectFlags.STATUS_INVALID_PARAMETER
    
    if service.Name.startswith(ProjectDefines.PROTECTED_STARTS_WITH) is False:
        Print(__function__ + " : service is not protected! Aborting!\n", PrintLevels.CRITICAL)
        return ProjectFlags.STATUS_INVALID_PARAMETER
        
    if os.path.isdir(target_path) is False:
        Print(__function__ + " : Target path is invalid! Aborting!\n", PrintLevels.CRITICAL)
        Print(target_path, PrintLevels.CRITICAL)
        return ProjectFlags.STATUS_INVALID_PARAMETER
        
    h_file_path     = target_path + '\\' + ProjectDefines.HSM_FILE_PREFIX +     \
                        service.Name[1:] + ProjectDefines.HSM_FILE_SUFFIX +         \
                        ProjectDefines.FILE_H_EXTENSION
    
    cc_file_path    = target_path + '\\' + ProjectDefines.HSM_FILE_PREFIX +     \
                        service.Name[1:] + ProjectDefines.HSM_FILE_SUFFIX +         \
                        ProjectDefines.FILE_CC_EXTENSION
    
    """ Are files there? """
    if os.path.isfile(h_file_path) is False:
        Print(__function__ + " : .h file not found! Aborting!\n", PrintLevels.CRITICAL)
        return ProjectFlags.STATUS_INVALID_PARAMETER
        
    if os.path.isfile(cc_file_path) is False:
        Print(__function__ + " : .cc file not found! Aborting!\n", PrintLevels.CRITICAL)
        return ProjectFlags.STATUS_INVALID_PARAMETER
    
    Print("\nScanning for new states...", PrintLevels.INFO)
    
    for StateList in service.StateLevelList:
        for State in StateList:
            if State.Name.startswith(ProjectDefines.PROTECTED_STARTS_WITH) is False:
                """ Add to new states list """
                new_states.append(State)

    if len(new_states) == 0:
        Print(__function__ + " : No new states found! Returning\n", PrintLevels.CRITICAL)
        return ProjectFlags.STATUS_OKAY
    
    status = AddNewStatesToFile(h_file_path, new_states)
    if (status != ProjectFlags.STATUS_OKAY):
        return status
        
    status = AddNewStatesToFile(cc_file_path, new_states)
    if (status != ProjectFlags.STATUS_OKAY):
        return status
    
    return ProjectFlags.STATUS_OKAY
    
    
    """ Write back to file """
    WriteToFile(cc_file_path,newfile)
    
    

    
    
    
    

    
  
