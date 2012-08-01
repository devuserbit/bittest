#!/usr/bin/env python




#This is the secrete to eternal live 1/2
import os,sys
pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd)

##################################################
## DEPENDENCIES
import sys
import os
import os.path
try:
    import builtins as builtin
except ImportError:
    import __builtin__ as builtin
from os.path import getmtime, exists
import time
import types
from Cheetah.Version import MinCompatibleVersion as RequiredCheetahVersion
from Cheetah.Version import MinCompatibleVersionTuple as RequiredCheetahVersionTuple
from Cheetah.Template import Template
from Cheetah.DummyTransaction import *
from Cheetah.NameMapper import NotFound, valueForName, valueFromSearchList, valueFromFrameOrSearchList
from Cheetah.CacheRegion import CacheRegion
import Cheetah.Filters as Filters
import Cheetah.ErrorCatchers as ErrorCatchers
from templates import genericHeaders
from genericHeaders import genericHeaders

##################################################
## MODULE CONSTANTS
VFFSL=valueFromFrameOrSearchList
VFSL=valueFromSearchList
VFN=valueForName
currentTime=time.time
__CHEETAH_version__ = '2.4.4'
__CHEETAH_versionTuple__ = (2, 4, 4, 'development', 0)
__CHEETAH_genTime__ = 1343804777.117
__CHEETAH_genTimestamp__ = 'Wed Aug 01 09:06:17 2012'
__CHEETAH_src__ = 'hsmService_h.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Aug 01 09:06:01 2012'
__CHEETAH_docstring__ = 'Autogenerated by Cheetah: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class hsmService_h(genericHeaders):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(hsmService_h, self).__init__(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def respond(self, trans=None):



        ## CHEETAH: main method generated for this template
        if (not trans and not self._CHEETAH__isBuffering and not callable(self.transaction)):
            trans = self.transaction # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else: _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter
        
        ########################################
        ## START - generated method body
        
        # 
        #     This is the template for the hsm service
        # 
        #     This is the secret to eternal live 2/2
        #     
        #     Without this you will get no output from the
        #     def's in the parent class
        write(u'''
''')
        #  ############################
        #  Get file header
        #  ############################
        todo = 'TODO'
        bmarker = '#^'
        emarker = '^#'
        service = 'Service'
        name = 'CHSM' + VFSL([locals()]+SL+[globals(), builtin],"srv.Name",True) + VFSL([locals()]+SL+[globals(), builtin],"service",True)
        _v = VFSL([locals()]+SL+[globals(), builtin],"InsertFileHeader",False)(VFSL([locals()]+SL+[globals(), builtin],"name",True), VFSL([locals()]+SL+[globals(), builtin],"extension",True), VFSL([locals()]+SL+[globals(), builtin],"todo",True)) # u'$InsertFileHeader($name, $extension, $todo)' on line 22, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$InsertFileHeader($name, $extension, $todo)')) # from line 22, col 1.
        write(u'''


#ifndef _CHSM_''')
        _v = VFN(VFSL([locals()]+SL+[globals(), builtin],"srv.Name",True),"upper",False)() # u'${srv.Name.upper()}' on line 25, col 16
        if _v is not None: write(_filter(_v, rawExpr=u'${srv.Name.upper()}')) # from line 25, col 16.
        write(u'''_SERVICE_H
#define _CHSM_''')
        _v = VFN(VFSL([locals()]+SL+[globals(), builtin],"srv.Name",True),"upper",False)() # u'${srv.Name.upper()}' on line 26, col 16
        if _v is not None: write(_filter(_v, rawExpr=u'${srv.Name.upper()}')) # from line 26, col 16.
        write(u'''_SERVICE_H

// Include base class service
#include "CHSMService.h"

// Include state headers
// ''')
        _v = VFSL([locals()]+SL+[globals(), builtin],"bmarker",True) # u'${bmarker}' on line 32, col 4
        if _v is not None: write(_filter(_v, rawExpr=u'${bmarker}')) # from line 32, col 4.
        write(u''' HEADERS
''')
        for StateList in VFSL([locals()]+SL+[globals(), builtin],"srv.StateLevelList",True): # generated from line 33, col 1
            for State in VFSL([locals()]+SL+[globals(), builtin],"StateList",True): # generated from line 34, col 1
                write(u'''#include "''')
                _v = VFSL([locals()]+SL+[globals(), builtin],"srv.Name",True) # u'${srv.Name}' on line 35, col 12
                if _v is not None: write(_filter(_v, rawExpr=u'${srv.Name}')) # from line 35, col 12.
                write(u'''.C''')
                _v = VFSL([locals()]+SL+[globals(), builtin],"State.Name",True) # u'${$State.Name}' on line 35, col 25
                if _v is not None: write(_filter(_v, rawExpr=u'${$State.Name}')) # from line 35, col 25.
                write(u'''State.h"
''')
        write(u'''// ''')
        _v = VFSL([locals()]+SL+[globals(), builtin],"emarker",True) # u'${emarker}' on line 38, col 4
        if _v is not None: write(_filter(_v, rawExpr=u'${emarker}')) # from line 38, col 4.
        write(u'''


''')
        # 
        # ## ############################
        # ## Get class header
        # ## ############################
        _v = VFSL([locals()]+SL+[globals(), builtin],"InsertClassHeader",False)(VFSL([locals()]+SL+[globals(), builtin],"name",True), VFSL([locals()]+SL+[globals(), builtin],"todo",True), VFSL([locals()]+SL+[globals(), builtin],"author",True)) # u'$InsertClassHeader($name, $todo, $author)' on line 46, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$InsertClassHeader($name, $todo, $author)')) # from line 46, col 1.
        write(u'''
class ''')
        _v = VFSL([locals()]+SL+[globals(), builtin],"name",True) # u'${name}' on line 47, col 7
        if _v is not None: write(_filter(_v, rawExpr=u'${name}')) # from line 47, col 7.
        write(u''' : public CHSMService
{
public:
''')
        # 
        # ## ############################
        # ## Parameters
        # ## ############################
        params_name = 'C' + VFSL([locals()]+SL+[globals(), builtin],"srv.Name",True) + 'Parameters'
        name_size = len(VFSL([locals()]+SL+[globals(), builtin],"name",True))
        intent = '    '
        space = ' '.rjust(VFSL([locals()]+SL+[globals(), builtin],"name_size",True))
        _v = VFSL([locals()]+SL+[globals(), builtin],"InsertClassHeader",False)(VFSL([locals()]+SL+[globals(), builtin],"params_name",True), todo, VFSL([locals()]+SL+[globals(), builtin],"author",True), VFSL([locals()]+SL+[globals(), builtin],"intent",True)) # u'$InsertClassHeader($params_name, todo, $author, $intent)' on line 59, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$InsertClassHeader($params_name, todo, $author, $intent)')) # from line 59, col 1.
        write(u'''
    struct ''')
        _v = VFSL([locals()]+SL+[globals(), builtin],"params_name",True) # u'${params_name}' on line 60, col 12
        if _v is not None: write(_filter(_v, rawExpr=u'${params_name}')) # from line 60, col 12.
        write(u'''
    {
        INT32U  m_nParameter1;
        INT32U  m_nParameter2;

        //c-tor
        ''')
        _v = VFSL([locals()]+SL+[globals(), builtin],"params_name",True) # u'${params_name}' on line 66, col 9
        if _v is not None: write(_filter(_v, rawExpr=u'${params_name}')) # from line 66, col 9.
        write(u'''(INT32U param1 = 0,
''')
        _v = VFSL([locals()]+SL+[globals(), builtin],"space",True) # u'${space}' on line 67, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'${space}')) # from line 67, col 1.
        write(u''' ''')
        write(u'''        INT32U param2 = 0): m_nParameter1(param1),
''')
        _v = VFSL([locals()]+SL+[globals(), builtin],"space",True) # u'${space}' on line 69, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'${space}')) # from line 69, col 1.
        write(u''' ''')
        write(u'''                            m_nParameter2(param2)
        {
        }
    
    };
    
    ///////////////////////////////////////////////////////////////////
    ///////////////////////// DEFINE IOCTLS /////////////////////////// 
    ///////////////////////////////////////////////////////////////////
    enum IOCTLS
    {
        PREPARE,                 // Prep the system 
        DO_ACTIVITY,             // Do some activity
        LAST_IOCTL
    };
    
    ///////////////////////////////////////////////////////////////////
    ////////////////////////// DEFINE ERRORS //////////////////////////
    ///////////////////////////////////////////////////////////////////
    // Error codes for this object
    #include "enumdefs.h"
    enum
    {
        #include "''')
        _v = VFSL([locals()]+SL+[globals(), builtin],"srv.Name",True) # u'${srv.Name}' on line 93, col 20
        if _v is not None: write(_filter(_v, rawExpr=u'${srv.Name}')) # from line 93, col 20.
        write(u'''.Errors.h"
    };
    
    // Constructor Service.  Place in transport stack is optional
    // By default all services will be place in the service list, for access via PC
    // Any service not wishing to be visible, should use HIDDEN_SERVICE for nSrvNo
    ''')
        _v = VFSL([locals()]+SL+[globals(), builtin],"name",True) # u'${name}' on line 99, col 5
        if _v is not None: write(_filter(_v, rawExpr=u'${name}')) # from line 99, col 5.
        write(u'''(INT16U      nSrvNo,                 // Service Number for external control
''')
        _v = VFSL([locals()]+SL+[globals(), builtin],"space",True) # u'${space}' on line 100, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'${space}')) # from line 100, col 1.
        write(u''' ''')
        write(u'''    const char  *pServiceName,          // Service Name
''')
        _v = VFSL([locals()]+SL+[globals(), builtin],"space",True) # u'${space}' on line 102, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'${space}')) # from line 102, col 1.
        write(u''' ''')
        write(u'''    CTask       *pTask,                 // Task for service to run functions
''')
        _v = VFSL([locals()]+SL+[globals(), builtin],"space",True) # u'${space}' on line 104, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'${space}')) # from line 104, col 1.
        write(u''' ''')
        write(u'''    CService    *pControlledObj);       // Object this state machine controlls

    ///////////////////////////////////////////////////////////////////
    //////////////////////////// CONSTANTS ////////////////////////////
    ///////////////////////////////////////////////////////////////////
    
    // TODO

protected:

    
    ///////////////////////////////////////////////////////////////////
    ////////////////////////// STATE ENUMS ////////////////////////////
    ///////////////////////////////////////////////////////////////////
    enum
    {
        // ''')
        _v = VFSL([locals()]+SL+[globals(), builtin],"bmarker",True) # u'${bmarker}' on line 121, col 12
        if _v is not None: write(_filter(_v, rawExpr=u'${bmarker}')) # from line 121, col 12.
        write(u''' ENUMS
''')
        state_num = 0
        sufix = '_STATE'
        for StateList in VFSL([locals()]+SL+[globals(), builtin],"srv.StateLevelList",True): # generated from line 124, col 1
            for State in VFSL([locals()]+SL+[globals(), builtin],"StateList",True): # generated from line 125, col 1
                post_intend = ' '.rjust(32 - (len(VFSL([locals()]+SL+[globals(), builtin],"State.Name",True)) + len(VFSL([locals()]+SL+[globals(), builtin],"sufix",True)) - 1))
                write(u'''        ''')
                _v = VFN(VFSL([locals()]+SL+[globals(), builtin],"State.Name",True),"upper",False)() # u'${State.Name.upper()}' on line 127, col 9
                if _v is not None: write(_filter(_v, rawExpr=u'${State.Name.upper()}')) # from line 127, col 9.
                _v = VFSL([locals()]+SL+[globals(), builtin],"sufix",True) # u'${sufix}' on line 127, col 30
                if _v is not None: write(_filter(_v, rawExpr=u'${sufix}')) # from line 127, col 30.
                write(u''',''')
                _v = VFSL([locals()]+SL+[globals(), builtin],"post_intend",True) # u'${post_intend}' on line 127, col 39
                if _v is not None: write(_filter(_v, rawExpr=u'${post_intend}')) # from line 127, col 39.
                write(u'''// ''')
                _v = VFSL([locals()]+SL+[globals(), builtin],"state_num",True) # u'${state_num}' on line 127, col 56
                if _v is not None: write(_filter(_v, rawExpr=u'${state_num}')) # from line 127, col 56.
                write(u''' - TODO: Decription
''')
                state_num = VFSL([locals()]+SL+[globals(), builtin],"state_num",True) + 1
        write(u'''        // ''')
        _v = VFSL([locals()]+SL+[globals(), builtin],"emarker",True) # u'${emarker}' on line 131, col 12
        if _v is not None: write(_filter(_v, rawExpr=u'${emarker}')) # from line 131, col 12.
        write(u'''
        LAST_STATE
    } STATE_NUMBERS;
    
    
    ///////////////////////////////////////////////////////////////////
    //////////////////////// CREATE THE STATES //////////////////////// 
    ///////////////////////////////////////////////////////////////////
    
    
    // Friend class declaration
    // make sure our states are friends so they can access this class
    // Compiler requires the namespace - "using" does not help
    // ''')
        _v = VFSL([locals()]+SL+[globals(), builtin],"bmarker",True) # u'${bmarker}' on line 144, col 8
        if _v is not None: write(_filter(_v, rawExpr=u'${bmarker}')) # from line 144, col 8.
        write(u''' FRIENDS
''')
        for StateList in VFSL([locals()]+SL+[globals(), builtin],"srv.StateLevelList",True): # generated from line 145, col 1
            for State in VFSL([locals()]+SL+[globals(), builtin],"StateList",True): # generated from line 146, col 1
                write(u'''    friend class    ns''')
                _v = VFSL([locals()]+SL+[globals(), builtin],"srv.Name",True) # u'${srv.Name}' on line 147, col 23
                if _v is not None: write(_filter(_v, rawExpr=u'${srv.Name}')) # from line 147, col 23.
                _v = VFSL([locals()]+SL+[globals(), builtin],"service",True) # u'${service}' on line 147, col 34
                if _v is not None: write(_filter(_v, rawExpr=u'${service}')) # from line 147, col 34.
                write(u'''::C''')
                _v = VFSL([locals()]+SL+[globals(), builtin],"State.Name",True) # u'${State.Name}' on line 147, col 47
                if _v is not None: write(_filter(_v, rawExpr=u'${State.Name}')) # from line 147, col 47.
                write(u'''State;
''')
        write(u'''    // ''')
        _v = VFSL([locals()]+SL+[globals(), builtin],"emarker",True) # u'${emarker}' on line 150, col 8
        if _v is not None: write(_filter(_v, rawExpr=u'${emarker}')) # from line 150, col 8.
        write(u'''
    
    
    // Define states
    // ''')
        _v = VFSL([locals()]+SL+[globals(), builtin],"bmarker",True) # u'${bmarker}' on line 154, col 8
        if _v is not None: write(_filter(_v, rawExpr=u'${bmarker}')) # from line 154, col 8.
        write(u''' DEFINES
''')
        for StateList in VFSL([locals()]+SL+[globals(), builtin],"srv.StateLevelList",True): # generated from line 155, col 1
            for State in VFSL([locals()]+SL+[globals(), builtin],"StateList",True): # generated from line 156, col 1
                post_intend = ' '.rjust(48 - ((len(VFSL([locals()]+SL+[globals(), builtin],"srv.Name",True)) + len(VFSL([locals()]+SL+[globals(), builtin],"service",True)) + 5) + (len(VFSL([locals()]+SL+[globals(), builtin],"State.Name",True)) + 5)))
                write(u'''    ns''')
                _v = VFSL([locals()]+SL+[globals(), builtin],"srv.Name",True) # u'${srv.Name}' on line 158, col 7
                if _v is not None: write(_filter(_v, rawExpr=u'${srv.Name}')) # from line 158, col 7.
                _v = VFSL([locals()]+SL+[globals(), builtin],"service",True) # u'${service}' on line 158, col 18
                if _v is not None: write(_filter(_v, rawExpr=u'${service}')) # from line 158, col 18.
                write(u'''::C''')
                _v = VFSL([locals()]+SL+[globals(), builtin],"State.Name",True) # u'${State.Name}' on line 158, col 31
                if _v is not None: write(_filter(_v, rawExpr=u'${State.Name}')) # from line 158, col 31.
                write(u'''State''')
                _v = VFSL([locals()]+SL+[globals(), builtin],"post_intend",True) # u'${post_intend}' on line 158, col 49
                if _v is not None: write(_filter(_v, rawExpr=u'${post_intend}')) # from line 158, col 49.
                _v = VFSL([locals()]+SL+[globals(), builtin],"State.Name",True) # u'${State.Name}' on line 158, col 63
                if _v is not None: write(_filter(_v, rawExpr=u'${State.Name}')) # from line 158, col 63.
                write(u'''State;
''')
        write(u'''    // ''')
        _v = VFSL([locals()]+SL+[globals(), builtin],"emarker",True) # u'${emarker}' on line 161, col 8
        if _v is not None: write(_filter(_v, rawExpr=u'${emarker}')) # from line 161, col 8.
        write(u'''
    
    // List of our errors and their respective string
    static const ENUM_STRING Errors[]; 
    
    // Error Translation Table
    static const HSM_SERVICE_ERROR_STRUCT ErrorMap[];
    
    ///////////////////////////////////////////////////////////////////
    //////////////////////////// FUNCTIONS //////////////////////////// 
    ///////////////////////////////////////////////////////////////////

    // Initialize our states
    SYSSTATUS InitStates();
    
    // Get the object we are controlling
    CService *GetControlledObj() const
    {
        return m_pControlledObj;
    }
    
    // Set the object we are controlling
    void SetControlledObj(CService *pNewObj)
    {
        m_pControlledObj = pNewObj;
    }
    
    // Keep a copy of the command that is being processed so
    // that we can return status when it finishes
    void SaveMessage(CServiceMessage *pMsg)
    {
        m_ReturnMessage.CopyOrigMsg(pMsg);
    }

    // Get a pointer to a saved msg
    CServiceMessage *GetSavedMessage()
    {
        return &m_ReturnMessage;
    }
    
    // Accessors for the parameters
    // TODO : Add get and set function when nedded
    
private:

    ///////////////////////////////////////////////////////////////////
    //////////////////////////// VARIABLES //////////////////////////// 
    ///////////////////////////////////////////////////////////////////
    
    // Configurable parameters of the object
    ''')
        _v = VFSL([locals()]+SL+[globals(), builtin],"params_name",True) # u'${params_name}' on line 211, col 5
        if _v is not None: write(_filter(_v, rawExpr=u'${params_name}')) # from line 211, col 5.
        write(u""" m_Parameters;       

    // The current object we're controlling
    CService *m_pControlledObj;

    // A copy of the incoming msg
    CServiceMessage m_ReturnMessage;

    // Define the arrays needed for Fingertip and remote communications
    static const SERVICE_FUNCTIONS ServiceFunctions[];
    static const IOCTL_FUNCTIONS   IOCTLFunctions[];
    static const SERVICE_SIZE_INFO SizeInfo;
};
#endif
""")
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        
    ##################################################
    ## CHEETAH GENERATED ATTRIBUTES


    _CHEETAH__instanceInitialized = False

    _CHEETAH_version = __CHEETAH_version__

    _CHEETAH_versionTuple = __CHEETAH_versionTuple__

    _CHEETAH_genTime = __CHEETAH_genTime__

    _CHEETAH_genTimestamp = __CHEETAH_genTimestamp__

    _CHEETAH_src = __CHEETAH_src__

    _CHEETAH_srcLastModified = __CHEETAH_srcLastModified__

    _mainCheetahMethod_for_hsmService_h= u'respond'

## END CLASS DEFINITION

if not hasattr(hsmService_h, '_initCheetahAttributes'):
    templateAPIClass = getattr(hsmService_h, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(hsmService_h)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=hsmService_h()).run()


