package com.example.pythontest;

import android.content.Context;
import android.os.Build;

import java.util.Objects;

class Common
{

    static String getEngineRootDirectory(Context aContext)
    {
        //return Common.ensureStringEndsWithForwardslash((Objects.requireNonNull(aContext.getExternalFilesDir(null))).getAbsolutePath());
        return Common.ensureStringEndsWithForwardslash(aContext.getFilesDir().getPath());

    }

    static boolean is64bitProcessor()
    {
        // The SUPPORTED_ABIS is a String Array with all of the architectures the CPU supports, we are specifically looking to see
        // if this one supports 64bit
        return (Build.SUPPORTED_64_BIT_ABIS.length > 0);
    }

    static String ensureStringEndsWithForwardslash(String aString)
    {
        if (!aString.endsWith("/"))
        {
            return (aString + "/");
        }

        return aString;
    }

}
