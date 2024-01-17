using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class UpgradeAbilities : MonoBehaviour
{
    [Header("Variables")]
    public LevelManager levelManagerRef;
    public float shootCoolDown_Multiplier = 0.75f;
    public float projectileSize_Multiplier = .25f;
    public float dashSpeed_Multipier = 1f;
    public float dashCool_Multipier = 0.75f;
    public float areaMarkSize_Multipier = 1f;
    public float areaMarkCoolDown_Multipier = 0.75f;

    [Header("Ability Defaults")]
    public float shootCooldown;
    public float dashCooldown;
    public float dashSpeed;
    public float areaMarkCooldown;

    [Header("Ability Levels Ref")]
    [SerializeField] int DashLevel;
    [SerializeField] int ShootLevel;
    [SerializeField] int AreaMarkLevel;

    public void Upgrades()
    {
        if(levelManagerRef)
        {
            DashLevel       = levelManagerRef.DashLevel;
            ShootLevel      = levelManagerRef.ShootLevel;
            AreaMarkLevel   = levelManagerRef.AreaMarkLevel;

            if(GetComponent<ShootAbility>()) 
            {
                GetComponent<ShootAbility>().coolDownTime = shootCooldown - levelManagerRef.ShootLevel * shootCoolDown_Multiplier; 
                //GetComponent<ShootAbility>().projectileSizeMultiplier = levelManagerRef.ShootLevel * projectileSize_Multiplier; 
            }
            if (GetComponent<DashAbility>())
            {
                GetComponent<DashAbility>().coolDownTime = dashCooldown + levelManagerRef.DashLevel * dashCool_Multipier;
                GetComponent<DashAbility>().speed = dashSpeed + levelManagerRef.DashLevel * dashSpeed_Multipier;
            }
            if (GetComponent<MarkAreaAbility>())
            {
                GetComponent<MarkAreaAbility>().coolDownTime = areaMarkCooldown + levelManagerRef.AreaMarkLevel * areaMarkCoolDown_Multipier;
                GetComponent<MarkAreaAbility>().sizeMultiplier = levelManagerRef.AreaMarkLevel * areaMarkCoolDown_Multipier;
            }
        }
    }
}
