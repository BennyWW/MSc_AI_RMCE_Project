using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Spawner_Bots : MonoBehaviour
{
    [Header("Spawner")]
    public GridGenerator gridGenerator;
    public BotsSpawner botsSpawner;
    public List<GameObject> bots = new();

    public void SpawnBots()
    {
        // Spawn warrior bots
        for (int i = 0; i < botsSpawner.WarriorBot_No; i++)
        {
            // Choose random Spawn location
            int randomIndex = Random.Range(0, gridGenerator.blocksList.Count);
            GameObject bot = Instantiate(botsSpawner.WarriorBot_prefab, transform);
            bot.GetComponent<Abilities_Warrior>().SetUp();
            bots.Add(bot);
            gridGenerator.blocksList[randomIndex].GetComponent<Block>().Spawn_Bot_Random(bot);
        }

        // Spawn scout bots
        for (int i = 0; i < botsSpawner.ScoutBot_No; i++)
        {
            // Choose random Spawn location
            int randomIndex = Random.Range(0, gridGenerator.blocksList.Count);
            GameObject bot = Instantiate(botsSpawner.ScoutBot_prefab, transform);
            bot.GetComponent<Abilities_Warrior>().SetUp();
            bots.Add(bot);
            gridGenerator.blocksList[randomIndex].GetComponent<Block>().Spawn_Bot_Random(bot);
        }

        // Spawn ally bots
        for (int i = 0; i < botsSpawner.AllyBot_No; i++)
        {
            // Choose random Spawn location
            int randomIndex = Random.Range(0, gridGenerator.blocksList.Count);
            GameObject bot = Instantiate(botsSpawner.AllyBot_prefab, transform);
            bot.GetComponent<Abilities_Ally>().SetUp();
            bots.Add(bot);
            gridGenerator.blocksList[randomIndex].GetComponent<Block>().Spawn_Bot_Random(bot);
        }
    }

    public void AddBots(LevelManager levelManagerRef)
    {
        // Spawn Enemy Bots
        /*for (int i = 0; i < gridGenerator.blocksList.Count; i++)
        {
            for (int j = 0; j < gridGenerator.blocksList[i].GetComponent<Block>().spawns_Enemy.Count; j++)
            {
                if (gridGenerator.blocksList[i].GetComponent<Block>().spawns_Enemy[j].activeSelf)
                {
                    GameObject bot = Instantiate(botsSpawner.WarriorBot_prefab, transform);
                    bot.GetComponent<Abilities_Warrior>().SetUp();
                    bots.Add(bot);
                    gridGenerator.blocksList[i].GetComponent<Block>().Spawn_Bot(this, levelManagerRef);
                }
            }
        }

        // Spawn Dangerous Enemy Bots (Bosses)
        for (int i = 0; i < gridGenerator.blocksList.Count; i++)
        {
            for (int j = 0; j < gridGenerator.blocksList[i].GetComponent<Block>().spawns_DangerousEnemy.Count; j++)
            {
                if (gridGenerator.blocksList[i].GetComponent<Block>().spawns_DangerousEnemy[j].activeSelf)
                {
                    GameObject bot = Instantiate(botsSpawner.BossBot_prefab, transform);
                    bot.GetComponent<Abilities_Warrior>().SetUp();
                    bots.Add(bot);
                    gridGenerator.blocksList[i].GetComponent<Block>().Spawn_Bot(this, levelManagerRef);
                }
            }
        }

        // Spawn Ally Bots
        for (int i = 0; i < gridGenerator.blocksList.Count; i++)
        {
            for (int j = 0; j < gridGenerator.blocksList[i].GetComponent<Block>().spawns_Ally.Count; j++)
            {
                if (gridGenerator.blocksList[i].GetComponent<Block>().spawns_Ally[j].activeSelf)
                {
                    GameObject bot = Instantiate(botsSpawner.AllyBot_prefab, transform);
                    bot.GetComponent<Abilities_Ally>().SetUp();
                    bots.Add(bot);
                    gridGenerator.blocksList[i].GetComponent<Block>().Spawn_Bot(this, levelManagerRef);
                }
            }
        }*/
        for (int i = 0; i < gridGenerator.blocksList.Count; i++)
        {
            gridGenerator.blocksList[i].GetComponent<Block>().Spawn_Bot(this, levelManagerRef);
        }

    }
}
