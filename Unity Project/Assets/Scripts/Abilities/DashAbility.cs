using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;

public class DashAbility : MonoBehaviour
{
    [Header("Ability")]
    public string abilityName = "Dash";
    public float coolDownTime = 2f;

    [Header("Dash Settings")]
    [SerializeField] public float distance;
    [SerializeField] public float speed;
    [SerializeField] public float duration;
    public Vector3 direction;

    public void Dash(bool MovementEnabled, CharacterController characterController)
    {
        StartCoroutine(DashCoroutine(MovementEnabled, characterController));
        
    }

    IEnumerator DashCoroutine(bool MovementEnabled, CharacterController characterController)
    {
        MovementEnabled = false;

        // Save the starting position of the dash
        Vector3 startPosition = transform.position;
        float dashTimer = 0f;

        while (dashTimer < duration)
        {
            // Calculate the dash distance covered during this frame
            float dashDistanceThisFrame = distance * Time.deltaTime / duration;

            // Move the character in the dash direction
            characterController.Move(direction * dashDistanceThisFrame);

            dashTimer += Time.deltaTime;
            yield return null;
        }

        MovementEnabled = true;
    }

}
