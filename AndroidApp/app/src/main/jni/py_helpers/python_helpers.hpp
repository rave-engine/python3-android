#pragma once

#include <vector>
#include <map>
#include <Python.h>
#include <util.hpp>

namespace py_helper
{
   /////////////////////////////////////////////////////////////////////
   /** 
      * \brief The AutoPyObject is a wrapper around PyObject that can be used 
      * to lessen the need to worry about the Python objects and when to clean
      * then up.
      *   
      *  The class uses the HandleClear bool to determine if the class
      *  will dereference the object when it goes out of scope.  It is assumed
      *  that an object is passed in.
      *
      */
   class AutoPyObject
   {
   public:

   /////////////////////////////////////////////////////////////////////
   /** 
      * \brief The base constructor that has an overloaded boolean to 
      * determine if the object is cleaned up in the destructor
      * then up.
      *   
      *  The class uses the HandleClear bool to determine if the class
      *  will de-reference the object when it goes out of scope.  It is assumed
      *  that an object is passed in.
      *
      */
      AutoPyObject(bool aDecrementReference = true);
      ~AutoPyObject();

      bool mDecrementReference;

      AutoPyObject(PyObject* aPyObject, bool aDecrementReference = true);

      AutoPyObject& operator=(PyObject* aObject);

      PyObject* mPyObject;
   };

   /////////////////////////////////////////////////////////////////////
   /** 
      * \brief The AutoPyList is a wrapper around PyList that can be used 
      * to lessen the need to worry about the Python objects and when to clean
      * then up.
      *   
      *  The class will take a Vector of strings and build a Python list
      *  from them.  It also has a setItem which should be used to help
      *  manage the reference count for the items in the list
      *  that an object is passed in.
      *
      */
   class AutoPyList
   {
   public:
      typedef std::vector<std::string> List_Array;
      typedef List_Array::iterator iList_Array;

      /////////////////////////////////////////////////////////////////////
      /** 
         * \brief The AutoPyList constructor takes the size of the array
         * It will create a list of that size, but the list will be empty
         *
         *  \param int aArraySize - The number of elements expected in the List
         */
      AutoPyList(int aArraySize);

      /////////////////////////////////////////////////////////////////////
      /** 
         * \brief The AutoPyList constructor takes the string vector and
         * builds a List based on these values
         *
         *  \param ListArray& aArray - The vector of elements to add to the list
         */
      AutoPyList(List_Array& aArray);

      ~AutoPyList();

      /////////////////////////////////////////////////////////////////////
      /** 
         * \brief The populateList is used to convert the Vector of strings
         * and build the List
         *
         *  \param ListArray& aArray - The vector of elements to add to the list
         *  \return int
         *  \retval 0 - Key Successfully Read
         *  \retval Non 0 - Errors occurred, Do error checking, may not be safe to continue running the application
         */
      int populateList(List_Array& aArray);

      /////////////////////////////////////////////////////////////////////
      /** 
         * \brief The setItem is used to add an individual Python Item to
         * the list.
         *
         * NOTE: This is going to take care of the reference count for you.  
         * PyList_SetItem will steal the reference, and this method handles
         * this by telling the Python Object that it no longer needs to manage
         * it's own reference.
         *
         *  \param AutoPyObject& aItem - The Python object to add
         *  \return NONE
         */
      void setItem( AutoPyObject& aItem );

      Py_ssize_t mItemCount;

      AutoPyList& operator=(PyObject* aObject);

      ///> The Object that is the Python List
      PyObject* mPyList;

   };

   /////////////////////////////////////////////////////////////////////
   /** 
      * \brief The AutoPyDict is a wrapper around PyDict that can be used 
      * to lessen the need to worry about the Python objects and when to clean
      * then up.
      *   
      *  The class will take a Map of strings with strings as a key and build 
      *  a Python map  from them.
      *
      */
   class AutoPyDict
   {
   public:
       typedef std::map<std::string, std::string, NoCaseFunctionObject> Dict_Map;
      typedef Dict_Map::iterator iDict_Map;

      /////////////////////////////////////////////////////////////////////
      /** 
         * \brief The AutoPyDict constructor takes no parameters and simply
         * creates an empty dictionary object.
         *
         */
      AutoPyDict();

      /////////////////////////////////////////////////////////////////////
      /** 
         * \brief The AutoPyDict constructor takes a Map of strings with
         * strings as keys.  It will then populate the dictionary with these
         * values.
         *
         *
         *  \param Dict_Map& aArray - The Map to build the Dictionary with
         *  \return NONE
         */
      AutoPyDict(Dict_Map& aArray);

      /////////////////////////////////////////////////////////////////////
      /** 
         * \brief The populateDict method takes a Map of strings with
         * strings as keys.  It will then populate the dictionary with these
         * values.
         *
         *
         *  \param Dict_Map& aArray - The Map to build the Dictionary with
         *  \return int
         *  \retval 0 - Success
         *  \retval Non 0 - Errors occurred, Do error checking.
         */
      int populateDict(Dict_Map& aArray);

      ~AutoPyDict();

      AutoPyDict& operator=(PyObject* aObject);
      PyObject* mPyDict;
   };
} // end namespace
