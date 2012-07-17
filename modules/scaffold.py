#! /python27/python.exe
# -*- coding: utf-8 -*-
#

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    Copyright (c) 2012 BIT Analytical Instruments GmbH. All rights reserved
    
    Designed for Python V2.7.2
    
    
    @@@ ABSTRACT
        This script defines the functions used to scaffold the hsm
        
    @@@ REVISION HISTORY
    
        Vers.   Date            Name            Comment
    
        1.0     09.07.2012      APopescu        Initial version
    
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""" Is this really the secret to eternal live """
import os,sys
pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd)

""" """"""""""""""""""""""""""""""""""""""""""""""""
    Imports
""" """"""""""""""""""""""""""""""""""""""""""""""""
import getpass
from hsm_template import VERBOSE
from hsm_template import Print
from hsm_template import WriteToFile
from XML2Class import HSMStruct
from XML2Class import ParseXML
from classes import *
#~ from Cheetah.Template import Template

""" Import templates """
from templates import hsmService_h
from templates import hsmService_cc
from templates import hsmErrors_h
from templates import hsmState_h
from templates import hsmState_cc

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \fn         ScaffoldService()

    \brief      Scaffolds the HSM service
            
    \params     service - class defining the service as described in the xml

    \return     SYSSTATUS
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def ScaffoldService(path):
    
    ServiceName         = ProjectDefines.HSM_DEFAULT_NAME
    UserName            = ProjectDefines.HSM_DEFAULT_FILLER
    
    """ Template defines for the .h and .cc files """
    cc_template         = None
    h_template          = None
    errors_template     = None
    state_h_template    = None
    state_cc_template   = None
    
    if path is None:
        Print("ScaffoldService: path is None",PrintLevels.CRITICAL) 
        return ProjectFlags.STATUS_INVALID_PARAMETER
    
    """ 
        The path was checked in hsm_template.py and it is a valid xml file.
        Now pass the path to the xml parser and get the hsm structure
    """
    XMLReference    = ParseXML(path)
    HSMStruct       = XMLReference.GetHSMStruct()

    """ Get target folder """
    target_folder = os.path.split(path)[0]
    
    if target_folder is None:
        Print("ScaffoldService: target folder is None",PrintLevels.CRITICAL) 
        return ProjectFlags.STATUS_INVALID_PARAMETER
    
    """ Get the user name """
    try:
        UserName = getpass.getuser()
    except:
        Print("\nUnable to get username from system!\n", PrintLevels.DEBUG)
    
    """ """"""""""""""""""""""""""""""""""""""""""""""""
        
        CREATE SERVICE FILES 
        
        Because we are using compiled templates we have to call them as
        classes
        
        http://packages.python.org/Cheetah/recipes/precompiled.html
        
        CHSM{Name}Service.cc
        CHSM{Name}Service.h
        
    """ """"""""""""""""""""""""""""""""""""""""""""""""
    
    """ .h """
    file_name = target_folder + '\\' + ProjectDefines.HSM_FILE_PREFIX +    \
                HSMStruct.Name + ProjectDefines.HSM_FILE_SUFFIX +           \
                ProjectDefines.FILE_H_EXTENSION
                
    Print("\nCreating : " + file_name, PrintLevels.INFO)
    
    tmpl = hsmService_h.hsmService_h(searchList=
                            [{
                            'srv'       : HSMStruct,
                            'author'    : UserName,
                            'extension' : ProjectDefines.FILE_H_EXTENSION,
                            }])
    
    h_template = tmpl.respond()
    
    WriteToFile(file_name,h_template)
    
    """ .cc """
    file_name = target_folder + '\\' + ProjectDefines.HSM_FILE_PREFIX +    \
                HSMStruct.Name + ProjectDefines.HSM_FILE_SUFFIX +           \
                ProjectDefines.FILE_CC_EXTENSION
    
    Print("\nCreating : " + file_name, PrintLevels.INFO)
    
    tmpl = hsmService_cc.hsmService_cc(searchList=
                            [{
                            'srv'       : HSMStruct,
                            'extension' : ProjectDefines.FILE_CC_EXTENSION,
                            }])
    cc_template = tmpl.respond()
    
    WriteToFile(file_name,cc_template)
    

    """ """"""""""""""""""""""""""""""""""""""""""""""""
        
        CREATE ERROR FILE 
        
        {Name}.Errors.h
        
    """ """"""""""""""""""""""""""""""""""""""""""""""""
    
    file_name = target_folder + '\\' + HSMStruct.Name + ProjectDefines.HSM_ERRORS_FILE
    
    Print("\nCreating : " + file_name, PrintLevels.INFO)
    
    tmpl = hsmErrors_h.hsmErrors_h(searchList=
                            [{
                            'srv'       : HSMStruct,
                            'extension' : ProjectDefines.FILE_H_EXTENSION,
                            }])
    
    errors_template = tmpl.respond()
    
    WriteToFile(file_name,errors_template)
    
    
    """ """"""""""""""""""""""""""""""""""""""""""""""""
        
        CREATE STATES
        
        {Name}.C{State_Name}State.cc
        {Name}.C{State_Name}State.h
        
    """ """"""""""""""""""""""""""""""""""""""""""""""""
    for StateList in HSMStruct.StateLevelList:
        for State in StateList:
            
            if State.Name.startswith(ProjectDefines.IGNORE_STARTS_WITH) is True:
                continue
            
            """ .h """
            file_name = target_folder + '\\' + HSMStruct.Name + '.' +        \
                        'C' + State.Name + ProjectDefines.HSM_STATE_SUFFIX + \
                        ProjectDefines.FILE_H_EXTENSION
            
            Print("\nCreating : " + file_name, PrintLevels.INFO)
            
            tmpl = hsmState_h.hsmState_h(searchList=
                            [{
                            'srv'       : HSMStruct,
                            'state'     : State,
                            'extension' : ProjectDefines.FILE_H_EXTENSION,
                            'author'    : UserName
                            }])
            
            state_h_template = tmpl.respond()
            
            WriteToFile(file_name,state_h_template)
            
            """ .cc """
            file_name = target_folder + '\\' + HSMStruct.Name + '.' +        \
                        'C' + State.Name + ProjectDefines.HSM_STATE_SUFFIX + \
                        ProjectDefines.FILE_CC_EXTENSION
            
            Print("\nCreating : " + file_name, PrintLevels.INFO)
    
            tmpl = hsmState_cc.hsmState_cc(searchList=
                            [{
                            'srv'       : HSMStruct,
                            'state'     : State,
                            'extension' : ProjectDefines.FILE_CC_EXTENSION,
                            }])
            
            state_cc_template = tmpl.respond()
            
            WriteToFile(file_name,state_cc_template)
    
    return ProjectFlags.STATUS_OKAY
