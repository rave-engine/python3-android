#pragma once

#include "python_helpers.hpp"

#include <Python.h>

namespace py_helper
{
class PythonProcessing
{

public:
   PythonProcessing(void);
   virtual ~PythonProcessing(void);

   /////////////////////////////////////////////////////////////////////
   /** 
      * \brief loadFile is used to load the file into a Python object for later
      * use. 
      *
      * NOTE: Do not put the file suffix.  So 'Script.py' should just be passed 
      * as 'Script'
      *
      *  \param std::string& aFileName - The name of the file to load
      *  \return int
      *  \retval 0 - Function processed successfully
      *  \retval Non 0 - Errors occurred, Do error checking.
      */
   int loadFile(std::string& aFileName);

   /////////////////////////////////////////////////////////////////////
   /** 
      * \brief unloadFile is used to unload the python file for shutdown or
      * to be able to use a different file
      *
      *  \return int
      *  \retval 0 - Function processed successfully
      *  \retval Non 0 - Errors occurred, Do error checking.
      */
   int unloadFile(void);

   /////////////////////////////////////////////////////////////////////
   /** 
      * \brief handlePythonError is the method to call when a Python error
      * occurs.  It will log the message returned from python, and clear
      * the error
      *
      *  \return int
      *  \retval 0 - Function processed successfully
      *  \retval Non 0 - Errors occurred, Do error checking.
      */
   int handlePythonError();

   /////////////////////////////////////////////////////////////////////
   /**
      * \brief executeFunction Is the base method to execute a python function
      * this instance simply takes the string which is the name of the function
      * and calls that function, returning the return value of the function
      *
      *  \param std::string& aFunctionName - The name of the function to call
      *  \return long
      *  \retval 0 - Function processed successfully
      *  \retval Non 0 - Errors occurred, Do error checking.
      */
   long executeFunction( const std::string& aFunctionName);

   /////////////////////////////////////////////////////////////////////
   /** 
      * \brief executeFunction is used to call a python function passing a map
      * by reference so that the values of the map may be updated.
      *
      *  \param std::string& aFunctionName - The name of the function to call
      *  \param AutoPyDict::Dict_map& aParameters - The Map of parameters to process with
      *  \return long
      *  \retval 0 - Function processed successfully
      *  \retval Non 0 - Errors occurred, Do error checking.
      */
   long executeFunction( const std::string& aFunctionName, AutoPyDict::Dict_Map& aParameters );

   /////////////////////////////////////////////////////////////////////
   /** 
      * \brief checkModule will verify that the file has been loaded.
      * map
      *
      *  \param NONE
      *  \return int
      *  \retval 0 - Module is initialized
      *  \retval Non 0 - Module is not initialized, abort
      */
   int checkModule();

   /////////////////////////////////////////////////////////////////////
   /**
      * \brief verifyPythonPath will *TRY* to make sure that Python has
      * everything it needs to run. Python is not forgiving, it has a
      * huge library of scripts it expects, and is also real persnickety
      * about where they need to be.
      *
      *  \param const std::string& aFileName -- The file to load
      *  \return int
      *  \retval 0 - Function processed successfully
      *  \retval Non 0 - Errors occurred, Do error checking.
      */
   int verifyPythonPath(const std::string& aFileName);

   /////////////////////////////////////////////////////////////////////
   /** 
      * \brief executeFunction is used to call a python function with a Python
      * Python object as the parameters.  This is used once you have turned the function
      * and Map/List into Python objects
      *
      *  \param PyObject* aFunction- The Python object that is the function
      *  \param PyObject* aParameters - The map as a Python Object
      *  \return int
      *  \retval 0 - Function processed successfully
      *  \retval Non 0 - Errors occurred, Do error checking.
      */
   long executeFunction( PyObject* aFunction, PyObject* aParameters );

   /////////////////////////////////////////////////////////////////////
   /** 
      * \brief getStringFromPyObject will convert a Python Object into a string
      *
      *  \param PyObject* aObject - The Python object to be converted
      *  \param std::string& aReturnString - The string to be returned
      *  \return int
      *  \retval 0 - Function processed successfully
      *  \retval Non 0 - Errors occurred, Do error checking.
      */
   int getStringFromPyObject(PyObject* aObject, std::string& aReturnString );

   /////////////////////////////////////////////////////////////////////
   /** 
      * \brief getMapFromPyDict will convert a Python Dictionary into a
      * map
      *
      *  \param AutoPyDict& aPyObject - The Python object to be converted
      *  \param AutoPyDict::Dict_Map& - The map to be returned
      *  \return int
      *  \retval 0 - Function processed successfully
      *  \retval Non 0 - Errors occurred, Do error checking.
      */
   int getMapFromPyObject(PyObject* aPyObject, AutoPyDict::Dict_Map& aItems);

   /////////////////////////////////////////////////////////////////////
   /** 
      * \brief getVectorFromPyList will convert a Python Dictionary into a
      * map
      *
      *  \param AutoPyList& aPyObject - The Python object to be converted
      *  \param AutoPyList::List_Array& - The listto be returned
      *  \return int
      *  \retval 0 - Function processed successfully
      *  \retval Non 0 - Errors occurred, Do error checking.
      */
   int getVectorFromPyObject(PyObject* aPyObject, AutoPyList::List_Array& aItems);

   int setPyPath( const std::string& aPythonPath );

private:


   ///> The Python Module is the Python script object
   PyObject* mPythonModule;

   std::string mPythonPath;
};

}