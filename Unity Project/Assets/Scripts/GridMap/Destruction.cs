using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(TakeDamage))]
public class Destruction : MonoBehaviour
{
    private void Update()
    {
        if (GetComponent<TakeDamage>().dead) 
        {
            gameObject.SetActive(false);
        }
    }
}
