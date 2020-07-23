using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Runtime.ExceptionServices;

using ThermoFisher.CommonCore.Data;
using ThermoFisher.CommonCore.Data.Business;
using ThermoFisher.CommonCore.Data.FilterEnums;
using ThermoFisher.CommonCore.Data.Interfaces;
using ThermoFisher.CommonCore.MassPrecisionEstimator;
using ThermoFisher.CommonCore.RawFileReader;

namespace SGStatistic
{
    /// <summary>
    /// Main program to run the Raw File Processor
    /// </summary>
    internal static class Program
    {

        public static void Main()
        {

            //string args=[]

            string filePath = "/Users/sarahzeichner/Documents/Caltech/Research/Code/SG-Statistic/testFolder/20200205_2_USGS37_full1.RAW"; //args[0]; 
            string methodFileName = "/Users/sarahzeichner/Documents/Caltech/Research/Code/SG-Statistic/testFolder/method.txt"; //args[1];
            string exportFileName = "output.txt"; //args[2];

            //Try get method file and list of raw file names from folder path
            if(File.Exists(filePath))
            {
                try
                {
                        RawDataProcessor thisProcessor = new RawDataProcessor(filePath, methodFileName);
                        thisProcessor.ProcessRawFile(thisProcessor.RawFilePathName, thisProcessor.MethodFile, exportFileName);

                }
                catch (Exception ex)
                {
                    Console.Write(ex); 
                }
            }

            Console.Write(".RAW file processing complete");

        }
    }
}
