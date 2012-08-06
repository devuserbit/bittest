#! /python27/python.exe
# -*- coding: utf-8 -*-
#

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    Copyright (c) 2012 BIT Analytical Instruments GmbH. All rights reserved
    
    Designed for Python V2.7.2
    
    
    @@@ ABSTRACT
        Script used for automatic hsm_template testing
    
    
    @@@ REVISION HISTORY
    
        Vers.   Date            Name            Comment
    
        1.0     31.07.2012      APopescu        Initial version

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import os , glob

files_to_delete = {'.cc' , '.h'}
searchable_folders = {'test','external'}

""" Save current dir for we need it later """
curr_dir = os.path.dirname(os.path.realpath(__file__))

def run_test(params = '', silent=True):
    
    if silent is True:
        fname = "hsm_template.py -x " + params
    else:
        fname = "hsm_template.py " + params
    
    ret = os.system(fname)
    
    if silent is True:
        if ret != 0:
            print "\nTest succesfull\n"
        else:
            print "\nTEST FAILED!\n"

def run_test_cases():
    
    __func__  = "run_test_cases()"
    
    """ 
        To find files we must change to test dir first 
        
        It seems that when doing a os.path.dirname you get
        a single backslashed path like:
        
            C:\Project\Tools\hsmtemplate\test
            
        Which is not really a valid path because each backslash
        must be escaped for a windows based enviroment using unix
        utils. So when passing this path to glob.glob you get
        nothing :-(
    """
    os.chdir(curr_dir)
    
    """ Find all test case xml's starting with numbers """
    test_cases = []
    test_cases = glob.glob('[1-9]*.xml')
    
    if test_cases is None:
        print __func__ + " : Unable to find any xml files in " + __fpath__
    
    """ Change to the root dir so we can call hsm_template.py """
    os.chdir("..\\")
    
    for xml_file in test_cases:
        print("-------------------------------------------------------------\n")
        print("Testing " + xml_file + "\n")
        fname = curr_dir + "\\" + xml_file
        
        run_test(fname,False)
        
        print("\n-------------------------------------------------------------\n")

    
def main():
    
    global curr_dir
    
    print("\n")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("~                                                                 ~")
    print("~                                                                 ~")
    print("~                     HSM Service testing                         ~")
    print("~                                                                 ~")
    print("~                                                                 ~")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("\n")
    
    """ Change to the root dir so we can call hsm_template.py """
    os.chdir("..\\")
    
    """ 1. Testing empty path"""
    print("-------------------------------------------------------------\n")
    print("1. Testing empty path\n\n")
    
    run_test()
    
    print("-------------------------------------------------------------\n")
    
    """ 2. Testing inexistent folder """
    print("-------------------------------------------------------------\n")
    print("2. Testing inexistent folder\n\n")
    
    run_test("C:\\test\\test\\")
    
    print("-------------------------------------------------------------\n")
    
    """ 3. Testing wrong file extension """
    print("-------------------------------------------------------------\n")
    print("3. Testing wrong file extension\n\n")
    
    params = os.getcwd() + "\\hsm_template.py"
    run_test(params)
    
    print("-------------------------------------------------------------\n")
    
    """ 4. Testing no file extension """
    print("-------------------------------------------------------------\n")
    print("4. Testing no file extension\n\n")
    
    params = os.getcwd() + "\\templates\\Makefile"
    run_test(params)
    
    print("-------------------------------------------------------------\n")
    
    """ 5. Testing missing keywords """
    print("-------------------------------------------------------------\n")
    print("5. Testing missing keywords")
    
    params = os.getcwd() + "\\test\\test_no_keywords.xml"
    run_test(params)
    
    print("-------------------------------------------------------------\n")
    
    """ 6. Testing existent valid file without keywords """
    print("-------------------------------------------------------------\n")
    print("6. Testing existent valid file without keywords")
    
    params = os.getcwd() + "\\test\\hsm_test_service_HSM.xml"
    run_test(params)
    
    print("-------------------------------------------------------------\n")
    
    run_test_cases()
    
    return 0

if __name__ == '__main__':
    main()

