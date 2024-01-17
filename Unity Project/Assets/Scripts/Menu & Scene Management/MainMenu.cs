using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class MainMenu : MonoBehaviour
{
    [Header("Menu Screens")]
    [SerializeField] private GameObject loadingScreen;
    [SerializeField] private GameObject mainMenu;
    [SerializeField] private bool canPause;
    [SerializeField] private GameObject pauseMenu;

    [SerializeField] LevelManager levelManager;

    [Header("Slider")]
    [SerializeField] private Slider loadingSlider;

    [Header("Player Input")]
    [SerializeField] private PlayerInput playerInput;
    private InputAction pauseAction;

    private void Start()
    {
        // Assign inputs
        if (playerInput != null)
        {
            pauseAction = playerInput.actions["Pause"];
        }
        levelManager = GetComponent<LevelManager>();
    }

    private void Update()
    {
        Pause();
    }
    public void LoadLevelBtn(string levelName)
    {
        if(mainMenu != null)
            mainMenu.SetActive(false);
        if(loadingScreen != null)
            loadingScreen.SetActive(true);

        Time.timeScale = 1f;

        StartCoroutine(LoadLevelAsync(levelName));
    }

    IEnumerator LoadLevelAsync(string levelName)
    {
        AsyncOperation loadOperation = SceneManager.LoadSceneAsync(levelName);

        while(!loadOperation.isDone)
        {
            float progressValue = Mathf.Clamp01(loadOperation.progress / 0.9f);
            loadingSlider.value = progressValue;
            yield return null;
        }
    }

    public void ExitGameBtn()
    {
        Application.Quit();
    }

    void Pause()
    {
        if(playerInput && canPause)
        if (pauseAction.IsPressed())
        {
            Time.timeScale = 0f;
            if(pauseMenu != null)
                pauseMenu.SetActive(true);
            if(levelManager != null)
            {
                levelManager.Scoreboard(true);
            }
        }
    }

    public void Resume()
    {
        Time.timeScale = 1f;
        if (pauseMenu != null)
            pauseMenu.SetActive(false);
        if (levelManager != null)
        {
            levelManager.Scoreboard(false);
        }
    }
}
