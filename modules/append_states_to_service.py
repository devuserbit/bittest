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
    
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


import os,sys
pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd)

""" """"""""""""""""""""""""""""""""""""""""""""""""
    Imports
""" """"""""""""""""""""""""""""""""""""""""""""""""
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
def ReadFromFile(path):
    
    sread = None
    
    if path is None:
        return sread
    
    try:
        def_fd = open(path, 'r')
    except IOError as e:
        print "Unable to open {} ({} : {})".format(path, e.errno, e.strerror)
        return sread
    else:
        sread = def_fd.read()
        def_fd.close()
    
    return sread


def InsertIntoString(to_string,from_string,start,stop):
    
    if to_string is None:
        return from_string
        
    if from_string is None:
        return to_string
    
    if stop <= start:
        return from_string
    
    start_string    = to_string[:start]
    stop_string     = to_string[stop:]
    
    size = len(start_string) + len(from_string)
    
    to_string = start_string + from_string + stop_string
    
    return to_string,size

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
        
    """ Read the .h and .cc file internals """
    h_file_read = ReadFromFile(h_file_path)
    cc_file_read = ReadFromFile(cc_file_path)
    
    if h_file_read is None or cc_file_read is None:
        Print(__function__ + " : Couldn't read .cc or .h service files! Aborting!\n", PrintLevels.CRITICAL)
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
        
    """ Add to .h file """
    while True:
        
        start_position = h_file_read.find[ProjectDefines.MARKER_START,start_position]
        if start_position == -1:
            break
            
        stop_position = h_file_read.find[ProjectDefines.MARKER_START,start_position]
        
        
        
        
        
    string_size         = len(cc_file_read) 
    current_position    = 0
    
    """ Add to .cc file """
    #while current_position < string_size:
        
        
    
    return ProjectFlags.STATUS_OKAY
