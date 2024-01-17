using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class DeathScreen : MonoBehaviour
{
    [Header("Variables")]
    public GameObject deathScreen;

    public void ShowDeathScreen(Abilities_Player playerAbilitiesRef)
    {
        if(playerAbilitiesRef != null)
        {
            if(playerAbilitiesRef.dead)
            {
                //Show Death Screen
                if(deathScreen != null)
                {
                    deathScreen.SetActive(true);
                }
            }
        }
    }
    // Load the same scene (retry) or main menu scene (quit)
    public void LoadScene(int sceneNumber)
    {
        SceneManager.LoadScene(0);
    }
}
