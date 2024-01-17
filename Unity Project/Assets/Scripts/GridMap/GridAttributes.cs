using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[CreateAssetMenu(fileName = "GridAttributes", menuName = "ScriptableObjects/GridAttributes")]
public class GridAttributes : ScriptableObject
{
    public Vector2 gridSize = new(8f, 9f);
    public float gapSize = 1f;
    public GameObject blockPrefab;
}
