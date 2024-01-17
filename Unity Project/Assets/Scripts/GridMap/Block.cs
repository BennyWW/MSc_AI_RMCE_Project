using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity;
using Random = UnityEngine.Random;
using System.Linq;
using JetBrains.Annotations;
using System.Security;
using UnityEngine.UIElements;
using UnityEngine.AI;

/*
    This is the basic element that defines the map(grid). The grid will have a defined number of blocks each with its unique features set up 
    randomly by the genetic algorithm. The blocks have a centre hexagon, 6 walls, and other objects such as trees, secrets, etc. What is in 
    each block will be defined by the map generated from the personality profile of the player. 

A block will have 2 functions:
> DefineFeatures()          =           Defines what objects will be active or not
> DetermineScore()          =           Evaluate the features and return a score. (Score will be used to calculate the fitness)

*/
public class Block : MonoBehaviour, IGA_Element
{
    [Header("Block Elements")]
    [SerializeField] GameObject hexagon;                        // Centre hexagon of the block
    [SerializeField] public List<GameObject> unlockObjs = new();       // Collectables to upgrade player
    [SerializeField] public List<GameObject> walls = new();            // Walls surrounding the hexagon
    [SerializeField] public List<GameObject> secrets = new();          // Secrets in block
    [SerializeField] public List<GameObject> trees = new();            // Trees in block
    [SerializeField] public List<GameObject> grass = new();            // grass in block
    [SerializeField] public List<GameObject> centralHex = new();       // central hexagon in middle of block
    [SerializeField] public List<GameObject> ally_Home = new();        // ally home in middle of block
    [SerializeField] public List<GameObject> spawns_Ally = new();      // ally spawns. 1 for each ally. 
    [SerializeField] public List<GameObject> spawns_Enemy = new();     // enemy spawns. 1 for each enemy
    [SerializeField] public List<GameObject> spawns_DangerousEnemy = new();     // dangerous enemy spawns. 1 for each enemy
    [SerializeField] public List<GameObject> interactableObjs = new();     // dangerous enemy spawns. 1 for each enemy
    //[SerializeField] List<GameObject> other = new();            // This can be trees, secrets, etc. (To provide some adventure)

    [Header("Bots Spawning")]
    public List<Transform> spawnLocations = new();
    public BotsSpawner botsSpawner;


    [Header("\n\nBlock Binary Structure (Chromosome)")]
    public string blockStructure;
    public List<int> wallsInt = new();
    public List<int> secretsInt = new();
    public List<int> treesInt = new();
    public List<int> centralHexInt = new();
    public List<int> ally_HomeInt = new();
    public List<int> spawns_AllyInt = new();
    public List<int> spawns_EnemyInt = new();
    public List<int> spawns_DangerousEnemyInt = new();
    public List<int> grassInt = new();
    public List<int> unlockObjsInt = new();
    public List<int> interactableObjsInt = new();

    public void DefineFeatures(string structure)
    {
        // Using Structure list provided
        /*
         The list is structured as follows:        
        [000        000000      0000            0000    0000000000      0           0         0          0              0         ]
        unlockObjs  walls       secrets_orbs    trees   grass       centralHex  allyHome    Allies      Enemies     DangerousEnemy
         */

        // Define features
        //Walls
        wallsInt = SplitStructure(structure, 0, 6);
        DefineFeatures(walls, wallsInt);                                
        
        //Secrets_Orbs
        secretsInt = SplitStructure(structure, 6, 4);
        DefineFeatures(secrets, secretsInt);
        
        //Trees
        treesInt = SplitStructure(structure, 10, 4);
        DefineFeatures(trees, treesInt);

        //Central Hex
        centralHexInt = SplitStructure(structure, 14, 1);
        DefineFeatures(centralHex, centralHexInt);
        
        //AllyHome
        ally_HomeInt = SplitStructure(structure, 15, 1);
        DefineFeatures(ally_Home, ally_HomeInt);
        
        //Allies
        spawns_AllyInt = SplitStructure(structure, 16, 1);
        DefineFeatures(spawns_Ally, spawns_AllyInt);
        
        //Enemies
        spawns_EnemyInt = SplitStructure(structure, 17, 1);
        DefineFeatures(spawns_Enemy, spawns_EnemyInt);

        //Dangerous Enemies
        spawns_DangerousEnemyInt = SplitStructure(structure, 18, 1);
        DefineFeatures(spawns_DangerousEnemy, spawns_DangerousEnemyInt);

        //Grass
        grassInt = SplitStructure(structure, 19, 10);
        DefineFeatures(grass, grassInt);

        // Unlock Objects (for upgrades)
        unlockObjsInt = SplitStructure(structure, 29, 3);
        DefineFeatures(unlockObjs, unlockObjsInt);

        //Interactables
        interactableObjsInt = SplitStructure(structure, 32, 3);
        DefineFeatures(interactableObjs, interactableObjsInt);


        List<int> SplitStructure(string structure,int startIndex, int length)
        {
            List<int> result = new List<int>();
            foreach(char c in structure.Substring(startIndex,length))
            {
                result.Add(int.Parse(c.ToString()));
            }
            return result;
        }
        
        void DefineFeatures(List<GameObject> features, List<int> featuresInt)
        {
            for(int i = 0; i < features.Count; i++)
            {
                features[i].SetActive(featuresInt[i] == 1);
            }
        }

    }

    float IGA_Element.DetermineScore()
    {            
        return 0f;
    }

    public void Spawn_Bot(Spawner_Bots spawner_Bots, LevelManager levelManagerRef)
    {
        /*// select the spawn location
        Vector3 spawnLocation = new();
        if (enemy)
        {
            spawnLocation = spawns_Enemy[spawnLocationIndex].transform.position;
        }
        else
        {
            spawnLocation = spawns_Ally[spawnLocationIndex].transform.position;
        }
        // Change location of bot to one of the spawn locations
        bot.transform.position = new Vector3(spawnLocation.x, bot.transform.position.y, spawnLocation.z);*/


        // Spawn bot in active spawns
        for(int i = 0; i < spawns_Enemy.Count; i++)
        {
            if (spawns_Enemy[i].gameObject.activeSelf)
            {
                GameObject newbot = Instantiate(botsSpawner.WarriorBot_prefab, spawner_Bots.gameObject.transform, true);
                newbot.GetComponent<Abilities_Warrior>().SetUp();
                newbot.GetComponent<Abilities_Warrior>().levelManager = levelManagerRef;

                if(newbot.GetComponent<KillScore>() != null)
                {
                    newbot.GetComponent<KillScore>().levelManagerRef = levelManagerRef;
                }

                //bots.Add(bot);
                //gridGenerator.blocksList[i].GetComponent<Block>().Spawn_Bot(bot, true, j);
               //newbot.transform.position = new Vector3(spawns_Enemy[i].transform.position.x, spawns_Enemy[i].transform.position.y, spawns_Enemy[i].transform.position.z);
                newbot.GetComponent<NavMeshAgent>().Warp(new Vector3(spawns_Enemy[i].transform.position.x, spawns_Enemy[i].transform.position.y, spawns_Enemy[i].transform.position.z));

                //Add bot to bot list
                spawner_Bots.bots.Add(newbot);

                // Revive Bot
                IAbilities abilities = newbot.GetComponent<IAbilities>();
                if (abilities != null)
                {
                    abilities.Die(false);
                }
            }
        }

        for (int i = 0; i < spawns_DangerousEnemy.Count; i++)
        {
            if (spawns_Ally[i].gameObject.activeSelf)
            {
                GameObject newbot = Instantiate(botsSpawner.BossBot_prefab, spawner_Bots.gameObject.transform, true);
                newbot.GetComponent<Abilities_Warrior>().SetUp();
                newbot.GetComponent<Abilities_Warrior>().levelManager = levelManagerRef;

                if (newbot.GetComponent<KillScore>() != null)
                {
                    newbot.GetComponent<KillScore>().levelManagerRef = levelManagerRef;
                }

                //bots.Add(bot);
                //gridGenerator.blocksList[i].GetComponent<Block>().Spawn_Bot(bot, true, j);
                //newbot.transform.position = new Vector3(spawns_DangerousEnemy[i].transform.position.x, spawns_DangerousEnemy[i].transform.position.y, spawns_DangerousEnemy[i].transform.position.z);
                newbot.GetComponent<NavMeshAgent>().Warp(new Vector3(spawns_DangerousEnemy[i].transform.position.x, spawns_DangerousEnemy[i].transform.position.y, spawns_DangerousEnemy[i].transform.position.z));

                //Add bot to bot list
                spawner_Bots.bots.Add(newbot);

                // Revive Bot
                IAbilities abilities = newbot.GetComponent<IAbilities>();
                if (abilities != null)
                {
                    abilities.Die(false);
                }
            }
        }

        for (int i = 0; i < spawns_Ally.Count; i++)
        {
            if (spawns_Ally[i].gameObject.activeSelf)
            {
                GameObject newbot = Instantiate(botsSpawner.AllyBot_prefab, spawner_Bots.gameObject.transform, true);
                newbot.GetComponent<Abilities_Ally>().SetUp();
                newbot.GetComponent<Abilities_Ally>().levelManager = levelManagerRef;
                //bots.Add(bot);
                //gridGenerator.blocksList[i].GetComponent<Block>().Spawn_Bot(bot, true, j);
                //newbot.transform.position = new Vector3(spawns_Ally[i].transform.position.x, spawns_Ally[i].transform.position.y, spawns_Ally[i].transform.position.z);
                newbot.GetComponent<NavMeshAgent>().Warp(new Vector3(spawns_Ally[i].transform.position.x, spawns_Ally[i].transform.position.y, spawns_Ally[i].transform.position.z));

                //Add bot to bot list
                spawner_Bots.bots.Add(newbot);

                // Revive Bot
                IAbilities abilities = newbot.GetComponent<IAbilities>();
                if (abilities != null)
                {
                    abilities.Die(false);
                }
            }
        }
    }

    public void Spawn_Bot_Random(GameObject bot)
    {
        // Randomly select a spawn location
        int randomIndex = Random.Range(0, spawnLocations.Count);
        Vector3 spawnLocation = spawnLocations[randomIndex].position;

        // Change location of bot to one of the spawn locations
        bot.transform.position = new Vector3(spawnLocation.x, bot.transform.position.y, spawnLocation.z);

        // Revive Bot
        IAbilities abilities = bot.GetComponent<IAbilities>();
        if (abilities != null)
        {
            abilities.Die(false);

        }
    }

}
