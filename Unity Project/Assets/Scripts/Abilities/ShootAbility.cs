using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;

public class ShootAbility : MonoBehaviour
{
    [Header("Ability")]
    public string abilityName = "Shoot";
    public float coolDownTime = 2f;

    [Header("Shooting Parameters")]
    [SerializeField] GameObject bulletPrefab;
    public Transform shootingPoint;
    public Vector3 direction=new();
    [SerializeField] float projectileSpeed = 50f;
    public float projectileLifeSpan = 5f;
    public float projectileSizeMultiplier = 1f;

    public void Shoot()
    {
        shootingPoint.LookAt(direction);

        // Instantiate the BulletEffect VFX graph at the shooting point
        GameObject projectile = Instantiate(bulletPrefab, shootingPoint.position, shootingPoint.rotation);
        projectile.transform.localScale *= projectileSizeMultiplier;
        if (projectile.GetComponent<ProjectileDamage>())
        {
            projectile.GetComponent<ProjectileDamage>().owner = gameObject; // Assign owner
        }
        projectile.GetComponent<Rigidbody>().AddForce(projectile.transform.forward * projectileSpeed, ForceMode.Impulse);
        Destroy(projectile, projectileLifeSpan);
       
    }
}
