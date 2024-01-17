import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Create the main application window
root = tk.Tk()
root.title("Big Five Personality Test")

# Initialize variables to store user responses
responses = {
    "Openness": tk.StringVar(),
    "Conscientiousness": tk.StringVar(),
    "Extraversion": tk.StringVar(),
    "Agreeableness": tk.StringVar(),
    "Neuroticism": tk.StringVar()
}

# Create a frame for the personality test content
personality_frame = ttk.Frame(root)
personality_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

# Create a canvas for the personality test content
canvas = tk.Canvas(personality_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Add a scrollbar to the canvas
scrollbar = ttk.Scrollbar(personality_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame to contain the questions and response widgets
test_content = ttk.Frame(canvas)
canvas.create_window((0, 0), window=test_content, anchor=tk.NW)

# Questions for each personality trait
questions = {
    "Openness": [
        "I enjoy trying new things and exploring new ideas.",
        "I prefer routine and familiar activities.",
        "I like to think deeply and contemplate life's mysteries.",
        "I tend to stick to my established habits and routines.",
        "I am open to unconventional ideas and concepts."
    ],
    "Conscientiousness": [
        "I am organized and like to plan ahead.",
        "I tend to be spontaneous and go with the flow.",
        "I pay attention to details and strive for perfection.",
        "I often misplace or forget things.",
        "I am diligent and work hard to achieve my goals."
    ],
    "Extraversion": [
        "I am outgoing and enjoy socializing with others.",
        "I prefer spending time alone or with a few close friends.",
        "I feel energized in social settings and like to be the center of attention.",
        "I find large social gatherings overwhelming and exhausting.",
        "I am talkative and enjoy expressing my thoughts and feelings."
    ],
    "Agreeableness": [
        "I am compassionate and considerate of others' feelings.",
        "I am competitive and prioritize my own interests.",
        "I am quick to forgive and hold no grudges.",
        "I can be argumentative and confrontational.",
        "I enjoy helping others and being a team player."
    ],
    "Neuroticism": [
        "I am emotionally stable and rarely get upset.",
        "I am prone to anxiety and worry about the future.",
        "I tend to be calm and composed even in stressful situations.",
        "I experience mood swings and emotional ups and downs.",
        "I am easily disturbed and upset by unpleasant events."
    ]
}


# Function to submit the personality test
def submit_personality_test():
    # Calculate and display the personality traits based on user responses
    results = []
    for trait, response_var in responses.items():
        score = response_var.get()
        results.append(f"{trait}: {score}")

    personality_summary = "\n".join(results)
    messagebox.showinfo("Personality Test Results", personality_summary)


# Create a label for each question and radio buttons for responses
row = 0
for trait, question_list in questions.items():
    ttk.Label(test_content, text=f"{trait} Trait:").grid(row=row, column=0, sticky="w", padx=10, pady=5)
    row += 1
    for i, question in enumerate(question_list):
        ttk.Label(test_content, text=f"{i + 1}. {question}").grid(row=row, column=0, columnspan=2, sticky="w", padx=10)
        ttk.Radiobutton(test_content, text="Strongly Disagree", variable=question, value=str(1)).grid(row=row,
                                                                                             column=2)
        ttk.Radiobutton(test_content, text="Disagree", variable=question, value=str(2)).grid(row=row, column=3)
        ttk.Radiobutton(test_content, text="Neutral", variable=question, value=str(3)).grid(row=row, column=4)
        ttk.Radiobutton(test_content, text="Agree", variable=question, value=str(4)).grid(row=row, column=5)
        ttk.Radiobutton(test_content, text="Strongly Agree", variable=question, value=str(5)).grid(row=row,
                                                                                                           column=6)
        row += 1

# Submit Button
submit_button = ttk.Button(test_content, text="Submit", command=submit_personality_test)
submit_button.grid(row=row, column=0, columnspan=7, pady=10)

# Update the canvas scroll region
test_content.update_idletasks()
canvas.configure(scrollregion=canvas.bbox("all"))

# Start the Tkinter main loop
root.mainloop()
