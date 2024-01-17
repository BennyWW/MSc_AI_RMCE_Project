using System.Collections;
using System.Collections.Generic;
using System.ComponentModel;
using TMPro;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.AI;
using UnityEngine.InputSystem;
using UnityEngine.UI;

public class Abilities_Player : MonoBehaviour, IPlayer, IAbilities
{
    PlayerInput playerInput;
    InputAction dashAction;
    InputAction shootAction;
    InputAction markAreaAction;

    // Abilities
    [Header("Dash Ability")]
    DashAbility dashAbility; 
    [SerializeField] bool dashReady=true;
    public Slider dashSlider;

    [Header("Dash Ability")]
    ShootAbility shootAbility; 
    [SerializeField] bool shootReady=true;
    public Slider shootSlider;

    [Header("Dash Ability")]
    MarkAreaAbility markAreaAbility;
    [SerializeField] bool markAreaReady = true;
    public Slider markAreaSlider;

    [Header("Pick Up Ability")]
    public int pickUp_Shoot;
    public int pickUp_Dash;
    public int pickUp_AreaMark;
    public int pickUp_SecretOrbs;

    [Header("Abilities Management")]
    [SerializeField] Dictionary<string, float> abilitiesDict = new();
    [SerializeField] List<string> abilitiesList = new();
    public bool dead = false;

    // Animations
    Animator animator;

    MouseRaycast mouseRaycast;
    CharacterController characterController;
    
    // Start is called before the first frame update
    void Start()
    {
        playerInput = GetComponent<PlayerInput>();
        dashAction = playerInput.actions["Dash"];
        shootAction = playerInput.actions["Shoot"];
        markAreaAction = playerInput.actions["MarkArea"];

        characterController = GetComponent<CharacterController>();

        // Assign default params for the abilities
        UpgradeAbilities upgrades = GetComponent<UpgradeAbilities>();

        // Load abilities
        if (TryGetComponent<DashAbility>(out dashAbility) && TryGetComponent<MouseRaycast>(out mouseRaycast))
        {
            dashAbility = GetComponent<DashAbility>();
            mouseRaycast = GetComponent<MouseRaycast>();
            abilitiesDict.Add(dashAbility.abilityName, dashAbility.coolDownTime);
            abilitiesList.Add(dashAbility.abilityName);
            if (upgrades != null)
            {
                upgrades.dashCooldown = dashAbility.coolDownTime;
                upgrades.dashSpeed = dashAbility.speed;
            }
        }
        if (TryGetComponent<ShootAbility>(out shootAbility) && TryGetComponent<MouseRaycast>(out mouseRaycast))
        {
            shootAbility = GetComponent<ShootAbility>();
            abilitiesDict.Add(shootAbility.abilityName, shootAbility.coolDownTime);
            abilitiesList.Add(shootAbility.abilityName);
            if (upgrades != null)
            {
                upgrades.shootCooldown = shootAbility.coolDownTime;
                //upgrades.projectileSize_Multiplier = shootAbility.projectileSizeMultiplier;
            }
        }
        if (TryGetComponent<MarkAreaAbility>(out markAreaAbility))
        {
            markAreaAbility = GetComponent<MarkAreaAbility>();
            abilitiesDict.Add(markAreaAbility.abilityName, markAreaAbility.coolDownTime);
            abilitiesList.Add(markAreaAbility.abilityName);
            if (upgrades != null)
            {
                upgrades.areaMarkCooldown = markAreaAbility.coolDownTime;
                upgrades.areaMarkSize_Multipier = markAreaAbility.sizeMultiplier;
            }
        }

        animator = GetComponent<Animator>();
    }

    // Update is called once per frame
    void Update()
    {
        AbilitiesCoolDown();
        RunAbilities();
        ManageUpgrades();
        Animations();
    }
    #region Abilities
    public void RunAbilities()
    {
        if(dead) return;

        // Dashing
        if (dashReady)
        {
            if (dashAction.IsPressed())
            {
                Dash();
            }
        }

        // Shooting
        if (shootReady)
        {
            if (shootAction.IsPressed())
            {
                Shoot();
            }
        }

        // Marking Area
        if (markAreaReady)
        {
            if (markAreaAction.IsPressed())
            {
                MarkArea();
            }
        }
    }
    public void Dash()
    {
        //Check if ability present
        if (TryGetComponent<DashAbility>(out dashAbility) && TryGetComponent<MouseRaycast>(out mouseRaycast))
        {
            // Initialize direction
            Vector3 newPos = transform.position - mouseRaycast.GetMousePos();
            dashAbility.direction = new Vector3(-newPos.x, 0f, -newPos.z);
            dashAbility.Dash(GetComponent<Movement_Player>().enabled, characterController);
            abilitiesDict[dashAbility.abilityName] = dashAbility.coolDownTime;
            dashSlider.value = 0f;
        }
    }

    public void Shoot()
    {
        if(TryGetComponent<ShootAbility>(out shootAbility) && TryGetComponent<MouseRaycast>(out mouseRaycast))
        {
            // Initialize shoot direction
            shootAbility.direction = new Vector3(mouseRaycast.GetMousePos().x,shootAbility.shootingPoint.position.y,mouseRaycast.GetMousePos().z);
            shootAbility.Shoot();
            abilitiesDict[shootAbility.abilityName] = shootAbility.coolDownTime;
            shootSlider.value = 0f;
        }
    }

    public void MarkArea()
    {
        if(TryGetComponent<MarkAreaAbility>(out markAreaAbility))
        {
            markAreaAbility.MarkArea();
            abilitiesDict[markAreaAbility.abilityName] = markAreaAbility.coolDownTime;
            markAreaSlider.value = 0f;
        }
    }

    public void AbilitiesCoolDown()
    {
        foreach(string abilityName in abilitiesList)
        {
            if(abilitiesDict.ContainsKey(abilityName))
                abilitiesDict[abilityName] -= Time.deltaTime;
        }

        dashReady   =    abilitiesDict[dashAbility.abilityName] <= 0;
        dashSlider.value -= abilitiesDict[dashAbility.abilityName];
        if (dashReady)
        {
            dashSlider.value = Mathf.Lerp(dashSlider.value, dashSlider.maxValue, 1f);
        }

        shootReady  =    abilitiesDict[shootAbility.abilityName] <= 0;
        shootSlider.value -= abilitiesDict[shootAbility.abilityName];
        if (shootReady)
        {
            shootSlider.value = Mathf.Lerp(shootSlider.value, shootSlider.maxValue, 1f);
        }

        markAreaReady = abilitiesDict[markAreaAbility.abilityName] <= 0;
        markAreaSlider.value -= abilitiesDict[markAreaAbility.abilityName];
        if (markAreaReady)
        {
            markAreaSlider.value = Mathf.Lerp(markAreaSlider.value, markAreaSlider.maxValue, 1f);
        }

    }

    public void Die(bool isDead)
    {
        Animator animator = GetComponent<Animator>();
        dead = isDead;
        if (isDead == true) 
        { 
            if(animator)
                animator.Play("Death", 0);
        }
        else
        {
            if(animator)
                animator.Play("Idle", 0);
        }

        Movement_Player movement_Player = GetComponent<Movement_Player>();
        if (movement_Player)
        {
            movement_Player.enabled = !isDead;
        }

        CapsuleCollider collider = GetComponent<CapsuleCollider>();
        if (collider)
            collider.enabled = !isDead;
    }

    void ManageUpgrades()
    {
        if (GetComponent<UpgradeAbilities>())
        {
            GetComponent<UpgradeAbilities>().Upgrades();
        }
    }

    public void PickUp()
    {
        
    }

    public void Animations()
    {
        // No implementation needed
    }

    #endregion
}
