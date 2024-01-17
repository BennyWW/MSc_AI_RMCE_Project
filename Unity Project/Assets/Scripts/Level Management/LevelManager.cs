using System.Collections;
using System.Collections.Generic;
using TMPro;
using Unity.AI.Navigation;
using UnityEngine;
using UnityEngine.UI;

public class LevelManager : MonoBehaviour
{
    public GameObject playerRef;

    [Header("Level Management")]
    public bool generateGrid = true;
    public bool spawnBots = true;
    public GridGenerator gridGenerator;
    public Spawner_Bots spawner_bots;

    [Header("Object Management")]
    public bool disableFarObjects = true;
    public float distanceFromPlayer = 100f;

    [Header("Objectives Management")]
    public Slider O_Upgrades;
    public Slider C_KillEnemies;
    public Slider E_KillBosses;
    public Slider A_SaveAllies;
    public Slider N_Explore;

    public int killedEnemies;
    public int killedBosses;
    public int savedAllies;
    public int blocksExplored;

    [Header("Scoreboard Management")]
    public Transform OffScreenPos;
    public Transform InScreenPos;
    public Transform scoreBoard;
    public TMP_Text O_Score;
    public TMP_Text C_Score;
    public TMP_Text E_Score;
    public TMP_Text A_Score;
    public TMP_Text N_Score;

    [Header("Upgrades Management")]
    public int DashLevel;
    public int ShootLevel;
    public int AreaMarkLevel;

    public TMP_Text dashLvl_Txt;
    public TMP_Text shootLvl_Txt;
    public TMP_Text areaMarkLvl_Txt;

    public int lvlDeterminerDivider; //e.g. if score = 50, level could be 50/10=5 or 50/20=2 (int of 2.5)

    [Header("Bots Navmesh")]
    public NavMeshSurface floor;

    /*
     Order of operations:
        - Generate grid
        - Spawn bots
     */

    private void Awake()
    {
        Scoreboard(false);

        if (generateGrid)
        {
            // Generate grid
            gridGenerator.GenerateGrid(this);
            gridGenerator.DefineBlocks();
            //gridGenerator.ModifyBlocks();
        }

        if (spawnBots)
        {
            // Spawn bots
            //spawner_bots.SpawnBots();
            spawner_bots.AddBots(this);
        }

        // Build NavMesh Surface
        BuildNavMeshSurface();

    }

    private void LateUpdate()
    {
        ManageObjects();
        ManageObjectivesScores();
        DeathScreen();
    }

    void ManageObjects()
    {
        if (disableFarObjects && playerRef.transform != null)
        {
            foreach (GameObject block in gridGenerator.blocksList)
            {
                if (block != null)
                {
                    if (Vector3.Distance(block.transform.position, playerRef.transform.position) > distanceFromPlayer)
                    {
                        block.SetActive(false);
                    }
                    else
                    {
                        block.SetActive(true);
                    }
                }
                else
                {
                    gridGenerator.blocksList.Remove(block);
                }
            }

            foreach (GameObject bot in spawner_bots.bots)
            {
                if (bot != null)
                {
                    if (Vector3.Distance(bot.transform.position, playerRef.transform.position) > distanceFromPlayer)
                    {
                        bot.SetActive(false);
                    }
                    else
                    {
                        bot.SetActive(true);
                    }
                }
                else
                {
                    // spawner_bots.bots.Remove(bot);
                    //bot.SetActive(false );
                }
            }
        }
    }

    void ManageObjectivesScores()
    {
        // calculate objectives
        if(playerRef.GetComponent<Abilities_Player>() != null)
        {
            Abilities_Player playerAbilities = playerRef.GetComponent<Abilities_Player>();
            O_Upgrades.value    = playerAbilities.pickUp_Dash + playerAbilities.pickUp_AreaMark + playerAbilities.pickUp_Shoot;
            C_KillEnemies.value = killedEnemies;
            E_KillBosses.value  = killedBosses;
            A_SaveAllies.value  = playerAbilities.pickUp_SecretOrbs + savedAllies;
            N_Explore.value     = blocksExplored;

            DashLevel       =(int)(playerAbilities.pickUp_Dash/ lvlDeterminerDivider)       + 1;
            ShootLevel      =(int)(playerAbilities.pickUp_Shoot/ lvlDeterminerDivider)      + 1;
            AreaMarkLevel   =(int)(playerAbilities.pickUp_AreaMark/ lvlDeterminerDivider)   + 1;

            dashLvl_Txt.text        = DashLevel.ToString();
            shootLvl_Txt.text       = ShootLevel.ToString();
            areaMarkLvl_Txt.text    = AreaMarkLevel.ToString();

            //Scores
            O_Score.text = O_Upgrades.value.ToString();
            C_Score.text = C_KillEnemies.value.ToString();
            E_Score.text = E_KillBosses.value.ToString();
            A_Score.text = A_SaveAllies.value.ToString();
            N_Score.text = N_Explore.value.ToString();
        }
    }

    void DeathScreen()
    {
        if (playerRef.GetComponent<Abilities_Player>() != null)
        {
            Abilities_Player playerAbilities = playerRef.GetComponent<Abilities_Player>();
            if (playerAbilities.dead)
            {
                if (GetComponent<DeathScreen>())
                {
                    Scoreboard(true);
                    GetComponent<DeathScreen>().ShowDeathScreen(playerAbilities);
                }
            }
        }
    }

    public void Scoreboard(bool show)
    {
        //Show Score board
        if (scoreBoard)
        {
            if (show)
            {
                scoreBoard.position = InScreenPos.position;
            }
            else
            {
                scoreBoard.position = OffScreenPos.position;
            }
        }
    }

    void BuildNavMeshSurface()
    {
        if(floor)
            floor.BuildNavMesh();
    }
}
