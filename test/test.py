import os,sys
os.chdir("../")
sys.path.append(os.getcwd())

from modules import XML2Class

#Start parse process
XMLReference = XML2Class.ParseXML("default_hsm.xml")

# For now HSM Struct is a sub class of XML2Class - this will be changed
HSMStruct = XMLReference.GetHSMStruct()

# HSMStruct has a 2D list - let's loop through it
for StateList in HSMStruct.StateLevelList:
    for State in StateList:
        str = State.Name
        if State.Parent is not None:
            str += " has Parent " + State.Parent.Name
        print str
        delimiter = "---"
        print ' {} Callbacks: {} \n {} Functions: {} '.format(delimiter, State.Callbacks, delimiter, State.Functions)
        print ' {} Initial: {} \n {} Dynamic: {} \n'.format(delimiter, State.Initial, delimiter, State.Dynamic)


        
RootState = HSMStruct.GetRootElement()

def ShowChildren(State):
    # Show Root
    if State.Parent is None:
        print State.Name
    if State.HasChildren():
        for SubState in State.GetChildren():
            print '{}{}'.format("-".rjust(SubState.Depth*2) , SubState.Name)
            ShowChildren(SubState)

ShowChildren(RootState)


XMLReference.SetXMLInvalid()
