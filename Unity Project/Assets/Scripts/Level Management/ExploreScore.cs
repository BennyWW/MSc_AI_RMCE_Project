using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ExploreScore : MonoBehaviour
{
    [Header("Variables")]
    public int exploreScoreAdd = 4;
    public LevelManager levelManager;
    bool explored;

    private void OnTriggerEnter(Collider other)
    {
        if(other.GetComponent<IPlayer>() != null)
        {
            if (levelManager)
            {
                if (!explored)
                {
                    levelManager.blocksExplored += exploreScoreAdd;
                    explored = true;
                }
            }
        }
    }

}
