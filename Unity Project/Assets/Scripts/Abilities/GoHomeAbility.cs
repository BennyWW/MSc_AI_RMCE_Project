using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GoHomeAbility : MonoBehaviour
{
    [Header("Ability")]
    public string abilityName = "GoHome";
    public float coolDownTime = 10f;

    [Header("GoHome")]
    public string HomeTag = "AllyHome";
    public float checkHomeRange = 5f;
    public float arriveHomeRange = 2f;
    public float runToHomeSpeed = 5f;
    public GameObject home;
    public bool arrivedHome;

    public void GoHome()
    {
        if (home != null)
        {
            if (TryGetComponent<Movement_Bots>(out var movement_Bots))
            {
                movement_Bots.moveSpeed = runToHomeSpeed;
                movement_Bots.targetPos = home.transform.position;
            }
        }
    }

    public void CheckForHome() 
    {
        Collider[] farColliders = Physics.OverlapSphere(transform.position, checkHomeRange);
        Collider[] closeColliders = Physics.OverlapSphere(transform.position, arriveHomeRange);

        foreach (Collider collider in farColliders)
        {
            if (collider.gameObject.CompareTag(HomeTag))
            {
                home = collider.gameObject;
                break;
            }
            else
            {
                home = null;
            }
        }

        foreach (Collider collider in closeColliders)
        {
            if (collider.gameObject.CompareTag(HomeTag))
            {
                ArriveHome();
                break;
            }
        }
    }

    void ArriveHome()
    {
        arrivedHome = true;
        if (TryGetComponent<Movement_Bots>(out var movement))
        {
            movement.enabled = false;
        }
        Destroy(gameObject);
    }
}
