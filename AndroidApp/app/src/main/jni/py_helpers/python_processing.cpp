#include "python_processing.hpp"
#include <string>
#include "util.hpp"

// Examples from http://ubuntuforums.org/archive/index.php/t-1266059.html

namespace py_helper
{

   PythonProcessing::PythonProcessing(void)
   {
      mPythonModule = nullptr;

      __android_log_write(ANDROID_LOG_VERBOSE, __FUNCTION__, "PythonProcessing Initialized");
   }

   PythonProcessing::~PythonProcessing(void)
   {
      __android_log_write(ANDROID_LOG_DEBUG, __FUNCTION__, "We are unloading our PythonProcessing Object");
      // This closes the connection to the Python file
      unloadFile();
   }


   int PythonProcessing::checkModule()
   {
      int lReturn(0);

      if (nullptr == mPythonModule)
      {
         __android_log_write(ANDROID_LOG_ERROR, __FUNCTION__, "Python Module was not imported. Unable to process any python functions.");
         lReturn = -1;
      }

      return lReturn;
   }

   int PythonProcessing::loadFile(std::string& aFileName)
   {
      if (nullptr != mPythonModule)
      {
         __android_log_write(ANDROID_LOG_WARN, __FUNCTION__, "Python module has already been loaded, no need to load again.");
         return 0;
      }

      int lReturn = verifyPythonPath(aFileName);

      // Did we have an error during the verify?
      if (lReturn != 0)
      {
         return lReturn;
      }

      // A place holder for the file we are going to call.  We need to strip
      // out any directory info and any file suffix
      std::string lRawFileName;

      // Look to see if our Filename has a Slash.  If it does, I assume the
      // FileName is really a full path with the file name
      std::size_t lFilePos = aFileName.find_last_of(cDirectorySlash);
      if (lFilePos != std::string::npos)
      {
         //we now have the position of the \ just before the name of the exe
         std::string lTempPath = mPythonPath + cPythonPathSeperator + aFileName.substr(0, lFilePos);
         std::wstring lWideString(lTempPath.begin(), lTempPath.end());

         // We cared about the directory for 2 reasons.  1) Python only wants the file name,
         // 2) We need to add this path to the Python Path for it to be findable by Python.
         // Add the path to our file to the python path
         PySys_SetPath(lWideString.c_str());

         // Save off just the file name (we will worry about a suffix below)
         lRawFileName = aFileName.substr(lFilePos + 1, aFileName.length());
      }
         // No slash, just the file.  Perfect
      else
      {
         lRawFileName = aFileName;
      }

      // Ok, we parsed off any path info, now we need to remove any file
      // suffix if it exists.
      std::size_t lSuffixPos = lRawFileName.find(".");

      // Did we find a suffix
      if (lSuffixPos != std::string::npos)
      {
         // Found it, destroy it!
         lRawFileName = lRawFileName.substr(0, lSuffixPos);
      }

      // So after a few checks, we should have just the file name, nothing else
      mPythonModule = PyImport_ImportModule(lRawFileName.c_str());

      if (PyErr_Occurred())
      {
         handlePythonError();
         return -5;
      }
      else if (nullptr == mPythonModule)
      {
         return -6;
      }

      __android_log_write(ANDROID_LOG_VERBOSE, __FUNCTION__, "PythonProcessing::loadFile Exit");
      // return response from Python - return lPythonValue string
      return 0;
   }

   int PythonProcessing::verifyPythonPath(const std::string &aFileName)
   {
      // No path, we can't do anything at all, fail
      if (mPythonPath.empty())
      {
         __android_log_print(ANDROID_LOG_ERROR, __FUNCTION__, "Unable to initialize Python. Error=Python Path is not defined");
         return -2;
      }
         // If we were not passed a file name, we can't load anything
      else if (aFileName.empty())
      {
         __android_log_print(ANDROID_LOG_ERROR, __FUNCTION__, "Python script file was not passed. Python cannot be initialized.");
         return -3;
      }

      // If we can't find the python script files, we can't do anything.  Make sure we can and keep
      // track of when we found it with this
      bool lFoundPython(false);

      // Try to verify that we have the Python stuff in our path.  If we don't Python
      // will abort the app.
      if (mPythonPath.find(cDirectorySlash) != std::string::npos)
      {
         // For code simplicity, we have a vector of strings, which is the list of paths we
         // need to check for existence.
         std::vector <std::string> lPathArray;

         // Ok, we have a directory.  Now check to see if we have to split
         if (mPythonPath.find(cPythonPathSeperator) != std::string::npos)
         {
            // We have multiple to check.  Great
            Utilities::split_trim(mPythonPath, cPythonPathSeperator, lPathArray);
         }
            // We only have one, put it in the list
         else
         {
            lPathArray.push_back(mPythonPath);
         }

         std::string lFileToFind(
               "filecmp.py");         // Just a random file I picked out of the Python scripts
         std::string lFullPath;

         // Iterate through the vector and just try to find 1 of them that
         // has our file to find
         for (auto &lPath:lPathArray)
         {
            // Check to see if the path already has the directory slash
            if (lPath.find_last_of(cDirectorySlash) != (lPath.size() - 1))
            {
               // No slash, add it and the file
               lFullPath = lPath + cDirectorySlash + lFileToFind;
            }
            else
            {
               // Just add the file, we have the slash
               lFullPath = lPath + lFileToFind;
            }

            // Finally, does this file exist?
            if (Utilities::fileExists(lFullPath))
            {
               lFoundPython = true;
               break;               // Good job, we found it, should be good to go.
            } // Directory Exists
         } // Loop through path items
      }  // Directory Slash find

      // If we never found the python file, chances are Python will fail to initialize and abort
      if (!lFoundPython)
      {
         __android_log_print(ANDROID_LOG_ERROR, __FUNCTION__, "Unable to find Python distributed core scripts. Python cannot be initialized.");
         return -8;
      }

      // We get this far, we are good to go
      return 0;
   }

   int PythonProcessing::unloadFile(void)
   {
      if (mPythonModule != nullptr)
      {
         Py_CLEAR(mPythonModule);
      }

      //Py_Finalize();

      return 0;
   }

   long PythonProcessing::executeFunction(const std::string &aFunctionName)
   {
      long lReturn(0);

      // Verify we were able to create the module
      lReturn = checkModule();
      if (lReturn != 0)
      {
         return lReturn;
      }

      if (!aFunctionName.empty())
      {
         // Create the PyObject
         AutoPyObject lFunction(PyObject_GetAttrString(mPythonModule, aFunctionName.c_str()));

         if (PyErr_Occurred())
         {
            __android_log_write(ANDROID_LOG_ERROR, __FUNCTION__, "Error returned creating PyObject for function");
            handlePythonError();
            return -1;
         }
         else if (lFunction.mPyObject == nullptr)
         {

            __android_log_print(ANDROID_LOG_ERROR, __FUNCTION__, "Unable to load python function.");
            return -2;
         }

         // Empty object, just needed for the call
         AutoPyObject lEmptyObject;

         lReturn = executeFunction(lFunction.mPyObject, lEmptyObject.mPyObject);
      }

      return lReturn;
   }
// Pass aMessage.m_MessageBase.mField as aParameters
    long PythonProcessing::executeFunction(const std::string &aFunctionName,
                                           AutoPyDict::Dict_Map &aParameters)
   {
      long lReturn(0);

      // Verify we were able to create the module
      lReturn = checkModule();

      if (lReturn != 0)
      {
         return lReturn;
      }

      if (!aFunctionName.empty())
      {
         // Create the PyObject
         AutoPyObject lFunction(PyObject_GetAttrString(mPythonModule, aFunctionName.c_str()));

         if (PyErr_Occurred())
         {
            __android_log_print(ANDROID_LOG_ERROR, __FUNCTION__, "Error returned while building the python function object");
            return handlePythonError();
         }
         else if (lFunction.mPyObject == nullptr)
         {
            return -1;
         }

         // Create the PyDict
         AutoPyDict lArray;
         lArray.populateDict(aParameters);

         lReturn = executeFunction(lFunction.mPyObject, lArray.mPyDict);

         // If we have a positive return, update our map with values from the call
         if (lReturn > 0)
         {
            getMapFromPyObject(lArray.mPyDict, aParameters);
         }
      }

      return lReturn;
   }

   long PythonProcessing::executeFunction(PyObject * aFunction, PyObject * aParameters)
   {
      long lReturn(0);

      // Verify we were able to create the module
      lReturn = checkModule();

      if (lReturn != 0)
      {
         return lReturn;
      }

      else if (aFunction == nullptr)
      {
         // Somehow we got here with no Module. Bail
         __android_log_print(ANDROID_LOG_ERROR, __FUNCTION__, "Unable to call python executeFunction. An invalid function was passed.");
         return -1;
      }

      std::string lFunctionText;
      lReturn = getStringFromPyObject(aFunction, lFunctionText);

      AutoPyObject lPythonReturnValue;

      if (mPythonModule == nullptr)
      {
         // Somehow we got here with no Module. Bail
         return -2;
      }

      // if aParameters is null, we have no parameters
      if (aParameters == nullptr)
      {
         lPythonReturnValue.mPyObject = PyObject_CallObject(aFunction, nullptr);
      }
      else
      {
         lPythonReturnValue.mPyObject = PyObject_CallFunctionObjArgs(aFunction, aParameters,
                                                                     nullptr);
      }

      if (PyErr_Occurred())
      {
         return handlePythonError();
      }

      // We should have a return code, and it should be a Long
      if (PyLong_Check(lPythonReturnValue.mPyObject))
      {
         lReturn = PyLong_AsLong(lPythonReturnValue.mPyObject);

         if (PyErr_Occurred())
         {
            __android_log_print(ANDROID_LOG_ERROR, __FUNCTION__, "Error returned while calling getting return value for call");
            return handlePythonError();
         }
      }

      // return response from Python - return lPythonValue string
      return lReturn;
   }

   int PythonProcessing::handlePythonError()
   {
      // Tried to implement https://github.com/Kozea/Multicorn/blob/master/src/errors.c

      int lReturn(0);

      AutoPyObject lType, lValue, lTraceback;
      PyErr_Fetch(&lType.mPyObject, &lValue.mPyObject, &lTraceback.mPyObject);
      //pvalue contains error message
      //ptraceback contains stack snapshot and many other information
      //(see python traceback structure)

      //Get error message
      std::string lErrorMessage;
      lReturn = getStringFromPyObject(lValue.mPyObject, lErrorMessage);

      // Only log the Name and Value.  The traceback will be a more detailed debug message
      std::string lMessage("Python Error.  Error= " + lErrorMessage);
      __android_log_write(ANDROID_LOG_ERROR, __FUNCTION__, lMessage.c_str());

      // Clear our error
      PyErr_Clear();

      return lReturn;
   }

   int PythonProcessing::getStringFromPyObject(PyObject * aPyObject, std::string & aReturnString)
   {
      if (aPyObject == nullptr)
      {
         __android_log_write(ANDROID_LOG_ERROR, __FUNCTION__, "Unable to get the string from a null object.");
         return -101;
      }

      if (PyUnicode_Check(aPyObject))
      {
         AutoPyObject lAscii(PyUnicode_AsASCIIString(aPyObject));
         aReturnString = PyBytes_AsString(lAscii.mPyObject);
      }
      else
      {
         AutoPyObject lRep(PyObject_Repr(aPyObject));
         AutoPyObject lAscii(PyUnicode_AsASCIIString(lRep.mPyObject));
         aReturnString = PyBytes_AsString(lAscii.mPyObject);
      }

      if (PyErr_Occurred())
      {
         __android_log_write(ANDROID_LOG_ERROR, __FUNCTION__, "Error returned getting string from object");
         handlePythonError();
         return -110;
      }
      return 0;
   }
   int PythonProcessing::getVectorFromPyObject(PyObject * aPyObject,
                                               AutoPyList::List_Array & aItems)
   {
      int lReturn(0);

      if (aPyObject == nullptr)
      {
         __android_log_print(ANDROID_LOG_ERROR, __FUNCTION__, "Unable to get the vector from a null dictionary object.");
         return -101;
      }
         // Verify that it's a Tuple
      else if (!PyList_Check(aPyObject))
      {
         __android_log_print(ANDROID_LOG_ERROR, __FUNCTION__, "Python object is not a Dictionary, and can not be converted to a vector.");
         return -102;
      }

      // We know we have a list, lets get the values out of it
      Py_ssize_t lListSize = PyList_Size(aPyObject);

      if (PyErr_Occurred())
      {
         __android_log_print(ANDROID_LOG_ERROR, __FUNCTION__, "Error returned while calling PyList_Size");
         handlePythonError();
         return -103;
      }
      else if (lListSize > 0)
      {
         aItems.clear();
      }

      std::string lValue;

      for (Py_ssize_t lLoop = 0; lLoop < lListSize; ++lLoop)
      {
         AutoPyObject lTempItem(PyList_GetItem(aPyObject, lLoop), false);

         if (PyErr_Occurred())
         {
            __android_log_print(ANDROID_LOG_ERROR, __FUNCTION__, "Error returned while calling PyList_GetItem");
            handlePythonError();
            return -105;
         }

         lReturn = getStringFromPyObject(lTempItem.mPyObject, lValue);

         if (lReturn != 0)
         {
            __android_log_print(ANDROID_LOG_WARN, __FUNCTION__, "Error getting string from py object.");
         }

         aItems.push_back(lValue);
      }

      return lReturn;
   }

   int PythonProcessing::setPyPath(const std::string &aPythonPath)
   {
      __android_log_print(ANDROID_LOG_INFO, __FUNCTION__, "Setting common Python path");

      mPythonPath = aPythonPath;
      return 0;
   }

   int PythonProcessing::getMapFromPyObject(PyObject * aPyObject, AutoPyDict::Dict_Map & aItems)
   {
      int lReturn(0);

      if (aPyObject == nullptr)
      {
         __android_log_print(ANDROID_LOG_ERROR, __FUNCTION__, "Unable to get the vector from a null dictionary object.");
         return -101;
      }
         // Verify that it's a Tuple
      else if (!PyDict_Check(aPyObject))
      {
         __android_log_print(ANDROID_LOG_ERROR, __FUNCTION__, "Python object is not a Dictionary, and can not be converted to a vector.");
         return -102;
      }

      AutoPyObject lDictKey(
            false);          // These should not be cleaned up, PyDict_Next gives us a borrowed reference
      AutoPyObject lDictValue(
            false);        // These should not be cleaned up, PyDict_Next gives us a borrowed reference
      Py_ssize_t lPosition = 0;

      std::string lKeyName;
      std::string lValue;

      while (PyDict_Next(aPyObject, &lPosition, &lDictKey.mPyObject, &lDictValue.mPyObject))
      {
         lReturn = getStringFromPyObject(lDictKey.mPyObject, lKeyName);

         if (lReturn != 0)
         {
            __android_log_print(ANDROID_LOG_WARN, __FUNCTION__, "Error getting string from python object");
            // With no Key name, we really can't put anything in
            continue;
         }

         lReturn = getStringFromPyObject(lDictValue.mPyObject, lValue);

         if (lReturn != 0)
         {
            // We should have already logged something, and we don't return or continue so that we atleast put
            // an empty string in the Map
            __android_log_print(ANDROID_LOG_WARN, __FUNCTION__, "Error getting string from python object");
         }

         aItems[lKeyName] = lValue;
      }
      return lReturn;
   }
} // end of namespace