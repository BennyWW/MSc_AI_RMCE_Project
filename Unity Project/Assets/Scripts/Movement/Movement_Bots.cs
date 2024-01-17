using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

public class Movement_Bots : MonoBehaviour
{
    [Header("NavMesh")]
    [SerializeField] public NavMeshAgent agent;

    [Header("Movement Variables")]
    public Vector3 targetPos = new();
    public float targetPosRadius = 10f; // Does not need to move to the exact position to avoid trying to go into a block (which will look weird)
    public float moveSpeed = 5f;
    public bool move;
    // Start is called before the first frame update
    void Start()
    {
        agent = GetComponent<NavMeshAgent>();
        targetPos = transform.position;
    }

    // Update is called once per frame
    void Update()
    {
        Movement();
    }

    #region Movement Script
    void Movement()
    {
        if (agent.isOnNavMesh)
        {
            agent.speed = moveSpeed;
            agent.SetDestination(targetPos);
            if (Vector3.Distance(transform.position, targetPos) <= targetPosRadius)
            {
                agent.isStopped = true;
            }
            else
            {
                agent.isStopped = false;
            }
        }

        #endregion
    }
}
