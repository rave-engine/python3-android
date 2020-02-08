#include "PythonThread.hpp"
#include "util.hpp"

#include "py_helpers/python_processing.hpp"
#include "python/Python.h"
#include "python/pythonrun.h"

#include <android/log.h>
#include <stdio.h>
#include <fcntl.h>
#include <pthread.h>


static std::string mPythonDirectory = "";
static std::string mSetupDirectory = "";
//
static std::string mSetupFunctionName("setupEnvironment");

// This is the object we use to call a specific method in a python file.
// Currently we only support 1 file, and that is android_setup.py
static py_helper::PythonProcessing mPyProcess;

// This flag tells us if we have initialized PyGIL
static bool mPyGIL_Init = false;
PyThreadState* mPyThreadState = nullptr;

long setupEnvironment();
int setupAndroidSetupFile(std::string aPythonPath, std::string aSetupPath);


#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wunused-parameter"
JNIEXPORT jint JNICALL JNI_OnLoad(JavaVM *jvm, void *reserved) {
   __android_log_write(ANDROID_LOG_VERBOSE, __FUNCTION__, "JNI_OnLoad");

   return JNI_VERSION_1_6;
}
#pragma clang diagnostic pop

JNIEXPORT jint JNICALL Java_com_example_pythontest_PythonThread_initPython
      (JNIEnv* env, jobject obj, jstring aPath, jstring aSetupDirectory)
{
   // We need to set this here so that when we restart it keeps running
   mPyGIL_Init = false;

   std::wstring lPassedPath = Utilities::getWStringFromJava(env, aPath);
   mSetupDirectory = Utilities::getStringFromJava(env, aSetupDirectory);

   std::string lDirectory;

   lDirectory = Utilities::convertWChar(lPassedPath);

   if (!Utilities::dirExists(lDirectory))
   {
      // Unable to initialize Python because the path does not exist
      __android_log_write(ANDROID_LOG_ERROR, __FUNCTION__, "Python path does not exist. Make sure you copy it from the assets! ");
      return -1;
   }

   // We need to add this lib-dynload so that we have all our .so libraries available.
   lDirectory += "/lib-dynload";

   // Now make sure the SO directory exists too
   if (!Utilities::dirExists(lDirectory))
   {
      // Unable to initialize Python because the path does not exist
      __android_log_write(ANDROID_LOG_ERROR, __FUNCTION__, "Python lib-dynload path does not exist. Make sure you copy it from the assets!");
      return -1;
   }

   // Based on the string passed in lets setup our Python Path
   std::wstring lPyPath;
   lPyPath = lPassedPath + L"/:" + lPassedPath + L"/lib-dynload";      // This is our path, where Python is, and where the shared libraries are

   // Tell Python our path
   Py_SetPath(lPyPath.c_str());
   __android_log_write(ANDROID_LOG_VERBOSE, __FUNCTION__, "initPython - PyPath");

   // Initialize Python, we only want to do this once!
   Py_Initialize();


   //If we can't init, handle it
   if (!Py_IsInitialized())
   {
      __android_log_write(ANDROID_LOG_WARN, __FUNCTION__, "Python was unable to initialize");
      return -4;
   }

   __android_log_write(ANDROID_LOG_VERBOSE, __FUNCTION__, "initPython - WF Python Engine has been initialized");

   // The Python Directory needs to be a wide char, convert our path
   mPythonDirectory = Utilities::convertWChar(lPyPath);

   // Setup our Python module for Android Setup
   setupAndroidSetupFile(mPythonDirectory, mSetupDirectory);

   // Call the setup initialize stuff for Android Setup
   setupEnvironment();

   __android_log_write(ANDROID_LOG_VERBOSE, __FUNCTION__, "Leaving initPython");
   return 0;
}

JNIEXPORT jint JNICALL Java_com_example_pythontest_PythonThread_cleanupPython
      (JNIEnv* env, jobject obj)
{

   __android_log_write(ANDROID_LOG_VERBOSE, __FUNCTION__, "We are in Cleanup Python");


   mPyProcess.unloadFile();

   //If we can't init, handle it
   if (!Py_IsInitialized())
   {
      __android_log_write(ANDROID_LOG_ERROR, __FUNCTION__, "Python has not been initialized");
      return -4;
   }

   // If we saved off our thread, we need to release it
   if (mPyGIL_Init)
   {
      __android_log_write(ANDROID_LOG_VERBOSE, __FUNCTION__, "We have cleared out GIL flag");
      mPyGIL_Init = false;
      PyEval_RestoreThread(mPyThreadState);  // This needs to be done if we did a PyEval_SaveThread
   }

   // Just call Finalize and be done
   __android_log_write(ANDROID_LOG_INFO, __FUNCTION__, "About to call finalize in Cleanup Python");
   Py_Finalize();

   __android_log_write(ANDROID_LOG_INFO, __FUNCTION__, "We are leaving Cleanup Python");
   return 1;
}

JNIEXPORT jint JNICALL Java_com_example_pythontest_PythonThread_runPython
      (JNIEnv* env, jobject obj, jstring filename)
{
   __android_log_write(ANDROID_LOG_VERBOSE, __FUNCTION__, "We are in Run Python");

//   char sendData[500];
//   char messageType[100];

   // Only initialize the Global Interpreter Lock once.
   if (!mPyGIL_Init)
   {
      mPyGIL_Init = true;
      PyEval_InitThreads();
      mPyThreadState = PyEval_SaveThread();
   }

   std::string lPythonFile = Utilities::getStringFromJava(env, filename);

   FILE* file = nullptr;

   if (!Utilities::fileExists(lPythonFile))
   {
      // The file does not exist, log a message and bail
      __android_log_write(ANDROID_LOG_ERROR, __FUNCTION__, "The Python file could not be found. Please verify it has been installed.");
      return -1;
   }

   //If we can't init, handle it
   if (!Py_IsInitialized())
   {
      __android_log_write(ANDROID_LOG_ERROR, __FUNCTION__, "Python has not been initialized while trying to start python in Run");
      return -4;
   }

   __android_log_write(ANDROID_LOG_VERBOSE, __FUNCTION__, "WfEngine process is starting");

   file = (FILE*) _Py_fopen(lPythonFile.c_str(), "r+");

   if (file != nullptr)
   {
      __android_log_write(ANDROID_LOG_VERBOSE, __FUNCTION__, "About to call SimpleFile with the following PY file");
      // Execute the python script.  A return of 0 is success, -1 is failure

      PyGILState_STATE lGILState = PyGILState_Ensure();                   // Make sure we are set thread safe
      int lPyReturn = PyRun_SimpleFile(file, lPythonFile.c_str());

      __android_log_write(ANDROID_LOG_INFO, __FUNCTION__, "After PyRun_SimpleFile ");
      PyGILState_Release(lGILState);                                      // Release our ensure
   }
   else
   {
      __android_log_write(ANDROID_LOG_WARN, __FUNCTION__, "Python was unable to open main.py");
   }

   __android_log_write(ANDROID_LOG_INFO, __FUNCTION__, "We are leaving run Python");

   return 0;
}

int setupAndroidSetupFile(std::string aPythonPath, std::string aSetupPath)
{
   std::string lPythonFile(aSetupPath + "android_setup.py");

   mPyProcess.setPyPath(aPythonPath);

   // So after a few checks, we should have just the file name, nothing else
   int lReturn = mPyProcess.loadFile(lPythonFile);

   return lReturn;
}

long setupEnvironment()
{
    long lReturnValue = mPyProcess.executeFunction(mSetupFunctionName.c_str());

    return lReturnValue;
}
