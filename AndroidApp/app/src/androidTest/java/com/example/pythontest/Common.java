package com.example.pythontest;

import android.content.Context;
import android.os.Build;

public class Common
{

    public static String getEngineRootDirectory(Context aContext)
    {
        return aContext.getExternalFilesDir(null).getAbsolutePath();
    }

    public static boolean is64bitProcessor()
    {
        // The SUPPORTED_ABIS is a String Array with all of the architectures the CPU supports, we are specifically looking to see
        // if this one supports 64bit
        return (Build.SUPPORTED_64_BIT_ABIS.length > 0);
    }


}
