using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MouseRaycast : MonoBehaviour
{
    [Header("Parameters")]
    public float raycastDistance = 100f;
    
    // Testing
    public Vector3 hitPos = new();

    private void Update()
    {
        hitPos = GetMousePos();
    }

    public Vector3 GetMousePos()
    {
        Vector3 pos = new();
        // Cast a ray from the mouse pointer
        Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
        RaycastHit hit;

        if (Physics.Raycast(ray, out hit, raycastDistance))
        {
            // Check if the ray hit a GameObject
            GameObject hitObject = hit.collider.gameObject;
            Debug.DrawLine(ray.origin, hit.point, Color.red, 1.0f);

            // Add your custom logic here based on the hit object, e.g., object selection, interaction, etc.
            pos = new Vector3(hit.point.x,hit.point.y,hit.point.z);
        }

        return pos;
        
    }
}
