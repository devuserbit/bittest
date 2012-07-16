
/*_____________________________________________________________________________________

    \file     Template.Errors.h

    \brief    TODO

    Copyright (c) 2012  Source Scientific, LLC. All rights reserved

    $LastChangedDate:  $
    $Rev:  $
    $URL:  $
______________________________________________________________________________________*/

// 
//    This file is included inside enumeration definition, and to create an error name table
//    inside class definition in the .h of your class
//    #include enumdefs.h
//    enum
//    {
//        #include "Template.Errors.h"
//    };
// 
//   and in the .cc create a table errors and their enums
// 
//   #include enumstrdefs.h - MUST BE AFTER INCLUDE OF CLASS HEADER
//   const static ENUM_STRING Errors[] = 
//   {
//      #include "Template.Errors.h"
//   };

ENUM_SET(UNEXPECTED_ERROR,ERROR_BASE_DEVICE)    // 400 - occurs when .. TODO
ENUMTERM
