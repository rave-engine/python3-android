#include "python_helpers.hpp"
#include <android/log.h>

namespace py_helper
{
   
   /*
    *
    *   Object
    *
    */
   AutoPyObject::AutoPyObject(bool aDecrementReference)
   {
      mDecrementReference = aDecrementReference;

      mPyObject = nullptr;
   }

   AutoPyObject::AutoPyObject(PyObject* aPyObject, bool aDecrementReference)
   {
      mPyObject = aPyObject;
      mDecrementReference = aDecrementReference;
   }

   AutoPyObject::~AutoPyObject()
   {
      // If we have no object, nothing to do
      if ( mPyObject != nullptr )
      {
         // If this is false, we determined at some point that
         // Python is taking control
         if ( mDecrementReference )
         {
            Py_XDECREF(mPyObject);
         }

         mPyObject = nullptr;
      }
   }

   AutoPyObject& AutoPyObject::operator=(PyObject* aObject)
   {
      if ( mPyObject == nullptr )
      {
         mPyObject = aObject;
      }
      else
      {
         __android_log_print(ANDROID_LOG_WARN, __FUNCTION__, "No Assignment allowed with NULL object");
      }

      return *this;
   }

   /*
    *
    *   LIST
    *
    */
   AutoPyList::AutoPyList(int aArraySize)
   {
      mItemCount = 0;
      // Create a list with x elements
      mPyList = PyList_New(aArraySize);
   }

   // Constructor to fill our PyList with the values from an Array
   AutoPyList::AutoPyList(List_Array& aArray)
   {
      mItemCount = 0;
      // Create a list with x elements
      mPyList = PyList_New(aArray.size());
      // Populate our Data
      populateList(aArray);
   }

   AutoPyList::~AutoPyList()
   {
      if ( mPyList!= nullptr )
      {
         Py_XDECREF(mPyList);
         mPyList = nullptr;
      }
   }

   int AutoPyList::populateList(List_Array& aArray)
   {
      int lResult(0);

      // Loop through and create Array
      for(std::size_t lLoopItem = 0; lLoopItem < aArray.size(); lLoopItem++ )
      {
         AutoPyObject lTempItem(PyUnicode_FromString(aArray[lLoopItem].c_str()));
         setItem(lTempItem);
      }

      return lResult;
   }

   void AutoPyList::setItem( AutoPyObject& aItem )
   {
      aItem.mDecrementReference = false;

      int lResult(0);
      lResult = PyList_SetItem(mPyList, mItemCount, aItem.mPyObject);

      if(lResult != 0)
      {
         PyErr_Print();
         PyErr_Clear();

         __android_log_print(ANDROID_LOG_WARN, __FUNCTION__, "The Python List for parameters passing failed to set for an argument.");
      }

      mItemCount++;
   }

   AutoPyList& AutoPyList::operator=(PyObject* aObject)
   {
      if ( mPyList == nullptr )
      {
         mPyList = aObject;
      }
      else
      {
         __android_log_print(ANDROID_LOG_WARN, __FUNCTION__, "No Assignment allowed with NULL object");
      }

      return *this;
   }

   /*
    *
    *   DICTIONARY
    *
    */
   AutoPyDict::AutoPyDict()
   {
      mPyDict = PyDict_New();
   }

   // Constructor to fill our PyDict with the values from an Array
   AutoPyDict::AutoPyDict(Dict_Map& aArray)
   {
      mPyDict = PyDict_New();
      // Populate our PyObject with the map
      populateDict(aArray);
   }

   AutoPyDict::~AutoPyDict()
   {
      if ( mPyDict != nullptr )
      {
         Py_XDECREF(mPyDict);
         mPyDict = nullptr;
      }
   }

   int AutoPyDict::populateDict(Dict_Map& aMessage)
   {
      int lReturn(0);
      std::string lLogMessage;

      // Loop through the passed message, and put it in the dictionary with the correct fields
      for( iDict_Map lIter = aMessage.begin(); lIter != aMessage.end(); ++lIter )
      {
         AutoPyObject lTempItem(PyUnicode_FromString(lIter->second.c_str()));

         lReturn = PyDict_SetItemString(mPyDict, lIter->first.c_str(), lTempItem.mPyObject);

         if ( lReturn != 0 )
         {
            PyErr_Print();
            PyErr_Clear();

            __android_log_print(ANDROID_LOG_WARN, __FUNCTION__, "Error adding field");
            return -1;
         }
      }

      return lReturn;
   } // End of Dict

   AutoPyDict& AutoPyDict::operator=(PyObject* aObject)
   {
      if ( mPyDict == nullptr )
      {
         mPyDict = aObject;
      }
      else
      {
         __android_log_print(ANDROID_LOG_WARN, __FUNCTION__, "No Assignment allowed with NULL object");
      }

      return *this;
   }

}; // end py_helper namespace
