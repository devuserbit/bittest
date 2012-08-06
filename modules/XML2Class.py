#! /python27/python.exe

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    Copyright (c) 2012 BIT Analytical Instruments GmbH. All rights reserved
    
    Designed for Python V2.7.2
    
    
    @@@ ABSTRACT
        Parses the XML file and returns the hierarchy of an HSM.
        And yes, this process is called parsing ->
        http://en.wikipedia.org/wiki/Parsing 
    
    
    @@@ REVISION HISTORY
    
        Vers.   Date            Name            Comment
    
        1.0     28.06.2012      BMoll           Initial version
        1.1     06.07.2012      BMoll           Enhancements
        1.2     16.07.2012      BMoll           Initial/Dynamic fix
        1.3     16.07.2012      BMoll           callbacks and std_fcts are now dictionaries
        1.4     23.07.2012      BMoll           service is now set invalid as well and minor changes
        1.5     26.07.2012      BMoll           Detect duplicate state entries, 
                                                added error handling,
                                                error nodes are commented out,
                                                added status error flag to HSM struct

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

    \brief      Class to represent an HSM hierachy 
            
    \author     BMoll
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class HSMStruct:
    # 2D array which has several nesting levels where each level can
    # hold several states
    StateLevelList = [[] for x in xrange(MAX_SUBSTATE_LEVELS)] 
    # Keep track of nesting
    NestingDepth = -1
    MaxNesting = 0
    HSM = None
    DuplicateEntries = []
    # Global Error Flag
    ErrorFlag = False
    InitialState = False
    
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
        # Look for duplicate entries
        if (self.FindState(state.Name) == True):
            return None
        self.StateLevelList[self.NestingDepth].append(state)
        return state
    
    def FindState(self, StateName):
        """ Look if we got this state already in our state list """
        for StateLevel in self.StateLevelList:
            for State in StateLevel:
                # Check for protected states as well
                if State.Name == StateName or State.Name == "!"+StateName:
                    self.DuplicateEntries.append(StateName)
                    return True
        return False
               
       

""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    \class      State

    \brief      Class to represent a state. Sit down and take a dict or just the member vars, whatever you want
            
    \author     BMoll
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class State:
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

    \brief      This class PARSES a given XML and returns an HSM object.
            
    \author     BMoll
            
""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class ParseXML:
    # Path to XML file
    XMLPath = ""
    # Reference to an HSM struct
    HSM = HSMStruct()
    # Debug Switch
    Debug = False
    # Hold the DOM reference of the XML
    XMLTree = None
    
    def __init__(self, PathToXml = "", Mode = False):
        """ CTOR """
        self.XMLPath = PathToXml
        self.Debug = Mode
        if (os.path.isfile(self.XMLPath)):
            self.Parse(self.XMLPath)
        else:
            self.HandleError("Path to XML not found or invalid\n"  + PathToXml, True)
            
    def GetHSMStruct(self):
        return self.HSM
        
    def GetTargetPath(self):
        return self.HSM.Path        
    
    def CommentOutNode(self, ParentNode, Node):
        """ Comment out the given node """
        doc = dom.Document()
        ParentNode.insertBefore(doc.createComment("ERROR FOUND IN THIS NODE. COMMENTED OUT AND NOT USED FOR PARSING. \n" + Node.toxml()), Node)
        ParentNode.removeChild(Node)
        self.HandleError("Node commented out", False)
            
    def CreateStateFromNode(self, Node, ParentNode, ParentState):
        """ We assume a Node which represents a state - should be verified already.
            State will be added to HSM Struct. Lets use a dict - makes it easier 
            for now 
            @RET: State instance or None in case of error """
        
        # Initialize vars    
        StateName = ""
        CallbackDict = {'entry':False,'active':False,'exit':False}
        FunctionsDict = {'stdcmd':False,'abort':False,'cmd':False,'reset':False,'timer':False,'all':False}
        Initial = False
        Dynamic = False

        # Mandatory attribute
        if Node.hasAttribute("name"):
            StateName = Node.getAttribute("name")
            if StateName == "":
                self.HandleError("State node has no name", False)
                self.CommentOutNode(ParentNode, Node)
                return None
        else:
            self.HandleError("State node is missing name attribute", False)
            self.CommentOutNode(ParentNode, Node)
            return None

        # Check the given node for additional attributes
        if Node.hasAttributes():
            if Node.hasAttribute("Initial"):
                isInitial = Node.getAttribute("Initial").upper()
                if (isInitial == "TRUE"):
                    if self.HSM.InitialState is False:
                        Initial = True
                        self.HSM.InitialState = True
                    else:
                        # There can only be one initial state
                        self.HandleError("There is more than one state set to initial", False)
                        self.CommentOutNode(ParentNode, Node)
                        return None                        
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
                            if(function.nodeName == "stdcmd"):
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
                    
            
        # Create a dict that represents a State
        StateDict = {   'Name': StateName, 
                        'Callbacks':CallbackDict, 
                        'Functions':FunctionsDict, 
                        'Initial':Initial, 
                        'Dynamic':Dynamic,
                        'Parent' :ParentState,
                        'NestLevel':self.HSM.NestingDepth
                    }
        
        # Pass the dictonary to the HSM struct to add it as a sub state
        State = self.HSM.AddSubState(StateDict)
        
        if State is None:
            # State is redundant
            self.HandleError("Duplicated state node detected", False)
            self.CommentOutNode(ParentNode, Node)
            return None
        else:
            # Return created state            
            return State
        
                                        
    def DigForGold(self, ParentNode, ParentState=None):
        """ Look if we got child nodes within ParentNode and determine 
            if this node is a state. If so add it so our HSM structure.
            @RET: nothing"""
        
        # Increase nesting depth
        self.HSM.NextLevel()
        # Loop through node of ParentNode
        for StateNode in ParentNode.childNodes:
            # Look for desired state nodes within given ParentNode
            if (StateNode.nodeName == STATE_NODE):
                # We have a hit - create a state from node
                state = self.CreateStateFromNode(StateNode, ParentNode, ParentState)
                if ParentState is not None and state is not None:
                    ParentState.AddChild(state)
                # Recursive call
                self.DigForGold(StateNode, state)
        # Decrease Nesting Depth
        self.HSM.PreviousLevel()       
        
    
    def Parse(self, FilePath): 
        """ Parse XML using DOM module
            @RET: nothing """
        
        # XMLTree is a class member for later access
        try:
            self.XMLTree = dom.parse(FilePath)
        except: 
            self.HandleError("XML Style Error. Please perform a syntax style check.", True)
            return
        
        # Loop through XML hierachy 
        for TopLevelNode in self.XMLTree.childNodes:
            # Remember: any comment is a node as well
            if (TopLevelNode.nodeType == COMMENT_NODE):
                continue
            # Look for our xml hierachy named PARENT_NODE
            if (TopLevelNode.nodeName == PARENT_NODE):
                # Check for mandatory attribute name
                if TopLevelNode.hasAttribute("name"):
                    self.HSM.Name = TopLevelNode.getAttribute("name")
                    if self.HSM.Name == "":
                        # No name given return error
                        self.HandleError("No HSM name given", True)
                        return None
                else:
                    self.HandleError("No HSM name given", True)
                    return None
                
                if TopLevelNode.hasAttribute("path"):
                    if TopLevelNode.getAttribute("path") == "":
                        self.HSM.Path = None
                        self.HandleError("No target path in given - CWD assumed.", False) 
                    else:
                        self.HSM.Path = TopLevelNode.getAttribute("path")
                else:
                    self.HSM.Path = None
                    self.HandleError("No target path in given - CWD assumed.", False) 
                
                # Look if we got child states
                self.DigForGold(TopLevelNode)
            else:
                self.HandleError("HSM name must be hsm_service", True)       
                           
        if(self.Debug is True):
            self.DebugOutput()


    def SetXMLInvalid(self):
        """ Each XML parsed can be set invalid by adding a ! previous to
            the state/HSM name. Hence, if s/o adds a new state to the xml
            the existing states will not be re-created """
        # Loop through XML hierachy
        if self.HSM.ErrorFlag is True:
            self.HandleError("We can not set XML invalid as we did not correctly finish parsing before", True)
            return
            
        for TopLevelNode in self.XMLTree.childNodes:
            # Remember: any comment is a node as well
            if (TopLevelNode.nodeType == COMMENT_NODE):
                continue
            # Look for our xml hierachy named PARENT_NODE
            if (TopLevelNode.nodeName == PARENT_NODE):
                # Set service name invalid as well
                self.SetNodeInvalid(TopLevelNode)
                # Pass this state node and search recursively for sub states
                self.LookForStateNodes(TopLevelNode)
            if(self.Debug is True):
                print self.XMLTree.toxml()
            # We are done - write xml to file
            myfile = open(self.XMLPath, "w")
            myfile.write(self.XMLTree.toxml())
            myfile.close


    def LookForStateNodes(self, Node):
        """ Look for sub states in the given node and set each state invalid.
            Perfrom recursive call to go through hierachy. """
        for StateNode in Node.childNodes:
            # Look for desired state nodes within given ParentNode
            if (StateNode.nodeName == STATE_NODE):
                # Set it invalid
                self.SetNodeInvalid(StateNode)
                # Recursive call
                self.LookForStateNodes(StateNode) 
         
                
    def SetNodeInvalid(self, Node):
        """ Attach a ! to each state that has not yet been set invalid """
        name = Node.getAttribute("name")
        # Look for ! char
        if (name.find("!") == -1):
            Node.setAttribute("name", "!" + name)
        
        
    def DebugOutput(self):
        """ Output for debug purposes """
        depth = self.HSM.GetMaxNestingDepth()
        for x in range(0,depth):
            for i in self.HSM.StateLevelList[x]:
                for key, value in dict.items(i.Dict):
                    # let's format the output a little bit
                    print '{:} {:12} {:>3} {:<15} '.format("-".rjust(i.Dict['NestLevel'] * 2), key,":", value)
    
    
    def HandleError(self, ErrorString, ErrorFlag = False):
        """ Handle hard and soft errors """
        # Errors
        if ErrorFlag is True:
            print "XML ERROR: " + ErrorString + "\nXML parsing aborted"
            self.HSM.ErrorFlag = True
        #Warnings
        else:
            print "XML WARNING: " + ErrorString + "\nXML parsing continues"
            self.HSM.ErrorFlag = False
                              
if __name__ == "__main__":
    if len(sys.argv) > 1:
        x = ParseXML(sys.argv[1])
    else:
        print "no path given"
