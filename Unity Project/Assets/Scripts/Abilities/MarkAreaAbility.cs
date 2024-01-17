using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MarkAreaAbility : MonoBehaviour
{
    [Header("Ability")]
    public string abilityName = "MarkArea";
    public float coolDownTime = 5f;
    public float sizeMultiplier = 1f;

    [Header("Mark Area")]
    public GameObject markUI;

    public void MarkArea()
    {
        if(markUI != null)
        {
            GameObject markedArea = Instantiate(markUI,new Vector3(transform.position.x,markUI.transform.position.y,transform.position.z), Quaternion.identity);
            markedArea.transform.localScale *= sizeMultiplier; 
        }
    }
}
