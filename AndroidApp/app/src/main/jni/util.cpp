

#include "util.hpp"
#include "Python.h"

const char *cDirectorySlash = "/";
const char *cPythonPathSeperator = ":";


const std::wstring Utilities::getWStringFromJava(JNIEnv *env, jstring aString)
{
   // For now I'm saying we only really support UTF8. When we need to support more,
   // well, that is when we spend more time on it.
   std::string lString = getStringFromJava(env, aString);

   // Convert our string to a wide string
   std::wstring lOutput(lString.begin(), lString.end());

   return lOutput;
}
