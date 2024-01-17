using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AttackAbility : MonoBehaviour
{
    [Header("Ability")]
    public string abilityName = "Attack";
    public float coolDownTime = 5f;

    [Header("Attack")]
    public Transform target;
    public float attackRadius = 2f;
    public bool shootReady;

    [Header("Shooting")]
    public Transform shootingPoint;

    public void Attack()
    {
        if (target != null && Vector3.Distance(target.position, transform.position) < attackRadius)
        {
            Movement_Bots movement_Bots = GetComponent<Movement_Bots>();
            if (movement_Bots != null)
            {
                movement_Bots.targetPos = transform.position;
                transform.LookAt(new Vector3(target.position.x, transform.position.y, target.position.z));                
            }
        }
        else
        {
            target = null;
        }

    }

    public void Shoot()
    {
        ShootAbility shootAbility = GetComponent<ShootAbility>();

        if (shootAbility != null && shootReady)
        {
            shootAbility.shootingPoint = shootingPoint;
            // Initialize shoot direction
            if (target != null)
            {
                shootAbility.direction = new Vector3(target.position.x, shootAbility.shootingPoint.position.y, target.position.z);
                shootAbility.Shoot();
            }
        }
    }

    public void CheckForTarget()
    {
        Collider[] colliders = Physics.OverlapSphere(transform.position, attackRadius);

        foreach (Collider collider in colliders)
        {
            // Do something with the colliders found within the radius
            if (collider.gameObject.GetComponent<IPlayer>() != null)
            {
                target = collider.transform;
                break;
            }
        }

        if (target != null)
        {
            if (Vector3.Distance(target.position, transform.position) > attackRadius + 0.01f)
                target = null;
        }

    }
}
