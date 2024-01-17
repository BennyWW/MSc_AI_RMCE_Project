using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;

public class Movement_Player : MonoBehaviour
{
    [Header("Player Input")]
    [SerializeField]private PlayerInput playerInput;
    private InputAction moveAction;

    [Header("Character Controller")]
    [SerializeField] CharacterController characterController;

    [Header("Movement Characteristics")]
    public float moveSpeed = 5f;
    public float playerHeight = 0.2f;
    public float gravity = 10f;

    // Start is called before the first frame update
    void Start()
    {
        //Initialize character controller
        characterController = GetComponent<CharacterController>();

        // Assign inputs
        playerInput = GetComponent<PlayerInput>();
        moveAction = playerInput.actions["Move"];
    }

    // Update is called once per frame
    void Update()
    {
        Movement();
    }

    #region Movement Script
    void Movement()
    {
        // Get the horizontal and vertical inputs
        Vector2 input = moveAction.ReadValue<Vector2>();
        float horizontalInput = moveAction.ReadValue<Vector2>().x;
        float verticalInput = moveAction.ReadValue<Vector2>().y;


        // Calculate the movement direction
        Vector3 moveDirection = transform.forward * verticalInput;
        moveDirection += transform.right * horizontalInput;
        moveDirection = moveDirection.normalized;

        if (characterController.isGrounded)
        {
            // Reset the vertical velocity if the character is on the ground
            moveDirection.y = -0.5f;
        }
        else
        {
            // Apply gravity to the vertical velocity
            moveDirection.y -= gravity * Time.deltaTime;
        }

        // Apply movement with the Character Controller
        transform.position = new Vector3(transform.position.x, playerHeight, transform.position.z);
        characterController.Move(moveDirection * moveSpeed * Time.deltaTime);

    }
    #endregion
}
