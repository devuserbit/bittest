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
        1.1     19.07.2012      BMOLL           Make it easy make it pretty and it will work like a charm
        1.2     02.08.2012      BMOLL           code cleanup to make the project manager happy
    
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""" """"""""""""""""""""""""""""""""""""""""""""""""
    COMMON IMPORTS
""" """"""""""""""""""""""""""""""""""""""""""""""""
import os,sys
import re

""" """"""""""""""""""""""""""""""""""""""""""""""""
    PATH
""" """"""""""""""""""""""""""""""""""""""""""""""""
pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd)

""" """"""""""""""""""""""""""""""""""""""""""""""""
    PROJECT IMPORTS
""" """"""""""""""""""""""""""""""""""""""""""""""""
from hsm_template import VERBOSE
from hsm_template import Print
from hsm_template import WriteToFile
from XML2Class import HSMStruct
from XML2Class import ParseXML
from classes import *

""" """"""""""""""""""""""""""""""""""""""""""""""""
    DEFINES
""" """"""""""""""""""""""""""""""""""""""""""""""""
FRIEND_SPACES           = 32
ENUM_SPACES             = 34
DEFINE_SPACES           = 48
SERVICE_STRING          = 'Service'
REGEX_MARKER_START      = r'( *)//( *)#\^( *)[A-Za-z]+'
REGEX_MARKER_END        = r'( *)//( *)\^#'
REGEX_FIND_MARKER_NAME  = r'[A-Za-z_]+'

""" """"""""""""""""""""""""""""""""""""""""""""""""
    GLOBALS
""" """"""""""""""""""""""""""""""""""""""""""""""""
global_line_counter = 0


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
    
    #Sanity check parameters
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
    
    # Are files there?
    if os.path.isfile(h_file_path) is False:
        Print(__function__ + " : .h file not found! Aborting!\n", PrintLevels.CRITICAL)
        return ProjectFlags.STATUS_INVALID_PARAMETER
        
    if os.path.isfile(cc_file_path) is False:
        Print(__function__ + " : .cc file not found! Aborting!\n", PrintLevels.CRITICAL)
        return ProjectFlags.STATUS_INVALID_PARAMETER
    
    Print("\nScanning for new states...", PrintLevels.INFO)
    
    # Create new state list
    for StateList in service.StateLevelList:
        for State in StateList:
            if State.Name.startswith(ProjectDefines.PROTECTED_STARTS_WITH) is False:
                """ Add to new states list """
                new_states.append(State)

    # Do we have any new states?
    if len(new_states) == 0:
        Print(__function__ + " : No new states found! Returning\n", PrintLevels.CRITICAL)
        return ProjectFlags.STATUS_OKAY
    
    # 
    status, NewHFile = AddNewStatesToFile(h_file_path, new_states, service)
    if (status != ProjectFlags.STATUS_OKAY):
        return status
        
    status, NewCFile = AddNewStatesToFile(cc_file_path, new_states, service)
    if (status != ProjectFlags.STATUS_OKAY):
        return status

    # Overwrite old files with new
    status = WriteToFile(h_file_path, NewHFile) 
    if (status != ProjectFlags.STATUS_OKAY):
        return status
        
    status = WriteToFile(cc_file_path, NewCFile)  
    if (status != ProjectFlags.STATUS_OKAY):
        return status    
    
    return ProjectFlags.STATUS_OKAY   


""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \fn         AddNewStatesToFile()

    \brief      Look for markers in file and add new states
    
    \params     Path - path to file
    
    \params     States - new states

    \return     Status
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def AddNewStatesToFile(Path, States, service):
    
    status, StringArray = ReadLinesFromFile(Path)
    
    if (status != ProjectFlags.STATUS_OKAY):
        return status, None
        
    if service.Name.startswith(ProjectDefines.PROTECTED_STARTS_WITH):
        service.Name = service.Name.lstrip(ProjectDefines.PROTECTED_STARTS_WITH)
        
    if StringArray is None:
        Print(__function__ + " : Couldn't read .cc or .h service files! Aborting!\n", PrintLevels.CRITICAL)
        return ProjectFlags.STATUS_INVALID_PARAMETER, None
    
    # Get modified file after new states were added
    NewFileString = ParseForMarkers(StringArray, States, service)
    
    return status, NewFileString

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \fn         ReadFromFile()

    \brief      Open file from path and return an line array
    
    \params     path - path to the existing file

    \return     sread - lines organized in an array
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def ReadLinesFromFile(path):
    
    sread = None
    
    if path is None:
        return ProjectFlags.STATUS_COMMON_ERROR, None
    
    try:
        def_fd = open(path, 'r')
    except IOError as e:
        print "Unable to open {} ({} : {})".format(path, e.errno, e.strerror)
        return ProjectFlags.STATUS_COMMON_ERROR, None
    else:
        sread = def_fd.readlines()
        def_fd.close()
    
    return ProjectFlags.STATUS_OKAY, sread

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \fn         ParseForMarkers()

    \brief      parse each line in given file and serach for desired markers.
                When found insert new string for each new state.
    
    \params     File - Array of file lines
    
    \params     States - new states

    \return     string that contains new file
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def ParseForMarkers(File, States, service):
    # global line counter var
    global global_line_counter
    # String that will contain the new file content
    NewFileString = ""
    # Our new string to be insert to file
    NewStateString = ""
    # Open marker flag
    MarkerActive = False
    # Keep track of current line number
    LineCounter = 0
    # Line of our starting marker
    LineMarkerStart = 0
    # Name marker
    MarkerName = ""
    
    # Scan each line for desired Marker
    for line in File:
        LineCounter = LineCounter + 1

        # Look for Starting Marker
        if RegExStartsWith(REGEX_MARKER_START, line) is not None:
            # Look for Marker Name
            MarkerString = RegExSearch(REGEX_FIND_MARKER_NAME, line)        
            if MarkerString is not None:
                # We found a valid marker
                MarkerName = MarkerString.group()
                # Set a flag
                MarkerActive = True
                LineMarkerStart = LineCounter

        # Look for Closing Marker
        if RegExStartsWith(REGEX_MARKER_END, line) is not None:
            # Make sure FLag is set
            if MarkerActive is True:
                # Update line counter - might be needed within markers
                global_line_counter = (LineCounter - LineMarkerStart - 1)
                # Our new string which will be included in our file
                NewStateString      = CreateStringOnMarker(MarkerName, States, service)
                # Get leading spaces
                WhiteSpaces         = GetLeadingWhiteSpaces(LastLine)
                # Adjust depending on leading white spaces
                NewStateString      = NewStateString.rjust(WhiteSpaces + len(NewStateString)) 
                # Add new string to our file string
                NewFileString += NewStateString
                MarkerActive = False
            
        NewFileString +=line
        # Save last line
        LastLine = line
        
    return NewFileString  
    
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \fn         GetLeadingWhiteSpaces()

    \brief      get leading white spaces of given stirng
    
    \params     string line

    \return     number of white spaces
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def GetLeadingWhiteSpaces(String):
    whitespace_matcher = re.compile(r'^\s+')
    match = whitespace_matcher.search(String)
    if match is not None:
        WhiteSpacesString = match.group()
        if len(WhiteSpacesString) == 1:
            length = 4
        else:
            length = len(WhiteSpacesString)    
        return length
    else:
        return 0

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \fn         RegExSearch()

    \brief      search for string within string
    
    \params     string to find
    
    \params     line to search in

    \return     regex instance or none
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def RegExSearch(FindString, Line):
    return re.search(FindString, Line, 0) 

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \fn         RegExStartsWith()

    \brief      search for string at the beginning of string
    
    \params     string to find
    
    \params     line to search in

    \return     regex instance or none
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def RegExStartsWith(FindString, Line):
    return re.compile(FindString).match(Line) 
    
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \fn         CreateStringOnMarker()

    \brief      create string depending on marker
    
    \params     marker - marker to look for
    
    \params     new_states - new states to be added

    \return     created string to add to file
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def CreateStringOnMarker(Marker, new_states, service):  
    ResultString = {
      r'CTOR_STATES'    :     lambda: CtorEntries(new_states),
      r'INIT_STATES'    :     lambda: InitEntries(new_states),
      r'INITIAL_STATE'  :     lambda: "",
      r'HEADERS'        :     lambda: HeaderEntries(new_states, service),
      r'ENUMS'          :     lambda: EnumEntries(new_states),
      r'FRIENDS'        :     lambda: FriendEntries(new_states, service),
      r'DEFINES'        :     lambda: DefineEntries(new_states, service)
    }[Marker.upper()]()
    return ResultString


""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \fn         HeaderEntries()

    \brief      create string depending on new states
    
    \params     new states and current service

    \return     string that contains the new line
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def HeaderEntries(states, service):
    string = ""
    for state in states:
        string += r'#include "' + service.Name + '.C' + state.Name + r'State.h"' + "\n"
    return string

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \fn         EnumEntries()

    \brief      create string depending on new states
    
    \params     new states

    \return     string that contains the new line
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def EnumEntries(states):
    string = ""
    global global_line_counter
    for state in states:
        insert_string = state.Name.upper() + '_STATE,'
        intend = ' '.rjust(ENUM_SPACES - len(insert_string))
        string += insert_string + intend + r'// ' + str(global_line_counter) + ' - TODO: Decription\n'
    return string    

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \fn         DefineEntries()

    \brief      create string depending on new states
    
    \params     new states and current service

    \return     string that contains the new line
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def DefineEntries(states, service):
    string = ""
    for state in states:
        intend = ' '.rjust(DEFINE_SPACES - ((len(service.Name) + len(SERVICE_STRING) + 5) + (len(state.Name) + 5)))
        string += r'ns' + service.Name + 'Service::C' + state.Name + 'State' + intend + state.Name + "State; \n"
    return string    

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \fn         FriendEntries()

    \brief      create string depending on new states
    
    \params     new states and current service

    \return     string that contains the new line
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def FriendEntries(states, service):
    string = ""
    for state in states:
        string += r'friend class    ns' + service.Name + 'Service::C' + state.Name + "State;\n"
    return string    

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \fn         InitEntries()

    \brief      create string depending on new states
    
    \params     new states

    \return     string that contains the new line
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def InitEntries(states):
    string = ""

    for state in states:
        parent_state = state.Parent.Name
        if parent_state.startswith(ProjectDefines.PROTECTED_STARTS_WITH) is True:
            parent_state = parent_state[1:len(parent_state)]
        string += r'nStatus = ' + state.Name + r'State.Init(&PrimaryHSM, &' + parent_state +'State, ' + state.Name.upper() + "_STATE);\n    ASSERT_RETURN_BAD_STATUS(nStatus);\n\n"
    return string    

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \fn         CtorEntries()

    \brief      create string depending on new states
    
    \params     new states

    \return     string that contains the new line
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def CtorEntries(states):
    string = ""
    for state in states:
        string += state.Name + "State(this),\n"
    return string    


""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \fn         WriteToFile()

    \brief      write string to file
    
    \params     Path - path to write file to
    
    \params     String - string whcih contains new file content

    \return     
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def WriteToFile(Path, String):
    if Path is None:
        return ProjectFlags.STATUS_COMMON_ERROR
    
    try:
        file = open(Path, 'w')
    except IOError as e:
        print "Unable to open {} ({} : {})".format(path, e.errno, e.strerror)
        return ProjectFlags.STATUS_COMMON_ERROR
    else:
        file.write(String)
        file.close()
        return ProjectFlags.STATUS_OKAY
        
             
    
    
    

    
  
