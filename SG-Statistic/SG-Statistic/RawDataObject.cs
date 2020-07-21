using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text;
using Newtonsoft.Json;

using ThermoFisher.CommonCore.Data;
using ThermoFisher.CommonCore.Data.Business;
using ThermoFisher.CommonCore.Data.FilterEnums;
using ThermoFisher.CommonCore.Data.Interfaces;
using ThermoFisher.CommonCore.MassPrecisionEstimator;
using ThermoFisher.CommonCore.RawFileReader;

namespace SGStatistic
{
    /// <summary>
    /// This object gets populated with input data for one peak from a RAW data file, based on input peak mass and mass tolerance.
    /// </summary>
    [Serializable]
    public class RawDataObject
    {
        //Constants
        ///<summary> Type of filter </summary>
        private const string FILTER_MS = "ms";

        //Properties from the Method file
        ///<summary> Mass Tolerance </summary>
        private double Tolerance { get; set; }
        private ToleranceUnits ToleranceUnits { get; set; }
        ///<summary> Mass of peak </summary>
        private double Mass { get; set; }
        ///<summary> High mass based on  input mass and  mass tolerance </summary>
        private double HighMass { get; set; }
        ///<summary> Low mass based on  input mass and  mass tolerance </summary>
        private double LowMass { get; set; }

        //Header info
        /// <summary>
        /// Mass resolution of the experiment
        /// </summary>
        public double MassResolution { get; set; }
        //Chromatogram Data
        /// <summary>
        /// List of scans from the analysis
        /// </summary>
        public int[] ScanNumList { get; set; }
        /// <summary>
        /// Time positions of the chromatogram
        /// </summary>
        public double[] ExactMassList { get; set; }
        /// <summary>
        /// Intensities of the chromatogram
        /// </summary>
        public double[] MassIntensityList { get; set; }
        //SpectrumData
        /// <summary>
        /// TIC from mass spectrum
        /// </summary>
        public double[] TICList { get; set; }
        /// <summary>
        /// Integration time of a specific scan in the spectra
        /// </summary>
        public double[] ITList { get; set; }
        /// <summary>
        /// Retention time of each scan from the mass spectrum for the peak of interest
        /// </summary>
        public double[] RetentionTimeList { get; set; }


        /// <summary>
        /// Instantiates and populates a raw data object based on input raw file and specified method
        /// <param name="inputRawFile"></param>
        /// <param name="formula"></param>
        /// <param name="mass"></param>
        /// <param name="tolerance"></param>
        /// <param name="toleranceUnits"></param>
        public RawDataObject(string inputRawFile, double mass, double tolerance, ToleranceUnits toleranceUnits)
        {
            CalculateHighAndLowMasses(mass, tolerance, toleranceUnits);
            IRawDataPlus rawFile = GetSetRawFileData(inputRawFile);
            GetChromatogramData(rawFile);
            GetSpectrumData(rawFile);
            CleanUpRawFile(rawFile);

        }

        /// <summary>
        /// Reads the information from the method file and populates fields based on specified peak and tolerance
        /// </summary>
        /// <param name="mass"></param>
        /// <param name="tolerance"></param>
        /// <param name="toleranceUnits"></param>
        private void CalculateHighAndLowMasses(double mass, double tolerance, ToleranceUnits toleranceUnits)
        {
            Mass = mass;
            ToleranceUnits = toleranceUnits;

            //convert tolerance into the correct units
            Tolerance = Convert.ToDouble(tolerance); // set to converted tolerance;

            // ToleranceUnits = toleranceUnits;
            if (ToleranceUnits == ToleranceUnits.mmu)
            {
                HighMass = mass + (tolerance / 1000);
                LowMass = mass - (tolerance / 1000);

            }
            else if (ToleranceUnits == ToleranceUnits.ppm)
            {
                HighMass = mass * (1 + tolerance / 1000000);
                LowMass = mass * (1 - tolerance / 1000000);
            }
            else
            {
                Console.WriteLine("Error in the mass tolerance unit.");
            }
        }
 
        /// <summary>
        /// Get and set general information from the raw file
        /// </summary>
        /// <param name="inputRawFile"></param>
        /// <returns></returns>
        private IRawDataPlus GetSetRawFileData(string inputRawFile)
        {
            // Create the IRawDataPlus object for accessing the RAW file
            IRawDataPlus rawFile = RawFileReaderAdapter.FileFactory(inputRawFile);

            if (!rawFile.IsOpen || rawFile.IsError)
            {
                Console.WriteLine("Unable to access the RAW file using the RawFileReader class!");
            }

            // Check for any errors in the RAW file
            if (rawFile.IsError)
            {
                Console.WriteLine("Error opening ({0})", rawFile.FileError);
            }

            // Check if the RAW file is being acquired
            if (rawFile.InAcquisition)
            {
                Console.WriteLine("RAW file still being acquired...");

            }

            // Select instrument we are intereted in looking at data from
            rawFile.SelectInstrument(Device.MS, 1);

            return rawFile;
        }
        /// <summary>
        /// Get and set chromatogram data from the raw file
        /// </summary>
        /// <param name="inputRawFile"></param>
        private void GetChromatogramData(IRawDataPlus inputRawFile)
        {
            try
            {
                //Get mass resolution for the run from the header
                MassResolution = inputRawFile.RunHeaderEx.MassResolution;

                // Find startScan and endScan
                int startScan = inputRawFile.RunHeader.FirstSpectrum;
                int endScan = inputRawFile.RunHeader.LastSpectrum;

                //Set up settings to extract the data
                ChromatogramTraceSettings traceSettings =
                new ChromatogramTraceSettings(TraceType.MassRange)
                {
                    Filter = FILTER_MS,
                    MassRanges = new[] { new Range(LowMass, HighMass) }
                };
                IChromatogramSettings[] allSettings = { traceSettings };

                MassOptions massOptions = new MassOptions() { Tolerance = Tolerance, ToleranceUnits = ToleranceUnits };
                var chromatogramData = inputRawFile.GetChromatogramData(allSettings, startScan, endScan, massOptions); //get all chromatogram data

                // Get data from the chromatogram
                ScanNumList = chromatogramData.ScanNumbersArray[0];
                ExactMassList = chromatogramData.PositionsArray[0]; //get positions  of each scan
                MassIntensityList = chromatogramData.IntensitiesArray[0]; //get list of intensities for scan numbers
            }
            catch(Exception ex)
            {
                Console.Write("Error in accessing chromatogram data: " + ex);
            }
            
        }

        /// <summary>
        /// Get and set data from the mass spectrum
        /// </summary>
        /// <param name="inputRawFile"></param>
        private void GetSpectrumData(IRawDataPlus inputRawFile)
        {
            // Get the first and last scan from the RAW file
            int firstScanNumber = inputRawFile.RunHeaderEx.FirstSpectrum;
            int lastScanNumber = inputRawFile.RunHeaderEx.LastSpectrum;
            string itHeaderParam = "Ion Injection Time (ms)";

            // Set up empty variables to populate with mass spectrum data
            TICList = new double[lastScanNumber];
            ITList = new double[lastScanNumber];
            RetentionTimeList = new double[lastScanNumber];

            try
            {
                //get out information from mass spectra for each scan
                for (int scan = 0; scan <= (ScanNumList.Length - 1); scan++)
                {
                    int thisScan = ScanNumList[scan];
                    // get the scan statistics for this scan number
                    ScanStatistics scanStatistic = inputRawFile.GetScanStatsForScanNumber(thisScan);

                    //get the TIC
                    TICList[scan] = scanStatistic.TIC;
                    //get retention time
                    RetentionTimeList[scan] = inputRawFile.RetentionTimeFromScanNumber(thisScan);
                    ITList[scan] = GetScanExtraDouble(inputRawFile, thisScan, itHeaderParam);

                    //TODO: get out noise for peaks

                }
            }
            catch (Exception ex)
            {
                Console.Write("Error in accessing spectrum data: " + ex);
            }
          
            }

        /// <summary>
        /// Get additional double from scan information
        /// </summary>
        /// <param name="rawPlus"></param>
        /// <param name="scan"></param>
        /// <param name="token"></param>
        /// <returns></returns>
        internal static double GetScanExtraDouble(IRawDataPlus rawPlus, int scan, string token)
        {

            double dVal = -1.0;

            LogEntry instLog = rawPlus.GetTrailerExtraInformation(scan);
            int iLen = instLog.Length;

            for (int ii = 0; ii < iLen; ii++)
            {
                if (instLog.Labels[ii].Contains(token))
                {
                    if (double.TryParse(instLog.Values[ii], out dVal))
                    {
                        return dVal;
                    }
                }
            }
            return dVal;
        }


        /// <summary>
        /// Dispose of the raw file object to handle memory situation
        /// </summary>
        /// <param name="rawFile"></param>
        private void CleanUpRawFile(IRawDataPlus rawFile)
        {
            rawFile.Dispose();
        }

    }  
    }
