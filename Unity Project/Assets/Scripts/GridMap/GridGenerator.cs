using System.Collections;
using System.Collections.Generic;
using System.Linq;
using TMPro;
using Unity.VisualScripting;
using UnityEngine;

/*
The grid will be a list that contains blocks. It could have a list for each row and a list to store the lists:
    gridRow :       [block, block, block,...]
    grid    :       [gridRow, gridRow, gridRow,...]
The the length of the rows will be determined by the grid attribute grid size X and length of the grid will be the grid size Y. 
The block will need to be separated by a gap and the consecutive lists should not start in the same position since the block are hexagonal:
   i.e      [- - - - - - - - - - - -]
             [- - - - - - - - - - - -]
            [- - - - - - - - - - - -]
             [- - - - - - - - - - - -]
            [- - - - - - - - - - - -]
             [- - - - - - - - - - - -]
            [- - - - - - - - - - - -]

 */
public class GridGenerator : MonoBehaviour
{
    [Header("Grid Features")]
    [SerializeField] GridAttributes gridAttributes;
    public List<List<GameObject>> grid = new();
    public List<GameObject> blocksList = new();

    [Header("Map Structure")]
    public GetMapStructure mapStructure;

    [Header("Map Statistsics")]
    public TMP_Text unlockObjs;
    public TMP_Text walls;
    public TMP_Text secrets_orbs;
    public TMP_Text trees;
    public TMP_Text interactableObjs;
    public TMP_Text grass;
    public TMP_Text centralHex;
    public TMP_Text allyHome;
    public TMP_Text spawns_Ally;
    public TMP_Text spawns_Enemy;
    public TMP_Text spawns_DangerousEnemy;

    int unlockObjsInt = 0;          int wallsInt = 0;           int secrets_orbsInt = 0;    int treesInt;
    int interactableObjsInt = 0;    int grassInt = 0;           int centralHexInt = 0;      int allyHomeInt;
    int spawns_AllyInt = 0;         int spawns_EnemyInt = 0;    int spawns_DangerousEnemyInt = 0;

    int unlockObjsInt_Max = 0; int wallsInt_Max = 0; int secrets_orbsInt_Max = 0; int treesInt_Max;
    int interactableObjsInt_Max = 0; int grassInt_Max = 0; int centralHexInt_Max = 0; int allyHomeInt_Max;
    int spawns_AllyInt_Max = 0; int spawns_EnemyInt_Max = 0; int spawns_DangerousEnemyInt_Max = 0;

    public void GenerateGrid(LevelManager levelManager)
    {
        // Create lists
        for (int i = 0; i < gridAttributes.gridSize.y; i++)
        {
            List<GameObject> gridRow = new();
            for (int j = 0; j < gridAttributes.gridSize.x; j++)
            {
                GameObject newBlock = Instantiate(gridAttributes.blockPrefab);
                if (newBlock.GetComponent<ExploreScore>())
                {
                    newBlock.GetComponent<ExploreScore>().levelManager = levelManager;
                }
                blocksList.Add(newBlock);
                newBlock.transform.parent = transform;  
                gridRow.Add(newBlock);
            }
            grid.Add(gridRow);
        }

        // Position the blocks and rows
        for (int i = 0; i < grid.Count; i++)
        {
            Vector3 startPos = transform.position;

            for (int j = 0; j < grid[i].Count; j++)
            {
                //Create gaps between the blocks
                if (j == 0)
                {
                    grid[i][j].transform.position = startPos;
                }
                else
                {
                    grid[i][j].transform.position = grid[i][j - 1].transform.position + new Vector3(gridAttributes.gapSize, 0f, 0f); // X axis
                }
            }

            if(i>0)
            {
                for (int j = 0; j < grid[i].Count; j++)
                {
                    //Create gaps between the blocks
                    if (j == 0)
                    {
                        grid[i][j].transform.position = grid[i-1][j].transform.position + new Vector3(0f,0f,gridAttributes.gapSize); // Z axis
                        if (i % 2 == 0)
                        {
                            grid[i][j].transform.position = grid[i - 1][j].transform.position + new Vector3(gridAttributes.gapSize/2, 0f, gridAttributes.gapSize); // X offset and Z axis
                        }
                        else
                        {
                            grid[i][j].transform.position = grid[i - 1][j].transform.position + new Vector3(-gridAttributes.gapSize / 2, 0f, gridAttributes.gapSize);
                        }
                    }
                    else
                    {                        
                        grid[i][j].transform.position = grid[i][j - 1].transform.position + new Vector3(gridAttributes.gapSize, 0f, 0f); // X axis                        
                    }
                }

            }
        }

    }

    public void DefineBlocks()
    {
        mapStructure.ExtractBlocks();
        if (mapStructure.MapStructure.Length > 0) { 
            for (int i = 0; i < mapStructure.MapStructure.Length; i++)
            {
                // Debug.Log(mapStructure.MapStructure[i]);
            }

            for (int i = 0; i < blocksList.Count; i++)
            {
                blocksList[i].GetComponent<IGA_Element>().DefineFeatures(mapStructure.MapStructure[i]);
                Debug.Log("block " + i);

                // Check map stats
                unlockObjsInt   += blocksList[i].GetComponent<Block>().unlockObjsInt.Sum();
                wallsInt        += blocksList[i].GetComponent<Block>().wallsInt.Sum();
                secrets_orbsInt += blocksList[i].GetComponent<Block>().secretsInt.Sum();
                treesInt        += blocksList[i].GetComponent<Block>().treesInt.Sum();
                interactableObjsInt += blocksList[i].GetComponent<Block>().interactableObjsInt.Sum();
                grassInt        += blocksList[i].GetComponent<Block>().grassInt.Sum();
                centralHexInt   += blocksList[i].GetComponent<Block>().centralHexInt.Sum();
                allyHomeInt     += blocksList[i].GetComponent<Block>().ally_HomeInt.Sum();
                spawns_AllyInt  += blocksList[i].GetComponent<Block>().spawns_AllyInt.Sum();
                spawns_EnemyInt += blocksList[i].GetComponent<Block>().spawns_EnemyInt.Sum();
                spawns_DangerousEnemyInt += blocksList[i].GetComponent<Block>().spawns_DangerousEnemyInt.Sum();

                unlockObjsInt_Max   += blocksList[i].GetComponent<Block>().unlockObjs.Count;
                wallsInt_Max        += blocksList[i].GetComponent<Block>().walls.Count;
                secrets_orbsInt_Max += blocksList[i].GetComponent<Block>().secrets.Count;
                treesInt_Max        += blocksList[i].GetComponent<Block>().trees.Count;
                interactableObjsInt_Max += blocksList[i].GetComponent<Block>().interactableObjs.Count;
                grassInt_Max        += blocksList[i].GetComponent<Block>().grass.Count;
                centralHexInt_Max   += blocksList[i].GetComponent<Block>().centralHex.Count;
                allyHomeInt_Max     += blocksList[i].GetComponent<Block>().ally_Home.Count;
                spawns_AllyInt_Max  += blocksList[i].GetComponent<Block>().spawns_Ally.Count;
                spawns_EnemyInt_Max += blocksList[i].GetComponent<Block>().spawns_Enemy.Count;
                spawns_DangerousEnemyInt_Max += blocksList[i].GetComponent<Block>().spawns_DangerousEnemy.Count;
            }

            // Update TMP texts
            unlockObjs.text     = unlockObjsInt.ToString() + " / " + unlockObjsInt_Max;
            walls.text          = wallsInt.ToString() + " / " + wallsInt_Max;
            secrets_orbs.text   = secrets_orbsInt.ToString() + " / " + secrets_orbsInt_Max;
            trees.text          = treesInt.ToString() + " / " + treesInt_Max;
            interactableObjs.text = interactableObjsInt.ToString() + " / " + interactableObjsInt_Max;
            grass.text          = grassInt.ToString() + " / " + grassInt_Max;
            centralHex.text     = centralHexInt.ToString() + " / " + centralHexInt_Max;
            allyHome.text       = allyHomeInt.ToString() + " / " + allyHomeInt_Max;
            spawns_Ally.text    = spawns_AllyInt.ToString() + " / " + spawns_AllyInt_Max;
            spawns_Enemy.text   = spawns_EnemyInt.ToString() + " / " + spawns_EnemyInt_Max;
            spawns_DangerousEnemy.text = spawns_DangerousEnemyInt.ToString() + " / " + spawns_DangerousEnemyInt_Max;
        }
        else
        {
            Debug.Log("Map Structure Empty");
        }
    }

    #region Testing (Delete after use)
    public void ModifyBlocks()
    {
        foreach(var blocks in grid)
        {
            foreach(var block in blocks)
            {
                string structure = "";
                block.gameObject.GetComponent<IGA_Element>().DefineFeatures(structure);
            }
        }
    }
    #endregion
}
