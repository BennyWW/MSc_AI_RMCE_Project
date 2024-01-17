using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

public class Abilities_Ally : MonoBehaviour, IAbilities, IAlly
{
    public LevelManager levelManager;
    
    Animator animator;

    Movement_Bots movement_Bots;

    public bool dead = false;
    FollowAbility followAbility;
    [SerializeField] bool followReady = false;
    GoHomeAbility goHomeAbility;
    [SerializeField] bool goHomeReady = false;
    bool saved;
    [SerializeField] int savedPointAdd = 2;
    IdleAbility idleAbility;
    [SerializeField] Dictionary<string, float> abilitiesDict = new();
    [SerializeField] List<string> abilitiesList = new();
    [SerializeField] string activeAbility;

    // Update is called once per frame
    void Update()
    {
        AbilitiesCoolDown();
        RunAbilities();
        Animations();
    }

    public void SetUp()
    {
        movement_Bots = GetComponent<Movement_Bots>();
        animator = GetComponent<Animator>();

        // Load abilities
        if (TryGetComponent<IdleAbility>(out idleAbility))
        {
            idleAbility = GetComponent<IdleAbility>();
            abilitiesDict.Add(idleAbility.abilityName, idleAbility.coolDownTime);
            abilitiesList.Add(idleAbility.abilityName);
        }
        if (TryGetComponent<FollowAbility>(out followAbility))
        {
            followAbility = GetComponent<FollowAbility>();
            abilitiesDict.Add(followAbility.abilityName, followAbility.coolDownTime);
            abilitiesList.Add(followAbility.abilityName);
        }
        if (TryGetComponent<GoHomeAbility>(out goHomeAbility))
        {
            goHomeAbility = GetComponent<GoHomeAbility>();
            abilitiesDict.Add(goHomeAbility.abilityName, goHomeAbility.coolDownTime);
            abilitiesList.Add(goHomeAbility.abilityName);
        }
    }
    public void AbilitiesCoolDown()
    {
        foreach (string abilityName in abilitiesList)
        {
            if (abilitiesDict[abilityName] > 0)
            {
                abilitiesDict[abilityName] -= Time.deltaTime;
            }
        }
        if (followAbility)
            followReady = abilitiesDict[followAbility.abilityName] <= 0;
    }


    public void Die(bool isDead)
    {
        Animator animator = GetComponent<Animator>();
        dead = isDead;

        if (isDead == true)
        {
            animator.Play("Death", 0);
        }
        else
        {
            animator.Play("Idle", 0);
        }

        Movement_Bots movement_bots = GetComponent<Movement_Bots>();
        if (movement_bots)
        {
            movement_bots.enabled = !isDead;
            NavMeshAgent agent = GetComponent<NavMeshAgent>();
            if (agent)
                agent.enabled = !isDead;
        }

        CapsuleCollider collider = GetComponent<CapsuleCollider>();
        if (collider)
            collider.enabled = !isDead;

        if (isDead)
        {
            Destroy(gameObject,10f);
        }
    }

    public void RunAbilities()
    {
        if (dead) return;

        Idle();
        FollowPlayer();   
        GoHome();
    }

    public void FollowPlayer()
    {
        if (followAbility)
        {
            followAbility.CheckForTarget();

            if(followAbility.target!=null)
            {
                activeAbility = followAbility.abilityName;
                followAbility.Follow();
                abilitiesDict[followAbility.abilityName] = followAbility.coolDownTime;
            }
        }
    }

    public void Idle()
    {
        if (idleAbility)
        {
            if (followAbility)
            {
                followAbility.CheckForTarget();

                if (followAbility.target == null)
                {
                    activeAbility = idleAbility.abilityName;
                    movement_Bots.targetPos = transform.position;
                }
            }
        }
    }

    public void GoHome()
    {
        if(goHomeAbility)
        {
            goHomeAbility.CheckForHome();

            if (goHomeAbility.home != null)
            {
                goHomeAbility.GoHome();
                activeAbility = goHomeAbility.abilityName;
                abilitiesDict[goHomeAbility.abilityName] = goHomeAbility.coolDownTime;
                if (levelManager)
                {
                    if (!saved)
                    {
                        levelManager.savedAllies += 1;
                        saved = true;
                    }
                }
            }
        }
    }

    public void PickUp()
    {
        // No need to implement
    }

    public void Animations()
    {
        if (animator)
        {
            if (idleAbility)
                animator.SetBool(idleAbility.abilityName, activeAbility == idleAbility.abilityName);
            if (followAbility)
                animator.SetBool(followAbility.abilityName, activeAbility == followAbility.abilityName);
            if (goHomeAbility)
                animator.SetBool(goHomeAbility.abilityName, activeAbility == goHomeAbility.abilityName);
        }
    }
}
