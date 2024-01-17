using Personality_World;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Personality_World {

    public class TestingScript : MonoBehaviour
    {
        public Block block;
        public float timeLimit = 5f; // Time limit in seconds
        private float currentTime = 0f;
        private bool isTimerRunning = false;

        public string structure;
        public GetMapStructure mapStructure;

        private void Update()
        {
            StartTimer();
            mapStructure.ExtractBlocks();
        }
        // Start the timer
        public void StartTimer()
        {
            if (!isTimerRunning)
            {
                isTimerRunning = true;
                StartCoroutine(DefineBlock());
            }
        }

        // Coroutine for the timer
        private IEnumerator TimerCoroutine()
        {
            currentTime = timeLimit;

            while (currentTime > 0)
            {
                yield return new WaitForSeconds(1f);
                currentTime--;
                Debug.Log("Time remaining: " + currentTime);
            }

            // Timer has finished
            Debug.Log("Timer has finished!");
            if(structure.Length == 22)
                block.GetComponent<IGA_Element>().DefineFeatures(structure);

            isTimerRunning = false;
        }

        IEnumerator DefineBlock()
        {
            currentTime = timeLimit;

            while (currentTime > 0)
            {
                yield return new WaitForSeconds(1f);
                currentTime--;
                Debug.Log("Time remaining: " + currentTime);
            }

            // Timer has finished
            Debug.Log("Timer has finished!");
            int randomIndex = Random.Range(0, mapStructure.MapStructure.Length);
            block.GetComponent<IGA_Element>().DefineFeatures(mapStructure.MapStructure[randomIndex]);

            isTimerRunning = false;
        }

        // Optionally, you can stop the timer prematurely
        public void StopTimer()
        {
            if (isTimerRunning)
            {
                StopAllCoroutines();
                isTimerRunning = false;
                Debug.Log("Timer stopped!");
            }
        }
    }
}
