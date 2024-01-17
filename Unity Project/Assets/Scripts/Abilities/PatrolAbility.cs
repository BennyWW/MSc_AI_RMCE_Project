using System.Collections;
using System.Collections.Generic;
using System.Diagnostics.Contracts;
using Unity.VisualScripting;
using UnityEngine;

public class PatrolAbility : MonoBehaviour
{
    [Header("Ability")]
    public string abilityName = "Patrol";
    public float coolDownTime = 10f;

    [Header("Patrol")]
    public Vector3 randomPos = new();
    public float patrolRadius = 20f;
    public float patrolSpeed = 2f;
    [SerializeField] bool patrolReady = true;    

    public void Patrol()
    {
        Movement_Bots movement_Bots = GetComponent<Movement_Bots>();
        if (movement_Bots)
        {
            movement_Bots.moveSpeed = patrolSpeed;
            if(Vector3.Distance(movement_Bots.targetPos,transform.position)<movement_Bots.targetPosRadius+0.1f)
                movement_Bots.targetPos = new Vector3(transform.position.x + Random.Range(-patrolRadius, patrolRadius),
                                                        transform.position.y,
                                                        transform.position.z + Random.Range(-patrolRadius, patrolRadius));
        }
    }
}
