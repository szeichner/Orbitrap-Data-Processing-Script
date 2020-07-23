//TODO: add header comments

using System;
using System.Collections.Generic;
using ThermoFisher.CommonCore.Data;

namespace SGStatistic
{
    /// <summary>
    /// Populate properties based on method file that will be used to process .RAW data files
    /// </summary>
    public class MethodFile
    {
        //Different strings used to parse the method file inputs
        private string inputPeakNumberString = "peakNumber";
        private string chemicalFormulaString = "chemicalFormula";
        private string massString = "mass";
        private string toleranceString = "tolerance";
        private string toleranceUnitsString = "toleranceUnits";

        public int InputPeakNumber { get; set; }
        public string[] ChemicalFormulas { get; set; }
        public double[] Masses { get; set; }
        public double[] MassTolerances { get; set; }
        public ToleranceUnits[] MassToleranceUnits { get; set; }

        ///<summary> Instantiate method file using input .txt file path</summary>
        public MethodFile(string inputMethodFile)
        {
            //Read lines in from the method file .txt
            string[] methodLines = System.IO.File.ReadAllLines(inputMethodFile);
            Dictionary<string, string> methodDictionary = new Dictionary<string, string>(methodLines.Length);

            //parse the input method file
            for (int i = 0; i < methodLines.Length; i++)
            {
                string[] splitValues = methodLines[i].Split('=');

                methodDictionary.Add(splitValues[0], splitValues[1]);
            }

            //parse the other inputs of the method file, and set the properties of the Method File object
            //get the number of peaks
            methodDictionary.TryGetValue(inputPeakNumberString, out string peakNumber);
            InputPeakNumber = Convert.ToInt32(peakNumber);

            //get the list of chemical formulas
            methodDictionary.TryGetValue(chemicalFormulaString, out string chemFormulas);
            chemFormulas = chemFormulas.Trim('\0');
            string[] formulaArray = chemFormulas.Split(',');
            ChemicalFormulas = new string[formulaArray.Length];
            for (int i = 0; i < formulaArray.Length; i++)
            {
                ChemicalFormulas[i] = formulaArray[i];
            }
            
            //get the list of masses
            methodDictionary.TryGetValue(massString, out string masses);
            masses = masses.Trim('\0');
            string[] massesArray = masses.Split(',');
            Masses = new double[massesArray.Length];
            for (int i = 0; i < massesArray.Length; i++)
            {
                Masses[i] = Convert.ToDouble(massesArray[i]);
            }

            //get the list of mass tolerances
            methodDictionary.TryGetValue(toleranceString, out string tolerances);
            tolerances = tolerances.Trim('\0');
            string[] tolerancesArray = tolerances.Split(',');
            MassTolerances = new double[tolerancesArray.Length];
            for (int i = 0; i < tolerancesArray.Length; i++)
            {
                MassTolerances[i] = Convert.ToDouble(tolerancesArray[i]);
            }

            methodDictionary.TryGetValue(toleranceUnitsString, out string toleranceUnits);
            toleranceUnits = toleranceUnits.Trim('\0');
            string[] toleranceUnitsArray = toleranceUnits.Split(',');
            MassToleranceUnits = new ToleranceUnits[toleranceUnitsArray.Length];
            for (int i = 0; i < toleranceUnitsArray.Length; i++)
            {
                MassToleranceUnits[i] = (ToleranceUnits)Enum.Parse(typeof(ToleranceUnits), toleranceUnitsArray[i]);
                 
            }

        }

    }
    }

