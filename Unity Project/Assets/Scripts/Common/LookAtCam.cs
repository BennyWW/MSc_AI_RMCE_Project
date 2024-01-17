using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LookAtCam : MonoBehaviour
{
    [Header("Variables")]
    public Camera cam;

    // Update is called once per frame
    void Update()
    {
       LookAtCamera();
    }

    void LookAtCamera()
    {
        cam = Camera.main;
        transform.LookAt(cam.transform.position);
    }
}

