using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.InputSystem.HID;

public class ChaseAbility : MonoBehaviour
{
    [Header("Ability")]
    public string abilityName = "Chase";
    public float coolDownTime = 5f;

    [Header("Chase")]
    public float chaseTime = 5f;
    public float chaseStartRange = 10f;
    public float chaseStopRange = 5f;
    public float chaseSpeed = 5f;
    public Transform target;
    public bool closeToTarget;
    [SerializeField] bool targetFound;

    public void Chase()
    {
        if (target != null && Vector3.Distance(target.position, transform.position)-chaseStopRange < chaseStartRange 
            && Vector3.Distance(target.position, transform.position) > chaseStopRange) {
            Movement_Bots movement_Bots = GetComponent<Movement_Bots>();
            if (movement_Bots != null)
            {
                movement_Bots.moveSpeed = chaseSpeed;
                movement_Bots.targetPos = target.transform.position;
            }
        }
        else
        {
            target = null;
        }

        if(target!=null)
            closeToTarget = Vector3.Distance(target.position, transform.position) < chaseStopRange;
    }

    public void CheckForTarget()
    {
        Collider[] colliders = Physics.OverlapSphere(transform.position, chaseStartRange);

        foreach (Collider collider in colliders)
        {
            if (collider.gameObject.GetComponent<IPlayer>()!=null)
            {
                target=collider.transform; 
                break;
            }
        }

        if (target != null)
        {
            if(Vector3.Distance(target.position, transform.position) > chaseStartRange + 0.01f)
                target = null;
        }

    }
}
