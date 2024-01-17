using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PickUp : MonoBehaviour
{
    public enum Type
    {
        secret_orb,
        dash,
        shoot,
        areaMark
    }

    [Header("Variables")]
    public Type type;
    public int amountAdd;

    private void OnTriggerEnter(Collider other)
    {
        if(other.GetComponent<IPlayer>() != null)
        {
            if(other.GetComponent<Abilities_Player>())
                AddAmount(other.GetComponent<Abilities_Player>());
        }
    }

    void AddAmount(Abilities_Player player)
    {
        if(type == Type.secret_orb )
        {
            player.pickUp_SecretOrbs += amountAdd;
        }
        if (type == Type.dash)
        {
            player.pickUp_Dash += amountAdd;
        }
        if (type == Type.shoot)
        {
            player.pickUp_Shoot += amountAdd;
        }
        if (type == Type.areaMark)
        {
            player.pickUp_AreaMark += amountAdd;
        }
        gameObject.SetActive(false);
    }
}
