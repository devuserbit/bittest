
/*_____________________________________________________________________________________

    \file     CHSMTemplateService.cc

    \brief    TODO

    Copyright (c) 2012  Source Scientific, LLC. All rights reserved

    $LastChangedDate:  $
    $Rev:  $
    $URL:  $
______________________________________________________________________________________*/

#include "CHSMTemplateService.h"


/////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////  Declare Functions and IOCTLs supported  ///////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////

// Declare functions available
const SERVICE_FUNCTIONS CHSMTemplateService::ServiceFunctions[] = 
{
    MSG_GET_ERROR_NAME,
    MSG_ABORT,
    MSG_RESET,
    MSG_GET_STATE, 
    MSG_GET_PARAMS, 
    MSG_SET_PARAMS,
    0
};

// Declare IOCTLS supported
const IOCTL_FUNCTIONS CHSMTemplateService::IOCTLFunctions[] =
{
    {CHSMTemplateService::PREPARE,            0,  0,  "Prepare",                ""},
    {CHSMTemplateService::DO_ACTIVITY,        0,  0,  "Do Some Activity ",      ""},
    IOCTL_FUNCTIONS_TERMINATE
};

// Size info for functions
const SERVICE_SIZE_INFO CHSMTemplateService::SizeInfo =
{
    sizeof(CTemplateParameters), sizeof(INT32U),    // Param size,Param Item size,
                              0,              0,    // Stats Size, Stats Item Size
                              0,              0,    // Max Data, Max Data Item,
                                              0};   // Max Control Response size. Needed if this object is ever remote

// Create a table of error values and names
#include "enumstrdefs.h"
const ENUM_STRING CHSMTemplateService::Errors[] = 
{
    #include "Template.Errors.h"
};


/////////////////////////////////////////////////////////////////////////////////
/////////////////////////////  ERROR TRANSLATION TABLE //////////////////////////
/////////////////////////////////////////////////////////////////////////////////
// Notice we do a catch-all of "Unable to home" on any other error except crash
// This is called from the function: 
//
//          OutputErrorCode = CHSMService::MapResponseCode(INT16U InputErrorCode,INT16U InputInfo1, INT16U InputInfo2)
//
// Input Error and Info of the function must match the table entries for the output 
// code of the table to be output. 
// INFO_DONT_CARE (0xffff) is reserved to signal not to require a match on that field.
// 
const HSM_SERVICE_ERROR_STRUCT CHSMTemplateService::ErrorMap[] = 
{
    // Output Error Code                Input Error Code        Input Info 1          InputInfo 2
    { CHSMTemplateService::UNEXPECTED_ERROR,        INFO_DONT_CARE        , INFO_DONT_CARE       ,INFO_DONT_CARE}, // any other error
    ERROR_STRUCT_TERMINATOR 
};


////////////////////////////////////////////////////////////////////////////////
/*!   \fn  CHSMTemplateService::CHSMTemplateService()

      \brief Set initial vars in construction of object for transport type of service

      \param nSrvNo - TODO
      \param pServiceName - TODO
      \param pTask - TODO
      \param pControlledObj - TODO

      \return n/a
*/
////////////////////////////////////////////////////////////////////////////////
CHSMTemplateService::CHSMTemplateService(INT16U     nSrvNo,
                                         const char *pServiceName,
                                         CTask      *pTask,
                                         CService   *pControlledObj)
                                         : CHSMService(nSrvNo,
                                                       pServiceName,
                                                       pTask,
                                                       NULL,
                                                       ErrorMap),
                                         // #^ CTOR_STATES
                                         RootState(this),
                                         ResetState(this),
                                         ReadyState(this),
                                         BusyState(this),
                                         ActivityState(this),
                                         // ^#
                                         m_pControlledObj(pControlledObj)
{
    // Setup the service information - INCLUDE errors pointer
    SET_SERVICE_INFO_EXT(ServiceFunctions, IOCTLFunctions, &SizeInfo, &m_Parameters, NULL, Errors);
}

////////////////////////////////////////////////////////////////////////////////
/*!   \fn  CHSMTemplateService::InitStates()

      \brief Initialize the states

      \param n/a

      \return SYSSTATUS
*/
////////////////////////////////////////////////////////////////////////////////
SYSSTATUS CHSMTemplateService::InitStates()
{
    //
    // We will initialize all our states
    // Send the HSM this state belongs, its parent state, and its enumerated state number
    //
    // #^ INIT_STATES
    SYSSTATUS16     nStatus = RootState.Init(&PrimaryHSM, NULL, ROOT_STATE);
    ASSERT_RETURN_BAD_STATUS(nStatus);

    nStatus = ResetState.Init(&PrimaryHSM, &RootState, RESET_STATE);
    ASSERT_RETURN_BAD_STATUS(nStatus);

    nStatus = ReadyState.Init(&PrimaryHSM, &RootState, READY_STATE);
    ASSERT_RETURN_BAD_STATUS(nStatus);

    nStatus = BusyState.Init(&PrimaryHSM, &RootState, BUSY_STATE);
    ASSERT_RETURN_BAD_STATUS(nStatus);

    nStatus = ActivityState.Init(&PrimaryHSM, &BusyState, ACTIVITY_STATE);
    ASSERT_RETURN_BAD_STATUS(nStatus);

    // ^#

    // Set initial state of the  main HSM
    // #^ INITIAL_STATE
    nStatus = PrimaryHSM.SetInitialState(this,&ResetState);
    ASSERT_RETURN_BAD_STATUS(nStatus);
    // ^#

    return nStatus;
}
