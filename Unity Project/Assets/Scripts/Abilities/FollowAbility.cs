using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FollowAbility : MonoBehaviour
{
    [Header("Ability")]
    public string abilityName = "Follow";
    public float coolDownTime = 5f;

    [Header("Follow")]
    public float followTime = 5f;
    public float followStartRange = 10f;
    public float followStopRange = 5f;
    public float followSpeed = 5f;
    public Transform target;
    public bool closeToTarget;
    [SerializeField] bool targetFound;

    public void Follow()
    {
        if (target != null)
        {
            if (TryGetComponent<Movement_Bots>(out var movement_Bots))
            {
                movement_Bots.moveSpeed = followSpeed;
                movement_Bots.targetPos = target.transform.position;
            }
        }
        else
        {
            if (TryGetComponent<Movement_Bots>(out var movement_Bots))
            {
                movement_Bots.moveSpeed = followSpeed;
                movement_Bots.targetPos = transform.position;
            }
        }
    }

    public void CheckForTarget()
    {
        Collider[] startRangeColliders = Physics.OverlapSphere(transform.position, followStartRange);
        Collider[] stopRangeColliders = Physics.OverlapSphere(transform.position, followStopRange);

        foreach (Collider collider in startRangeColliders)
        {
            if (collider.gameObject.GetComponent<IPlayer>() != null)
            {
                target = collider.transform;
                break;
            }
        }

        foreach (Collider collider in stopRangeColliders)
        {
            if(collider.gameObject.GetComponent<IPlayer>() != null)
            {
                target = null; 
                break; 
            }
        }
    }
}
