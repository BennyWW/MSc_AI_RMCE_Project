using System.Collections;
using System.Collections.Generic;
using System.IO;
using TMPro;
using UnityEngine;
using UnityEngine.InputSystem.Controls;
using UnityEngine.Networking;

/*
    - Retrieve the structure of the environment from the results of the prediction model. 
    - The results will be saved in a csv file. They need to be read and saved as a list of strings where each string represent each blocks structure.
        i.e: [["100101010..."], ["100101001001..."], ... ]
 */
public class GetMapStructure : MonoBehaviour
{
    [Header("Parameters")]
    public TextAsset csvFile; // Drag and drop your CSV file here in the Unity inspector
    public string[] MapStructure;
    public TMP_Text debugTxt;

    [Header("Accessing Streaming Assets Folder")]
    public string subfolderName = "Genetic Algorithm Results";
    public string fileName = "Set Up Results.csv";
    List<string> MapStructureList = new List<string>();

    public void ExtractBlocks()
    {
        string filePath = Path.Combine(Application.streamingAssetsPath, subfolderName, fileName+".csv");

        using (StreamReader reader = new StreamReader(filePath))
        {
            while (!reader.EndOfStream)
            {
                string line = reader.ReadLine();
                line = line.Replace(",", "");
                Debug.Log("From Streaming Assets: "+line);
                MapStructureList.Add(line);
            }
        }

        MapStructure = new string[MapStructureList.Count];

        for(int i = 0;i < MapStructureList.Count; i++)
        {
            MapStructure[i] = MapStructureList[i];
            MapStructure[i].Replace(",", "");
        }
    }
}
