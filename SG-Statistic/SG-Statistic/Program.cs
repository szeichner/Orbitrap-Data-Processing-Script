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

        public static void Main(string[] args)
        {
            //look for a method file in the input folder path

            //Console.Write("Please input a folder path with .RAW files of interest for analysis");
            string folderPath = args[0]; 
            string methodFileName = args[1];
            //Console.Write("Please input what path name you would like to append to each of your output files.");
            string exportFileName = args[2];

            //Try get method file and list of raw file names from folder path
            if(Directory.Exists(folderPath))
            {
                try
                {
                        RawDataProcessor thisProcessor = new RawDataProcessor(folderPath, methodFileName);
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
