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
__CHEETAH_genTime__ = 1343804777.18
__CHEETAH_genTimestamp__ = 'Wed Aug 01 09:06:17 2012'
__CHEETAH_src__ = 'hsmState_cc.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Aug 01 08:54:51 2012'
__CHEETAH_docstring__ = 'Autogenerated by Cheetah: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class hsmState_cc(genericHeaders):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(hsmState_cc, self).__init__(*args, **KWs)
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
        #     This is the template for the hsm states
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
        service = 'Service'
        if VFSL([locals()]+SL+[globals(), builtin],"protected",True) == False: # generated from line 19, col 1
            srv_name = VFSL([locals()]+SL+[globals(), builtin],"srv.Name",True)
            serv_name = 'CHSM' + VFSL([locals()]+SL+[globals(), builtin],"srv.Name",True) + VFSL([locals()]+SL+[globals(), builtin],"service",True)
        else: # generated from line 22, col 1
            srv_name = VFN(VFSL([locals()]+SL+[globals(), builtin],"srv",True),"Name",True)[1:]
            serv_name = 'CHSM' + VFN(VFSL([locals()]+SL+[globals(), builtin],"srv",True),"Name",True)[1:] + VFSL([locals()]+SL+[globals(), builtin],"service",True)
        state_name = 'C' +  VFSL([locals()]+SL+[globals(), builtin],"state.Name",True) + 'State'
        intent = '    '
        def_fct_key = {'cmd', 'reset', 'resp', 'event', 'abort', 'timer', 'stdcmd'}
        def_fct = {                            'cmd'       : 'Command',                            'stdcmd'    : 'StdCommand',                            'reset'     : 'Reset',                            'resp'      : 'Response',                            'event'     : 'Event',                            'abort'     : 'Abort',                            'timer'     : 'Timer'                            }
        serv_msg_type = {                            'cmd'       : 'COMMAND_TYPE',                            'stdcmd'    : 'STD_COMMAND_TYPE',                            'reset'     : 'RESET_TYPE',                            'resp'      : 'COMMAND_RESPONSE_TYPE',                            'event'     : 'SYSTEM_EVENT_TYPE',                            'abort'     : 'ABORT_TYPE',                            'timer'     : 'TIMEOUT_TYPE'                            }
        callbacks = {                            'entry'     : 'OnEntry',                            'active'    : 'OnActive',                            'exit'      : 'OnExit'                            }
        _v = VFSL([locals()]+SL+[globals(), builtin],"InsertFileHeader",False)(VFSL([locals()]+SL+[globals(), builtin],"state_name",True), VFSL([locals()]+SL+[globals(), builtin],"extension",True), VFSL([locals()]+SL+[globals(), builtin],"todo",True)) # u'$InsertFileHeader($state_name, $extension, $todo)' on line 52, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$InsertFileHeader($state_name, $extension, $todo)')) # from line 52, col 1.
        write(u'''

#include "''')
        _v = VFSL([locals()]+SL+[globals(), builtin],"serv_name",True) # u'${serv_name}' on line 54, col 12
        if _v is not None: write(_filter(_v, rawExpr=u'${serv_name}')) # from line 54, col 12.
        write(u'''.h"
#include "''')
        _v = VFSL([locals()]+SL+[globals(), builtin],"srv_name",True) # u'${srv_name}' on line 55, col 12
        if _v is not None: write(_filter(_v, rawExpr=u'${srv_name}')) # from line 55, col 12.
        write(u'''.''')
        _v = VFSL([locals()]+SL+[globals(), builtin],"state_name",True) # u'${state_name}' on line 55, col 24
        if _v is not None: write(_filter(_v, rawExpr=u'${state_name}')) # from line 55, col 24.
        write(u'''.h"

using namespace ns''')
        _v = VFSL([locals()]+SL+[globals(), builtin],"srv_name",True) # u'${srv_name}' on line 57, col 19
        if _v is not None: write(_filter(_v, rawExpr=u'${srv_name}')) # from line 57, col 19.
        _v = VFSL([locals()]+SL+[globals(), builtin],"service",True) # u'${service}' on line 57, col 30
        if _v is not None: write(_filter(_v, rawExpr=u'${service}')) # from line 57, col 30.
        write(u''';

''')
        #  ############################
        #  OnEntry
        #  ############################
        case = 'entry'
        if VFN(VFSL([locals()]+SL+[globals(), builtin],"state.Callbacks",True),"get",False)(VFSL([locals()]+SL+[globals(), builtin],"case",True)) == True: # generated from line 63, col 1
            params = {'pMsg'}
            comment = 'Entry handler for this ' + VFSL([locals()]+SL+[globals(), builtin],"state.Name",True) + ' state'
            _v = VFSL([locals()]+SL+[globals(), builtin],"InsertFunctionHeader",False)(VFSL([locals()]+SL+[globals(), builtin],"state_name",True), VFN(VFSL([locals()]+SL+[globals(), builtin],"callbacks",True),"get",False)(VFSL([locals()]+SL+[globals(), builtin],"case",True)), VFSL([locals()]+SL+[globals(), builtin],"comment",True), VFSL([locals()]+SL+[globals(), builtin],"params",True), 'HSM_SVC_STATE_RESPONSE') # u"$InsertFunctionHeader($state_name, $callbacks.get($case), $comment, $params, 'HSM_SVC_STATE_RESPONSE')" on line 66, col 1
            if _v is not None: write(_filter(_v, rawExpr=u"$InsertFunctionHeader($state_name, $callbacks.get($case), $comment, $params, 'HSM_SVC_STATE_RESPONSE')")) # from line 66, col 1.
            write(u'''
HSM_SVC_STATE_RESPONSE ''')
            _v = VFSL([locals()]+SL+[globals(), builtin],"state_name",True) # u'${state_name}' on line 67, col 24
            if _v is not None: write(_filter(_v, rawExpr=u'${state_name}')) # from line 67, col 24.
            write(u'''::''')
            _v = VFN(VFSL([locals()]+SL+[globals(), builtin],"callbacks",True),"get",False)(VFSL([locals()]+SL+[globals(), builtin],"case",True)) # u'${callbacks.get($case)}' on line 67, col 39
            if _v is not None: write(_filter(_v, rawExpr=u'${callbacks.get($case)}')) # from line 67, col 39.
            write(u'''(CServiceMessage *pMsg)
{

    // Report back that the message is handled.
    HSM_RET_MSG_HANDLED();
}
''')
        write(u'''
''')
        #  ############################
        #  OnActive
        #  ############################
        case = 'active'
        if VFN(VFSL([locals()]+SL+[globals(), builtin],"state.Callbacks",True),"get",False)(VFSL([locals()]+SL+[globals(), builtin],"case",True)) == True: # generated from line 79, col 1
            params = {'pMsg'}
            leftover = []
            comment = 'Our state is active. Take messages.'
            _v = VFSL([locals()]+SL+[globals(), builtin],"InsertFunctionHeader",False)(VFSL([locals()]+SL+[globals(), builtin],"state_name",True), VFN(VFSL([locals()]+SL+[globals(), builtin],"callbacks",True),"get",False)(VFSL([locals()]+SL+[globals(), builtin],"case",True)), VFSL([locals()]+SL+[globals(), builtin],"comment",True), VFSL([locals()]+SL+[globals(), builtin],"params",True), 'HSM_SVC_STATE_RESPONSE') # u"$InsertFunctionHeader($state_name, $callbacks.get($case), $comment, $params, 'HSM_SVC_STATE_RESPONSE')" on line 83, col 1
            if _v is not None: write(_filter(_v, rawExpr=u"$InsertFunctionHeader($state_name, $callbacks.get($case), $comment, $params, 'HSM_SVC_STATE_RESPONSE')")) # from line 83, col 1.
            write(u'''
HSM_SVC_STATE_RESPONSE ''')
            _v = VFSL([locals()]+SL+[globals(), builtin],"state_name",True) # u'${state_name}' on line 84, col 24
            if _v is not None: write(_filter(_v, rawExpr=u'${state_name}')) # from line 84, col 24.
            write(u'''::''')
            _v = VFN(VFSL([locals()]+SL+[globals(), builtin],"callbacks",True),"get",False)(VFSL([locals()]+SL+[globals(), builtin],"case",True)) # u'${callbacks.get($case)}' on line 84, col 39
            if _v is not None: write(_filter(_v, rawExpr=u'${callbacks.get($case)}')) # from line 84, col 39.
            write(u'''(CServiceMessage *pMsg)
{
    // Handle all the message types
    switch(pMsg->GetMsgType())
    {
''')
            #  Scroll to the callbacks and add those existing
            for fct in VFSL([locals()]+SL+[globals(), builtin],"def_fct_key",True): # generated from line 90, col 1
                if VFN(VFSL([locals()]+SL+[globals(), builtin],"state.Functions",True),"get",False)(VFSL([locals()]+SL+[globals(), builtin],"fct",True)) == True or VFN(VFSL([locals()]+SL+[globals(), builtin],"state.Functions",True),"get",False)('all') == True: # generated from line 91, col 1
                    write(u'''        case CServiceMessage::''')
                    _v = VFN(VFSL([locals()]+SL+[globals(), builtin],"serv_msg_type",True),"get",False)(VFSL([locals()]+SL+[globals(), builtin],"fct",True)) # u'$serv_msg_type.get($fct)' on line 92, col 31
                    if _v is not None: write(_filter(_v, rawExpr=u'$serv_msg_type.get($fct)')) # from line 92, col 31.
                    write(u''':
        {
            return On''')
                    _v = VFN(VFSL([locals()]+SL+[globals(), builtin],"def_fct",True),"get",False)(VFSL([locals()]+SL+[globals(), builtin],"fct",True)) # u'${def_fct.get($fct)}' on line 94, col 22
                    if _v is not None: write(_filter(_v, rawExpr=u'${def_fct.get($fct)}')) # from line 94, col 22.
                    write(u'''Msg(pMsg);
        }
''')
                else: # generated from line 96, col 1
                    #  Add to $leftovers to be added at the end
                    _v = VFN(VFSL([locals()]+SL+[globals(), builtin],"leftover",True),"append",False)(VFSL([locals()]+SL+[globals(), builtin],"fct",True)) # u'$leftover.append($fct)' on line 98, col 1
                    if _v is not None: write(_filter(_v, rawExpr=u'$leftover.append($fct)')) # from line 98, col 1.
                    write(u'''
''')
            if len(VFSL([locals()]+SL+[globals(), builtin],"leftover",True)) > 0: # generated from line 101, col 1
                for i in VFSL([locals()]+SL+[globals(), builtin],"leftover",True): # generated from line 102, col 1
                    write(u'''        case CServiceMessage::''')
                    _v = VFN(VFSL([locals()]+SL+[globals(), builtin],"serv_msg_type",True),"get",False)(VFSL([locals()]+SL+[globals(), builtin],"i",True)) # u'$serv_msg_type.get($i)' on line 103, col 31
                    if _v is not None: write(_filter(_v, rawExpr=u'$serv_msg_type.get($i)')) # from line 103, col 31.
                    write(u''':
''')
            write(u'''        default:
        {
            // Set to Handled
            HSM_RET_MSG_HANDLED();
        }
        
    }   // switch on message type
}''')
        write(u'''
''')
        #  ############################
        #  OnExit
        #  ############################
        case = 'exit'
        if VFN(VFSL([locals()]+SL+[globals(), builtin],"state.Callbacks",True),"get",False)(VFSL([locals()]+SL+[globals(), builtin],"case",True)) == True: # generated from line 120, col 1
            comment = 'exit - cleanup or statistics on state'
            _v = VFSL([locals()]+SL+[globals(), builtin],"InsertFunctionHeader",False)(VFSL([locals()]+SL+[globals(), builtin],"state_name",True), VFN(VFSL([locals()]+SL+[globals(), builtin],"callbacks",True),"get",False)(VFSL([locals()]+SL+[globals(), builtin],"case",True)), VFSL([locals()]+SL+[globals(), builtin],"comment",True)) # u'$InsertFunctionHeader($state_name, $callbacks.get($case), $comment)' on line 122, col 1
            if _v is not None: write(_filter(_v, rawExpr=u'$InsertFunctionHeader($state_name, $callbacks.get($case), $comment)')) # from line 122, col 1.
            write(u'''
void ''')
            _v = VFSL([locals()]+SL+[globals(), builtin],"state_name",True) # u'${state_name}' on line 123, col 6
            if _v is not None: write(_filter(_v, rawExpr=u'${state_name}')) # from line 123, col 6.
            write(u'''::''')
            _v = VFN(VFSL([locals()]+SL+[globals(), builtin],"callbacks",True),"get",False)(VFSL([locals()]+SL+[globals(), builtin],"case",True)) # u'${callbacks.get($case)}' on line 123, col 21
            if _v is not None: write(_filter(_v, rawExpr=u'${callbacks.get($case)}')) # from line 123, col 21.
            write(u'''()
{
    // nothing yet
}
''')
        write(u'''
''')
        #  ############################
        #  Default fct
        #  ############################
        for fct in VFSL([locals()]+SL+[globals(), builtin],"def_fct_key",True): # generated from line 132, col 1
            if VFN(VFSL([locals()]+SL+[globals(), builtin],"state.Functions",True),"get",False)(VFSL([locals()]+SL+[globals(), builtin],"fct",True)) == True or VFN(VFSL([locals()]+SL+[globals(), builtin],"state.Functions",True),"get",False)('all') == True: # generated from line 133, col 1
                fct_name = 'On' + VFN(VFSL([locals()]+SL+[globals(), builtin],"def_fct",True),"get",False)(VFSL([locals()]+SL+[globals(), builtin],"fct",True)) + 'Msg'
                params = {'pMsg'}
                _v = VFSL([locals()]+SL+[globals(), builtin],"InsertFunctionHeader",False)(VFSL([locals()]+SL+[globals(), builtin],"state_name",True), VFSL([locals()]+SL+[globals(), builtin],"fct_name",True), VFSL([locals()]+SL+[globals(), builtin],"todo",True), VFSL([locals()]+SL+[globals(), builtin],"params",True), 'HSM_SVC_STATE_RESPONSE') # u"$InsertFunctionHeader($state_name, $fct_name, $todo, $params, 'HSM_SVC_STATE_RESPONSE')" on line 136, col 1
                if _v is not None: write(_filter(_v, rawExpr=u"$InsertFunctionHeader($state_name, $fct_name, $todo, $params, 'HSM_SVC_STATE_RESPONSE')")) # from line 136, col 1.
                write(u'''
HSM_SVC_STATE_RESPONSE ''')
                _v = VFSL([locals()]+SL+[globals(), builtin],"state_name",True) # u'${state_name}' on line 137, col 24
                if _v is not None: write(_filter(_v, rawExpr=u'${state_name}')) # from line 137, col 24.
                write(u'''::''')
                _v = VFSL([locals()]+SL+[globals(), builtin],"fct_name",True) # u'${fct_name}' on line 137, col 39
                if _v is not None: write(_filter(_v, rawExpr=u'${fct_name}')) # from line 137, col 39.
                write(u'''(CServiceMessage *pMsg)
{
    // TODO

    // Done with the message
    HSM_RET_MSG_HANDLED();
}

''')
        
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

    _mainCheetahMethod_for_hsmState_cc= u'respond'

## END CLASS DEFINITION

if not hasattr(hsmState_cc, '_initCheetahAttributes'):
    templateAPIClass = getattr(hsmState_cc, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(hsmState_cc)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=hsmState_cc()).run()


