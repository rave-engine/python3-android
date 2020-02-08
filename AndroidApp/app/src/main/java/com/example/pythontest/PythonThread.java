package com.example.pythontest;


import android.content.Context;
import android.content.res.AssetManager;
import android.system.ErrnoException;
import android.system.Os;
import android.util.Log;
import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

public class PythonThread extends Thread
{
    @SuppressWarnings("FieldCanBeLocal")
    private static String TAG = "PythonThread";

    // JNI links
    public native int initPython(String aPath, String aSetupDirectory);
    public native int runPython(String aFilename);
    public native int cleanupPython();

    private Logger mLogger;
    private Context mContext;


    PythonThread(Context aContext)
    {
        mLogger = Logger.getLogger(TAG);
        mContext = aContext;

        initializePython();
    }

    @SuppressWarnings("UnusedReturnValue")
    private int initializePython()
    {
        mLogger.log(Level.INFO, "We are in initialize inside of the service");

        String lTempPath = Common.getEngineRootDirectory(mContext);

        // Unzip the right folder for he processor
        if ( Common.is64bitProcessor())
        {
            // Extract our 64bit zip
            unzipFileFromAssets("Python64.zip");
            lTempPath += "Python64";
        }
        else
        {
            unzipFileFromAssets("Python32");
            lTempPath += "Python32";
        }

        // Put the python files where we can execute them
        copyPythonFilesFromAssets("android_setup.py");
        copyPythonFilesFromAssets("main.py");

        final String lPythonRootPath = lTempPath;

        // run a python file
        Thread lPythonThread = new Thread()
        {
            public void run()
            {
                this.setName("PythonEngine");     // Give our thread a friendly name we can debug with.

                // set all the environment variables for python to use
                try
                {
                    Os.setenv("NumberToWrite", "104", true);
                }
                catch (ErrnoException e)
                {
                    mLogger.log(Level.SEVERE, "Could not set environment variables for Python");
                }

                // initialize python
                int lPythonReturn = initPython(lPythonRootPath, Common.getEngineRootDirectory(mContext));

                // Make sure that we initialized cleanly
                if (lPythonReturn < 0)
                {
                    mLogger.log(Level.INFO, "Failed to initialize Python. Possible Python corruption. Python will be deleted and re-downloaded");
                    return;
                }

                File lPathToMain = new File(Common.getEngineRootDirectory(mContext) + "/main.py");

                // Make sure that the file exists0
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

    private void copyPythonFilesFromAssets(String aFileName)
    {
        AssetManager assetManager = mContext.getAssets();

        InputStream lInputStream;
        OutputStream lOutputStream;
        try
        {
            lInputStream = assetManager.open(aFileName, AssetManager.ACCESS_BUFFER);

            String outDir = Common.getEngineRootDirectory(mContext);

            File outFile = new File(outDir, aFileName);

            lOutputStream = new FileOutputStream(outFile);
            copyFile(lInputStream, lOutputStream);
            lInputStream.close();
            lOutputStream.flush();
            lOutputStream.close();
        }
        catch(IOException e)
        {
            Log.e("tag", "Failed to copy asset file: " + aFileName, e);
        }

    }

    private void copyFile(InputStream in, OutputStream out) throws IOException
    {
        byte[] buffer = new byte[1024];
        int read;
        while ((read = in.read(buffer)) != -1)
        {
            out.write(buffer, 0, read);
        }
    }

    private void unzipFileFromAssets(String aSourceFile)
    {
        AssetManager assetManager = mContext.getAssets();

        InputStream lInputStream = null;
        try
        {
            lInputStream = assetManager.open(aSourceFile, AssetManager.ACCESS_BUFFER);
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }




//        String lDestinationFile = mContext.getExternalFilesDir(null) + \"\\\\Python" + aSourceFile;
        String lDestinationFile = Common.getEngineRootDirectory(mContext);

        ZipInputStream zis;
        try
        {
            // ensure the destination directory exists
            if (!new File(lDestinationFile).mkdirs())
            {
                mLogger.log(Level.INFO, "Unable to create directory '" + lDestinationFile + "'. It probably already exists");
            }

            // get the input stream of the zip file itself
            assert lInputStream != null;
            zis = new ZipInputStream(new BufferedInputStream(lInputStream));
            ZipEntry ze;
            byte[] buffer = new byte[8192];
            int count;

            // loop through all the zip entries in the zip
            while ((ze = zis.getNextEntry()) != null)
            {
                // if this entry is simply a directory, just create it and move on
                if (ze.isDirectory())
                {
                    String dir = Common.ensureStringEndsWithForwardslash(lDestinationFile + File.separator + ze.getName());
                    File fmd = new File(dir);
                    if (!fmd.exists())
                    {
                        // directory doesn't exist yet, try to create it
                        if (!fmd.mkdirs())
                        {
                            mLogger.log(Level.WARNING, "Unable to create directory on device from zip: " + dir + ", DirExistsAlready=" + fmd.exists());
                        }
                    }
                    continue;
                }

                // if we get here, we're dealing with a straight file
                File destFile = new File(lDestinationFile, ze.getName());
                File destinationParent = destFile.getParentFile();

                // create the parent directory structure if needed for the file
                assert destinationParent != null;
                if (!destinationParent.isDirectory() && !destinationParent.mkdirs())
                {
                    mLogger.log(Level.WARNING, "Unable to create directory " + destinationParent);
                }

                // write the file
                FileOutputStream lFileStream = new FileOutputStream(lDestinationFile + File.separator + ze.getName());
                while ((count = zis.read(buffer)) != -1)
                {
                    lFileStream.write(buffer, 0, count);
                }

                lFileStream.close();
                zis.closeEntry();
            }

            zis.close();

            mLogger.log(Level.INFO, aSourceFile + " unzipped successfully");
        }
        catch (Exception e)
        {
            mLogger.log(Level.SEVERE, "Exception while unzipping file:" + e.getMessage());
        }
    }
}
