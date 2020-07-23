using System;
using System.Collections.Generic;
using System.IO;
using Newtonsoft.Json;
using System.Linq;
using System.Reflection;
using System.Text;

namespace SGStatistic
{
    /// <summary>
    /// Process Raw Data files within a folder path, given an input method and list of raw files
    /// </summary>
    public class RawDataProcessor
    {
        /// <summary>
        /// list of raw files to process
        /// </summary>
        public string RawFilePathName { get; set; }
        /// <summary>
        /// method file object created from input method.txt file
        /// </summary>
        public MethodFile MethodFile { get; set; }

        /// <summary>
        /// Create a RawDataProcessor object with input folder 
        /// </summary>
        /// <param name="filenamePath"> Location of .RAW file to process </param>
        /// <param name="methodFileNamePath"> Location of method.txt </param>
        public RawDataProcessor(string filenamePath, string methodFileNamePath)
        {
            try
            {
                //read in the file path name, and the method file
                RawFilePathName = filenamePath;
                MethodFile = new MethodFile(methodFileNamePath);
               
            }
            catch (Exception ex)
            {
                Console.Write(ex);
            }

        }

        /// <summary>
        /// Process a list of files in a specified folder using a specified method 
        /// </summary>
        /// <param name="fileNames"></param>
        /// <param name="methodFile"></param>
        /// <param name="exportFileName"></param>
        public void ProcessRawFile(string fileName, MethodFile methodFile, string exportFileName)
        {

            List<RawDataObject> rawDataObjects = new List<RawDataObject>();
            for (int j = 0; j < methodFile.Masses.Length; j++)
            {
                rawDataObjects.Add(new RawDataObject(fileName, methodFile.Masses[j], methodFile.MassTolerances[j], methodFile.MassToleranceUnits[j]));
            }

            try
            {
                //write to json object to export
                string rtnJsonObject = JsonConvert.SerializeObject(rawDataObjects);
                //write json object to the file
                System.IO.File.WriteAllText(fileName + exportFileName, rtnJsonObject);

            }
            catch (Exception ex)
            {
                Console.Write(ex);
            }

        }

    }
}
