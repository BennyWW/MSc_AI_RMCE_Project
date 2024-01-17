using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[CreateAssetMenu(fileName = "Spawner Attributes", menuName = "ScriptableObjects/Spawner Attributes")]

/*
 This provides:
    - Bot prefabs: x and y bot
    - Number of bots to spawn at start
 */
public class BotsSpawner : ScriptableObject
{
    [Header("Bots")]
    public GameObject ScoutBot_prefab;
    public float ScoutBot_No = 20f;
    public GameObject WarriorBot_prefab;
    public float WarriorBot_No = 40f;
    public GameObject BossBot_prefab;
    public float BossBot_No = 40f;
    public GameObject AllyBot_prefab;
    public float AllyBot_No = 40f;
}
