using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class KillScore : MonoBehaviour
{
    public enum Type
    {
        Ally,
        Enemy,
        Boss
    }
    [Header("Variables")]
    public LevelManager levelManagerRef;
    public int killScore;
    public Type type;

    public void AddToKillScore()
    {
        if (levelManagerRef)
        {
            if (type == Type.Enemy || type == Type.Ally)
            {
                levelManagerRef.killedEnemies += killScore;
            }
            else
            {
                levelManagerRef.killedBosses += killScore;
            }
        }
    }
}
