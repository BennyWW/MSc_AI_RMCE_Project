using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ProjectileDamage : MonoBehaviour
{
    [Header("Damage Properties")]
    public GameObject owner;
    public float damage = 5f;
    [SerializeField] GameObject hitEffect;
    public float hitEffectDestroyTime = 3f;
    public MeshRenderer meshRenderer;


    private void OnTriggerEnter(Collider other)
    {
        Debug.Log("ProjectileCollision");
        if (!other.isTrigger && other.gameObject.tag != gameObject.tag)
        {
            InflictDamage(other.gameObject);
            Debug.Log(other.gameObject.tag);
        }
    }

    void InflictDamage(GameObject victim)
    {
        if (victim != owner)
        {
            IDamageable victimDamageable = victim.GetComponent<IDamageable>();            
            if (victimDamageable != null)
            {
                victimDamageable.TakeDamage(damage);
            }

            Rigidbody rigidbody = GetComponent<Rigidbody>();
            if (rigidbody != null)
            {
                rigidbody.isKinematic = true;
            }
            SpawnHitEffect(transform.position);
            meshRenderer.enabled = false;
        }
    }

    void SpawnHitEffect(Vector3 hitPos)
    {
        if (hitEffect != null)
        {
            GameObject newhitEffect = Instantiate(hitEffect, hitPos, Quaternion.identity);
            Destroy(newhitEffect, hitEffectDestroyTime);
        }
    }
}
