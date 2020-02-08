#pragma once

#include <string>
#include <vector>
#include <iostream>
#include <iomanip>
#include <sstream>
#include <cctype>
#include <algorithm>


class Conversion
{
public:

   //////////////////////////////////////////////////////////////////
   /** \brief Does an in place conversion to upper case
     */
   inline static std::string& toupper(std::string & aString)
   {
      std::string::iterator lIterator;
      for(lIterator = aString.begin(); lIterator!=aString.end();lIterator++)
         *lIterator = (char) std::toupper(*lIterator);
      return aString;
   };


   //////////////////////////////////////////////////////////////////
   /** \brief Does an in place conversion to lower case
     */
   inline static std::string& tolower(std::string& aString)
   {
      std::string::iterator lIterator;
      for(lIterator = aString.begin(); lIterator!=aString.end();lIterator++)
        *lIterator = (char) std::tolower(*lIterator);
      return aString;
   };

   //////////////////////////////////////////////////////////////////
   /** \brief Converts a binary value into a string of 1's and 0's.
     */
   inline static std::string& decimalToBinary( std::string& aString, unsigned int aNumber )
   {
      unsigned int lRemainder;
      if ( aNumber <= 1 )
      {
         if ( aNumber == 0 )
            aString = aString + '0';
         else
            aString = aString + '1';
         return aString;
      }

      lRemainder = aNumber % 2;
      decimalToBinary( aString, aNumber >> 1 );

      if ( lRemainder == 0 )
         aString = aString + '0';
      else
         aString = aString + '1';
      return aString;
   };

}; //end class Conversions


