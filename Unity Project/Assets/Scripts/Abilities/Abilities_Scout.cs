using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Abilities_Scout : MonoBehaviour, IAbilities, IScout
{
    public bool dead = false;
    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {

    }

    public void AbilitiesCoolDown()
    {
        throw new System.NotImplementedException();
    }

    public void Animations()
    {
        throw new System.NotImplementedException();
    }

    public void RunAbilities()
    {
        throw new System.NotImplementedException();
    }

    public void SearchForPlayer()
    {
        throw new System.NotImplementedException();
    }

    public void Flee()
    {
        throw new System.NotImplementedException();
    }

    public void ReportPlayerLocation()
    {
        throw new System.NotImplementedException();
    }

    public void Die()
    {
        dead = true;
    }

    public void Die(bool isDead)
    {
        throw new System.NotImplementedException();
    }

    public void PickUp()
    {
        // No need to implement
    }
}
