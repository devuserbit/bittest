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
from append_states_to_service import *
#~ from Cheetah.Template import Template

""" Import precompiled templates """
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
    
    __function__            = "ScaffoldService()"
    
    user_name               = ProjectDefines.HSM_DEFAULT_FILLER
    service_name            = None
    
    """ Protected service starts with '!' """
    service_is_protected    = False
    
    """ Template defines for the .h and .cc files """
    cc_template             = None
    h_template              = None
    errors_template         = None
    state_h_template        = None
    state_cc_template       = None
    
    if path is None:
        Print("\nScaffoldService: path is None",PrintLevels.CRITICAL) 
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
        Print("\nScaffoldService: target folder is None",PrintLevels.CRITICAL) 
        return ProjectFlags.STATUS_INVALID_PARAMETER
    
    """ Get the user name """
    try:
        user_name = getpass.getuser()
    except:
        Print("\nScaffoldService: Unable to get username from system!\n", PrintLevels.DEBUG)
    
    """ 
        Check for errors in the XML parsing
    """
    if HSMStruct.ErrorFlag is True:
        Print("An serious error occured during XML parsing.\nAborting!", PrintLevels.CRITICAL)
        return ProjectFlags.STATUS_XML_PARSING_ERROR
    
    
    """ """"""""""""""""""""""""""""""""""""""""""""""""
        
        CHECK FOR PROTECTION
        
        If '!' is in front of the service name that means
        the service is allready created and we will only
        add the states which are not proetected with 
        '!'.
        For that we are scanning the service .h and .cc
        for the markers '#^' and '^#'
        
    """ """"""""""""""""""""""""""""""""""""""""""""""""
    if HSMStruct.Name.startswith(ProjectDefines.PROTECTED_STARTS_WITH) is True:
        
        Print("\nService : " + HSMStruct.Name[1:] + " is protected!", PrintLevels.INFO)
        
        service_name = HSMStruct.Name[1:]
        service_is_protected = True
        
        AppendStatesToService(HSMStruct, target_folder)
    
    else:
        
        """ """"""""""""""""""""""""""""""""""""""""""""""""
        
        CREATE SERVICE FILES 
        
        The service is not protected
        Because we are using compiled templates we have to call them as
        classes
        
        http://packages.python.org/Cheetah/recipes/precompiled.html
        
        CHSM{Name}Service.cc
        CHSM{Name}Service.h
            
        """ """"""""""""""""""""""""""""""""""""""""""""""""
        
        service_name = HSMStruct.Name
        
        """ Create service .h """
        file_name = target_folder + '\\' + ProjectDefines.HSM_FILE_PREFIX +    \
                    service_name + ProjectDefines.HSM_FILE_SUFFIX +           \
                    ProjectDefines.FILE_H_EXTENSION
                
        Print("\nCreating : " + file_name, PrintLevels.INFO)
    
        tmpl = hsmService_h.hsmService_h(searchList=
                                        [{
                                        'srv'       : HSMStruct,
                                        'author'    : user_name,
                                        'extension' : ProjectDefines.FILE_H_EXTENSION,
                                        }])
    
        h_template = tmpl.respond()
    
        if WriteToFile(file_name,h_template) is False:
            Print("Unable to create " + file_name, PrintLevels.CRITICAL)
            return
    
        """ Create service .cc """
        file_name = target_folder + '\\' + ProjectDefines.HSM_FILE_PREFIX +    \
                    service_name + ProjectDefines.HSM_FILE_SUFFIX +           \
                    ProjectDefines.FILE_CC_EXTENSION
    
        Print("\nCreating : " + file_name, PrintLevels.INFO)
    
        tmpl = hsmService_cc.hsmService_cc(searchList=
                                            [{
                                            'srv'       : HSMStruct,
                                            'extension' : ProjectDefines.FILE_CC_EXTENSION,
                                            }])
        cc_template = tmpl.respond()
    
        if WriteToFile(file_name,cc_template) is False:
            Print("Unable to create " + file_name, PrintLevels.CRITICAL)
            return

        """ """"""""""""""""""""""""""""""""""""""""""""""""
        
            CREATE ERROR FILE 
        
            {Name}.Errors.h
        
        """ """"""""""""""""""""""""""""""""""""""""""""""""
    
        file_name = target_folder + '\\' + service_name + ProjectDefines.HSM_ERRORS_FILE
    
        Print("\nCreating : " + file_name, PrintLevels.INFO)
    
        tmpl = hsmErrors_h.hsmErrors_h(searchList=
                                        [{
                                        'srv'       : HSMStruct,
                                        'extension' : ProjectDefines.FILE_H_EXTENSION,
                                        }])
    
        errors_template = tmpl.respond()
    
        if WriteToFile(file_name,errors_template) is False:
            Print("Unable to create " + file_name, PrintLevels.CRITICAL)
            return
    
    
    """ """"""""""""""""""""""""""""""""""""""""""""""""
        
        CREATE STATES
        
        {Name}.C{State_Name}State.cc
        {Name}.C{State_Name}State.h
        
    """ """"""""""""""""""""""""""""""""""""""""""""""""
    for StateList in HSMStruct.StateLevelList:
        for State in StateList:
            
            if State.Name.startswith(ProjectDefines.PROTECTED_STARTS_WITH) is True:
                Print("\nState : " + State.Name[1:] + " is protected and will not be created!", PrintLevels.INFO)
                continue
            
            """ .h """
            file_name = target_folder + '\\' + service_name + '.' +        \
                        'C' + State.Name + ProjectDefines.HSM_STATE_SUFFIX + \
                        ProjectDefines.FILE_H_EXTENSION
            
            Print("\nCreating : " + file_name, PrintLevels.INFO)
            
            tmpl = hsmState_h.hsmState_h(searchList=
                            [{
                            'srv'       : HSMStruct,
                            'protected' : service_is_protected,
                            'state'     : State,
                            'extension' : ProjectDefines.FILE_H_EXTENSION,
                            'author'    : user_name
                            }])
            
            state_h_template = tmpl.respond()
            
            if WriteToFile(file_name,state_h_template) is False:
                Print("Unable to create " + file_name, PrintLevels.CRITICAL)
                return
            
            """ .cc """
            file_name = target_folder + '\\' + service_name + '.' +        \
                        'C' + State.Name + ProjectDefines.HSM_STATE_SUFFIX + \
                        ProjectDefines.FILE_CC_EXTENSION
            
            Print("\nCreating : " + file_name, PrintLevels.INFO)
    
            tmpl = hsmState_cc.hsmState_cc(searchList=
                            [{
                            'srv'       : HSMStruct,
                            'protected' : service_is_protected,
                            'state'     : State,
                            'extension' : ProjectDefines.FILE_CC_EXTENSION,
                            }])
            
            state_cc_template = tmpl.respond()
            
            if WriteToFile(file_name,state_cc_template) is False:
                Print("Unable to create " + file_name, PrintLevels.CRITICAL)
                return
                
    
    """ We are done so invalidate xml struct """
    XMLReference.SetXMLInvalid()
    
    return ProjectFlags.STATUS_OKAY
