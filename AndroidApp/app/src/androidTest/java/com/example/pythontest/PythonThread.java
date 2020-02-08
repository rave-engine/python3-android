package com.example.pythontest;


import android.content.Context;
import android.system.ErrnoException;
import android.system.Os;


import java.io.File;
import java.util.logging.Level;
import java.util.logging.Logger;

public class PythonThread extends Thread
{
    protected static String TAG = "PythonThread";

    // JNI links
    public native int initPython(String aPath, String aSetupDirectory);
    public native int runPython(String aFilename);
    public native int cleanupPython();

    private Logger mLogger;
    private Context mContext;


    public PythonThread(Context aContext, String aPath)
    {
        mLogger = Logger.getLogger(TAG);
        mContext = aContext;

        initializePython(aPath);
    }

    @SuppressWarnings("UnusedReturnValue")
    private int initializePython(String aPath)
    {
        final String lPath = aPath;
        mLogger.log(Level.INFO, "We are in initialize inside of the service");


// TODO - We need to extract the ZIP file for Python
        if ( Common.is64bitProcessor())
        {
            // Extract our 64bit zip
        }
        else
        {
            // extract our 32 it zip
        }


        // run a python file
        Thread lPythonThread = new Thread()
        {
            public void run()
            {
                this.setName("PythonEngine");     // Give our thread a friendly name we can debug with.

                // set all the environment variables for python to use
                try
                {
                    Os.setenv("ICanPassThis", "SuperString", true);
                }
                catch (ErrnoException e)
                {
                    mLogger.log(Level.SEVERE, "Could not set environment variables for Python");
                }

                // initialize python
                int lPythonReturn = initPython(lPath, Common.getEngineRootDirectory(mContext));

                // Make sure that we initialized cleanly
                if (lPythonReturn < 0)
                {
                    mLogger.log(Level.INFO, "Failed to initialize Python. Possible Python corruption. Python will be deleted and re-downloaded");


                    pythonCrashed(lPythonReturn, "Python Init Failed", "Unable to use Pything");

                    return;
                }

                File lPathToMain = new File(Common.getEngineRootDirectory(mContext) + "/main.py");

                // Make sure that the file exists
                if (!lPathToMain.exists())
                {
                    mLogger.log(Level.SEVERE, "Unable to run the Python Level 3.  The main.py does not exist in proper location.  File Location=" + lPathToMain.getAbsolutePath());
                    return;
                }

                try
                {
                    // Run our main
                    runPython(lPathToMain.getAbsolutePath());
                    // We are done running, we will init again, cleanup
                    cleanupPython();
                }
                catch (Exception e)
                {
                    mLogger.log(Level.SEVERE, "!@!@!@!@ Our thread was interrupted!!!");
                }
            }
        };

        // Start this thread
        lPythonThread.start();

        return 0;
    }

    /**
     * A method to handle when Python crashes.  Simply show a dialog and tell them to restart
     */
    @SuppressWarnings("unused")
    public void pythonCrashed(int aCode, String aSignalDescription, String aSignalCodeDescription)
    {
        // log the fatal signal
        RuntimeException lException = new RuntimeException("pythonCrashed");
        mLogger.log(Level.SEVERE, "Python crash occurred!", lException);


        // try to ensure our process dies completely
        System.exit(0);
    }

}
