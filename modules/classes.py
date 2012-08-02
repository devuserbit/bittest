#! /python27/python.exe
# -*- coding: utf-8 -*-
#

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    Copyright (c) 2012 BIT Analytical Instruments GmbH. All rights reserved
    
    Designed for Python V2.7.2
    
    
    @@@ ABSTRACT
        This script defines all classes used in the project
    
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \class      PrintLevels

    \brief      Used by the Print function to distinguish the gravity
                of the message
            
    \author     APopescu
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class PrintLevels:
    
    CRITICAL            = 1
    WARNING             = 2
    INFO                = 3
    DEBUG               = 4

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \class      ProjectFlags

    \brief      Various flags that will be returned from different 
                functions
            
    \author     APopescu
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class ProjectFlags:
    
    """ Flags that describes the validity and the type of a path """
    PATH_IS_INVALID             = -1
    PATH_IS_FOLDER              = 1
    PATH_IS_FILE                = 2
    
    """ SYSSTATUS Flags """
    STATUS_OKAY                 = 0
    
    STATUS_INVALID_PARAMETER    = 190
    STATUS_XML_PARSING_ERROR    = 191
    STATUS_COMMON_ERROR         = 192
    
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \class      ProjectDefines

    \brief      Various defines used across the project
            
    \author     APopescu
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class ProjectDefines:
    
    """ Generic """
    PROTECTED_STARTS_WITH               = '!'
    MARKER_START                        = '#^'
    MARKER_END                          = '^#'
    SINGLE_LINE_COMMENT                 = '//'
    
    """ File extension defines """
    FILE_H_EXTENSION                    = ".h"
    FILE_CC_EXTENSION                   = ".cc"
    FILE_TEMPLATE_EXTENSION             = ".tmpl"
    
    """ Template file names """
    TPL_BASE_FOLDER_PATH                = "templates\\"
    
    """ HSM defines """
    HSM_FILE_PREFIX                     = "CHSM"
    HSM_FILE_SUFFIX                     = "Service"
    HSM_ERRORS_FILE                     = ".Errors" + FILE_H_EXTENSION
    HSM_STATE_SUFFIX                    = "State"
    HSM_DEFAULT_NAME                    = "HSMTemplateService"
    HSM_DEFAULT_FILLER                  = "TODO"
    

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \class      Path

    \brief      Class defining a path
            
    \author     APopescu
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class Path:
    m_Path             = None
    m_PathType         = ProjectFlags.PATH_IS_INVALID
    
    def __init__ (self):
        m_Path          = None
        m_PathType      = ProjectFlags.PATH_IS_INVALID
