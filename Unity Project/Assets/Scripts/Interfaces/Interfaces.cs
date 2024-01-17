using System;
using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;

#region Functions for the GA Algorithm
// Functions to aid in generating a map with the genetic algorithm. 
public interface IGA_Element
{
    float DetermineScore();
    void DefineFeatures(string structure);

}
#endregion

#region Functions for gameplay
public interface IDamageable
{
    void TakeDamage(float damage);
    void Die();
    void Heal();
}
public interface IScout
{
    void SearchForPlayer(); // Search for player
    void Flee(); // Run away when close to a fight
    void ReportPlayerLocation(); // Scout finds player and run to closest warriors to report
}
public interface IWarrior
{
    void Chase(); // Run after player/suspected area
    void Patrol(); // Patrol an area
    void Attack(); // Attack player
    void Idle();
    void SetUp();
    void RunAbilities();
    void AbilitiesCoolDown();
}

public interface IAlly
{
    void FollowPlayer();
    void Idle();
    void SetUp();
    void RunAbilities();
    void AbilitiesCoolDown();
    void GoHome();

}

public interface IPlayer
{
    void Shoot();
    void Dash();
    void MarkArea();
}

#endregion

#region Functions for Abilities
public interface IAbilities
{
    void RunAbilities();
    void AbilitiesCoolDown();
    void Animations();
    void Die(bool isDead);
    void PickUp();
}
#endregion