#! /python27/python.exe

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    Copyright (c) 2012 BIT Analytical Instruments GmbH. All rights reserved
    
    Designed for Python V2.7.2
    
    
    @@@ ABSTRACT
        Parses the xml file and returns the hierarchy of the hsm
    
    
    @@@ REVISION HISTORY
    
        Vers.   Date            Name            Comment
    
        1.0     28.06.2012      BMoll           Initial version
        1.1     06.07.2012      BMoll           Enhancements
        1.2     16.07.2012      BMoll           Initial/Dynamic fix
        1.3     16.07.2012      BMoll           callbacks and std_fcts are now dictionaries

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""" """"""""""""""""""""""""""""""""""""""""""""""""
    File information
""" """"""""""""""""""""""""""""""""""""""""""""""""
__filename__    = "hsm_template.py"
__version__     = "$Revision: $"
__author__      = "$LastChangedBy:        $"
__date__        = "$LastChangedDate:   $"

""" """"""""""""""""""""""""""""""""""""""""""""""""
    Imports
""" """"""""""""""""""""""""""""""""""""""""""""""""
import ctypes
import subprocess
import sys, os, imp
import shutil
import xml.dom.minidom as dom

""" """"""""""""""""""""""""""""""""""""""""""""""""
    Global defines
""" """"""""""""""""""""""""""""""""""""""""""""""""
COMMENT_NODE = 8
PARENT_NODE = "hsm_service"
STATE_NODE = "state"
MAX_SUBSTATE_LEVELS = 7
INVALID_NODE = "#text"
  
  
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \class      HSMStruct

    \brief      TODO
            
    \author     BMoll
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class HSMStruct:
    """ Class to represent an HSM hierachy """
    # Each Level is an array organized in an array
    StateLevelList = [[] for x in xrange(MAX_SUBSTATE_LEVELS)] 
    # Keep track of nesting
    NestingDepth = -1
    MaxNesting = 0
    
    def GetRootElement(self):
        """ Haha that was easy """
        return self.StateLevelList[0][0]
        
    def GetMaxNestingDepth(self):
        return self.MaxNesting
        
    def GetStateList(self):
        return self.StateLevelList
 
    def PreviousLevel(self):
        if self.NestingDepth > -1:
            self.NestingDepth = self.NestingDepth - 1
            
    def NextLevel(self):
        if self.NestingDepth < 6:
            self.NestingDepth = self.NestingDepth + 1
            self.MaxNesting = self.NestingDepth 
            
    def AddSubState(self, StateDict):
        """ Add it to our List """
        state = State(StateDict)
        state.Depth = self.NestingDepth
        self.StateLevelList[self.NestingDepth].append(state)
        return state
       

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \class      State

    \brief      TODO
            
    \author     BMoll
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class State:
    """ Class to represent a state. Sit down and take a dict or just the member vars, whatever you want """
    Name = ""
    Callbacks = []
    Functions = []
    Initial = False
    Dynamic = False
    Dict = {}
    Parent = None
    ChildList = []
    Depth = 0
    
    def __init__(self, StateDict):
        """ CTOR """
        self.Name = StateDict['Name']
        self.Callbacks = StateDict['Callbacks']
        self.Functions = StateDict['Functions']
        self.Initial = StateDict['Initial']
        self.Dynamic = StateDict['Dynamic']
        self.Parent = StateDict['Parent']
        # Provide a dict as well
        self.Dict = StateDict
        # We need to initialize members otherwise it is threatend as singleton
        self.ChildList = []
    
    def AddChild(self, Child):
        if Child is not None:
            self.ChildList.append(Child)
            self.Dict['Childs'] = self.ChildList
    
    def HasChildren(self):
        if len(self.ChildList) > 0:
            return True
            
    def GetChildren(self):
        return self.ChildList
    

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \class      ParseXML

    \brief      TODO
            
    \author     BMoll
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class ParseXML:
    """ This class takes an XML as parameter and returns an HSM object. """
    XMLPath = ""
    HSM = HSMStruct()
    Debug = False
    
    def __init__(self, PathToXml, Mode = False):
        """ CTOR """
        self.XMLPath = PathToXml
        self.Debug = Mode
        if (os.path.isfile(self.XMLPath)):
            self.Parse(self.XMLPath)
        else:
            print "Path not found or invalid: " + PathToXml
            
    def GetHSMStruct(self):
        return self.HSM
        
    def CreateStateFromNode(self, Node, ParentNode):
        """ We assume a Node which represents a state - should be verified already.
            State will be added to HSM Struct.
            Lets use a dict - makes it easier for now """
            
        StateName = ""
        CallbackDict = {'entry':False,'active':False,'exit':False}
        FunctionsDict = {'stdcmd':False,'abort':False,'cmd':False,'reset':False,'timer':False,'all':False}
        Initial = False
        Dynamic = False

        if Node.hasAttributes():
            StateName = Node.getAttribute("name")
            if Node.hasAttribute("Initial"):
                isInitial = Node.getAttribute("Initial").upper()
                if (isInitial == "TRUE"):
                    Initial = True
                else:
                    Initial = False

            if Node.hasAttribute("Dynamic"):
                isDynamic = Node.getAttribute("Dynamic").upper()
                if (isDynamic == "TRUE"):
                    Dynamic = True
                else:
                    Dynamic = False

                
        for sub_node in Node.childNodes:
            if sub_node.nodeName == 'callbacks':
                if sub_node.hasChildNodes():
                    for callback in sub_node.childNodes:
                        if callback.nodeName != INVALID_NODE:
                            if(callback.nodeName == "entry"):
                                CallbackDict['entry'] = True
                            if(callback.nodeName == "active"):
                                CallbackDict['active'] = True
                            if(callback.nodeName == "exit"):
                                CallbackDict['exit'] = True                                
 

            if sub_node.nodeName == 'default_fct':
                if sub_node.hasChildNodes():
                    for function in sub_node.childNodes:
                        if function.nodeName != "#text":
                            if(function.nodeName == "stdcmd "):
                                FunctionsDict['stdcmd'] = True
                            if(function.nodeName == "abort"):
                                FunctionsDict['abort'] = True
                            if(function.nodeName == "reset"):
                                FunctionsDict['reset'] = True
                            if(function.nodeName == "timer"):
                                FunctionsDict['timer'] = True
                            if(function.nodeName == "cmd"):
                                FunctionsDict['cmd'] = True
                            if(function.nodeName == "all"):
                                FunctionsDict['all'] = True                                    
        
        StateDict = {   'Name': StateName, 
                        'Callbacks':CallbackDict, 
                        'Functions':FunctionsDict, 
                        'Initial':Initial, 
                        'Dynamic':Dynamic,
                        'Parent' :ParentNode,
                        'NestLevel':self.HSM.NestingDepth
                    }
        
        return self.HSM.AddSubState(StateDict)
        
                                        
    def DigForGold(self, ParentNode, ParentState=None):
        """ Look if we got child nodes within ParentNode """
        # Increase nesting depth
        self.HSM.NextLevel()
        # Loop through node of ParentNode
        for StateNode in ParentNode.childNodes:
            # Look for desired state nodes within given ParentNode
            if (StateNode.nodeName == STATE_NODE):
                # We have a hit - create a state from node
                state = self.CreateStateFromNode(StateNode, ParentState)
                if ParentState is not None:
                    ParentState.AddChild(state)
                # Recursive call
                self.DigForGold(StateNode, state)
        # Decrease Nesting Depth
        self.HSM.PreviousLevel()       
        
    
    def Parse(self, FilePath): 
        """ Parse XML using DOM module """
        Tree = dom.parse(FilePath)         
        for TopLevelNode in Tree.childNodes:
            # Remember: any comment is a node as well
            if (TopLevelNode.nodeType == COMMENT_NODE):
                continue
            # Look for our xml hierachy named PARENT_NODE
            if (TopLevelNode.nodeName == PARENT_NODE):
                # Look if we got a child state
                if TopLevelNode.hasAttributes():
                    self.HSM.Name = TopLevelNode.getAttribute("name")
                    self.DigForGold(TopLevelNode)
                else:
                    print "Error - no HSM name given"
                    return
                    
        if(self.Debug is True):
            self.DebugOutput()

            
    def DebugOutput(self):
        """ Output for debug purposes """
        depth = self.HSM.GetMaxNestingDepth()
        for x in range(0,depth):
            for i in self.HSM.StateLevelList[x]:
                for key, value in dict.items(i.Dict):
                    # let's format the output a little bit
                    print '{:} {:12} {:>3} {:<15} '.format("-".rjust(i.Dict['NestLevel'] * 2), key,":", value)

                              
if __name__ == "__main__":
    if len(sys.argv) > 1:
        x = ParseXML(sys.argv[1])
    else:
        print "no path given"
