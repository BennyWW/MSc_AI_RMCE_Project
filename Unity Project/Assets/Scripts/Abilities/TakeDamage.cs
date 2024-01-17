using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;
using UnityEngine.AI;
using Unity.VisualScripting;

public class TakeDamage : MonoBehaviour, IDamageable
{
    [Header("Damage Variables")]
    public float health = 100f;
    public float maxHealth = 100f;
    public float healAmount = 5f;
    public bool dead = false;

    [Header("UI")]
    [SerializeField] TMP_Text healthTxt;
    [SerializeField] Slider healthSlider;

    private void Update()
    {
        CheckDamage();
    }


    public void CheckDamage()
    {
        if (healthTxt)
        {
            healthTxt.text = ((int)health).ToString();
            healthSlider.value = health / maxHealth;
        }
        Heal();
        Die();
    }

    public void Die()
    {
        if (health < 1)
        {
            dead = true;
            IAbilities abilities = GetComponent<IAbilities>();
            if (abilities != null)
            {
                abilities.Die(true);
            }
        }
    }

    public void Heal()
    {
        if (!dead)
        {
            // Increase the heal value by healRate multiplied by Time.deltaTime
            health += healAmount * Time.deltaTime;

            // Ensure the heal value doesn't exceed the maxHealValue
            health = Mathf.Clamp(health, 0f, maxHealth);
        }
    }

    void IDamageable.TakeDamage(float damage)
    {
        if (health > 0)
        {
            health -= damage;
            if(health<0f)
                health = 0f;
        }
    }

 
}
