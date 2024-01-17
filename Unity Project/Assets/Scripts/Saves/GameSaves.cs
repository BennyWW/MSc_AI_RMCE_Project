using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[CreateAssetMenu(fileName = "Game Saves", menuName = "Game Saves/Saves")]
public class GameSaves : ScriptableObject
{
    [Header("Save Names/Titles")]
    public List<Save> saveList = new();
}
