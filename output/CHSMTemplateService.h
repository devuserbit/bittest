
/*_____________________________________________________________________________________

    \file     CHSMTemplateService.h

    \brief    TODO

    Copyright (c) 2012  Source Scientific, LLC. All rights reserved

    $LastChangedDate:  $
    $Rev:  $
    $URL:  $
______________________________________________________________________________________*/


#ifndef _CHSM_TEMPLATE_SERVICE_H
#define _CHSM_TEMPLATE_SERVICE_H

// Include base class service
#include "CHSMService.h"

// Include state headers
// #^ HEADERS
#include "Template.CRootState.h"
#include "Template.CResetState.h"
#include "Template.CReadyState.h"
#include "Template.CBusyState.h"
#include "Template.CActivityState.h"
// ^#


////////////////////////////////////////////////////////////////////////////////
/*!   \fn  CHSMTemplateService

      \brief TODO

      \author Andrei.Popescu
*/
////////////////////////////////////////////////////////////////////////////////
class CHSMTemplateService : public CHSMService
{
public:
    ////////////////////////////////////////////////////////////////////////////////
    /*!   \fn  CTemplateParameters

          \brief TODO

          \author Andrei.Popescu
    */
    ////////////////////////////////////////////////////////////////////////////////
    struct CTemplateParameters:
    {
        INT32U  m_nParameter1;
        INT32U  m_nParameter2;

        //c-tor
        CTemplateParameters(INT32U param1 = 0,
                            INT32U param2 = 0): m_nParameter1(param1),
                                                m_nParameter2(param2)
    
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
        #include "Template.Errors.h"
    };
    
    // Constructor Service.  Place in transport stack is optional
    // By default all services will be place in the service list, for access via PC
    // Any service not wishing to be visible, should use HIDDEN_SERVICE for nSrvNo
    CHSMTemplateService(INT16U      nSrvNo,                 // Service Number for external control
                        const char  *pServiceName,          // Service Name
                        CTask       *pTask,                 // Task for service to run functions
                        CService    *pControlledObj);       // Object this state machine controlls

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
        // #^ ENUMS
        ROOT_STATE,                       // 0 - TODO: Decription
        RESET_STATE,                      // 1 - TODO: Decription
        READY_STATE,                      // 2 - TODO: Decription
        BUSY_STATE,                       // 3 - TODO: Decription
        ACTIVITY_STATE,                   // 4 - TODO: Decription
        // ^#
        LAST_STATE
    } STATE_NUMBERS;
    
    
    ///////////////////////////////////////////////////////////////////
    //////////////////////// CREATE THE STATES //////////////////////// 
    ///////////////////////////////////////////////////////////////////
    
    
    // Friend class declaration
    // make sure our states are friends so they can access this class
    // Compiler requires the namespace - "using" does not help
    // #^ FRIENDS
    friend class    nsTemplateService::CRootState;
    friend class    nsTemplateService::CResetState;
    friend class    nsTemplateService::CReadyState;
    friend class    nsTemplateService::CBusyState;
    friend class    nsTemplateService::CActivityState;
    // ^#
    
    
    // Define states
    // #^ DEFINES
    nsTemplateService::CRootState                   RootState;
    nsTemplateService::CResetState                  ResetState;
    nsTemplateService::CReadyState                  ReadyState;
    nsTemplateService::CBusyState                   BusyState;
    nsTemplateService::CActivityState               ActivityState;
    // ^#
    
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
    CTemplateParameters m_Parameters;       

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
