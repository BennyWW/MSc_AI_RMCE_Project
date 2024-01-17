using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

public class Abilities_Warrior : MonoBehaviour, IWarrior, IAbilities
{
    public LevelManager levelManager;

    public Animator animator;

    Movement_Bots movement_Bots;

    public bool dead = false;
    PatrolAbility patrolAbility;
    [SerializeField] bool patrolReady = true; 
    ChaseAbility chaseAbility;
    //[SerializeField] bool chaseReady = false;
    AttackAbility attackAbility;
    [SerializeField] bool attackReady = false;
    IdleAbility idleAbility;
    [SerializeField] Dictionary<string, float> abilitiesDict = new();
    [SerializeField] List<string> abilitiesList = new();
    [SerializeField] string activeAbility;

    [SerializeField] bool addedKillScore;

    public bool patrolAnimBool;

    public bool setUpOnStart;

    private void Start()
    {
        if(setUpOnStart)
            SetUp();
    }

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
        if(animator == null)
            animator = GetComponent<Animator>();

        // Load abilities
        if (TryGetComponent<PatrolAbility>(out patrolAbility))
        {
            patrolAbility = GetComponent<PatrolAbility>();
            abilitiesDict.Add(patrolAbility.abilityName, patrolAbility.coolDownTime);
            abilitiesList.Add(patrolAbility.abilityName);
        }
        if (TryGetComponent<IdleAbility>(out idleAbility))
        {
            idleAbility = GetComponent<IdleAbility>();
            abilitiesDict.Add(idleAbility.abilityName, idleAbility.coolDownTime);
            abilitiesList.Add(idleAbility.abilityName);
        }
        if (TryGetComponent<ChaseAbility>(out chaseAbility))
        {
            chaseAbility = GetComponent<ChaseAbility>();
            abilitiesDict.Add(chaseAbility.abilityName, chaseAbility.coolDownTime);
            abilitiesList.Add(chaseAbility.abilityName);
        }
        if (TryGetComponent<AttackAbility>(out attackAbility))
        {
            attackAbility = GetComponent<AttackAbility>();
            abilitiesDict.Add(attackAbility.abilityName, attackAbility.coolDownTime);
            abilitiesList.Add(attackAbility.abilityName);
        }
    }

    public void RunAbilities()
    {
        if (dead) return;
     
        Patrol();
        Idle();
        Chase();
        Attack();   
    }

    public void Patrol()
    {
        if(patrolAbility && patrolReady)
        {
            activeAbility = patrolAbility.abilityName;
            patrolAbility.Patrol();
            abilitiesDict[patrolAbility.abilityName] = patrolAbility.coolDownTime;
        }

        if (chaseAbility)
        {
            if (chaseAbility.target == null)
            {
                activeAbility = patrolAbility.abilityName;
                patrolAbility.Patrol();
                abilitiesDict[patrolAbility.abilityName] = patrolAbility.coolDownTime;
            }
        }
    }

    public void Idle()
    {
        if(GetComponent<NavMeshAgent>().isOnNavMesh)
            if (idleAbility && (Vector3.Distance(transform.position,movement_Bots.targetPos) <= movement_Bots.targetPosRadius+0.2f || GetComponent<NavMeshAgent>().remainingDistance<0.1f))
            {
                if(idleAbility)
                    activeAbility = idleAbility.abilityName;
            }
    }

    public void Chase()
    {
        if (chaseAbility)
        {
            chaseAbility.CheckForTarget();

            if (chaseAbility.target != null)
            {
                activeAbility = chaseAbility.abilityName;
                chaseAbility.Chase();
                abilitiesDict[chaseAbility.abilityName] = chaseAbility.coolDownTime;
            }
        }
    }

    public void Attack()
    {
        if(attackAbility)
        {
            attackAbility.CheckForTarget();
            if (attackAbility.target != null)
            {
                activeAbility = attackAbility.abilityName;
                attackAbility.shootReady = attackReady;
                attackAbility.Attack();
                if (attackReady)
                {
                    attackAbility.Shoot();
                    abilitiesDict[attackAbility.abilityName] = attackAbility.coolDownTime;
                }
            }
        }
    }

    public void Die(bool isDead)
    {        
        Animator animator = GetComponent<Animator>();
        dead = isDead;

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


        if (isDead == true)
        {
            if (GetComponent<KillScore>() && !addedKillScore)
            {
                GetComponent<KillScore>().AddToKillScore();
                addedKillScore = true;
            }
            animator.Play("Death", 0); 
            Destroy(gameObject, 10f);
        }
        else
        {
            animator.Play("Idle", 0);
        }       
    }


    public void AbilitiesCoolDown()
    {
        foreach (string abilityName in abilitiesList)
        {
            if (abilitiesDict.ContainsKey(abilityName))
                if (abilitiesDict[abilityName] > 0)
                {
                    abilitiesDict[abilityName] -= Time.deltaTime;
                }
        }

        if(patrolAbility)
            patrolReady = abilitiesDict[patrolAbility.abilityName] <= 0;
        if(attackAbility)
            attackReady = abilitiesDict[attackAbility.abilityName] <= 0;
    }

    public void PickUp()
    {
        // No need to implement
    }

    public void Animations()
    {
        if (animator)
        {
            if(patrolAbility)
                animator.SetBool(patrolAbility.abilityName, activeAbility == patrolAbility.abilityName);
            if(idleAbility)
                animator.SetBool(idleAbility.abilityName, activeAbility == idleAbility.abilityName);
            if(chaseAbility)
                animator.SetBool(chaseAbility.abilityName, activeAbility == chaseAbility.abilityName);
            if (attackAbility)
                animator.SetBool(attackAbility.abilityName, activeAbility == attackAbility.abilityName);
        }
    }
}
