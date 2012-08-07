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

import os , glob, re

files_to_delete = {'.cc' , '.h'}
searchable_folders = {'test','external'}

""" Save current dir for we need it later """
curr_dir = os.path.dirname(os.path.realpath(__file__))

def run_test(params = '', silent=True):
    
    if silent is True:
        fname = "hsm_template.py -x " + params
    else:
        fname = "hsm_template.py " + params
    
    print "hsm_template.py says: \n\n"
    
    ret = os.system(fname)
    
    if silent is True:
        if ret != 0:
            print "\nTest succesfull\n"
        else:
            print "\nTEST FAILED!\n"
            
    return ret

def get_test_case_comment(path):
    commentstring = None
    def_fc = None
    
    if path is None:
        return commentstring
        
    try:
        def_fd = open(path,'r')
    except IOError as e:
        print "Unable to open {0} ({1} : {2})".format(path, e.errno, e.strerror)
        return False
    else:
        def_fc = def_fd.readlines()
        def_fd.close()
    
    commentstring = DoSomeRegExMagic(def_fc)
    return commentstring

def RegexAction(expression, string):
    #pattern = re.compile(expression).match(string) 
    pattern = re.search(expression, string, 0) 
    if pattern is not None:
        return pattern.group()
    else:
        return None    
        
def DoSomeRegExMagic(lines):
    startmarker = False
    commentstring = ""
    if lines is not None:
        for line in lines:
            # Has this line a start marker
            startstring = RegexAction(r'(<!--)', line)
            # Has this line a stop marker
            endstring = RegexAction(r'(-->)', line)
            # Set markers
            if startstring is not None:
                startmarker = True
                continue
            if endstring is not None:
                startmarker = False
                return commentstring                
            if startmarker is True:
                commentstring += line
    return None

    

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
    test_cases = glob.glob('[1-9]*.xml')
    
    if test_cases is None:
        print __func__ + " : Unable to find any xml files in " + __fpath__
    
    """ Change to the root dir so we can call hsm_template.py """
    os.chdir("..\\")
    
    for xml_file in test_cases:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")
        
        fname = curr_dir + "\\" + xml_file
        commentstring = get_test_case_comment(fname)
        if commentstring is not None:
            print("Testing " + commentstring + "\n")
        else:
            print("Testing... \n")
        
        
        
        ret = run_test(fname,False)
        
        """ If test failed then skip wait for user input """
        if ret == 0:
            try:
                uinp = raw_input("\n\nTest succeeded!\nPlease check files and press enter when ready!")
            except EOFError:
                print "Moving on...."
            
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")

    
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
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")
    print("1. Testing empty path\n\n")
    
    run_test()
    
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
    
    """ 2. Testing inexistent folder """
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")
    print("2. Testing inexistent folder\n\n")
    
    run_test("C:\\test\\test\\")
    
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
    
    """ 3. Testing wrong file extension """
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")
    print("3. Testing wrong file extension\n\n")
    
    params = os.getcwd() + "\\hsm_template.py"
    run_test(params)
    
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
    
    """ 4. Testing no file extension """
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")
    print("4. Testing no file extension\n\n")
    
    params = os.getcwd() + "\\templates\\Makefile"
    run_test(params)
    
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
    
    """ 5. Testing missing keywords """
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")
    print("5. Testing missing keywords")
    
    params = os.getcwd() + "\\test\\test_no_keywords.xml"
    run_test(params)
    
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
    
    """ 6. Testing existent valid file without keywords """
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")
    print("6. Testing existent valid file without keywords")
    
    params = os.getcwd() + "\\test\\hsm_test_service_HSM.xml"
    run_test(params)
    
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
    
    run_test_cases()
    
    return 0

if __name__ == '__main__':
    main()

