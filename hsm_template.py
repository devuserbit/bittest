#! /python27/python.exe
# -*- coding: utf-8 -*-
#

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    Copyright (c) 2012 BIT Analytical Instruments GmbH. All rights reserved
    
    Designed for Python V2.7.2
    
    
    @@@ ABSTRACT
        This script is used for scaffolding a HSM Service from scratch.
    
    
    @@@ REVISION HISTORY
    
        Vers.   Date            Name            Comment
    
        1.0     28.06.2012      APopescu        Initial version

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


""" """"""""""""""""""""""""""""""""""""""""""""""""
    File information
""" """"""""""""""""""""""""""""""""""""""""""""""""
__filename__    = "hsm_template.py"
__author__      = "APopescu / BMoll"
__copyright__   = "Copyright (C) 2012 BIT Analytical Instruments GmbH"

__version__     = "1.0"
__required_python_version__ = ('2','7')

""" """"""""""""""""""""""""""""""""""""""""""""""""
    Imports
""" """"""""""""""""""""""""""""""""""""""""""""""""
import os, glob, sys, getopt

""" Dedicated to Mathis """
try:
    from Cheetah.Template import Template
except ImportError:
    print("Unable to import Cheetah template module!\n"                     \
          "Before using this scaffolding service you have to install:\n"    \
          "\t 1. setuptools\n"                                              \
          "\t 2. Cheetah\n\n"                                               \
          "Both can be found in the 'external' folder!\n"                     \
          "Aborting before any damage could be made!")
    sys.exit(2)

from modules.search_path_for_files import *
from modules.classes import *
from modules.XML2Class import *
from modules.scaffold import *


"""
!!! 
    Each compiled template file needs to have the below code at the 
    very begining directly after "#!/usr/bin/env python" of course 
    in combination only with the above 'from' include 
!!!

import os,sys
pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd)
"""

""" """"""""""""""""""""""""""""""""""""""""""""""""
    Global defines
""" """"""""""""""""""""""""""""""""""""""""""""""""
# Config file extension
CONFIG_FILE_EXTENSION       = "xml"

# Path to the default xml which will be used when no xml will be found in the given path
DEFAULT_XML_FILE_PATH       = os.getcwd() + "\default_hsm." + CONFIG_FILE_EXTENSION


# If True enables additional information output
VERBOSE                     = False
PRINT_DISABLED              = False

# If only a default xml should be created then this will be set to True
CREATE_DEFAULT_XML_ONLY     = False

# Path to the folder with the xml file which describes the HSM (states, hierarchy, functions, etc.)
xml_file_path               = Path()
command_line_path           = Path()

# The XML class we will recieve from the parseing
# and the apropriate hsm structure
XMLReference                = None
HSMStruct                   = None


""" """"""""""""""""""""""""""""""""""""""""""""""""
    Keywords
""" """"""""""""""""""""""""""""""""""""""""""""""""
# At least one of this keywords needs to be in the xml file name
# or we will ignore it and return and error
xml_file_name_keywords = { 'hsm', 'HSM' , 'service', 'Service' }


""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \fn         Welcome()

    \brief      Print a welcome message including the version number
            
    \params     n/a

    \return     n/a
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def Welcome():
    
    print("\n")
    print("*******************************************************************")
    print("****************** HSM Service scaffolding V" + __version__ + " *******************")
    print("*******************************************************************")
    print("\n")

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \fn         Usage()

    \brief      Display the usage of this programm
            
    \params     n/a

    \return     n/a
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def Usage():
    
    print("\n")
    print("Usage:")
    print("\n")
    print("\t" + __filename__ + " [-n,-v] path")
    print("")
    print("\t\t" + "path" + "          " + "Path to the folder in which the HSM Servie should be created")
    print("\t\t" + "-n  " + "          " + "Create default hsm description xml in the given folder path")
    print("\t\t" + "-v  " + "          " + "Verbose")
    print("\t\t" + "-?  " + "          " + "Print version and exit")
    print("\t\t" + "" + ""  + "")

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \fn         Print()

    \brief      Print the string if verbose mode is on
            
    \params     string - string to be printed

    \return     n/a
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def Print(string,level):
    
    global VERBOSE
    
    if string is not None:
        if level != PrintLevels.DEBUG or VERBOSE is True:
            print(string)

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \fn         UsersFileChoice()

    \brief      Scans folder for files ending "xml". Check the found files
                for keywords and present user a choice.
            
    \params     path - path of the folder to be scanned

    \return     the chosen xml file path
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def UsersFileChoice(path):
    
    if path is None:
        return None
    
    xml_files_with_keywords  = []
    
    xml_files_in_dir = SearchPathForFiles(path,CONFIG_FILE_EXTENSION)
    
    """ Nothing found -> return error """
    if xml_files_in_dir is None:
        Print("No xml file found in the given folder! Aborting!\n", PrintLevels.CRITICAL)
        return None
    
    """ 
        Scan the found files for keywords
        If only one was found add file to list
    """
    for xml_file in xml_files_in_dir:
        file_name = os.path.split(xml_file)
        for keyword in xml_file_name_keywords:
            if file_name[1].find(keyword) != -1:
                xml_files_with_keywords.append(xml_file)
                break
    
    """ Present user the choice """
    for num,files in enumerate(xml_files_with_keywords):
        print("[" + str(num) + "]  " + files + "\n")
                    
    users_choice = input("Please choose a number: ")
    
    """ We got a valid choice """
    if (int(users_choice) <= len(xml_files_with_keywords)) and (int(users_choice) >= 0):
        return_path = path + "\\" +  xml_files_with_keywords[int(users_choice)]
        Print("\nParsing: ", PrintLevels.DEBUG)
        Print(return_path, PrintLevels.DEBUG)
        return return_path
        
    """ User chose a sys.exit(2). Oblidge """
    Print("\nYou have selected a inexistent file! Aborting!", PrintLevels.CRITICAL)
    return None

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \fn         CheckForKeywords()

    \brief      Scan string for given keywords
            
    \params     keywords - keywords list to be searched for
                string - string to search keywords in

    \return     False - if error or nothing found
                True - if keyword found
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def CheckForKeywords(keywords, string):
    
    if keywords is None or string is None:
        return False
        
    for keyword in keywords:
        if string.find(keyword) != -1:
            return True
    
    return False

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \fn         WriteToFile()

    \brief      Writes the given string to the given file
            
    \params     path - path to the file
                string - string to be writen

    \return     n/a
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def WriteToFile(path, string):
    
    if path is None or string is None:
        return False
        
    try:
        def_fd = open(path, 'w')
    except IOError as e:
        print "Unable to open {} ({} : {})".format(path, e.errno, e.strerror)
        return False
    else:
        def_fd.write(string)
        def_fd.close()
        
    return True

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \fn         CreateXMLFromDefault()

    \brief      Creates the given file from the default xml
            
    \params     path - path to file to be created

    \return     False - if error 
                True - if file created succesfully
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def CreateXMLFromDefault(file_path):
    
    global DEFAULT_XML_FILE_PATH
    
    if file_path is None:
        return False
        
    """ Open default xml file and read internals """
    try:
        def_fd = open(DEFAULT_XML_FILE_PATH, 'r')
    except IOError as e:
        print "Unable to open default xml ({0} : {1})".format(e.errno, e.strerror)
        return False
    else:
        def_fc = def_fd.read()
        def_fd.close()
    
    
    """ Check if folder is there and if not create it """
    base_folder = os.path.split(file_path)
    
    if os.path.isdir(base_folder[0]) is False:
        try:
            os.mkdir(base_folder[0])
        except OSError as e:
            print "Unable to create directory ({0} :  {1})".format(e.errno,e.strerror)
            

    """ now create the new file """
    try:
        new_fd = open(file_path,'w')
    except IOError as e:
        print "Unable to create new xml file ({0} : {1})".format(e.errno, e.strerror)
        return False
    else:
        new_fd.write(def_fc)
    
    return True

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \fn         SplitPath()

    \brief      Splits the path for file and folder
            
    \params     path - path to file

    \return     File extension found or None
                
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def SplitPath(path):
    
    if path is None:
        return None,None
    
    split_path  = os.path.split(path)
    
    if len(split_path) < 2:
        return None, None
    
    extension = split_path[1].split(".")
    
    if len(extension) < 2:
        return None, None
    
    ret = extension[1].lower()
    
    return ret, extension[0]
    

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \fn         main()

    \brief      The mother of all functions
            
    \params     n/a

    \return     n/a
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def main():

    global  xml_file_path, default_xml_file_path, command_line_path
    global  xml_file_name_keywords
    
    global CREATE_DEFAULT_XML_ONLY, CONFIG_FILE_EXTENSION
    global VERBOSE, PRINT_DISABLED
    
    """ Check to see if Python 2.7 is used """
    if sys.version_info[0] > __required_python_version__[0]        \
        or sys.version_info[1] > __required_python_version__[1]:
        raise AssertionError(
        '\n\nThis template was compiled with Python version 2.7.3!\n'
        'You are using a much higher version which has a different syntax\n'
        'and could lead to unexpected behavior!\n'
        'Aborting operation!\n')
        
    
    """ Get command line arguments """
    arg = sys.argv
    
    if len(arg) > 1:
        opts, args = getopt.getopt(sys.argv[1:], "nvx?")
        
        for o,a in opts:
            if o == "-n":
                CREATE_DEFAULT_XML_ONLY = True
            
            if o == "-v":
                VERBOSE = True
                
            if o == "-x":
                PRINT_DISABLED = True
                
            if o == "-?":
                print "V" + __version__
                sys.exit(0)
        
        """ Get the path from the command line """
        if len(args) == 1:
            command_line_path.m_Path = args[0]
            Print("\nCommand line path received:\n\n", PrintLevels.DEBUG)
            Print(command_line_path.m_Path, PrintLevels.DEBUG)
            
            """ 
                Big problems with cygwin and mingw about the command line path.
                Unix based shells do not accept "\" as path delimitor so they tend
                to cut it out.
                So if you pass somthing like "C:\Projects\Tools\HSMTemplateScaffolding\test"
                to this here script in cygwin you will get something like
                "C:ProjectsToolsHSMTemplateScaffoldingtest"
                
                Till we find a workaround (something like 'cygpath') we must
                stop cygwin script here by searching in the path for '\'. If we
                find it it is a windows cmd shell and we can go on, if not arrivederci!
            """
            if command_line_path.m_Path.find("\\") == -1:
                Print("\nUnable to work inside a cygwin/mingw shell! Aborting!\n", PrintLevels.CRITICAL)
                sys.exit(2)
            
        else:
            Print("\nPath is missing! Aborting!\n", PrintLevels.CRITICAL)
            if PRINT_DISABLED is False:
                Usage()
            sys.exit(2)
            
    elif len(arg) == 1: 
        Print("\nPath is missing! Aborting!\n", PrintLevels.CRITICAL)
        if PRINT_DISABLED is False:
            Usage()
        sys.exit(2)
    
    if PRINT_DISABLED is False:
        Welcome()
    
    """ """"""""""""""""""""""""""""""""""""""""""""""""
        Sanity checks
        
        Is the path a valid file or a valid folder?
        Does it contain a valid xml inside?
        If not can we create the folder or the file?
    """ """"""""""""""""""""""""""""""""""""""""""""""""
    if os.path.isfile(command_line_path.m_Path) is True:
        
        """ Path is a valid file """
        Print("Path is a valid file!\n", PrintLevels.DEBUG)
        
        xml_file_path.m_Path = command_line_path.m_Path
        xml_file_path.m_PathType = ProjectFlags.PATH_IS_FILE
        
    elif os.path.isdir(command_line_path.m_Path) is True:
        
        """ Path is dir, check for xml files """
        Print("Path is a valid folder!\n", PrintLevels.DEBUG)
        
        """ Only check for xml files in the folder if the -n flag was not set """
        if CREATE_DEFAULT_XML_ONLY == True:
            Print("You did not specify a proper file path!\nAborting!", PrintLevels.CRITICAL)
            sys.exit(2)
        
        xml_file_path.m_Path = UsersFileChoice(command_line_path.m_Path)
        xml_file_path.m_PathType = ProjectFlags.PATH_IS_FILE
            
        if xml_file_path.m_Path is None:
            sys.exit(2)
    
    """ 
        The file or folder does not exist
        Only one choice here:
            - if xml file and -n flag then create it with the default value 
              (also create folder if missing)
        If folder do nothing because it does not exist
    """
    if xml_file_path.m_Path is None or xml_file_path.m_PathType != ProjectFlags.PATH_IS_FILE:
        xml_file_path.m_Path = command_line_path.m_Path
        xml_file_path.m_PathType = ProjectFlags.PATH_IS_FILE
    
    """ Split path and get extension and file name """
    ext,name = SplitPath(xml_file_path.m_Path)
    
    """ Check ending """
    if ext != CONFIG_FILE_EXTENSION:
        Print("You did not specify a proper file path!\n"
              "The file path should have a .xml ending!\n"
              "Aborting!", PrintLevels.CRITICAL)
        sys.exit(2)
    
    """ Check for keywords """
    if CheckForKeywords(xml_file_name_keywords,name) is False:
        Print("\nFile name contains no keywords!\n"
              "Aborting!\n\n"
              "Please use at least one of the following keywords in the file name:", PrintLevels.CRITICAL)
        Print(xml_file_name_keywords, PrintLevels.CRITICAL)
        sys.exit(2)
    
    if CREATE_DEFAULT_XML_ONLY is True:
        """ If flag is raised and we have a xml file name then create file from default xml"""
        if CreateXMLFromDefault(xml_file_path.m_Path) is False:
            sys.exit(2)
        else:
            sys.exit(0)
                
    """ """"""""""""""""""""""""""""""""""""""""""""""""
        Create HSM
        
        Now after we have recieved the hsm service 
        structure we can scaffold the hsm service. 
    """ """"""""""""""""""""""""""""""""""""""""""""""""
    if ScaffoldService(xml_file_path.m_Path) != ProjectFlags.STATUS_OKAY:
        sys.exit(2)
    
    return 0
    
if __name__ == '__main__':
    main()

